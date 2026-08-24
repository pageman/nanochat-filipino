#!/usr/bin/env python3
"""Write Gate I_s authorization (one seed only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import ASPREDICTED_ID, P5_RUN_ID, PANEL_SEEDS, ROOT, seed_card, utc_now, write_json  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()
    if args.seed not in PANEL_SEEDS:
        raise SystemExit("seed must be 1, 2, or 3")
    out = seed_card(args.seed) / "gate-i-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED",
        "aspredicted_id": ASPREDICTED_ID,
        "p5_run_id": P5_RUN_ID,
        "gate": "I",
        "seed": args.seed,
        "authorized": True,
        "authorizes_children": False,
        "authorizes_other_seeds": False,
        "scope": f"fresh Tagalog TL0 d8 then d20; parent-init seed {args.seed} only; tag p5-s{args.seed}-tl0-d{{8,20}}",
        "must_not": [
            "p5-s0-*",
            "p4-c0-*",
            "print BPB",
            "Mac MPS",
            "start next seed",
        ],
        "host_class": "NVIDIA CUDA A40",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: Gates I to X",
        "note": f"Does not authorize P0-T, Q, children, or seed {args.seed + 1 if args.seed < 3 else 'X'}.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "seed": args.seed, "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
