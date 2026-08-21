#!/usr/bin/env bash
# Shared child train body. Sourced by gate_r/s/t shells.
# Args: GATE ARM TAG STREAM_KIND AUTH_FILE DATA_DIR_VAR LOCK_SUFFIX
p4_child_train() {
  local GATE="$1" ARM="$2" TAG="$3" STREAM="$4" AUTH="$5" DATA_DIR="$6"
  local gate_l
  gate_l="$(echo "$GATE" | tr '[:upper:]' '[:lower:]')"
  local LOCK_LOG="${P4_LOCKBOX_ROOT}/gate-${gate_l}-${ARM}-full.log"
  local SAFE="${P4_SAFE_PROGRESS_ROOT}/gate-${gate_l}-${ARM}-progress.txt"
  local FROZEN="${NANOCHAT_BASE_DIR}/c0/frozen/p4-c0-tl-d20"
  local C0_SHA

  if [[ ! -f "$AUTH" ]]; then
    echo "REFUSE: missing $AUTH" >&2
    return 3
  fi
  python - "$AUTH" "$GATE" <<'PY'
import json, sys
row = json.load(open(sys.argv[1]))
gate = sys.argv[2]
if row.get("gate") != gate or row.get("authorized") is not True:
    raise SystemExit(f"authorization is not Gate {gate}")
PY

  C0_SHA="$(python - <<'PY'
import json, os
from pathlib import Path
root = Path(os.environ["NANOCHAT_FILIPINO_ROOT"])
row = json.loads((root / "docs/run-cards/p4" / os.environ["P4_RUN_ID"] / "gate-q-c0-freeze.json").read_text())
print(row["checkpoint_sha256"])
PY
)"

  export NANOCHAT_DATA_DIR="$DATA_DIR"
  export WANDB_MODE=disabled
  export WANDB_RUN=dummy
  export OMP_NUM_THREADS=1

  mkdir -p "$(dirname "$LOCK_LOG")" "$P4_SAFE_PROGRESS_ROOT"
  : >"$SAFE"
  echo "gate_${gate_l}_started tag=${TAG} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$SAFE"

  cd "$NANOCHAT_FILIPINO_ROOT/vendor/nanochat"
  set +e
  python "$NANOCHAT_FILIPINO_ROOT/scripts/p4/continue_from_frozen.py" \
    --init-from "$FROZEN" --init-step 294 \
    --expected-sha "$C0_SHA" \
    --allowed-model-tag "$TAG" -- \
    --device-type=cuda --depth=20 --max-seq-len=2048 --window-pattern=SSSL \
    --device-batch-size="${DEVICE_BATCH:-8}" --total-batch-size=65536 \
    --num-iterations=294 --warmup-steps=14 \
    --embedding-lr=0.09 --unembedding-lr=0.0024 --matrix-lr=0.006 --scalar-lr=0.15 --weight-decay=0.28 \
    --eval-every=-1 --core-metric-every=-1 --sample-every=-1 --save-every=-1 \
    --resume-from-step=-1 \
    --model-tag="$TAG" --run="$TAG" >"$LOCK_LOG" 2>&1
  local RC=$?
  set -e
  echo "gate_${gate_l}_exit_code=${RC}" | tee -a "$SAFE"
  chmod 600 "$LOCK_LOG" 2>/dev/null || true
  cd "$NANOCHAT_FILIPINO_ROOT"

  local EXTRA=()
  if [[ "$GATE" == "T" ]]; then
    EXTRA+=(--mix-manifest-sha f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107)
  fi
  python scripts/p4/gate_phase2_accept.py \
    --gate "$GATE" --arm "$ARM" --model-tag "$TAG" \
    --stream "$STREAM" --data-dir "${DATA_DIR#$NANOCHAT_FILIPINO_ROOT/}" \
    --exit-code "$RC" --c0-sha "$C0_SHA" "${EXTRA[@]}"
  return $?
}
