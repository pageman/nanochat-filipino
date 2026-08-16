#!/usr/bin/env python3
"""Print pre-Gate-A sign-off status. Exit 0 only if ready to start Gate A."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "manifests" / "gate_ledger.json"
HOST = ROOT / "manifests" / "execution_host.json"
PDF = ROOT / "docs" / "run-cards" / "AsPredicted-306780.pdf"
NOTE = ROOT / "docs" / "EXECUTION-CLARIFICATIONS-p1.1.md"
TEST_ACCESS = ROOT / "manifests" / "test_access_log.json"
BUDGET = ROOT / "manifests" / "budget_manifest.json"
TEMPLATE = ROOT / "manifests" / "gate_ledger.template.json"

EXPECTED_NOTE = "71c2b992ef1771fc7f31cad6d2f259d23d5c3b99367e7b9cbdcf7ae749552c8e"
EXPECTED_PDF = "a34f119df557d2e763aa154e02b76b0ebcbcba1f3fb32c3219d85ae6395cc5ca"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rows = []
    ready = True

    def check(name: str, ok: bool, detail: str) -> None:
        nonlocal ready
        rows.append((name, "pass" if ok else "open", detail))
        if not ok:
            ready = False

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    host = json.loads(HOST.read_text(encoding="utf-8"))
    access = json.loads(TEST_ACCESS.read_text(encoding="utf-8"))
    budget = json.loads(BUDGET.read_text(encoding="utf-8"))

    pdf_ok = PDF.is_file() and PDF.read_bytes()[:4] == b"%PDF" and sha256(PDF) == EXPECTED_PDF
    check(
        "registration_pdf",
        pdf_ok
        and ledger["registration"].get("registration_pdf_sha256") == EXPECTED_PDF,
        EXPECTED_PDF if pdf_ok else f"missing or wrong file at {PDF}",
    )
    check(
        "execution_note_hash",
        NOTE.is_file() and sha256(NOTE) == EXPECTED_NOTE,
        EXPECTED_NOTE,
    )
    check("ledger_template_present", TEMPLATE.is_file(), str(TEMPLATE.relative_to(ROOT)))
    check(
        "test_access_empty",
        access.get("test_read_events", 0) == 0 and access.get("events") == [],
        "zero test reads",
    )
    check(
        "budget_stub_unfilled",
        budget.get("t_train") is None and budget.get("d_3x") is None,
        "Gate G has not been faked",
    )
    check(
        "no_confirmatory_bpb",
        ledger["confirmatory_outcomes"]["val_bpb_computed"] is False
        and ledger["confirmatory_outcomes"]["test_bpb_computed"] is False,
        "no confirmatory outcomes",
    )
    a_status = next(g["status"] for g in ledger["gates"] if g["id"] == "A")
    check("gate_a_not_started", a_status == "not_started", a_status)
    check(
        "execution_host_named",
        host.get("status") != "pending_operator_decision" and bool(host.get("intended_host")),
        host.get("intended_host") or "operator must name the host",
    )
    check(
        "p_scaling_method",
        True,
        "not required before Gate A; capture from pinned base_train.py during Gate A",
    )

    print("P1.1 pre-Gate-A sign-off")
    print("========================")
    for name, status, detail in rows:
        print(f"{status:4}  {name}: {detail}")
    print()
    if ready:
        print("READY: name a commit/tag, then start Gate A only.")
        return 0
    print("NOT READY: fill the open items, then re-run this script.")
    print("Do not start confirmatory training.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
