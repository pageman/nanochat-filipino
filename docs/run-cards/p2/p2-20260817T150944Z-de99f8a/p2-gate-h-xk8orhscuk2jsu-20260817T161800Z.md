# P2 Gate H pass — labeled re-smoke `eval-tokens=32768`

- Date (UTC): 2026-08-17T16:17–16:18Z
- Pod: `xk8orhscuk2jsu` (`p2-gate-h-smoke`), NVIDIA A40 48 GB, EU-SE-1, Secure Cloud, $0.44/hr
- Image: `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404` · torch `2.9.1+cu128` · SM 8.6
- Attention: unpatched SDPA (FA3 not on image; `flash_attention.py` unmodified)
- **Status: pass**
- **EN0 has not started.** `--num-iterations=30`, not 5415. Gate I is not authorized by this card.

## Relation to the first smoke

| Run | Tag | `--eval-tokens` | `eval_steps` | In-loop val BPB |
|---|---|---|---|---|
| Zero-evaluation-window attempt | `p2-smoke-en-d4` | 8192 | 0 | inf (vacuous) |
| Prespecified correction | `p2-resmoke-en-d4-eval32768-not-en0` | **32768** | **2** | finite, descending |

The first run is kept as the config-defect record (`p2-gate-h-xk8orhscuk2jsu-20260817T161320Z.md`). This run did **not** resume `p2-smoke-en-d4/model_000030.pt` (`resume_from_step=-1`). The only substantive command change is `--eval-tokens=32768`.

## Command

`--depth=4 --max-seq-len=2048 --device-batch-size=8 --total-batch-size=65536 --num-iterations=30 --warmup-steps=3 --eval-tokens=32768 --eval-every=10 --core-metric-every=-1 --sample-every=15 --save-every=30 --model-tag=p2-resmoke-en-d4-eval32768-not-en0`

`NANOCHAT_DATA_DIR` = English `en-active`. No `ratio=-1`. No P1 env. No P1.1 weights. No test / no Tagalog.

Log: `docs/run-cards/p2/p2-20260817T150944Z-de99f8a/p2-resmoke-en-d4-eval32768.log`

## Acceptance

| ID | Result |
|---|---|
| H0 | pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; hook only |
| H1 | last train loss finite: **6.402673** |
| H2 | last train loss **<** step-0: **10.397203 → 6.402673** |
| H3 | last val BPB **<** first: **3.168204 → 1.841073** (also 2.105738 at step 10, 1.880376 at step 20); finite, non-NaN |
| H4 | checkpoint reloadable: `model_000030.pt` SHA-256 `7172600625c862b2ea1b33f1cb6e689c5171ebd75f5c27384021c77cff7dd946` |
| H5 | warmup 3 < 30 |
| H6 | CORE off |
| H7 | English prompt completions; not Tagalog Wikipedia |

In-loop val here is **32768 tokens** (two 16384-token batches). It does **not** replace registered `val_bpb_full`.

Checkpoint dir: `$NANOCHAT_BASE_DIR/base_checkpoints/p2-resmoke-en-d4-eval32768-not-en0/`

Do not merge into P1.1 `execution_host.json`. Do not start Gate I until an explicit EN0 go-ahead with `--num-iterations=5415`.
