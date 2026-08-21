#!/usr/bin/env bash
# P4 serial driver: Q → R → S → T → U → V. Stop on first failure. No BPB on stdout.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NANOCHAT_FILIPINO_ROOT="$ROOT"
# shellcheck disable=SC1091
source scripts/p4/env.cuda.sh

DRIVER="${P4_SAFE_PROGRESS_ROOT}/gate-q-to-v-driver.log"
mkdir -p "$P4_SAFE_PROGRESS_ROOT"
echo "gate_q_to_v_started utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"

run_step() {
  local name="$1"
  shift
  echo "BEGIN ${name} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
  set +e
  "$@"
  local rc=$?
  set -e
  echo "END ${name} exit=${rc} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
  if [[ "$rc" -ne 0 ]]; then
    echo "STOP after ${name}" | tee -a "$DRIVER"
    exit "$rc"
  fi
}

run_step Q python scripts/p4/gate_q_c0_freeze.py
run_step R bash scripts/p4/gate_r_c1.sh
run_step S bash scripts/p4/gate_s_c2.sh
run_step T bash scripts/p4/gate_t_c3.sh
run_step U python scripts/p4/gate_u_seal.py
run_step V python scripts/p4/gate_v_c3_test.py

echo "gate_q_to_v_complete utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
