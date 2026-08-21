#!/usr/bin/env bash
# P4 Gate I: fresh Tagalog TL0 (d8 and/or d20) on C1 pack only.
# Run on NVIDIA CUDA after gate_i_preflight.py exits 0.
# Full log -> lockbox. Operator stdout is minimal (no BPB, no loss curve).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p4/env.cuda.sh

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: Gate I TL0 is not Mac MPS." >&2
  exit 3
fi

AUTH="$P4_RUN_CARD_ROOT/gate-i-authorization.json"
if [[ ! -f "$AUTH" ]]; then
  echo "REFUSE: missing gate-i-authorization.json" >&2
  exit 3
fi

DEPTH="${1:-}"
if [[ -z "$DEPTH" || ! "$DEPTH" =~ ^(8|20|all)$ ]]; then
  echo "Usage: $0 {8|20|all}" >&2
  exit 2
fi

python - <<'PY'
import json, os, sys
from pathlib import Path
auth = Path(os.environ["P4_RUN_CARD_ROOT"]) / "gate-i-authorization.json"
row = json.loads(auth.read_text())
if row.get("gate") != "I" or row.get("authorized") is not True or row.get("authorizes_children") is True:
    print("REFUSE: authorization is not Gate-I-only", file=sys.stderr)
    sys.exit(3)
PY

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

case "$NANOCHAT_DATA_DIR" in
  *c3_mix*|*c2_en*|*test*)
    echo "REFUSE: TL0 data-dir must be Tagalog C1 train pack" >&2
    exit 3
    ;;
esac

N_TL0=294
WARMUP=14
GATE_G="$ROOT/docs/run-cards/p4/${P4_RUN_ID}/gate-g-budget-command-freeze.json"
if [[ -f "$GATE_G" ]]; then
  read -r N_TL0 WARMUP < <(python - "$GATE_G" <<'PY'
import json, sys
g = json.load(open(sys.argv[1]))
parent = g["commands"]["parent"]
print(g["N_TL0"], parent["warmup_steps"])
PY
)
fi

train_depth() {
  local depth="$1"
  local tag="p4-tl0-d${depth}"
  local lock_log="${P4_LOCKBOX_ROOT}/gate-i-tl0-d${depth}-full.log"
  local safe="${P4_SAFE_PROGRESS_ROOT}/gate-i-tl0-d${depth}-progress.txt"
  local ckpt_dir="${NANOCHAT_BASE_DIR}/base_checkpoints/${tag}"

  if [[ -d "$ckpt_dir" ]] && compgen -G "${ckpt_dir}/model_*.pt" >/dev/null; then
    echo "REFUSE: ${tag} output dir already has checkpoints." >&2
    return 4
  fi

  mkdir -p "$(dirname "$lock_log")" "$P4_SAFE_PROGRESS_ROOT" "$ckpt_dir"
  : >"$safe"
  echo "gate_i_tl0_started depth=${depth} tag=${tag} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$safe"

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

  echo "gate_i_tl0_exit_code=${rc} depth=${depth}" | tee -a "$safe"
  chmod 600 "$lock_log" 2>/dev/null || true

  cd "$ROOT"
  python scripts/p4/gate_i_accept.py --depth "${depth}" --exit-code "${rc}"
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
