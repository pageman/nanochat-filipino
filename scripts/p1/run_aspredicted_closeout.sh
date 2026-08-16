#!/usr/bin/env bash
# Extra seeds, D_1x pilots, D* samples, document bootstrap. No test reread.
set -euo pipefail
export P1_ROOT=/workspace/p1/nanochat-filipino
export RUN_ID=p1-20260816T025911Z-0067a57
export NANOCHAT_BASE_DIR="$P1_ROOT/data/cache/${RUN_ID}"
export NANOCHAT_DATA_DIR="$P1_ROOT/data/processed/wikitext-tl39/active"
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=1
export PYTHONPATH="$P1_ROOT/vendor/nanochat"
export WANDB_MODE=offline
export WANDB_DISABLED=true
export WANDB_RUN=dummy
VENV="$P1_ROOT/vendor/nanochat/.venv"
PY="$VENV/bin/python"
OUT=/workspace/exports/gate_j
LOG="$OUT/closeout.log"
mkdir -p "$OUT"
cd "$P1_ROOT/vendor/nanochat"

if [ -e "$P1_ROOT/data/processed/wikitext-tl39/test/test.jsonl" ]; then
  echo "TEST_IN_STANDARD_PATH" >&2
  exit 2
fi

echo "CLOSEOUT_START $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"

echo "SAMPLES $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
P1_SAMPLE_OUT="$OUT/samples_d20.json" "$PY" "$P1_ROOT/scripts/p1/gate_j_samples.py" 2>&1 | tee -a "$LOG"

run_seeded() {
  local depth="$1"
  local ratio="$2"
  local seed="$3"
  local tag="$4"
  local iters="$5"
  local warmup="$6"
  echo "START ${tag} seed=${seed} $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
  "$PY" "$P1_ROOT/scripts/p1/run_seeded_base_train.py" --p1-seed "$seed" -- \
    --device-type=cuda \
    --depth="$depth" \
    --max-seq-len=2048 \
    --device-batch-size=8 \
    --total-batch-size=65536 \
    --num-iterations="$iters" \
    --target-param-data-ratio="$ratio" \
    --eval-tokens=262144 \
    --eval-every=50 \
    --core-metric-every=-1 \
    --sample-every=200 \
    --save-every=200 \
    --warmup-steps="$warmup" \
    --run="$tag" \
    --model-tag="$tag" \
    2>&1 | tee "$OUT/${tag}.train.log"
  "$PY" "$P1_ROOT/scripts/p1/gate_j_full_bpb.py" \
    --phase val_one --device-type cuda --device-batch-size 8 \
    --model-tag "$tag" --out-dir "$OUT" 2>&1 | tee -a "$LOG"
  echo "END ${tag} $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
}

# Q7 extra seeds at d8/d12 only. s0 already used nanochat default 42.
run_seeded 8 0.45783403148331536 1 p1-fixed-d8-3x-s1 294 14
run_seeded 8 0.45783403148331536 2 p1-fixed-d8-3x-s2 294 14
run_seeded 12 0.17441307843117593 1 p1-fixed-d12-3x-s1 294 14
run_seeded 12 0.17441307843117593 2 p1-fixed-d12-3x-s2 294 14

# Q8 secondary D_1x pilots, seed 42 / label s0. Not confirmatory.
run_seeded 8 0.15261134382777178 42 p1-fixed-d8-1x-s0 98 4
run_seeded 12 0.05813769281039198 42 p1-fixed-d12-1x-s0 98 4

echo "BOOTSTRAP $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
for tag in p1-fixed-d8-3x p1-fixed-d12-3x p1-fixed-d16-3x p1-fixed-d20-3x; do
  "$PY" "$P1_ROOT/scripts/p1/gate_j_full_bpb.py" \
    --phase bootstrap_val --device-type cuda --device-batch-size 8 \
    --model-tag "$tag" --out-dir "$OUT" 2>&1 | tee -a "$LOG"
done

echo "CLOSEOUT_DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
