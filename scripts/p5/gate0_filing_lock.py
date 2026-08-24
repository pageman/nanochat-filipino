#!/usr/bin/env python3
"""P5 Gate 0 filing lock: verify filed PDF/plan hashes and mint run-card receipt."""

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    ADDENDUM,
    ASPREDICTED_ID,
    ASPREDICTED_URL,
    BASE,
    FILED_ADDENDUM_SHA,
    FILED_GATE_PLAN_SHA,
    FILED_PDF_SHA,
    GATE_PLAN,
    LOCK_PATH,
    LOCKBOX,
    P5_RUN_ID,
    PDF,
    PIN,
    RESEARCHBOX_ID,
    RUN_CARD,
    SAFE,
    PANEL_SEEDS,
    blinded_print,
    mark_ledger,
    seed_lockbox_dirs,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-0-filing-lock.json"


def no_p5_outcomes() -> bool:
    bad = []
    for pat in ("val_bpb", "test_bpb", "gate-v-test", "gate-u-status", "p5-validation-seal"):
        for p in BASE.rglob("*") if BASE.is_dir() else []:
            if pat in p.name.lower() and p.is_file():
                bad.append(str(p.relative_to(BASE)))
    for s in PANEL_SEEDS:
        for p in (LOCKBOX / f"seed-{s}").rglob("*.pt") if (LOCKBOX / f"seed-{s}").is_dir() else []:
            bad.append(str(p))
    return bad == []


def main() -> int:
    os.environ.setdefault("NANOCHAT_FILIPINO_ROOT", str(Path(__file__).resolve().parents[2]))
    RUN_CARD.mkdir(parents=True, exist_ok=True)
    seed_lockbox_dirs()

    pdf_sha = sha256_file(PDF)
    plan_sha = sha256_file(GATE_PLAN) if GATE_PLAN.is_file() else None
    addendum_sha = sha256_file(ADDENDUM) if ADDENDUM.is_file() else None
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    checks = [
        {"id": "0_pdf_sha", "ok": pdf_sha == FILED_PDF_SHA, "detail": pdf_sha},
        {"id": "0_gate_plan_sha", "ok": plan_sha == FILED_GATE_PLAN_SHA, "detail": plan_sha},
        {
            "id": "0_lock_pdf_binding",
            "ok": lock.get("aspredicted_pdf_sha256") == FILED_PDF_SHA,
            "detail": lock.get("aspredicted_pdf_sha256"),
        },
        {
            "id": "0_lock_plan_binding",
            "ok": lock.get("gate_plan_sha256") == FILED_GATE_PLAN_SHA,
            "detail": lock.get("gate_plan_sha256"),
        },
        {
            "id": "0_lock_addendum_binding",
            "ok": lock.get("addendum_sha256") == FILED_ADDENDUM_SHA,
            "detail": lock.get("addendum_sha256"),
        },
        {
            "id": "0_panel_lockbox_dirs",
            "ok": all((LOCKBOX / f"seed-{s}").is_dir() for s in PANEL_SEEDS),
            "detail": [f"seed-{s}" for s in PANEL_SEEDS],
        },
        {
            "id": "0_lockbox_mode",
            "ok": stat.S_IMODE(LOCKBOX.stat().st_mode) != stat.S_IMODE(SAFE.stat().st_mode),
            "detail": {
                "lockbox": oct(stat.S_IMODE(LOCKBOX.stat().st_mode)),
                "safe": oct(stat.S_IMODE(SAFE.stat().st_mode)),
            },
        },
        {"id": "0_no_p5_outcomes", "ok": no_p5_outcomes(), "detail": "scan cache/lockbox"},
    ]
    addendum_matches = addendum_sha == FILED_ADDENDUM_SHA
    payload = {
        "gate": "0",
        "status": "pass" if all(c["ok"] for c in checks) else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p5_run_id": P5_RUN_ID,
        "aspredicted_id": ASPREDICTED_ID,
        "aspredicted_url": ASPREDICTED_URL,
        "aspredicted_pdf_local": str(PDF.relative_to(Path(__file__).resolve().parents[2])),
        "aspredicted_pdf_sha256": pdf_sha,
        "gate_plan_path": str(GATE_PLAN.relative_to(Path(__file__).resolve().parents[2])),
        "gate_plan_sha256": plan_sha,
        "addendum_path": str(ADDENDUM.relative_to(Path(__file__).resolve().parents[2])),
        "addendum_filed_sha256": FILED_ADDENDUM_SHA,
        "addendum_local_sha256": addendum_sha,
        "addendum_local_matches_filed": addendum_matches,
        "addendum_note": (
            "PDF+LOCK bind the filed addendum SHA; working draft may drift post-filing."
            if not addendum_matches
            else "local addendum matches filed SHA"
        ),
        "nanochat_pin": PIN,
        "does_not_amend_306780": True,
        "does_not_amend_306935": True,
        "does_not_amend_307342": True,
        "does_not_amend_307591": True,
        "designed_after_p4_gate_x": True,
        "panel_seeds": list(PANEL_SEEDS),
        "researchbox_id": RESEARCHBOX_ID,
        "checks": checks,
        "no_p5_outcomes": True,
        "next": "gate-0-lockbox-tests then Gate A (already passed if backfill)",
    }
    write_json(OUT, payload)
    if payload["status"] == "pass":
        update_lock_gate("0", "pass", {"status": "gate_0_pass"})
        mark_ledger("0", "pass", str(OUT.relative_to(Path(__file__).resolve().parents[2])), "A")
    blinded_print("0", payload["status"], {"path": str(OUT.relative_to(Path(__file__).resolve().parents[2]))})
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
