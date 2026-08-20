#!/usr/bin/env python3
"""P3 Gate G: freeze T_tl_train, N_TL0, argv. Desk calc only. No BPB."""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch

from p3_common import (
    ASPREDICTED_ID,
    B,
    BASE,
    D_PHASE2,
    N_PHASE2,
    P3_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TL_TRAIN_JSONL,
    T,
    VOCAB,
    VENDOR,
)

sys.path.insert(0, str(VENDOR))
from nanochat.gpt import GPT, GPTConfig  # noqa: E402
from nanochat.tokenizer import RustBPETokenizer  # noqa: E402

OUT = RUN_CARD / "gate-g-budget-command-freeze.json"
DEPTHS = (8, 20)
ASPECT_RATIO = 64
HEAD_DIM = 128
WINDOW_PATTERN = "SSSL"
P1_D8_SEC = 226
P1_D20_SEC = 1002


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_texts(path: Path) -> list[str]:
    return [json.loads(line)["text"] for line in path.read_text(encoding="utf-8").splitlines() if line]


def count_tokens(tokenizer: RustBPETokenizer, texts: list[str], batch_size: int = 256) -> dict:
    n_tokens = n_bytes = n_chars = 0
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        encoded = tokenizer.encode(batch)
        n_tokens += sum(len(ids) for ids in encoded)
        n_bytes += sum(len(t.encode("utf-8")) for t in batch)
        n_chars += sum(len(t) for t in batch)
    return {"n_docs": len(texts), "n_tokens": n_tokens, "n_bytes": n_bytes, "n_chars": n_chars, "bos_prepended": False, "packing": False, "crop": False}


def build_model_meta(depth: int, vocab_size: int) -> GPT:
    base_dim = depth * ASPECT_RATIO
    model_dim = ((base_dim + HEAD_DIM - 1) // HEAD_DIM) * HEAD_DIM
    num_heads = model_dim // HEAD_DIM
    config = GPTConfig(sequence_len=T, vocab_size=vocab_size, n_layer=depth, n_head=num_heads, n_kv_head=num_heads, n_embd=model_dim, window_pattern=WINDOW_PATTERN)
    with torch.device("meta"):
        return GPT(config)


def main() -> int:
    tok_dir = BASE / "tokenizer"
    tok_sha = sha256_file(tok_dir / "tokenizer.pkl")
    tokenizer = RustBPETokenizer.from_directory(str(tok_dir))
    vocab = tokenizer.get_vocab_size()
    train_stats = count_tokens(tokenizer, load_texts(TL_TRAIN_JSONL))
    t_tl_train = train_stats["n_tokens"]
    d_3x = 3 * t_tl_train
    n_tl0 = math.ceil(d_3x / B)
    d_actual = n_tl0 * B
    warmup_tl0 = min(40, max(1, int(0.05 * n_tl0)))
    if warmup_tl0 >= n_tl0:
        warmup_tl0 = max(1, n_tl0 // 10)
    warmup_phase2 = 14 if 14 < N_PHASE2 else max(1, N_PHASE2 // 10)

    depth_rows = []
    for depth in DEPTHS:
        model = build_model_meta(depth, vocab)
        counts = model.num_scaling_params()
        depth_rows.append({"depth": depth, "p_scaling": int(counts["transformer_matrices"] + counts["lm_head"]), "num_iterations_tl0": n_tl0})

    tl0_argv = {
        "depths": list(DEPTHS),
        "num_iterations": n_tl0,
        "max_seq_len": T,
        "window_pattern": WINDOW_PATTERN,
        "device_batch_size": 8,
        "total_batch_size": B,
        "eval_every": -1,
        "core_metric_every": -1,
        "sample_every": -1,
        "save_every": -1,
        "warmup_steps": warmup_tl0,
        "model_tags": ["p3-tl0-d8", "p3-tl0-d20"],
    }
    phase2_argv = {
        "num_iterations": N_PHASE2,
        "D_phase2": D_PHASE2,
        "warmup_steps": warmup_phase2,
        "load_optimizer": False,
        "fresh_muon_adamw": True,
        "lr_peak_rule": "0.3 * TL0 scheduled peak",
        "opaque_labels": {"job-amber": "B1", "job-cobalt": "B2", "job-cedar": "B3"},
    }

    checks = [
        {"id": "G1_vocab_32768", "ok": vocab == VOCAB},
        {"id": "G2_n_tl0_ge_200", "ok": n_tl0 >= 200},
        {"id": "G3_warmup_lt_n", "ok": warmup_tl0 < n_tl0 and warmup_phase2 < N_PHASE2},
        {"id": "G4_d_phase2_locked", "ok": D_PHASE2 == 19267584},
        {"id": "G5_no_bpb", "ok": True},
    ]
    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "G",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_g_budget.py",
        "tokenizer_pkl_sha256": tok_sha,
        "t_tl_train": t_tl_train,
        "d_3x_tl": d_3x,
        "B": B,
        "N_TL0": n_tl0,
        "d_actual_tl0": d_actual,
        "N_phase2": N_PHASE2,
        "D_phase2": D_PHASE2,
        "train": train_stats,
        "depths": depth_rows,
        "commands": {"tl0": tl0_argv, "phase2": phase2_argv},
        "cost_note": {"p1_d8_sec_294": P1_D8_SEC, "p1_d20_sec_294": P1_D20_SEC, "user_must_read_before_gate_h": True},
        "checks": checks,
        "computed_bpb": False,
        "next_gate": "H",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "t_tl_train": t_tl_train, "N_TL0": n_tl0, "D_phase2": D_PHASE2, "failed": [c["id"] for c in checks if not c["ok"]]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
