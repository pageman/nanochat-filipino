#!/usr/bin/env python3
"""P3 contrast/seal script. Refuses until six child val JSON + B0 EN descriptive exist.

Does not print BPB to stdout. Writes seal JSON to lockbox when complete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

CHILD = [
    "b1_en_val_bpb_full.json",
    "b1_tl_val_bpb_full.json",
    "b2_en_val_bpb_full.json",
    "b2_tl_val_bpb_full.json",
    "b3_en_val_bpb_full.json",
    "b3_tl_val_bpb_full.json",
]
B0_EN = "b0_en_val_bpb_full.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lockbox", required=True)
    p.add_argument("--safe-progress", required=True)
    args = p.parse_args()
    lockbox = Path(args.lockbox)
    safe = Path(args.safe_progress)
    missing = [n for n in CHILD + [B0_EN] if not (lockbox / n).exists()]
    if missing:
        print("contrast refused: incomplete inventory", file=sys.stderr)
        return 2
    cells = {n: _load(lockbox / n) for n in CHILD}
    b0 = _load(lockbox / B0_EN)
    c_tl = cells["b2_tl_val_bpb_full.json"]["val_bpb_full"] - cells["b1_tl_val_bpb_full.json"]["val_bpb_full"]
    g_en = cells["b2_en_val_bpb_full.json"]["val_bpb_full"] - cells["b1_en_val_bpb_full.json"]["val_bpb_full"]
    c_tl_b3 = cells["b3_tl_val_bpb_full.json"]["val_bpb_full"] - cells["b1_tl_val_bpb_full.json"]["val_bpb_full"]
    g_en_b3 = cells["b3_en_val_bpb_full.json"]["val_bpb_full"] - cells["b1_en_val_bpb_full.json"]["val_bpb_full"]
    seal = {
        "six_child_cells": True,
        "b0_en_descriptive": True,
        "b0_en_excluded_from_contrasts": True,
        "C_tl": c_tl,
        "G_en": g_en,
        "C_tl_B3": c_tl_b3,
        "G_en_B3": g_en_b3,
        "not_mitigation": True,
        "test_access": 0,
        "b0_en_val_bpb_full": b0["val_bpb_full"],
    }
    out = lockbox / "p3-validation-seal.json"
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
                "P3_test_access": 0,
                "seal_sha256": digest,
            },
            indent=2,
        )
        + "\n"
    )
    print("seven Gate U val outputs complete (six child + B0 EN descriptive); validation seal created; P3 test access = 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
