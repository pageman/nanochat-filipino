#!/usr/bin/env bash
# P3 Gates Q→W orchestrator (CUDA pod). Blinding: train/U/V logs → lockbox.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NANOCHAT_FILIPINO_ROOT="$ROOT"
export P3_RUN_ID="${P3_RUN_ID:-p3-20260819T192700Z-92d63d4}"
source scripts/p3/env.cuda.sh

echo "=== Gate Q ==="
python scripts/p3/gate_q_b0_freeze.py

echo "=== Gate R ==="
bash scripts/p3/gate_r_b1.sh

echo "=== Gate S ==="
bash scripts/p3/gate_s_b2.sh

echo "=== Gate T ==="
bash scripts/p3/gate_t_b3.sh

echo "=== Gate U ==="
LOCK="${P3_LOCKBOX_ROOT}/gate-u-eval-full.log"
python scripts/p3/gate_u_seal.py >"$LOCK" 2>&1
chmod 600 "$LOCK" 2>/dev/null || true
tail -1 "$LOCK"

echo "=== Gate V ==="
export GATE_V_AUTHORIZED=1
LOCKV="${P3_LOCKBOX_ROOT}/gate-v-eval-full.log"
python scripts/p3/gate_v_test.py --phase all >"$LOCKV" 2>&1
chmod 600 "$LOCKV" 2>/dev/null || true
tail -1 "$LOCKV"

echo "=== Gate W ==="
python scripts/p3/gate_w_closeout.py

echo "=== P3 Gates Q-W complete ==="
