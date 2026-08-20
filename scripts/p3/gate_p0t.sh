#!/usr/bin/env bash
# P3 Gate P0-T: Tagalog parent eligibility (TL0 d8 + d20 vs untrained + byte-unigram).
# Full eval log -> lockbox. Operator stdout is PASS/BLOCKED only via accept.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p3/env.cuda.sh

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: Gate P0-T is not Mac MPS." >&2
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

cd "$ROOT/scripts/p3"
python gate_p0t_preflight.py
cd "$ROOT"

LOCK_LOG="${P3_LOCKBOX_ROOT}/gate-p0-t-eval-full.log"
SAFE="${P3_SAFE_PROGRESS_ROOT}/gate-p0t-runner.txt"
mkdir -p "$(dirname "$LOCK_LOG")" "$P3_SAFE_PROGRESS_ROOT"
: >"$SAFE"
echo "gate_p0t_started utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"$SAFE"

set +e
python scripts/p3/evaluate_bpb.py \
  --phase p0t \
  --device-type=cuda \
  --device-batch-size="${DEVICE_BATCH:-8}" \
  --out-dir "${P3_LOCKBOX_ROOT}" \
  >"$LOCK_LOG" 2>&1
RC=$?
set -e

echo "gate_p0t_eval_exit_code=${RC}" >>"$SAFE"
chmod 600 "$LOCK_LOG" 2>/dev/null || true

python scripts/p3/gate_p0t_accept.py --eval-exit-code "$RC"
exit $?
