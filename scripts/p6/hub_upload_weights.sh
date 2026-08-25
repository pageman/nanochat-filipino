#!/usr/bin/env bash
# P6-M Hub sibling release: manifest stage → exact count → upload_folder.
# Works on Mac or pod. Requires HF_TOKEN. Refuses partial via pack_hub_staging.py.
#
# Env:
#   P6_CACHE_ROOT or NANOCHAT_BASE_DIR  — run cache with source_relpath layout
#   HF_TOKEN                           — Hugging Face write token
#   P6_HUB_REPO_ID                     — default pageman/nanochat-filipino-p6-m-schedule-topology
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

LOG_DIR="${P6_HUB_LOG_DIR:-$ROOT/transfer}"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/p6-hub-upload.log"
STATUS="$LOG_DIR/p6-hub-upload.status"
COMMIT_OUT="$LOG_DIR/p6-hub-upload.commit"
REPO_ID="${P6_HUB_REPO_ID:-pageman/nanochat-filipino-p6-m-schedule-topology}"

phase() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] PHASE=$1"; echo "$1" > "$STATUS"; }

exec > >(tee -a "$LOG") 2>&1

phase START
test -n "${HF_TOKEN:-}" || { phase FAIL_NO_TOKEN; exit 2; }

if command -v python3 >/dev/null; then PY=python3; else PY=python; fi

phase STAGE
"$PY" "$ROOT/scripts/p6/pack_hub_staging.py"
STAGE="$ROOT/transfer/p6-hub-pageman-nanochat-filipino-p6-m-schedule-topology"
test -d "$STAGE"
test -f "$STAGE/SHA256SUMS-weights.txt"

phase COUNT
n=$("$PY" - <<PY
from pathlib import Path
import json
m=json.loads(Path("$STAGE/RELEASE_MANIFEST.json").read_text())
keys=m["logical_keys"]
stage=Path("$STAGE")
missing=[]
for k in keys:
    p=stage/m["entries"][k]["hub_path"]
    if not p.is_file():
        missing.append(str(p))
print("missing", len(missing))
for x in missing:
    print(x)
print("count", len(keys))
raise SystemExit(1 if missing else 0)
PY
)
echo "inventory_ok repo=$REPO_ID"

phase UPLOAD
"$PY" - <<PY
import os
from pathlib import Path
from huggingface_hub import create_repo, upload_folder

repo_id = os.environ.get("P6_HUB_REPO_ID", "$REPO_ID")
token = os.environ["HF_TOKEN"]
stage = Path("$STAGE")
create_repo(repo_id=repo_id, repo_type="model", exist_ok=True, token=token, private=False)
print("upload_folder start", flush=True)
url = upload_folder(
    folder_path=str(stage),
    repo_id=repo_id,
    repo_type="model",
    commit_message="P6-M weights: C0+C1+C2+M-fine+M-coarse+M-blocked+M-rand + tokenizer (manifest hash-verified)",
    token=token,
)
print("UPLOAD_COMMIT_URL", url, flush=True)
Path("$COMMIT_OUT").write_text(str(url) + "\n")
PY

phase DONE
echo "P6_HUB_UPLOAD_COMPLETE"
