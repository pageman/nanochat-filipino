# Engineering record — DGX Spark Gate H smoke, H2 fail

- Date (UTC): 2026-08-16 / local 2026-08-17
- Host: `spark-a9f0`, aarch64, NVIDIA GB10 (Blackwell, compute capability 12.1)
- Operator on Spark: automated assistant under `HANDOFF-dgx-spark-gate-h-i.md`
- Classification: **engineering smoke fail**. Not official Gate H. Do not merge into Mac `manifests/gate_h.json` or `manifests/execution_host.json`.

P1.1 official H remains Runpod A40 `p7e5zk3njnglgy` (pass). Official I remains A40 `68bei7d3vx4krc`. `D*` and `test_bpb` are sealed.

## What ran

Literal handoff command: d4, `T=512`, `--device-batch-size=1`, `--total-batch-size=2048`, `--num-iterations=30`, no `--warmup-steps` (nanochat default **40**). After a compile/FA3 crash, the Spark run added:

- `TORCHDYNAMO_DISABLE=1`
- `patches/nanochat-sdpa-fallback-blackwell.patch` (not in the Mac repo; attention-path patch)

`setup_spark.sh` otherwise matched: pin `92d63d4`, `NANOCHAT_DATA_DIR` hook, `torch 2.9.1+cu128`, `cuda_available=True`. Frozen hashes matched. `test.jsonl` stayed 0444.

## Numbers (Spark)

| Step | Train loss | Val BPB (`eval-tokens=4096`) |
|---:|---:|---:|
| 0 untrained | 10.396767 | 3.150195 |
| 1 | 10.397074 | — |
| 20 | 10.273608 | 3.073723 (best) |
| 29 final | **10.538978** | **3.226611** |

H2 is `train loss at step 30 < step 1`. Final 10.539 > 10.397 → fail. Final val BPB worse than untrained.

## Contrast (official A40 H, same 30-step recipe)

| | A40 `p7e5zk3njnglgy` | Spark `spark-a9f0` |
|---|---|---|
| step 1 train | 10.397174 | 10.397074 |
| step 30 train | **10.084134** | **10.538978** |
| smoke val BPB | 2.914874 | 3.226611 |
| `torch.compile` | on (default) | off (`TORCHDYNAMO_DISABLE=1`) |
| attention | FA3 Ampere path or compiled SDPA | eager SDPA after SM121 crash |
| competing GPU users | none recorded | **ollama ~87 GB / 128 GB unified** |

Init matched. The endpoint did not. The Spark model **did** descend by step 20, then spiked.

## Causal chain (ordered)

1. **Handoff omitted `--warmup-steps`.** Gate G rule is `min(40, 5% of N)`. For N=30 that is **1**. Default 40 means the LR multiplier is `(step+1)/40` for the whole smoke (≈0.025→0.75). No plateau, no warmdown. This is a real config hole, but A40 used the same hole and still passed H2. Insufficient as a sole cause.
2. **Pin `92d63d4` FA3 detector treats CC 12.x as “try community FA3”.** Hopper is `major==9`. Else it loads `kernels-community/flash-attn3`. GB10 is 12.1. `torch.compile` then traces a kernel with no SM121 object; FakeTensor `data_ptr` crash. `TORCHDYNAMO_DISABLE=1` is a legitimate env lever. Forcing SDPA is a **code** change; the Spark offer classified that as `blocked` for official H.
3. **Default `--window-pattern=SSSL` + SDPA** uses an explicit sliding-window mask (nanochat warns utilization/correctness is the fallback path). Do not silently switch to `L` on a confirmatory card.
4. **ollama holding ~87 GB unified memory** during the smoke. d4 may still run; paging / kernel choice / late-run spikes are plausible. Not present on A40.
5. **PyTorch reports CC 12.1 > build max 12.0.** Preflight matmul was finite; this remains a host-class warning, not a crash.

H2 failed because of a **late spike (steps 20–29)** under climbing LR + eager SDPA + memory pressure, not because the stack never trained.

## What this does not authorize

- Overwriting official `gate_h.json` / naming Spark as `gpu_host_for_H_I` on the Mac lock
- Gate I `p1-fixed-d*-3x` on Spark
- A second P1.1 test read
- Treating Spark smoke BPB as `val_bpb_full`

## If Spark is still wanted (Paper 2 / curiosity only)

Kill `ollama` first. New `model-tag`, not `p1-smoke-d4`. Keep `TORCHDYNAMO_DISABLE=1` and a dated SDPA-force card. One isolation at a time:

| Tag | Change | Question |
|---|---|---|
| `p1-eng-spark-warmup1` | `--warmup-steps=1` only | Is the handoff hole enough? |
| `p1-eng-spark-warmup10` | `--warmup-steps=10` only | Spark agent’s proposed retry |
| `p1-eng-spark-no-ollama` | same 30/40 command, ollama gone | Was memory the spike? |

Stop if train loss still ends above step 1 **and** above untrained val BPB. Do not start EN0 on that host.
