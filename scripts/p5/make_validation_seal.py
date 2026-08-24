#!/usr/bin/env python3
"""P4 contrast/seal. Refuses until six child val JSON + C0 EN descriptive exist.

Writes R_TL / A_EN only into lockbox. Safe progress has counts/hashes, not BPB.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

CHILD = [
    "c1_en_val_bpb_full.json",
    "c1_tl_val_bpb_full.json",
    "c2_en_val_bpb_full.json",
    "c2_tl_val_bpb_full.json",
    "c3_en_val_bpb_full.json",
    "c3_tl_val_bpb_full.json",
]
C0_EN = "c0_en_val_bpb_full.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lockbox", required=True)
    p.add_argument("--safe-progress", required=True)
    args = p.parse_args()
    lockbox = Path(args.lockbox)
    safe = Path(args.safe_progress)
    missing = [n for n in CHILD + [C0_EN] if not (lockbox / n).exists()]
    if missing:
        print("contrast refused: incomplete inventory", file=sys.stderr)
        return 2
    cells = {n: _load(lockbox / n) for n in CHILD}
    c0 = _load(lockbox / C0_EN)
    r_tl = cells["c3_tl_val_bpb_full.json"]["val_bpb_full"] - cells["c2_tl_val_bpb_full.json"]["val_bpb_full"]
    a_en = cells["c3_en_val_bpb_full.json"]["val_bpb_full"] - cells["c1_en_val_bpb_full.json"]["val_bpb_full"]
    seal = {
        "six_child_cells": True,
        "c0_en_descriptive": True,
        "c0_en_excluded_from_contrasts": True,
        "R_TL": r_tl,
        "A_EN": a_en,
        "not_mitigation": True,
        "c3_is_not_p3_b3": True,
        "test_access": 0,
        "c0_en_val_bpb_full": c0["val_bpb_full"],
    }
    out = lockbox / "p4-validation-seal.json"
    blob = json.dumps(seal, indent=2, sort_keys=True).encode()
    out.write_bytes(blob)
    os.chmod(out, 0o600)
    digest = hashlib.sha256(blob).hexdigest()
    safe.mkdir(parents=True, exist_ok=True)
    (safe / "gate-u-status.json").write_text(
        json.dumps(
            {
                "seven_Gate_U_val_outputs_complete": True,
                "validation_seal_created": True,
                "P4_test_access": 0,
                "seal_sha256": digest,
            },
            indent=2,
        )
        + "\n"
    )
    print("seven Gate U val outputs complete (six child + C0 EN descriptive); validation seal created; P4 test access = 0")
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
