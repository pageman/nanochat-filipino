#!/usr/bin/env bash
# After sticky pod o82o3p6dr3trzh is RUNNING: pull the four topology model_000294.pt
# into the generalized cache layout, verify SHA vs RELEASE_MANIFEST, then Hub upload.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CACHE="${P6_CACHE_ROOT:-$ROOT/data/cache/p6-20260824T155226Z-769f807a}"
MANIFEST="$ROOT/docs/hub/p6-m-schedule-topology/RELEASE_MANIFEST.json"
SSH_KEY="${P6_SSH_KEY:-$HOME/.ssh/p1_runpod_h}"
# Prefer direct SSH if set; else RunPod proxy from env.
REMOTE_BASE="${P6_REMOTE_CACHE:-/workspace/nanochat-filipino/data/cache/p6-20260824T155226Z-769f807a}"

if [[ -z "${P6_SSH_HOST:-}" || -z "${P6_SSH_PORT:-}" ]]; then
  echo "Set P6_SSH_HOST and P6_SSH_PORT (direct) or export from get-pod ssh.direct" >&2
  exit 2
fi

SSH=(ssh -i "$SSH_KEY" -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -o ConnectTimeout=30 -p "$P6_SSH_PORT")
RSYNC_E="ssh -i $SSH_KEY -o IdentitiesOnly=yes -o StrictHostKeyChecking=no -p $P6_SSH_PORT"

for arm in m-fine m-coarse m-blocked m-rand; do
  dest_dir="$CACHE/base_checkpoints/p6-s4-${arm}-d20"
  mkdir -p "$dest_dir"
  src="$REMOTE_BASE/base_checkpoints/p6-s4-${arm}-d20/model_000294.pt"
  echo "pull $arm …"
  rsync -av --progress -e "$RSYNC_E" \
    "root@${P6_SSH_HOST}:${src}" \
    "$dest_dir/model_000294.pt"
done

python3 - <<PY
import hashlib, json, sys
from pathlib import Path
root = Path("$CACHE")
manifest = json.loads(Path("$MANIFEST").read_text())
for key in ("m-fine", "m-coarse", "m-blocked", "m-rand"):
    row = manifest["entries"][key]
    p = root / row["source_relpath"]
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    got = h.hexdigest()
    if got != row["sha256"]:
        raise SystemExit(f"hash mismatch {key}: {got}")
    print("OK", key, got)
PY

echo "topology_pull_ok — next: HF_TOKEN=… ./scripts/p6/hub_upload_weights.sh"
