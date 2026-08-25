#!/usr/bin/env bash
# P6 Gate P0-T_s: seed-matched untrained floors + shared Tagalog byte-unigram.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p6/env.cuda.sh
SEED="${1:?usage: gate_p0t.sh SEED}"
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: P0-T is not Mac MPS." >&2; exit 3; fi
python - <<PY
import json, os
from pathlib import Path
auth = Path(os.environ["P6_RUN_CARD_ROOT"]) / "seed-$SEED" / "gate-p0t-authorization.json"
row = json.loads(auth.read_text())
if row.get("gate") != "P0-T" or row.get("authorized") is not True or row.get("seed") != int("$SEED"):
    raise SystemExit("REFUSE: P0-T authorization")
PY
python - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY
export NANOCHAT_DATA_DIR="${NANOCHAT_DATA_DIR_TL:?}"
export WANDB_MODE=disabled WANDB_RUN=dummy OMP_NUM_THREADS=1
C1="${NANOCHAT_DATA_DIR_TL}"
chmod u+w "$C1"
ln -sfn train_00000.parquet "$C1/shard_00000.parquet"
ln -sfn train_00001.parquet "$C1/shard_00001.parquet"
ln -sfn val.parquet "$C1/shard_00002.parquet"
BOX="${P6_LOCKBOX_ROOT}/seed-${SEED}"
SAFE="${P6_SAFE_PROGRESS_ROOT}/seed-${SEED}"
mkdir -p "$BOX" "$SAFE"
echo "gate_p0t_started seed=${SEED} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$SAFE/gate-p0t-runner.txt"
set +e
python scripts/p6/evaluate_bpb.py \
  --phase p0t --seed "$SEED" --device-type=cuda \
  --device-batch-size="${DEVICE_BATCH:-8}" \
  --out-dir "$BOX" >"$BOX/gate-p0-t-eval-full.log" 2>&1
RC=$?
set -e
echo "gate_p0t_eval_exit_code=${RC}" | tee -a "$SAFE/gate-p0t-runner.txt"
chmod 600 "$BOX/gate-p0-t-eval-full.log" 2>/dev/null || true
python scripts/p6/gate_p0t_accept.py --seed "$SEED" --eval-exit-code "$RC"
exit $?
