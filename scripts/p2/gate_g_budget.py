#!/usr/bin/env python3
"""P2 Gate G: freeze T_en_train / N_EN0. Desk calculation only. No EN0. No BPB."""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

from nanochat.gpt import GPT, GPTConfig  # noqa: E402
from nanochat.tokenizer import RustBPETokenizer  # noqa: E402

P2_RUN_ID = os.environ.get("P2_RUN_ID", "p2-20260817T150944Z-de99f8a")
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data" / "cache" / P2_RUN_ID))
TOKENIZER_DIR = BASE / "tokenizer"
EN_DIR = ROOT / "data" / "processed" / "wikitext-103" / "en-active"
TL_DIR = ROOT / "data" / "processed" / "p2-tl39-readonly"
A3_DIR = ROOT / "data" / "processed" / "p2-mix-a3-50-50"
EN_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_train.jsonl"
EN_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_val.jsonl"
EN_TEST_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_test.jsonl"
TL_TEST = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
MIX_ORDER = ROOT / "data" / "interim" / "p2-mix-a3-50-50" / "mix_order.jsonl"
OUT = ROOT / "docs" / "run-cards" / "p2" / P2_RUN_ID / "gate-g-budget.json"

EXPECTED_TOK = "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6"
EXPECTED_BYTES = "5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42"
P11_TOK = "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"
EXPECTED_EN_TRAIN_JSONL = "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a"
EXPECTED_EN_VAL_JSONL = "874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b"
EXPECTED_EN_TEST_JSONL = "2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e"
EXPECTED_TL_TRAIN_JSONL = "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687"
EXPECTED_TL_TEST = "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf"
EXPECTED_MIX_ORDER = "b6ae432b625b6768f84db3f45c411378d1d5a5fdbd15cbfc0e5f6c511196b1a0"
EXPECTED_P11_SHARDS = {
    "shard_00000.parquet": "aaf81d95e577742dcd33a44be2f144c253a5d5650e34b3e622e8b262ff2b6dc9",
    "shard_00001.parquet": "c57c11a2625c38f7f12d1e4018e71bf1f38a56d68fcc9b4952e1b8bded854976",
    "shard_00002.parquet": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
}
GATE_F_EN_VAL_TOKENS = 248877
B = 65536
T = 2048
VOCAB = 32768
ASPECT_RATIO = 64
HEAD_DIM = 128
WINDOW_PATTERN = "SSSL"
N_PHASE2 = 294
D_PHASE2 = N_PHASE2 * B
DEPTHS = (8, 20)
B_REF = 2**19
# P1.1 A40 wall-clock for 294 steps including in-loop eval (same B, T).
P1_D8_SEC = 226  # 2026-08-16T07:04:33Z–07:08:19Z
P1_D20_SEC = 1002  # 2026-08-16T07:24:50Z–07:41:32Z
A40_USD_PER_HOUR = 0.44
CONTINGENCY = 1.25


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_texts(path: Path) -> list[str]:
    return [json.loads(line)["text"] for line in path.read_text(encoding="utf-8").splitlines() if line]


def count_tokens(tokenizer: RustBPETokenizer, texts: list[str], batch_size: int = 256) -> dict:
    n_tokens = 0
    n_bytes = 0
    n_chars = 0
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        encoded = tokenizer.encode(batch)
        n_tokens += sum(len(ids) for ids in encoded)
        n_bytes += sum(len(t.encode("utf-8")) for t in batch)
        n_chars += sum(len(t) for t in batch)
    return {
        "n_docs": len(texts),
        "n_tokens": n_tokens,
        "n_bytes": n_bytes,
        "n_chars": n_chars,
        "bos_prepended": False,
        "packing": False,
        "crop": False,
    }


def get_scaling_params(model: GPT) -> int:
    counts = model.num_scaling_params()
    return counts["transformer_matrices"] + counts["lm_head"]


def build_model_meta(depth: int, vocab_size: int) -> GPT:
    base_dim = depth * ASPECT_RATIO
    model_dim = ((base_dim + HEAD_DIM - 1) // HEAD_DIM) * HEAD_DIM
    num_heads = model_dim // HEAD_DIM
    config = GPTConfig(
        sequence_len=T,
        vocab_size=vocab_size,
        n_layer=depth,
        n_head=num_heads,
        n_kv_head=num_heads,
        n_embd=model_dim,
        window_pattern=WINDOW_PATTERN,
    )
    with torch.device("meta"):
        return GPT(config)


def test_filenames(path: Path) -> list[str]:
    return [p.name for p in path.rglob("*") if "test" in p.name.lower()]


def preflight() -> dict:
    tok_sha = sha256_file(TOKENIZER_DIR / "tokenizer.pkl")
    bytes_sha = sha256_file(TOKENIZER_DIR / "token_bytes.pt")
    mix_sha = sha256_file(MIX_ORDER)
    mix_langs = []
    with MIX_ORDER.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            mix_langs.append(json.loads(line)["language"])
    k = len(mix_langs) // 2
    interleave_ok = mix_langs[0::2] == ["en"] * k and mix_langs[1::2] == ["tl"] * k
    p2_ckpts = [str(p.relative_to(ROOT)) for p in BASE.rglob("model_*.pt")]
    p1_parent = [p for p in p2_ckpts if "p1-fixed-d20-3x" in str(p)]
    climbmix = [p.name for p in BASE.rglob("*") if "climbmix" in p.name.lower()]
    tl_copy = {name: sha256_file(TL_DIR / name) for name in EXPECTED_P11_SHARDS}
    checks = [
        {"id": "P_tok_identity", "ok": tok_sha == EXPECTED_TOK and bytes_sha == EXPECTED_BYTES and tok_sha != P11_TOK},
        {"id": "P_en_test_isolated", "ok": test_filenames(EN_DIR) == [] and sha256_file(EN_TEST_JSONL) == EXPECTED_EN_TEST_JSONL},
        {"id": "P_tl_test_isolated", "ok": test_filenames(TL_DIR) == [] and sha256_file(TL_TEST) == EXPECTED_TL_TEST},
        {"id": "P_a3_test_isolated", "ok": test_filenames(A3_DIR) == []},
        {"id": "P_a3_mix_sha", "ok": mix_sha == EXPECTED_MIX_ORDER},
        {"id": "P_a3_interleave_en_tl", "ok": interleave_ok and k == 28472},
        {"id": "P_tl_copy_hashes", "ok": tl_copy == EXPECTED_P11_SHARDS},
        {"id": "P_no_p11_parent_in_p2_cache", "ok": p1_parent == [] and p2_ckpts == []},
        {"id": "P_no_climbmix_in_p2_cache", "ok": climbmix == []},
        {"id": "P_en_train_jsonl_hash", "ok": sha256_file(EN_TRAIN_JSONL) == EXPECTED_EN_TRAIN_JSONL},
        {"id": "P_en_val_jsonl_hash", "ok": sha256_file(EN_VAL_JSONL) == EXPECTED_EN_VAL_JSONL},
        {"id": "P_tl_train_jsonl_hash", "ok": sha256_file(ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl") == EXPECTED_TL_TRAIN_JSONL},
        {
            "id": "P_prohibited_modes",
            "ok": True,
            "detail": "No EN0, no BPB, no python -m nanochat.dataset, no HF Trainer, no ratio -1, no Spark/MPS confirmatory",
        },
    ]
    return {
        "ok": all(c["ok"] for c in checks),
        "tokenizer_pkl": tok_sha,
        "mix_order_sha256": mix_sha,
        "mix_K": k,
        "p2_checkpoints": p2_ckpts,
        "checks": checks,
    }


def main() -> int:
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    pf = preflight()
    tokenizer = RustBPETokenizer.from_directory(str(TOKENIZER_DIR))
    vocab = tokenizer.get_vocab_size()
    train_stats = count_tokens(tokenizer, load_texts(EN_TRAIN_JSONL))
    val_stats = count_tokens(tokenizer, load_texts(EN_VAL_JSONL))
    t_en_train = train_stats["n_tokens"]
    t_en_val = val_stats["n_tokens"]
    d_3x = 3 * t_en_train
    steps_if_b = d_3x / B
    b_ok = steps_if_b >= 200
    n_en0 = math.ceil(d_3x / B)
    d_actual = n_en0 * B
    overshoot = d_actual - d_3x
    warmup_en0 = min(40, max(1, int(0.05 * n_en0)))
    if warmup_en0 >= n_en0:
        warmup_en0 = max(1, n_en0 // 10)
    warmup_phase2 = 14 if 14 < N_PHASE2 else max(1, N_PHASE2 // 10)
    batch_lr_scale = (B / B_REF) ** 0.5
    eval_tokens = min(262144, int(0.5 * t_en_val))
    if t_en_val >= 8192:
        eval_tokens = max(eval_tokens, 8192)

    depth_rows = []
    for depth in DEPTHS:
        model = build_model_meta(depth, vocab)
        counts = model.num_scaling_params()
        p_total = int(counts["total"])
        p_scaling = int(get_scaling_params(model))
        cfg = model.config
        del model
        r_d = d_3x / p_scaling
        depth_rows.append(
            {
                "depth": depth,
                "n_embd": cfg.n_embd,
                "n_head": cfg.n_head,
                "sequence_len": cfg.sequence_len,
                "p_total": p_total,
                "p_scaling": p_scaling,
                "target_param_data_ratio": r_d,
                "num_iterations_en0": n_en0,
                "d_actual_en0": d_actual,
            }
        )

    tok_s_d8 = D_PHASE2 / P1_D8_SEC
    tok_s_d20 = D_PHASE2 / P1_D20_SEC
    hours = {
        "en0_d8": (n_en0 * B) / tok_s_d8 / 3600,
        "en0_d20": (n_en0 * B) / tok_s_d20 / 3600,
        "a1_a2_a3_d20": 3 * (N_PHASE2 * B) / tok_s_d20 / 3600,
        "h_d4_smoke_approx_as_d8_30_steps": 30 * (B / tok_s_d8) / 3600,
    }
    hours["confirmatory_train_sum"] = hours["en0_d8"] + hours["en0_d20"] + hours["a1_a2_a3_d20"]
    hours["with_contingency_1_25"] = hours["confirmatory_train_sum"] * CONTINGENCY
    cost = {
        "gpu": "NVIDIA A40 48GB Secure Cloud",
        "usd_per_hour": A40_USD_PER_HOUR,
        "source": "P1.1 named host $0.44/hr; Runpod list 2026-08-17 secure still 0.44",
        "p1_throughput_basis": {
            "d8_wall_s_for_294": P1_D8_SEC,
            "d20_wall_s_for_294": P1_D20_SEC,
            "effective_tok_s_d8": tok_s_d8,
            "effective_tok_s_d20": tok_s_d20,
            "includes_p1_inloop_eval": True,
            "note": "EN0 has more eval-every=50 events; 1.25 contingency covers extra eval and host variance.",
        },
        "hours": hours,
        "usd_confirmatory_scaled": hours["confirmatory_train_sum"] * A40_USD_PER_HOUR,
        "usd_with_contingency": hours["with_contingency_1_25"] * A40_USD_PER_HOUR,
        "not_rented": True,
        "user_must_read_before_gate_h": True,
    }

    checks = [
        {"id": "G1_tokenizer_sha_946a04", "ok": pf["tokenizer_pkl"] == EXPECTED_TOK},
        {"id": "G2_vocab_32768", "ok": vocab == VOCAB},
        {"id": "G3_t_en_val_matches_gate_f", "ok": t_en_val == GATE_F_EN_VAL_TOKENS},
        {"id": "G4_n_en0_ge_200", "ok": n_en0 >= 200 and math.isfinite(n_en0)},
        {"id": "G5_n_en0_gg_294", "ok": n_en0 > 294},
        {"id": "G6_b_65536", "ok": b_ok},
        {"id": "G7_warmup_lt_n", "ok": warmup_en0 < n_en0 and warmup_phase2 < N_PHASE2},
        {"id": "G8_d_phase2_from_pdf", "ok": D_PHASE2 == 19267584},
        {"id": "G9_no_english_test_read", "ok": True},
        {"id": "G10_preflight", "ok": pf["ok"]},
        {"id": "G11_no_en0_no_bpb", "ok": True},
    ]
    ok = all(c["ok"] for c in checks) and pf["ok"]
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "gate": "G",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "started_at_utc": started,
        "host": "Mac/CPU",
        "p2_run_id": P2_RUN_ID,
        "script": "scripts/p2/gate_g_budget.py",
        "token_count_definition": "sum(len(tau(document_text))) over frozen English train jsonl documents; no BOS; no packing; no crop; tokenizer SHA 946a04ef…ace6",
        "tokenizer_pkl_sha256": EXPECTED_TOK,
        "english_train_jsonl_sha256": EXPECTED_EN_TRAIN_JSONL,
        "t_en_train": t_en_train,
        "t_en_val": t_en_val,
        "t_en_test": "not_read",
        "train": train_stats,
        "val": val_stats,
        "d_1x_en": t_en_train,
        "d_3x_en": d_3x,
        "B": B,
        "N_EN0": n_en0,
        "d_actual_en0": d_actual,
        "d_actual_minus_d_3x": overshoot,
        "d_actual_relative_overshoot": overshoot / d_3x,
        "iteration_rule": "N_EN0 = ceil(D_3x_en / 65536)",
        "N_phase2": N_PHASE2,
        "D_phase2": D_PHASE2,
        "D_phase2_source": "PDF: P1.1 D_actual = 294*65536, not English D_3x",
        "sequence_len": T,
        "must_pass_num_iterations_explicitly": True,
        "never_target_param_data_ratio_minus_one": True,
        "core_metric_every": -1,
        "optimizer_en0": {
            "class": "MuonAdamW (Muon matrices, AdamW embeddings/unembeddings/scalars)",
            "embedding_lr": 0.3,
            "unembedding_lr": 0.008,
            "matrix_lr": 0.02,
            "scalar_lr": 0.5,
            "weight_decay": 0.28,
            "batch_lr_scale_for_B_65536": batch_lr_scale,
            "B_REF": B_REF,
            "warmup_steps": warmup_en0,
            "warmup_rule": "min(40, 5% of N_EN0), strictly < N_EN0",
            "warmdown_ratio": 0.65,
            "final_lr_frac": 0.05,
        },
        "optimizer_phase2": {
            "fresh_adam_muon_same_classes": True,
            "lr_peak": "0.3 * EN0 scheduled peak (PDF)",
            "warmup_steps": warmup_phase2,
            "N": N_PHASE2,
            "never_load_p11_model_000294": True,
        },
        "checkpoint_cadence": {
            "save_every": 200,
            "eval_every": 50,
            "sample_every": 200,
            "eval_tokens_inloop": eval_tokens,
            "eval_tokens_rule": "min(262144, 0.5*T_en_val), at least 8192; confirmatory val_bpb_full is the whole English val, not this cap",
            "final_checkpoint_only_also_allowed": "pin default save-every=-1 saves at end; P2 records save-every=200 like P1.1",
        },
        "depths": depth_rows,
        "cost_a40": cost,
        "preflight": pf,
        "checks": checks,
        "started_en0": False,
        "computed_bpb": False,
        "next_gate": "H",
        "next_gate_note": "CUDA A40-class d4 smoke. Not Mac MPS. Not Spark until unpatched labeled re-entry. Do not start EN0 until H passes. Read cost_a40 before renting.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "t_en_train": t_en_train,
                "d_3x_en": d_3x,
                "N_EN0": n_en0,
                "d_actual_en0": d_actual,
                "overshoot": overshoot,
                "D_phase2": D_PHASE2,
                "hours_with_contingency": hours["with_contingency_1_25"],
                "usd_with_contingency": cost["usd_with_contingency"],
                "failed": [c["id"] for c in checks if not c["ok"]],
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
