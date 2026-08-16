# Host amendment — Runpod NVIDIA A40 named for official Gate I

- Date (UTC): 2026-08-16
- Operator: Paul Pajo
- Classification: **new named NVIDIA CUDA host for confirmatory I**
- Pod: `68bei7d3vx4krc` (`p1-gate-i`)
- GPU: NVIDIA A40, 48 GB, EU-SE-1, Secure Cloud, $0.44/hr
- Image: `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404`
- torch (project venv): `2.9.1+cu128`
- Volume: 80 GB pod volume at `/workspace` (network volumes unavailable in A40 DCs)
- Input: `transfer/p1.1-gate-i-notest-20260816.zip` (no `test.jsonl`)
- Preflight: `manifests/runpod_gate_i_preflight.json` (`ok: true`)
- `--require-pre-i`: exit 0
- d20 memory fit: `T=2048`, `--device-batch-size=8`, peak 27.65 GiB
- Auto-terminate: 2026-08-17T02:54:15Z

Gate H host `p7e5zk3njnglgy` is preserved separately and is not this Pod.
