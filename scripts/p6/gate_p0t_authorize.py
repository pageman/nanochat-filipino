#!/usr/bin/env python3
"""Write Gate P0-T authorization (filed parent seed only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import ASPREDICTED_ID, P6_RUN_ID, PANEL_SEEDS, ROOT, seed_card, utc_now, write_json  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()
    if args.seed not in PANEL_SEEDS:
        raise SystemExit(f"seed must be one of {PANEL_SEEDS}")
    out = seed_card(args.seed) / "gate-p0t-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "P0-T",
        "seed": args.seed,
        "authorized": True,
        "authorizes_children": False,
        "authorizes_q": False,
        "authorizes_test": False,
        "scope": f"Tagalog validation eligibility only for seed {args.seed}; scalars lockboxed; safe output PASS/BLOCKED/TECHNICAL BLOCK",
        "must_not": [
            "print BPB scalars outside lockbox",
            "read test split",
            "freeze C0",
            "start children",
            "replace seed",
            "Mac MPS",
        ],
        "host_class": "NVIDIA CUDA A40",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: go Gate P0-T",
        "note": "Does not authorize Q, children, Gate V test, unblinding, public release, or pod stop.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "seed": args.seed, "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
