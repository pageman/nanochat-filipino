# P6 environment — CPU gates A–G after Gate 0.
# MUST NOT source scripts/p1–p5 env.sh
# Set NANOCHAT_FILIPINO_ROOT to the clone root before sourcing.

_p6_fail() {
  echo "P6 env refuses: $1" >&2
  return 1 2>/dev/null || exit 1
}

if [[ -z "${NANOCHAT_FILIPINO_ROOT:-}" ]]; then
  _p6_fail "Set NANOCHAT_FILIPINO_ROOT to the nanochat-filipino clone root"
  return 1 2>/dev/null || exit 1
fi

for _v in P1_RUN_ID P1_ROOT P2_RUN_ID P2_ROOT P3_RUN_ID P3_ROOT P4_RUN_ID P4_ROOT P5_RUN_ID P5_ROOT \
  P1_ENV_SOURCED P2_ENV_SOURCED P3_ENV_SOURCED P4_ENV_SOURCED P5_ENV_SOURCED; do
  if [[ -n "${!_v:-}" ]]; then
    _p6_fail "prior-study env appears sourced (${_v} set). Open a new shell."
    return 1 2>/dev/null || exit 1
  fi
done

case "${NANOCHAT_BASE_DIR:-}" in
  */p1-*|*/p2-*|*/p3-*|*/p4-*|*/p5-*)
    _p6_fail "NANOCHAT_BASE_DIR points at a prior-study cache"
    return 1 2>/dev/null || exit 1
    ;;
esac

export P6_ROOT="$NANOCHAT_FILIPINO_ROOT"
export P6_RUN_ID="${P6_RUN_ID:?Set P6_RUN_ID after Gate 0 mint}"
export NANOCHAT_BASE_DIR="$P6_ROOT/data/cache/${P6_RUN_ID}"
export P6_SAFE_PROGRESS_ROOT="${P6_SAFE_PROGRESS_ROOT:-$NANOCHAT_BASE_DIR/safe_progress}"
export P6_LOCKBOX_ROOT="${P6_LOCKBOX_ROOT:-$NANOCHAT_BASE_DIR/lockbox}"
export P6_RUN_CARD_ROOT="$P6_ROOT/docs/run-cards/p6/${P6_RUN_ID}"
export P6_TIER2_LOCAL_ROOT="${P6_TIER2_LOCAL_ROOT:-$P6_ROOT/data/cache/${P6_RUN_ID}/tier2-resume-kit}"
export P6_NETWORK_VOLUME_ID="${P6_NETWORK_VOLUME_ID:-3xuadadrph}"
export P6_NETWORK_VOLUME_DC="${P6_NETWORK_VOLUME_DC:-CA-MTL-3}"
export P6_NETWORK_VOLUME_GB="${P6_NETWORK_VOLUME_GB:-200}"
export VIRTUAL_ENV="${VIRTUAL_ENV:-$P6_ROOT/vendor/nanochat/.venv}"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export WANDB_RUN=dummy
export WANDB_MODE=disabled
export P6_ENV_SOURCED=1
unset NANOCHAT_DATA_DIR || true
unset P6_TEST_JSONL_EN || true
unset P6_TEST_JSONL_TL || true

echo "P6_ROOT=$P6_ROOT"
echo "P6_RUN_ID=$P6_RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "P6_SAFE_PROGRESS_ROOT=$P6_SAFE_PROGRESS_ROOT"
echo "P6_LOCKBOX_ROOT=$P6_LOCKBOX_ROOT"
echo "P6_TIER2_LOCAL_ROOT=$P6_TIER2_LOCAL_ROOT"
echo "P6_NETWORK_VOLUME_ID=$P6_NETWORK_VOLUME_ID"
echo "P6_NETWORK_VOLUME_DC=$P6_NETWORK_VOLUME_DC"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "P6_TEST_JSONL_EN=${P6_TEST_JSONL_EN-<UNSET>}"
echo "P6_TEST_JSONL_TL=${P6_TEST_JSONL_TL-<UNSET>}"
echo "NOTE: Gate 0 filed. Shared gates A–G next; GPU only after authorization. Lockout-resistant Tier-2 is mandatory."
