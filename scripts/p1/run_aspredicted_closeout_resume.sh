#!/usr/bin/env bash
# Resume after D_1x val_one looked for step 294. No test read.
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
PY="$P1_ROOT/vendor/nanochat/.venv/bin/python"
OUT=/workspace/exports/gate_j
LOG="$OUT/closeout.log"
cd "$P1_ROOT/vendor/nanochat"

echo "RESUME $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"

"$PY" "$P1_ROOT/scripts/p1/gate_j_full_bpb.py" \
  --phase val_one --device-type cuda --device-batch-size 8 \
  --model-tag p1-fixed-d8-1x-s0 --out-dir "$OUT" 2>&1 | tee -a "$LOG"

echo "START p1-fixed-d12-1x-s0 seed=42 $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
"$PY" "$P1_ROOT/scripts/p1/run_seeded_base_train.py" --p1-seed 42 -- \
  --device-type=cuda --depth=12 --max-seq-len=2048 \
  --device-batch-size=8 --total-batch-size=65536 --num-iterations=98 \
  --target-param-data-ratio=0.05813769281039198 \
  --eval-tokens=262144 --eval-every=50 --core-metric-every=-1 \
  --sample-every=200 --save-every=200 --warmup-steps=4 \
  --run=p1-fixed-d12-1x-s0 --model-tag=p1-fixed-d12-1x-s0 \
  2>&1 | tee "$OUT/p1-fixed-d12-1x-s0.train.log"

"$PY" "$P1_ROOT/scripts/p1/gate_j_full_bpb.py" \
  --phase val_one --device-type cuda --device-batch-size 8 \
  --model-tag p1-fixed-d12-1x-s0 --out-dir "$OUT" 2>&1 | tee -a "$LOG"

echo "BOOTSTRAP $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
for tag in p1-fixed-d8-3x p1-fixed-d12-3x p1-fixed-d16-3x p1-fixed-d20-3x; do
  "$PY" "$P1_ROOT/scripts/p1/gate_j_full_bpb.py" \
    --phase bootstrap_val --device-type cuda --device-batch-size 8 \
    --model-tag "$tag" --out-dir "$OUT" 2>&1 | tee -a "$LOG"
done

echo "CLOSEOUT_DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
