"""P4 phase-2 (C1/C2/C3) shared constants. Not a rename of scripts/p3."""

from __future__ import annotations

import json
from pathlib import Path

from p4_common import N_PHASE2, N_TL0, RUN_CARD, TOKENIZER_PKL_SHA, WARMUP

C0_SOURCE_TAG = "p4-tl0-d20"
C0_TAG = "p4-c0-tl-d20"
C1_TAG = "p4-c1-tl-d20"
C2_TAG = "p4-c2-en-d20"
C3_TAG = "p4-c3-mix-d20"
C0_STEP = N_TL0
DEPTH = 20
TOKENIZER_SHA = TOKENIZER_PKL_SHA
PROTOCOL_ALIAS_C1 = "p4-c1-extra-tl-d20"

PHASE2_TRAIN_ARGS = [
    "--device-type=cuda",
    "--depth=20",
    "--max-seq-len=2048",
    "--window-pattern=SSSL",
    "--device-batch-size=8",
    "--total-batch-size=65536",
    "--num-iterations=294",
    "--warmup-steps=14",
    "--embedding-lr=0.09",
    "--unembedding-lr=0.0024",
    "--matrix-lr=0.006",
    "--scalar-lr=0.15",
    "--weight-decay=0.28",
    "--eval-every=-1",
    "--core-metric-every=-1",
    "--sample-every=-1",
    "--save-every=-1",
]


def load_c0_sha() -> str:
    path = RUN_CARD / "gate-q-c0-freeze.json"
    if not path.is_file():
        raise SystemExit("missing Gate Q receipt; freeze C0 first")
    row = json.loads(path.read_text(encoding="utf-8"))
    if row.get("status") != "pass":
        raise SystemExit("Gate Q not pass")
    return row["checkpoint_sha256"]
