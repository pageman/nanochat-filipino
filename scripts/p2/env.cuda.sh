#!/usr/bin/env bash
# P2 CUDA-host environment. Source from the repo root on the named NVIDIA host.
# MUST NOT source scripts/p1/env.sh
# MUST NOT source this file as proof that EN0 started.

if [[ -z "${P2_ROOT:-}" ]]; then
  export P2_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
export P2_RUN_ID="${P2_RUN_ID:-p2-20260817T150944Z-de99f8a}"
export NANOCHAT_BASE_DIR="${NANOCHAT_BASE_DIR:-$P2_ROOT/data/cache/${P2_RUN_ID}}"
export NANOCHAT_DATA_DIR_EN="$P2_ROOT/data/processed/wikitext-103/en-active"
export NANOCHAT_DATA_DIR_TL="$P2_ROOT/data/processed/p2-tl39-readonly"
export NANOCHAT_DATA_DIR_A3="$P2_ROOT/data/processed/p2-mix-a3-50-50"
export VIRTUAL_ENV="${VIRTUAL_ENV:-$P2_ROOT/vendor/nanochat/.venv}"
export PATH="$VIRTUAL_ENV/bin:$PATH"
export WANDB_RUN=dummy
export WANDB_MODE=disabled
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
unset NANOCHAT_DATA_DIR || true

echo "P2_ROOT=$P2_ROOT"
echo "P2_RUN_ID=$P2_RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "NANOCHAT_DATA_DIR=${NANOCHAT_DATA_DIR-<unset>}"
echo "NANOCHAT_DATA_DIR_EN=$NANOCHAT_DATA_DIR_EN"
echo "python=$(command -v python)"
echo "NOTE: EN0 has not started. This file only sets paths."
