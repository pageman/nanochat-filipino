#!/usr/bin/env python3
"""P3 Gate U: six child val cells + B0 EN descriptive; seal to lockbox."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "p3"))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

from evaluate_bpb import (  # noqa: E402
    PACKING,
    eval_model,
    pack_one_pass,
    parquet_texts,
    require_hash,
    sha256_file,
)
from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402
from nanochat.tokenizer import get_token_bytes  # noqa: E402
from p3_common import ASPREDICTED_ID, BASE, EN_DIR, EXPECTED, P3_RUN_ID, RESEARCHBOX_ID, ROOT as P3_ROOT, RUN_CARD, TL_DIR  # noqa: E402
from phase2_common import B0_SHA256, B0_STEP, B0_TAG, B1_TAG, B2_TAG, B3_TAG, N_PHASE2, TOKENIZER_SHA  # noqa: E402

LOCKBOX = BASE / "lockbox"
EN_VAL_DIR = Path(os.environ.get("P3_EN_VAL_DIR", str(EN_DIR)))
TL_VAL_DIR = Path(os.environ.get("P3_TL_VAL_DIR", str(TL_DIR)))
ARMS = {
    "b1": B1_TAG,
    "b2": B2_TAG,
    "b3": B3_TAG,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ckpt_sha(tag: str) -> str:
    p = BASE / "base_checkpoints" / tag / f"model_{N_PHASE2:06d}.pt"
    return sha256_file(p)


def eval_arm(tag: str, en_batches, tl_batches, token_bytes, en_pack, tl_pack, device) -> tuple[dict, dict]:
    model, _tok, meta = load_model("base", device, phase="eval", model_tag=tag, step=N_PHASE2)
    assert meta["step"] == N_PHASE2
    en = eval_model(model, en_batches, token_bytes, en_pack, f"{tag}/english_val")
    tl = eval_model(model, tl_batches, token_bytes, tl_pack, f"{tag}/tagalog_val")
    del model
    torch.cuda.empty_cache()
    return en, tl


def write_cell(name: str, val_bpb: float, detail: dict, tag: str, split: str) -> None:
    payload = {
        "gate": "U",
        "cell": name,
        "model_tag": tag,
        "split": split,
        "val_bpb_full": val_bpb,
        "evaluated_at_utc": utc_now(),
        "packing": PACKING,
        "test_read_count": 0,
        "detail": detail,
    }
    path = LOCKBOX / name
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def main() -> int:
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(BASE))
    LOCKBOX.mkdir(parents=True, exist_ok=True)

    for gate, arm in (("r", "b1"), ("s", "b2"), ("t", "b3")):
        rec = RUN_CARD / f"gate-{gate}-{arm}.json"
        if not rec.is_file() or json.loads(rec.read_text()).get("status") != "pass":
            raise SystemExit(f"Gate {gate.upper()} not pass")

    require_hash(BASE / "tokenizer" / "tokenizer.pkl", TOKENIZER_SHA, "tokenizer")
    en_val = EN_VAL_DIR / "val.parquet"
    tl_val = TL_VAL_DIR / "shard_00002.parquet"
    require_hash(en_val, EXPECTED["en_train_shards"]["val.parquet"], "en_val")
    require_hash(tl_val, EXPECTED["p11_shards"]["shard_00002.parquet"], "tl_val")

    for tag in ARMS.values():
        actual = ckpt_sha(tag)
        print(f"ckpt ok {tag} sha256={actual[:16]}...", flush=True)

    b0_path = BASE / "base_checkpoints" / B0_TAG / f"model_{B0_STEP:06d}.pt"
    if sha256_file(b0_path) != B0_SHA256:
        raise SystemExit("B0 SHA mismatch at Gate U")

    compute_init("cuda")
    device = torch.device("cuda")
    B, T = 8, 2048
    _m, tokenizer, _meta = load_model("base", device, phase="eval", model_tag=B1_TAG, step=N_PHASE2)
    token_bytes = get_token_bytes(device=device)
    en_batches, en_pack = pack_one_pass(parquet_texts(en_val), tokenizer, B, T, device)
    tl_batches, tl_pack = pack_one_pass(parquet_texts(tl_val), tokenizer, B, T, device)
    del _m
    torch.cuda.empty_cache()

    for prefix, tag in ARMS.items():
        en_d, tl_d = eval_arm(tag, en_batches, tl_batches, token_bytes, en_pack, tl_pack, device)
        write_cell(f"{prefix}_en_val_bpb_full.json", en_d["bpb"], en_d, tag, "english_val")
        write_cell(f"{prefix}_tl_val_bpb_full.json", tl_d["bpb"], tl_d, tag, "tagalog_val")

    # B0 English descriptive (once)
    model, _, _ = load_model("base", device, phase="eval", model_tag=B0_TAG, step=B0_STEP)
    b0_en = eval_model(model, en_batches, token_bytes, en_pack, f"{B0_TAG}/english_val")
    del model
    torch.cuda.empty_cache()
    write_cell("b0_en_val_bpb_full.json", b0_en["bpb"], b0_en, B0_TAG, "english_val")

    # Seal via frozen script (stdout is safe-only)
    seal_script = P3_ROOT / "scripts" / "p3" / "make_validation_seal.py"
    subprocess.run(
        [
            sys.executable,
            str(seal_script),
            "--lockbox",
            str(LOCKBOX),
            "--safe-progress",
            str(BASE / "safe_progress"),
        ],
        check=True,
        cwd=P3_ROOT,
    )

    receipt = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "U",
        "status": "pass",
        "at_utc": utc_now(),
        "p3_run_id": P3_RUN_ID,
        "seal_path": str((LOCKBOX / "p3-validation-seal.json").relative_to(P3_ROOT)),
        "safe_status": str((BASE / "safe_progress" / "gate-u-status.json").relative_to(P3_ROOT)),
        "test_access": 0,
        "no_bpb_in_receipt": True,
        "next_gate": "V",
    }
    out = RUN_CARD / "gate-u-seal.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("seven Gate U val outputs complete (six child + B0 EN descriptive); validation seal created; P3 test access = 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
