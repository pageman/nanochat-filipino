#!/usr/bin/env python3
"""Gate P0-T accept: lockbox scalars -> safe PASS/BLOCKED/TECHNICAL BLOCK only."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    DELTA,
    LOCKBOX,
    LOCK_PATH,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    SAFE,
    sha256_bytes,
    utc_now,
    write_json,
    mark_ledger,
)

OUT = RUN_CARD / "gate-p0-t.json"
DETAIL = LOCKBOX / "gate-p0-t-eval-detail.json"
ELIG = LOCKBOX / "gate-p0-t-eligibility.json"
SAFE_STATUS = SAFE / "gate-p0-t-status.json"
LOCK_LOG = LOCKBOX / "gate-p0-t-eval-full.log"
P0_T_MARGIN = DELTA


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-exit-code", type=int, default=0)
    args = ap.parse_args()

    technical = args.eval_exit_code not in {0, 1} and not DETAIL.is_file()
    if args.eval_exit_code not in {0, 1} and DETAIL.is_file():
        technical = False
    if args.eval_exit_code not in {0, 1} and not DETAIL.is_file():
        technical = True
    if args.eval_exit_code == 0 and not DETAIL.is_file():
        technical = True

    status = "TECHNICAL BLOCK"
    depths_safe = {}
    lockbox_sha = None

    if technical or not DETAIL.is_file():
        status = "TECHNICAL BLOCK"
        safe_payload = {"P0-T": status}
    else:
        detail = json.loads(DETAIL.read_text(encoding="utf-8"))
        status = detail.get("automated_status", "BLOCKED")
        if status not in {"PASS", "BLOCKED"}:
            status = "BLOCKED"

        eligibility = {
            "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
            "aspredicted_id": ASPREDICTED_ID,
            "researchbox_id": RESEARCHBOX_ID,
            "gate": "P0-T",
            "p4_run_id": P4_RUN_ID,
            "margin_bpb": P0_T_MARGIN,
            "status": status,
            "at_utc": utc_now(),
            "test_read_count": 0,
            "english_val_used": False,
            "byte_unigram_val_bpb": detail.get("byte_unigram_tagalog", {}).get("val_bpb_unigram"),
            "depths": {},
        }
        for d_key, row in detail.get("depths", {}).items():
            eligibility["depths"][d_key] = {
                "depth": row.get("depth"),
                "model_tag": row.get("model_tag"),
                "checkpoint_sha256": row.get("checkpoint_sha256"),
                "val_bpb_full": row.get("val_bpb_full"),
                "untrained_val_bpb": row.get("untrained_val_bpb"),
                "byte_unigram_val_bpb": row.get("byte_unigram_val_bpb"),
                "gap_vs_untrained": row.get("gap_vs_untrained"),
                "gap_vs_unigram": row.get("gap_vs_unigram"),
                "pass_untrained_floor": row.get("pass_untrained_floor"),
                "pass_unigram_floor": row.get("pass_unigram_floor"),
                "pass_both_floors": row.get("pass_both_floors"),
            }
            depths_safe[d_key] = {
                "pass_both_floors": row.get("pass_both_floors"),
                "checkpoint_sha256": row.get("checkpoint_sha256"),
            }

        elig_text = json.dumps(eligibility, indent=2) + "\n"
        ELIG.parent.mkdir(parents=True, exist_ok=True)
        ELIG.write_text(elig_text, encoding="utf-8")
        try:
            ELIG.chmod(0o600)
            if LOCK_LOG.is_file():
                LOCK_LOG.chmod(0o600)
            if DETAIL.is_file():
                DETAIL.chmod(0o600)
        except OSError:
            pass
        lockbox_sha = sha256_bytes(elig_text.encode("utf-8"))
        safe_payload = {"P0-T": status, "lockbox_sha256": lockbox_sha}

    SAFE_STATUS.parent.mkdir(parents=True, exist_ok=True)
    SAFE_STATUS.write_text(json.dumps(safe_payload) + "\n", encoding="utf-8")

    receipt_status = "pass" if status == "PASS" else ("blocked" if status == "BLOCKED" else "technical_block")
    receipt = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "P0-T",
        "status": receipt_status,
        "p0_t_status": status,
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": True,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "script": "scripts/p4/gate_p0t.sh",
        "preflight_script": "scripts/p4/gate_p0t_preflight.py",
        "accept_script": "scripts/p4/gate_p0t_accept.py",
        "eval_script": "scripts/p4/evaluate_bpb.py",
        "margin_bpb": P0_T_MARGIN,
        "depths": depths_safe,
        "test_access": 0,
        "english_val_used": False,
        "lockbox_eligibility": str(ELIG.relative_to(ROOT)) if ELIG.is_file() else None,
        "lockbox_eval_detail": str(DETAIL.relative_to(ROOT)) if DETAIL.is_file() else None,
        "lockbox_eval_log": str(LOCK_LOG.relative_to(ROOT)) if LOCK_LOG.is_file() else None,
        "safe_status": str(SAFE_STATUS.relative_to(ROOT)),
        "lockbox_sha256": lockbox_sha,
        "eval_exit_code": args.eval_exit_code,
        "c0_not_frozen": True,
        "next_gate": "Q" if status == "PASS" else "P0-T-blocked",
        "no_bpb_in_receipt": True,
    }
    write_json(OUT, receipt)

    if status == "PASS":
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["P0-T"] = "pass"
        lock["status"] = "gate_p0t_pass"
        write_json(LOCK_PATH, lock)
        mark_ledger("P0-T", "pass", str(OUT.relative_to(ROOT)), "Q")
    elif status == "BLOCKED":
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["P0-T"] = "blocked"
        lock["status"] = "gate_p0t_blocked"
        write_json(LOCK_PATH, lock)
        mark_ledger("P0-T", "blocked", str(OUT.relative_to(ROOT)), "X-blocked-study")
    else:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["P0-T"] = "technical_block"
        lock["status"] = "gate_p0t_technical_block"
        write_json(LOCK_PATH, lock)
        mark_ledger("P0-T", "technical_block", str(OUT.relative_to(ROOT)), "P0-T")

    print(f"P0-T: {status}")
    print(
        json.dumps(
            {
                "p0_t_status": status,
                "receipt": str(OUT.relative_to(ROOT)),
                "safe_status": str(SAFE_STATUS.relative_to(ROOT)),
                "lockbox_sha256": lockbox_sha,
                "blinded": True,
                "no_bpb_printed": True,
            },
            indent=2,
        )
    )
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
