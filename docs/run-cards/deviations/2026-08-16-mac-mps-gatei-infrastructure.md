# Deviation / classification — Mac M4 MPS Gate I infrastructure preflight

- Date (UTC): 2026-08-16 (written before generating Gate I run cards and before any Mac d8–d20 command)
- Operator: Paul Pajo
- Parent RUN_ID: `p1-20260816T025911Z-0067a57`
- Label: `p1-m4-mps-gatei-preflight`
- `platform`: `macos-mps`
- `purpose`: `gate_i_infrastructure_preflight`
- `confirmatory_eligible`: **false**
- Protocol: P1.1 / AsPredicted #306780

## Frozen statement affected

`manifests/execution_host.json` still says official Gate H and confirmatory Gate I wait for a named NVIDIA CUDA host. `gpu_host_for_H_I` is null. Official Gate H remains `not_started`.

## Change

Use this Mac to build and exercise the **Gate I execution apparatus**:

1. Generate, from the frozen budget manifest, four immutable confirmatory run cards and command lines for d8/d12/d16/d20 at `D_3x`.
2. Recheck paths, hashes, test isolation, and preflight locks.
3. Instantiate each registered depth at `T=2048`.
4. If MPS memory allows, run a **one-step** engineering dry run per depth to test path resolution, checkpoint naming, save, and fresh-process reload.

This is **not** a host-policy amendment and **not** the registered equal-exposure series.

## Why this is being done

NVIDIA time should not be the first time the four-run protocol is assembled. A labeled Mac preflight can fail on tags, hashes, iteration math, checkpoint directories, or evaluator wiring before CUDA launch. It cannot certify CUDA/BF16/Flash Attention/VRAM fit.

## What is frozen and unchanged

- Corpus, split, tokenizer, `T_train`, `D_3x`, common `B=65536`, `N=294`, `D_actual=19267584`
- Confirmatory depths 8/12/16/20 and `T=2048`
- No `python -m nanochat.dataset`
- No `--target-param-data-ratio=-1`
- No FP8, no `torchrun`, no MPS-to-CPU fallback
- No tokenizer/split/shard rewrite
- Test split is not read
- Official Gate H stays `not_started`
- Confirmatory Gate I is not started

## Dry-run rules

| Rule | Value |
|---|---|
| Steps | 1 |
| `max-seq-len` | 2048 (do not shrink if a depth OOMs; record the OOM) |
| Mac `total-batch-size` | 2048 (one microbatch; **not** the frozen confirmatory B) |
| Confirmatory B | remains 65536 on the CUDA cards |
| CORE / sample / test | disabled |
| Validation | only if needed to prove the evaluator does not crash; record **finite/non-finite only** |
| Comparison | do not rank, graph, or select `D*` from Mac numbers |
| Checkpoint tags | `p1-m4-mps-gatei-preflight-d{8,12,16,20}` — distinct from confirmatory `p1-fixed-d{8,12,16,20}-3x` |

## Expected methodological impact

None on the confirmatory comparison. Mac dry-run tokens, losses, and any engineering BPB are outside the main table.

## Confirmatory eligibility retained?

**No** for these Mac executions. The parent A–G artifacts remain eligible. Official H and confirmatory I still require the named NVIDIA host.

## How the result will be labeled

`platform=macos-mps`, `purpose=gate_i_infrastructure_preflight`, `confirmatory_eligible=false`. Never “Gate I pass,” never a confirmatory depth result.

## Outcome (after execution)

| Check | Result |
|---|---|
| Four confirmatory run cards generated from budget | yes, still `prepared_not_executed` |
| `preflight.py --check-apparatus` | pass |
| `preflight.py --require-pre-i` | correctly **fails** (H `not_started`) |
| Instantiate d8/d12/d16/d20 at `T=2048` | all match Gate G `P_total` |
| One-step MPS dry run d8/d12/d16 | pass: finite train loss, checkpoint, finite dummy reload |
| One-step MPS dry run d20 | **MPS OOM** (~18 GiB). `T` was not shrunk. Not a confirmatory block. |
| Comparison / `D*` / test read | none |
| Official H / confirmatory I | still not started |

Manifest: `manifests/mac_mps_gatei_preflight.json`
