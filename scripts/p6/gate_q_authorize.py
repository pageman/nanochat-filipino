#!/usr/bin/env python3
"""Write Gate Q authorization (C0 freeze only; filed parent seed)."""

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
    out = seed_card(args.seed) / "gate-q-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "Q",
        "seed": args.seed,
        "authorized": True,
        "authorizes_children": False,
        "scope": f"freeze eligible TL0 d20 as immutable C0 for seed {args.seed}; zero additional train tokens",
        "must_not": [
            "train",
            "print BPB",
            "start R/S/T children",
            "amend parent seed",
            "load_optimizer=True",
        ],
        "host_class": "CPU ok (file freeze); CUDA host optional for path parity",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: do Gate Q (freeze C0)",
        "note": "Does not authorize children, validation seal, test, unblinding, or pod stop.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "seed": args.seed, "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
