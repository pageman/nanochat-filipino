#!/usr/bin/env python3
"""Prove P5 parent-init seeds 1,2,3 yield distinct initial model states before training."""

from __future__ import annotations

import hashlib
import io
import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "vendor" / "nanochat"))

from p5_common import PANEL_SEEDS, T, VOCAB, WRAPPER_RNG_SEED, sha256_file, utc_now, write_json  # noqa: E402
from nanochat.gpt import GPT, GPTConfig  # noqa: E402

OUT = ROOT / "docs" / "run-cards" / "p5" / "seed-knob-proof.json"
SCRIPT_SHA = sha256_file(Path(__file__))
ASPECT_RATIO = 64
HEAD_DIM = 128
WINDOW_PATTERN = "SSSL"


def build_config(depth: int) -> GPTConfig:
    base_dim = depth * ASPECT_RATIO
    model_dim = ((base_dim + HEAD_DIM - 1) // HEAD_DIM) * HEAD_DIM
    num_heads = model_dim // HEAD_DIM
    return GPTConfig(
        sequence_len=T,
        vocab_size=VOCAB,
        n_layer=depth,
        n_head=num_heads,
        n_kv_head=num_heads,
        n_embd=model_dim,
        window_pattern=WINDOW_PATTERN,
    )


def initial_state_sha(seed: int, depth: int = 8) -> str:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
    config = build_config(depth)
    model = GPT(config)
    model.init_weights()
    buf = io.BytesIO()
    torch.save(model.state_dict(), buf)
    return hashlib.sha256(buf.getvalue()).hexdigest()


def main() -> int:
    rows = {}
    for s in PANEL_SEEDS:
        rows[str(s)] = {"d8_initial_state_sha256": initial_state_sha(s, 8), "d20_initial_state_sha256": initial_state_sha(s, 20)}
    d8 = [rows[str(s)]["d8_initial_state_sha256"] for s in PANEL_SEEDS]
    d20 = [rows[str(s)]["d20_initial_state_sha256"] for s in PANEL_SEEDS]
    ok = len(set(d8)) == len(PANEL_SEEDS) and len(set(d20)) == len(PANEL_SEEDS)
    payload = {
        "gate": "A-seed-knob",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "wrapper_script_sha256": SCRIPT_SHA,
        "wrapper_numpy_rng_seed": WRAPPER_RNG_SEED,
        "panel_seeds": list(PANEL_SEEDS),
        "rows": rows,
        "all_distinct_d8": len(set(d8)) == len(PANEL_SEEDS),
        "all_distinct_d20": len(set(d20)) == len(PANEL_SEEDS),
        "blinded": True,
        "no_training": True,
    }
    write_json(OUT, payload)
    print(json.dumps({"status": payload["status"], "path": str(OUT.relative_to(ROOT)), "distinct": ok}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
