#!/usr/bin/env bash
# P4 Gate T: C3 token-share mix from frozen C0.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p4/env.cuda.sh
# shellcheck disable=SC1091
source scripts/p4/gate_child_common.sh
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate T is not Mac MPS." >&2; exit 3; fi
python - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY
python - <<'PY'
import json, os, sys
from pathlib import Path
root = Path(os.environ["NANOCHAT_FILIPINO_ROOT"])
run = root / "docs/run-cards/p4" / os.environ["P4_RUN_ID"]
for name in ("gate-r-c1.json", "gate-s-c2.json"):
    rec = run / name
    if not rec.is_file() or json.loads(rec.read_text()).get("status") != "pass":
        raise SystemExit(f"{name} must pass before T")
PY
case "${NANOCHAT_DATA_DIR_C3}" in *c1_tl*|*c2_en*|*test*) echo "REFUSE: T stream"; exit 3;; esac
p4_child_train T c3 p4-c3-mix-d20 c3_token_share_mix \
  "$P4_RUN_CARD_ROOT/gate-t-authorization.json" "${NANOCHAT_DATA_DIR_C3}"
