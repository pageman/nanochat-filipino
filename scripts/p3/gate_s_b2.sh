#!/usr/bin/env bash
# P3 Gate S: B2 English intervention from frozen B0.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
source scripts/p3/env.cuda.sh
export NANOCHAT_DATA_DIR="${NANOCHAT_DATA_DIR_EN:?}"
export NANOCHAT_BASE_DIR="${NANOCHAT_BASE_DIR:?}"
TAG="p3-b2-en-d20"
FROZEN="${NANOCHAT_BASE_DIR}/b0/frozen/p3-tl0-d20"
LOCK="${P3_LOCKBOX_ROOT}/gate-s-b2-full.log"
mkdir -p "$(dirname "$LOCK")"
: >"${P3_SAFE_PROGRESS_ROOT}/gate-s-b2-progress.txt"
echo "gate_s_started utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"${P3_SAFE_PROGRESS_ROOT}/gate-s-b2-progress.txt"
set +e
python scripts/p3/continue_from_frozen.py \
  --init-from "$FROZEN" --init-step 294 \
  --expected-sha ae621be2c90a3d295f8d21b0e53cb9d4b717803f5d5337fa68f3c3f84d57193c \
  --allowed-model-tag "$TAG" -- \
  --device-type=cuda --depth=20 --max-seq-len=2048 --window-pattern=SSSL \
  --device-batch-size=8 --total-batch-size=65536 --num-iterations=294 --warmup-steps=14 \
  --embedding-lr=0.09 --unembedding-lr=0.0024 --matrix-lr=0.006 --scalar-lr=0.15 --weight-decay=0.28 \
  --eval-every=-1 --core-metric-every=-1 --sample-every=-1 --save-every=-1 \
  --model-tag="$TAG" --run="$TAG" >"$LOCK" 2>&1
RC=$?
set -e
chmod 600 "$LOCK" 2>/dev/null || true
python scripts/p3/gate_phase2_accept.py --gate S --arm b2 --model-tag "$TAG" \
  --stream english_train --data-dir "$NANOCHAT_DATA_DIR" --exit-code "$RC"
exit $?
