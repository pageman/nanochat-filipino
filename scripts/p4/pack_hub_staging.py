#!/usr/bin/env python3
"""Stage C0+C1+C2+C3 + tokenizer for Hub upload. Refuses a partial inventory."""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data/cache/p4-20260821T060032Z-92d63d4"
HUB_DOCS = ROOT / "docs/hub/p4-token-share-mix"
STAGING = ROOT / "transfer/p4-hub-pageman-nanochat-filipino-p4-token-share-mix"

WEIGHTS = {
    "c0/p4-c0-tl-d20-model_000294.pt": (
        CACHE / "c0/frozen/p4-c0-tl-d20/model_000294.pt",
        "34e069646be4158979809c023691188439047d6cbee08a141db432c78bcf02e2",
    ),
    "c1/p4-c1-tl-d20-model_000294.pt": (
        CACHE / "base_checkpoints/p4-c1-tl-d20/model_000294.pt",
        "87b9f55146de72dd6ae53598b9aea8d99079ff0f9492b7f9ea4fdce550664c55",
    ),
    "c2/p4-c2-en-d20-model_000294.pt": (
        CACHE / "base_checkpoints/p4-c2-en-d20/model_000294.pt",
        "0787aed0f13a0ab3ec144baf6802b144a18412780a2d00a64ca7adcb67a4a375",
    ),
    "c3/p4-c3-mix-d20-model_000294.pt": (
        CACHE / "base_checkpoints/p4-c3-mix-d20/model_000294.pt",
        "eef9a4e11c4840ac036d42c3bf4d87a2139ea1fa5809e1c756df2770fe0609f3",
    ),
    "tokenizer.pkl": (
        CACHE / "tokenizer/tokenizer.pkl",
        "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8",
    ),
    "token_bytes.pt": (
        CACHE / "tokenizer/token_bytes.pt",
        "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132",
    ),
}

DOC_SKIP = {".DS_Store"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def link_or_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def main() -> int:
    missing = [str(src) for src, _ in WEIGHTS.values() if not src.is_file()]
    if missing:
        print("hub staging refuses incomplete inventory:", *missing, sep="\n", file=sys.stderr)
        return 2
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    shutil.copytree(HUB_DOCS, STAGING, dirs_exist_ok=True, ignore=shutil.ignore_patterns(*DOC_SKIP))
    for rel, (src, expect) in WEIGHTS.items():
        got = sha256(src)
        if got != expect:
            print(f"hash mismatch {rel}: {got} != {expect}", file=sys.stderr)
            return 3
        link_or_copy(src, STAGING / rel)
    print(STAGING)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
