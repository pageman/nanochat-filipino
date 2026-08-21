#!/usr/bin/env python3
"""P4 parent-SHA reject list. Confirmatory P4 MUST NOT load these files.

This is not a renamed scripts/p3/forbidden_parents.py: it also rejects every
P3 Hub checkpoint and refuses P1/P2/P3 cache paths.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_PARENT_SHA256 = {
    # P1.1 d20
    "9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38",
    # P2 A0 EN0 d20
    "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d",
    # P3 Hub pageman/nanochat-filipino-p3-tl-then-en
    "ae621be2c90a3d295f8d21b0e53cb9d4b717803f5d5337fa68f3c3f84d57193c",  # B0 d20
    "3f98784bf6e6bdf78785f370140a0db2dd170a848f93897d75c88b44740e2c54",  # B1
    "5ee34b20f6601b1753ee6338b5447e091964ddd1087ca66c57434011e6341cc1",  # B2
    "521bea166f13a8eee57fef1ac381aa4f715037a3f3f60a85c74c05e02b55ae2d",  # B3
    # P3 local d8 parent (eligibility ckpt; still not a P4 parent)
    "feaf7017cd55fab48a8acf9087b9f444b015167c7725c0d695278c20dbf462e2",
}

_FORBIDDEN_PATH_MARKERS = (
    "/data/cache/p1-",
    "/data/cache/p2-",
    "/data/cache/p3-",
    "/artifacts/p1/",
    "/artifacts/p2/",
    "/artifacts/p3/",
    "nanochat-filipino-p1",
    "nanochat-filipino-p2",
    "nanochat-filipino-p3",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def reject_parent_sha256(sha256: str) -> None:
    digest = sha256.lower().strip()
    if digest in FORBIDDEN_PARENT_SHA256:
        raise SystemExit(f"P4 forbids P1.1/P2/P3 parent SHA256 {digest}")


def reject_parent_path(path: str | Path) -> None:
    text = str(path).replace("\\", "/")
    if any(m in text for m in _FORBIDDEN_PATH_MARKERS):
        raise SystemExit(f"P4 forbids parent path from a prior study cache: {path}")
    p = Path(path)
    if p.is_file() and p.suffix == ".pt":
        reject_parent_sha256(sha256_file(p))


def scan_local_prior_checkpoints() -> dict[str, str]:
    """Hash model_*.pt under prior-study caches if present. Slow; Gate 0/A only."""
    found: dict[str, str] = {}
    roots = [
        ROOT / "data" / "cache",
        ROOT / "artifacts",
    ]
    for base in roots:
        if not base.exists():
            continue
        for p in base.rglob("model_*.pt"):
            rel = str(p)
            if not any(m in rel.replace("\\", "/") for m in ("/p1", "/p2", "/p3", "p1-", "p2-", "p3-")):
                continue
            digest = sha256_file(p)
            found[rel] = digest
            FORBIDDEN_PARENT_SHA256.add(digest)
    return found


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
