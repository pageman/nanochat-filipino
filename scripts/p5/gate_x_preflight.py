#!/usr/bin/env python3
"""P5 Gate X preflight: hashes/counters only. No BPB printed."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    LOCK_PATH,
    PANEL_SEEDS,
    ROOT,
    RUN_CARD,
    seed_box,
    seed_card,
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-x-preflight.json"


def main() -> int:
    lock = json.loads(LOCK_PATH.read_text())
    checks = []

    def rec(cid, ok, detail=None):
        checks.append({"check": cid, "status": "PASS" if ok else "FAIL", "detail": detail})

    rec("outcome_access_zero", lock.get("outcome_access_count", 1) == 0, lock.get("outcome_access_count"))
    rec("panel_not_yet_unblinded", lock.get("panel_unblinded") is False)
    terminals = {}
    for s in PANEL_SEEDS:
        v = seed_card(s) / "gate-v-test.json"
        inelig = seed_card(s) / "ineligible_parent.json"
        v_ok = v.is_file() and json.loads(v.read_text()).get("status") == "pass"
        terminals[s] = "V" if v_ok else ("ineligible_parent" if inelig.is_file() else "incomplete")
        rec(f"seed_{s}_terminal", terminals[s] != "incomplete", terminals[s])
        if v_ok:
            rec(f"seed_{s}_test_access_1", lock.get("test_access_count", {}).get(str(s)) == 1)
            rec(f"seed_{s}_seal_exists", (seed_box(s) / f"p5-s{s}-validation-seal.json").is_file())
            rec(f"seed_{s}_no_seed_level_x", not (seed_card(s) / "P5_UNBLINDING_EVENT.json").is_file())
    ready = all(c["status"] == "PASS" for c in checks)
    write_json(
        OUT,
        {
            "gate": "X-preflight",
            "ready_for_unblinding": ready,
            "at_utc": utc_now(),
            "terminals": terminals,
            "checks": checks,
            "blinded": True,
            "no_bpb_printed": True,
        },
    )
    print(json.dumps({"ready_for_unblinding": ready, "failed": [c["check"] for c in checks if c["status"] != "PASS"], "path": str(OUT.relative_to(ROOT)), "blinded": True}, indent=2))
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
