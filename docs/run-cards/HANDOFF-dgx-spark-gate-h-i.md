# DGX Spark hand-off — official Gates H and I

**Study:** NANOCHAT-FILIPINO P1.1  
**Registration:** AsPredicted #306780 · ResearchBox #8735  
**Parent RUN_ID:** `p1-20260816T025911Z-0067a57`  
**Offer:** `dgx_spark_gate_h_i_assessment.md` (included)  
**Date packed (UTC):** 2026-08-16  
**Packed from:** MacBook Pro Mac16,1 (Gates A–G only)

> **Control.** The Spark is *conditionally eligible*, not automatically official. Name it in `execution_host.json` only after `scripts/p1/spark_host_preflight.py` exits 0. Mac MPS jobs are not Gate H and not Gate I.

---

## 1. What this bundle is

A frozen transfer of the confirmatory apparatus after Gates **A–G passed** on the Mac. It contains the locked corpus shards, train-only tokenizer, isolated test set, manifests, generated Gate I cards, and setup scripts. It does **not** contain:

- the Mac CPU/MPS virtualenv
- Mac MPS checkpoints
- confirmatory `val_bpb_full` or `test_bpb` (they do not exist)
- the ResearchBox passcode
- a pre-named `gpu_host_for_H_I`

Official H and confirmatory I have **not** started.

---

## 2. What already happened (A–G, do not redo)

| Gate | Status | Keep these facts |
|---|---|---|
| A | pass | nanochat pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; hook patch SHA `faaded83…`; no ClimbMix download |
| B | pass | `train.parquet` SHA `706d7064…`; 1,524,071 rows; S3 404 |
| C | pass | LF-only canonical; registered drops 0; 120,971 articles |
| D | pass | **`reconstructed_article_70_15_15`**; 37,602 / 8,058 / 8,058; exact hash overlap 0 |
| E | pass | `active/shard_00000`+`00001` train, `00002` val last; test not in `active/` |
| F | pass | train-only 32768 BPE; `tokenizer.pkl` `04436b85…`; `token_bytes.pt` `a5dbc1c8…` |
| G | pass | `T_train=6401013`; `D_3x=19203039`; `B=65536`; `N=294`; `D_actual=19267584`; `T=2048` |

Do **not** re-download the parquet, re-split, or retrain the tokenizer. Recheck hashes only.

Mac-only (not official): `project1_m4_mps_preH` and one-step d8/d12/d16 dry-runs. d20 MPS OOM at `T=2048` is a Mac finding. It does **not** drop depth 20.

---

## 3. Unpack on the Spark

```bash
# On the DGX Spark
mkdir -p ~/p1 && cd ~/p1
unzip p1.1-dgx-spark-handoff-20260816.zip
cd p1.1-dgx-spark-handoff/nanochat-filipino
chmod 0444 data/processed/wikitext-tl39/test/test.jsonl
# Confirm you will not train from the test directory.
```

Expected layout after unzip:

```text
nanochat-filipino/
  data/raw/wikitext-tl39/train.parquet          # provenance; write-protect
  data/processed/wikitext-tl39/active/          # train+val shards
  data/processed/wikitext-tl39/test/            # isolated; do not train
  data/cache/p1-20260816T025911Z-0067a57/tokenizer/
  data/interim/wikitext-tl39/splits/{train,val}.jsonl
  manifests/   docs/   scripts/p1/   patches/   configs/
```

---

## 4. Spark preflight (required before naming the host)

The Spark is ARM64 + Blackwell. The Mac used `torch 2.9.1+cpu`. You must install a **real CUDA** environment on the Spark without editing nanochat model, dataloader, tokenizer, split, or evaluator code.

```bash
# 1) Record the machine (save the output)
uname -a
uname -m          # expect aarch64
cat /etc/os-release
nvidia-smi
nvcc --version || true

# 2) Clone the pinned nanochat and install GPU extra
bash scripts/p1/setup_spark.sh

# 3) Frozen-input + CUDA preflight (no training)
source scripts/p1/env.spark.sh
python scripts/p1/spark_host_preflight.py
# must exit 0 and write manifests/spark_host_preflight.json
```

`setup_spark.sh` runs `uv sync --extra gpu` against pin `92d63d4` and applies `patches/nanochat-NANOCHAT_DATA_DIR.patch`. If the extra resolves a CPU wheel, `torch.cuda.is_available()` is false, a required ARM64 package is missing, or anyone changes application code to “make it work,” **stop**. Classify the Spark `blocked`. Do not start official H.

Also run:

```bash
python scripts/p1/preflight.py --check-apparatus
# --require-pre-i must still FAIL until official H passes. That is correct.
```

If preflight exits 0, fill `manifests/execution_host.spark.template.json` with the real hostname, `nvidia-smi` name, driver, CUDA, torch, and wheel/container digest. Merge that object into `manifests/execution_host.json` as `gpu_host_for_H_I`. Record **DGX Spark / GB10 / Arm64** explicitly. Only then is the host named.

---

## 5. Official Gate H (CUDA only)

Single process. No `torchrun` on one GPU. No FP8 unless you separately document Hopper (Spark is not Hopper). CORE off. Do not pass `--target-param-data-ratio=-1`.

```bash
source scripts/p1/env.spark.sh
cd "$P1_ROOT/vendor/nanochat"
export OMP_NUM_THREADS=1
export WANDB_RUN=dummy

python -m scripts.base_train \
  --device-type=cuda \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=1 \
  --total-batch-size=2048 \
  --num-iterations=30 \
  --eval-tokens=4096 \
  --eval-every=10 \
  --core-metric-every=-1 \
  --sample-every=15 \
  --save-every=30 \
  --model-tag=p1-smoke-d4 \
  --run=dummy
```

Then a **fresh process** reload (val/train BPB only — never test):

```bash
source scripts/p1/env.spark.sh
cd "$P1_ROOT/vendor/nanochat"
python -m scripts.base_eval \
  --eval=bpb \
  --model-tag=p1-smoke-d4 \
  --device-type=cuda \
  --device-batch-size=1 \
  --split-tokens=4096
```

### H acceptance

| ID | Pass if |
|---|---|
| H1 | Train loss finite at step 30 |
| H2 | Train loss at 30 < train loss at step 1 |
| H3 | `data/cache/p1-20260816T025911Z-0067a57/base_checkpoints/p1-smoke-d4` exists |
| H4 | Sample has a Tagalog function word, or is garbage; **not** fluent English ClimbMix |
| H5 | `--core-metric-every=-1`; no CORE/eval_bundle download |
| H6 | Fresh-process reload emits finite val BPB |
| H7 | `NANOCHAT_DATA_DIR` is the three Tagalog shards; last file is val; test absent |
| H8 | Device is CUDA on the named Spark, not MPS, not CPU |

If H4 talks about the United States Congress, the data dir is wrong. Stop. Do not reuse that cache.

On pass: set ledger Gate H to `pass` with Spark identity and checkpoint hashes. Keep `confirmatory_outcomes.val_bpb_computed=false` and `test_read_events=0`. Then:

```bash
python scripts/p1/preflight.py --require-pre-i
# must now exit 0
```

---

## 6. Official Gate I (only after H pass)

Do not hand-edit the cards. Execute them from `docs/run-cards/gate-i/`. Shared frozen quantities:

- `T=2048`
- `total_batch_size=65536`
- `num_iterations=294` (must be passed explicitly)
- `D_actual=19267584`
- `eval-tokens=262144`
- `warmup-steps=14`
- `core-metric-every=-1`
- per-depth **positive** `--target-param-data-ratio` (never `-1`, never `12`)

| Tag | Depth | Ratio to pass | Card |
|---|---:|---:|---|
| `p1-fixed-d8-3x` | 8 | 0.45783403148331536 | `docs/run-cards/gate-i/p1-fixed-d8-3x.md` |
| `p1-fixed-d12-3x` | 12 | 0.17441307843117593 | `docs/run-cards/gate-i/p1-fixed-d12-3x.md` |
| `p1-fixed-d16-3x` | 16 | 0.08175618397870534 | `docs/run-cards/gate-i/p1-fixed-d16-3x.md` |
| `p1-fixed-d20-3x` | 20 | 0.044128661662655576 | `docs/run-cards/gate-i/p1-fixed-d20-3x.md` |

Set `DEVICE_BATCH` on the Spark. Start at 8. If VRAM/unified memory pressure appears, **halve `DEVICE_BATCH` only**. Preserve `B=65536` with gradient accumulation. Do **not** shrink `T`, drop d20, or change `B` or `N`.

```bash
source scripts/p1/env.spark.sh
export DEVICE_BATCH=8    # or 4, 2, 1 — never change T or B
# then the command from the matching run card, with --device-type=cuda
```

Confirmatory checkpoint is the **final step 294**, not mid-run val-best. After all four final `val_bpb_full` values exist: untrained same-depth baseline and Laplace add-1 byte unigram on val only; `D*` = exact minimum; gaps `< 0.01` BPB are practically indistinguishable; **one** test read for `D*` only.

d8/d12 `D_1x` pilots are optional secondary checks. `D_10x`, d24, CORE, chat, and detok stay exploratory.

---

## 7. Hard bans

- `python -m nanochat.dataset`
- `--target-param-data-ratio=-1`
- Official H or I on MPS/CPU
- Marking H pass from the Mac smoke
- Reading `test.jsonl` for BPB before validation-only `D*`
- Claiming original 2019 splits (label is `reconstructed_article_70_15_15`)
- Putting Mac engineering BPB in the main table
- Amending AsPredicted #306780
- Shipping or echoing the ResearchBox passcode

---

## 8. Hashes to recheck on the Spark

See `MANIFEST.sha256` in this zip and `scripts/p1/spark_host_preflight.py`. Critical:

| Object | SHA-256 |
|---|---|
| train.parquet | `706d706496e3a085cf4506f97aa8b03faa20d4773d69453eaab4e3ca8f33caf9` |
| shard_00000 | `aaf81d95e577742dcd33a44be2f144c253a5d5650e34b3e622e8b262ff2b6dc9` |
| shard_00001 | `c57c11a2625c38f7f12d1e4018e71bf1f38a56d68fcc9b4952e1b8bded854976` |
| shard_00002 val | `13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02` |
| tokenizer.pkl | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| token_bytes.pt | `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132` |
| test.jsonl | `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf` |
| nanochat commit | `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` |

---

## 9. What to send back

After work on the Spark, export (do not overwrite the Mac A–G lock):

- `manifests/spark_host_preflight.json`
- updated `manifests/execution_host.json` (only if preflight passed)
- Gate H logs + `p1-smoke-d4` checkpoint hashes
- updated `manifests/gate_ledger.json`
- each Gate I run’s final `meta_000294.json`, metrics, and `val_bpb_full`
- `manifests/test_access_log.json` (must stay 0 until D*)

---

## 10. Contact / ownership

Operator of the A–G lock: Paul Pajo (De La Salle – College of Saint Benilde).  
Public registration: https://aspredicted.org/6r6v4v.pdf  
If anything in this bundle disagrees with AsPredicted #306780, the PDF wins.
