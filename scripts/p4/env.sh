# P4 environment — CPU gates A–G after Gate 0.
# MUST NOT source scripts/p1/env.sh, scripts/p2/env.sh, or scripts/p3/env.sh
# MUST NOT run python -m nanochat.dataset
# MUST NOT pass ratio=-1
# MUST NOT load P1.1, P2, or P3 model_*.pt
# Set NANOCHAT_FILIPINO_ROOT to the clone root before sourcing.

_p4_fail() {
  echo "P4 env refuses: $1" >&2
  return 1 2>/dev/null || exit 1
}

if [[ -z "${NANOCHAT_FILIPINO_ROOT:-}" ]]; then
  _p4_fail "Set NANOCHAT_FILIPINO_ROOT to the nanochat-filipino clone root"
  return 1 2>/dev/null || exit 1
fi

if [[ -n "${P3_RUN_ID:-}" || -n "${P3_ROOT:-}" || -n "${P3_ENV_SOURCED:-}" ]]; then
  _p4_fail "scripts/p3/env.sh appears sourced (P3_RUN_ID/P3_ROOT set). Open a new shell."
  return 1 2>/dev/null || exit 1
fi
if [[ -n "${P2_RUN_ID:-}" || -n "${P2_ROOT:-}" || -n "${P1_RUN_ID:-}" || -n "${P1_ROOT:-}" ]]; then
  _p4_fail "a prior-study env is still in this shell. Open a new shell."
  return 1 2>/dev/null || exit 1
fi
case "${NANOCHAT_BASE_DIR:-}" in
  */p3-*|*/p2-*|*/p1-*)
    _p4_fail "NANOCHAT_BASE_DIR points at a prior-study cache"
    return 1 2>/dev/null || exit 1
    ;;
esac

export P4_ROOT="$NANOCHAT_FILIPINO_ROOT"
export P4_RUN_ID="${P4_RUN_ID:-p4-20260821T060032Z-92d63d4}"
export NANOCHAT_BASE_DIR="$P4_ROOT/data/cache/${P4_RUN_ID}"
export P4_SAFE_PROGRESS_ROOT="${P4_SAFE_PROGRESS_ROOT:-$NANOCHAT_BASE_DIR/safe_progress}"
export P4_LOCKBOX_ROOT="${P4_LOCKBOX_ROOT:-$NANOCHAT_BASE_DIR/lockbox}"
export P4_RUN_CARD_ROOT="$P4_ROOT/docs/run-cards/p4/${P4_RUN_ID}"
export VIRTUAL_ENV="${VIRTUAL_ENV:-$P4_ROOT/vendor/nanochat/.venv}"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export WANDB_RUN=dummy
export WANDB_MODE=disabled
export P4_ENV_SOURCED=1
unset NANOCHAT_DATA_DIR || true
unset P4_TEST_JSONL_EN || true
unset P4_TEST_JSONL_TL || true
unset P3_TEST_JSONL_EN || true
unset P3_TEST_JSONL_TL || true

echo "P4_ROOT=$P4_ROOT"
echo "P4_RUN_ID=$P4_RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "P4_SAFE_PROGRESS_ROOT=$P4_SAFE_PROGRESS_ROOT"
echo "P4_LOCKBOX_ROOT=$P4_LOCKBOX_ROOT"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "P4_TEST_JSONL_EN=${P4_TEST_JSONL_EN-<UNSET>}"
echo "P4_TEST_JSONL_TL=${P4_TEST_JSONL_TL-<UNSET>}"
echo "python=$(command -v python)"
echo "NOTE: Gate 0 instrument only. tok_train / parent / children have not started."
