# Source from the repo root before any P2 Gate A–G command.
# Gate H/I need a CUDA NVIDIA host (A40-class). Not this Mac. Not Spark until a labeled unpatched smoke.
# MUST NOT source scripts/p1/env.sh
# MUST NOT run: python -m nanochat.dataset
# MUST NOT write into pageman/nanochat-filipino-p1-fixed-d20-3x
# MUST NOT load P1.1 model_000294.pt as EN0/A2 start weights

export P2_ROOT="/Users/paulpajo/Projects/nanochat-filipino"
export P2_RUN_ID="p2-20260817T150944Z-de99f8a"
export NANOCHAT_BASE_DIR="$P2_ROOT/data/cache/${P2_RUN_ID}"
export PATH="/opt/homebrew/bin:$PATH"
export VIRTUAL_ENV="$P2_ROOT/vendor/nanochat/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export WANDB_RUN=dummy
export WANDB_MODE=disabled

# Language data dirs are set per gate. Do not default to P1.1 Tagalog active.
# Gate E freeze (read-only copies / packed shards). Still do not export NANOCHAT_DATA_DIR
# until a specific arm (EN tok_train / EN0 / A2 / A3) is running.
export NANOCHAT_DATA_DIR_EN="$P2_ROOT/data/processed/wikitext-103/en-active"
export NANOCHAT_DATA_DIR_TL="$P2_ROOT/data/processed/p2-tl39-readonly"
export NANOCHAT_DATA_DIR_A3="$P2_ROOT/data/processed/p2-mix-a3-50-50"
unset NANOCHAT_DATA_DIR || true

echo "P2_ROOT=$P2_ROOT"
echo "P2_RUN_ID=$P2_RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "NANOCHAT_DATA_DIR_EN=$NANOCHAT_DATA_DIR_EN"
echo "NANOCHAT_DATA_DIR_TL=$NANOCHAT_DATA_DIR_TL"
echo "NANOCHAT_DATA_DIR_A3=$NANOCHAT_DATA_DIR_A3"
echo "python=$(command -v python)"
