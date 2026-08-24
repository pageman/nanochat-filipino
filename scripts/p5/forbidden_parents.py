#!/usr/bin/env python3
"""P5 parent-SHA reject list. Confirmatory P5 MUST NOT load prior-study weights."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import FORBIDDEN_P4_PARENT_SHA256  # noqa: E402

FORBIDDEN_PARENT_SHA256 = {
    "9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38",
    "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d",
    "ae621be2c90a3d295f8d21b0e53cb9d4b717803f5d5337fa68f3c3f84d57193c",
    "3f98784bf6e6bdf78785f370140a0db2dd170a848f93897d75c88b44740e2c54",
    "5ee34b20f6601b1753ee6338b5447e091964ddd1087ca66c57434011e6341cc1",
    "521bea166f13a8eee57fef1ac381aa4f715037a3f3f60a85c74c05e02b55ae2d",
    "feaf7017cd55fab48a8acf9087b9f444b015167c7725c0d695278c20dbf462e2",
}
FORBIDDEN_PARENT_SHA256.update(FORBIDDEN_P4_PARENT_SHA256)

_FORBIDDEN_PATH_MARKERS = (
    "/data/cache/p1-",
    "/data/cache/p2-",
    "/data/cache/p3-",
    "/data/cache/p4-",
    "nanochat-filipino-p1",
    "nanochat-filipino-p2",
    "nanochat-filipino-p3",
    "nanochat-filipino-p4",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def reject_parent_sha256(digest: str) -> None:
    d = digest.lower().strip()
    if d in FORBIDDEN_PARENT_SHA256:
        raise SystemExit(f"P5 forbids prior-study parent SHA256 {d}")


def reject_parent_path(path: str | Path) -> None:
    text = str(path).replace("\\", "/")
    if any(m in text for m in _FORBIDDEN_PATH_MARKERS):
        raise SystemExit(f"P5 forbids parent path from a prior study cache: {path}")
    p = Path(path)
    if p.is_file() and p.suffix == ".pt":
        reject_parent_sha256(sha256_file(p))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: forbidden_parents.py <sha256-or-path>", file=sys.stderr)
        return 2
    arg = sys.argv[1]
    if Path(arg).exists():
        reject_parent_path(arg)
    else:
        reject_parent_sha256(arg)
    print("not a forbidden parent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
