#!/usr/bin/env bash
# P6 CUDA-host environment. Source from the repo root on the named NVIDIA host.
# MUST NOT source scripts/p1/p2/p3/p4 env.sh

if [[ -n "${P4_ENV_SOURCED:-}" || -n "${P3_ENV_SOURCED:-}" ]]; then
  echo "P6 CUDA env refuses: prior-study env appears sourced" >&2
  return 1 2>/dev/null || exit 1
fi

if [[ -z "${NANOCHAT_FILIPINO_ROOT:-}" ]]; then
  export NANOCHAT_FILIPINO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi

# shellcheck source=/dev/null
source "$NANOCHAT_FILIPINO_ROOT/scripts/p6/env.sh" || return 1 2>/dev/null || exit 1

export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export NANOCHAT_DATA_DIR_TL="${NANOCHAT_BASE_DIR}/streams/c1_tl"
export NANOCHAT_DATA_DIR_EN="${NANOCHAT_BASE_DIR}/streams/c2_en"
export NANOCHAT_DATA_DIR_C3="${NANOCHAT_BASE_DIR}/streams/c3_mix"
unset NANOCHAT_DATA_DIR || true

echo "NANOCHAT_DATA_DIR_TL=$NANOCHAT_DATA_DIR_TL"
echo "NANOCHAT_DATA_DIR_EN=$NANOCHAT_DATA_DIR_EN"
echo "NANOCHAT_DATA_DIR_C3=$NANOCHAT_DATA_DIR_C3"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "NOTE: P6 CUDA env only. Parent/children have not started. Confirmatory class is NVIDIA CUDA (A40 class)."
