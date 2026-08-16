# Host amendment — Runpod NVIDIA A40 named for official H/I

- Date (UTC): 2026-08-16
- Operator: Paul Pajo
- Classification: **named NVIDIA CUDA host after preflight exit 0**
- Pod: `p7e5zk3njnglgy` (`p1-gate-h-smoke`)
- GPU: NVIDIA A40, 48 GB, CA-MTL-1, Secure Cloud, $0.44/hr
- Image: `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404`
- torch: `2.9.1+cu128`
- Preflight: `manifests/runpod_host_preflight.json` (`ok: true`)
- Auto-terminate: 2026-08-16T09:22:18Z

## Why this host

A6000 community ($0.33/hr) had no instances. A40 secure was the cheapest in-stock NVIDIA GPU with ≥40 GB. Host-local preflight hashed all frozen inputs, confirmed test isolation, CUDA matmul, and instantiated d4/d8/d12/d16/d20 at `T=2048` without shrinking `T`.

## Authorized now

Official Gate H only (`p1-smoke-d4`). Confirmatory I is not started. `$10` balance is treated as H-only.

## Still banned

- Marking H pass from Mac MPS
- Running `p1-fixed-d*-3x` before official H pass
- Shrinking `T=2048`, dropping d20, ratio `-1`, `python -m nanochat.dataset`
- Reading test BPB
- Leaving the Pod running after H without an explicit I go-ahead
