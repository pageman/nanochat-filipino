# Project 1: Pure Tagalog nanochat Base Model from WikiText-TL-39

## Super-exhaustive implementation blueprint

**Prepared for:** Project 1 implementation and research planning  
**Primary objective:** Train and evaluate a decoder-only Tagalog/Filipino base language model using the current Karpathy nanochat pipeline and the publicly available WikiText-TL-39 mirror.  
**Scope:** Unsupervised tokenizer training, causal pretraining, validation, held-out testing, diagnostics, and reproducible reporting. No instruction tuning, supervised fine-tuning, reinforcement learning, or chat-optimization stage is part of the core project.  
**Recommended repository baseline:** `karpathy/nanochat`, commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`, checked out on 2026-08-16.  

> **Central recommendation:** Treat Project 1 as a controlled corpus-and-pipeline reproduction experiment, not merely as “run nanochat on a downloaded file.” The academically defensible result requires a provenance manifest, an explicit reconstruction of train/validation/test handling, a documented minimal nanochat data-path adapter, tokenizer diagnostics, fixed-budget depth experiments, and a held-out Tagalog evaluation that does not depend on nanochat’s English-oriented CORE score.

---

## 1. Executive summary

The project should answer whether the current nanochat codebase can be used, with only a minimal and transparent data-path adaptation, to train a useful pure Tagalog decoder-only base model from WikiText-TL-39. The original WikiText-TL-39 work introduced a Filipino language-modeling corpus and reported a 70%/15%/15% train/validation/test split, with approximately 39.27 million training tokens in the original corpus statistics [9]. The currently accessible Hugging Face mirror exposes a single Parquet training file and reports approximately 1.52 million rows [8]. Because the current mirror does not visibly expose the original three split files, the first research gate must determine whether the mirror is an exact reserialization of the original corpus, a merged representation, or a modified/partial representation. If the original split boundaries cannot be recovered, the project must create a deterministic reconstructed split and label it as such rather than claiming an exact replication of the original paper.

The modern nanochat repository is intentionally minimal. It expects a local collection of Parquet shards whose rows contain a single `text` column. The current `nanochat/dataset.py` is configured for the repository’s ClimbMix dataset, so Project 1 must either add a small environment-variable data-directory hook or use an isolated cache directory containing a deliberately documented compatibility layout. The recommended implementation is the environment-variable hook because it preserves the default behavior while making the Tagalog data source explicit and auditable.

The first successful milestone is not a large model. It is a complete, verified, end-to-end d4 or d8 run that proves the following chain: source acquisition → source audit → deterministic split → Parquet repackaging → tokenizer training → tokenizer round-trip testing → data-loader smoke test → short causal-pretraining run → checkpoint save → checkpoint reload → validation bits-per-byte evaluation. Only after that gate passes should the project run the depth series.

The recommended primary depth series is `d8`, `d12`, `d16`, and `d20`, with `d4` used as a smoke-test model and `d24` treated as optional. The original nanochat scripts commonly use the single `--depth` dial to derive model width, attention heads, training horizon, learning-rate adjustments, and other quantities [1] [2] [3]. However, WikiText-TL-39 is a small corpus by modern language-model standards. Therefore, blindly using the default data-to-parameter horizon for every depth may cause many passes over the same data and severe overfitting. The plan uses two complementary modes: a native nanochat depth-dial run for compatibility, and a fixed-data-budget comparison in which each depth sees the same number of model tokens.

The primary metric should be **Tagalog held-out bits per byte**, computed on a never-trained validation/test split with the same tokenizer and model sequence length. Raw training loss, validation loss, tokenization efficiency, bytes per token, throughput, memory, and train–validation gap should be reported as secondary diagnostics. The built-in nanochat CORE score should not be treated as a primary result because the current CORE bundle is designed around English-oriented in-context tasks and is not a valid direct measure of a Tagalog-only base model.

---

## 2. Research objective, questions, hypotheses, and boundaries

### 2.1 Main research objective

The main objective is:

> **To construct a reproducible pure Tagalog nanochat base model from WikiText-TL-39, quantify the effect of nanochat depth under a low-resource corpus constraint, and establish a rigorously evaluated baseline for subsequent Tagalog downstream experiments.**

The phrase **pure Tagalog base model** means that the pretraining corpus is restricted to the selected WikiText-TL-39 release and its explicitly documented preprocessing, with no English web corpus, ClimbMix, FineWeb, OSCAR, CulturaX, synthetic instruction data, or supervised task data mixed into the training shards. Incidental English words, names, technical terms, and multilingual material already present inside the source corpus are not silently removed unless a separate ablation explicitly defines a language-filtered variant.

### 2.2 Research questions

| ID | Research question | Required evidence |
|---|---|---|
| RQ1 | Can the current nanochat tokenizer–pretrain–evaluate pipeline run on WikiText-TL-39 with no architectural modification and only a minimal explicit data-path adaptation? | Passing smoke test, successful tokenizer artifact, successful checkpoint, successful validation BPB, clean repository diff |
| RQ2 | How does transformer depth affect Tagalog held-out BPB, training efficiency, overfitting, and sample quality when the same corpus is used? | Depth-series table with fixed preprocessing, tokenizer, sequence length, data budget, and evaluation split |
| RQ3 | Does the nanochat BPE tokenizer provide efficient segmentation for Tagalog relative to general-purpose tokenizers? | Bytes/token, characters/token, token count, compression ratio, and diagnostic examples |
| RQ4 | Does the nanochat default compute-optimal data-to-parameter horizon remain sensible for this small corpus? | Comparison of native ratio runs with fixed-data-budget runs and train–validation curves |
| RQ5 | Does the project produce a scientifically useful base model, rather than merely a technically completed run? | Held-out test BPB, contamination analysis, sample audit, checkpoint reload, and optional downstream probe plan |

### 2.3 Hypotheses

| ID | Hypothesis | Falsification condition |
|---|---|---|
| H1 | The current nanochat pipeline can support WikiText-TL-39 after a small, isolated data-directory change. | More than a trivial adapter is required, or the current loader cannot consume the packaged corpus without architectural changes. |
| H2 | A 32,768-vocabulary byte-level BPE tokenizer trained on the Tagalog corpus will reduce bytes per token relative to a general English tokenizer on Tagalog text. | The Tagalog tokenizer has equal or worse compression on the held-out corpus after controlling for vocabulary size and evaluation text. |
| H3 | Increasing depth will improve held-out BPB up to a point, after which the small corpus will yield diminishing returns or a widening train–validation gap. | Larger depths continue improving held-out BPB without increased variance or overfitting under the same data budget. |
| H4 | The default nanochat target parameter-to-data ratio will induce substantial data reuse for WikiText-TL-39. | The measured number of corpus passes remains low and train–validation curves show no data-reuse concerns. |
| H5 | A fixed held-out Tagalog BPB is more informative for this project than the built-in English CORE score. | A validated Tagalog-specific task suite demonstrates that English CORE tracks the relevant behavior; this is not expected and would require separate justification. |

### 2.4 Out of scope for the core project

The following are explicitly excluded from the main result: instruction tuning; supervised classification heads; chat SFT; reinforcement learning; synthetic instruction generation; translation training; multilingual mixing; claims of broad Filipino conversational ability; claims of state-of-the-art performance; claims of legal clearance without an independent license review; and claims that the current Hugging Face Parquet mirror is byte-for-byte identical to the original 2019 release unless that is demonstrated.

These can be follow-on projects. In particular, dengue classification, hate-speech classification, and NewsPH-NLI evaluation should be treated as downstream validation projects after the base model is complete, not folded into the definition of the pure pretraining experiment.

---

## 3. Acceptance criteria and non-negotiable gates

The project is complete only when all of the following conditions are satisfied.

| Gate | Acceptance condition | Evidence to archive |
|---|---|---|
| G0: Scope | The exact corpus variant, split rule, tokenizer settings, depth grid, data budget, and primary metrics are written down before production training. | `configs/project1.yaml`, dated preregistration or experiment note |
| G1: Source | The dataset is downloaded from the current public mirror, its SHA-256 hash is recorded, its schema is inspected, and its provenance is documented. | Raw-file checksum, source URL, retrieval timestamp, dataset-card snapshot, manifest |
| G2: Corpus audit | Null rows, empty rows, Unicode anomalies, duplicates, extreme lengths, suspicious markup, and language/script statistics are measured. | `corpus_audit.json`, audit CSV, diagnostic plots |
| G3: Split | Train, validation, and test are document-disjoint, deterministic, and documented. If reconstructed, they are explicitly labeled reconstructed rather than original. | Split manifest, row counts, hashes, leakage report |
| G4: Packaging | Nanochat-compatible Parquet shards contain one non-null `text` column, use the documented compression/row-group format, and place validation as the final Parquet file in the active data directory. | Shard manifest, Parquet metadata, checksums |
| G5: Tokenizer | A 32,768-vocabulary tokenizer is trained, saved, loaded, and round-trip tested on Tagalog Unicode and punctuation cases. | Tokenizer directory, `token_bytes.pt`, test logs, tokenizer statistics |
| G6: Smoke training | A tiny run completes without NaNs, shape errors, data-loader errors, or checkpoint failures. | Smoke log, checkpoint, reload log |
| G7: Pilot | At least one d8 or d12 pilot produces a decreasing training loss, a finite validation BPB, and a reloadable checkpoint. | Pilot log, W&B or local metrics, checkpoint metadata |
| G8: Production | Every preregistered depth completes or is explicitly marked failed with a diagnosed cause. | Per-depth log, metadata, checkpoint, resource record |
| G9: Evaluation | Primary validation and test BPB are computed on data not used for parameter updates, using a fixed tokenizer and evaluation protocol. | Evaluation JSON/CSV, per-example or per-batch measurements |
| G10: Reproducibility | Another operator can reproduce the data package, tokenizer, smoke run, and at least one production run from the archived instructions. | README, lockfile hash, scripts, manifests, commit IDs |
| G11: Reporting | The final report distinguishes verified measurements, assumptions, reconstructed choices, and limitations. | Final report and artifact index |

A run that produces a checkpoint but fails G9 is a **technical prototype**, not a completed scientific result. A run that produces a good validation score but lacks a source hash and split manifest is **not reproducible enough for publication**.

---

## 4. Evidence base and exact nanochat interfaces

### 4.1 Current nanochat workflow

The current nanochat README describes a minimal full-stack language-model harness containing tokenization, pretraining, fine-tuning, evaluation, and inference [1]. Its research documentation identifies `runs/miniseries.sh` and `runs/scaling_laws.sh` as the main experiment scripts [1] [3]. The `--depth` argument is intended to be the main complexity dial; the code derives model dimensions and several optimization quantities from it [1] [7].

The relevant current interfaces are:

| Component | Current file | Project 1 implication |
|---|---|---|
| Data location and download utility | `nanochat/dataset.py` | Current constants point to ClimbMix; do not call its default downloader for WikiText-TL-39. |
| Data iteration | `nanochat/dataset.py` and `nanochat/dataloader.py` | The runtime expects Parquet files with a `text` column and treats the last Parquet as validation. |
| Tokenizer training | `scripts/tok_train.py` | Reads the active training Parquet files, crops documents to 10,000 characters for tokenizer training, defaults to 2B characters and vocabulary size 32,768, and saves the tokenizer under the nanochat base directory. |
| Tokenizer evaluation | `scripts/tok_eval.py` | Can compare compression behavior on canned text and active train/validation data; supplement it with Tagalog-specific probes. |
| Base pretraining | `scripts/base_train.py` | Uses the active tokenizer, active Parquet directory, explicit depth, explicit or automatically derived horizon, and optional validation BPB/CORE/sample/checkpoint cadence. |
| Base evaluation | `scripts/base_eval.py` | Supports BPB and samples, but its built-in train/validation split model has no native third test split. |
| Data repackaging reference | `dev/repackage_data_reference.py` | Defines the recommended Parquet shape, shuffle policy, row-group size, compression, and shard naming. |
| Checkpoint handling | `nanochat/checkpoint_manager.py` | Save model, optimizer, configuration, and data-loader state; test reload before production. |

### 4.2 Critical data-loader behavior

The current loader uses a BOS-aligned best-fit packing algorithm [6]. It inserts a BOS token at the start of every document, packs documents into rows of capacity `T+1`, and uses a buffer to select documents that fit. It reports 100% sequence utilization but documents approximately 35% token cropping at `T=2048` [6]. This behavior has four consequences that must appear in the methods section.

First, a Parquet row is a document candidate, not necessarily a model sequence. Multiple documents may be packed into one training sequence. Second, the model sees a BOS boundary before every document, which is useful for document-level separation. Third, source tokens may be discarded when a document is cropped to fill the remaining sequence capacity. Fourth, the number of source-corpus tokens and the number of model-visible training tokens are not identical. The project must report both where possible.

### 4.3 Critical training-horizon behavior

The current `base_train.py` calculates `target_tokens` as:

\[
D_{\text{target}} = r_{\text{param-data}} \times P_{\text{scaling}},
\]

where `r_param-data` is `--target-param-data-ratio` and `P_scaling` is the selected scaling-parameter count [7]. It then calculates a batch size and training iterations. If `--num-iterations` is supplied, that value takes precedence for the number of optimization steps, but `target_tokens` is still used in the batch-size and weight-decay calculations unless a total batch size is explicitly provided. Therefore, do not set `--target-param-data-ratio=-1` casually: the current implementation still uses that value in the scaling calculations and can produce nonsensical negative or invalid derived quantities.

For a fixed-data-budget experiment, the safe procedure is to retain a **positive** target parameter-to-data ratio that corresponds to the intended budget, explicitly set `--num-iterations`, explicitly set `--total-batch-size`, and record the resulting actual token budget. Alternatively, implement and test a small, explicit code change that separates “optimizer-scaling reference tokens” from “actual training horizon.” Do not silently alter this behavior in a production run.

### 4.4 CORE metric limitation

The current base evaluation implementation downloads an evaluation bundle and evaluates an English-oriented CORE task suite [5]. This is useful for the default English nanochat benchmark, but it is not a valid primary metric for a pure Tagalog language model. A Tagalog model may receive a low CORE score simply because the tasks and prompts are not linguistically matched. For Project 1, disable CORE during the main run or record it only as a clearly labeled auxiliary diagnostic. The main evaluation must be Tagalog held-out BPB plus corpus and tokenizer diagnostics.

---

## 5. Recommended project repository and artifact layout

Create a separate project directory rather than editing the nanochat checkout in place without a record.

```text
project1-wikitext-tl39/
├── README.md
├── LICENSE_NOTES.md
├── pyproject-or-environment-notes.md
├── configs/
│   ├── project1.yaml
│   ├── smoke_d4.yaml
│   ├── pilot_d8.yaml
│   ├── pilot_d12.yaml
│   ├── fixed_budget_miniseries.yaml
│   └── native_nanochat_miniseries.yaml
├── data/
│   ├── raw/
│   │   └── Wikitext-TL39_train.parquet
│   ├── canonical/
│   │   ├── train/
│   │   ├── validation/
│   │   └── test/
│   ├── clean_ablation/
│   │   ├── train/
│   │   ├── validation/
│   │   └── test/
│   └── manifests/
│       ├── source_manifest.json
│       ├── split_manifest.json
│       ├── canonical_shards.json
│       └── clean_ablation_shards.json
├── scripts/
│   ├── download_wikitext_tl39.sh
│   ├── audit_wikitext_tl39.py
│   ├── split_wikitext_tl39.py
│   ├── package_wikitext_tl39.py
│   ├── evaluate_wikitext_tl39.py
│   ├── compare_tokenizers.py
│   ├── summarize_runs.py
│   └── make_report_tables.py
├── reports/
│   ├── corpus_audit.md
│   ├── tokenizer_report.md
│   ├── run_cards/
│   └── final_project1_report.md
├── results/
│   ├── smoke/
│   ├── pilot/
│   ├── miniseries/
│   └── figures/
└── manifests/
    ├── nanochat_commit.txt
    ├── uv_lock_sha256.txt
    ├── hardware.json
    └── run_index.csv
```

Keep the nanochat source checkout separately:

```text
/home/ubuntu/research/nanochat/
```

The project repository should contain either a small tracked patch to nanochat or a script that applies the patch and verifies it. The raw dataset should not be committed to Git. Store hashes and download instructions instead.

---

## 6. Phase 0 — Freeze the research protocol before training

### Step 0.1: Write the project charter

Create `configs/project1.yaml` containing at least:

```yaml
project: project1_wikitext_tl39
language_label: Tagalog/Filipino
source_dataset: Wikitext-TL39
source_url: https://huggingface.co/datasets/linkanjarad/Wikitext-TL39
source_file: data/train.parquet
nanochat_repo: https://github.com/karpathy/nanochat
nanochat_commit: 92d63d4e8bb4df75c3b71618f31ddde2378b2bcd
sequence_length: 2048
tokenizer_vocab_size: 32768
tokenizer_doc_cap_chars: 10000
tokenizer_max_chars: 2000000000
split_policy: deterministic_reconstructed_70_15_15_if_original_unavailable
split_seed: 42
canonical_normalization: source_text_plus_line_ending_normalization
clean_ablation: false
primary_metric: heldout_tagalog_bits_per_byte
secondary_metrics:
  - validation_loss
  - training_loss
  - bytes_per_token
  - tokens_per_byte
  - train_validation_gap
  - throughput_tokens_per_second
  - mfu
  - peak_memory
  - checkpoint_reload_success
depths:
  smoke: [4]
  pilot: [8, 12]
  production: [8, 12, 16, 20]
  optional: [24]
```

Do not change the source, split rule, vocabulary size, or primary metric after inspecting production results unless the change is explicitly recorded as a new experiment. If a design change is necessary, create a versioned configuration such as `project1_v2.yaml`.

### Step 0.2: Define the canonical and ablation data variants

The **canonical variant** should be as conservative as possible. Read the source `text` field, preserve casing and punctuation, normalize only line endings and the minimum required representation details, and remove only null or truly empty rows. Do not detokenize punctuation, remove English words, lowercase, aggressively normalize whitespace, or run a language classifier in the canonical run.

The **clean ablation** may apply Unicode NFC normalization, HTML entity handling if needed, whitespace normalization, exact deduplication, and optional near-duplicate filtering. It must be packaged separately and must never overwrite the canonical data. The canonical result answers “what happens when the current nanochat pipeline is applied to the public WikiText-TL-39 representation?” The clean ablation answers a different question: “what happens when additional modern corpus cleaning is applied?”

### Step 0.3: Define the primary comparison design

Use two experiment families.

| Family | Purpose | Horizon | Interpretation |
|---|---|---|---|
| Native-depth family | Follow nanochat’s intended single-depth control logic as closely as possible. | Positive `--target-param-data-ratio`, usually the current default unless pre-registered otherwise. | Measures behavior under nanochat’s own scaling assumptions, but may reuse the small corpus heavily. |
| Fixed-data family | Compare depths under the same number of model-visible training tokens. | Explicit `D_budget` and `--num-iterations`; optimizer scaling tied to the selected budget. | Best for isolating the effect of depth under low-resource data. |

The fixed-data family should be the primary scientific comparison. The native-depth family is a compatibility and reproducibility result.

### Step 0.4: Set the stopping and failure rules

Predefine that a run is invalid or requires rerun if any of the following occurs: NaN or Inf loss; non-finite BPB; corrupted or incomplete checkpoint; tokenizer round-trip failure; validation data accidentally included in train; train/validation/test overlap above the declared threshold; a changed data manifest without a new run ID; an OOM resolved by changing a model or sequence-length parameter without recording the change; or a run that cannot be reloaded from its final checkpoint.

Do not stop a run merely because a validation metric is temporarily worse. Stop only for a predeclared numerical, infrastructure, data-integrity, or safety failure, unless the run is a pilot explicitly designed to be exploratory.

---

## 7. Phase 1 — Create and freeze the software environment

### Step 1.1: Clone and record nanochat

Run from the project machine:

```bash
mkdir -p /home/ubuntu/research
cd /home/ubuntu/research
gh repo clone karpathy/nanochat nanochat
cd nanochat
git rev-parse HEAD
git log -1 --format='%H%n%ad%n%s' --date=iso
```

If the repository has already been cloned, do not silently use a newer commit. Record the existing commit and decide whether to update. The plan’s baseline commit is `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; if the actual experiment uses another commit, place that exact commit in every run manifest.

### Step 1.2: Install dependencies with uv

For CUDA:

```bash
cd /home/ubuntu/research/nanochat
uv sync --extra gpu --group dev
source .venv/bin/activate
```

For CPU-only or MPS experimentation:

```bash
uv sync --extra cpu --group dev
source .venv/bin/activate
```

The current project configuration depends on PyTorch 2.9.1, PyArrow, RustBPE, tiktoken, W&B, and related utilities [10]. The `datasets` package is not required by nanochat’s normal runtime and is not present as a core dependency in the current project configuration. Prefer downloading the public Parquet file directly with `curl` or `wget` and reading it through PyArrow. Install `datasets` only if a separate audit script specifically requires it, and record that extra dependency.

### Step 1.3: Record environment metadata

Archive the following before training:

```bash
python --version
uv --version
python -c 'import torch, pyarrow, rustbpe; print(torch.__version__); print(torch.version.cuda); print(pyarrow.__version__)'
nvidia-smi || true
git rev-parse HEAD
sha256sum uv.lock
```

Write the output to `manifests/environment.txt`. Also record GPU model, GPU count, VRAM per GPU, driver version, CUDA runtime, CPU model, RAM, storage volume, operating system, and whether the run is on a preemptible/spot instance.

### Step 1.4: Establish a separate cache directory

Use an isolated base directory for the project rather than mixing artifacts with a default English nanochat run:

```bash
export PROJECT_ROOT=/home/ubuntu/project1-wikitext-tl39
export NANOCHAT_BASE_DIR=$PROJECT_ROOT/runtime/nanochat_cache
mkdir -p "$NANOCHAT_BASE_DIR"
```

The cache will contain the tokenizer, token-byte mapping, base checkpoints, evaluation outputs, and any downloaded nanochat bundles. Keep the Parquet corpus outside the cache if storage management requires it, but ensure that the runtime data directory is explicit and versioned.

---

## 8. Phase 2 — Acquire and verify WikiText-TL-39

### Step 2.1: Use the current public Hugging Face file

The current practical source is the Hugging Face dataset repository [8]. The repository metadata lists `data/train.parquet`; the direct resolved file URL is:

```text
https://huggingface.co/datasets/linkanjarad/Wikitext-TL39/resolve/main/data/train.parquet
```

The older S3 ZIP URL retained in the historical Filipino-Text-Benchmarks README currently returns HTTP 404 and must not be used as the primary acquisition path. The historical repository remains useful as provenance context [11].

Download to a temporary file, verify that it is not an HTML error page, and compute a checksum:

```bash
mkdir -p "$PROJECT_ROOT/data/raw" "$PROJECT_ROOT/data/download_tmp"
cd "$PROJECT_ROOT/data/download_tmp"
curl -L --fail --retry 5 --retry-delay 3 \
  -o Wikitext-TL39_train.parquet \
  'https://huggingface.co/datasets/linkanjarad/Wikitext-TL39/resolve/main/data/train.parquet'
file Wikitext-TL39_train.parquet
sha256sum Wikitext-TL39_train.parquet | tee "$PROJECT_ROOT/data/manifests/source_sha256.txt"
mv Wikitext-TL39_train.parquet "$PROJECT_ROOT/data/raw/"
```

The `file` command should identify a Parquet-compatible binary rather than HTML, XML, or plain text. If the download is redirected to an access page, stop and record the issue rather than proceeding with an unverified file.

### Step 2.2: Record the source manifest

Create `data/manifests/source_manifest.json` with fields similar to:

```json
{
  "dataset_name": "WikiText-TL-39",
  "source_repository": "linkanjarad/Wikitext-TL39",
  "source_url": "https://huggingface.co/datasets/linkanjarad/Wikitext-TL39",
  "source_file_url": "https://huggingface.co/datasets/linkanjarad/Wikitext-TL39/resolve/main/data/train.parquet",
  "retrieval_time_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "sha256": "REPLACE_WITH_ACTUAL_HASH",
  "nanochat_commit": "REPLACE_WITH_ACTUAL_COMMIT",
  "raw_filename": "Wikitext-TL39_train.parquet",
  "source_representation": "Hugging Face Parquet mirror",
  "legacy_s3_status": "HTTP 404 on verification date",
  "license_status": "verify current source terms independently"
}
```

Do not claim that the Hugging Face mirror is identical to the original corpus until the row content, ordering, split structure, and statistics have been compared. The current card shows one train split, whereas the original paper reports separate training, validation, and testing statistics [8] [9].

### Step 2.3: Inspect the Parquet schema and metadata

Before transforming the source, inspect:

```python
import pyarrow.parquet as pq

path = "data/raw/Wikitext-TL39_train.parquet"
pf = pq.ParquetFile(path)
print(pf.schema)
print("row_groups:", pf.num_row_groups)
print("metadata:", pf.metadata)
```

The expected primary field is a `text` string column. Measure the following before normalization:

| Measurement | Why it matters |
|---|---|
| Row count | Detects whether the mirror matches the dataset card and future runs. |
| Number of row groups | Determines efficient scanning and repackaging. |
| Null count | Null text cannot be passed to the tokenizer. |
| Empty/whitespace-only count | These rows waste shard capacity and can distort statistics. |
| Minimum, median, p95, p99, maximum character length | Determines document-cap effects and long-document handling. |
| Total Unicode code points | Useful source-size baseline. |
| Total UTF-8 bytes | Needed for source compression and BPB calculations. |
| Exact duplicate count | Indicates whether deduplication is already present. |
| Script distribution | Detects unexpected non-Tagalog or malformed rows without silently deleting them. |
| HTML/entity frequency | Determines whether source normalization is already applied. |
| Sentence/punctuation spacing patterns | Helps distinguish the original Moses-tokenized representation from raw prose. |

Save these measurements in `reports/corpus_audit.md` and `data/manifests/source_statistics.json`.

### Step 2.4: Verify the original-paper statistics without assuming exact replication

The original paper reports 120,975 training documents, 25,919 validation documents, and 25,921 testing documents; 39,267,089 training tokens; 8,356,898 validation tokens; and 8,333,288 testing tokens [9]. Use those figures as historical reference points, not as expected values for the current mirror. Compute the same statistics on the downloaded Parquet only after defining what counts as a token. The current nanochat BPE token count is not comparable to the paper’s original Moses/word-vocabulary token count.

Report at least three token notions separately:

1. **Source-paper token count:** only if the original tokenization procedure can be reconstructed exactly.
2. **Whitespace or Moses-like token count:** useful for historical comparison, but must be labeled as an approximation if the exact tokenizer is unavailable.
3. **Nanochat BPE token count:** the actual model token count produced by the trained tokenizer.

Never place these quantities in one column labeled simply “tokens.”

---

## 9. Phase 3 — Audit, normalize, and define the corpus variant

### Step 3.1: Preserve an immutable source layer

Never modify `data/raw/Wikitext-TL39_train.parquet`. All transformations must write to a new directory. The raw file, checksum, source URL, retrieval timestamp, and source metadata form the immutable provenance layer.

### Step 3.2: Define canonical normalization

The canonical normalization function should be deliberately conservative:

```text
Input: source text string
1. Reject null values.
2. Convert CRLF and CR line endings to LF.
3. Normalize only the minimum representation required for stable file handling.
4. Strip leading/trailing whitespace from the whole document if and only if this is recorded.
5. Preserve internal whitespace, casing, punctuation, Unicode symbols, markup remnants, and source tokenization.
6. Reject the document only if it becomes empty.
Output: canonical text string
```

Do not apply lowercasing, punctuation detokenization, accent stripping, aggressive whitespace collapsing, stopword removal, language filtering, or stemming in the canonical run. These transformations would make the experiment a new corpus rather than a direct nanochat adaptation of WikiText-TL-39.

### Step 3.3: Create a separate clean-data ablation

If resources permit, create a second variant with:

- Unicode NFC normalization.
- HTML entity decoding only when entities are genuinely present.
- Consistent whitespace normalization.
- Exact deduplication after normalization.
- Optional near-duplicate detection using document-level hashes or MinHash.
- Optional removal of obvious navigation boilerplate, URLs, or malformed markup, each with a count and example log.

The clean variant is not the main Project 1 result. It exists to quantify whether modern cleaning changes the result. Every deletion must be categorized and counted.

### Step 3.4: Build the audit report

The audit script should produce:

| Output | Required contents |
|---|---|
| `corpus_audit.json` | Machine-readable counts, lengths, bytes, Unicode categories, duplicates, split-independent statistics |
| `corpus_audit.csv` | One row per metric and variant |
| `length_histogram.png` | Character-length distribution, preferably log-scaled |
| `unicode_categories.csv` | Counts of letters, numbers, punctuation, symbols, whitespace, controls, and replacement characters |
| `sample_rows.jsonl` | Stratified random samples from short, median, long, and anomalous documents |
| `anomaly_rows.jsonl` | Rows with nulls, controls, malformed Unicode, extreme length, high non-Tagalog script share, or suspicious markup |
| `dedup_report.json` | Exact and optional near-duplicate statistics |
| `language_report.json` | Script/language-ID diagnostics, explicitly labeled as diagnostics rather than automatic deletion rules |

Use fixed audit sampling seeds. Save the exact sampled row IDs and hashes so that a reviewer can inspect the same examples.

### Step 3.5: Perform a human-readable native-language inspection

Ask at least one Tagalog/Filipino-proficient reviewer, if available, to inspect a stratified sample. The reviewer should classify each sample as:

- natural Tagalog/Filipino prose;
- acceptable encyclopedia or technical text;
- English or another language;
- markup/navigation noise;
- malformed or unintelligible;
- ambiguous/mixed.

This is not a replacement for automatic audit. It is a quality-control sample that prevents an algorithm from silently treating corpus artifacts as language quality. Record reviewer identity or role, sample size, rubric, disagreements, and unresolved ambiguity.

---

## 10. Phase 4 — Reconstruct or recover data splits

### Step 4.1: First attempt to recover original split boundaries

Before reconstructing splits, inspect:

1. The Hugging Face dataset repository’s complete file tree.
2. The dataset card and commit history.
3. The historical Filipino-Text-Benchmarks repository.
4. Any archived or linked release assets.
5. The original paper’s linked resource repository.

If separate original train, validation, and test files are found and their statistics agree with the paper, use them and record their individual hashes. If only a merged/one-split Parquet is available, do not pretend that a new split reproduces the original boundaries.

### Step 4.2: Recommended fallback: deterministic reconstructed 70/15/15 split

If the original boundaries cannot be recovered, create a deterministic split that follows the original paper’s proportions but is explicitly named `reconstructed_70_15_15`.

Recommended procedure:

1. Canonicalize each document according to the chosen variant.
2. Compute a stable document identity such as `sha256(canonical_text.encode("utf-8"))`.
3. Remove exact duplicates only in the clean ablation; in the canonical variant, retain them but report them.
4. Sort document identities lexicographically by hash, or assign by a documented hash bucket.
5. Allocate the first approximately 70% to train, the next 15% to validation, and the final 15% to test.
6. Record the exact row counts, character counts, byte counts, and hashes for each split.
7. Verify exact disjointness of split identities.
8. Run near-duplicate detection across splits and report the count rather than silently removing it.

A deterministic hash split is preferable to an unrecorded in-memory random shuffle because it is stable across Python versions and iteration order changes. If historical compatibility with nanochat’s repackaging convention is prioritized, a seeded shuffle with seed 42 may be used, but the exact algorithm and library version must be recorded.

### Step 4.3: Split manifest schema

Create `data/manifests/split_manifest.json`:

```json
{
  "split_name": "reconstructed_70_15_15",
  "source_sha256": "...",
  "normalization_variant": "canonical",
  "identity_hash": "sha256_utf8_text",
  "assignment_rule": "lexicographic_hash_order_70_15_15",
  "seed": null,
  "train_rows": 0,
  "validation_rows": 0,
  "test_rows": 0,
  "train_characters": 0,
  "validation_characters": 0,
  "test_characters": 0,
  "exact_overlap_count": 0,
  "near_overlap_count": 0,
  "historical_split_recovered": false,
  "notes": "Reconstructed because current public mirror exposes one train Parquet file."
}
```

### Step 4.4: Prevent test leakage in nanochat’s active directory

The current nanochat loader treats all Parquet files except the last as training files and the last as validation [6]. It has no native third test split. Therefore:

```text
active_data_dir/
├── shard_00000.parquet   # train
├── shard_00001.parquet   # train, if needed
└── shard_000NN.parquet   # validation; must sort last

test_data_dir/
└── test.parquet          # never placed in active_data_dir during training
```

Do not put the test file in the active directory merely because it is convenient. Write a separate evaluation script that opens `test_data_dir/test.parquet` and computes held-out BPB without changing the training directory. If the test evaluator temporarily changes an environment variable, record that operation and verify that the training directory is restored before any resumed training.

---

## 11. Phase 5 — Repackage into nanochat-compatible Parquet shards

### Step 5.1: Use the official reference format

The current `dev/repackage_data_reference.py` documents a Parquet format with one `text` column, shuffled documents, approximately 250 million characters per shard, row-group size 1024, Zstandard compression level 3, dictionary encoding disabled, and statistics disabled [4]. WikiText-TL-39 is much smaller than the corpora for which the reference script was written, so the target shard size can be reduced if necessary. The row-group size and schema should remain compatible.

Recommended writer settings:

```python
pq.write_table(
    table,
    shard_path,
    row_group_size=1024,
    use_dictionary=False,
    compression="zstd",
    compression_level=3,
    write_statistics=False,
)
```

### Step 5.2: Choose deterministic shard ordering

Within each split, use a fixed document order derived from the split manifest. Do not rely on filesystem enumeration. Write training shards in lexicographic order and write validation last. Include a `shard_index`, `split`, `row_count`, `character_count`, `utf8_byte_count`, and SHA-256 checksum in `canonical_shards.json`.

### Step 5.3: Ensure enough files for train/validation behavior

Even if the entire dataset is small enough to fit into one Parquet file, write at least one training shard and one validation shard in the active directory. Otherwise nanochat’s `parquet_paths[:-1]` and `parquet_paths[-1:]` logic can yield an empty training set or accidentally treat the only file as validation.

### Step 5.4: Validate every shard

For every generated shard:

1. Open it with `pyarrow.parquet.ParquetFile`.
2. Assert exactly one `text` column.
3. Assert the column is string-compatible.
4. Assert no null rows.
5. Assert no empty rows unless explicitly retained and counted.
6. Check row-group sizes.
7. Recompute character and byte totals.
8. Compare the written document hashes with the split manifest.
9. Compute the shard checksum.
10. Read a first, middle, and last row from every shard.

The packaging stage is complete only when a fresh process can read all shards in sorted order and reproduce the same aggregate statistics.

---

## 12. Phase 6 — Add the smallest transparent nanochat data-path adapter

### Step 6.1: Avoid the ClimbMix downloader

Do not run the current command from `runs/miniseries.sh` that downloads ClimbMix shards. The current `nanochat/dataset.py` defines a ClimbMix URL, maximum shard count, and ClimbMix-specific cache directory. Project 1 has already prepared its own Parquet files and must not mix or overwrite them.

### Step 6.2: Recommended one-line environment-variable extension

The cleanest small code change is to replace the hard-coded active data directory with an environment-variable override while preserving the default behavior:

```python
DATA_DIR = os.environ.get(
    "NANOCHAT_DATA_DIR",
    os.path.join(base_dir, "base_data_climbmix"),
)
```

Keep the existing default for ordinary nanochat users. Do not remove the ClimbMix downloader. Add a unit test that verifies:

- no environment variable preserves the existing default path;
- `NANOCHAT_DATA_DIR=/path/to/project1_active_data` selects the Project 1 directory;
- `list_parquet_files()` returns sorted files;
- the last file is validation according to the current loader convention.

Record the patch as a separate commit, for example:

```text
project1: add explicit NANOCHAT_DATA_DIR override for custom corpora
```

Do not make unrelated refactors in the same commit.

### Step 6.3: Alternative zero-source-change route

For a pure smoke test, it is possible to place or symlink the Project 1 shards under the default expected directory inside an isolated `NANOCHAT_BASE_DIR`. This avoids modifying source code but is less transparent because the directory name remains ClimbMix-specific. It may be used only for a preliminary compatibility check, not as the preferred publication configuration.

### Step 6.4: Runtime environment

Before any tokenizer or training command:

```bash
export PROJECT_ROOT=/home/ubuntu/project1-wikitext-tl39
export NANOCHAT_BASE_DIR=$PROJECT_ROOT/runtime/nanochat_cache
export NANOCHAT_DATA_DIR=$PROJECT_ROOT/data/runtime/canonical_active
export OMP_NUM_THREADS=1
mkdir -p "$NANOCHAT_BASE_DIR" "$NANOCHAT_DATA_DIR"
```

Write these variables to every run manifest. A common failure mode is training with a tokenizer from one cache directory and data from another. The run preflight must print the resolved base directory, tokenizer directory, and data directory before training begins.

---

## 13. Phase 7 — Train and validate the Tagalog tokenizer

### Step 7.1: Keep the primary tokenizer settings fixed

Use the current nanochat tokenizer training defaults for the canonical run:

| Setting | Primary value | Rationale |
|---|---:|---|
| Vocabulary size | 32,768 | Current nanochat default and power-of-two size. |
| Maximum tokenizer characters | 2,000,000,000 or all available corpus text if smaller | Ensures the small corpus is fully represented. |
| Document cap | 10,000 characters | Current `scripts/tok_train.py` default. |
| Casing | Preserve | Tagalog names, acronyms, and punctuation behavior should remain observable. |
| Tokenizer family | nanochat RustBPE wrapper | Preserves pipeline compatibility. |
| Training split | Train only | Validation and test must not influence tokenizer learning in the primary experiment. |

Run:

```bash
cd /home/ubuntu/research/nanochat
source .venv/bin/activate
export NANOCHAT_BASE_DIR=/home/ubuntu/project1-wikitext-tl39/runtime/nanochat_cache
export NANOCHAT_DATA_DIR=/home/ubuntu/project1-wikitext-tl39/data/runtime/canonical_active
python -m scripts.tok_train \
  --max-chars=2000000000 \
  --doc-cap=10000 \
  --vocab-size=32768 \
  2>&1 | tee /home/ubuntu/project1-wikitext-tl39/results/tokenizer_train.log
```

The script reads the active training Parquet files and saves the tokenizer under `$NANOCHAT_BASE_DIR/tokenizer` [4]. It also creates `token_bytes.pt`, which is required for BPB evaluation.

### Step 7.2: Validate the tokenizer artifact

Check:

```bash
find "$NANOCHAT_BASE_DIR/tokenizer" -maxdepth 2 -type f -print
python -m scripts.test_tokenizer 2>/dev/null || true
```

If no standalone module exists for the second command, run the repository’s tokenizer tests through pytest:

```bash
pytest -q tests/test_tokenizer.py
```

Required checks:

- tokenizer loads in a fresh process;
- vocabulary size is exactly 32,768 or the explicitly configured value;
- `token_bytes.pt` exists and has one entry per token ID;
- Tagalog Unicode characters survive encode/decode round trips;
- punctuation, apostrophes, hyphens, quotation marks, numbers, emojis, and mixed Tagalog/English text do not crash the tokenizer;
- no token ID is out of range;
- special-token IDs are recorded;
- decoded text behavior is documented, including any normalization that is not exactly reversible.

### Step 7.3: Measure tokenization quality

Run the repository tokenizer evaluation if its current CLI supports the intended active dataset, and supplement it with a project-specific script. The project-specific report should compute on train, validation, and test separately:

\[
\text{bytes/token} = \frac{\text{UTF-8 bytes}}{\text{number of BPE tokens}},
\]

\[
\text{tokens/byte} = \frac{\text{number of BPE tokens}}{\text{UTF-8 bytes}},
\]

and the relative compression ratio against at least one general-purpose reference tokenizer, such as GPT-2’s tokenizer. The reference tokenizer is a diagnostic only; it is not used for nanochat training.

Include examples of:

- common Tagalog function words;
- affixed or reduplicated forms;
- clitics and apostrophes;
- diacritics and loanwords;
- proper names;
- numbers and dates;
- punctuation-heavy encyclopedia text;
- sentences containing English names or technical terms.

Do not infer linguistic quality solely from compression. Compression is a useful engineering measure, not a complete measure of linguistic adequacy.

### Step 7.4: Optional vocabulary ablation

After the primary 32,768 run is complete, an optional ablation may compare 16,384, 32,768, and 65,536 vocabulary sizes. Every vocabulary size requires a new tokenizer, new `token_bytes.pt`, new model initialization, and a new training run. Do not compare models across vocabulary sizes using raw cross-entropy alone; use BPB and bytes/token because raw token loss depends on vocabulary segmentation.

---

## 14. Phase 8 — Smoke-test the complete pipeline before production training

### Step 8.1: Run repository tests

From the nanochat root:

```bash
pytest -q tests/test_tokenizer.py tests/test_tasks.py
```

Run broader tests if GPU and time permit:

```bash
pytest -q
```

Record skipped tests and their reasons. A skipped GPU test is not a failure, but it must not be reported as passed.

### Step 8.2: Run a minimal tokenizer–loader smoke test

Write a small script that:

1. imports `get_tokenizer()`;
2. loads the active Parquet files;
3. creates one train batch and one validation batch with `B=1`, `T=128` or `T=512`;
4. verifies tensor shapes `(B,T)` for inputs and targets;
5. verifies token IDs are in `[0, vocab_size)`;
6. verifies the first target is the next-token shift of the first input;
7. prints the loader state dictionary;
8. exits without modifying the dataset.

This catches data-path and tokenizer errors before a model is initialized.

### Step 8.3: Run the d4 smoke model

A CPU/MPS or one-GPU smoke command can follow the repository’s small example:

```bash
python -m scripts.base_train \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=1 \
  --eval-tokens=512 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=10 \
  --total-batch-size=512 \
  --num-iterations=20 \
  --eval-every=10 \
  --run=project1_d4_smoke \
  --model-tag=project1_d4_smoke \
  2>&1 | tee "$PROJECT_ROOT/results/smoke/d4_smoke.log"
```

This is a pipeline test, not a scientific result. It must demonstrate:

- model initialization;
- data loader consumption;
- finite forward and backward passes;
- optimizer updates;
- validation BPB computation;
- checkpoint creation;
- no NaNs or Infs;
- process cleanup.

### Step 8.4: Reload the smoke checkpoint

Use `scripts/base_eval.py` with BPB and samples only:

```bash
python -m scripts.base_eval \
  --eval=bpb,sample \
  --model-tag=project1_d4_smoke \
  --device-batch-size=1 \
  --split-tokens=512 \
  2>&1 | tee "$PROJECT_ROOT/results/smoke/d4_reload_eval.log"
```

A successful original run is not enough. The checkpoint must load in a fresh process and produce a finite evaluation result. Record the exact checkpoint step and metadata hash.

---

## 15. Phase 9 — Design the pilot experiments

### Step 9.1: Determine corpus token counts after tokenizer training

After the tokenizer exists, compute `T_train`, `T_val`, and `T_test` as the number of BPE tokens in each split before the nanochat loader’s best-fit cropping. Also compute UTF-8 byte counts. Save them in `data/manifests/token_statistics.json`.

Use these quantities to define the model-token budgets. For example:

```text
D_1x = 1.0 * T_train
D_3x = 3.0 * T_train
D_10x = 10.0 * T_train
```

The `x` notation means nominal repetitions of the train corpus in model-token budget, not exact passes through source documents, because the loader packs and crops documents. The run must report actual model-visible tokens:

\[
D_{\text{actual}} = N_{\text{iterations}} \times B_{\text{total}}.
\]

### Step 9.2: Use a staged pilot matrix

| Pilot | Depth | Budget | Purpose |
|---|---:|---:|---|
| P0 | d4 | 20–100 steps | Confirm pipeline and numerical stability. |
| P1 | d8 | 1× train-token budget | Confirm learning and basic held-out behavior. |
| P2 | d12 | 1× train-token budget | Compare a more capable model at the same exposure. |
| P3 | d8 | 3× train-token budget | Detect whether more data reuse improves or harms BPB. |
| P4 | d12 | 3× train-token budget | Establish the main low-resource baseline. |
| P5 | d16 | 3× train-token budget | Probe depth scaling and overfitting. |

Do not launch d20 or d24 before P4 and P5 are numerically stable. The purpose of the pilot is to discover data-path, budget, and memory problems cheaply.

### Step 9.3: Choose batch sizes by hardware, not by wishful thinking

The current code requires:

\[
B_{\text{total}} \bmod (B_{\text{device}} \times T \times W) = 0,
\]

where `W` is DDP world size [7]. For `T=2048`, eight GPUs, and `device-batch-size=32`, one micro-batch already contains 524,288 tokens. If the device has less than 80 GB of VRAM, reduce `device-batch-size` to 16, 8, 4, 2, or 1 as recommended by the nanochat README [1]. Keep `total_batch_size` a multiple of the resulting world micro-batch.

Example for eight GPUs, device batch 16, sequence length 2048:

```text
world micro-batch = 16 × 2048 × 8 = 262,144 tokens
```

A total batch size of 524,288 then uses two gradient-accumulation steps. Example for one GPU, device batch 4, sequence length 2048:

```text
world micro-batch = 4 × 2048 × 1 = 8,192 tokens
```

A total batch size of 65,536 then uses eight gradient-accumulation steps.

### Step 9.4: Keep the pilot evaluator Tagalog-aware

Disable CORE for the pilot:

```bash
--core-metric-every=-1
```

Use validation BPB every 25–100 steps for short runs, but do not evaluate so often that validation dominates training time. For the small corpus, a validation budget of several hundred thousand or several million model tokens may be adequate for a pilot; record the exact value and ensure it is divisible by the evaluation micro-batch.

---

## 16. Phase 10 — Run the native nanochat depth family

### Step 10.1: Adapt, do not blindly reuse, `runs/miniseries.sh`

The current miniseries script downloads the default corpus and trains depths `[12, 14, 16, 18, 20, 22, 24, 26]` [3]. For Project 1, copy it to `scripts/project1_native_miniseries.sh` and make the following changes:

1. Remove or disable the default ClimbMix data download.
2. Set `NANOCHAT_BASE_DIR` and `NANOCHAT_DATA_DIR` explicitly.
3. Train the tokenizer only after the WikiText package has been verified.
4. Use the Project 1 depth list `[8, 12, 16, 20]` initially.
5. Disable CORE or set it to final-only with a prominent caveat.
6. Disable sampling during the main throughput run unless sampling is an explicit checkpointed evaluation.
7. Set a Project 1 series name and output directory.
8. Save the complete command line and environment for every depth.
9. Add a preflight check that the active directory’s last Parquet file is validation.
10. Add a post-run checkpoint reload test.

### Step 10.2: Native-horizon command template

Use a positive data-to-parameter ratio and let nanochat derive its native horizon for the compatibility family:

```bash
OMP_NUM_THREADS=1 \
torchrun --standalone --nproc_per_node=8 \
  -m scripts.base_train -- \
  --depth=12 \
  --run=project1_native_d12 \
  --model-tag=project1_native_d12 \
  --target-param-data-ratio=12 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=-1 \
  --eval-every=250 \
  --device-batch-size=16 \
  2>&1 | tee "$PROJECT_ROOT/results/miniseries/project1_native_d12.log"
```

The exact device batch size must be selected after the memory preflight. Do not copy the example blindly. The native family may run for many effective passes through the small corpus. Record the observed loader epoch, validation curve, and train–validation gap.

### Step 10.3: Interpret native-family results carefully

A lower BPB in a native-horizon run may reflect additional repeated exposure to the same source documents rather than better data efficiency. Report:

- total model tokens trained;
- approximate source-corpus passes;
- unique source tokens available;
- number of loader epochs;
- number of cropped source tokens if measurable;
- depth and parameter count;
- effective parameter-to-data ratio;
- training and validation BPB;
- wall-clock time and throughput.

Do not compare native-horizon d8 and d20 as if they saw the same data exposure unless the logged token budgets confirm that they did.

---

## 17. Phase 11 — Run the fixed-data depth family

### Step 11.1: Define the fixed data budget

Choose the primary fixed budget before training. A practical first choice is `D_3x = 3 × T_train`, with an optional `D_1x` and `D_10x` sensitivity analysis. The exact budget should be based on measured nanochat BPE tokens, not on the original paper’s word-token count.

For each depth, calculate:

```text
N_iterations = ceil(D_budget / B_total)
D_actual = N_iterations × B_total
R_scaling = D_budget / P_scaling(depth)
```

Pass a positive `--target-param-data-ratio=R_scaling` so that the current code’s derived weight-decay scaling is based on the chosen budget, while `--num-iterations=N_iterations` makes the actual horizon explicit. Set `--total-batch-size=B_total` explicitly.

### Step 11.2: Produce a depth configuration table

Before launching, write a CSV with one row per depth:

| Field | Meaning |
|---|---|
| `depth` | Transformer layer count. |
| `aspect_ratio` | Model dimension multiplier, normally 64. |
| `head_dim` | Attention head dimension, normally 128. |
| `model_dim` | Derived model width. |
| `num_heads` | Derived attention head count. |
| `num_params_total` | Total parameter count from training log. |
| `num_scaling_params` | Parameter count used for horizon scaling. |
| `target_tokens` | Planned fixed budget. |
| `target_param_data_ratio` | `target_tokens / num_scaling_params`. |
| `total_batch_size` | Tokens per optimizer step. |
| `num_iterations` | Explicit step count. |
| `actual_tokens` | `num_iterations × total_batch_size`. |
| `device_batch_size` | Per-device sequence batch. |
| `world_size` | Number of processes/GPUs. |
| `grad_accum_steps` | Derived accumulation count. |
| `max_seq_len` | Context length, normally 2048. |

This table is the pre-run contract. If a run changes a value, make a new row and a new run ID.

### Step 11.3: Fixed-data command template

```bash
OMP_NUM_THREADS=1 \
torchrun --standalone --nproc_per_node=8 \
  -m scripts.base_train -- \
  --depth=12 \
  --aspect-ratio=64 \
  --head-dim=128 \
  --max-seq-len=2048 \
  --device-batch-size=16 \
  --total-batch-size=524288 \
  --num-iterations=REPLACE_WITH_N \
  --target-param-data-ratio=REPLACE_WITH_R \
  --eval-every=250 \
  --eval-tokens=REPLACE_WITH_EVAL_TOKENS \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=REPLACE_WITH_CHECKPOINT_INTERVAL \
  --run=project1_fixed_d12 \
  --model-tag=project1_fixed_d12 \
  2>&1 | tee "$PROJECT_ROOT/results/miniseries/project1_fixed_d12.log"
```

Run the same command structure for d8, d16, and d20, changing only the preregistered depth-specific values. If the hardware changes, do not change the total-data comparison silently; adjust gradient accumulation while preserving the same total batch size whenever feasible.

### Step 11.4: Checkpoint policy

For a short pilot, final-only checkpoints may be sufficient. For a production run, save at least:

- final checkpoint;
- best validation-BPB checkpoint, if the training script or postprocessing supports it;
- one mid-run checkpoint for recovery and curve inspection;
- checkpoint metadata and optimizer state.

The current checkpoint metadata includes model configuration, user configuration, total batch size, sequence length, data-loader state, validation BPB, and loop state [7]. Preserve all of it. Never publish only the model weights without the tokenizer, token-byte map, configuration, and data manifest.

---

## 18. Phase 12 — Evaluation design

### 18.1 Primary metrics

The primary result is held-out Tagalog **bits per byte**. BPB is appropriate because it is less dependent on the tokenizer vocabulary size than raw token loss and can compare tokenizer variants more fairly. Report separately:

- validation BPB during training;
- final validation BPB;
- final test BPB;
- minimum validation BPB and the step at which it occurred;
- test BPB evaluated only at the preregistered final or selected checkpoint;
- bootstrap confidence intervals where per-example values are available.

### 18.2 Secondary metrics

| Metric | Purpose |
|---|---|
| Raw cross-entropy loss | Optimization diagnostic; not directly comparable across vocabularies. |
| Train BPB | Measures fit to seen data and helps identify memorization. |
| Train–validation BPB gap | Overfitting/data-reuse diagnostic. |
| Bytes/token | Tokenization efficiency. |
| Tokens/byte | Complementary compression measure. |
| Validation perplexity | Optional within-tokenizer diagnostic; label the tokenizer clearly. |
| Tokens/sec | Throughput. |
| MFU | Hardware utilization diagnostic. |
| Peak VRAM | Resource planning. |
| Wall-clock time | Reproducibility and cost estimate. |
| Checkpoint size | Artifact and deployment planning. |
| Reload success | Artifact integrity. |

### 18.3 Built-in BPB evaluation

Use `scripts/base_eval.py --eval=bpb,sample` for the active train/validation directory. Do not include `core` in the primary command. The evaluator requires a valid tokenizer and `token_bytes.pt` and uses the active data-loader convention [5].

Example:

```bash
python -m scripts.base_eval \
  --eval=bpb,sample \
  --model-tag=project1_fixed_d12 \
  --device-batch-size=16 \
  --split-tokens=8388608 \
  2>&1 | tee "$PROJECT_ROOT/results/miniseries/project1_fixed_d12_eval.log"
```

Choose `split-tokens` as a multiple of `device_batch_size × sequence_length × world_size`, or let the evaluator adjust it and record the adjustment.

### 18.4 Independent test evaluator

Write `scripts/evaluate_wikitext_tl39.py` rather than treating the test split as validation. It should:

1. load the saved model and tokenizer;
2. load `data/runtime/test_only/test.parquet` directly;
3. tokenize with the saved tokenizer;
4. apply the same BOS and sequence-packing semantics as the training loader, or clearly document any difference;
5. compute next-token loss;
6. convert loss to BPB using the saved `token_bytes.pt` or an equivalent byte-count procedure;
7. record per-batch or per-document totals;
8. write JSON and CSV outputs;
9. never update model parameters;
10. never write into the training or validation directory.

The evaluator must expose enough intermediate information to verify the denominator. A single scalar without total bytes and total evaluated tokens is not sufficient.

### 18.5 Sampling protocol

Sampling is qualitative and should not substitute for held-out evaluation. Define a fixed Tagalog prompt suite before looking at model outputs. Use prompts that test:

- factual continuation from encyclopedia-style text;
- ordinary descriptive prose;
- a definition;
- a short narrative;
- a question in Tagalog;
- a sentence containing a proper name;
- a sentence containing numbers and dates;
- a sentence containing a technical term;
- an incomplete sentence requiring syntactic continuation;
- a paragraph boundary.

Use fixed temperatures and maximum token lengths. Save prompts, random seed, model checkpoint, tokenizer hash, generated text, and decoding settings. For deterministic comparisons, use temperature 0. For diversity inspection, use one or more stochastic settings with fixed seeds and clearly label them.

Have a Tagalog-proficient reviewer rate samples using a predeclared rubric such as grammatical continuity, lexical plausibility, topical coherence, factual caution, and repetition. Report the rubric and inter-rater agreement if more than one reviewer participates. Do not present a handful of attractive samples as evidence of broad language competence.

### 18.6 Optional downstream probes

After the pure base-model result is locked, a separate follow-on evaluation may use the public dengue, hate-speech, or NewsPH-NLI tasks associated with Filipino NLP research [8] [11]. That follow-on must not alter the Project 1 pretraining result. It should compare:

- a random or minimally trained baseline;
- the Project 1 base model;
- an existing Filipino/Tagalog pretrained model;
- optionally, a multilingual baseline.

Use identical task splits, preprocessing, and evaluation metrics. Keep all task test data out of pretraining or perform explicit contamination analysis.

---

## 19. Phase 13 — Statistical analysis and scientific interpretation

### 19.1 Replication strategy

The full depth series may be expensive, but the project should include repeated seeds where feasible. Recommended design:

| Experiment | Seeds | Reason |
|---|---:|---|
| d4 smoke | 1 | Infrastructure only. |
| d8 pilot | 3 | Estimate run-to-run variance cheaply. |
| d12 pilot | 3 | Main low-resource baseline variance. |
| d16/d20 production | 1–2 | Compute-intensive depth comparison. |
| Best selected model | 3 if resources permit | Stable final estimate and checkpoint selection. |

The current nanochat initialization uses seed 42 in its common initialization path, but full deterministic algorithms are not enabled [12]. Record the seed and hardware; do not claim bitwise determinism. If multiple seeds are run, keep the corpus, split, tokenizer, and training budget fixed and vary only the declared seed.

### 19.2 Confidence intervals

For BPB, prefer document-level or batch-level bootstrap intervals rather than treating every token as independent. A practical procedure is:

1. evaluate the same held-out documents or batches for every depth;
2. record each unit’s total negative log-likelihood and byte denominator;
3. resample units with replacement 1,000 or more times;
4. recompute aggregate BPB for each resample;
5. report the 2.5th and 97.5th percentiles;
6. for paired depth comparisons, resample the same units for both models.

Do not use token-level confidence intervals that ignore document correlation.

### 19.3 Multiple comparisons

If many depths, tokenizers, budgets, and clean-data variants are compared, distinguish primary and exploratory comparisons. Predeclare the primary depth comparison and avoid choosing the “best” model solely by inspecting the test set. Use validation BPB for model selection and test BPB once at the locked checkpoint.

### 19.4 Scaling and overfitting analysis

Plot for each depth:

- train BPB versus model tokens;
- validation BPB versus model tokens;
- train–validation gap versus model tokens;
- validation BPB versus total FLOPs;
- validation BPB versus parameter count;
- throughput versus depth;
- peak memory versus depth;
- BPB against approximate source-corpus passes.

The key interpretation is not simply “deeper is better.” A deeper model that achieves lower train BPB but worse held-out BPB at equal data exposure is evidence of data-limited overfitting or optimization mismatch, not evidence that the model architecture is intrinsically inferior.

### 19.5 Tokenizer comparison analysis

Compare tokenizer variants using BPB, not raw token loss alone. Include:

- vocabulary size;
- train/validation/test bytes/token;
- average and percentile sequence lengths;
- fraction of very long sequences;
- rare-character handling;
- compression on native Tagalog samples;
- training throughput under identical model and hardware settings.

A tokenizer that compresses better but causes longer tail sequences or increases memory pressure may not be operationally superior.

---

## 20. Phase 14 — Reproducibility and provenance protocol

### 20.1 Run manifest

Every run must have a machine-readable manifest containing:

```json
{
  "run_id": "project1_fixed_d12_seed42",
  "timestamp_start_utc": "...",
  "timestamp_end_utc": "...",
  "nanochat_commit": "...",
  "project_patch_commit": "...",
  "uv_lock_sha256": "...",
  "source_dataset_url": "...",
  "source_dataset_sha256": "...",
  "processed_shard_manifest_sha256": "...",
  "split_manifest_sha256": "...",
  "normalization_variant": "canonical",
  "tokenizer_directory_sha256": "...",
  "tokenizer_vocab_size": 32768,
  "tokenizer_training_max_chars": 2000000000,
  "depth": 12,
  "aspect_ratio": 64,
  "head_dim": 128,
  "max_seq_len": 2048,
  "device_batch_size": 16,
  "total_batch_size": 524288,
  "world_size": 8,
  "grad_accum_steps": 2,
  "num_iterations": 0,
  "actual_training_tokens": 0,
  "target_param_data_ratio": 0.0,
  "compute_dtype": "bfloat16",
  "fp8": false,
  "seed": 42,
  "primary_metric": "heldout_tagalog_bpb",
  "core_metric_status": "disabled_primary_not_language_matched"
}
```

Replace every zero or placeholder before archiving.

### 20.2 Hash all important artifacts

Hash:

- raw Parquet;
- every processed Parquet shard;
- split manifest;
- tokenizer files;
- `token_bytes.pt`;
- project configuration;
- nanochat source patch;
- lockfile;
- final checkpoint files;
- evaluation outputs.

For large files, store SHA-256 in a text manifest and include file size and modification timestamp. A hash without a filename is not useful.

### 20.3 Maintain a run index

Create `manifests/run_index.csv` with columns:

```text
run_id,depth,seed,budget_family,budget_tokens,actual_tokens,model_params,scaling_params,tokenizer_hash,source_hash,train_bpb,val_bpb,test_bpb,wall_time_sec,tok_per_sec,peak_vram,checkpoint_path,status,notes
```

Populate the row only after checkpoint reload and evaluation. Failed runs should remain in the index with `status=failed` and a diagnosis; do not delete them.

### 20.4 W&B and local logging

If W&B is used, create one project and one run per depth/seed. Store the local log alongside the W&B URL. If W&B is unavailable or inappropriate for private data, use `--run=dummy` and retain local logs plus structured CSV/JSON metrics. The experiment must remain reproducible without a W&B account.

---

## 21. Compute and storage planning

### 21.1 Hardware tiers

| Tier | Hardware | Use |
|---|---|---|
| Tier A | CPU or MPS | Data audit, tokenizer, d4 smoke, evaluator development. Not a strong-model training environment. |
| Tier B | One CUDA GPU | d4–d12 pilot, debugging, checkpoint reload, selected fixed-budget runs with gradient accumulation. |
| Tier C | Eight A100/H100-class GPUs | Main miniseries and comparable nanochat-style throughput measurements. |
| Tier D | Larger or faster node | Optional d20/d24 or repeated seeds; only if the low-resource result justifies it. |

The nanochat README notes that a single GPU can run the code by omitting `torchrun`, at the cost of substantially longer wall-clock time, and that smaller VRAM requires reducing `--device-batch-size` [1].

### 21.2 Storage estimate

Reserve space for:

- raw Parquet download;
- canonical and clean Parquet copies;
- tokenizer files and token-byte mapping;
- checkpoints and optimizer states for each depth;
- evaluation outputs;
- logs and W&B caches;
- at least one duplicated backup of manifests and final artifacts.

Even if the source corpus is only around 119 MB in its current Parquet representation [8], optimizer states and multiple checkpoints can dominate storage. Keep raw data, processed data, runtime cache, and final artifacts in separate directories so that cleanup does not delete provenance.

### 21.3 Preemption and recovery

For spot/preemptible runs:

1. enable periodic checkpointing;
2. test `--resume-from-step` on the d4 smoke run;
3. preserve optimizer state, not only model weights;
4. archive the last completed log line and manifest;
5. record whether the resumed run repeats or skips any data-loader row groups;
6. compare the resumed checkpoint’s validation curve with the uninterrupted pilot if available.

The current loader stores a resumable state involving Parquet index, row-group index, and epoch, but approximate resume behavior should still be treated as a documented operational detail rather than assumed to be mathematically exact [6] [7].

---

## 22. Failure modes and corrective actions

| Failure mode | Diagnostic signal | Corrective action | Do not do |
|---|---|---|---|
| Downloaded HTML instead of Parquet | `file` reports HTML or PyArrow fails | Re-download with `curl --fail -L`; inspect response; record URL status | Do not feed the file to the tokenizer. |
| Legacy S3 URL fails | HTTP 404 | Use current Hugging Face mirror; record historical URL as unavailable | Do not keep retrying a known-dead URL. |
| No Parquet files found | Loader assertion | Check `NANOCHAT_DATA_DIR`, active directory, file permissions, and shard naming | Do not copy files into an unrelated default cache without recording it. |
| Validation set is empty | Loader sees one file only or wrong file order | Ensure at least one train shard plus a final validation shard | Do not train with an unverified split. |
| Test leakage | Hash overlap or test file visible in active directory | Rebuild active directory and test directory; rerun manifest checks | Do not merely rename the file. |
| Tokenizer round-trip failure | Assertion or Unicode corruption | Inspect special tokens, encoding, and source normalization | Do not silently drop non-ASCII text. |
| CUDA OOM | OOM during model init or micro-step | Reduce device batch size, verify total-batch divisibility, consider full-attention window pattern if needed | Do not change depth or sequence length without a new run ID. |
| NaN/Inf loss | Non-finite log values | Reproduce on d4; inspect dtype, FP8, LR, data anomalies; disable FP8 first | Do not continue a non-finite run as valid. |
| Excessive overfitting | Train BPB falls while validation BPB worsens | Compare fixed budgets, reduce repeated exposure, add explicit early-checkpoint analysis | Do not select the final model using test BPB. |
| Invalid CORE interpretation | Low English CORE despite good Tagalog BPB | Mark CORE auxiliary/non-diagnostic; use Tagalog evaluation | Do not claim the model failed Tagalog from English CORE alone. |
| Run cannot reload | Checkpoint metadata/tokenizer mismatch | Preserve tokenizer with checkpoint; verify model tag and base directory | Do not publish weights without tokenizer artifacts. |
| Data-loader throughput is poor | Low tokens/sec, high CPU wait | Check row-group size, shard locality, Parquet compression, tokenizer threads, storage throughput | Do not change model conclusions based on a bottlenecked pilot. |
| Reproducibility drift | Different row counts or BPB across reruns | Compare hashes, commit, lockfile, split manifest, environment, and data order | Do not average runs with different data variants. |

---

## 23. Minimum viable execution sequence

If the full plan must be executed incrementally, use this exact order.

### Milestone M1: Source verified

1. Clone and freeze nanochat.
2. Download the current Hugging Face Parquet file.
3. Record checksum and source manifest.
4. Inspect schema, rows, lengths, nulls, duplicates, and sample content.
5. Confirm whether original split files are available.

**Exit condition:** source artifact is valid and provenance is complete.

### Milestone M2: Data package verified

1. Create canonical normalization.
2. Create deterministic reconstructed splits if necessary.
3. Run overlap checks.
4. Write train/validation/test Parquet files.
5. Place only train and validation in the active directory.
6. Validate shard schema and checksums.

**Exit condition:** all split and packaging invariants pass.

### Milestone M3: Tokenizer verified

1. Apply the data-directory adapter.
2. Train 32,768-vocabulary tokenizer on train only.
3. Verify round trips and token IDs.
4. Save `token_bytes.pt`.
5. Compute Tagalog tokenization statistics.

**Exit condition:** tokenizer loads and produces stable diagnostics.

### Milestone M4: Pipeline verified

1. Run unit tests.
2. Run one data-loader batch.
3. Run d4 smoke for 20 steps.
4. Evaluate validation BPB.
5. Reload checkpoint.

**Exit condition:** end-to-end training and reload succeed.

### Milestone M5: Pilot verified

1. Run d8 and d12 at 1× budget.
2. Run d8 and d12 at 3× budget.
3. Compare train/validation BPB and resource use.
4. Confirm no budget or data-leakage issue.

**Exit condition:** a defensible budget and depth series are selected.

### Milestone M6: Production series

1. Run fixed-data d8, d12, d16, d20.
2. Optionally run native-horizon counterparts.
3. Save checkpoints, logs, manifests, and metrics.
4. Run independent validation/test evaluator.
5. Generate tables and plots.

**Exit condition:** all preregistered runs are complete or diagnosed.

### Milestone M7: Final scientific result

1. Lock the selected checkpoint using validation only.
2. Run the test evaluator once.
3. Run fixed prompt sampling.
4. Complete statistical analysis.
5. Write limitations and release instructions.

**Exit condition:** final report distinguishes exact reproduction, reconstruction, ablation, and exploratory evidence.

---

## 24. Suggested final tables and figures

### Table A: Source and split statistics

Include rows for raw source, canonical train, canonical validation, canonical test, and optional clean variants. Columns should include documents, characters, UTF-8 bytes, approximate source tokens, nanochat BPE tokens, exact duplicates, and near-duplicate counts.

### Table B: Tokenizer statistics

Include vocabulary size, tokenizer training characters, bytes/token, tokens/byte, sequence-length percentiles, special tokens, and examples of Tagalog segmentation.

### Table C: Model configurations

Include depth, model dimension, heads, total parameters, scaling parameters, sequence length, total batch size, device batch size, gradient accumulation, target tokens, actual tokens, FLOPs estimate, dtype, and FP8 status.

### Table D: Main results

Include depth, seed, budget family, train BPB, validation BPB, test BPB, minimum validation step, train–validation gap, throughput, wall-clock time, peak VRAM, and checkpoint status.

### Figure 1: Pipeline diagram

Show source acquisition → audit → deterministic split → Parquet packaging → tokenizer → nanochat loader → causal pretraining → validation BPB → independent test evaluator.

### Figure 2: Data-size and split distribution

Show document and byte counts across train, validation, and test. Use separate panels for document count and UTF-8 bytes so that a large number of short documents is not confused with corpus volume.

### Figure 3: Training curves

Plot train loss/BPB and validation BPB against model tokens, with one panel per depth or one color per depth. Mark the selected checkpoint and the point at which validation BPB stops improving.

### Figure 4: Depth scaling

Plot test BPB against parameter count and against total training FLOPs. Include confidence intervals where repeated seeds permit them.

### Figure 5: Overfitting and data reuse

Plot train–validation BPB gap against approximate source-corpus passes. This figure is central to interpreting whether deeper models are data-limited.

### Figure 6: Tokenizer compression

Compare bytes/token and tokens/byte for the nanochat Tagalog tokenizer and reference tokenizers on the same held-out text.

### Figure 7: Throughput and memory

Plot tokens/sec and peak VRAM against depth, with hardware and batch configuration in the caption.

---

## 25. Final reporting structure

The final paper or technical report should contain the following sections.

1. **Abstract:** State the corpus, nanochat version, model family, primary metric, and main result without overclaiming.
2. **Introduction:** Motivate low-resource Tagalog modeling and explain why a pure base-model reproduction is useful.
3. **Related work:** Cite WikiText-TL-39, TLUnified, Filipino benchmark work, and nanochat.
4. **Research questions and hypotheses:** State the preregistered questions and expected failure modes.
5. **Data provenance:** Describe the current Hugging Face mirror, historical source, checksum, retrieval date, and split-recovery status.
6. **Corpus audit and preprocessing:** Separate canonical and clean variants and report all deletions or transformations.
7. **Data packaging:** Explain Parquet shards, row groups, compression, validation-last convention, and test isolation.
8. **Tokenizer:** Describe RustBPE, vocabulary size, training data, document cap, and compression metrics.
9. **Model and training:** Report nanochat commit, depth dial, sequence length, batch size, optimizer settings, dtype, horizon, and hardware.
10. **Evaluation:** Define BPB, test evaluator, sampling rubric, and optional downstream probes.
11. **Results:** Present source statistics, tokenizer statistics, training curves, depth results, and resource use.
12. **Ablations:** Native versus fixed-budget horizon; canonical versus clean data; optional vocabulary size.
13. **Error and risk analysis:** Discuss leakage, source noise, overfitting, language mismatch, and checkpoint failures.
14. **Limitations:** State that the corpus is small, the current mirror may not expose original split boundaries, and base-model BPB does not establish conversational competence.
15. **Reproducibility:** Provide exact commands, manifests, hashes, environment, and artifact locations.
16. **Conclusion:** State the narrow conclusion supported by the data.

Use calibrated language. For example:

- “The evidence supports the conclusion that the pipeline can train a reproducible Tagalog base model on the current public WikiText-TL-39 mirror.”
- “The fixed-budget results are consistent with diminishing returns from depth under this corpus size.”
- “We cannot claim exact replication of the 2019 split unless the original split boundaries are recovered.”
- “The results do not establish instruction-following or conversational ability because no SFT or chat evaluation was performed.”

---

## 26. Completion checklist

### Source and provenance

- [ ] Current Hugging Face source URL recorded.
- [ ] Raw Parquet SHA-256 recorded.
- [ ] Retrieval timestamp recorded.
- [ ] Historical S3 link status recorded as unavailable.
- [ ] License/provenance terms reviewed and documented.
- [ ] Nanochat commit recorded.
- [ ] Project patch commit recorded.
- [ ] Environment and lockfile hashes recorded.

### Corpus

- [ ] Schema verified.
- [ ] Row count verified.
- [ ] Null and empty rows measured.
- [ ] Length distributions computed.
- [ ] Unicode diagnostics computed.
- [ ] Exact duplicates measured.
- [ ] Near-duplicates assessed.
- [ ] Canonical and clean variants kept separate.
- [ ] Original split recovery attempted.
- [ ] Reconstructed split labeled if necessary.
- [ ] Exact train/validation/test disjointness verified.
- [ ] Test data excluded from active training directory.

### Packaging

- [ ] Parquet `text` schema verified.
- [ ] Zstandard compression verified.
- [ ] Row-group size recorded.
- [ ] Train shards sorted.
- [ ] Validation shard placed last.
- [ ] Shard checksums recorded.
- [ ] Fresh-process read test passed.

### Tokenizer

- [ ] Vocabulary size recorded.
- [ ] Tokenizer trained on train only.
- [ ] `token_bytes.pt` generated.
- [ ] Unicode round trips passed.
- [ ] Special token IDs recorded.
- [ ] Tokenization statistics computed on all splits.
- [ ] Optional reference-tokenizer comparison completed.

### Training

- [ ] Repository tests run.
- [ ] Data-loader smoke test passed.
- [ ] d4 smoke passed.
- [ ] Checkpoint reload passed.
- [ ] d8 and d12 pilots passed.
- [ ] Fixed-data budget calculated per depth.
- [ ] Batch divisibility verified.
- [ ] Native and fixed-budget families labeled.
- [ ] OOM/dtype/FP8 choices recorded.
- [ ] All production logs archived.

### Evaluation

- [ ] Validation BPB measured.
- [ ] Test BPB measured independently.
- [ ] Test evaluated only after checkpoint selection.
- [ ] Train–validation gap computed.
- [ ] Throughput and memory recorded.
- [ ] Fixed Tagalog prompt suite evaluated.
- [ ] CORE disabled or explicitly marked auxiliary.
- [ ] Optional downstream probes kept separate.

### Reporting

- [ ] Main result table complete.
- [ ] Data table complete.
- [ ] Tokenizer table complete.
- [ ] Training curves generated.
- [ ] Depth scaling plot generated.
- [ ] Overfitting plot generated.
- [ ] Limitations written before final interpretation.
- [ ] Reproduction commands tested from a clean environment.
- [ ] Artifact index and hashes attached.

---

## 27. Short command sequence for the first successful run

The following is a condensed execution path after the detailed gates above have been satisfied. It is intentionally not a substitute for the full plan.

```bash
# 1. Environment
cd /home/ubuntu/research/nanochat
source .venv/bin/activate
export PROJECT_ROOT=/home/ubuntu/project1-wikitext-tl39
export NANOCHAT_BASE_DIR=$PROJECT_ROOT/runtime/nanochat_cache
export NANOCHAT_DATA_DIR=$PROJECT_ROOT/data/runtime/canonical_active
export OMP_NUM_THREADS=1

# 2. Verify active data
python - <<'PY'
import os
import pyarrow.parquet as pq
root = os.environ["NANOCHAT_DATA_DIR"]
files = sorted(os.path.join(root, f) for f in os.listdir(root) if f.endswith(".parquet"))
assert len(files) >= 2, files
for p in files:
    pf = pq.ParquetFile(p)
    assert pf.schema.names == ["text"], (p, pf.schema.names)
    print(p, pf.metadata.num_rows, pf.num_row_groups)
print("validation_candidate:", files[-1])
PY

# 3. Train tokenizer
python -m scripts.tok_train \
  --max-chars=2000000000 \
  --doc-cap=10000 \
  --vocab-size=32768 \
  2>&1 | tee "$PROJECT_ROOT/results/tokenizer_train.log"

# 4. Run d4 smoke
python -m scripts.base_train \
  --depth=4 \
  --max-seq-len=512 \
  --device-batch-size=1 \
  --eval-tokens=512 \
  --total-batch-size=512 \
  --num-iterations=20 \
  --eval-every=10 \
  --core-metric-every=-1 \
  --sample-every=-1 \
  --save-every=10 \
  --run=project1_d4_smoke \
  --model-tag=project1_d4_smoke \
  2>&1 | tee "$PROJECT_ROOT/results/smoke/d4_smoke.log"

# 5. Reload and evaluate
python -m scripts.base_eval \
  --eval=bpb,sample \
  --model-tag=project1_d4_smoke \
  --device-batch-size=1 \
  --split-tokens=512 \
  2>&1 | tee "$PROJECT_ROOT/results/smoke/d4_reload_eval.log"
```

The first successful run should be considered a **pipeline certificate**, not the scientific conclusion. The scientific conclusion begins only after the data manifest, tokenizer statistics, fixed-budget depth series, independent test evaluation, and limitations are complete.

---

## References

[1]: https://github.com/karpathy/nanochat "Karpathy nanochat repository"

[2]: https://github.com/karpathy/nanochat/blob/master/README.md "nanochat README: setup, research workflow, depth dial, and hardware notes"

[3]: https://github.com/karpathy/nanochat/blob/master/runs/miniseries.sh "nanochat miniseries script"

[4]: https://github.com/karpathy/nanochat/blob/master/dev/repackage_data_reference.py "nanochat Parquet repackaging reference"

[5]: https://github.com/karpathy/nanochat/blob/master/scripts/base_eval.py "nanochat base evaluation script"

[6]: https://github.com/karpathy/nanochat/blob/master/nanochat/dataloader.py "nanochat distributed BOS-aligned best-fit data loader"

[7]: https://github.com/karpathy/nanochat/blob/master/scripts/base_train.py "nanochat base training script"

[8]: https://huggingface.co/datasets/linkanjarad/Wikitext-TL39 "WikiText-TL-39 current Hugging Face mirror"

[9]: https://arxiv.org/html/1907.00409v1 "Cruz and Cheng, Evaluating Language Model Finetuning Techniques for Low-resource Languages"

[10]: https://github.com/karpathy/nanochat/blob/master/pyproject.toml "nanochat dependency and environment configuration"

[11]: https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks "Filipino Text Benchmarks historical repository and WikiText-TL-39 provenance link"

[12]: https://github.com/karpathy/nanochat/blob/master/nanochat/common.py "nanochat initialization, seed, dtype, and cache utilities"
