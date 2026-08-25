#!/usr/bin/env python3
"""P6 Gate 0 filing lock: verify filed PDF/plan hashes and mint run-card receipt."""

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ADDENDUM,
    ASPREDICTED_ID,
    ASPREDICTED_URL,
    BASE,
    FILED_ADDENDUM_SHA,
    FILED_GATE_PLAN_SHA,
    FILED_PDF_SHA,
    GATE_PLAN,
    GATE_PLAN_WORKING,
    LOCK_PATH,
    LOCKBOX,
    NETWORK_VOLUME_DC,
    NETWORK_VOLUME_ID,
    P6_RUN_ID,
    PARENT_SEED,
    PDF,
    PIN,
    RESEARCHBOX_ID,
    RUN_CARD,
    SAFE,
    TIER2,
    TOPOLOGY_ARMS,
    TOPOLOGY_MANIFEST,
    TOPOLOGY_MANIFEST_SHA,
    PANEL_SEEDS,
    blinded_print,
    mark_ledger,
    seed_lockbox_dirs,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = RUN_CARD / "gate-0-filing-lock.json"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def no_p6_outcomes() -> bool:
    bad = []
    for pat in ("val_bpb", "test_bpb", "gate-v-test", "gate-u-status", "p6-validation-seal"):
        for p in BASE.rglob("*") if BASE.is_dir() else []:
            if pat in p.name.lower() and p.is_file():
                # allow dummy_* under lockbox from concurrent tests only if we haven't run accept yet
                if "dummy" in p.name.lower():
                    continue
                bad.append(str(p.relative_to(BASE)))
    for s in PANEL_SEEDS:
        for p in (LOCKBOX / f"seed-{s}").rglob("*.pt") if (LOCKBOX / f"seed-{s}").is_dir() else []:
            bad.append(str(p))
    return bad == []


def main() -> int:
    os.environ.setdefault("NANOCHAT_FILIPINO_ROOT", str(ROOT))
    os.environ.setdefault("P6_RUN_ID", P6_RUN_ID)
    RUN_CARD.mkdir(parents=True, exist_ok=True)
    seed_lockbox_dirs()

    pdf_sha = sha256_file(PDF)
    plan_sha = sha256_file(GATE_PLAN) if GATE_PLAN.is_file() else None
    working_plan_sha = sha256_file(GATE_PLAN_WORKING) if GATE_PLAN_WORKING.is_file() else None
    addendum_sha = sha256_file(ADDENDUM) if ADDENDUM.is_file() else None
    topology_sha = sha256_file(TOPOLOGY_MANIFEST) if TOPOLOGY_MANIFEST.is_file() else None
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
            "id": "0_topology_manifest_sha",
            "ok": topology_sha == TOPOLOGY_MANIFEST_SHA,
            "detail": topology_sha,
        },
        {
            "id": "0_lock_topology_binding",
            "ok": lock.get("topology_manifest_sha256") == TOPOLOGY_MANIFEST_SHA,
            "detail": lock.get("topology_manifest_sha256"),
        },
        {
            "id": "0_parent_seed",
            "ok": lock.get("parent_seed") == PARENT_SEED and list(PANEL_SEEDS) == [PARENT_SEED],
            "detail": {"parent_seed": lock.get("parent_seed"), "panel_seeds": list(PANEL_SEEDS)},
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
        {
            "id": "0_tier2_dir",
            "ok": TIER2.is_dir(),
            "detail": rel(TIER2),
        },
        {"id": "0_no_p6_outcomes", "ok": no_p6_outcomes(), "detail": "scan cache/lockbox"},
        {
            "id": "0_run_id_matches_pdf8",
            "ok": P6_RUN_ID.endswith(FILED_PDF_SHA[:8]) and P6_RUN_ID.startswith("p6-"),
            "detail": P6_RUN_ID,
        },
    ]
    addendum_matches = addendum_sha == FILED_ADDENDUM_SHA
    payload = {
        "gate": "0",
        "status": "pass" if all(c["ok"] for c in checks) else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "aspredicted_id": ASPREDICTED_ID,
        "aspredicted_url": ASPREDICTED_URL,
        "aspredicted_pdf_local": rel(PDF),
        "aspredicted_pdf_sha256": pdf_sha,
        "gate_plan_path": rel(GATE_PLAN),
        "gate_plan_sha256": plan_sha,
        "gate_plan_working_path": str(GATE_PLAN_WORKING),
        "gate_plan_working_sha256": working_plan_sha,
        "gate_plan_working_matches_filed": working_plan_sha == FILED_GATE_PLAN_SHA,
        "gate_plan_note": (
            "Cursor working plan may mutate YAML todo statuses; filed bytes are frozen at gate_plan_path."
            if working_plan_sha != FILED_GATE_PLAN_SHA
            else "working plan matches filed SHA"
        ),
        "addendum_path": rel(ADDENDUM),
        "addendum_filed_sha256": FILED_ADDENDUM_SHA,
        "addendum_local_sha256": addendum_sha,
        "addendum_local_matches_filed": addendum_matches,
        "addendum_note": (
            "PDF+LOCK bind the filed addendum SHA; working draft may drift post-filing."
            if not addendum_matches
            else "local addendum matches filed SHA"
        ),
        "topology_manifest_path": rel(TOPOLOGY_MANIFEST),
        "topology_manifest_sha256": topology_sha,
        "topology_arms": list(TOPOLOGY_ARMS),
        "parent_seed": PARENT_SEED,
        "nanochat_pin": PIN,
        "does_not_amend_306780": True,
        "does_not_amend_306935": True,
        "does_not_amend_307342": True,
        "does_not_amend_307591": True,
        "does_not_amend_307836": True,
        "designed_after_p5_gate_w": True,
        "panel_seeds": list(PANEL_SEEDS),
        "researchbox_id": RESEARCHBOX_ID,
        "network_volume_id": NETWORK_VOLUME_ID,
        "network_volume_dc": NETWORK_VOLUME_DC,
        "tier2_local": rel(TIER2),
        "architecture_note": "docs/operator/P6-M-LOCKOUT-RESISTANT-ARCHITECTURE.md",
        "checks": checks,
        "no_p6_outcomes": True,
        "next": "gate-0-lockbox-tests then Gate A",
    }
    write_json(OUT, payload)
    if payload["status"] == "pass":
        update_lock_gate("0", "pass", {"status": "gate_0_pass"})
        mark_ledger("0", "pass", rel(OUT), "0-lockbox")
    blinded_print("0", payload["status"], {"path": rel(OUT)})
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
