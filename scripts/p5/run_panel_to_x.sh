#!/usr/bin/env bash
# Filed order: seed 1 then 2 then 3. Does not run Gate X (laptop).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NANOCHAT_FILIPINO_ROOT="$ROOT"
# shellcheck disable=SC1091
source scripts/p5/env.cuda.sh
MASTER="${P5_SAFE_PROGRESS_ROOT}/panel-driver.log"
mkdir -p "$(dirname "$MASTER")"
echo "panel_started utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
for s in 1 2 3; do
  echo "BEGIN seed=${s} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
  bash scripts/p5/run_seed_panel.sh "$s"
  echo "END seed=${s} utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
done
echo "panel_gpu_complete ready_for_X utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$MASTER"
