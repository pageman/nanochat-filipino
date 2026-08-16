# Source from the extracted hand-off root on the DGX Spark.
# MUST NOT run: python -m nanochat.dataset
# Official H/I only after Spark CUDA preflight and a named host record.

if [ -z "${P1_ROOT:-}" ]; then
  export P1_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
export RUN_ID="p1-20260816T025911Z-0067a57"
export NANOCHAT_BASE_DIR="${P1_ROOT}/data/cache/${RUN_ID}"
export NANOCHAT_DATA_DIR="${P1_ROOT}/data/processed/wikitext-tl39/active"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export WANDB_RUN="${WANDB_RUN:-dummy}"
unset PYTORCH_ENABLE_MPS_FALLBACK

if [ -x "${P1_ROOT}/vendor/nanochat/.venv/bin/python" ]; then
  export VIRTUAL_ENV="${P1_ROOT}/vendor/nanochat/.venv"
  export PATH="${VIRTUAL_ENV}/bin:${PATH}"
fi

echo "P1_ROOT=$P1_ROOT"
echo "RUN_ID=$RUN_ID"
echo "NANOCHAT_BASE_DIR=$NANOCHAT_BASE_DIR"
echo "NANOCHAT_DATA_DIR=$NANOCHAT_DATA_DIR"
echo "uname=$(uname -m)"
