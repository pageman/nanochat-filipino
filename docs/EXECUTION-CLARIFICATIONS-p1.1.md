# Execution Clarifications for NANOCHAT-FILIPINO P1.1

**Study:** WikiText-TL-39 fixed-budget depth versus held-out Tagalog BPB  
**Registration:** AsPredicted #306780  
**Registration URL:** https://aspredicted.org/6r6v4v.pdf  
**Status:** Pre-Gate-A operational clarification note  
**Effective date:** 2026-08-16 (UTC+8), timestamped before Gate A starts  
**Scope:** Definitions and execution controls only; this note does not amend AsPredicted #306780.

> **Control statement.** AsPredicted #306780 is the governing confirmatory record. Its question, four-depth grid, fixed-budget target, corpus restriction, tokenizer rule, primary metric, exclusions, and one-test-touch rule remain unchanged. This document defines how named quantities and gates are operationalized before confirmatory BPB outcomes exist. It does not add a new hypothesis, model, corpus, metric, downstream task, or selection rule.

This file is the repository copy of the reviewer’s full execution note. It supersedes the short 2026-08-16 draft that previously occupied this path.

---

## 1. Purpose and authority

The confirmatory question is intentionally narrow: when depths 8, 12, 16, and 20 receive the same nominal model-visible token budget, `D_3x = 3 × T_train`, on one canonical WikiText-TL-39 package, does held-out Tagalog validation bits per byte decrease, flatten, or show a widening train–validation gap? AsPredicted #306780 names the data source, depth grid, corpus restriction, tokenizer size, sequence length, BPB outcome, baselines, exclusion rules, and test-touch constraint [1].

That registration is not a draft to be rewritten in response to engineering discoveries. The allowable pre-start work is narrower: define how `T_train`, `P`, the final evaluation checkpoint, the byte-unigram baseline, article reconstruction, and gate status will be implemented so that an independent reader can determine whether the study was executed as filed.

The following hierarchy applies.

| Level | Instrument | Role | May it alter the confirmatory design? |
| --- | --- | --- | --- |
| 1 | **AsPredicted #306780** | Governing scientific commitment | No. It is the lock. |
| 2 | **This execution clarification note** | Defines computations and operational controls already named by the registration | No. It may only resolve implementational ambiguity before relevant outcomes are observed. |
| 3 | **Gate ledger and run manifests** | Dated factual record of what was executed, observed, stopped, or blocked | No. They document implementation, not revised hypotheses. |
| 4 | **Run-card deviation** | Records an unavoidable departure from the registered design | No. It cannot retroactively make a departed run confirmatory; it classifies the impact. |
| 5 | **Exploratory supplement** | Separately labeled work such as d24, `D_10x`, clean data, CORE, or downstream tasks | No. It is reported outside the confirmatory main table. |

This ordering means that a useful engineering improvement is not automatically permitted in the main study. If it changes corpus content, split construction, tokenizer selection, model depth, sequence length, token budget, primary metric, test selection, or confirmatory comparison, it must be treated as a deviation or an exploratory follow-on rather than smuggled into the registered result.

---

## 2. Confirmatory design that remains fixed

The following table restates commitments from the registration for clarity. It does not add any new commitment.

| Element | Frozen confirmatory commitment |
| --- | --- |
| Corpus | `linkanjarad/Wikitext-TL39`, `data/train.parquet`, with no additional pretraining documents. |
| Model family | Pinned nanochat commit `92d63d4`, decoder-only base model, official `tok_train → base_train → base_eval` path plus the documented custom data-directory integration. |
| Canonical text | Source text with LF line-ending normalization only; no Moses detokenization in the canonical package. |
| Split | Original 2019 train/validation/test files if recovered and verified; otherwise deterministic hash 70/15/15 using reconstructed articles when the registered reconstruction procedure succeeds, and row-level fallback otherwise. |
| Tokenizer | One 32,768 BPE tokenizer trained on train text only. |
| Confirmatory depths | 8, 12, 16, and 20. |
| Sequence length | `T = 2048`. |
| Budget | `D_3x = 3 × T_train`; actual trained tokens are `num_iterations × total_batch_size`. |
| Primary outcome | `val_bpb_full` on the held-out validation split. |
| Secondary outcome | One `test_bpb` after validation-only selection of `D*`. |
| Main baselines | An untrained same-depth model and a train-fitted UTF-8 byte unigram. |
| Excluded from the main study | CORE, chat/SFT, classification, dengue, hate speech, OSCAR/TLUnified/ClimbMix mixing, clean or detokenized canonical data, GPT-2 tokenizer selection, d24, and `D_10x`. |

The purpose of this table is practical: any script, manifest, or later report should be checked against it before execution. It is not a substitute for the registration itself [1].

---

## 3. What this note may define—and what it may not decide

An execution clarification is permissible when it gives a deterministic implementation for language already present in the registration, is written before the affected confirmatory outcome exists, and does not create a new avenue to select a more favorable result. The five clarifications below meet that standard.

| Allowed clarification | Not allowed under the same label |
| --- | --- |
| Defining exactly how BPE tokens are counted for `T_train` | Choosing the token-counting method after seeing which budget gives the preferred depth result. |
| Defining how the registered final/selected checkpoint is operationalized | Selecting a different checkpoint for each depth after observing test BPB. |
| Defining a finite byte-unigram probability for unseen bytes | Replacing the required baseline with an advantaged learned model. |
| Defining a deterministic article parser and thresholded row fallback | Manually repairing articles or choosing row/article units after seeing BPB. |
| Recording pass/stop/blocked gate states and hashes | Overwriting a failed gate as if it passed, or omitting a failed attempt. |

If a choice falls into the right-hand column, it must not be presented as part of the locked confirmatory study. It can be explored later, with a dated run card and an explicit exploratory label.

---

## 4. Clarification 1 — Definitions of `T_train`, `P_total`, `P_scaling`, `D_3x`, and actual tokens

### 4.1 Definition of `T_train`

Let `τ` be the frozen 32,768-vocabulary nanochat BPE tokenizer trained only on the frozen train partition. Let `x_d` denote the canonical UTF-8 text of train document `d` after the registered LF line-ending normalization and any registered null/empty or overlength exclusion. Then:

```text
T_train = sum_{d in Train} |τ(x_d)|
```

Operationally, `T_train` is the sum of ordinary BPE tokens emitted from each train document using the saved tokenizer, **without manually prepending a BOS token**, **without sequence packing**, and **without loader-side cropping**. The tokenizer-training document cap of 10,000 characters belongs to the tokenizer-training stage; it does not redefine the full-document token count used for `T_train` unless the registration is explicitly amended, which it is not.

The calculation must be executed in a fresh script that accepts a frozen train manifest and frozen tokenizer directory, writes per-shard counts, and emits one aggregate number. It should fail if the manifest hash or tokenizer hash differs from the values recorded in the gate ledger.

### 4.2 Definitions of parameter counts

The run manifest must record both quantities reported by the pinned nanochat training code:

| Symbol | Definition | Reporting requirement |
| --- | --- | --- |
| `P_total` | Total trainable parameter count of the instantiated depth-specific model. | Report in the configuration and main result table. |
| `P_scaling` | The parameter count emitted or used by pinned `base_train.py` for its scaling calculation. | Report separately; it is the denominator used for the registered positive `--target-param-data-ratio`. |

The implementation must not assume that `P_total = P_scaling`. It must capture the exact value from the pinned source code or run log for each depth. The per-depth ratio is:

```text
R_d = D_3x / P_scaling,d
```

`R_d` must be positive for every confirmatory run. A value of `-1`, an auto-derived unrecorded fallback, or a ratio calculated against an unverified parameter count triggers the exclusion condition already registered in AsPredicted Q6 [1].

### 4.3 Fixed-budget implementation

The nominal registered budget is:

```text
D_3x = 3 × T_train
```

Each actual run consumes:

```text
D_actual,d = N_iterations,d × B_total,d
```

Before Gate I, choose and record one `total_batch_size` that is feasible at every confirmatory depth. When depth-specific VRAM constraints require smaller per-device micro-batches, preserve the chosen total batch size through gradient accumulation whenever the pinned code supports it. This is an execution-strengthening interpretation of the registered equal-exposure condition: it makes actual model-visible token counts identical across depths after the common ceiling operation.

If a single common total batch size is technically impossible, the run card must record the reason, the realized `D_actual,d`, and the absolute and relative distance from `D_3x`. The run is not silently discarded; its confirmatory eligibility must be classified before its result is interpreted. This does not change the registration—it makes any departure from “same model-visible token budget” visible.

### 4.4 Required budget-manifest fields

Write `manifests/budget_manifest.json` before confirmatory training begins. It must contain the following fields for all four depths, even if a later run is blocked. The `null` values mean the manifest is not complete and Gate G has not passed.

See the initialized stub at [../manifests/budget_manifest.json](../manifests/budget_manifest.json).

---

## 5. Clarification 2 — Final fixed-budget checkpoint and validation-only selection

### 5.1 The wording tension

AsPredicted Q3 states that test BPB is evaluated once after freezing the “best-val checkpoint,” while Q2, Q4, Q5, and the restatement frame the scientific comparison as equal-exposure training to a fixed budget `D_3x` [1]. If “best-val checkpoint” were interpreted as the minimum validation point among multiple intermediate checkpoints, each depth would obtain an unregistered opportunity for within-run checkpoint selection. That would weaken the clean fixed-budget comparison.

The pre-start operational reading adopted in this note is therefore:

> **Each confirmatory depth is scored using the final checkpoint produced after its fixed `D_3x` budget is exhausted. The four final `val_bpb_full` values are compared. `D*` is the exact lowest final validation BPB. The isolated test set is read once for that validation-selected final checkpoint.**

This reading is intentionally stricter than a flexible “minimum validation point” interpretation. It does not alter the registered question; it fixes the otherwise ambiguous checkpoint operationalization before confirmatory BPB outcomes exist.

### 5.2 How to reduce future ambiguity

For Gate I, use final-only checkpointing or an implementation configuration that clearly identifies the checkpoint at `D_actual,d`. Intermediate checkpoints may be saved for recovery and diagnostics, but they must not be used to select a different confirmatory model. The run card must record:

| Field | Required value |
| --- | --- |
| `selection_rule` | `exact_minimum_final_val_bpb_full` |
| `evaluation_checkpoint_rule` | `final_checkpoint_at_fixed_budget` |
| `test_selection_source` | `validation_only` |
| `test_read_count` | `0` before selection and `1` after selection |
| `checkpoint_step` | The final completed iteration corresponding to `D_actual,d` |

### 5.3 The `< 0.01 BPB` rule

The registration says to ignore gaps under 0.01 BPB with one seed [1]. The term “ignore” should govern **substantive interpretation**, not create a second unregistered model-selection rule. The execution rule is:

1. Calculate the exact final `val_bpb_full` for each depth.
2. Select `D*` as the depth with the exact numerical minimum.
3. If the selected depth’s margin from an adjacent or competing depth is less than 0.01 BPB, report the models as practically indistinguishable at the registered one-seed resolution.
4. Do not claim that the small numerical minimum demonstrates a meaningful depth advantage.
5. Do not use test BPB to break an apparent tie.

If a reviewer later reads “best-val checkpoint” as requiring a within-run minimum, the dated pre-Gate-A nature of this note is the defense: the stricter fixed-budget reading was selected before the relevant outcomes existed, recorded explicitly, and applied symmetrically to all four depths.

---

## 6. Clarification 3 — Baseline implementations and finite byte-unigram BPB

### 6.1 Random-initialization same-depth baseline

For each confirmatory depth, the random-initialization baseline must use:

- the same depth and architecture construction;
- the same frozen tokenizer;
- the same `T = 2048` sequence length;
- the same validation document package and packing/evaluation semantics;
- the same special-token exclusion rule; and
- a recorded initialization seed.

It is not trained. Its purpose is a sanity baseline: the trained model should improve on an architecture-identical model that has received no parameter updates. It should be evaluated on validation only and must not read the test split.

### 6.2 Byte-unigram baseline

The byte-unigram is fit using only bytes from the frozen canonical train split. Let `c[b]` be the count of UTF-8 byte value `b ∈ {0,…,255}` in that train byte stream, and let `N = Σ_b c[b]`. Use Laplace add-one smoothing:

```text
p(b) = (c[b] + 1) / (N + 256)
```

For a held-out byte stream `y_1, …, y_M`, compute:

```text
BPB_unigram = - (1 / (M * ln 2)) * sum_{i=1..M} ln p(y_i)
```

This definition guarantees finite values even when a byte is absent from the train corpus. It is a simple compression-style baseline, not a tokenizer baseline and not a learned language model. It must not be fitted on validation or test bytes.

### 6.3 Evaluation-component logging

For every trained and baseline validation/test evaluation, retain the components needed to reconstruct BPB.

| Artifact | Required components |
| --- | --- |
| Trained-model BPB | Total scored NLL, number of scored ordinary tokens, total denominator bytes, excluded special-token count, evaluator commit, sequence length, packing rule. |
| Random-init BPB | The same components plus initialization seed and model configuration hash. |
| Byte-unigram BPB | `c[0:256]`, total train bytes, smoothing constant, held-out total bytes, total negative log likelihood in nats, and final BPB. |

This logging introduces no additional metric. It makes the registered metric independently checkable.

---

## 7. Clarification 4 — Deterministic article reconstruction and row-level fallback

### 7.1 Purpose of reconstruction

The original work reports document-level statistics and derives its corpus from Tagalog Wikipedia material [2]. The current public Parquet representation may not expose the original train/validation/test files or original article boundaries. The registration already provides a recovery rule: use original files if they are found and match the paper; otherwise sort `sha256(utf-8 text)` and allocate 70/15/15, with reconstructed articles used when the audit supports them and rows otherwise [1].

This clarification removes human discretion from “if the audit supports them.”

### 7.2 Deterministic reconstruction procedure

The audit script uses only the canonical source text after LF line-ending normalization. It must:

1. Scan the source in its frozen row order without detokenizing or manually repairing text.
2. Apply one predeclared line-level heading regex: `(?m)^= [^=\n][^\n]*? =$`.
3. Treat each matched heading as the beginning of a candidate reconstructed article.
4. Concatenate the heading and following lines until the next matched heading.
5. Preserve source text exactly apart from LF normalization; no manual title repair, row reordering, or language-based deletion is allowed.
6. Create stable candidate IDs from `sha256(utf-8 canonical_article_text)`.

The exact code, Python version, regex string, input source hash, candidate count, candidate byte count, and rejected-fragment count must be written to the audit artifact.

### 7.3 Automatic fallback condition

Use reconstructed articles only if all of the following are true:

| Invariant | Required condition |
| --- | --- |
| Candidate count | At least 1,000 nonempty candidate articles. |
| Coverage | Every nonempty source row is assigned to exactly one candidate article or is represented in a documented, deterministic preamble bucket. |
| Nonempty condition | No candidate article becomes empty after LF normalization. |
| Hash condition | Candidate identities are stable SHA-256 hashes of their canonical UTF-8 text. |
| Audit completeness | Candidate count, coverage, and rejected-fragment statistics are present in the audit report. |

If any invariant fails, do not inspect examples and decide manually. Automatically use `reconstructed_row_70_15_15`: the split unit is the Parquet row’s canonical text, row identity is `sha256(utf-8 text)`, rows are sorted lexicographically by that hash, and the resulting ordered rows are split 70%/15%/15%.

### 7.4 Split integrity requirements

Regardless of the selected unit, the final split must satisfy:

- zero exact text-hash overlap among train, validation, and test;
- a recorded split-unit label, either `original_2019`, `reconstructed_article_70_15_15`, or `reconstructed_row_70_15_15`;
- a split manifest containing unit IDs, unit counts, character counts, byte counts, and aggregate hashes;
- a test manifest stored outside the active training directory;
- read-only protection or equivalent test-access protection before confirmatory training starts.

Near-duplicate measurements may be reported as audit context, but no unregistered near-duplicate removal occurs in the canonical package. Exact overlap, not near-duplicate similarity, is the registered hard split-validity condition.

---

## 8. Clarification 5 — Gate ledger, preflight controls, and stop behavior

### 8.1 Ledger purpose

The study already requires gates A–H before confirmatory Gate I. The gate ledger is not a new analysis. It is the dated administrative and technical record proving that each mandatory precondition either passed, stopped, or was blocked before production training began.

Initialize `manifests/gate_ledger.json` from `manifests/gate_ledger.template.json` before Gate A. Its initial status contains no model result, no validation BPB, and no test read. A gate transitions only from `not_started` to `pass`, `stop`, or `blocked`; it is never silently rewritten. If a correction is needed, append an event explaining the correction and preserve the prior record.

### 8.2 Status vocabulary

| Status | Meaning | Permitted next action |
| --- | --- | --- |
| `not_started` | Gate has not been attempted. | Start the declared work. |
| `pass` | All gate-specific acceptance conditions were met and artifacts are hashed. | Proceed only to the next ordered gate. |
| `stop` | A registered hard-stop condition was triggered. | Do not continue toward Gate I without a separately recorded decision about non-confirmatory handling. |
| `blocked` | Infrastructure or access issue prevented assessment, but no registered failure was observed. | Resolve the issue, document it, and re-run the gate from its declared start. |

### 8.3 Preflight script

Immediately before every smoke, pilot, or confirmatory training command, run a preflight program that exits nonzero if any condition fails:

1. The raw Parquet SHA-256 matches `source_manifest.json`.
2. The active data directory contains only registered train shards and one lexicographically final validation shard.
3. No test path, test manifest, test symlink, or test filename occurs inside the active training directory.
4. The active shard aggregate hashes match `shard_manifest.json`.
5. The tokenizer directory and `token_bytes.pt` hashes match `tokenizer_manifest.json`.
6. The run depth and `T=2048` match the frozen run manifest.
7. `target_param_data_ratio` is positive and equals the budget manifest value within declared machine precision.
8. `num_iterations × total_batch_size` equals the registered `D_actual` for that depth.
9. For Gate I, Gates A–H have status `pass`.

Preflight output must be archived beside the training log. A green console message is not sufficient; the JSON result and exit status are the artifact.

### 8.4 Hard-stop triggers

The following entries are registered hard stops or explicit invalidation conditions and must remain visible in the ledger:

| Trigger | Action |
| --- | --- |
| More than 5% of source units are dropped by the registered null/empty/overlength rule | Set Gate C to `stop`; do not replace the corpus or expand cleaning. |
| Any exact text hash appears in multiple splits | Set Gate D to `stop`; do not proceed to packaging. |
| Test file is located or read from the train directory | Set the affected gate or run to `stop`; do not classify the result as confirmatory. |
| Validation or test text is used to train the tokenizer | Set Gate F to `stop`; rebuild from a verified train-only tokenizer. |
| `target_param_data_ratio = -1` | Mark the run ineligible for the confirmatory table. |
| Silent change to depth or `T` after OOM | Mark the run ineligible for the confirmatory table. |
| NaN or Inf BPB | Mark the run ineligible and preserve the failure log. |

The correct response to a hard stop is not to improve the corpus with OSCAR, select a new metric, or quietly substitute another model. Those actions would initiate a different study.

### 8.5 Test-access log

The test evaluator must write a test-access record containing the timestamp, operator identity or automated job ID, exact test manifest hash, selected `D*`, validation selection evidence, model/checkpoint hash, and exit status. Before the final selected test evaluation, the test-access log must contain zero read events. After it, it should contain exactly one planned read event unless an explicitly labeled report-all-depth extension is later authorized and disclosed.

Path: [../manifests/test_access_log.json](../manifests/test_access_log.json).

---

## 9. Gate-by-gate operational reading

### Gate A — Environment

Pin nanochat at `92d63d4`, record the exact full commit SHA, install the declared environment, isolate `NANOCHAT_BASE_DIR`, and implement the smallest transparent `NANOCHAT_DATA_DIR` hook. The hook must preserve nanochat’s default behavior when the environment variable is absent. The resulting project patch is itself a versioned artifact. Do not run `python -m nanochat.dataset`, because the canonical study cannot ingest the default English ClimbMix data.

### Gate B — Download

Acquire the named public Parquet, validate its file type, inspect schema, verify the text column and row count, compute SHA-256, and write source provenance. A temporary inability to use a secondary mirror or loader does not alter or fail the specified primary source acquisition. The old S3 location is historical context, not an alternative source path.

### Gate C — Audit

Leave the raw file immutable. Count rows, null/empty entries, length distribution, Unicode features, `@-@` residue, and exact duplicates. Canonical text is source text with LF line endings only. A rule allowing drops for null/empty entries or entries over 200,000 characters does not authorize any further quality filtering. If the allowed-drop proportion exceeds 5%, stop as filed.

### Gate D — Split

Attempt original split recovery first. If it fails, choose the reconstruction unit only by the deterministic rule in Section 7 and generate a hash-based 70/15/15 split. The selected split type belongs in every title, manifest, table, and report caption.

### Gate E — Shards

Produce compatible Parquet shards with a `text` column, Zstandard compression, and row group 1024. Place at least one train shard before the lexicographically final validation shard. Keep test in an isolated directory. Fresh-process read tests and checksums are prerequisites, not a post hoc convenience.

### Gate F — Tokenizer

Train the registered 32,768 BPE only on the frozen train shards. Save `token_bytes.pt`, verify Tagalog Unicode round-tripping, and report bytes per token on train, validation, and test. GPT-2 comparison is descriptive only: it must not determine the tokenizer or primary model setup.

### Gate G — Budget

Calculate `T_train`, then `D_3x`, `P_total`, `P_scaling`, positive ratio, `total_batch_size`, `num_iterations`, and `D_actual` for all four registered depths. This gate establishes the run matrix but does not choose the depths. If a depth cannot be configured under the frozen `T=2048` and registered rule set, record `blocked` or `stop`; do not silently reduce the context length or substitute an unregistered depth.

### Gate H — Smoke

Run d4 for 20–100 steps with CORE disabled. Require finite loss, a saved checkpoint, a successful reload, and evidence that the active data path is not ClimbMix. This validates the pipeline only. It is not a pilot, does not modify the registered grid, and does not produce a confirmatory observation.

### Gate I and beyond

Only after A–H all pass does the study enter pilots and confirmatory training. d8/d12 `D_1x` pilots are secondary checks. The four d8/d12/d16/d20 `D_3x` final-checkpoint runs are confirmatory. Later clean-data, detokenization, vocabulary, d24, `D_10x`, CORE, or downstream results remain exploratory.

---

## 10. Run-card deviation policy

An unavoidable change is not necessarily useless, but it must never be hidden. Create a dated run card under `docs/run-cards/deviations/` before executing a changed run whenever the change affects a frozen element or a gate invariant.

| Situation | Classification | Required response |
| --- | --- | --- |
| GPU outage delays work, but all manifests and settings remain unchanged | Operational interruption | Record in ledger; resume through tested checkpoint logic. |
| Required package version is incompatible, but a pin-compatible environment can be created | Blocked Gate A | Document the issue and resolve without changing the confirmed code target. |
| Needed data directory hook is added with default behavior preserved | Permitted implementation adaptation | Record patch hash and tests. |
| VRAM requires a smaller micro-batch but the same total batch is preserved by accumulation | Permitted hardware adaptation | Record micro-batch and accumulation settings; preserve fixed `D_actual`. |
| VRAM requires a changed total batch, changes `D_actual`, or changes sequence length | Potential confirmatory deviation | Write run card first; do not call the run confirmatory unless its eligibility is independently justified from the frozen terms. |
| A second corpus, tokenizer selection, model depth, or task metric is added | Exploratory extension | Put it outside the confirmatory table. |
| Test BPB is observed before validation-only model selection | Test-touch violation | Mark affected selection process non-confirmatory. |

The deviation record should state the dated reason, the exact frozen statement affected, the change, why it was unavoidable, the expected methodological impact, whether confirmatory eligibility is retained, and how the result will be labeled. It should never revise the original registration PDF.

---

## 11. Minimal test suite before confirmatory GPU time

The following are engineering tests, not additional analyses. They should pass before Gate H or as part of its evidence.

| Test ID | Assertion |
| --- | --- |
| `test_source_hash` | Raw Parquet hash equals the source manifest. |
| `test_source_schema` | The expected text column exists and all required rows are string-compatible. |
| `test_split_disjointness` | Exact SHA-256 text-hash overlap across every pair of splits is zero. |
| `test_article_fallback` | The deterministic parser either satisfies every invariant or automatically selects the row-level fallback. |
| `test_active_directory` | The active directory contains only registered train shards and the final validation shard; no test file or symlink is present. |
| `test_tokenizer_train_only` | The tokenizer manifest can be traced solely to train shard hashes. |
| `test_t_train_count` | `T_train` is reproducible from the frozen tokenizer and train manifest without BOS, packing, or crop. |
| `test_ratio_positive` | Every registered depth has positive `R_d`. |
| `test_budget_math` | `D_actual = num_iterations × total_batch_size` and matches the frozen run manifest. |
| `test_checkpoint_reload` | d4 smoke checkpoint reloads in a fresh process and emits finite validation BPB. |
| `test_test_access_zero` | Test-access log is empty before validation-only `D*` selection. |

No test in this suite may read confirmatory test BPB. A test that reads the test text solely to calculate a pretraining-byte diagnostic should still be avoided before final evaluation; maintain the cleanest possible test protection boundary.

---

## 12. Reporting discipline after Gate I

The confirmatory main table should show one final validation BPB per registered depth, the corresponding actual token count, train–validation gap, random-init baseline comparison, byte-unigram comparison, and resource/configuration metadata. Test BPB should appear only for validation-selected `D*`, unless the report later adds test values for all four with an explicit statement that this did not influence selection. Do not present a marginal sub-0.01 BPB numerical lead as robust evidence of a meaningful depth ordering with one seed.

Run cards and the final report should separate four categories of statement:

1. **Verified execution fact:** for example, a source SHA, split type, exact depth, or recorded BPB component.
2. **Registered confirmatory result:** a final `val_bpb_full` comparison under the frozen run matrix.
3. **Secondary or exploratory result:** a pilot, native-ratio copy, clean-data ablation, alternate vocabulary, d24, `D_10x`, CORE, or downstream task.
4. **Limitation:** uncertainty about original split recovery, corpus size, data reuse, one-seed resolution, and the absence of chat/instruction training.

This separation is a scientific strength. It prevents the report from promising more than the small, controlled study can support.

---

## 13. Pre-Gate-A sign-off

Completed in the repository copy of this note on 2026-08-16 (UTC+8), before Gate A.

| Item | Required sign-off |
| --- | --- |
| Registration PDF saved and its SHA-256 recorded | `pending` — local PDF not yet in `docs/run-cards/`; record SHA-256 when the file is restored |
| This note dated before Gate A | `accepted` — 2026-08-16 (UTC+8) |
| Final-fixed-budget checkpoint interpretation accepted | `accepted` |
| `T_train` definition accepted | `accepted` |
| `P_scaling` capture method identified in pinned code/log | `pending` — identify at Gate A from commit `92d63d4` |
| Byte-unigram add-one smoothing accepted | `accepted` |
| Deterministic article parser and row fallback accepted | `accepted` |
| Gate ledger initialized with A–H as `not_started` | `accepted` — `manifests/gate_ledger.json` from template |
| No confirmatory validation or test BPB has been computed | `accepted` |

Once this sign-off is completed and timestamped, proceed to **Gate A** only. Do not begin the d8/d12/d16/d20 `D_3x` runs until the ledger shows A–H as `pass`.

---

## References

[1] AsPredicted #306780: NANOCHAT-FILIPINO P1.1 — WikiText-TL-39 fixed-budget depth vs held-out BPB. https://aspredicted.org/6r6v4v.pdf

[2] Cruz and Cheng, Evaluating Language Model Finetuning Techniques for Low-resource Languages. https://arxiv.org/html/1907.00409v1
