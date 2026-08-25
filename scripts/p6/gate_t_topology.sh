#!/usr/bin/env bash
# P6 Gate T: four filed schedule-topology arms from frozen C0 (serial).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p6/env.cuda.sh
# shellcheck disable=SC1091
source scripts/p6/gate_child_common.sh

SEED="${1:?usage: gate_t_topology.sh SEED}"
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate T is not Mac MPS." >&2; exit 3; fi

python - <<'PY'
import torch, sys
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY

python - "$SEED" <<'PY'
import json, os, sys
from pathlib import Path
seed = int(sys.argv[1])
root = Path(os.environ["NANOCHAT_FILIPINO_ROOT"])
run = root / "docs/run-cards/p6" / os.environ["P6_RUN_ID"] / f"seed-{seed}"
for name in ("gate-r-c1.json", "gate-s-c2.json"):
    rec = run / name
    if not rec.is_file() or json.loads(rec.read_text()).get("status") != "pass":
        raise SystemExit(f"{name} must pass before Gate T")
PY

AUTH="$P6_RUN_CARD_ROOT/seed-${SEED}/gate-t-authorization.json"
if [[ ! -f "$AUTH" ]]; then echo "REFUSE: missing $AUTH" >&2; exit 3; fi

run_topology_arm() {
  local ARM="$1" TAG="$2" STREAM="$3" DATA_DIR="$4"
  local receipt="$P6_RUN_CARD_ROOT/seed-${SEED}/gate-t-${ARM}.json"
  if [[ -f "$receipt" ]] && python - "$receipt" <<'PY'
import json, sys
raise SystemExit(0 if json.load(open(sys.argv[1])).get("status") == "pass" else 1)
PY
  then
    echo "skip_passed arm=${ARM} tag=${TAG}"
    return 0
  fi
  ckpt="$NANOCHAT_BASE_DIR/base_checkpoints/${TAG}"
  if [[ -d "$ckpt" ]] && compgen -G "$ckpt/model_*.pt" >/dev/null; then
    echo "REFUSE: output already has checkpoints for ${TAG}" >&2
    return 3
  fi
  echo "gate_t_arm_start arm=${ARM} tag=${TAG} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  p6_child_train "$SEED" T "$ARM" "$TAG" "$STREAM" "$AUTH" "$DATA_DIR"
}

BASE_STREAMS="$NANOCHAT_BASE_DIR/streams"
run_topology_arm m-fine "p6-s${SEED}-m-fine-d20" p6_topology_m_fine "${BASE_STREAMS}/m-fine"
run_topology_arm m-coarse "p6-s${SEED}-m-coarse-d20" p6_topology_m_coarse "${BASE_STREAMS}/m-coarse"
run_topology_arm m-blocked "p6-s${SEED}-m-blocked-d20" p6_topology_m_blocked "${BASE_STREAMS}/m-blocked"
run_topology_arm m-rand "p6-s${SEED}-m-rand-d20" p6_topology_m_rand "${BASE_STREAMS}/m-rand"

python - "$SEED" <<'PY'
import json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(os.environ["NANOCHAT_FILIPINO_ROOT"]) / "scripts" / "p6"))
from p6_common import TOPOLOGY_ARMS, seed_card, update_lock_gate, mark_ledger, utc_now

seed = int(sys.argv[1])
card = seed_card(seed)
rows = {}
for arm in TOPOLOGY_ARMS:
    path = card / f"gate-t-{arm}.json"
    if not path.is_file():
        raise SystemExit(f"missing receipt {path.name}")
    row = json.loads(path.read_text())
    if row.get("status") != "pass":
        raise SystemExit(f"{path.name} status={row.get('status')}")
    rows[arm] = row
update_lock_gate(f"T_{seed}", "pass", {"status": f"gate_t_{seed}_pass", "updated_utc": utc_now()})
mark_ledger(f"T_{seed}", "pass", f"docs/run-cards/p6/{os.environ['P6_RUN_ID']}/seed-{seed}/gate-t-m-rand.json", f"U_{seed}")
print(json.dumps({"gate": "T", "seed": seed, "status": "pass", "arms": list(rows.keys())}, sort_keys=True))
PY
