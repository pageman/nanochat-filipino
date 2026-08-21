#!/usr/bin/env bash
# P4 Gate R: C1 extra-Tagalog from frozen C0.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p4/env.cuda.sh
# shellcheck disable=SC1091
source scripts/p4/gate_child_common.sh
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate R is not Mac MPS." >&2; exit 3; fi
python - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY
case "${NANOCHAT_DATA_DIR_TL}" in *c3_mix*|*c2_en*|*test*) echo "REFUSE: R stream"; exit 3;; esac
p4_child_train R c1 p4-c1-tl-d20 tagalog_c1_train \
  "$P4_RUN_CARD_ROOT/gate-r-authorization.json" "${NANOCHAT_DATA_DIR_TL}"
