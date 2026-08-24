#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p5/env.cuda.sh
# shellcheck disable=SC1091
source scripts/p5/gate_child_common.sh
SEED="${1:?usage: gate_t_c3.sh SEED}"
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate T is not Mac MPS." >&2; exit 3; fi
python - <<'PY'
import torch, sys
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY
p5_child_train "$SEED" T c3 "p5-s${SEED}-c3-mix-d20" p4_token_share_c3 \
  "$P5_RUN_CARD_ROOT/seed-${SEED}/gate-t-authorization.json" "${NANOCHAT_DATA_DIR_C3}"
