#!/usr/bin/env bash
# P6-M W5 technical recreate: retrain four topology arms from frozen C0.
# Accept ONLY if terminal model SHA-256 matches docs/hub/.../RELEASE_MANIFEST.json.
# Does not amend science; deposit recovery only. No BPB / no Gate U-V.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p6/env.cuda.sh

SEED=4
C0_SHA=7fbd24de792aa4ee27d841866db2114e0fb45b1fdcaa4edcc9b24582220123c9
FROZEN="${NANOCHAT_BASE_DIR}/p6-s${SEED}/c0/frozen/p6-s${SEED}-c0-tl-d20"
MANIFEST="${ROOT}/docs/hub/p6-m-schedule-topology/RELEASE_MANIFEST.json"
AUTH="${P6_RUN_CARD_ROOT}/seed-${SEED}/gate-t-recreate-w5-authorization.json"
LOG_ROOT="${P6_LOCKBOX_ROOT}/seed-${SEED}/w5-recreate"
SAFE_ROOT="${P6_SAFE_PROGRESS_ROOT}/seed-${SEED}/w5-recreate"
mkdir -p "$LOG_ROOT" "$SAFE_ROOT" "$(dirname "$AUTH")"

if [[ "$(uname -s)" == "Darwin" ]]; then
  echo "REFUSE: recreate requires NVIDIA CUDA host" >&2
  exit 3
fi
python - <<'PY'
import torch, sys
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY

# Write scoped recreate authorization (deposit recovery, not new Gate T)
python - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path
path = Path("$AUTH")
path.write_text(json.dumps({
  "arms": ["m-fine", "m-coarse", "m-blocked", "m-rand"],
  "aspredicted_id": 307969,
  "authorized": True,
  "authorized_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
  "authorized_by": "operator chat: Authorize technical recreate (option 2) for W5 Hub",
  "authorizes_validation": False,
  "gate": "W5-recreate",
  "host_class": "NVIDIA CUDA (A40 class)",
  "must_not": ["print BPB", "start Gate U", "test access", "unblind", "amend filed SHAs"],
  "note": "Technical recreate for Hub deposit only. Accept iff terminal SHA matches RELEASE_MANIFEST.",
  "p6_run_id": "$P6_RUN_ID",
  "scope": "retrain topology arms from frozen C0; load_optimizer=False; exact phase-two budget",
  "seed": $SEED,
  "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
}, indent=2, sort_keys=True) + "\n")
print(path)
PY

expect_sha() {
  python - "$MANIFEST" "$1" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
print(m["entries"][sys.argv[2]]["sha256"])
PY
}

train_arm() {
  local ARM="$1" TAG="$2" DATA_DIR="$3"
  local EXPECT
  EXPECT="$(expect_sha "$ARM")"
  local OUT="${NANOCHAT_BASE_DIR}/base_checkpoints/${TAG}"
  local MODEL="${OUT}/model_000294.pt"
  if [[ -f "$MODEL" ]]; then
    local GOT
    GOT="$(python - "$MODEL" <<'PY'
import hashlib, sys
from pathlib import Path
p = Path(sys.argv[1])
h = hashlib.sha256()
with p.open("rb") as f:
    for c in iter(lambda: f.read(1 << 20), b""):
        h.update(c)
print(h.hexdigest())
PY
)"
    if [[ "$GOT" == "$EXPECT" ]]; then
      echo "skip_match arm=${ARM} sha=${GOT}"
      return 0
    fi
    echo "REFUSE: existing ${MODEL} sha ${GOT} != ${EXPECT}; remove before retry" >&2
    return 3
  fi

  echo "recreate_start arm=${ARM} tag=${TAG} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "${SAFE_ROOT}/${ARM}.txt"
  export NANOCHAT_DATA_DIR="$DATA_DIR"
  export WANDB_MODE=disabled WANDB_RUN=dummy OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1
  local LOCK_LOG="${LOG_ROOT}/${ARM}-full.log"
  cd "$NANOCHAT_FILIPINO_ROOT/vendor/nanochat"
  set +e
  python "$NANOCHAT_FILIPINO_ROOT/scripts/p6/continue_from_frozen.py" \
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
  cd "$NANOCHAT_FILIPINO_ROOT"
  echo "recreate_exit arm=${ARM} code=${RC}" | tee -a "${SAFE_ROOT}/${ARM}.txt"
  chmod 600 "$LOCK_LOG" 2>/dev/null || true
  if [[ "$RC" -ne 0 ]]; then
    # M-rand historically hit ENOSPC on optimizer save after model write — accept model if present+hash
    if [[ -f "$MODEL" ]]; then
      echo "train_nonzero_but_model_present arm=${ARM} rc=${RC}" | tee -a "${SAFE_ROOT}/${ARM}.txt"
    else
      echo "REFUSE: train failed arm=${ARM} rc=${RC}" >&2
      return "$RC"
    fi
  fi
  local GOT
  GOT="$(python - "$MODEL" <<'PY'
import hashlib, sys
from pathlib import Path
p = Path(sys.argv[1])
h = hashlib.sha256()
with p.open("rb") as f:
    for c in iter(lambda: f.read(1 << 20), b""):
        h.update(c)
print(h.hexdigest())
PY
)"
  if [[ "$GOT" != "$EXPECT" ]]; then
    echo "REFUSE: SHA mismatch arm=${ARM} got=${GOT} expect=${EXPECT}" >&2
    return 4
  fi
  echo "recreate_ok arm=${ARM} sha=${GOT}" | tee -a "${SAFE_ROOT}/${ARM}.txt"
}

# Preflight C0
python - "$FROZEN/model_000294.pt" "$C0_SHA" <<'PY'
import hashlib, sys
from pathlib import Path
p = Path(sys.argv[1])
exp = sys.argv[2]
h = hashlib.sha256()
with p.open("rb") as f:
    for c in iter(lambda: f.read(1 << 20), b""):
        h.update(c)
got = h.hexdigest()
if got != exp:
    raise SystemExit(f"C0 mismatch {got}")
print("c0_ok", got)
PY

BASE_STREAMS="${NANOCHAT_BASE_DIR}/streams"
train_arm m-fine "p6-s${SEED}-m-fine-d20" "${BASE_STREAMS}/m-fine"
train_arm m-coarse "p6-s${SEED}-m-coarse-d20" "${BASE_STREAMS}/m-coarse"
train_arm m-blocked "p6-s${SEED}-m-blocked-d20" "${BASE_STREAMS}/m-blocked"
train_arm m-rand "p6-s${SEED}-m-rand-d20" "${BASE_STREAMS}/m-rand"

python - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path
out = Path("$P6_RUN_CARD_ROOT") / "seed-$SEED" / "gate-w5-topology-recreate.json"
out.write_text(json.dumps({
  "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
  "gate": "W5-recreate",
  "seed": $SEED,
  "status": "pass",
  "arms": ["m-fine", "m-coarse", "m-blocked", "m-rand"],
  "note": "Technical recreate; SHAs matched RELEASE_MANIFEST entries",
  "manifest": "docs/hub/p6-m-schedule-topology/RELEASE_MANIFEST.json",
}, indent=2, sort_keys=True) + "\n")
print(out)
PY
echo "W5_TOPOLOGY_RECREATE_COMPLETE"
