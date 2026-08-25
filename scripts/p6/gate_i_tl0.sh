#!/usr/bin/env bash
# P6 Gate I_s: fresh Tagalog TL0 (d8 then d20) with parent-init seed s.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p6/env.cuda.sh
SEED="${1:?usage: gate_i_tl0.sh SEED [8|20|all]}"
DEPTH="${2:-all}"
if [[ "$SEED" != "4" ]]; then echo "SEED must be filed parent seed 4" >&2; exit 2; fi
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate I is not Mac MPS." >&2; exit 3; fi
python scripts/p6/gate_i_preflight.py "$SEED"
python - <<PY
import json, os, sys
from pathlib import Path
auth = Path(os.environ["P6_RUN_CARD_ROOT"]) / "seed-$SEED" / "gate-i-authorization.json"
row = json.loads(auth.read_text())
if row.get("gate") != "I" or row.get("authorized") is not True or row.get("seed") != int("$SEED"):
    raise SystemExit("REFUSE: I authorization")
PY
python - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY

export NANOCHAT_DATA_DIR="${NANOCHAT_DATA_DIR_TL:?}"
export WANDB_MODE=disabled WANDB_RUN=dummy OMP_NUM_THREADS=1
case "$NANOCHAT_DATA_DIR" in *c3_mix*|*c2_en*|*test*) echo "REFUSE: TL0 data-dir" >&2; exit 3;; esac

train_depth() {
  local depth="$1"
  local tag="p6-s${SEED}-tl0-d${depth}"
  local lock_log="${P6_LOCKBOX_ROOT}/seed-${SEED}/gate-i-tl0-d${depth}-full.log"
  local safe="${P6_SAFE_PROGRESS_ROOT}/seed-${SEED}/gate-i-tl0-d${depth}-progress.txt"
  local ckpt_dir="${NANOCHAT_BASE_DIR}/base_checkpoints/${tag}"
  if [[ -d "$ckpt_dir" ]] && compgen -G "${ckpt_dir}/model_*.pt" >/dev/null; then
    echo "REFUSE: ${tag} already has checkpoints." >&2
    return 4
  fi
  mkdir -p "$(dirname "$lock_log")" "$(dirname "$safe")" "$ckpt_dir"
  echo "gate_i_tl0_started seed=${SEED} depth=${depth} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$safe"
  cd "$NANOCHAT_FILIPINO_ROOT/vendor/nanochat"
  set +e
  python "$NANOCHAT_FILIPINO_ROOT/scripts/p6/parent_train.py" \
    --parent-init-seed "$SEED" --wrapper-depth "$depth" \
    --record-initial-state "${P6_LOCKBOX_ROOT}/seed-${SEED}/initial_state_d${depth}.json" -- \
    --device-type=cuda --depth="${depth}" --max-seq-len=2048 --window-pattern=SSSL \
    --device-batch-size="${DEVICE_BATCH:-8}" --total-batch-size=65536 \
    --num-iterations=294 --warmup-steps=14 \
    --eval-every=-1 --core-metric-every=-1 --sample-every=-1 --save-every=-1 \
    --model-tag="${tag}" --run="${tag}" >"$lock_log" 2>&1
  local rc=$?
  set -e
  echo "gate_i_tl0_exit_code=${rc} seed=${SEED} depth=${depth}" | tee -a "$safe"
  chmod 600 "$lock_log" 2>/dev/null || true
  cd "$ROOT"
  python scripts/p6/gate_i_accept.py --seed "$SEED" --depth "$depth" --exit-code "$rc"
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
