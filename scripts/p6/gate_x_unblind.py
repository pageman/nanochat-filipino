#!/usr/bin/env python3
"""P6-M Gate X: one unblinding. Primary = topology contrasts vs M-fine. No P5 recurrence table as primary. No mean/CI/p."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    CHILD_ARMS,
    DELTA,
    LOCK_PATH,
    P6_RUN_ID,
    PANEL_SEEDS,
    POLICY_A_TEST_ARM,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TOPOLOGY_ARMS,
    mark_ledger,
    require_auth,
    seed_box,
    seed_card,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

PREFLIGHT = RUN_CARD / "gate-x-preflight.json"
EVENT = RUN_CARD / "P6_UNBLINDING_EVENT.json"
GATE0_X_SHA = "c6b69ea0500daddd20b0fea140dc8b8899accf5080226a9b6dccec1a3f8a726b"
THIS = Path(__file__).resolve()


def cell(box: Path, arm: str, lang: str) -> float:
    return float(json.loads((box / f"{arm}_{lang}_val_bpb_full.json").read_text())["val_bpb_full"])


def direction(delta: float) -> str:
    # Lower BPB is better. Negative Delta vs M-fine means the arm is better than M-fine.
    if delta <= -DELTA:
        return "better_than_m_fine_by_delta"
    if delta >= DELTA:
        return "worse_than_m_fine_by_delta"
    return "within_delta"


def main() -> int:
    require_auth(RUN_CARD / "gate-x-authorization.json", "X")
    if EVENT.is_file():
        raise SystemExit("P6_UNBLINDING_EVENT.json already exists; refuse second unblinding")
    pre = json.loads(PREFLIGHT.read_text())
    if not pre.get("ready_for_unblinding"):
        raise SystemExit("preflight not ready")
    running_sha = sha256_file(THIS)
    deviation = {
        "gate0_pinned_gate_x_unblind_sha256": GATE0_X_SHA,
        "executed_gate_x_unblind_sha256": running_sha,
        "hash_match": running_sha == GATE0_X_SHA,
        "reason": (
            "Gate 0 pinned a P5-rename unblind script that reads c3_* cells and emits a "
            "recurrence count table. Filed P6-M primary analysis is 12-cell topology "
            "contrasts vs M-fine (addendum + gate plan). Gate U wrote topology-named cells. "
            "Authority order: filed analysis over the Gate 0 P5-rename script hash."
        ),
        "p5_recurrence_not_primary": True,
    }

    released = BASE / "released"
    released.mkdir(parents=True, exist_ok=True)
    seeds_out = {}
    for s in PANEL_SEEDS:
        box = seed_box(s)
        cells = {f"{arm}_{lang}": cell(box, arm, lang) for arm in CHILD_ARMS for lang in ("en", "tl")}
        cells["c0_en"] = float(json.loads((box / "c0_en_val_bpb_full.json").read_text())["val_bpb_full"])
        fine_tl = cells[f"{POLICY_A_TEST_ARM}_tl"]
        fine_en = cells[f"{POLICY_A_TEST_ARM}_en"]
        c2_tl = cells["c2_tl"]
        c1_en = cells["c1_en"]
        delta_vs_fine = {}
        for tau in TOPOLOGY_ARMS:
            if tau == POLICY_A_TEST_ARM:
                continue
            d_tl = cells[f"{tau}_tl"] - fine_tl
            d_en = cells[f"{tau}_en"] - fine_en
            delta_vs_fine[tau] = {
                "Delta_TL": d_tl,
                "Delta_EN": d_en,
                "Delta_TL_class": direction(d_tl),
                "Delta_EN_class": direction(d_en),
            }
        contextual = {}
        for tau in TOPOLOGY_ARMS:
            r_tl = cells[f"{tau}_tl"] - c2_tl
            a_en = cells[f"{tau}_en"] - c1_en
            contextual[tau] = {"R_TL": r_tl, "A_EN": a_en}
        # Verify lockboxed U contrasts if present
        u_path = box / f"p6-s{s}-topology-contrasts.json"
        u_match = None
        if u_path.is_file():
            u = json.loads(u_path.read_text())
            u_match = True
            for tau, row in delta_vs_fine.items():
                locked = u["delta_vs_m_fine"][tau]
                if abs(locked["Delta_TL"] - row["Delta_TL"]) > 1e-12 or abs(locked["Delta_EN"] - row["Delta_EN"]) > 1e-12:
                    u_match = False
        secondary_test = None
        test_summary = box / f"gate-v-s{s}-test.json"
        if test_summary.is_file():
            ts = json.loads(test_summary.read_text())
            secondary_test = {
                "arm": ts.get("arm"),
                "component_evaluations": ts.get("component_evaluations"),
                "excluded_from_topology": True,
                "events": [
                    {"component": e["component"], "bpb": e["bpb"]}
                    for e in ts.get("events", [])
                ],
            }
        seeds_out[str(s)] = {
            "status": "eligible",
            "cells_val_bpb_full": cells,
            "delta_vs_m_fine": delta_vs_fine,
            "contextual": contextual,
            "delta": DELTA,
            "u_contrasts_match": u_match,
            "secondary_m_fine_test": secondary_test,
        }
        write_json(released / f"p6-s{s}-released-contrasts.json", seeds_out[str(s)])
        # Copy seal hash only companion
        seal = box / f"p6-s{s}-validation-seal.json"
        if seal.is_file():
            shutil.copy2(seal, released / seal.name)

    at = utc_now()
    event = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "p6_run_id": P6_RUN_ID,
        "event": "P6_UNBLINDING",
        "gate": "X",
        "at_utc": at,
        "delta": DELTA,
        "primary": "topology_contrasts_Delta_TL_Delta_EN_vs_m_fine",
        "contextual": "R_TL vs C2; A_EN vs C1",
        "no_mean": True,
        "no_ci": True,
        "no_pvalue": True,
        "no_p5_recurrence_primary": True,
        "does_not_confirm_p4": True,
        "does_not_confirm_p5": True,
        "one_seed": True,
        "eligible_n": len(PANEL_SEEDS),
        "seeds": seeds_out,
        "script_deviation": deviation,
        "preflight_sha256": sha256_file(PREFLIGHT),
    }
    write_json(EVENT, event)
    write_json(
        RUN_CARD / "gate-x-unblind.json",
        {
            "gate": "X",
            "status": "pass",
            "at_utc": at,
            "event": str(EVENT.relative_to(ROOT)),
            "primary": event["primary"],
            "script_hash_match_gate0": deviation["hash_match"],
            "next_gate": "W",
        },
    )
    lock = json.loads(LOCK_PATH.read_text())
    lock["panel_unblinded"] = True
    lock["outcome_access_count"] = int(lock.get("outcome_access_count") or 0) + 1
    write_json(LOCK_PATH, lock)
    update_lock_gate("X", "pass", {"status": "gate_x_unblinded"})
    mark_ledger("X", "pass", str(EVENT.relative_to(ROOT)), "W")
    # Safe console: structure only plus that values were written; print the actual
    # released JSON path so W can insert without chat transcription.
    print(
        json.dumps(
            {
                "gate": "X",
                "status": "pass",
                "event": str(EVENT.relative_to(ROOT)),
                "released": str((released / "p6-s4-released-contrasts.json").relative_to(ROOT)),
                "script_hash_match_gate0": deviation["hash_match"],
                "next_gate": "W",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
