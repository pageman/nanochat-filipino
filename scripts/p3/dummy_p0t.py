#!/usr/bin/env python3
"""Dummy P0-T: lockbox holds scalars; stdout/safe is PASS/BLOCKED only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lockbox", required=True)
    p.add_argument("--safe-progress", required=True)
    p.add_argument("--status", choices=["PASS", "BLOCKED"], default="PASS")
    args = p.parse_args()
    lockbox = Path(args.lockbox)
    safe = Path(args.safe_progress)
    lockbox.mkdir(parents=True, exist_ok=True)
    safe.mkdir(parents=True, exist_ok=True)
    scalars = {
        "d8_tl_val_bpb_full": 1.111111,
        "d20_tl_val_bpb_full": 1.222222,
        "untrained_d8": 3.0,
        "untrained_d20": 3.0,
        "byte_unigram": 2.5,
        "status": args.status,
    }
    (lockbox / "gate-p0-t-eligibility.json").write_text(json.dumps(scalars, indent=2) + "\n")
    (safe / "gate-p0-t-status.json").write_text(json.dumps({"P0-T": args.status}) + "\n")
    print(f"P0-T: {args.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
