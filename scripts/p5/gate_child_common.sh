#!/usr/bin/env bash
# Shared P5 child train. Args: SEED GATE ARM TAG STREAM AUTH DATA_DIR
p5_child_train() {
  local SEED="$1" GATE="$2" ARM="$3" TAG="$4" STREAM="$5" AUTH="$6" DATA_DIR="$7"
  local gate_l
  gate_l="$(echo "$GATE" | tr '[:upper:]' '[:lower:]')"
  local LOCK_LOG="${P5_LOCKBOX_ROOT}/seed-${SEED}/gate-${gate_l}-${ARM}-full.log"
  local SAFE="${P5_SAFE_PROGRESS_ROOT}/seed-${SEED}/gate-${gate_l}-${ARM}-progress.txt"
  local FROZEN="${NANOCHAT_BASE_DIR}/p5-s${SEED}/c0/frozen/p5-s${SEED}-c0-tl-d20"
  if [[ ! -f "$AUTH" ]]; then echo "REFUSE: missing $AUTH" >&2; return 3; fi
  python - "$AUTH" "$GATE" "$SEED" <<'PY'
import json, sys
row = json.load(open(sys.argv[1]))
if row.get("gate") != sys.argv[2] or row.get("authorized") is not True or row.get("seed") != int(sys.argv[3]):
    raise SystemExit("authorization mismatch")
PY
  local C0_SHA
  C0_SHA="$(python - "$SEED" <<'PY'
import json, os, sys
from pathlib import Path
seed = sys.argv[1]
root = Path(os.environ["NANOCHAT_FILIPINO_ROOT"])
row = json.loads((root / "docs/run-cards/p5" / os.environ["P5_RUN_ID"] / f"seed-{seed}" / "gate-q-c0-freeze.json").read_text())
print(row["checkpoint_sha256"])
PY
)"
  export NANOCHAT_DATA_DIR="$DATA_DIR"
  export WANDB_MODE=disabled WANDB_RUN=dummy OMP_NUM_THREADS=1
  export PYTHONUNBUFFERED=1
  mkdir -p "$(dirname "$LOCK_LOG")" "$(dirname "$SAFE")"
  echo "gate_${gate_l}_started seed=${SEED} tag=${TAG} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$SAFE"
  cd "$NANOCHAT_FILIPINO_ROOT/vendor/nanochat"
  set +e
  python "$NANOCHAT_FILIPINO_ROOT/scripts/p5/continue_from_frozen.py" \
    --init-from "$FROZEN" --init-step 294 \
    --expected-sha "$C0_SHA" --allowed-model-tag "$TAG" --seed "$SEED" -- \
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
  python scripts/p5/gate_phase2_accept.py \
    --seed "$SEED" --gate "$GATE" --arm "$ARM" --model-tag "$TAG" \
    --stream "$STREAM" --data-dir "${DATA_DIR#$NANOCHAT_FILIPINO_ROOT/}" \
    --exit-code "$RC" --c0-sha "$C0_SHA" "${EXTRA[@]}"
  return $?
}
