# P2 Gate I — EN0 d8 complete (d20 not started)

- Date (UTC): 2026-08-17T16:23:37Z–17:41Z (wall 73.18 min)
- Pod: `xk8orhscuk2jsu`, NVIDIA A40 48 GB, EU-SE-1, $0.44/hr
- Image: `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404` · torch `2.9.1+cu128`
- **EN0 d8 started and finished \(N_{\mathrm{EN0}}=5415\).**
- **EN0 d20 has not started.** Gate I is not fully passed. **No Tagalog. No P0 yet.**

## Command

`--depth=8 --max-seq-len=2048 --device-batch-size=8 --total-batch-size=65536 --num-iterations=5415 --warmup-steps=40 --eval-tokens=124438 --eval-every=50 --core-metric-every=-1 --sample-every=200 --save-every=200 --model-tag=p2-en0-d8`

English `en-active` only. No `ratio=-1`. No P1 env. No P1.1 parent weights. Final checkpoint (not in-loop val-best). In-loop val is **not** `val_bpb_full`.

## Results

| Field | Value |
|---|---|
| Train loss | **10.397712 → 2.077411** (step 5414) |
| In-loop val BPB | **3.205935 → 1.070887** (step 5415); min in-loop 1.011524 (diagnostic only) |
| Final ckpt | `model_005415.pt` (321 MiB) |
| SHA-256 | `5e1db47f0609995e2309a2c04ede4cd330aa0f2d113e07d6498790d5ca707a8c` |
| Reload | ok (63 keys) |
| Peak VRAM | 4775 MiB |

Log: `docs/run-cards/p2/p2-20260817T150944Z-de99f8a/p2-en0-d8.log`

Samples are English-ish encyclopedia fragments, not Tagalog Wikipedia.

## Still banned

- Starting Tagalog continuation
- Reading English or Tagalog test
- Uploading to `pageman/nanochat-filipino-p1-fixed-d20-3x`
- Treating in-loop 124438-token val as `val_bpb_full`
- Declaring full Gate I pass before EN0 d20 finishes \(N=5415\)

Empty HF repo `pageman/nanochat-filipino-p2-en-then-tl` was **not** created in this launch (protocol I.1.3 still open).
