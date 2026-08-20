# P3 environment — CPU gates A–G after Gate 0.
# MUST NOT source scripts/p1/env.sh or scripts/p2/env.sh
# MUST NOT run python -m nanochat.dataset
# MUST NOT load P1.1 or P2 model_*.pt
# Set NANOCHAT_FILIPINO_ROOT to the clone root before sourcing.

if [ -z "${NANOCHAT_FILIPINO_ROOT:-}" ]; then
  echo "Set NANOCHAT_FILIPINO_ROOT to the nanochat-filipino clone root" >&2
  return 1 2>/dev/null || exit 1
fi

export P3_ROOT="$NANOCHAT_FILIPINO_ROOT"
export P3_RUN_ID="${P3_RUN_ID:-p3-20260819T192700Z-92d63d4}"
export NANOCHAT_BASE_DIR="$P3_ROOT/data/cache/${P3_RUN_ID}"
export P3_SAFE_PROGRESS_ROOT="${P3_SAFE_PROGRESS_ROOT:-$NANOCHAT_BASE_DIR/safe_progress}"
export P3_LOCKBOX_ROOT="${P3_LOCKBOX_ROOT:-$NANOCHAT_BASE_DIR/lockbox}"
export P3_RUN_CARD_ROOT="$P3_ROOT/docs/run-cards/p3/${P3_RUN_ID}"
export VIRTUAL_ENV="${VIRTUAL_ENV:-$P3_ROOT/vendor/nanochat/.venv}"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export WANDB_RUN=dummy
export WANDB_MODE=disabled
unset NANOCHAT_DATA_DIR || true
unset P3_TEST_JSONL_EN || true
unset P3_TEST_JSONL_TL || true

echo "P3_ROOT=$P3_ROOT"
echo "P3_RUN_ID=$P3_RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "P3_SAFE_PROGRESS_ROOT=$P3_SAFE_PROGRESS_ROOT"
echo "P3_LOCKBOX_ROOT=$P3_LOCKBOX_ROOT"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "python=$(command -v python)"
echo "NOTE: Gate 0 only. tok_train / TL0 have not started."
