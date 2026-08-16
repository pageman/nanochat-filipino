# Response to the published d20 Hub assessment

**Assessment:** [published_d20_checkpoint_assessment.md](published_d20_checkpoint_assessment.md)  
**Hub reviewed:** https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x  
**This repository:** https://github.com/pageman/nanochat-filipino  
**This note does not amend AsPredicted #306780.**

The assessment is correct that the Hugging Face repo is a **hash-identifiable weight release**, not the preregistration close-out archive. This GitHub repository is that archive: protocol, manifests, evaluator, selection chronology, and machine-readable result bundles. Checkpoints stay on the Hub. Held-out `test.jsonl` and ResearchBox credentials are not published.

## Loop `val_bpb` is not `val_bpb_full`

| Source | Metric | d8 | d12 | d16 | d20 |
|---|---|---:|---:|---:|---:|
| Hub `meta_000294.json` / training-loop `--eval-tokens=262144` | diagnostic card eval | 1.124545 | 1.125139 | 1.137399 | 1.117213 |
| [results/full_validation.json](../../results/full_validation.json) | registered `val_bpb_full` | 1.179135 | 1.180824 | 1.195546 | **1.172248** |

`D* = 20` by exact minimum **final** `val_bpb_full`. Mid-run d12 min 1.084991 was not selected. Margin d20 vs d8 is 0.006887 BPB and is not a ranking.

## Recommended Hub tree → this repository

| Assessment path | GitHub path |
|---|---|
| `results/full_validation.json` | [results/full_validation.json](../../results/full_validation.json) |
| `results/untrained_baselines.json` | [results/untrained_baselines.json](../../results/untrained_baselines.json) |
| `results/byte_unigram.json` | [results/byte_unigram.json](../../results/byte_unigram.json) |
| `results/selected_test_d20.json` | [results/selected_test_d20.json](../../results/selected_test_d20.json) |
| `protocol/selection_record.json` | [manifests/selection_record.json](../../manifests/selection_record.json) |
| `protocol/test_access_log.json` | [manifests/test_access_log.json](../../manifests/test_access_log.json) |
| `protocol/execution_clarifications_p1_1.md` | [docs/EXECUTION-CLARIFICATIONS-p1.1.md](../EXECUTION-CLARIFICATIONS-p1.1.md) |
| `protocol/deviations_and_incidents.md` | [docs/run-cards/deviations/](deviations/) |
| `manifests/source_manifest.json` | [manifests/source_manifest.json](../../manifests/source_manifest.json) |
| `manifests/split_manifest.json` | [manifests/split_manifest.json](../../manifests/split_manifest.json) |
| `manifests/tokenizer_manifest.json` | [manifests/tokenizer_manifest.json](../../manifests/tokenizer_manifest.json) |
| `manifests/budget_manifest.json` | [manifests/budget_manifest.json](../../manifests/budget_manifest.json) |
| `manifests/final_checkpoint_manifest.json` | [manifests/final_checkpoint_manifest.json](../../manifests/final_checkpoint_manifest.json) |
| `reproducibility/nanochat_commit.txt` | [reproducibility/nanochat_commit.txt](../../reproducibility/nanochat_commit.txt) |
| `reproducibility/data_directory_patch.diff` | [reproducibility/data_directory_patch.diff](../../reproducibility/data_directory_patch.diff) and [patches/nanochat-NANOCHAT_DATA_DIR.patch](../../patches/nanochat-NANOCHAT_DATA_DIR.patch) |
| `reproducibility/environment_lock.txt` | [reproducibility/environment_lock.txt](../../reproducibility/environment_lock.txt) |
| `reproducibility/evaluation_commands.md` | [reproducibility/evaluation_commands.md](../../reproducibility/evaluation_commands.md) |
| `LICENSE-RESEARCH.md` | [LICENSE-RESEARCH.md](../../LICENSE-RESEARCH.md) |
| `DATA_AND_CODE_NOTICES.md` | [DATA_AND_CODE_NOTICES.md](../../DATA_AND_CODE_NOTICES.md) |
| Evaluator | [scripts/p1/gate_j_full_bpb.py](../../scripts/p1/gate_j_full_bpb.py) |

Weights remain at https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x (`d8/` `d12/` `d16/` `d20/` only). Do not add SFT weights to that repo. SFT and English catastrophic-forgetting studies are new registrations, as the assessment states.

## One-test-touch chronology (already sealed)

1. Validation bundle ended `2026-08-16T07:56:24Z` with `test_read_count=0` ([results/full_validation.json](../../results/full_validation.json)).
2. `D* = 20` from that file. The named [manifests/selection_record.json](../../manifests/selection_record.json) reconstructs that seal; it does not reopen `D*`.
3. One test read at `2026-08-16T07:58:35Z`, `test_bpb=1.164768` ([results/selected_test_d20.json](../../results/selected_test_d20.json), [manifests/test_access_log.json](../../manifests/test_access_log.json)).
