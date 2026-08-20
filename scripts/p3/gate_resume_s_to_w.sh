#!/usr/bin/env bash
# Resume P3 Gates S→W after EN/B3 staging sync.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
export NANOCHAT_FILIPINO_ROOT="$ROOT"
export P3_RUN_ID="${P3_RUN_ID:-p3-20260819T192700Z-92d63d4}"
source scripts/p3/env.cuda.sh
export NANOCHAT_DATA_DIR_EN="$ROOT/data/staging/en-clean"
export NANOCHAT_DATA_DIR_B3="$ROOT/data/staging/b3-clean"
export GATE_V_AUTHORIZED=1

echo "=== Gate S (EN staging) ==="
export NANOCHAT_DATA_DIR="$NANOCHAT_DATA_DIR_EN"
bash scripts/p3/gate_s_b2.sh

echo "=== Gate T (B3 staging) ==="
export NANOCHAT_DATA_DIR="$NANOCHAT_DATA_DIR_B3"
bash scripts/p3/gate_t_b3.sh

echo "=== Gate U ==="
export P3_EN_VAL_DIR="$NANOCHAT_DATA_DIR_EN"
export P3_TL_VAL_DIR="${NANOCHAT_DATA_DIR_TL:?}"
LOCK="${P3_LOCKBOX_ROOT}/gate-u-eval-full.log"
P3_EN_VAL_DIR="$P3_EN_VAL_DIR" P3_TL_VAL_DIR="$P3_TL_VAL_DIR" \
  python scripts/p3/gate_u_seal.py >"$LOCK" 2>&1
chmod 600 "$LOCK" 2>/dev/null || true
tail -1 "$LOCK"

echo "=== Gate V ==="
LOCKV="${P3_LOCKBOX_ROOT}/gate-v-eval-full.log"
python scripts/p3/gate_v_test.py --phase all >"$LOCKV" 2>&1
chmod 600 "$LOCKV" 2>/dev/null || true
tail -1 "$LOCKV"

echo "=== Gate W ==="
python scripts/p3/gate_w_closeout.py

echo "=== P3 Gates S-W complete ==="
