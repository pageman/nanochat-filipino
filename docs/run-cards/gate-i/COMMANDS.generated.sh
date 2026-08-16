#!/usr/bin/env bash
# Generated. Confirmatory commands are NVIDIA-only.

# --- confirmatory d8 (NVIDIA only) ---
# Execute ONLY on the named NVIDIA CUDA host after official Gate H passes.
# Do not run this command on the Mac. Do not pass --target-param-data-ratio=-1.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
export OMP_NUM_THREADS=1
# Set DEVICE_BATCH on the GPU host; start at 8 and halve until VRAM fits.
# Preserve --total-batch-size=65536 via gradient accumulation.

python -m scripts.base_train \
  --device-type=cuda \
  --depth=8 \
  --max-seq-len=2048 \
  --device-batch-size=${DEVICE_BATCH} \
  --total-batch-size=65536 \
  --num-iterations=294 \
  --target-param-data-ratio=0.45783403148331536 \
  --eval-tokens=262144 \
  --eval-every=50 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --save-every=200 \
  --warmup-steps=14 \
  --run=p1-fixed-d8-3x \
  --model-tag=p1-fixed-d8-3x

# --- mac preflight d8 (non-confirmatory) ---
# Non-confirmatory Mac MPS one-step dry run. confirmatory_eligible=false.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
unset PYTORCH_ENABLE_MPS_FALLBACK
export OMP_NUM_THREADS=1

python -m scripts.base_train \
  --device-type=mps \
  --depth=8 \
  --max-seq-len=2048 \
  --device-batch-size=1 \
  --total-batch-size=2048 \
  --num-iterations=1 \
  --target-param-data-ratio=0.45783403148331536 \
  --eval-every=-1 \
  --eval-tokens=2048 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=1 \
  --warmup-steps=1 \
  --run=dummy \
  --model-tag=p1-m4-mps-gatei-preflight-d8

# --- confirmatory d12 (NVIDIA only) ---
# Execute ONLY on the named NVIDIA CUDA host after official Gate H passes.
# Do not run this command on the Mac. Do not pass --target-param-data-ratio=-1.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
export OMP_NUM_THREADS=1
# Set DEVICE_BATCH on the GPU host; start at 8 and halve until VRAM fits.
# Preserve --total-batch-size=65536 via gradient accumulation.

python -m scripts.base_train \
  --device-type=cuda \
  --depth=12 \
  --max-seq-len=2048 \
  --device-batch-size=${DEVICE_BATCH} \
  --total-batch-size=65536 \
  --num-iterations=294 \
  --target-param-data-ratio=0.17441307843117593 \
  --eval-tokens=262144 \
  --eval-every=50 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --save-every=200 \
  --warmup-steps=14 \
  --run=p1-fixed-d12-3x \
  --model-tag=p1-fixed-d12-3x

# --- mac preflight d12 (non-confirmatory) ---
# Non-confirmatory Mac MPS one-step dry run. confirmatory_eligible=false.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
unset PYTORCH_ENABLE_MPS_FALLBACK
export OMP_NUM_THREADS=1

python -m scripts.base_train \
  --device-type=mps \
  --depth=12 \
  --max-seq-len=2048 \
  --device-batch-size=1 \
  --total-batch-size=2048 \
  --num-iterations=1 \
  --target-param-data-ratio=0.17441307843117593 \
  --eval-every=-1 \
  --eval-tokens=2048 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=1 \
  --warmup-steps=1 \
  --run=dummy \
  --model-tag=p1-m4-mps-gatei-preflight-d12

# --- confirmatory d16 (NVIDIA only) ---
# Execute ONLY on the named NVIDIA CUDA host after official Gate H passes.
# Do not run this command on the Mac. Do not pass --target-param-data-ratio=-1.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
export OMP_NUM_THREADS=1
# Set DEVICE_BATCH on the GPU host; start at 8 and halve until VRAM fits.
# Preserve --total-batch-size=65536 via gradient accumulation.

python -m scripts.base_train \
  --device-type=cuda \
  --depth=16 \
  --max-seq-len=2048 \
  --device-batch-size=${DEVICE_BATCH} \
  --total-batch-size=65536 \
  --num-iterations=294 \
  --target-param-data-ratio=0.08175618397870534 \
  --eval-tokens=262144 \
  --eval-every=50 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --save-every=200 \
  --warmup-steps=14 \
  --run=p1-fixed-d16-3x \
  --model-tag=p1-fixed-d16-3x

# --- mac preflight d16 (non-confirmatory) ---
# Non-confirmatory Mac MPS one-step dry run. confirmatory_eligible=false.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
unset PYTORCH_ENABLE_MPS_FALLBACK
export OMP_NUM_THREADS=1

python -m scripts.base_train \
  --device-type=mps \
  --depth=16 \
  --max-seq-len=2048 \
  --device-batch-size=1 \
  --total-batch-size=2048 \
  --num-iterations=1 \
  --target-param-data-ratio=0.08175618397870534 \
  --eval-every=-1 \
  --eval-tokens=2048 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=1 \
  --warmup-steps=1 \
  --run=dummy \
  --model-tag=p1-m4-mps-gatei-preflight-d16

# --- confirmatory d20 (NVIDIA only) ---
# Execute ONLY on the named NVIDIA CUDA host after official Gate H passes.
# Do not run this command on the Mac. Do not pass --target-param-data-ratio=-1.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
export OMP_NUM_THREADS=1
# Set DEVICE_BATCH on the GPU host; start at 8 and halve until VRAM fits.
# Preserve --total-batch-size=65536 via gradient accumulation.

python -m scripts.base_train \
  --device-type=cuda \
  --depth=20 \
  --max-seq-len=2048 \
  --device-batch-size=${DEVICE_BATCH} \
  --total-batch-size=65536 \
  --num-iterations=294 \
  --target-param-data-ratio=0.044128661662655576 \
  --eval-tokens=262144 \
  --eval-every=50 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --save-every=200 \
  --warmup-steps=14 \
  --run=p1-fixed-d20-3x \
  --model-tag=p1-fixed-d20-3x

# --- mac preflight d20 (non-confirmatory) ---
# Non-confirmatory Mac MPS one-step dry run. confirmatory_eligible=false.
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
unset PYTORCH_ENABLE_MPS_FALLBACK
export OMP_NUM_THREADS=1

python -m scripts.base_train \
  --device-type=mps \
  --depth=20 \
  --max-seq-len=2048 \
  --device-batch-size=1 \
  --total-batch-size=2048 \
  --num-iterations=1 \
  --target-param-data-ratio=0.044128661662655576 \
  --eval-every=-1 \
  --eval-tokens=2048 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=1 \
  --warmup-steps=1 \
  --run=dummy \
  --model-tag=p1-m4-mps-gatei-preflight-d20
