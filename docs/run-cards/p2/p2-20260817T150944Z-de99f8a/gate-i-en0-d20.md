# P2 Gate I — EN0 d20 complete ✓

- Date (UTC): 2026-08-17T17:57Z → 2026-08-18T03:17Z (wall ~481 min)
- Pod: `8ik4ix7j8iju9u`, NVIDIA A40 48 GB, EU-SE-1, $0.44/hr
- Image: `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404` · torch `2.9.1+cu128`
- **EN0 d20 finished at N_EN0 = 5415. Gate I fully passed.**
- Run was interrupted at step 2599 (volume full), then resumed from step 2400 with `--save-every=-1`. See `docs/run-cards/deviations/2026-08-17-en0-d20-resume-2400.md`.

## Command (resumed portion)

`--depth=20 --n-embd=1280 --n-head=10 --max-seq-len=2048 --device-batch-size=8 --total-batch-size=65536 --num-iterations=5415 --warmup-steps=40 --eval-tokens=124438 --eval-every=50 --core-metric-every=-1 --sample-every=200 --save-every=-1 --resume-from-step=2400 --model-tag=p2-en0-d20`

English `en-active` only. No `ratio=-1`. No P1 env. No P1.1 parent weights. Final checkpoint (not in-loop val-best). In-loop val is **not** `val_bpb_full`.

## Results

| Field | Value |
|---|---|
| Train loss (step 5414) | **0.218735** |
| In-loop val BPB (step 5415) | **1.531876** |
| Min in-loop val BPB | **0.978079** (diagnostic only) |
| Total training time | **481.39 min** |
| Final ckpt | `model_005415.pt` (2.48 GiB) |
| SHA-256 | `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d` |
| Reload | ok (147 keys; first key: `resid_lambdas`) |
| Peak VRAM | 25,650 MiB |
| Tok/sec (steady) | ~12,283 |

Log: `docs/run-cards/p2/p2-20260817T150944Z-de99f8a/p2-en0-d20.log`

## Gate I verdict

| Arm | Status |
|---|---|
| EN0 d8 | **complete** — `model_005415.pt` SHA `5e1db4…` |
| EN0 d20 | **complete** — `model_005415.pt` SHA `bd35a8…` |
| **Gate I** | **PASS** |

## Still banned

- Starting Tagalog continuation (requires Gate P0 first)
- Reading English or Tagalog test set
- Treating in-loop 124438-token val as `val_bpb_full`
- Using P1.1 weights as EN0 or A2 start weights

## Next step

**Gate P0 — Provenance battery** on both `p2-en0-d8/model_005415.pt` and `p2-en0-d20/model_005415.pt`.
Empty HF repo `pageman/nanochat-filipino-p2-en-then-tl` (protocol I.1.3) still open.
