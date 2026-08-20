"""P3 phase-2 (B1/B2/B3) shared constants."""

from __future__ import annotations

B0_TAG = "p3-tl0-d20"
B0_STEP = 294
B0_SHA256 = "ae621be2c90a3d295f8d21b0e53cb9d4b717803f5d5337fa68f3c3f84d57193c"
B1_TAG = "p3-b1-extra-tl-d20"
B2_TAG = "p3-b2-en-d20"
B3_TAG = "p3-b3-mix-d20"
N_PHASE2 = 294
WARMUP = 14
DEPTH = 20
TOKENIZER_SHA = "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"

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
