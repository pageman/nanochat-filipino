#!/usr/bin/env python3
"""P2 Gate U: seal val_bpb_full for A1/A2/A3. Val only. No test.

Uses scripts/p2/evaluate_bpb.py packing and official evaluate_bpb components.
Does not recompute A0 English (P0-E) or A0 Tagalog (Gate Q CUDA).
Does not amend #306780 / #306935.

C_en = English(A2) - English(A1)
G_tl = Tagalog(A2) - Tagalog(A1)
A0→A2 Tagalog is descriptive only (AsPredicted #306935 Q2).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "p2"))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

from evaluate_bpb import (  # noqa: E402
    EXPECTED,
    PACKING,
    RUN_ID,
    STRIDE,
    eval_model,
    pack_one_pass,
    parquet_texts,
    require_hash,
    sha256_file,
    utc_now,
)
from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402
from nanochat.tokenizer import get_token_bytes  # noqa: E402

CUTOFF = 0.01
A0_EN = 1.3899902041579162
A0_TL = 4.917649994523231
UNTRAINED_EN = 3.246977715228228
UNIGRAM_EN = 4.582801206418281
ARMS = {
    "A1": {
        "tag": "p2-a1-extra-en-d20",
        "step": 294,
        "sha256": "e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d",
    },
    "A2": {
        "tag": "p2-a2-tagalog-d20",
        "step": 294,
        "sha256": "2b01acf8fac0e8c783162582cbb384e8ce1c37795aae2f7dd4ae34c2a5c76026",
    },
    "A3": {
        "tag": "p2-a3-mix-d20",
        "step": 294,
        "sha256": "d6c62bb793a57c7c23d98c5bd62ec36b41606234524f76855b4459d98c42b368",
    },
}


def refuse_test(root: Path) -> None:
    forbidden = [
        root / "data" / "interim" / "wikitext-103" / "english_test.jsonl",
        root / "data" / "processed" / "wikitext-103" / "en-active" / "test.parquet",
        root / "data" / "processed" / "p2-tl39-readonly" / "test.jsonl",
    ]
    # Existence is allowed; reading is not. We never open these paths.
    for p in forbidden:
        if p.exists():
            print(f"test artifact present but unread: {p}", flush=True)


def contrast(a: float, b: float) -> dict:
    delta = a - b
    return {
        "delta": delta,
        "abs_delta": abs(delta),
        "material_at_0_01": abs(delta) >= CUTOFF,
        "not_a_ranking_if_below_cutoff": abs(delta) < CUTOFF,
    }


def main() -> int:
    os.environ.setdefault("P2_ROOT", str(ROOT))
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / RUN_ID))
    base = Path(os.environ["NANOCHAT_BASE_DIR"])
    en_active = Path(os.environ.get("NANOCHAT_DATA_DIR_EN", str(ROOT / "data" / "processed" / "wikitext-103" / "en-active")))
    tl_readonly = Path(os.environ.get("NANOCHAT_DATA_DIR_TL", str(ROOT / "data" / "processed" / "p2-tl39-readonly")))
    out_dir = Path(os.environ.get("GATE_U_OUT", str(ROOT / "docs" / "run-cards" / "p2" / RUN_ID)))
    out_dir.mkdir(parents=True, exist_ok=True)

    refuse_test(ROOT)
    require_hash(base / "tokenizer" / "tokenizer.pkl", EXPECTED["tokenizer"], "tokenizer")
    en_val = en_active / "val.parquet"
    tl_val = tl_readonly / "shard_00002.parquet"
    require_hash(en_val, EXPECTED["val_parquet"], "en_val")
    require_hash(tl_val, EXPECTED["tl_val_shard"], "tl_val")

    for arm, spec in ARMS.items():
        ckpt = base / "base_checkpoints" / spec["tag"] / f"model_{spec['step']:06d}.pt"
        actual = sha256_file(ckpt)
        if actual != spec["sha256"]:
            raise SystemExit(f"{arm} SHA mismatch {actual} != {spec['sha256']}")
        print(f"{arm} ckpt ok {actual}", flush=True)

    compute_init("cuda")
    device = torch.device("cuda")
    B, T = 8, 2048
    model0, tokenizer, meta0 = load_model("base", device, phase="eval", model_tag="p2-a1-extra-en-d20", step=294)
    assert meta0["model_config"]["sequence_len"] == T
    token_bytes = get_token_bytes(device=device)

    print("packing English val", flush=True)
    en_batches, en_pack = pack_one_pass(parquet_texts(en_val), tokenizer, B, T, device)
    print("packing Tagalog val", flush=True)
    tl_batches, tl_pack = pack_one_pass(parquet_texts(tl_val), tokenizer, B, T, device)
    del model0
    torch.cuda.empty_cache()

    cells = {}
    for arm, spec in ARMS.items():
        print(f"\n=== {arm} {spec['tag']} ===", flush=True)
        model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=spec["tag"], step=spec["step"])
        assert int(meta["step"]) == spec["step"]
        assert meta["model_config"]["n_layer"] == 20
        token_bytes = get_token_bytes(device=device)
        en = eval_model(model, en_batches, token_bytes, en_pack, f"{spec['tag']}/english_val")
        tl = eval_model(model, tl_batches, token_bytes, tl_pack, f"{spec['tag']}/tagalog_val")
        if not en["finite"] or not tl["finite"]:
            raise SystemExit(f"{arm} non-finite BPB")
        cells[arm] = {
            "model_tag": spec["tag"],
            "checkpoint_step": spec["step"],
            "checkpoint_sha256": spec["sha256"],
            "english_val_bpb_full": en["bpb"],
            "tagalog_val_bpb_full": tl["bpb"],
            "english": en,
            "tagalog": tl,
        }
        del model
        torch.cuda.empty_cache()

    c_en = contrast(cells["A2"]["english_val_bpb_full"], cells["A1"]["english_val_bpb_full"])
    g_tl = contrast(cells["A2"]["tagalog_val_bpb_full"], cells["A1"]["tagalog_val_bpb_full"])
    c_en_a3 = contrast(cells["A3"]["english_val_bpb_full"], cells["A1"]["english_val_bpb_full"])
    g_tl_a3 = contrast(cells["A3"]["tagalog_val_bpb_full"], cells["A1"]["tagalog_val_bpb_full"])
    a0_a2_tl_descriptive = contrast(A0_TL, cells["A2"]["tagalog_val_bpb_full"])

    seal = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "does_not_amend_306935": True,
        "gate": "U",
        "status": "pass",
        "depth": 20,
        "T": T,
        "device_batch_size": B,
        "packing": PACKING,
        "stride": STRIDE,
        "evaluator": "scripts/p2/evaluate_bpb.py via scripts/p2/gate_u_seal.py",
        "tokenizer_sha256": EXPECTED["tokenizer"],
        "english_val_parquet_sha256": EXPECTED["val_parquet"],
        "tagalog_val_shard_sha256": EXPECTED["tl_val_shard"],
        "test_read_events_p2_english": 0,
        "test_read_events_p2_tagalog": 0,
        "test_read_count": 0,
        "inloop_val_is_not_val_bpb_full": True,
        "practical_cutoff_bpb": CUTOFF,
        "copied_not_recomputed": {
            "A0_english_val_bpb_full": A0_EN,
            "A0_english_source": "gate_p0_val_baselines.json / P0-E d20",
            "A0_tagalog_val_bpb_full": A0_TL,
            "A0_tagalog_source": "p2-en0-d20_a0_tagalog_val.json CUDA Gate Q",
            "untrained_english_val_bpb": UNTRAINED_EN,
            "byte_unigram_english_val_bpb": UNIGRAM_EN,
        },
        "table_d20": {
            "Untrained": {"english_val_bpb_full": UNTRAINED_EN, "tagalog_val_bpb_full": None, "tagalog_note": "not required for C_en/G_tl; not recomputed"},
            "A0": {"english_val_bpb_full": A0_EN, "tagalog_val_bpb_full": A0_TL, "recomputed": False},
            "A1": {"english_val_bpb_full": cells["A1"]["english_val_bpb_full"], "tagalog_val_bpb_full": cells["A1"]["tagalog_val_bpb_full"]},
            "A2": {"english_val_bpb_full": cells["A2"]["english_val_bpb_full"], "tagalog_val_bpb_full": cells["A2"]["tagalog_val_bpb_full"]},
            "A3": {"english_val_bpb_full": cells["A3"]["english_val_bpb_full"], "tagalog_val_bpb_full": cells["A3"]["tagalog_val_bpb_full"]},
            "P1.1_d20_descriptive": {"english_val_bpb_full": None, "tagalog_val_bpb_full": 1.172248, "note": "native Tagalog BPE; different tokenizer; not a C_en/G_tl input"},
        },
        "cells": cells,
        "contrasts": {
            "C_en": {"formula": "English(A2)-English(A1)", "prediction": ">= 0.01", **c_en},
            "G_tl": {"formula": "Tagalog(A2)-Tagalog(A1)", "prediction": "<= -0.01", **g_tl},
            "C_en_A3": {"formula": "English(A3)-English(A1)", "note": "trade-off arm; smaller C_en is not mitigation", **c_en_a3},
            "G_tl_A3": {"formula": "Tagalog(A3)-Tagalog(A1)", "note": "trade-off arm; not mitigation", **g_tl_a3},
            "A0_minus_A2_tagalog_descriptive": {
                "formula": "Tagalog(A0)-Tagalog(A2)",
                "note": "AsPredicted Q2: A0 to A2 Tagalog change is descriptive only",
                **a0_a2_tl_descriptive,
            },
        },
        "one_seed_point_estimates_only": True,
        "evaluated_at_utc": utc_now(),
        "next_gate": "V",
        "next_requires_authorization": True,
        "note": "Val seal only. Do not read test. A2-only test is Gate V after this seal. Does not amend #306780.",
    }
    out_path = out_dir / "gate-u-seal.json"
    out_path.write_text(json.dumps(seal, indent=2) + "\n")
    print(json.dumps({
        "C_en": c_en["delta"],
        "G_tl": g_tl["delta"],
        "C_en_A3": c_en_a3["delta"],
        "G_tl_A3": g_tl_a3["delta"],
        "table": seal["table_d20"],
        "out": str(out_path),
    }, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
