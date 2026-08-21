#!/usr/bin/env bash
# P4 Gate H: Tagalog-path d4 CUDA smoke (NOT TL0 / NOT C0).
# Run on NVIDIA CUDA after gate_h_preflight.py exits 0.
# Full log -> lockbox. Operator stdout is minimal (no loss curve, no BPB).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p4/env.cuda.sh

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: Gate H is not Mac MPS." >&2
  exit 3
fi

AUTH="$P4_RUN_CARD_ROOT/gate-h-authorization.json"
if [[ ! -f "$AUTH" ]]; then
  echo "REFUSE: missing gate-h-authorization.json" >&2
  exit 3
fi

python - <<'PY'
import json, sys
from pathlib import Path
import os
auth = Path(os.environ["P4_RUN_CARD_ROOT"]) / "gate-h-authorization.json"
row = json.loads(auth.read_text())
if row.get("gate") != "H" or row.get("authorized") is not True or row.get("authorizes_gate_i") is True:
    print("REFUSE: authorization is not Gate-H-only", file=sys.stderr)
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
    echo "REFUSE: smoke data-dir must be Tagalog C1 train pack, not C3/C2/test" >&2
    exit 3
    ;;
esac

LOCK_LOG="${P4_LOCKBOX_ROOT}/gate-h-smoke-full.log"
SAFE="${P4_SAFE_PROGRESS_ROOT}/gate-h-smoke-progress.txt"
mkdir -p "$(dirname "$LOCK_LOG")" "$P4_SAFE_PROGRESS_ROOT"
: >"$SAFE"
STARTED="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "gate_h_smoke_started utc=$STARTED" >>"$SAFE"
echo "gate_h_smoke_started utc=$STARTED"

cd "$NANOCHAT_FILIPINO_ROOT/vendor/nanochat"
set +e
python -m scripts.base_train \
  --device-type=cuda \
  --depth=4 \
  --max-seq-len=2048 \
  --window-pattern=SSSL \
  --device-batch-size="${DEVICE_BATCH:-8}" \
  --total-batch-size=65536 \
  --num-iterations=30 \
  --warmup-steps=3 \
  --eval-every=-1 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=30 \
  --model-tag=p4-smoke-tl-d4 \
  --run=p4-smoke-tl-d4 \
  >"$LOCK_LOG" 2>&1
RC=$?
set -e

echo "gate_h_smoke_exit_code=$RC" >>"$SAFE"
echo "gate_h_smoke_exit_code=$RC"
chmod 600 "$LOCK_LOG" 2>/dev/null || true

cd "$ROOT"
python scripts/p4/gate_h_accept.py --exit-code "$RC"
exit $?
