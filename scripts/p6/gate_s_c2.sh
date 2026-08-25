#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p6/env.cuda.sh
# shellcheck disable=SC1091
source scripts/p6/gate_child_common.sh
SEED="${1:?usage: gate_s_c2.sh SEED}"
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate S is not Mac MPS." >&2; exit 3; fi
python - <<'PY'
import torch, sys
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY
p6_child_train "$SEED" S c2 "p6-s${SEED}-c2-en-d20" english_c2_train \
  "$P6_RUN_CARD_ROOT/seed-${SEED}/gate-s-authorization.json" "${NANOCHAT_DATA_DIR_EN}"
