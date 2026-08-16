# Assessment of `pageman/nanochat-filipino-p1-fixed-d20-3x`

**Repository reviewed:** <https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x>  
**Repository revision observed:** `ff4486a4d0dbdb3ee5c8c85b6798ab061db1693f`  
**Assessment date:** 2026-08-16 UTC+8  
**Status of this note:** Repository review only. It does not independently reproduce BPB, verify hidden files, or amend AsPredicted #306780.

## Bottom line

This is a **substantive and carefully scoped base-model release**, not an empty checkpoint dump. The model card identifies the corpus, tokenizer scope, pinned nanochat commit, depth, context length, actual token exposure, A40 environment, no-SFT status, expected loading mechanism, and SHA-256 values for all four final seed-0 checkpoints. The public file inventory is consistent with the stated architecture and final step: it contains d8, d12, d16, and d20 `model_000294.pt` plus matching metadata, with a public SHA-256 manifest. [1] [2]

The most important positive choice is conceptual: the repository says **“research base language model”** and explicitly rules out chat, instruction following, safety filtering, official government/medical use, English CORE comparison, and classification. That is the correct scope for the P1.1 artifact. It is not an assistant yet, and it should not be marketed as one.

However, the Hub release by itself is **not a complete preregistration close-out archive**. The model card reports `val_bpb_full=1.172248`, a one-time selected-model `test_bpb=1.164768`, and a d20–d8 gap of 0.0069 BPB. If accurate, that means the registered execution has moved beyond the earlier “evaluation pending” state and into close-out/reporting. But these values are currently **self-reported model-card claims**, not independently auditable results from the public repository, because the repository does not contain the full-validation result bundles, baseline outputs, selection record, test-access log, tokenizer byte map, split manifests, or evaluator scripts/configuration needed to replay the decision chain. [1] [2]

> **Interpretation:** The release makes the trained candidates available and hash-identifiable. It does not, on its own, establish the preregistered ranking or prove one-test-touch compliance. The close-out archive must provide that proof.

## What is publicly supported

| Claim | Public evidence | Assessment |
|---|---|---|
| Four seed-0 candidates were published | File inventory lists d8/d12/d16/d20 directories, each with `model_000294.pt` and `meta_000294.json`. [2] | **Supported.** |
| Candidate weights are hash-identifiable | `SHA256` names a SHA-256 for every published weight and metadata file. [2] | **Supported, subject to download/re-hash verification.** |
| Final step is 294 | Each inspected metadata file has `step: 294` and `num_iterations: 294`. [3] [4] [5] [6] | **Supported for checkpoint metadata.** |
| Common core training geometry | Inspected metadata specifies `T=2048`, `total_batch_size=65536`, CUDA, and depth-specific configs. [3] [4] [5] [6] | **Supported for published metadata.** |
| Equal actual exposure | Model card reports `D_actual=19,267,584`; metadata reports 294 iterations × 65,536 total batch. [1] [3] | **Arithmetic-consistent.** |
| The stored `val_bpb` in checkpoint metadata is the primary result | Metadata has `eval_tokens=262144`; e.g., d20 stored `val_bpb=1.117213...`. [3] | **Not supported.** These are short loop evaluations, not necessarily `val_bpb_full`. |
| Model-card full-validation/test values exist | Card reports `val_bpb_full=1.172248` and selected `test_bpb=1.164768`. [1] | **Self-reported only until result bundles/logs are archived.** |
| d20 was selected properly | Card labels d20 as `D*` and says selection was validation-only. [1] | **Not independently auditable from current files.** |
| No SFT occurred | Model card says “No SFT.” [1] | **Declared; consistent with the repository scope, but provenance evidence should be in the close-out archive.** |

## Important distinction: metadata `val_bpb` versus registered `val_bpb_full`

The exposed checkpoint metadata shows `eval_tokens=262144` for the training-loop metric. Its d20 `val_bpb` is `1.117213...`; d8 is `1.124544...`; d12 is `1.125139...`; d16 is `1.137399...`. The recorded loop minima tell a different story again: d12 has `1.084991...` and d16 `1.089718...`, while d20 has `1.110730...`. [3] [4] [5] [6]

None of those values should be used as the primary P1.1 result. AsPredicted requires full held-out `val_bpb_full`, not the `--eval-tokens` loop slice; it also requires validation-only selection and a single selected-model test evaluation. [7]

The model card appropriately reports different full-evaluation values, but it should **add a machine-readable public result table** that makes the distinction unmistakable. Otherwise, a reader may accidentally infer a ranking from the metadata loop metrics.

## What to add before calling the public record “P1.1 closed out”

| Missing or not visible in current Hub tree | Why it matters | Recommended artifact |
|---|---|---|
| Full validation result bundle for all four depths | Establishes the registered primary comparison. | `results/full_validation.json` containing NLL, ordinary-token count, byte count, special-token exclusion count, evaluator hash, checkpoint hash, and `val_bpb_full` for d8/d12/d16/d20. |
| Same-depth untrained validation baselines | Required by AsPredicted Q5. | `results/untrained_baselines.json` with architecture/config/seed and BPB values. |
| Train-fitted add-one UTF-8 byte-unigram baseline | Required by AsPredicted Q5. | `results/byte_unigram.json` with byte-count hash, `N`, smoothing definition, validation byte denominator, nats, and BPB. |
| Immutable validation-only selection record | Proves d20 was selected before test access. | `selection_record.json` plus SHA-256 and UTC timestamp. |
| Test access log | Proves one-test-touch chronology. | `test_access_log.json`, including explicit prior event count `0`, selected checkpoint hash, command hash, and event outcome. |
| Test evaluation component bundle | Supports the model card’s `test_bpb`. | `results/test_d20.json`; retain raw test text privately if redistribution is not permitted. |
| Tokenizer + `token_bytes.pt` hash and manifest | BPB/reloading depend on the same tokenizer byte mapping. | `tokenizer_manifest.json`; distribute files if permitted or provide retrievable immutable source. |
| Split, source, and shard manifests | Confirms reconstructed split and train-only tokenizer isolation. | `source_manifest.json`, `split_manifest.json`, `shard_manifest.json`, overlap audit. |
| Evaluator script/patch/environment identity | Allows independent replay and distinguishes full BPB from loop BPB. | nanochat patch, commit, lockfile/container hash, commands, host fingerprint. |
| Eligibility/deviation record | Makes W&B/restart, host transition, d20 microbatch configuration, and MPS dry-runs transparent. | `deviations_and_incidents/` index. |
| Release license/provenance file | Hub says `other`; underlying corpus and code obligations need precision. | `LICENSE-RESEARCH.md` and `DATA_AND_CODE_NOTICES.md`. |

## Recommended public-repository structure

Keep the current weight layout unchanged, and add only small text/JSON artifacts. Do not put test text, credentials, or passcodes in the repository.

```text
p1-fixed-d20-3x/
  README.md
  SHA256
  d8/ d12/ d16/ d20/                         # existing final candidates
  manifests/
    source_manifest.json
    split_manifest.json
    tokenizer_manifest.json
    budget_manifest.json
    final_checkpoint_manifest.json
  results/
    full_validation.json
    untrained_baselines.json
    byte_unigram.json
    selected_test_d20.json                   # aggregate components only; not raw test text
  protocol/
    execution_clarifications_p1_1.md
    selection_record.json
    test_access_log.json
    deviations_and_incidents.md
  reproducibility/
    nanochat_commit.txt
    data_directory_patch.diff
    environment_lock.txt
    evaluation_commands.md
  LICENSE-RESEARCH.md
  DATA_AND_CODE_NOTICES.md
```

## SFT: useful later, but a new study and a new artifact lineage

The current base checkpoint is the correct parent for an eventual SFT effort **only after its base-model identity is frozen**. Do not overwrite d20 or add SFT weights to `p1-fixed-d20-3x`; make SFT a new named descendant, for example:

```text
pageman/nanochat-filipino-p1-d20-sft-v1
  parent_base_repo: pageman/nanochat-filipino-p1-fixed-d20-3x
  parent_base_revision: ff4486a4d0dbdb3ee5c8c85b6798ab061db1693f
  parent_checkpoint_sha256: 9e30...dde38
  sft_protocol_sha256: ...
  sft_data_manifest_sha256: ...
```

An SFT protocol should predefine its data provenance/license, prompt template, train/validation/test partitions, exclusions, maximum sequence policy, optimizer/schedule, number of epochs/steps, checkpoint-selection rule, safety/quality review, and evaluation suite. Keep the **same tokenizer** unless a separate study justifies changing it. Evaluate SFT on held-out instruction behavior separately from base-model BPB; do not let instruction data or SFT outputs rewrite the P1.1 primary result.

## Catastrophic forgetting: SFT is optional and should not be conflated with it

P1.1 is a Tagalog-from-scratch base-model depth study. It **cannot directly demonstrate English catastrophic forgetting**, because it does not begin with a fixed English-capable base model and measure English before/after a Tagalog continuation intervention.

The clean direct-forgetting study should be separate:

| Arm | Parent | Continuation | Purpose |
|---|---|---|---|
| A | Frozen English base | No continuation | Detect evaluation drift. |
| B | Same English base | Matched English continuation | Measure generic continued-training/update drift. |
| C | Same English base | Frozen Tagalog continuation | Estimate target-language continuation effect on retained English. |
| D, optional | Same English base | Predeclared English–Tagalog rehearsal mixture | Test mitigation, not the primary contrast. |
| E, optional later | Same English base or frozen Tagalog base | Explicit SFT data | Study instruction-tuning interference as its own factor. |

The principal forgetting contrast is **C minus B** on an untouched English retention suite, accompanied by target-language adaptation measures. SFT is neither required nor desirable in the first clean causal comparison because it changes objective, data distribution, and behavioral target simultaneously. Add it only as a preregistered subsequent factor.

## Recommended sequence

1. **Close P1.1 first.** Attach/protect the evidence artifacts listed above, reconcile the model card with full-validation components, and preserve the one-test-touch chronology.
2. **Freeze the base release.** Tag the Hub commit, preserve checkpoint hashes, clarify `other` license/data notices, and add a citation/version instruction.
3. **Write a standalone SFT protocol.** New corpus, new objectives, new benchmark suite, new repository lineage; no change to P1.1 reporting.
4. **Design the direct forgetting study separately.** Use English-base controls, matched token budgets, frozen English and Tagalog evaluation, multiple seeds, and predeclared analysis.
5. **Only then connect results narratively.** The base P1.1 model is infrastructure/motivation for the later work, not direct evidence of forgetting.

## References

[1]: https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x "Model card for pageman/nanochat-filipino-p1-fixed-d20-3x"

[2]: https://huggingface.co/api/models/pageman/nanochat-filipino-p1-fixed-d20-3x "Hugging Face repository metadata and file inventory"

[3]: https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x/raw/main/d20/meta_000294.json "Published d20 final checkpoint metadata"

[4]: https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x/raw/main/d8/meta_000294.json "Published d8 final checkpoint metadata"

[5]: https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x/raw/main/d12/meta_000294.json "Published d12 final checkpoint metadata"

[6]: https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x/raw/main/d16/meta_000294.json "Published d16 final checkpoint metadata"

[7]: https://aspredicted.org/6r6v4v.pdf "AsPredicted #306780: NANOCHAT-FILIPINO P1.1"
