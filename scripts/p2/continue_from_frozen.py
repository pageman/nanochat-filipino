#!/usr/bin/env python3
"""P2 continuation from frozen A0: parent weights only, fresh optimizer.

Pinned nanochat ``scripts.base_train`` has no ``--load``. Its
``--resume-from-step`` path sets ``load_optimizer=True``, which is forbidden
for A1/A2/A3 (fresh Muon/Adam; no EN0 or sibling optimizer state).

This P2-only wrapper does not edit vendor files. It:

1. Verifies the frozen parent SHA-256 and refuses a mutable EN0 tag as the
   sole parent reference.
2. Monkey-patches ``GPT.init_weights`` so A0 weights replace random init.
3. Execs pin ``scripts/base_train.py`` with ``--resume-from-step`` unset so
   the pin creates a new optimizer and starts at step 0.
4. Writes checkpoints only under ``base_checkpoints/<model-tag>/``.

Never write into ``a0/frozen/``. Never load P1.1 ``model_000294.pt``.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
A0_SHA256 = "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d"
A0_STEP = 5415
A0_TAG = "p2-en0-d20"
P11_FORBIDDEN_SHA256 = "9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_wrapper(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description="Load frozen A0 weights, then run pin base_train with a fresh optimizer.",
    )
    parser.add_argument("--init-from", required=True, help="Frozen A0 checkpoint directory (read-only).")
    parser.add_argument("--init-step", type=int, default=A0_STEP)
    parser.add_argument("--expected-sha", default=A0_SHA256)
    parser.add_argument("--allowed-model-tag", default="p2-a1-extra-en-d20")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Hash parent, check argv and output isolation, then exit. Does not build a model or train.",
    )
    args, rest = parser.parse_known_args(argv)
    if rest[:1] == ["--"]:
        rest = rest[1:]
    return args, rest


def _arg_value(rest: list[str], flag: str) -> str | None:
    prefix = flag + "="
    for i, tok in enumerate(rest):
        if tok == flag and i + 1 < len(rest):
            return rest[i + 1]
        if tok.startswith(prefix):
            return tok[len(prefix) :]
    return None


def _has_flag(rest: list[str], flag: str) -> bool:
    return flag in rest or any(t.startswith(flag + "=") for t in rest)


def validate(wrapper: argparse.Namespace, rest: list[str]) -> Path:
    init_dir = Path(wrapper.init_from).resolve()
    if A0_TAG not in init_dir.parts or "frozen" not in init_dir.parts or "a0" not in init_dir.parts:
        raise SystemExit(f"init-from must be the frozen A0 directory, got {init_dir}")
    if wrapper.init_step != A0_STEP:
        raise SystemExit(f"init-step must be {A0_STEP}, got {wrapper.init_step}")
    if wrapper.expected_sha != A0_SHA256:
        raise SystemExit("expected-sha is not the Gate Q / LOCK A0 d20 SHA-256")

    model_path = init_dir / f"model_{wrapper.init_step:06d}.pt"
    if not model_path.is_file():
        raise SystemExit(f"missing frozen parent: {model_path}")
    actual = sha256_file(model_path)
    if actual != wrapper.expected_sha:
        raise SystemExit(f"A0 SHA mismatch: {actual} != {wrapper.expected_sha}")
    if actual == P11_FORBIDDEN_SHA256:
        raise SystemExit("refusing P1.1 model_000294.pt SHA")

    if _has_flag(rest, "--resume-from-step"):
        resume = _arg_value(rest, "--resume-from-step")
        if resume not in (None, "-1"):
            raise SystemExit("--resume-from-step loads optimizer state; forbidden for P2 children")
    if _arg_value(rest, "--target-param-data-ratio") == "-1":
        raise SystemExit("refusing --target-param-data-ratio=-1")
    n_iter = _arg_value(rest, "--num-iterations")
    if n_iter != "294":
        raise SystemExit(f"--num-iterations must be 294, got {n_iter!r}")
    tag = _arg_value(rest, "--model-tag")
    if tag != wrapper.allowed_model_tag:
        raise SystemExit(f"--model-tag must be {wrapper.allowed_model_tag}, got {tag!r}")
    if tag == A0_TAG:
        raise SystemExit("refusing to write into the EN0 / A0 tag")
    warmup = _arg_value(rest, "--warmup-steps")
    if warmup != "14":
        raise SystemExit(f"--warmup-steps must be 14, got {warmup!r}")
    if _arg_value(rest, "--max-seq-len") != "2048":
        raise SystemExit("T must be 2048")
    if _arg_value(rest, "--total-batch-size") != "65536":
        raise SystemExit("total batch size must be 65536")
    if _arg_value(rest, "--depth") != "20":
        raise SystemExit("child depth must be 20")
    if _arg_value(rest, "--core-metric-every") != "-1":
        raise SystemExit("--core-metric-every must be -1")

    base = os.environ.get("NANOCHAT_BASE_DIR")
    if not base:
        raise SystemExit("NANOCHAT_BASE_DIR must be set")
    base_path = Path(base).resolve()
    out_dir = base_path / "base_checkpoints" / tag
    frozen_root = (base_path / "a0" / "frozen").resolve()
    if out_dir == frozen_root or frozen_root in out_dir.parents or out_dir == init_dir.resolve():
        raise SystemExit("refusing to write inside a0/frozen/ or onto the parent checkpoint directory")
    if out_dir.exists():
        contents = list(out_dir.iterdir())
        if contents:
            raise SystemExit(f"output directory must be absent or empty, found {len(contents)} entries in {out_dir}")
        print(f"P2 continue_from_frozen: output dir exists and is empty {out_dir}", flush=True)
    else:
        print(f"P2 continue_from_frozen: output dir absent (will be created by pin save) {out_dir}", flush=True)
    return model_path


def install_weight_loader(init_dir: Path, init_step: int, expected_sha: str) -> None:
    from nanochat.checkpoint_manager import load_checkpoint
    from nanochat.gpt import GPT

    orig_init_weights = GPT.init_weights

    def init_then_load_frozen(self):
        orig_init_weights(self)
        device = self.transformer.wte.weight.device
        model_data, optimizer_data, meta_data = load_checkpoint(
            str(init_dir), init_step, device, load_optimizer=False, rank=0
        )
        if optimizer_data is not None:
            raise SystemExit("load_optimizer=False returned optimizer state")
        model_data = {k.removeprefix("_orig_mod."): v for k, v in model_data.items()}
        self.load_state_dict(model_data, strict=True, assign=True)
        parent_sha = sha256_file(init_dir / f"model_{init_step:06d}.pt")
        if parent_sha != expected_sha:
            raise SystemExit("parent SHA changed between preflight and load")
        print(
            f"P2 continue_from_frozen: loaded A0 step {init_step} from {init_dir} "
            f"sha256={parent_sha} extra_train_tokens_on_parent=0 optimizer=fresh",
            flush=True,
        )
        print(
            f"P2 continue_from_frozen: parent_meta_step={meta_data.get('step')} "
            f"(ignored for child step counter)",
            flush=True,
        )

    GPT.init_weights = init_then_load_frozen


def main() -> None:
    wrapper, rest = parse_wrapper(sys.argv[1:])
    model_path = validate(wrapper, rest)
    print(f"P2 continue_from_frozen: parent_ok {model_path} sha256={wrapper.expected_sha}", flush=True)
    print(
        "P2 continue_from_frozen: load_optimizer=False; child step starts at 0; "
        "--init-step is parent provenance only; pin creates a fresh optimizer",
        flush=True,
    )
    print(f"P2 continue_from_frozen: pin argv: {rest}", flush=True)

    if wrapper.validate_only:
        print("P2 continue_from_frozen: validate-only; not importing GPT, not creating optimizer, not training", flush=True)
        return

    if not (VENDOR / "scripts" / "base_train.py").is_file():
        raise SystemExit(f"missing pin trainer: {VENDOR / 'scripts' / 'base_train.py'}")
    sys.path.insert(0, str(VENDOR))
    os.chdir(VENDOR)
    os.environ["WANDB_MODE"] = os.environ.get("WANDB_MODE", "disabled")

    install_weight_loader(Path(wrapper.init_from).resolve(), wrapper.init_step, wrapper.expected_sha)
    sys.argv = ["scripts/base_train.py", *rest]
    runpy.run_path(str(VENDOR / "scripts" / "base_train.py"), run_name="__main__")


if __name__ == "__main__":
    main()
