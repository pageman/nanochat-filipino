#!/usr/bin/env bash
# After relaxed recreate completes: rewrite RELEASE_MANIFEST SHAs from receipt, stage, upload.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source scripts/p6/env.sh

RECEIPT="${P6_RUN_CARD_ROOT}/seed-4/gate-w5-topology-recreate-relaxed.json"
MANIFEST="${ROOT}/docs/hub/p6-m-schedule-topology/RELEASE_MANIFEST.json"
test -f "$RECEIPT"
test -n "${HF_TOKEN:-}"

python - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path

receipt = json.loads(Path("$RECEIPT").read_text())
manifest = json.loads(Path("$MANIFEST").read_text())
arms = receipt["arms"]
for key, row in arms.items():
    entry = manifest["entries"][key]
    hub = entry["hub_path"]
    sha = row["sha256"]
    entry["sha256"] = sha
    entry["bytes"] = row["bytes"]
    entry["technical_recreate"] = True
    entry["original_gate_t_sha256"] = row["original_gate_t_sha256"]
    entry["matches_original_gate_t"] = row["matches_original_gate_t"]
    manifest["checksums"][hub] = sha

# keep c0/c1/c2/tokenizer as already correct if present
manifest["status"] = "recreate_ready"
manifest["weight_lineage"] = "technical_recreate_w5_relaxed"
manifest["recreate_receipt"] = "docs/run-cards/p6/p6-20260824T155226Z-769f807a/seed-4/gate-w5-topology-recreate-relaxed.json"
manifest["updated_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
manifest["note"] = (
    "Topology children are technical-recreate weights (new SHAs). "
    "C0/C1/C2/tokenizer remain original study artifacts. "
    "Not bitwise identical to original Gate T terminals."
)
Path("$MANIFEST").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
print("manifest_updated", {k: arms[k]["sha256"][:16] for k in arms})
PY

export P6_CACHE_ROOT="${NANOCHAT_BASE_DIR}"
bash "$ROOT/scripts/p6/hub_upload_weights.sh"
