#!/usr/bin/env python3
"""Write Gate X authorization (one formal unblinding)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import ASPREDICTED_ID, P6_RUN_ID, PANEL_SEEDS, ROOT, utc_now, write_json  # noqa: E402

RUN_CARD = ROOT / "docs" / "run-cards" / "p6" / P6_RUN_ID


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    args = ap.parse_args()
    if args.seed not in PANEL_SEEDS:
        raise SystemExit(f"seed must be one of {PANEL_SEEDS}")
    out = RUN_CARD / "gate-x-authorization.json"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "X",
        "seed": args.seed,
        "authorized": True,
        "authorizes_unblind": True,
        "authorizes_w": True,
        "scope": "one Gate X unblinding of sealed validation contrasts; then Gate W archive/paper; Hub/ResearchBox/git push remain deferred unless separately executed",
        "must_not": ["second unblinding", "amend filing", "upload Hub without staging", "push public git without W3 check"],
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: Do Gate W to X",
        "note": "Filed order is X then W. Primary analysis is topology contrasts, not P5 recurrence counts.",
    }
    write_json(out, payload)
    print(json.dumps({"status": "authorized", "path": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
