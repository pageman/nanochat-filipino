#!/usr/bin/env bash
# P3 CUDA-host environment. Source from the repo root on the named NVIDIA host.
# MUST NOT source scripts/p1/env.sh or scripts/p2/env.sh
# MUST NOT source this file as proof that TL0 started.

if [[ -z "${NANOCHAT_FILIPINO_ROOT:-}" ]]; then
  if [[ -n "${P3_ROOT:-}" ]]; then
    export NANOCHAT_FILIPINO_ROOT="$P3_ROOT"
  else
    export NANOCHAT_FILIPINO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
  fi
fi

# shellcheck source=/dev/null
source "$NANOCHAT_FILIPINO_ROOT/scripts/p3/env.sh"

export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export NANOCHAT_DATA_DIR_TL="$NANOCHAT_FILIPINO_ROOT/data/processed/p3-tl39-active"
export NANOCHAT_DATA_DIR_EN="$NANOCHAT_FILIPINO_ROOT/data/processed/p3-en-active"
export NANOCHAT_DATA_DIR_B3="$NANOCHAT_FILIPINO_ROOT/data/processed/p3-mix-b3-50-50"
# Pod: Gate C hygiene may leave processed/ read-only; prefer clean staging when populated.
if [[ -f "$NANOCHAT_FILIPINO_ROOT/data/staging/en-clean/train_00000.parquet" ]]; then
  export NANOCHAT_DATA_DIR_EN="$NANOCHAT_FILIPINO_ROOT/data/staging/en-clean"
elif [[ -f "$NANOCHAT_FILIPINO_ROOT/data/staging/en-run/train_00000.parquet" ]]; then
  export NANOCHAT_DATA_DIR_EN="$NANOCHAT_FILIPINO_ROOT/data/staging/en-run"
fi
if [[ -f "$NANOCHAT_FILIPINO_ROOT/data/staging/b3-clean/train_00000.parquet" ]]; then
  export NANOCHAT_DATA_DIR_B3="$NANOCHAT_FILIPINO_ROOT/data/staging/b3-clean"
elif [[ -f "$NANOCHAT_FILIPINO_ROOT/data/staging/b3-run/train_00000.parquet" ]]; then
  export NANOCHAT_DATA_DIR_B3="$NANOCHAT_FILIPINO_ROOT/data/staging/b3-run"
fi
unset NANOCHAT_DATA_DIR || true

echo "NANOCHAT_DATA_DIR_TL=$NANOCHAT_DATA_DIR_TL"
echo "NANOCHAT_DATA_DIR_EN=$NANOCHAT_DATA_DIR_EN"
echo "NOTE: CUDA env only. TL0 has not started."
