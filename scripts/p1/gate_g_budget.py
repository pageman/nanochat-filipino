#!/usr/bin/env python3
"""Gate G: desk-calculate T_train, D_3x, P_scaling, and D_actual.

Does not train. Does not read the isolated test split. Instantiates
models on the meta device only to capture parameter counts.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

from nanochat.gpt import GPT, GPTConfig  # noqa: E402
from nanochat.tokenizer import RustBPETokenizer  # noqa: E402

RUN_ID = "p1-20260816T025911Z-0067a57"
NANOCHAT_COMMIT = "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
DEPTHS = (8, 12, 16, 20)
SEQUENCE_LEN = 2048
ASPECT_RATIO = 64
HEAD_DIM = 128
WINDOW_PATTERN = "SSSL"
VOCAB_SIZE_EXPECTED = 32768

SPLIT = json.loads((ROOT / "manifests" / "split_manifest.json").read_text(encoding="utf-8"))
TOKENIZER_MANIFEST = json.loads(
    (ROOT / "manifests" / "tokenizer_manifest.json").read_text(encoding="utf-8")
)
TOKENIZER_DIR = ROOT / "data" / "cache" / RUN_ID / "tokenizer"
TRAIN_JSONL = ROOT / SPLIT["paths"]["train"]
VAL_JSONL = ROOT / SPLIT["paths"]["val"]
FERTILITY_PATH = ROOT / "artifacts" / "p1" / RUN_ID / "tokenizer_eval.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_texts(path: Path) -> list[str]:
    return [json.loads(line)["text"] for line in path.read_text(encoding="utf-8").splitlines() if line]


def count_tokens(tokenizer: RustBPETokenizer, texts: list[str], batch_size: int = 512) -> dict:
    n_tokens = 0
    n_bytes = 0
    n_chars = 0
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        encoded = tokenizer.encode(batch)  # no prepend => no BOS
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
    """Pinned scripts/base_train.py get_scaling_params (commit 92d63d4)."""
    params_counts = model.num_scaling_params()
    return params_counts["transformer_matrices"] + params_counts["lm_head"]


def build_model_meta(depth: int, vocab_size: int) -> GPT:
    """Pinned scripts/base_train.py build_model_meta, T=2048 frozen."""
    base_dim = depth * ASPECT_RATIO
    model_dim = ((base_dim + HEAD_DIM - 1) // HEAD_DIM) * HEAD_DIM
    num_heads = model_dim // HEAD_DIM
    config = GPTConfig(
        sequence_len=SEQUENCE_LEN,
        vocab_size=vocab_size,
        n_layer=depth,
        n_head=num_heads,
        n_kv_head=num_heads,
        n_embd=model_dim,
        window_pattern=WINDOW_PATTERN,
    )
    with torch.device("meta"):
        return GPT(config)


def choose_common_total_batch_size(d_3x: int) -> dict:
    """Largest power-of-two multiple of T that still yields >= 200 steps.

    Locked before any confirmatory BPB. device_batch_size may later shrink
    on the GPU host; this total is preserved through gradient accumulation.
    """
    if d_3x <= 0:
        raise SystemExit("D_3x must be positive")
    max_b = d_3x // 200
    candidates = []
    b = SEQUENCE_LEN
    while b <= max_b:
        if b & (b - 1) == 0:  # power of two
            candidates.append(b)
        b += SEQUENCE_LEN
    if not candidates:
        raise SystemExit(
            f"no power-of-two multiple of {SEQUENCE_LEN} is <= D_3x/200={max_b}"
        )
    chosen = max(candidates)
    return {
        "common_total_batch_size": chosen,
        "rule": (
            "largest power-of-two multiple of max_seq_len=2048 such that "
            "B <= D_3x/200 (at least 200 optimizer steps)"
        ),
        "max_b_for_200_steps": max_b,
        "candidates_considered": candidates,
        "nanochat_b_ref_not_used": 524288,
        "reason_not_b_ref": (
            "B_REF=524288 is the ClimbMix-scale default and would yield "
            "fewer than 40 steps here, making warmup degenerate"
        ),
    }


def write_json(path: Path, payload: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    started = utc_now()
    errors: list[str] = []

    tok_hash = sha256_file(TOKENIZER_DIR / "tokenizer.pkl")
    expected_tok = TOKENIZER_MANIFEST["hashes"]["tokenizer.pkl"]
    if tok_hash != expected_tok:
        errors.append(f"tokenizer.pkl hash mismatch: {tok_hash} != {expected_tok}")

    train_hash = sha256_file(TRAIN_JSONL)
    expected_train = SPLIT["file_sha256"]["train"]
    if train_hash != expected_train:
        errors.append(f"train.jsonl hash mismatch: {train_hash} != {expected_train}")

    val_hash = sha256_file(VAL_JSONL)
    expected_val = SPLIT["file_sha256"]["val"]
    if val_hash != expected_val:
        errors.append(f"val.jsonl hash mismatch: {val_hash} != {expected_val}")

    if errors:
        json.dump({"ok": False, "errors": errors}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 2

    tokenizer = RustBPETokenizer.from_directory(str(TOKENIZER_DIR))
    vocab_size = tokenizer.get_vocab_size()
    if vocab_size != VOCAB_SIZE_EXPECTED:
        json.dump({"ok": False, "errors": [f"vocab_size={vocab_size}"]}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 2

    train_stats = count_tokens(tokenizer, load_texts(TRAIN_JSONL))
    val_stats = count_tokens(tokenizer, load_texts(VAL_JSONL))
    t_train = train_stats["n_tokens"]
    t_val = val_stats["n_tokens"]

    fertility = json.loads(FERTILITY_PATH.read_text(encoding="utf-8"))
    fertility_train = fertility["fertility"]["train"]["n_tokens"]
    fertility_val = fertility["fertility"]["val"]["n_tokens"]
    fertility_test = fertility["fertility"]["test"]["n_tokens"]
    if t_train != fertility_train:
        errors.append(f"T_train {t_train} != Gate F fertility train {fertility_train}")
    if t_val != fertility_val:
        errors.append(f"T_val {t_val} != Gate F fertility val {fertility_val}")

    d_1x = t_train
    d_3x = 3 * t_train
    d_10x = 10 * t_train

    batch_choice = choose_common_total_batch_size(d_3x)
    common_b = batch_choice["common_total_batch_size"]
    num_iterations = math.ceil(d_3x / common_b)
    d_actual = num_iterations * common_b

    depth_rows = []
    blocked = []
    for depth in DEPTHS:
        try:
            model = build_model_meta(depth, vocab_size)
            counts = model.num_scaling_params()
            p_total = int(counts["total"])
            p_scaling = int(get_scaling_params(model))
            cfg = model.config
            del model
        except Exception as exc:  # noqa: BLE001
            blocked.append({"depth": depth, "error": str(exc)})
            continue
        if p_scaling <= 0:
            blocked.append({"depth": depth, "error": f"non-positive P_scaling={p_scaling}"})
            continue
        r_d = d_3x / p_scaling
        if r_d <= 0:
            blocked.append({"depth": depth, "error": f"non-positive R_d={r_d}"})
            continue
        depth_rows.append(
            {
                "depth": depth,
                "n_embd": cfg.n_embd,
                "n_head": cfg.n_head,
                "n_kv_head": cfg.n_kv_head,
                "n_layer": cfg.n_layer,
                "sequence_len": cfg.sequence_len,
                "window_pattern": cfg.window_pattern,
                "p_total": p_total,
                "p_scaling": p_scaling,
                "param_counts": {k: int(v) for k, v in counts.items()},
                "target_param_data_ratio": r_d,
                "target_param_data_ratio_must_stay_positive": True,
                "never_pass_target_param_data_ratio_minus_one": True,
                "total_batch_size": common_b,
                "num_iterations": num_iterations,
                "d_actual": d_actual,
                "d_actual_minus_d_3x": d_actual - d_3x,
                "d_actual_over_d_3x": d_actual / d_3x,
                "r_d_nominal": r_d,
                "r_d_actual": d_actual / p_scaling,
            }
        )

    if blocked:
        json.dump({"ok": False, "errors": errors, "blocked_depths": blocked}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 3

    if errors:
        json.dump({"ok": False, "errors": errors}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 2

    eval_tokens = min(262144, int(0.5 * t_val))
    if t_val >= 8192:
        eval_tokens = max(eval_tokens, 8192)
    warmup_steps = min(40, max(1, int(0.05 * num_iterations)))

    token_statistics = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "run_id": RUN_ID,
        "gate": "G",
        "definition": (
            "sum(len(tokenizer.encode(document_text))) over frozen canonical "
            "split documents; no BOS; no packing; no crop"
        ),
        "tokenizer_hash": tok_hash,
        "train_split_hash": train_hash,
        "val_split_hash": val_hash,
        "t_train": t_train,
        "t_val": t_val,
        "t_test": fertility_test,
        "t_test_source": "gate_f_fertility_not_reread",
        "t_test_note": (
            "Cited from artifacts/p1/.../tokenizer_eval.json to avoid a new "
            "test-split read. Not confirmatory test_bpb."
        ),
        "train": train_stats,
        "val": val_stats,
        "bytes": {
            "train": train_stats["n_bytes"],
            "val": val_stats["n_bytes"],
        },
        "matched_gate_f_fertility_train_val": True,
        "test_not_reread": True,
    }

    budget_manifest = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "run_id": RUN_ID,
        "gate": "G",
        "status": "pass",
        "budget_label": "D_3x",
        "token_count_definition": (
            "sum(len(tau(document_text))) over frozen canonical train "
            "documents; no BOS; no packing; no crop"
        ),
        "tokenizer_hash": tok_hash,
        "train_split_hash": train_hash,
        "t_train": t_train,
        "t_val": t_val,
        "d_1x": d_1x,
        "d_3x": d_3x,
        "d_10x": d_10x,
        "d_10x_is_exploratory": True,
        "sequence_length": SEQUENCE_LEN,
        "common_total_batch_size": common_b,
        "common_total_batch_size_rule": batch_choice,
        "num_iterations": num_iterations,
        "d_actual": d_actual,
        "d_actual_minus_d_3x": d_actual - d_3x,
        "d_actual_relative_overshoot": (d_actual - d_3x) / d_3x,
        "iteration_rule": "num_iterations = ceil(D_3x / total_batch_size)",
        "must_pass_num_iterations_explicitly": True,
        "do_not_use_trainer_floor_from_ratio": (
            "pinned base_train.py uses target_tokens // total_batch_size "
            "(floor) when --num-iterations is omitted; Gate I must pass "
            "--num-iterations explicitly so D_actual matches this manifest"
        ),
        "never_target_param_data_ratio_minus_one": True,
        "recommended_overrides_not_executed": {
            "eval_tokens": eval_tokens,
            "eval_tokens_rule": "min(262144, 0.5 * T_val), at least 8192",
            "warmup_steps": warmup_steps,
            "warmup_steps_rule": "min(40, 5% of num_iterations)",
            "device_batch_size": (
                "set on the named GPU host; start at 8 and halve until VRAM "
                "fits; preserve common_total_batch_size via grad accum; "
                "do not change T=2048 or B"
            ),
            "core_metric_every": -1,
            "max_seq_len": SEQUENCE_LEN,
        },
        "note": "Desk calculation only. No confirmatory training. No test BPB.",
        "depths": [
            {
                "depth": row["depth"],
                "p_total": row["p_total"],
                "p_scaling": row["p_scaling"],
                "target_param_data_ratio": row["target_param_data_ratio"],
                "total_batch_size": row["total_batch_size"],
                "num_iterations": row["num_iterations"],
                "d_actual": row["d_actual"],
            }
            for row in depth_rows
        ],
        "depth_details": depth_rows,
        "architecture_defaults": {
            "aspect_ratio": ASPECT_RATIO,
            "head_dim": HEAD_DIM,
            "window_pattern": WINDOW_PATTERN,
            "vocab_size": vocab_size,
            "source": "vendor/nanochat/scripts/base_train.py build_model_meta",
            "nanochat_commit": NANOCHAT_COMMIT,
        },
        "p_scaling_method": (
            "transformer_matrices + lm_head from model.num_scaling_params(); "
            "see manifests/p_scaling_capture.json"
        ),
    }

    token_hash = write_json(ROOT / "manifests" / "token_statistics.json", token_statistics)
    write_json(ROOT / "data" / "manifests" / "token_statistics.json", token_statistics)
    budget_hash = write_json(ROOT / "manifests" / "budget_manifest.json", budget_manifest)

    checks = {
        "test_t_train_count": t_train == fertility_train and t_train > 0,
        "test_ratio_positive": all(row["target_param_data_ratio"] > 0 for row in depth_rows),
        "test_budget_math": all(
            row["d_actual"] == row["num_iterations"] * row["total_batch_size"]
            and row["d_actual"] == d_actual
            and row["total_batch_size"] == common_b
            for row in depth_rows
        ),
        "sequence_length_2048": all(row["sequence_len"] == SEQUENCE_LEN for row in depth_rows),
        "four_registered_depths": [row["depth"] for row in depth_rows] == list(DEPTHS),
        "hashes_matched": True,
        "test_not_reread": True,
        "no_training": True,
    }
    ok = all(checks.values()) and not blocked and not errors

    payload = {
        "ok": ok,
        "gate": "G",
        "status": "pass" if ok else "stop",
        "run_id": RUN_ID,
        "started_at_utc": started,
        "ended_at_utc": utc_now(),
        "t_train": t_train,
        "t_val": t_val,
        "d_3x": d_3x,
        "common_total_batch_size": common_b,
        "num_iterations": num_iterations,
        "d_actual": d_actual,
        "depths": [
            {
                "depth": row["depth"],
                "p_total": row["p_total"],
                "p_scaling": row["p_scaling"],
                "target_param_data_ratio": row["target_param_data_ratio"],
            }
            for row in depth_rows
        ],
        "checks": checks,
        "hashes": {
            "tokenizer.pkl": tok_hash,
            "train.jsonl": train_hash,
            "val.jsonl": val_hash,
            "budget_manifest.json": budget_hash,
            "token_statistics.json": token_hash,
        },
        "artifacts": [
            "manifests/budget_manifest.json",
            "manifests/token_statistics.json",
            "data/manifests/token_statistics.json",
            "scripts/p1/gate_g_budget.py",
        ],
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
