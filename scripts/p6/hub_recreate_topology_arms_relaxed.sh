#!/usr/bin/env bash
# P6-M W5 technical recreate (relaxed): retrain topology arms; accept new SHAs.
# Does NOT require match to original Gate T receipts. Documents recreate digests.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p6/env.cuda.sh

SEED=4
C0_SHA=7fbd24de792aa4ee27d841866db2114e0fb45b1fdcaa4edcc9b24582220123c9
FROZEN="${NANOCHAT_BASE_DIR}/p6-s${SEED}/c0/frozen/p6-s${SEED}-c0-tl-d20"
RECEIPT_DIR="${P6_RUN_CARD_ROOT}/seed-${SEED}"
RECEIPT="${RECEIPT_DIR}/gate-w5-topology-recreate-relaxed.json"
LOG_ROOT="${P6_LOCKBOX_ROOT}/seed-${SEED}/w5-recreate-relaxed"
SAFE_ROOT="${P6_SAFE_PROGRESS_ROOT}/seed-${SEED}/w5-recreate-relaxed"
mkdir -p "$LOG_ROOT" "$SAFE_ROOT" "$RECEIPT_DIR"

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

sha_of() {
  python - "$1" <<'PY'
import hashlib, sys
from pathlib import Path
p = Path(sys.argv[1])
h = hashlib.sha256()
with p.open("rb") as f:
    for c in iter(lambda: f.read(1 << 20), b""):
        h.update(c)
print(h.hexdigest())
PY
}

python - "$FROZEN/model_000294.pt" "$C0_SHA" <<'PY'
import hashlib, sys
from pathlib import Path
p = Path(sys.argv[1]); exp = sys.argv[2]
h = hashlib.sha256()
with p.open("rb") as f:
    for c in iter(lambda: f.read(1 << 20), b""):
        h.update(c)
got = h.hexdigest()
if got != exp:
    raise SystemExit(f"C0 mismatch {got}")
print("c0_ok", got)
PY

train_arm() {
  local ARM="$1" TAG="$2" DATA_DIR="$3"
  local OUT="${NANOCHAT_BASE_DIR}/base_checkpoints/${TAG}"
  local MODEL="${OUT}/model_000294.pt"
  if [[ -f "$MODEL" ]]; then
    local GOT
    GOT="$(sha_of "$MODEL")"
    echo "skip_existing arm=${ARM} sha=${GOT}" | tee -a "${SAFE_ROOT}/${ARM}.txt"
    return 0
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
  if [[ ! -f "$MODEL" ]]; then
    echo "REFUSE: no model after train arm=${ARM} rc=${RC}" >&2
    return "${RC:-1}"
  fi
  # Nonzero exit OK if model written (ENOSPC-on-optim pattern)
  local GOT
  GOT="$(sha_of "$MODEL")"
  echo "recreate_ok arm=${ARM} sha=${GOT}" | tee -a "${SAFE_ROOT}/${ARM}.txt"
}

BASE_STREAMS="${NANOCHAT_BASE_DIR}/streams"
train_arm m-fine "p6-s${SEED}-m-fine-d20" "${BASE_STREAMS}/m-fine"
train_arm m-coarse "p6-s${SEED}-m-coarse-d20" "${BASE_STREAMS}/m-coarse"
train_arm m-blocked "p6-s${SEED}-m-blocked-d20" "${BASE_STREAMS}/m-blocked"
train_arm m-rand "p6-s${SEED}-m-rand-d20" "${BASE_STREAMS}/m-rand"

python - <<PY
import json, hashlib
from datetime import datetime, timezone
from pathlib import Path

seed = $SEED
base = Path("$NANOCHAT_BASE_DIR")
arms = {
    "m-fine": f"base_checkpoints/p6-s{seed}-m-fine-d20/model_000294.pt",
    "m-coarse": f"base_checkpoints/p6-s{seed}-m-coarse-d20/model_000294.pt",
    "m-blocked": f"base_checkpoints/p6-s{seed}-m-blocked-d20/model_000294.pt",
    "m-rand": f"base_checkpoints/p6-s{seed}-m-rand-d20/model_000294.pt",
}
orig = {
    "m-fine": "a0139607a8fdf2772d4b8e722b449b6a8db04056a8dc38cd177708af8f15eeab",
    "m-coarse": "86588ee9f72ea4a85a821c2c882a363d55d3e50ccb325bdabaa0706e1e911dfe",
    "m-blocked": "5ec45216eb0a09b5bc04f04f4622d85f7d8f7ff8861fdea6de5487f7c18fa526",
    "m-rand": "38580cd501c0d87a1a502397697f7c7e427134eb7cb64bdce2ba6be1a036f108",
}

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

rows = {}
for arm, rel in arms.items():
    p = base / rel
    if not p.is_file():
        raise SystemExit(f"missing {rel}")
    got = sha(p)
    rows[arm] = {
        "source_relpath": rel,
        "bytes": p.stat().st_size,
        "sha256": got,
        "matches_original_gate_t": got == orig[arm],
        "original_gate_t_sha256": orig[arm],
    }

out = {
    "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "gate": "W5-recreate-relaxed",
    "status": "pass",
    "seed": seed,
    "note": "Technical recreate for Hub deposit. New SHAs supersede original Gate T bits for Hub only; science claims remain Gate X / filed receipts.",
    "accept_rule": "relaxed_new_sha",
    "c0_sha256": "$C0_SHA",
    "arms": rows,
}
Path("$RECEIPT").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"receipt": "$RECEIPT", "shas": {k: v["sha256"] for k, v in rows.items()}}, indent=2))
PY

echo "W5_TOPOLOGY_RECREATE_RELAXED_COMPLETE"
