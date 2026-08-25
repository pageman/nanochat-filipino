#!/usr/bin/env python3
"""Gate X-style release. Refuses incomplete inventory. Writes hashes only."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REQUIRED = [
    "p4-validation-seal.json",
    "gate-v-test.json",
    "c1_en_val_bpb_full.json",
    "c1_tl_val_bpb_full.json",
    "c2_en_val_bpb_full.json",
    "c2_tl_val_bpb_full.json",
    "c3_en_val_bpb_full.json",
    "c3_tl_val_bpb_full.json",
    "c0_en_val_bpb_full.json",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lockbox", required=True)
    p.add_argument("--released", required=True)
    args = p.parse_args()
    lockbox = Path(args.lockbox)
    missing = [n for n in REQUIRED if not (lockbox / n).exists()]
    if missing:
        print("release refuses incomplete inventory", file=sys.stderr)
        return 2
    released = Path(args.released)
    released.mkdir(parents=True, exist_ok=True)
    manifest = {n: sha256(lockbox / n) for n in REQUIRED}
    (released / "released_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print("release complete; hashes only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
