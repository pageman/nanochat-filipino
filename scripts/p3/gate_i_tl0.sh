#!/usr/bin/env bash
# P3 Gate I: TL0 confirmatory train (d8 and/or d20) on Tagalog p3-tl39-active only.
# Run on NVIDIA CUDA after gate_i_preflight.py exits 0.
# Full log -> lockbox. Operator stdout is minimal.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p3/env.cuda.sh

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: Gate I TL0 is not Mac MPS." >&2
  exit 3
fi

DEPTH="${1:-}"
if [[ -z "$DEPTH" || ! "$DEPTH" =~ ^(8|20|all)$ ]]; then
  echo "Usage: $0 {8|20|all}" >&2
  exit 2
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

N_TL0=294
WARMUP=14
GATE_G="$ROOT/docs/run-cards/p3/${P3_RUN_ID}/gate-g-budget-command-freeze.json"
if [[ -f "$GATE_G" ]]; then
  read -r N_TL0 WARMUP < <(python - "$GATE_G" <<'PY'
import json, sys
g = json.load(open(sys.argv[1]))
tl0 = g["commands"]["tl0"]
print(g["N_TL0"], tl0["warmup_steps"])
PY
)
fi

train_depth() {
  local depth="$1"
  local tag="p3-tl0-d${depth}"
  local lock_log="${P3_LOCKBOX_ROOT}/gate-i-tl0-d${depth}-full.log"
  local safe="${P3_SAFE_PROGRESS_ROOT}/gate-i-tl0-d${depth}-progress.txt"
  local ckpt_dir="${NANOCHAT_BASE_DIR}/base_checkpoints/${tag}"

  if [[ -d "$ckpt_dir" ]] && compgen -G "${ckpt_dir}/model_*.pt" >/dev/null; then
    echo "REFUSE: ${tag} output dir already has checkpoints. Use accept-only or clean first." >&2
    return 4
  fi

  mkdir -p "$(dirname "$lock_log")" "$P3_SAFE_PROGRESS_ROOT" "$ckpt_dir"
  : >"$safe"
  echo "gate_i_tl0_started depth=${depth} tag=${tag} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"$safe"

  cd "$NANOCHAT_FILIPINO_ROOT/vendor/nanochat"
  set +e
  python -m scripts.base_train \
    --device-type=cuda \
    --depth="${depth}" \
    --max-seq-len=2048 \
    --window-pattern=SSSL \
    --device-batch-size="${DEVICE_BATCH:-8}" \
    --total-batch-size=65536 \
    --num-iterations="${N_TL0}" \
    --warmup-steps="${WARMUP}" \
    --eval-every=-1 \
    --core-metric-every=-1 \
    --sample-every=-1 \
    --save-every=-1 \
    --model-tag="${tag}" \
    --run="${tag}" \
    >"$lock_log" 2>&1
  local rc=$?
  set -e

  echo "gate_i_tl0_exit_code=${rc} depth=${depth}" >>"$safe"
  chmod 600 "$lock_log" 2>/dev/null || true

  cd "$ROOT"
  python scripts/p3/gate_i_accept.py --depth "${depth}" --exit-code "${rc}"
  return $?
}

if [[ "$DEPTH" == "all" ]]; then
  overall=0
  train_depth 8 || overall=$?
  train_depth 20 || overall=$?
  exit "$overall"
else
  train_depth "$DEPTH"
fi
