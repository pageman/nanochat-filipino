#!/usr/bin/env bash
# Wait for sticky P6 pod capacity, then pull missing topology checkpoints and upload Hub.
# Explicit operator loop for host-pinned /workspace recovery (CA-MTL-1 A40).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
POD_ID="${P6_POD_ID:-o82o3p6dr3trzh}"
CACHE="$ROOT/data/cache/p6-20260824T155226Z-769f807a"
SSH_KEY="${P6_SSH_KEY:-$HOME/.ssh/p1_runpod_h}"
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"

echo "This helper expects: runpodctl authenticated, pod $POD_ID startable, SSH key $SSH_KEY"
echo "Refusing to auto-bill without operator; call scripts/p6/hub_upload_weights.sh after sources exist."
echo "Missing local topology arms (need pull from pod when host has free GPU):"
for arm in m-fine m-coarse m-blocked m-rand; do
  p="$CACHE/base_checkpoints/p6-s4-${arm}-d20/model_000294.pt"
  if [[ -f "$p" ]]; then echo "  OK $arm"; else echo "  MISSING $arm → $p"; fi
done
