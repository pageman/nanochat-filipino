#!/usr/bin/env python3
"""Write Gate V authorization (Policy A M-fine restricted test only)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    P6_RUN_ID,
    PANEL_SEEDS,
    POLICY_A_TEST_ARM,
    ROOT,
    seed_card,
    utc_now,
    write_json,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()
    if args.seed not in PANEL_SEEDS:
        raise SystemExit(f"seed must be one of {PANEL_SEEDS}")
    out = seed_card(args.seed) / "gate-v-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "V",
        "seed": args.seed,
        "arm": POLICY_A_TEST_ARM,
        "authorized": True,
        "authorizes_unblind": False,
        "scope": (
            f"exactly one restricted-test event for {POLICY_A_TEST_ARM} (EN+TL components) "
            f"after Gate U seal for seed {args.seed}; secondary; excluded from topology"
        ),
        "must_not": [
            "test C0/C1/C2/m-coarse/m-blocked/m-rand",
            "print BPB",
            "unblind",
            "pod stop",
            "repeat test",
        ],
        "host_class": "NVIDIA CUDA (A40 class)",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: Do Gate U to V",
        "note": "Does not authorize Gate X unblinding or pod stop.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "seed": args.seed, "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
