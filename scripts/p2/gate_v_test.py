#!/usr/bin/env python3
"""P2 Gate V: A2-only test. One authorized touch, two named evaluations.

Does not amend #306780 / #306935.
Does not load A1 or A3. Does not recompute C_en or G_tl.
Does not write P1.1 manifests/test_access_log.json.

Usage:
  python scripts/p2/gate_v_test.py --phase receipt
  GATE_V_AUTHORIZED=1 python scripts/p2/gate_v_test.py --phase english
  GATE_V_AUTHORIZED=1 python scripts/p2/gate_v_test.py --phase tagalog
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "p2-20260817T150944Z-de99f8a"
TOKENIZER_SHA256 = "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6"

A2_TAG = "p2-a2-tagalog-d20"
A2_STEP = 294
A2_SHA256 = "2b01acf8fac0e8c783162582cbb384e8ce1c37795aae2f7dd4ae34c2a5c76026"
TOKEN_BYTES_SHA256 = "5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42"
EN_TEST_SHA256 = "2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e"
TL_TEST_SHA256 = "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf"
FORBIDDEN_TAGS = ("p2-a1-extra-en-d20", "p2-a3-mix-d20", "p2-en0-d20")
LEDGER = ROOT / "docs" / "run-cards" / "p2" / "test_access_log.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_hash(path: Path, expected: str, label: str) -> str:
    actual = sha256_file(path)
    if actual != expected:
        raise SystemExit(f"hash mismatch {label} {path}: {actual} != {expected}")
    return actual


def paths() -> dict[str, Path]:
    base = Path(os.environ.get("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / RUN_ID)))
    return {
        "ckpt": base / "base_checkpoints" / A2_TAG / f"model_{A2_STEP:06d}.pt",
        "tokenizer": base / "tokenizer" / "tokenizer.pkl",
        "token_bytes": base / "tokenizer" / "token_bytes.pt",
        "en_test": ROOT / "data" / "interim" / "wikitext-103" / "english_test.jsonl",
        "tl_test": ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl",
        "evaluator": ROOT / "scripts" / "p2" / "evaluate_bpb.py",
        "this_script": Path(__file__).resolve(),
    }


def refuse_other_arms() -> None:
    joined = " ".join(sys.argv)
    for tag in FORBIDDEN_TAGS:
        if tag in joined:
            raise SystemExit(f"Gate V refuses non-A2 tag in argv: {tag}")


def receipt() -> dict:
    p = paths()
    a2 = require_hash(p["ckpt"], A2_SHA256, "A2")
    tok = require_hash(p["tokenizer"], TOKENIZER_SHA256, "tokenizer")
    tb = require_hash(p["token_bytes"], TOKEN_BYTES_SHA256, "token_bytes")
    en = require_hash(p["en_test"], EN_TEST_SHA256, "english_test")
    tl = require_hash(p["tl_test"], TL_TEST_SHA256, "tagalog_test")
    ev = sha256_file(p["evaluator"])
    gv = sha256_file(p["this_script"])
    rec = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "does_not_amend_306935": True,
        "gate": "V",
        "phase": "pretest_receipt",
        "test_access_count_before_execution": 0,
        "authorized_touch_semantics": "one Gate V authorization contains two prespecified evaluations (english then tagalog)",
        "arm": "A2",
        "model_tag": A2_TAG,
        "checkpoint_step": A2_STEP,
        "a2_sha256": a2,
        "a2_matches_gate_u_seal": a2 == A2_SHA256,
        "tokenizer_sha256": tok,
        "token_bytes_sha256": tb,
        "english_test_sha256": en,
        "tagalog_test_sha256": tl,
        "tagalog_test_role": "legacy_external_holdout_p11_test_jsonl_not_virgin_p2_test",
        "do_not_reuse_p11_test_bpb": 1.164768,
        "evaluator_sha256": ev,
        "gate_v_script_sha256": gv,
        "forbidden_parents_or_siblings": list(FORBIDDEN_TAGS),
        "p11_ledger_untouched": True,
        "at_utc": utc_now(),
    }
    print(json.dumps(rec, indent=2), flush=True)
    return rec


def append_ledger(event: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    if LEDGER.exists():
        data = json.loads(LEDGER.read_text())
    else:
        data = {
            "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
            "aspredicted_id": 306935,
            "does_not_amend_306780": True,
            "note": "P2 ledger. Not manifests/test_access_log.json (P1.1).",
            "authorized_touches": 0,
            "component_evaluations": 0,
            "events": [],
        }
    data["events"].append(event)
    data["component_evaluations"] = len(data["events"])
    data["authorized_touches"] = 1 if data["events"] else 0
    LEDGER.write_text(json.dumps(data, indent=2) + "\n")


def run_one(which: str) -> dict:
    if os.environ.get("GATE_V_AUTHORIZED") != "1":
        raise SystemExit("refusing test evaluation: set GATE_V_AUTHORIZED=1 after explicit user authorization")
    refuse_other_arms()
    rec = receipt()
    p = paths()
    if which == "english":
        test_path = p["en_test"]
        expected = EN_TEST_SHA256
        role = "wt103_raw_official_english_test"
    elif which == "tagalog":
        test_path = p["tl_test"]
        expected = TL_TEST_SHA256
        role = "legacy_external_holdout_p11_test_jsonl"
    else:
        raise SystemExit(which)

    sys.path.insert(0, str(ROOT / "scripts" / "p2"))
    sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))
    from evaluate_bpb import PACKING, STRIDE, eval_model, jsonl_texts, pack_one_pass
    from nanochat.checkpoint_manager import load_model
    from nanochat.common import compute_init
    from nanochat.tokenizer import get_token_bytes
    import torch

    compute_init("cuda")
    device = torch.device("cuda")
    B, T = 8, 2048
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=A2_TAG, step=A2_STEP)
    if int(meta["step"]) != A2_STEP:
        raise SystemExit(f"A2 step mismatch {meta['step']}")
    if meta["model_config"]["n_layer"] != 20:
        raise SystemExit("A2 depth must be 20")
    token_bytes = get_token_bytes(device=device)
    texts = jsonl_texts(test_path)
    batches, pack = pack_one_pass(texts, tokenizer, B, T, device)
    out = eval_model(model, batches, token_bytes, pack, f"{A2_TAG}/{which}_test")
    if not out["finite"]:
        raise SystemExit(f"{which} test BPB not finite")
    event = {
        "at_utc": utc_now(),
        "component": which,
        "role": role,
        "model_tag": A2_TAG,
        "checkpoint_sha256": rec["a2_sha256"],
        "test_path": str(test_path.relative_to(ROOT)),
        "test_sha256": expected,
        "bpb": out["bpb"],
        "total_nats": out["total_nats"],
        "total_bytes": out["total_bytes"],
        "n_scored_tokens": out["n_scored_tokens"],
        "packing": PACKING,
        "stride": STRIDE,
        "secondary_treatment_outcome": True,
        "does_not_alter_sealed_C_en_or_G_tl": True,
        "not_a_test_set_contrast": True,
    }
    append_ledger(event)
    print(json.dumps(event, indent=2), flush=True)
    return event


def main() -> int:
    refuse_other_arms()
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["receipt", "english", "tagalog"], required=True)
    args = parser.parse_args()
    os.environ.setdefault("P2_ROOT", str(ROOT))
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / RUN_ID))
    if args.phase == "receipt":
        receipt()
        return 0
    run_one(args.phase)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
