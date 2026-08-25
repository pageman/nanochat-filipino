#!/usr/bin/env python3
"""Write Gate I_s authorization (one seed only)."""

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
    out = seed_card(args.seed) / "gate-i-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "I",
        "seed": args.seed,
        "authorized": True,
        "authorizes_children": False,
        "authorizes_other_seeds": False,
        "authorizes_p0t": False,
        "scope": f"fresh Tagalog TL0 d8 then d20; parent-init seed {args.seed} only; tag p6-s{args.seed}-tl0-d{{8,20}}",
        "must_not": [
            "p6-s0-*",
            "p4-c0-*",
            "print BPB",
            "Mac MPS",
            "start other seeds",
            "P0-T",
            "children",
        ],
        "host_class": "NVIDIA CUDA A40",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: do Gate I",
        "note": "Does not authorize P0-T, Q, children, test access, unblinding, or pod stop.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "seed": args.seed, "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
