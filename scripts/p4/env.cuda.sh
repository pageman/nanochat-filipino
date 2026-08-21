#!/usr/bin/env bash
# P4 CUDA-host environment. Source from the repo root on the named NVIDIA host.
# MUST NOT source scripts/p1/env.sh, scripts/p2/env.sh, or scripts/p3/env.sh
# MUST NOT source this file as proof that the parent started.

if [[ -n "${P3_RUN_ID:-}" || -n "${P3_ROOT:-}" ]]; then
  echo "P4 CUDA env refuses: scripts/p3/env.sh appears sourced" >&2
  return 1 2>/dev/null || exit 1
fi

if [[ -z "${NANOCHAT_FILIPINO_ROOT:-}" ]]; then
  export NANOCHAT_FILIPINO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi

# shellcheck source=/dev/null
source "$NANOCHAT_FILIPINO_ROOT/scripts/p4/env.sh" || return 1 2>/dev/null || exit 1

export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
# Packed streams from Gates E/F. Do not point at p3-*-active paths.
export NANOCHAT_DATA_DIR_TL="${NANOCHAT_BASE_DIR}/streams/c1_tl"
export NANOCHAT_DATA_DIR_EN="${NANOCHAT_BASE_DIR}/streams/c2_en"
export NANOCHAT_DATA_DIR_C3="${NANOCHAT_BASE_DIR}/streams/c3_mix"
unset NANOCHAT_DATA_DIR || true
unset NANOCHAT_DATA_DIR_B3 || true

echo "NANOCHAT_DATA_DIR_TL=$NANOCHAT_DATA_DIR_TL"
echo "NANOCHAT_DATA_DIR_EN=$NANOCHAT_DATA_DIR_EN"
echo "NANOCHAT_DATA_DIR_C3=$NANOCHAT_DATA_DIR_C3"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "NOTE: CUDA env only. Parent / children have not started. Confirmatory class is NVIDIA CUDA (A40 class)."
