#!/usr/bin/env bash
# P4 Gate S: C2 pure-English from frozen C0.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p4/env.cuda.sh
# shellcheck disable=SC1091
source scripts/p4/gate_child_common.sh
if [[ "$(uname -s)" == "Darwin" ]]; then echo "REFUSE: Gate S is not Mac MPS." >&2; exit 3; fi
python - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    raise SystemExit("REFUSE: cuda unavailable")
print("cuda", torch.cuda.get_device_name(0))
PY
# Require R pass (serial)
python - <<'PY'
import json, os, sys
from pathlib import Path
root = Path(os.environ["NANOCHAT_FILIPINO_ROOT"])
rec = root / "docs/run-cards/p4" / os.environ["P4_RUN_ID"] / "gate-r-c1.json"
if not rec.is_file() or json.loads(rec.read_text()).get("status") != "pass":
    raise SystemExit("Gate R must pass before S")
PY
case "${NANOCHAT_DATA_DIR_EN}" in *c3_mix*|*c1_tl*|*test*) echo "REFUSE: S stream"; exit 3;; esac
p4_child_train S c2 p4-c2-en-d20 english_c2_train \
  "$P4_RUN_CARD_ROOT/gate-s-authorization.json" "${NANOCHAT_DATA_DIR_EN}"
