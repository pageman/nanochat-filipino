#!/usr/bin/env python3
"""P4 Gate U: six child val cells + C0 EN descriptive; seal to lockbox. No BPB on stdout."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "p4"))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

import torch  # noqa: E402
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
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C2_DIR,
    EXPECTED,
    FILED_EVALUATOR_SHA,
    LOCK_PATH,
    LOCKBOX,
    N_PHASE2,
    N_TL0,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT as P4_ROOT,
    RUN_CARD,
    SAFE,
    TOKENIZER_PKL_SHA,
    mark_ledger,
    utc_now,
    write_json,
)
from phase2_common import C0_SOURCE_TAG, C1_TAG, C2_TAG, C3_TAG  # noqa: E402

AUTH = RUN_CARD / "gate-u-authorization.json"
ARMS = {"c1": C1_TAG, "c2": C2_TAG, "c3": C3_TAG}


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


def eval_arm(tag: str, en_batches, tl_batches, token_bytes, en_pack, tl_pack):
    model, _tok, meta = load_model("base", torch.device("cuda"), phase="eval", model_tag=tag, step=N_PHASE2)
    assert meta["step"] == N_PHASE2
    en = eval_model(model, en_batches, token_bytes, en_pack, f"{tag}/english_val")
    tl = eval_model(model, tl_batches, token_bytes, tl_pack, f"{tag}/tagalog_val")
    del model
    torch.cuda.empty_cache()
    return en, tl


def main() -> int:
    auth = json.loads(AUTH.read_text(encoding="utf-8")) if AUTH.is_file() else {}
    if auth.get("gate") != "U" or auth.get("authorized") is not True:
        raise SystemExit("missing Gate U authorization")

    for gate, arm in (("r", "c1"), ("s", "c2"), ("t", "c3")):
        rec = RUN_CARD / f"gate-{gate}-{arm}.json"
        if not rec.is_file() or json.loads(rec.read_text()).get("status") != "pass":
            raise SystemExit(f"Gate {gate.upper()} not pass")

    eval_sha = sha256_file(P4_ROOT / "scripts" / "p4" / "evaluate_bpb.py")
    if eval_sha != FILED_EVALUATOR_SHA:
        raise SystemExit("evaluator SHA drifted from Gate A")

    require_hash(BASE / "tokenizer" / "tokenizer.pkl", TOKENIZER_PKL_SHA, "tokenizer")
    en_val = C2_DIR / "val.parquet"
    tl_val = C1_DIR / "val.parquet"
    pack = json.loads((RUN_CARD / "gate-e-c1-c2-pack.json").read_text(encoding="utf-8"))
    en_expected = pack["c2_en"]["shards"]["val.parquet"]["sha256"]
    require_hash(tl_val, EXPECTED["c1_shards"]["val.parquet"], "tl_val")
    require_hash(en_val, en_expected, "en_val")

    q = json.loads((RUN_CARD / "gate-q-c0-freeze.json").read_text())
    c0_sha = q["checkpoint_sha256"]
    if sha256_file(BASE / "base_checkpoints" / C0_SOURCE_TAG / f"model_{N_TL0:06d}.pt") != c0_sha:
        raise SystemExit("C0 source SHA mismatch at Gate U")

    os.environ.setdefault("NANOCHAT_BASE_DIR", str(BASE))
    LOCKBOX.mkdir(parents=True, exist_ok=True)

    # Symlink C1 last-is-val aliases if evaluator helpers ever need shard names
    for src, dst in (
        (C1_DIR / "train_00000.parquet", C1_DIR / "shard_00000.parquet"),
        (C1_DIR / "val.parquet", C1_DIR / "shard_00002.parquet"),
    ):
        if src.is_file() and not dst.exists():
            try:
                dst.symlink_to(src.name)
            except OSError:
                pass

    compute_init("cuda")
    device = torch.device("cuda")
    B, T = 8, 2048
    _m, tokenizer, _meta = load_model("base", device, phase="eval", model_tag=C1_TAG, step=N_PHASE2)
    token_bytes = get_token_bytes(device=device)
    en_batches, en_pack = pack_one_pass(parquet_texts(en_val), tokenizer, B, T, device)
    tl_batches, tl_pack = pack_one_pass(parquet_texts(tl_val), tokenizer, B, T, device)
    del _m
    torch.cuda.empty_cache()

    for prefix, tag in ARMS.items():
        print(f"Gate U evaluating {tag} (scalars -> lockbox)", flush=True)
        en_d, tl_d = eval_arm(tag, en_batches, tl_batches, token_bytes, en_pack, tl_pack)
        write_cell(f"{prefix}_en_val_bpb_full.json", en_d["bpb"], en_d, tag, "english_val")
        write_cell(f"{prefix}_tl_val_bpb_full.json", tl_d["bpb"], tl_d, tag, "tagalog_val")

    print("Gate U evaluating C0 English descriptive (scalars -> lockbox)", flush=True)
    model, _, _ = load_model("base", device, phase="eval", model_tag=C0_SOURCE_TAG, step=N_TL0)
    c0_en = eval_model(model, en_batches, token_bytes, en_pack, f"{C0_SOURCE_TAG}/english_val")
    del model
    torch.cuda.empty_cache()
    write_cell("c0_en_val_bpb_full.json", c0_en["bpb"], c0_en, C0_SOURCE_TAG, "english_val")

    # Copy C0 Tagalog from P0-T lockbox into seal inventory (not a new confirmatory look).
    p0t_elig = LOCKBOX / "gate-p0-t-eligibility.json"
    if p0t_elig.is_file():
        elig = json.loads(p0t_elig.read_text(encoding="utf-8"))
        tl_bpb = elig.get("depths", {}).get("20", {}).get("val_bpb_full")
        if tl_bpb is not None:
            write_cell(
                "c0_tl_val_bpb_full.json",
                float(tl_bpb),
                {"copied_from": "gate-p0-t-eligibility.json", "depth": 20},
                C0_SOURCE_TAG,
                "tagalog_val_from_p0t",
            )

    subprocess.run(
        [
            sys.executable,
            str(P4_ROOT / "scripts" / "p4" / "make_validation_seal.py"),
            "--lockbox",
            str(LOCKBOX),
            "--safe-progress",
            str(SAFE),
        ],
        check=True,
        cwd=str(P4_ROOT),
    )

    safe_status = SAFE / "gate-u-status.json"
    seal = LOCKBOX / "p4-validation-seal.json"
    receipt = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "U",
        "status": "pass",
        "at_utc": utc_now(),
        "host": os.uname().nodename,
        "gpu": True,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "seal_path": str(seal.relative_to(P4_ROOT)),
        "safe_status": str(safe_status.relative_to(P4_ROOT)),
        "seal_sha256": json.loads(safe_status.read_text()).get("seal_sha256") if safe_status.is_file() else None,
        "test_access": 0,
        "no_bpb_in_receipt": True,
        "next_gate": "V",
    }
    write_json(RUN_CARD / "gate-u-seal.json", receipt)
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["gate_statuses"]["U"] = "pass"
    lock["status"] = "gate_u_pass"
    write_json(LOCK_PATH, lock)
    mark_ledger("U", "pass", "docs/run-cards/p4/p4-20260821T060032Z-92d63d4/gate-u-seal.json", "V")
    print(
        "seven Gate U val outputs complete (six child + C0 EN descriptive); validation seal created; P4 test access = 0",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
