#!/usr/bin/env bash
# P3 Gate H: Tagalog-path d4 CUDA smoke (NOT TL0).
# Run on NVIDIA CUDA after gate_h_preflight.py exits 0.
# Full log -> lockbox. Operator stdout is minimal.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p3/env.cuda.sh

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: Gate H is not Mac MPS." >&2
  exit 3
fi

python - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    print("REFUSE: torch.cuda.is_available() is False.", file=sys.stderr)
    sys.exit(3)
print("cuda", torch.cuda.get_device_name(0), "sm", torch.cuda.get_device_capability())
PY

export NANOCHAT_DATA_DIR="${NANOCHAT_DATA_DIR_TL:?}"
export NANOCHAT_BASE_DIR="${NANOCHAT_BASE_DIR:?}"
export WANDB_MODE=disabled
export WANDB_RUN=dummy
export OMP_NUM_THREADS=1

LOCK_LOG="${P3_LOCKBOX_ROOT}/gate-h-smoke-full.log"
SAFE="${P3_SAFE_PROGRESS_ROOT}/gate-h-smoke-progress.txt"
mkdir -p "$(dirname "$LOCK_LOG")" "$P3_SAFE_PROGRESS_ROOT"
: >"$SAFE"
echo "gate_h_smoke_started utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"$SAFE"

cd "$NANOCHAT_FILIPINO_ROOT/vendor/nanochat"
set +e
python -m scripts.base_train \
  --device-type=cuda \
  --depth=4 \
  --max-seq-len=2048 \
  --device-batch-size="${DEVICE_BATCH:-8}" \
  --total-batch-size=65536 \
  --num-iterations=30 \
  --warmup-steps=3 \
  --eval-every=-1 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=30 \
  --model-tag=p3-smoke-tl-d4 \
  --run=p3-smoke-tl-d4 \
  >"$LOCK_LOG" 2>&1
RC=$?
set -e

echo "gate_h_smoke_exit_code=$RC" >>"$SAFE"
chmod 600 "$LOCK_LOG" 2>/dev/null || true

cd "$ROOT"
python scripts/p3/gate_h_accept.py --exit-code "$RC"
exit $?
