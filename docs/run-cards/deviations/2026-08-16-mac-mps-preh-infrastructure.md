# Deviation / classification — Mac M4 MPS pre-H infrastructure validation

- Date (UTC): 2026-08-16 (written before the Mac training command)
- Operator: Paul Pajo
- RUN_ID (parent confirmatory package): `p1-20260816T025911Z-0067a57`
- Label: `project1_m4_mps_preH`
- Classification: **non-confirmatory Mac MPS infrastructure validation**
- Protocol: P1.1 / AsPredicted #306780

## Frozen statement affected

`manifests/execution_host.json` records this Mac for Gates A–G only. Gate H smoke and Gate I confirmatory training wait for a named NVIDIA GPU host (`gpu_host_for_H_I` is still null).

## Change

Run a tiny official `scripts.base_train` d4 job on this Mac using `--device-type=mps`, after Gates A–G have passed, to validate that the isolated cache, Tagalog shards, Tagalog tokenizer, trainer, checkpoint write, and checkpoint reload path work on the local machine.

This is **not** a host-policy amendment. Official Gate H remains unstarted until a named NVIDIA CUDA host is recorded.

## Why this is being done

Local end-to-end wiring can fail for reasons unrelated to the confirmatory question (data-dir hook, tokenizer path, checkpoint I/O, finite loss). A labeled Mac MPS smoke finds those failures before GPU time. It is not required by the registration.

## What is frozen and unchanged

- Corpus, split, tokenizer, `T_train`, `D_3x`, depths 8/12/16/20, and `T=2048` confirmatory budget
- No `python -m nanochat.dataset`
- No `--target-param-data-ratio=-1`
- No FP8, no `torchrun`, no MPS-to-CPU fallback env workaround
- No tokenizer/split/shard rewrite to make the Mac run work
- Test split is not read; no confirmatory `val_bpb_full` or `test_bpb`

## Mac command (pre-declared)

```bash
source scripts/p1/env.sh
cd "$P1_ROOT/vendor/nanochat"
# NANOCHAT_BASE_DIR and NANOCHAT_DATA_DIR remain the frozen project paths.

python -m scripts.base_train \
  --device-type=mps \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=1 \
  --total-batch-size=512 \
  --num-iterations=20 \
  --eval-every=10 \
  --eval-tokens=512 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=10 \
  --run=dummy \
  --model-tag=project1_m4_mps_preH
```

Deliberate differences from official Gate H / confirmatory runs:

| Setting | This Mac preflight | Official Gate H / Gate I |
|---|---|---|
| Host | Mac M4 MPS | Named NVIDIA CUDA host (not yet recorded) |
| `max-seq-len` | 512 | Gate H protocol example is 512; confirmatory I is 2048 |
| `total-batch-size` | 512 | Not the frozen common B=65536 |
| Steps | 20 | H: 20–100; I: 294 at D_3x |
| Ledger H | Must stay `not_started` | `pass` only after NVIDIA H acceptance |

## Expected methodological impact

None on the confirmatory comparison. The run cannot choose `D*`, cannot produce a confirmatory BPB, and cannot satisfy Gate H while `gpu_host_for_H_I` is null.

## Confirmatory eligibility retained?

**No** for this run. The parent A–G artifacts remain eligible. This Mac job is outside the confirmatory table.

## How the result will be labeled

`Mac MPS pre-H infrastructure validation` / `project1_m4_mps_preH`. Never “Gate H pass,” never a confirmatory depth result.

## Post-run checklist

- [x] MPS was used (not CPU): `COMPUTE_DTYPE: torch.float32 (auto-detected: no CUDA (CPU/MPS))`; `--device-type=mps`
- [x] Train loss finite: 10.399171 at step 0 → 10.388938 at step 19
- [x] Checkpoint written: `data/cache/p1-20260816T025911Z-0067a57/base_checkpoints/project1_m4_mps_preH/model_000020.pt`
- [x] Fresh-process reload produced finite validation BPB (engineering only): train 2.760515, val 3.294264 (matches final in-run val)
- [x] Active data path was the Tagalog shards, not ClimbMix; `~/.cache/nanochat` still absent
- [x] Ledger Gate H remains `not_started`
- [x] Test access log still empty

## Outcome

**Infrastructure validation succeeded.** Official Gate H is still waiting for a named NVIDIA CUDA host. The engineering val BPB values above are not confirmatory `val_bpb_full` and must not enter the main table.

Manifest: `manifests/mac_mps_preh.json`
