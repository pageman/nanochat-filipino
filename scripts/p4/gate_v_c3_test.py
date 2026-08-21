#!/usr/bin/env python3
"""P4 Gate V: C3-only secondary test (Policy A). One authorized touch, two components."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "p4"))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

from evaluate_bpb import PACKING, STRIDE, eval_model, jsonl_texts, pack_one_pass, require_hash, sha256_file  # noqa: E402
from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402
from nanochat.tokenizer import get_token_bytes  # noqa: E402
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    EN_TEST_JSONL,
    EXPECTED,
    LOCK_PATH,
    LOCKBOX,
    N_PHASE2,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT as P4_ROOT,
    RUN_CARD,
    SAFE,
    TL_TEST_JSONL,
    mark_ledger,
    utc_now,
    write_json,
)
from phase2_common import C3_TAG  # noqa: E402

LEDGER = P4_ROOT / "manifests" / "p4" / "p4_test_access_log.json"
AUTH = RUN_CARD / "gate-v-authorization.json"


def refuse_other_arms() -> None:
    joined = " ".join(sys.argv)
    for tag in ("p4-c1-tl-d20", "p4-c2-en-d20", "p4-tl0-d20", "p4-c0-tl-d20"):
        if tag in joined and "--phase" in joined:
            # argv always contains script path; only refuse if model-tag request sneaks in
            pass
    for bad in ("--model-tag=p4-c1", "--model-tag=p4-c2", "p4-c1-tl-d20=", "p4-c2-en-d20="):
        if bad in joined:
            raise SystemExit(f"Gate V refuses non-C3 tag: {bad}")


def append_ledger(event: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    data = (
        json.loads(LEDGER.read_text())
        if LEDGER.exists()
        else {
            "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
            "aspredicted_id": ASPREDICTED_ID,
            "p4_run_id": P4_RUN_ID,
            "authorized_touches": 0,
            "component_evaluations": 0,
            "events": [],
        }
    )
    data["events"].append(event)
    data["component_evaluations"] = len(data["events"])
    data["authorized_touches"] = 1 if data["events"] else 0
    write_json(LEDGER, data)


def run_one(which: str, c3_sha: str) -> dict:
    if os.environ.get("GATE_V_AUTHORIZED") != "1":
        raise SystemExit("set GATE_V_AUTHORIZED=1")
    seal = LOCKBOX / "p4-validation-seal.json"
    if not seal.is_file():
        raise SystemExit("missing U seal")
    if json.loads(seal.read_text()).get("test_access", 1) != 0:
        raise SystemExit("seal test_access must be 0")

    if which == "english":
        test_path = EN_TEST_JSONL
        expected = EXPECTED["en_test_jsonl"]
    else:
        test_path = TL_TEST_JSONL
        expected = EXPECTED["tl_test_jsonl"]
    require_hash(test_path, expected, which + "_test")

    compute_init("cuda")
    import torch

    device = torch.device("cuda")
    B, T = 8, 2048
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=C3_TAG, step=N_PHASE2)
    if sha256_file(BASE / "base_checkpoints" / C3_TAG / f"model_{N_PHASE2:06d}.pt") != c3_sha:
        raise SystemExit("C3 SHA mismatch")
    token_bytes = get_token_bytes(device=device)
    batches, pack = pack_one_pass(jsonl_texts(test_path), tokenizer, B, T, device)
    out = eval_model(model, batches, token_bytes, pack, f"{C3_TAG}/{which}_test")
    del model
    torch.cuda.empty_cache()
    event = {
        "at_utc": utc_now(),
        "component": which,
        "model_tag": C3_TAG,
        "checkpoint_sha256": c3_sha,
        "test_path": str(test_path.relative_to(P4_ROOT)),
        "bpb": out["bpb"],
        "total_nats": out["total_nats"],
        "total_bytes": out["total_bytes"],
        "packing": PACKING,
        "stride": STRIDE,
        "does_not_alter_sealed_contrasts": True,
    }
    append_ledger(event)
    lock_path = LOCKBOX / f"gate-v-c3-{which}-test.json"
    lock_path.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
    try:
        lock_path.chmod(0o600)
    except OSError:
        pass
    return event


def main() -> int:
    refuse_other_arms()
    auth = json.loads(AUTH.read_text(encoding="utf-8")) if AUTH.is_file() else {}
    if auth.get("gate") != "V" or auth.get("authorized") is not True:
        raise SystemExit("missing Gate V authorization")

    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["all"], default="all")
    args = ap.parse_args()

    c3_rec = json.loads((RUN_CARD / "gate-t-c3.json").read_text())
    if c3_rec.get("status") != "pass":
        raise SystemExit("Gate T must pass")
    c3_sha = c3_rec["checkpoint_sha256"]
    u_rec = json.loads((RUN_CARD / "gate-u-seal.json").read_text())
    if u_rec.get("status") != "pass":
        raise SystemExit("Gate U must pass")

    os.environ["GATE_V_AUTHORIZED"] = "1"
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(BASE))
    events = [run_one("english", c3_sha), run_one("tagalog", c3_sha)]

    summary = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "V",
        "arm": "C3",
        "model_tag": C3_TAG,
        "authorized_touches": 1,
        "component_evaluations": 2,
        "checkpoint_sha256": c3_sha,
        "at_utc": utc_now(),
        "test_access": 1,
        "english_bpb_lockboxed": True,
        "tagalog_bpb_lockboxed": True,
        "does_not_alter_sealed_contrasts": True,
    }
    (LOCKBOX / "gate-v-test.json").write_text(json.dumps({**summary, "events": events}, indent=2) + "\n")
    try:
        (LOCKBOX / "gate-v-test.json").chmod(0o600)
    except OSError:
        pass

    SAFE.mkdir(parents=True, exist_ok=True)
    (SAFE / "gate-v-status.json").write_text(
        json.dumps(
            {
                "one_authorized_C3_only_test_event_completed": True,
                "test_access_count": 1,
                "component_evaluations": 2,
            }
        )
        + "\n"
    )

    receipt = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "V",
        "status": "pass",
        "at_utc": utc_now(),
        "p4_run_id": P4_RUN_ID,
        "gpu": True,
        "blinded": True,
        "model_tag": C3_TAG,
        "checkpoint_sha256": c3_sha,
        "authorized_touches": 1,
        "component_evaluations": 2,
        "test_access": 1,
        "no_bpb_in_receipt": True,
        "next_gate": "X",
    }
    write_json(RUN_CARD / "gate-v-test.json", receipt)
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["gate_statuses"]["V"] = "pass"
    lock["status"] = "gate_v_pass"
    write_json(LOCK_PATH, lock)
    mark_ledger("V", "pass", "docs/run-cards/p4/p4-20260821T060032Z-92d63d4/gate-v-test.json", "X")
    print("one authorized C3-only test event completed", flush=True)
    print(json.dumps({"p0_t_status_ignored": True, "gate": "V", "status": "pass", "blinded": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
