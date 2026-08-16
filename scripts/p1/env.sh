# Source from the repo root before any Gate A–G command. Gate H/I need a GPU host.
# MUST NOT run: python -m nanochat.dataset

export P1_ROOT="/Users/paulpajo/Projects/nanochat-filipino"
export RUN_ID="p1-20260816T025911Z-0067a57"
export NANOCHAT_BASE_DIR="$P1_ROOT/data/cache/${RUN_ID}"
export NANOCHAT_DATA_DIR="$P1_ROOT/data/processed/wikitext-tl39/active"
export PATH="/opt/homebrew/bin:$PATH"
export VIRTUAL_ENV="$P1_ROOT/vendor/nanochat/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

echo "P1_ROOT=$P1_ROOT"
echo "RUN_ID=$RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "NANOCHAT_DATA_DIR=$NANOCHAT_DATA_DIR"
