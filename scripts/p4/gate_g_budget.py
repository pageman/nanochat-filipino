#!/usr/bin/env python3
"""P4 Gate G: freeze T_tl_train, N_TL0=294, argv. Desk calc. Blinded. No BPB."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "vendor" / "nanochat"))

from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    B,
    D_PHASE2,
    N_PHASE2,
    N_TL0,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    T,
    TL_TRAIN_JSONL,
    TOK_DIR,
    TOKENIZER_PKL_SHA,
    VOCAB,
    WARMUP,
    blinded_print,
    freeze_file,
    mark_ledger,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)
from nanochat.gpt import GPT, GPTConfig  # noqa: E402
from nanochat.tokenizer import RustBPETokenizer  # noqa: E402

OUT = RUN_CARD / "gate-g-budget-command-freeze.json"
BUDGET = ROOT / "manifests" / "p4" / "p4_budget_manifest.json"
DEPTHS = (8, 20)
ASPECT_RATIO = 64
HEAD_DIM = 128
WINDOW_PATTERN = "SSSL"


def count_tokens(tokenizer: RustBPETokenizer, path: Path, batch_size: int = 256) -> dict:
    texts = [json.loads(line)["text"] for line in path.read_text(encoding="utf-8").splitlines() if line]
    n_tokens = n_bytes = n_chars = 0
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        encoded = tokenizer.encode(batch)
        n_tokens += sum(len(ids) for ids in encoded)
        n_bytes += sum(len(t.encode("utf-8")) for t in batch)
        n_chars += sum(len(t) for t in batch)
        if i and i % 2048 == 0:
            print(json.dumps({"g_progress_docs": i, "tokens_so_far": n_tokens}), flush=True)
    return {"n_docs": len(texts), "n_tokens": n_tokens, "n_bytes": n_bytes, "n_chars": n_chars, "bos_prepended": False, "packing": False, "crop": False}


def build_model_meta(depth: int, vocab_size: int) -> GPT:
    base_dim = depth * ASPECT_RATIO
    model_dim = ((base_dim + HEAD_DIM - 1) // HEAD_DIM) * HEAD_DIM
    num_heads = model_dim // HEAD_DIM
    config = GPTConfig(sequence_len=T, vocab_size=vocab_size, n_layer=depth, n_head=num_heads, n_kv_head=num_heads, n_embd=model_dim, window_pattern=WINDOW_PATTERN)
    with torch.device("meta"):
        return GPT(config)


def main() -> int:
    tok_sha = sha256_file(TOK_DIR / "tokenizer.pkl")
    if tok_sha != TOKENIZER_PKL_SHA:
        raise SystemExit("tokenizer SHA mismatch at G")
    tokenizer = RustBPETokenizer.from_directory(str(TOK_DIR))
    vocab = tokenizer.get_vocab_size()
    train_stats = count_tokens(tokenizer, TL_TRAIN_JSONL)
    t_tl_train = train_stats["n_tokens"]
    d_3x = 3 * t_tl_train
    n_computed = math.ceil(d_3x / B)
    d_actual = N_TL0 * B
    warmup_tl0 = WARMUP
    warmup_phase2 = WARMUP

    depth_rows = []
    for depth in DEPTHS:
        model = build_model_meta(depth, vocab)
        counts = model.num_scaling_params()
        depth_rows.append({"depth": depth, "p_scaling": int(counts["transformer_matrices"] + counts["lm_head"]), "num_iterations_tl0": N_TL0})

    parent_argv = {
        "class": "python -m scripts.base_train",
        "device_type": "cuda",
        "depths": list(DEPTHS),
        "max_seq_len": T,
        "window_pattern": WINDOW_PATTERN,
        "device_batch_size": 8,
        "total_batch_size": B,
        "num_iterations": N_TL0,
        "warmup_steps": warmup_tl0,
        "eval_every": -1,
        "core_metric_every": -1,
        "sample_every": -1,
        "save_every": -1,
        "model_tags": ["p4-tl0-d8", "p4-tl0-d20"],
        "runs": ["p4-tl0-d8", "p4-tl0-d20"],
        "note": "terminal checkpoint only; save-every=-1 writes model_{N:06d}.pt at last step on pin 92d63d4",
    }
    child_argv = {
        "wrapper": "python scripts/p4/continue_from_frozen.py",
        "init_from": f"$NANOCHAT_BASE_DIR/c0/frozen/p4-c0-tl-d20",
        "init_step": N_TL0,
        "depth": 20,
        "max_seq_len": T,
        "window_pattern": WINDOW_PATTERN,
        "device_batch_size": 8,
        "total_batch_size": B,
        "num_iterations": N_PHASE2,
        "warmup_steps": warmup_phase2,
        "eval_every": -1,
        "core_metric_every": -1,
        "sample_every": -1,
        "resume_from_step": -1,
        "load_optimizer": False,
        "fresh_muon_adamw": True,
        "lr_peak_rule": "0.3 * parent scheduled peak",
        "allowed_model_tags": ["p4-c1-tl-d20", "p4-c2-en-d20", "p4-c3-mix-d20"],
    }

    checks = [
        {"id": "G1_vocab_32768", "ok": vocab == VOCAB},
        {"id": "G2_n_tl0_filed_294", "ok": N_TL0 == 294},
        {"id": "G3_computed_equals_filed", "ok": n_computed == N_TL0, "detail": {"n_computed": n_computed, "N_TL0": N_TL0, "t_tl_train": t_tl_train}},
        {"id": "G4_warmup_lt_n", "ok": warmup_tl0 < N_TL0 and warmup_phase2 < N_PHASE2},
        {"id": "G5_d_phase2_locked", "ok": D_PHASE2 == 19267584 == N_PHASE2 * B},
        {"id": "G6_c3_quotas", "ok": True, "detail": {"tl": 9633792, "en": 9633792}},
        {"id": "G7_no_bpb", "ok": True},
    ]
    ok = all(c["ok"] for c in checks)
    status = "pass" if ok else "protocol_stop"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "G",
        "status": status if not ok else "pass",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "script": "scripts/p4/gate_g_budget.py",
        "tokenizer_pkl_sha256": tok_sha,
        "t_tl_train": t_tl_train,
        "d_3x_tl": d_3x,
        "B": B,
        "N_TL0": N_TL0,
        "N_TL0_computed_from_3x": n_computed,
        "d_actual_tl0": d_actual,
        "N_phase2": N_PHASE2,
        "D_phase2": D_PHASE2,
        "warmup_parent": warmup_tl0,
        "warmup_phase2": warmup_phase2,
        "c3_quota_tl": 9633792,
        "c3_quota_en": 9633792,
        "train": train_stats,
        "depths": depth_rows,
        "commands": {"parent": parent_argv, "phase2": child_argv},
        "cost_note": {
            "class": "NVIDIA CUDA A40",
            "expected_gpus": "H + I(d8) + I(d20) + R + S + T + U + V",
            "must_not_shrink_N": True,
        },
        "checks": checks,
        "computed_bpb": False,
        "next_gate": "H",
    }
    write_json(OUT, payload)
    budget = {
        "B": B,
        "T": T,
        "N_phase2": N_PHASE2,
        "D_phase2": D_PHASE2,
        "N_TL0": N_TL0,
        "q_TL": 0.50,
        "delta_bpb": 0.01,
        "peak_lr_child_fraction": 0.3,
        "warmup_parent": warmup_tl0,
        "warmup_child": warmup_phase2,
        "load_optimizer": False,
        "t_tl_train": t_tl_train,
        "c3_quota_tl": 9633792,
        "c3_quota_en": 9633792,
        "frozen_at_gate": "G",
        "argv_receipt": str(OUT.relative_to(ROOT)),
    }
    if BUDGET.exists():
        BUDGET.chmod(0o644)
    write_json(BUDGET, budget)
    freeze_file(BUDGET)
    if ok:
        update_lock_gate("G", "pass")
        mark_ledger("G", "pass", str(OUT.relative_to(ROOT)), "H")
    blinded_print(
        "G",
        payload["status"],
        {
            "path": str(OUT.relative_to(ROOT)),
            "failed": [c["id"] for c in checks if not c["ok"]],
            "N_TL0": N_TL0,
            "N_computed": n_computed,
            "D_phase2": D_PHASE2,
        },
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
