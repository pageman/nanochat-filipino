#!/usr/bin/env bash
# P4 Gate P0-T: Tagalog parent eligibility (TL0 d8 + d20 vs untrained + byte-unigram).
# Full eval log -> lockbox. Operator stdout is PASS/BLOCKED/TECHNICAL BLOCK via accept.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p4/env.cuda.sh

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: Gate P0-T is not Mac MPS." >&2
  exit 3
fi

AUTH="$P4_RUN_CARD_ROOT/gate-p0t-authorization.json"
if [[ ! -f "$AUTH" ]]; then
  echo "REFUSE: missing gate-p0t-authorization.json" >&2
  exit 3
fi

python - <<'PY'
import json, os, sys
from pathlib import Path
auth = Path(os.environ["P4_RUN_CARD_ROOT"]) / "gate-p0t-authorization.json"
row = json.loads(auth.read_text())
if row.get("gate") != "P0-T" or row.get("authorized") is not True or row.get("authorizes_children") is True:
    print("REFUSE: authorization is not P0-T-only", file=sys.stderr)
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
    echo "REFUSE: P0-T data-dir must be Tagalog C1 train pack" >&2
    exit 3
    ;;
esac

# Frozen evaluator still names last-is-val shard_00002. Bind to P4 C1 names.
C1="${NANOCHAT_DATA_DIR_TL}"
chmod u+w "$C1"
ln -sfn train_00000.parquet "$C1/shard_00000.parquet"
ln -sfn train_00001.parquet "$C1/shard_00001.parquet"
ln -sfn val.parquet "$C1/shard_00002.parquet"

python scripts/p4/gate_p0t_preflight.py

LOCK_LOG="${P4_LOCKBOX_ROOT}/gate-p0-t-eval-full.log"
SAFE="${P4_SAFE_PROGRESS_ROOT}/gate-p0t-runner.txt"
mkdir -p "$(dirname "$LOCK_LOG")" "$P4_SAFE_PROGRESS_ROOT"
: >"$SAFE"
echo "gate_p0t_started utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$SAFE"

set +e
python scripts/p4/evaluate_bpb.py \
  --phase p0t \
  --device-type=cuda \
  --device-batch-size="${DEVICE_BATCH:-8}" \
  --out-dir "${P4_LOCKBOX_ROOT}" \
  >"$LOCK_LOG" 2>&1
RC=$?
set -e

echo "gate_p0t_eval_exit_code=${RC}" | tee -a "$SAFE"
chmod 600 "$LOCK_LOG" 2>/dev/null || true

python scripts/p4/gate_p0t_accept.py --eval-exit-code "$RC"
exit $?
