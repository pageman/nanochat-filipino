#!/usr/bin/env python3
"""Write Gate T authorization (four topology arms from frozen C0; filed parent seed)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import ASPREDICTED_ID, P6_RUN_ID, PANEL_SEEDS, ROOT, TOPOLOGY_ARMS, seed_card, utc_now, write_json  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()
    if args.seed not in PANEL_SEEDS:
        raise SystemExit(f"seed must be one of {PANEL_SEEDS}")
    out = seed_card(args.seed) / "gate-t-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "T",
        "seed": args.seed,
        "arms": list(TOPOLOGY_ARMS),
        "authorized": True,
        "authorizes_validation": False,
        "scope": (
            f"train topology arms {list(TOPOLOGY_ARMS)} serially from frozen C0 for seed {args.seed}; "
            "exact phase-two budget; load_optimizer=False"
        ),
        "must_not": [
            "print BPB",
            "start Gate U validation",
            "resume with optimizer state",
            "amend parent seed",
            "use sibling as parent",
            "test access",
            "unblind",
            "pod stop",
        ],
        "host_class": "NVIDIA CUDA (A40 class)",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: Do Gate T",
        "note": "Does not authorize U/V, test, unblinding, or pod stop.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "seed": args.seed, "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
