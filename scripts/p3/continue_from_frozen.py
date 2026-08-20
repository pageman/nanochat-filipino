#!/usr/bin/env python3
"""P3 continuation from frozen B0: parent weights only, fresh optimizer."""

from __future__ import annotations

import argparse
import hashlib
import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"

from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256  # noqa: E402
from phase2_common import B0_SHA256, B0_STEP, B0_TAG, N_PHASE2, WARMUP  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_wrapper(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-from", required=True)
    parser.add_argument("--init-step", type=int, default=B0_STEP)
    parser.add_argument("--expected-sha", default=B0_SHA256)
    parser.add_argument("--allowed-model-tag", required=True)
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
    if B0_TAG not in init_dir.parts or "frozen" not in init_dir.parts or "b0" not in init_dir.parts:
        raise SystemExit(f"init-from must be frozen B0 directory, got {init_dir}")
    if wrapper.init_step != B0_STEP:
        raise SystemExit(f"init-step must be {B0_STEP}")
    reject_parent_sha256(wrapper.expected_sha)
    if wrapper.expected_sha != B0_SHA256:
        raise SystemExit("expected-sha is not Gate Q B0 SHA-256")

    model_path = init_dir / f"model_{wrapper.init_step:06d}.pt"
    if not model_path.is_file():
        raise SystemExit(f"missing frozen parent: {model_path}")
    actual = sha256_file(model_path)
    if actual != wrapper.expected_sha:
        raise SystemExit(f"B0 SHA mismatch: {actual} != {wrapper.expected_sha}")
    if actual in FORBIDDEN_PARENT_SHA256:
        raise SystemExit("refusing forbidden parent SHA")

    if _has_flag(rest, "--resume-from-step"):
        resume = _arg_value(rest, "--resume-from-step")
        if resume not in (None, "-1"):
            raise SystemExit("--resume-from-step loads optimizer; forbidden for P3 children")
    if _arg_value(rest, "--num-iterations") != str(N_PHASE2):
        raise SystemExit(f"--num-iterations must be {N_PHASE2}")
    tag = _arg_value(rest, "--model-tag")
    if tag != wrapper.allowed_model_tag:
        raise SystemExit(f"--model-tag must be {wrapper.allowed_model_tag}, got {tag!r}")
    if tag == B0_TAG:
        raise SystemExit("refusing to write into B0 tag")
    if _arg_value(rest, "--warmup-steps") != str(WARMUP):
        raise SystemExit(f"--warmup-steps must be {WARMUP}")
    if _arg_value(rest, "--depth") != "20":
        raise SystemExit("child depth must be 20")

    base = Path(os.environ["NANOCHAT_BASE_DIR"])
    out_dir = base / "base_checkpoints" / tag
    frozen_root = (base / "b0" / "frozen").resolve()
    if out_dir == frozen_root or frozen_root in out_dir.parents or out_dir == init_dir.resolve():
        raise SystemExit("refusing to write inside b0/frozen/")
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"output directory must be empty: {out_dir}")
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
            f"P3 continue_from_frozen: loaded B0 step {init_step} sha256={parent_sha} optimizer=fresh",
            flush=True,
        )

    GPT.init_weights = init_then_load_frozen


def main() -> None:
    wrapper, rest = parse_wrapper(sys.argv[1:])
    if rest[:1] == ["--"]:
        rest = rest[1:]
    model_path = validate(wrapper, rest)
    print(f"P3 continue_from_frozen: parent_ok {model_path}", flush=True)
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
