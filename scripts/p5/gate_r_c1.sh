#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p5/env.cuda.sh
# shellcheck disable=SC1091
source scripts/p5/gate_child_common.sh
SEED="${1:?usage: gate_r_c1.sh SEED}"
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate R is not Mac MPS." >&2; exit 3; fi
python - <<'PY'
import torch, sys
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY
p5_child_train "$SEED" R c1 "p5-s${SEED}-c1-tl-d20" tagalog_c1_train \
  "$P5_RUN_CARD_ROOT/seed-${SEED}/gate-r-authorization.json" "${NANOCHAT_DATA_DIR_TL}"
