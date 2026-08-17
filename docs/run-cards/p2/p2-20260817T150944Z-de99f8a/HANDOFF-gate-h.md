# P2 Gate H handoff — wait for a named NVIDIA CUDA host

**Study:** NANOCHAT-FILIPINO P2-EN→TL  
**Registration:** AsPredicted **#306935** · https://aspredicted.org/xa56bs.pdf · ResearchBox **#8763**  
**Does not amend** AsPredicted #306780 or ResearchBox #8735.  
**P2_RUN_ID:** `p2-20260817T150944Z-de99f8a`  
**Packed from:** Mac/CPU (Gates 0, A–G). Date (UTC): 2026-08-17.  
**Gate H status:** prepared, **not executed**. `gpu_host_for_H_I` is **null**.

> **EN0 has not started.** Preparing this handoff, copying files, or bringing up a GPU pod does not start confirmatory English pretraining.

**No P1 environment. No P1.1 parent weights. No `ratio=-1`. No `python -m nanochat.dataset`. No test evaluation. No Tagalog continuation. No declaration that EN0 has started merely by preparing the GPU host.**

The $3.91 / ~8.9 A40-hour figure in Gate G is a **planning estimate** only. It is not a commitment. Actual cost depends on the named host, disk state, eval overhead, and observed smoke throughput.

---

## Hard stops (operational)

**Do not:**

- source `scripts/p1/env.sh` or any P1 environment
- load P1.1 parent weights (`p1-fixed-d20-3x` / `model_000294.pt` SHA `9e30fff3…dde38`)
- pass `--target-param-data-ratio=-1`
- run `python -m nanochat.dataset` (ClimbMix)
- evaluate English test or Tagalog `test.jsonl`
- point `NANOCHAT_DATA_DIR` at Tagalog or A3 for this smoke
- start Tagalog continuation (A2) or mix (A3)
- patch `nanochat/flash_attention.py`
- run this smoke on Mac MPS
- run this smoke on DGX Spark until a **labeled unpatched** `p2-spark-smoke-*` card exists (P1.1 Spark H2 failed; see `docs/run-cards/deviations/2026-08-17-dgx-spark-gate-h-h2.md`)
- declare that EN0 has started merely by preparing the GPU host
- upload anywhere under `pageman/nanochat-filipino-p1-fixed-d20-3x`
- treat in-loop `--eval-tokens=8192` as `val_bpb_full`

**Do:** source `scripts/p2/env.cuda.sh` on the GPU host. Use English `en-active` only. Keep warmup **3 < 30**.

---

## Immutable identifiers (do not regenerate)

| Item | Frozen value |
|---|---|
| nanochat pin | `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` |
| Hook only | `patches/nanochat-NANOCHAT_DATA_DIR.patch` SHA `faaded83ef79e6d5b2e6856a444cf17e20ddb534ddd29d6b600f9568304ec4ff` |
| English split | `wikitext103_official_raw_splits` |
| `tokenizer.pkl` | `946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6` |
| `token_bytes.pt` | `5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42` |
| P1.1 tokenizer (do **not** use) | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| `T_en_train` | 118,286,771 |
| `D_3x_en` | 354,860,313 |
| `B` | 65,536 |
| `N_EN0` | 5,415 (Gate **I**, not this smoke) |
| `D_actual_en0` | 354,877,440 |
| `D_phase2` | 19,267,584 (294 steps; continuation, not EN0) |
| `T` | 2048 |
| A3 mix SHA | `b6ae432b625b6768f84db3f45c411378d1d5a5fdbd15cbfc0e5f6c511196b1a0` (not used in H) |

English train/val parquet SHA256 (Gate E):

| File | SHA256 |
|---|---|
| `train_00000.parquet` | `9bdee964368da85a9b97af0d8cd50c4cd13ec392a8045dbec602ce31bd587861` |
| `train_00001.parquet` | `7331e6219eec3bf619b92c38f686778395b77b500d267cfb25412abb41c6379c` |
| `train_00002.parquet` | `59bc144b0191d10009baa7698bbb96ba25c2c750b7ab8cdbc9bba52998c4d9f7` |
| `train_00003.parquet` | `ac693bfc6c1820e9f978f90958b1afb4bf82d91c9bcbba682467d6a357ebcb0b` |
| `val.parquet` (last / val) | `b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f` |

---

## What to copy (English smoke only)

Copy hashes, do not rebuild.

```text
vendor/nanochat/                          # detached HEAD at pin + DATA_DIR hook
data/processed/wikitext-103/en-active/    # four train shards + val.parquet
data/cache/p2-20260817T150944Z-de99f8a/tokenizer/
scripts/p2/
docs/papers/p2-cf-english/LOCK.json
docs/run-cards/p2/p2-20260817T150944Z-de99f8a/
patches/nanochat-NANOCHAT_DATA_DIR.patch
```

Do **not** copy Tagalog train, A3 mix, English test, P1.1 `test.jsonl`, or `p1-fixed-d20-3x` weights into the smoke `NANOCHAT_DATA_DIR`.

On the GPU host, `P2_ROOT` is the unpacked repo (not the Mac path in `scripts/p2/env.sh`).

---

## On the CUDA host, in order

```bash
cd "$P2_ROOT"
source scripts/p2/env.cuda.sh
# 1) CUDA / pin / hashes. Exit 0 is required. This still does not start EN0.
python3 scripts/p2/gate_h_preflight.py
# 2) Confirmatory-path d4 smoke (T=2048).
bash scripts/p2/gate_h_smoke.sh
```

If VRAM OOM: `DEVICE_BATCH=4 bash scripts/p2/gate_h_smoke.sh` (then 2, then 1). **Do not** drop `T` below 2048 for a confirmatory H pass. A labeled `T=512` smoke may prove wiring only; it does **not** pass H for d20 EN0.

### Exact d4 command (also inside `gate_h_smoke.sh`)

```bash
cd "$P2_ROOT/vendor/nanochat"
export NANOCHAT_BASE_DIR="$P2_ROOT/data/cache/p2-20260817T150944Z-de99f8a"
export NANOCHAT_DATA_DIR="$P2_ROOT/data/processed/wikitext-103/en-active"
export WANDB_MODE=disabled OMP_NUM_THREADS=1

python -m scripts.base_train \
  --device-type=cuda \
  --depth=4 \
  --max-seq-len=2048 \
  --device-batch-size=${DEVICE_BATCH:-8} \
  --total-batch-size=65536 \
  --num-iterations=30 \
  --warmup-steps=3 \
  --eval-tokens=8192 \
  --eval-every=10 \
  --core-metric-every=-1 \
  --sample-every=15 \
  --save-every=30 \
  --model-tag=p2-smoke-en-d4 \
  --run=p2-smoke-en-d4
```

**Checkpoint destination:**  
`$NANOCHAT_BASE_DIR/base_checkpoints/p2-smoke-en-d4/`  
Expect `model_000030.pt` (final). Card name after a pass: `p2-gate-h-<gpu-id>-<timestamp>.md`. Do **not** merge into P1.1 `execution_host.json`.

Omit `--target-param-data-ratio` (pin default is 12, unused when `--num-iterations` is explicit). **Never** pass `-1`.

### Optional d8 smoke (not EN0, not required for H)

Same 30-step recipe, `--depth=8`, `--model-tag=p2-smoke-en-d8-not-en0`. **Forbidden:** `--num-iterations=5415` on this tag (that would be Gate I). A d8 smoke does not replace the d4 confirmatory-path H card and does not start EN0.

---

## Acceptance (H2 analogue)

| ID | Pass |
|---|---|
| H0 | pin match; `flash_attention.py` diff vs pin empty |
| H1 | last train loss finite |
| H2 | last train loss **<** step-0 train loss |
| H3 | last val BPB **<** first val BPB (or < untrained if logged in-process) |
| H4 | checkpoint reloadable |
| H5 | `--warmup-steps=3` < `--num-iterations=30` |
| H6 | no CORE / no DCLM fetch (`--core-metric-every=-1`) |
| H7 | samples English-ish or garbage; **not** Tagalog Wikipedia boilerplate (wrong `NANOCHAT_DATA_DIR`) |

In-loop val here is **8192 tokens**, operational only. It does not replace registered `val_bpb_full`.

If H fails: file a dated deviation. **Do not** start Gate I. **Do not** patch attention. Try A40 if the host was Spark/MPS.

---

## After H passes (not now)

1. Name the host in a new `p2-gate-h-<gpu-id>-<timestamp>.md`.  
2. Then Gate I EN0: d8 first (`--num-iterations=5415`, `--warmup-steps=40`), then d20, **final** checkpoint, same CUDA class.  
3. Still no Tagalog train token until P0-E on EN0.

Mac Gates A–G remain the lock. Recheck hashes on the GPU host; do not retrain the tokenizer.
