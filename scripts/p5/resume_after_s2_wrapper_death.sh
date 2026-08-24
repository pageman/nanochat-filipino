#!/usr/bin/env bash
# Resume seed 2 after the S2 trainer wrote model_000294.pt and the panel
# process tree died before accept. Does not retrain C2 (output dir already filled).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NANOCHAT_FILIPINO_ROOT="$ROOT"
# shellcheck disable=SC1091
source scripts/p5/env.cuda.sh
export PYTHONUNBUFFERED=1
SEED=2
C0_SHA=e4c4cc7bcdf5033a97f9eedd97f7818d3c8e3ddca2b46fffc8b8c78d6137c4b1
DRIVER="${P5_SAFE_PROGRESS_ROOT}/seed-${SEED}/driver.log"
MASTER="${P5_SAFE_PROGRESS_ROOT}/panel-driver.log"
NOTE="${P5_SAFE_PROGRESS_ROOT}/seed-${SEED}/s2-wrapper-death-recovery.txt"
{
  echo "recovery=s2_wrapper_death_after_save"
  echo "action=accept_existing_c2_then_TUV_then_seed3"
  echo "no_retrain=true"
  echo "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} | tee "$NOTE" | tee -a "$DRIVER" | tee -a "$MASTER"

echo "BEGIN S_${SEED} accept-only utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
python scripts/p5/gate_phase2_accept.py \
  --seed "$SEED" --gate S --arm c2 \
  --model-tag "p5-s${SEED}-c2-en-d20" \
  --stream english_c2_train \
  --data-dir "data/cache/${P5_RUN_ID}/streams/c2_en" \
  --exit-code 0 \
  --c0-sha "$C0_SHA"
echo "END S_${SEED} exit=0 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"

echo "BEGIN T_${SEED} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
bash scripts/p5/gate_t_c3.sh "$SEED"
echo "END T_${SEED} exit=0 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"

echo "BEGIN U_${SEED} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
python scripts/p5/gate_u_seal.py "$SEED"
echo "END U_${SEED} exit=0 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"

echo "BEGIN V_${SEED} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
python scripts/p5/gate_v_c3_test.py "$SEED"
echo "END V_${SEED} exit=0 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
echo "seed_panel_complete seed=${SEED} path=V utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$DRIVER"
echo "END seed=${SEED} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"

echo "BEGIN seed=3 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
bash scripts/p5/run_seed_panel.sh 3
echo "END seed=3 utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
echo "panel_gpu_complete ready_for_X utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
