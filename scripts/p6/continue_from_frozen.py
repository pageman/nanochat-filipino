#!/usr/bin/env python3
"""P6 continuation from frozen C0: parent weights only, fresh optimizer."""

from __future__ import annotations

import argparse
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256  # noqa: E402
from p6_common import CHILD_ARMS, N_PHASE2, N_TL0, WARMUP, child_tag, c0_tag, sha256_file  # noqa: E402


def parse_wrapper(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-from", required=True)
    parser.add_argument("--init-step", type=int, default=N_TL0)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--allowed-model-tag", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_known_args(argv)


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
    parts = set(init_dir.parts)
    expected_c0 = c0_tag(wrapper.seed)
    if "c0" not in parts or "frozen" not in parts or expected_c0 not in parts:
        raise SystemExit(f"init-from must be frozen C0 directory for seed {wrapper.seed}, got {init_dir}")
    if wrapper.init_step != N_TL0:
        raise SystemExit(f"init-step must be {N_TL0}")
    reject_parent_sha256(wrapper.expected_sha)
    if wrapper.expected_sha in FORBIDDEN_PARENT_SHA256:
        raise SystemExit("refusing forbidden parent SHA")

    model_path = init_dir / f"model_{wrapper.init_step:06d}.pt"
    if not model_path.is_file():
        raise SystemExit(f"missing frozen parent: {model_path}")
    actual = sha256_file(model_path)
    if actual != wrapper.expected_sha:
        raise SystemExit(f"C0 SHA mismatch: {actual} != {wrapper.expected_sha}")

    if _has_flag(rest, "--resume-from-step"):
        resume = _arg_value(rest, "--resume-from-step")
        if resume not in (None, "-1"):
            raise SystemExit("--resume-from-step loads optimizer; forbidden for P6 children")
    if _arg_value(rest, "--num-iterations") != str(N_PHASE2):
        raise SystemExit(f"--num-iterations must be {N_PHASE2}")
    tag = _arg_value(rest, "--model-tag")
    if tag != wrapper.allowed_model_tag:
        raise SystemExit(f"--model-tag must be {wrapper.allowed_model_tag}, got {tag!r}")
    allowed = {child_tag(wrapper.seed, a) for a in CHILD_ARMS}
    if tag not in allowed:
        raise SystemExit(f"refusing model tag {tag}")
    if _arg_value(rest, "--warmup-steps") != str(WARMUP):
        raise SystemExit(f"--warmup-steps must be {WARMUP}")
    if _arg_value(rest, "--depth") != "20":
        raise SystemExit("child depth must be 20")

    base = Path(os.environ["NANOCHAT_BASE_DIR"])
    out_dir = base / "base_checkpoints" / tag
    frozen_root = (base / f"p6-s{wrapper.seed}" / "c0" / "frozen").resolve()
    if out_dir == frozen_root or frozen_root in out_dir.parents or out_dir == init_dir.resolve():
        raise SystemExit("refusing to write inside c0/frozen/")
    if out_dir.exists() and any(out_dir.glob("model_*.pt")):
        raise SystemExit(f"output directory already has checkpoints: {out_dir}")
    return model_path


def install_weight_loader(init_dir: Path, init_step: int, expected_sha: str) -> None:
    from nanochat.checkpoint_manager import load_checkpoint
    from nanochat.gpt import GPT

    orig = GPT.init_weights

    def init_then_load_frozen(self):
        orig(self)
        device = self.transformer.wte.weight.device
        model_data, optimizer_data, _meta = load_checkpoint(
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
            f"P6 continue_from_frozen: loaded C0 step {init_step} sha256={parent_sha} optimizer=fresh",
            flush=True,
        )

    GPT.init_weights = init_then_load_frozen


def main() -> None:
    wrapper, rest = parse_wrapper(sys.argv[1:])
    if rest[:1] == ["--"]:
        rest = rest[1:]
    model_path = validate(wrapper, rest)
    print(f"P6 continue_from_frozen: parent_ok {model_path}", flush=True)
    if wrapper.validate_only:
        print("validate-only OK", flush=True)
        return
    sys.path.insert(0, str(VENDOR))
    os.chdir(VENDOR)
    install_weight_loader(Path(wrapper.init_from).resolve(), wrapper.init_step, wrapper.expected_sha)
    sys.argv = ["scripts/base_train.py", *rest]
    runpy.run_path(str(VENDOR / "scripts" / "base_train.py"), run_name="__main__")


if __name__ == "__main__":
    main()
