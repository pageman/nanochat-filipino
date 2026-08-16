#!/usr/bin/env bash
# First-boot setup on the DGX Spark. Does not train. Does not name the host.
set -euo pipefail

P1_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
NANOCHAT_COMMIT="92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
VENDOR="${P1_ROOT}/vendor/nanochat"

echo "P1_ROOT=${P1_ROOT}"
echo "Expected uname -m: aarch64 (this host: $(uname -m))"

if [ ! -d "${VENDOR}/.git" ]; then
  mkdir -p "${P1_ROOT}/vendor"
  git clone https://github.com/karpathy/nanochat.git "${VENDOR}"
fi
git -C "${VENDOR}" fetch --all --tags
git -C "${VENDOR}" checkout "${NANOCHAT_COMMIT}"
if grep -q 'NANOCHAT_DATA_DIR' "${VENDOR}/nanochat/dataset.py"; then
  echo "NANOCHAT_DATA_DIR hook already present"
else
  git -C "${VENDOR}" apply "${P1_ROOT}/patches/nanochat-NANOCHAT_DATA_DIR.patch"
fi
if ! grep -q 'NANOCHAT_DATA_DIR' "${VENDOR}/nanochat/dataset.py"; then
  echo "ERROR: NANOCHAT_DATA_DIR hook missing after patch" >&2
  exit 2
fi

cd "${VENDOR}"
command -v uv >/dev/null || { echo "Install uv first: https://docs.astral.sh/uv/" >&2; exit 3; }

echo "Installing GPU extra. On ARM64 this must resolve a real CUDA wheel, not CPU."
echo "If uv sync --extra gpu fails or torch.cuda.is_available() is false, STOP and classify blocked."
uv sync --extra gpu

# shellcheck disable=SC1091
source "${P1_ROOT}/scripts/p1/env.spark.sh"
python - <<'PY'
import torch
print("torch", torch.__version__)
print("cuda", torch.version.cuda)
print("cuda_available", torch.cuda.is_available())
if not torch.cuda.is_available():
    raise SystemExit("CUDA unavailable after uv sync --extra gpu")
print("device", torch.cuda.get_device_name(0))
PY

echo "Setup finished. Next: source scripts/p1/env.spark.sh && python scripts/p1/spark_host_preflight.py"
echo "Do not run official Gate H until that preflight exits 0 and the host is named."
