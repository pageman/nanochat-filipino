# P2 Gate H d4 smoke — `xk8orhscuk2jsu`

- Date (UTC): 2026-08-17T16:12:42Z–16:13:20Z
- Pod: `xk8orhscuk2jsu` (`p2-gate-h-smoke`), NVIDIA A40 48 GB, EU-SE-1, Secure Cloud, $0.44/hr
- Image: `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404` · torch `2.9.1+cu128` · SM 8.6
- Attention: pin FA3 not present on this image; **unpatched SDPA** fallback (no `flash_attention.py` edit)
- Log: `docs/run-cards/p2/p2-20260817T150944Z-de99f8a/p2-gate-h-smoke.log`
- **EN0 has not started.** `--num-iterations=30`, not 5415.

## Command (as run)

`--depth=4 --max-seq-len=2048 --device-batch-size=8 --total-batch-size=65536 --num-iterations=30 --warmup-steps=3 --eval-tokens=8192 --eval-every=10 --core-metric-every=-1 --sample-every=15 --save-every=30 --model-tag=p2-smoke-en-d4`

`NANOCHAT_DATA_DIR` = English `en-active`. No `ratio=-1`. No P1 env. No P1.1 weights.

## Acceptance

| ID | Result |
|---|---|
| H0 | pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; `flash_attention.py` diff empty; hook only on `dataset.py` |
| H1 | last train loss finite: **6.401896** |
| H2 | last train loss **<** step-0: **10.397203 → 6.401896** |
| H3 | in-loop val BPB **inf at every eval** (see hole below). Not a scored descent. |
| H4 | checkpoint reloadable: `model_000030.pt` SHA-256 `5c801758f6932350d3769bb615fdcb5b655de7e88de46261651adb510e05fe73` |
| H5 | warmup 3 < 30 |
| H6 | CORE off (`--core-metric-every=-1`); no DCLM fetch |
| H7 | samples are English prompt completions / boilerplate (`The capital of France…`); **not** Tagalog Wikipedia |

In-loop val is **not** `val_bpb_full`.

## H3 hole (do not patch attention)

`eval_steps = eval_tokens // (device_batch_size * T) = 8192 // (8 * 2048) = 0`.

`evaluate_bpb` then sums zero batches, `total_bytes==0`, returns `inf`. This is a smoke **eval-window** bug, not a failed English descent. Train H2 is real.

A labeled re-smoke that keeps d4 / T=2048 / 30 / warmup 3 and sets `--eval-tokens=32768` (eval_steps=2) would make H3 scorable. That re-smoke is still not EN0.

## Status

**Gate H is not passed on this card.** Do not start Gate I. Do not declare EN0 started.

Correction: labeled re-smoke `p2-resmoke-en-d4-eval32768-not-en0` with `--eval-tokens=32768` is `p2-gate-h-xk8orhscuk2jsu-20260817T161800Z.md`.

Do not merge this card into P1.1 `execution_host.json`.
