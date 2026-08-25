#!/usr/bin/env bash
# Idempotent CPU development-environment bootstrap for nanochat-filipino.
#
# Creates a project virtualenv at .venv and installs the CPU verification
# toolchain (requirements-dev.txt). Safe to re-run: it reuses an existing
# .venv and lets pip skip already-satisfied packages.
#
# This does NOT set up GPU training. Confirmatory Gate H/I training and Gate J
# BPB evaluation require a named NVIDIA CUDA host and a separate vendor/nanochat
# checkout; see scripts/p1/setup_spark.sh and reproducibility/environment_lock.txt.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="$ROOT/.venv"

echo "== nanochat-filipino CPU dev setup =="
echo "root:   $ROOT"
echo "python: $("$PYTHON_BIN" --version 2>&1)"

# The stdlib `venv` module needs ensurepip, which is packaged separately on
# Debian/Ubuntu. Install it once if missing so `python -m venv` can bootstrap pip.
if ! "$PYTHON_BIN" -c "import ensurepip" >/dev/null 2>&1; then
  echo "ensurepip missing; installing python venv support via apt"
  PY_MM="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  if command -v sudo >/dev/null 2>&1; then APT="sudo apt-get"; else APT="apt-get"; fi
  $APT update -y
  $APT install -y "python${PY_MM}-venv"
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
  echo "Creating virtualenv at $VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip >/dev/null
python -m pip install -r "$ROOT/requirements-dev.txt"

echo "== installed =="
python -c "import sys, pyarrow, pytest; print('python', sys.version.split()[0]); print('pyarrow', pyarrow.__version__); print('pytest', pytest.__version__)"
echo "Done. Activate with: source .venv/bin/activate"
