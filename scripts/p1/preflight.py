#!/usr/bin/env python3
"""P1.1 preflight: ledger status and (later) artifact checks.

Exits nonzero if a required condition fails. JSON is written to stdout.
A green message is not the artifact; the JSON and exit status are.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = ROOT / "manifests" / "gate_ledger.json"
TEST_ACCESS_PATH = ROOT / "manifests" / "test_access_log.json"
NOTE_PATH = ROOT / "docs" / "EXECUTION-CLARIFICATIONS-p1.1.md"
REQUIRED_GATES = ("A", "B", "C", "D", "E", "F", "G", "H")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="P1.1 preflight ledger check")
    parser.add_argument(
        "--require-pre-i",
        action="store_true",
        help="Fail unless gates A-H all have status pass",
    )
    parser.add_argument(
        "--check-apparatus",
        action="store_true",
        help="Check Gate I manifests and run cards without requiring official Gate H",
    )
    args = parser.parse_args()

    checks = []
    failed = False

    def record(name: str, ok: bool, detail: str) -> None:
        nonlocal failed
        checks.append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            failed = True

    if not LEDGER_PATH.is_file():
        record("ledger_exists", False, f"missing {LEDGER_PATH}")
        payload = {"ok": False, "checks": checks}
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 1

    ledger = load_json(LEDGER_PATH)
    gates = {g["id"]: g for g in ledger.get("gates", [])}
    statuses = {gid: gates.get(gid, {}).get("status") for gid in REQUIRED_GATES}
    record(
        "ledger_schema_gates",
        all(gid in gates for gid in REQUIRED_GATES),
        json.dumps(statuses, sort_keys=True),
    )

    outcomes = ledger.get("confirmatory_outcomes", {})
    record(
        "no_confirmatory_test_yet",
        outcomes.get("test_bpb_computed") is False
        and outcomes.get("test_read_events", 0) == 0,
        json.dumps(outcomes, sort_keys=True),
    )

    if TEST_ACCESS_PATH.is_file():
        access = load_json(TEST_ACCESS_PATH)
        record(
            "test_test_access_zero",
            access.get("test_read_events", 0) == 0
            and len(access.get("events", [])) == 0,
            f"test_read_events={access.get('test_read_events')}",
        )
    else:
        record("test_access_log_exists", False, f"missing {TEST_ACCESS_PATH}")

    note_hash = ledger.get("clarification_note", {}).get("sha256")
    if NOTE_PATH.is_file() and note_hash:
        import hashlib

        actual = hashlib.sha256(NOTE_PATH.read_bytes()).hexdigest()
        record(
            "clarification_note_hash",
            actual == note_hash,
            f"expected={note_hash} actual={actual}",
        )

    if args.require_pre_i:
        all_pass = all(statuses.get(gid) == "pass" for gid in REQUIRED_GATES)
        record("gates_a_h_pass", all_pass, json.dumps(statuses, sort_keys=True))

    if args.check_apparatus:
        budget_path = ROOT / "manifests" / "budget_manifest.json"
        matrix_path = ROOT / "manifests" / "gate_i_run_matrix.json"
        if budget_path.is_file():
            budget = load_json(budget_path)
            depths = [row.get("depth") for row in budget.get("depths", [])]
            record(
                "budget_four_depths",
                depths == [8, 12, 16, 20]
                and all(row.get("target_param_data_ratio", 0) > 0 for row in budget.get("depths", []))
                and budget.get("sequence_length") == 2048
                and budget.get("num_iterations") == 294,
                f"depths={depths} B={budget.get('common_total_batch_size')} N={budget.get('num_iterations')}",
            )
        else:
            record("budget_exists", False, str(budget_path))
        if matrix_path.is_file():
            matrix = load_json(matrix_path)
            cards = [ROOT / run["run_card"] for run in matrix.get("runs", [])]
            record(
                "gate_i_cards_exist",
                len(cards) == 4 and all(p.is_file() for p in cards),
                ",".join(run.get("run_name", "") for run in matrix.get("runs", [])),
            )
            record(
                "gate_i_not_started",
                matrix.get("official_gate_i_started") is False,
                f"official_gate_i_started={matrix.get('official_gate_i_started')}",
            )
        else:
            record("gate_i_matrix_exists", False, str(matrix_path))
        host = load_json(ROOT / "manifests" / "execution_host.json")
        record(
            "gpu_host_still_unnamed",
            host.get("gpu_host_for_H_I") is None,
            f"gpu_host_for_H_I={host.get('gpu_host_for_H_I')}",
        )

    payload = {
        "ok": not failed,
        "require_pre_i": args.require_pre_i,
        "check_apparatus": args.check_apparatus,
        "gate_statuses": statuses,
        "checks": checks,
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
