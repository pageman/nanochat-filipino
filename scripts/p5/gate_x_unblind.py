#!/usr/bin/env python3
"""P5 panel Gate X: one unblinding; per-seed contrasts; count table. No mean/CI/p."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    ASPREDICTED_ID,
    DELTA,
    LOCK_PATH,
    P5_RUN_ID,
    PANEL_SEEDS,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    mark_ledger,
    seed_box,
    seed_card,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

PREFLIGHT = RUN_CARD / "gate-x-preflight.json"
EVENT = RUN_CARD / "P5_UNBLINDING_EVENT.json"


def classify(r_tl: float, a_en: float) -> str:
    r_hit = r_tl <= -DELTA
    a_hit = a_en <= -DELTA
    if r_hit and a_hit:
        return "both"
    if r_hit:
        return "only-R"
    if a_hit:
        return "only-A"
    return "neither"


def main() -> int:
    pre = json.loads(PREFLIGHT.read_text())
    if not pre.get("ready_for_unblinding"):
        raise SystemExit("preflight not ready")
    rows = {}
    counts = {"both": 0, "only-R": 0, "only-A": 0, "neither": 0, "ineligible_parent": 0}
    for s in PANEL_SEEDS:
        inelig = seed_card(s) / "ineligible_parent.json"
        if inelig.is_file():
            rows[str(s)] = {"status": "ineligible_parent", "class": "ineligible_parent"}
            counts["ineligible_parent"] += 1
            continue
        box = seed_box(s)
        cells = {n: json.loads((box / n).read_text())["val_bpb_full"] for n in (
            "c1_en_val_bpb_full.json",
            "c2_tl_val_bpb_full.json",
            "c3_en_val_bpb_full.json",
            "c3_tl_val_bpb_full.json",
        )}
        r_tl = cells["c3_tl_val_bpb_full.json"] - cells["c2_tl_val_bpb_full.json"]
        a_en = cells["c3_en_val_bpb_full.json"] - cells["c1_en_val_bpb_full.json"]
        klass = classify(r_tl, a_en)
        counts[klass] += 1
        rows[str(s)] = {
            "status": "eligible",
            "R_TL": r_tl,
            "A_EN": a_en,
            "class": klass,
            "delta": DELTA,
            "equality_counts": True,
            "cells": cells,
        }
    at = utc_now()
    event = {
        "study_id": "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "p5_run_id": P5_RUN_ID,
        "event": "P5_UNBLINDING",
        "gate": "X",
        "at_utc": at,
        "delta": DELTA,
        "seeds": rows,
        "panel_count_table": counts,
        "eligible_n": sum(1 for r in rows.values() if r["status"] == "eligible"),
        "no_mean": True,
        "no_ci": True,
        "no_pvalue": True,
        "does_not_confirm_p4": True,
        "p4_seed0_not_a_p5_cell": True,
    }
    write_json(EVENT, event)
    write_json(RUN_CARD / "gate-x-unblind.json", {"gate": "X", "status": "pass", "at_utc": at, "event": str(EVENT.relative_to(ROOT)), "panel_count_table": counts, "next_gate": "W"})
    lock = json.loads(LOCK_PATH.read_text())
    lock["panel_unblinded"] = True
    lock["outcome_access_count"] = int(lock.get("outcome_access_count") or 0) + 1
    write_json(LOCK_PATH, lock)
    update_lock_gate("X", "pass", {"status": "gate_x_unblinded"})
    mark_ledger("X", "pass", str(EVENT.relative_to(ROOT)), "W")
    print(json.dumps({"gate": "X", "status": "pass", "panel_count_table": counts, "event": str(EVENT.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
