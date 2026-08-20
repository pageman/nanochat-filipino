#!/usr/bin/env python3
"""P3 Gate V: B2-only test. One authorized touch, two component evaluations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "p3"))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

from evaluate_bpb import PACKING, STRIDE, eval_model, jsonl_texts, pack_one_pass, require_hash, sha256_file  # noqa: E402
from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402
from nanochat.tokenizer import get_token_bytes  # noqa: E402
from p3_common import ASPREDICTED_ID, BASE, EN_TEST_JSONL, EXPECTED, P3_RUN_ID, RESEARCHBOX_ID, ROOT as P3_ROOT, RUN_CARD, TL_TEST  # noqa: E402
from phase2_common import B2_TAG, N_PHASE2, TOKENIZER_SHA  # noqa: E402

LEDGER = ROOT / "docs" / "run-cards" / "p3" / "test_access_log.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def refuse_other_arms() -> None:
    joined = " ".join(sys.argv)
    for tag in ("p3-b1-extra-tl-d20", "p3-b3-mix-d20", "p3-tl0-d20"):
        if tag in joined:
            raise SystemExit(f"Gate V refuses non-B2 tag: {tag}")


def append_ledger(event: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(LEDGER.read_text()) if LEDGER.exists() else {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "p3_run_id": P3_RUN_ID,
        "authorized_touches": 0,
        "component_evaluations": 0,
        "events": [],
    }
    data["events"].append(event)
    data["component_evaluations"] = len(data["events"])
    data["authorized_touches"] = 1 if data["events"] else 0
    LEDGER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def run_one(which: str, b2_sha: str) -> dict:
    if os.environ.get("GATE_V_AUTHORIZED") != "1":
        raise SystemExit("set GATE_V_AUTHORIZED=1")
    refuse_other_arms()
    seal = BASE / "lockbox" / "p3-validation-seal.json"
    if not seal.is_file():
        raise SystemExit("missing U seal")
    if json.loads(seal.read_text()).get("test_access", 1) != 0:
        raise SystemExit("seal test_access must be 0")

    if which == "english":
        test_path = EN_TEST_JSONL
        expected = EXPECTED["en_test_jsonl"]
    else:
        test_path = TL_TEST
        expected = EXPECTED["tl_test_jsonl"]
    require_hash(test_path, expected, which + "_test")

    compute_init("cuda")
    device = __import__("torch").device("cuda")
    import torch

    B, T = 8, 2048
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=B2_TAG, step=N_PHASE2)
    if sha256_file(BASE / "base_checkpoints" / B2_TAG / f"model_{N_PHASE2:06d}.pt") != b2_sha:
        raise SystemExit("B2 SHA mismatch")
    token_bytes = get_token_bytes(device=device)
    batches, pack = pack_one_pass(jsonl_texts(test_path), tokenizer, B, T, device)
    out = eval_model(model, batches, token_bytes, pack, f"{B2_TAG}/{which}_test")
    event = {
        "at_utc": utc_now(),
        "component": which,
        "model_tag": B2_TAG,
        "checkpoint_sha256": b2_sha,
        "test_path": str(test_path.relative_to(P3_ROOT)),
        "bpb": out["bpb"],
        "total_nats": out["total_nats"],
        "total_bytes": out["total_bytes"],
        "packing": PACKING,
        "stride": STRIDE,
        "does_not_alter_sealed_contrasts": True,
    }
    append_ledger(event)
    return event


def main() -> int:
    refuse_other_arms()
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["receipt", "english", "tagalog", "all"], required=True)
    args = ap.parse_args()

    b2_rec = json.loads((RUN_CARD / "gate-s-b2.json").read_text())
    b2_sha = b2_rec["checkpoint_sha256"]
    lockbox = BASE / "lockbox"

    if args.phase == "receipt":
        rec = {
            "gate": "V",
            "arm": "B2",
            "model_tag": B2_TAG,
            "b2_sha256": b2_sha,
            "test_access_before": 0,
            "at_utc": utc_now(),
        }
        print(json.dumps(rec, indent=2))
        return 0

    os.environ.setdefault("GATE_V_AUTHORIZED", "1")
    events = []
    if args.phase in ("english", "all"):
        events.append(run_one("english", b2_sha))
    if args.phase in ("tagalog", "all"):
        events.append(run_one("tagalog", b2_sha))

    summary = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "V",
        "arm": "B2",
        "authorized_touches": 1,
        "component_evaluations": len(events),
        "english": events[0] if args.phase == "english" or (args.phase == "all" and events) else None,
        "tagalog": events[-1] if args.phase == "tagalog" else (events[1] if args.phase == "all" and len(events) > 1 else None),
        "at_utc": utc_now(),
        "test_access": 1,
    }
    (lockbox / "gate-v-test.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    safe = BASE / "safe_progress" / "gate-v-status.json"
    safe.parent.mkdir(parents=True, exist_ok=True)
    safe.write_text(json.dumps({"one_authorized_B2_only_test_event_completed": True, "test_access_count": 1}) + "\n")
    receipt = {
        "gate": "V",
        "status": "pass",
        "p3_run_id": P3_RUN_ID,
        "lockbox": str((lockbox / "gate-v-test.json").relative_to(P3_ROOT)),
        "safe_status": str(safe.relative_to(P3_ROOT)),
        "no_bpb_in_receipt": True,
        "next_gate": "W",
    }
    (RUN_CARD / "gate-v-test.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("one authorized B2-only test event completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
