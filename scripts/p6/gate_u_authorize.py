#!/usr/bin/env python3
"""Write Gate U authorization (validation seal; no test)."""

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
    out = seed_card(args.seed) / "gate-u-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "U",
        "seed": args.seed,
        "authorized": True,
        "authorizes_test": False,
        "scope": (
            f"12-cell validation BPB matrix + lockboxed topology contrasts for seed {args.seed}; "
            "seal hashes only; no restricted test"
        ),
        "must_not": ["print BPB", "run Gate V", "unblind", "pod stop", "test access"],
        "host_class": "NVIDIA CUDA (A40 class)",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: Do Gate U to V",
        "note": "Does not authorize V/X, unblinding, or pod stop by itself; V needs same chat auth.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "seed": args.seed, "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
