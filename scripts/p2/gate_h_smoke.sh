#!/usr/bin/env bash
# P2 Gate H confirmatory-path English d4 smoke.
# Run ONLY on a named NVIDIA CUDA host AFTER scripts/p2/gate_h_preflight.py exits 0.
# This script is NOT EN0. Passing it does not declare that EN0 started.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# Prefer CUDA env; fall back only if already exported.
if [[ -f scripts/p2/env.cuda.sh ]]; then
  # shellcheck disable=SC1091
  source scripts/p2/env.cuda.sh
fi

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: Gate H is not Mac MPS. Wait for a named NVIDIA CUDA host." >&2
  exit 3
fi

python - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    print("REFUSE: torch.cuda.is_available() is False. Gate H not executed.", file=sys.stderr)
    sys.exit(3)
print("cuda", torch.cuda.get_device_name(0), "sm", torch.cuda.get_device_capability())
PY

export NANOCHAT_DATA_DIR="$NANOCHAT_DATA_DIR_EN"
export NANOCHAT_BASE_DIR="${NANOCHAT_BASE_DIR:?}"
export WANDB_MODE=disabled
export WANDB_RUN=dummy
export OMP_NUM_THREADS=1

if [[ "${NANOCHAT_DATA_DIR}" != *"/wikitext-103/en-active" ]]; then
  echo "REFUSE: NANOCHAT_DATA_DIR is not English en-active." >&2
  exit 3
fi

cd "$P2_ROOT/vendor/nanochat"
# Confirmatory-path smoke: T=2048, warmup 3 < 30. Never default warmup 40.
exec python -m scripts.base_train \
  --device-type=cuda \
  --depth=4 \
  --max-seq-len=2048 \
  --device-batch-size="${DEVICE_BATCH:-8}" \
  --total-batch-size=65536 \
  --num-iterations=30 \
  --warmup-steps=3 \
  --eval-tokens=8192 \
  --eval-every=10 \
  --core-metric-every=-1 \
  --sample-every=15 \
  --save-every=30 \
  --model-tag=p2-smoke-en-d4 \
  --run=p2-smoke-en-d4
