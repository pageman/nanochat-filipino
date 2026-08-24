# P5 environment — CPU gates A–G after Gate 0.
# MUST NOT source scripts/p1/env.sh, scripts/p2/env.sh, scripts/p3/env.sh, or scripts/p4/env.sh
# Set NANOCHAT_FILIPINO_ROOT to the clone root before sourcing.

_p5_fail() {
  echo "P5 env refuses: $1" >&2
  return 1 2>/dev/null || exit 1
}

if [[ -z "${NANOCHAT_FILIPINO_ROOT:-}" ]]; then
  _p5_fail "Set NANOCHAT_FILIPINO_ROOT to the nanochat-filipino clone root"
  return 1 2>/dev/null || exit 1
fi

for _v in P1_RUN_ID P1_ROOT P2_RUN_ID P2_ROOT P3_RUN_ID P3_ROOT P4_RUN_ID P4_ROOT P1_ENV_SOURCED P2_ENV_SOURCED P3_ENV_SOURCED P4_ENV_SOURCED; do
  if [[ -n "${!_v:-}" ]]; then
    _p5_fail "prior-study env appears sourced (${_v} set). Open a new shell."
    return 1 2>/dev/null || exit 1
  fi
done

case "${NANOCHAT_BASE_DIR:-}" in
  */p1-*|*/p2-*|*/p3-*|*/p4-*)
    _p5_fail "NANOCHAT_BASE_DIR points at a prior-study cache"
    return 1 2>/dev/null || exit 1
    ;;
esac

export P5_ROOT="$NANOCHAT_FILIPINO_ROOT"
export P5_RUN_ID="${P5_RUN_ID:-p5-20260823T160632Z-439d1de5}"
export NANOCHAT_BASE_DIR="$P5_ROOT/data/cache/${P5_RUN_ID}"
export P5_SAFE_PROGRESS_ROOT="${P5_SAFE_PROGRESS_ROOT:-$NANOCHAT_BASE_DIR/safe_progress}"
export P5_LOCKBOX_ROOT="${P5_LOCKBOX_ROOT:-$NANOCHAT_BASE_DIR/lockbox}"
export P5_RUN_CARD_ROOT="$P5_ROOT/docs/run-cards/p5/${P5_RUN_ID}"
export VIRTUAL_ENV="${VIRTUAL_ENV:-$P5_ROOT/vendor/nanochat/.venv}"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export WANDB_RUN=dummy
export WANDB_MODE=disabled
export P5_ENV_SOURCED=1
unset NANOCHAT_DATA_DIR || true
unset P5_TEST_JSONL_EN || true
unset P5_TEST_JSONL_TL || true

echo "P5_ROOT=$P5_ROOT"
echo "P5_RUN_ID=$P5_RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "P5_SAFE_PROGRESS_ROOT=$P5_SAFE_PROGRESS_ROOT"
echo "P5_LOCKBOX_ROOT=$P5_LOCKBOX_ROOT"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "P5_TEST_JSONL_EN=${P5_TEST_JSONL_EN-<UNSET>}"
echo "P5_TEST_JSONL_TL=${P5_TEST_JSONL_TL-<UNSET>}"
echo "NOTE: Gate 0 filed. Shared gates A–G only; no parent/child training yet."
