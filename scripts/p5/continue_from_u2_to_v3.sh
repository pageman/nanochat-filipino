#!/usr/bin/env bash
# After T2 pass: U2 -> V2 -> seed 3 I..V. Does not run Gate X/W (laptop).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NANOCHAT_FILIPINO_ROOT="$ROOT"
# shellcheck disable=SC1091
source scripts/p5/env.cuda.sh
export PYTHONUNBUFFERED=1
DRIVER="${P5_SAFE_PROGRESS_ROOT}/seed-2/driver.log"
MASTER="${P5_SAFE_PROGRESS_ROOT}/panel-driver.log"
mkdir -p "$(dirname "$DRIVER")" "$(dirname "$MASTER")"

run_step() {
  local name="$1"; shift
  echo "BEGIN ${name} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER" | tee -a "$MASTER"
  set +e
  "$@"
  local rc=$?
  set -e
  echo "END ${name} exit=${rc} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER" | tee -a "$MASTER"
  return "$rc"
}

echo "resume_from_u2 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER" | tee -a "$MASTER"

# U2 only if not already sealed
if [[ ! -f "$P5_RUN_CARD_ROOT/seed-2/gate-u-seal.json" ]]; then
  run_step "U_2" python scripts/p5/gate_u_seal.py 2
else
  echo "SKIP U_2 already sealed" | tee -a "$DRIVER"
fi

# V2 only if not already tested
if [[ ! -f "$P5_RUN_CARD_ROOT/seed-2/gate-v-test.json" ]]; then
  run_step "V_2" python scripts/p5/gate_v_c3_test.py 2
else
  echo "SKIP V_2 already tested" | tee -a "$DRIVER"
fi
echo "seed_panel_complete seed=2 path=V utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
echo "END seed=2 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"

echo "BEGIN seed=3 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
bash scripts/p5/run_seed_panel.sh 3
echo "END seed=3 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
echo "panel_gpu_complete ready_for_X utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
