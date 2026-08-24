#!/usr/bin/env bash
# Run one filed seed: I -> P0-T -> (if PASS) Q R S T U V. Blinded.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NANOCHAT_FILIPINO_ROOT="$ROOT"
# shellcheck disable=SC1091
source scripts/p5/env.cuda.sh
SEED="${1:?usage: run_seed_panel.sh SEED}"
DRIVER="${P5_SAFE_PROGRESS_ROOT}/seed-${SEED}/driver.log"
mkdir -p "$(dirname "$DRIVER")"
echo "seed_panel_started seed=${SEED} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"

run_step() {
  local name="$1"; shift
  echo "BEGIN ${name} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
  set +e
  "$@"
  local rc=$?
  set -e
  echo "END ${name} exit=${rc} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
  return "$rc"
}

python scripts/p5/authorize_seed_gates.py --seed "$SEED" --phase i
run_step "I_${SEED}" bash scripts/p5/gate_i_tl0.sh "$SEED" all || { echo "STOP I" | tee -a "$DRIVER"; exit 1; }
python scripts/p5/authorize_seed_gates.py --seed "$SEED" --phase p0t
if run_step "P0-T_${SEED}" bash scripts/p5/gate_p0t.sh "$SEED"; then
  python scripts/p5/authorize_seed_gates.py --seed "$SEED" --phase children
  run_step "Q_${SEED}" python scripts/p5/gate_q_c0_freeze.py "$SEED"
  run_step "R_${SEED}" bash scripts/p5/gate_r_c1.sh "$SEED"
  run_step "S_${SEED}" bash scripts/p5/gate_s_c2.sh "$SEED"
  run_step "T_${SEED}" bash scripts/p5/gate_t_c3.sh "$SEED"
  run_step "U_${SEED}" python scripts/p5/gate_u_seal.py "$SEED"
  run_step "V_${SEED}" python scripts/p5/gate_v_c3_test.py "$SEED"
  echo "seed_panel_complete seed=${SEED} path=V utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
else
  STATUS="$(python - <<PY
import json
from pathlib import Path
import os
p = Path(os.environ["P5_RUN_CARD_ROOT"]) / "seed-$SEED" / "gate-p0-t.json"
print(json.loads(p.read_text()).get("p0_t_status", "UNKNOWN"))
PY
)"
  echo "seed_panel_stopped seed=${SEED} p0t=${STATUS} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
  if [[ "$STATUS" == "BLOCKED" ]]; then
    echo "ineligible_parent recorded; no replacement seed" | tee -a "$DRIVER"
    exit 0
  fi
  exit 1
fi
