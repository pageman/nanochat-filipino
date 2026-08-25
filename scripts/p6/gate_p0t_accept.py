#!/usr/bin/env python3
"""Gate P0-T_s accept: lockbox scalars -> safe PASS/BLOCKED/TECHNICAL BLOCK only."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    DELTA,
    LOCK_PATH,
    P6_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    mark_ledger,
    seed_box,
    seed_card,
    seed_safe,
    sha256_bytes,
    update_lock_gate,
    utc_now,
    write_json,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--eval-exit-code", type=int, default=0)
    args = ap.parse_args()
    seed = args.seed
    box = seed_box(seed)
    detail = box / "gate-p0-t-eval-detail.json"
    elig = box / "gate-p0-t-eligibility.json"
    safe_status = seed_safe(seed) / "gate-p0-t-status.json"
    out = seed_card(seed) / "gate-p0-t.json"
    technical = args.eval_exit_code not in {0, 1} or (args.eval_exit_code == 0 and not detail.is_file())
    if args.eval_exit_code in {0, 1} and detail.is_file():
        technical = False
    depths_safe = {}
    lockbox_sha = None
    if technical or not detail.is_file():
        status = "TECHNICAL BLOCK"
        safe_payload = {"P0-T": status, "seed": seed}
    else:
        det = json.loads(detail.read_text())
        status = det.get("automated_status", "BLOCKED")
        if status not in {"PASS", "BLOCKED"}:
            status = "BLOCKED"
        eligibility = {
            "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
            "gate": "P0-T",
            "seed": seed,
            "untrained_floor_policy": "seed_matched",
            "untrained_seed": seed,
            "margin_bpb": DELTA,
            "status": status,
            "at_utc": utc_now(),
            "test_read_count": 0,
            "english_val_used": False,
            "depths": {},
        }
        for d_key, row in det.get("depths", {}).items():
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
        text = json.dumps(eligibility, indent=2) + "\n"
        elig.write_text(text)
        try:
            elig.chmod(0o600)
            if detail.is_file():
                detail.chmod(0o600)
        except OSError:
            pass
        lockbox_sha = sha256_bytes(text.encode())
        safe_payload = {"P0-T": status, "seed": seed, "lockbox_sha256": lockbox_sha}
    safe_status.write_text(json.dumps(safe_payload) + "\n")
    receipt_status = "pass" if status == "PASS" else ("blocked" if status == "BLOCKED" else "technical_block")
    # P6-M is seed-4 only: BLOCKED means blocked-study closeout, not seed replacement.
    if status == "PASS":
        next_gate = f"Q_{seed}"
    elif status == "BLOCKED":
        next_gate = "blocked_study_closeout"
    else:
        next_gate = "technical_stop"
    if status == "BLOCKED":
        write_json(
            seed_card(seed) / "ineligible_parent.json",
            {
                "seed": seed,
                "reason": "P0-T BLOCKED",
                "replacement_forbidden": True,
                "note": "Filed seed-4 only; do not replace parent seed.",
                "at_utc": utc_now(),
            },
        )
    write_json(
        out,
        {
            "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
            "aspredicted_id": ASPREDICTED_ID,
            "researchbox_id": RESEARCHBOX_ID,
            "gate": "P0-T",
            "seed": seed,
            "status": receipt_status,
            "p0_t_status": status,
            "at_utc": utc_now(),
            "host": platform.node(),
            "gpu": True,
            "blinded": True,
            "p6_run_id": P6_RUN_ID,
            "untrained_floor_policy": "seed_matched",
            "depths": depths_safe,
            "lockbox_sha256": lockbox_sha,
            "no_bpb_in_receipt": True,
            "next_gate": next_gate,
        },
    )
    update_lock_gate(f"P0-T_{seed}", receipt_status, {"status": f"gate_p0t_{seed}_{receipt_status}"})
    mark_ledger(f"P0-T_{seed}", receipt_status, str(out.relative_to(ROOT)), next_gate)
    print(f"P0-T: {status}")
    print(json.dumps({"seed": seed, "p0_t_status": status, "blinded": True, "no_bpb_printed": True}, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
