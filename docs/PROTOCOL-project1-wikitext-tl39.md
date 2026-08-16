# Protocol P1.1 — Pure Tagalog Base Language Model on WikiText-TL-39 with nanochat

**Document type:** Pre-analysis plan, filed as AsPredicted #306780  
**Project catalog ID:** Project 1 (not rank 1; catalog Project 3 is BalitaNLP; catalog Project 8 is dengue)  
**Short title:** `nanochat-tl-wikitext39`  
**Status:** Filed. AsPredicted #306780, anonymous PDF https://aspredicted.org/6r6v4v.pdf (2026-08-15 19:34 PT). ResearchBox #8735. No confirmatory training yet. Full wording: [run-cards/aspredicted-p1-submitted.txt](run-cards/aspredicted-p1-submitted.txt).  
**Charter:** [../configs/project1.yaml](../configs/project1.yaml)  
**Execution clarifications (pre-start, not an AsPredicted amendment):** [EXECUTION-CLARIFICATIONS-p1.1.md](EXECUTION-CLARIFICATIONS-p1.1.md)  
**Gate ledger:** [../manifests/gate_ledger.json](../manifests/gate_ledger.json)  
**Implementation source folded in:** [SOURCE-implementation-plan-2026-08-16.md](SOURCE-implementation-plan-2026-08-16.md)  
**nanochat pin:** `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`  
**Corresponding papers:** Cruz & Cheng (2019), arXiv:1907.00409; Karpathy (2025–2026), `karpathy/nanochat`  
**Primary metric:** held-out Tagalog bits-per-byte (`val_bpb_full`, then one `test_bpb`)  
**Primary comparison:** fixed-data family at `D_3x = 3 * T_train` BPE tokens, depths 8/12/16/20  
**Forbidden as a primary claim:** DCLM CORE, English MMLU/ARC/GSM8K, training loss alone, native-horizon depth rankings as equal-exposure comparisons  

This protocol is written so that a second experimenter, given only this document, the public parquet, and a pinned nanochat commit, can reproduce the artifact and the numbers. Every gate below is a hard stop: do not proceed if the acceptance test fails.

---

## 0. How to use this document

### 0.1 Reading order

1. Read §1–§4 before touching a GPU. These sections fix the scientific claim.  
2. Execute §5–§8 on a CPU machine. These sections lock the environment and the corpus.  
3. Execute §9–§12 on CPU or a small GPU. These sections produce shards and a tokenizer.  
4. Execute §13 on CPU or one GPU (smoke).  
5. Execute §14–§16 on the intended GPU node (primary runs).  
6. Execute §17–§22 before writing a paper, README, or tweet.

### 0.2 Notation

| Symbol | Meaning |
|---|---|
| \(N_{\text{doc}}\) | Number of Wikipedia articles after reconstruction |
| \(N_{\text{line}}\) | Number of parquet rows (lines / paragraphs) |
| \(C\) | Unicode character count, NFC, after the chosen detokenization policy |
| \(T_{\text{BPE}}\) | Token count under the trained nanochat tokenizer |
| \(T_{\text{Moses}}\) | Token count under the original Moses whitespace tokens |
| \(P_{\text{total}}\) | All trainable parameters (report in tables) |
| \(P_{\text{scaling}}\) | Nanochat scaling-param count used for horizon math |
| \(T_{\text{train}}\) | Source BPE inventory of the train split after tokenizer training, **before** packer crop; see [EXECUTION-CLARIFICATIONS-p1.1.md](EXECUTION-CLARIFICATIONS-p1.1.md) §4 |
| \(D\) | Transformer depth (`--depth`) |
| \(\rho\) | Tokens-to-parameters ratio \(T_{\text{seen}} / P\) |
| BPB | Bits per byte, \(\mathrm{BPB} = \bar{\ell} / (\ln 2 \cdot \overline{b})\), vocab-size invariant |
| PPL | Token-level perplexity \(\exp(\bar{\ell})\). Report only with the tokenizer named. |

### 0.3 Gate language

- **MUST** — required for the run to count as Protocol P1.0.  
- **MUST NOT** — forbidden; a violation invalidates the run.  
- **SHOULD** — default; record a deviation in the run card if skipped.  
- **MAY** — optional extension; must be labeled as such in the report.

### 0.4 What this project is and is not

**This project is:** an unsupervised Tagalog language-modeling experiment. Obtain WikiText-TL-39, package it as nanochat parquet shards, train a GPT-4-style BPE tokenizer, train a small compute-appropriate GPT with nanochat’s official `scripts.tok_train` → `scripts.base_train` → `scripts.base_eval` path, and report held-out BPB plus qualitative samples.

**This project is not:** TLUnified reconstruction; OSCAR filtering; dengue or hate-speech classification; English GPT-2 speedrun; a claim that a d24 model is compute-optimal on 39 million tokens; a chatbot until a later protocol (P8/P9) attaches a probe or SFT head.

---

## 1. Scientific objective

### 1.1 One-sentence objective

Train the smallest *honest* nanochat base model that (a) uses only the public WikiText-TL-39 corpus, (b) never sees the held-out documents during tokenizer training, optimization, or model selection, and (c) reports a vocab-invariant likelihood on those documents.

### 1.2 Motivation (why this, why now)

Cruz & Cheng (2019) released WikiText-TL-39 as the first large open Tagalog language-modeling corpus: 39,267,089 Moses tokens in the training split, constructed analogously to Merity et al. (2016) WikiText. Subsequent Cheng-group work (Cruz & Cheng 2020; Cruz & Cheng 2022 / TLUnified) showed that *more and more varied* pretraining data improves Filipino classifiers. Project 1 does not try to beat TLUnified. It establishes a **minimum viable, fully public, fully inspectable** Tagalog nanochat baseline against which later corpus upgrades (Wikipedia dump, CC-100 `tl`, OSCAR if access opens) can be compared with every other knob held fixed.

Karpathy’s nanochat is designed around a single complexity dial (`--depth`) and a native metric (`val_bpb`). That combination is the right instrument for a first Tagalog base: one script family, one metric that does not secretly depend on English multiple-choice sets.

### 1.3 Research questions (P1.1)

**RQ1 (feasibility).** Can the official nanochat tokenizer → pretrain → eval loop run on WikiText-TL-39 with no ClimbMix download and only a minimal explicit data-path adaptation (`NANOCHAT_DATA_DIR`)?

**RQ2 (depth, fixed budget).** How does transformer depth in {8, 12, 16, 20} affect Tagalog held-out BPB, train–val gap, and sample quality when every depth sees the same number of model-visible tokens (`D_3x`)?

**RQ3 (tokenizer).** Does a 32,768 Tagalog BPE reduce bytes/token on held-out Tagalog relative to a general English tokenizer (e.g. GPT-2) at the same evaluation text? Secondary: train-only vs all-split tokenizer leakage.

**RQ4 (horizon).** Does nanochat’s default `--target-param-data-ratio` (12) induce substantial corpus reuse on this small dump, relative to a fixed-data family?

**RQ5 (usefulness).** After independent test BPB, contamination checks, checkpoint reload, and a fixed prompt audit, is the artifact a scientifically usable Tagalog base — not merely a completed run?

### 1.4 Non-questions (explicitly out of scope for P1.0)

- Downstream accuracy on dengue, hate-speech, fake news, or NewsPH-NLI. Those are Protocols P8, P9, P10, P11 and MUST use this checkpoint as a frozen or lightly tuned base, not as an excuse to peek at those labels during P1.  
- Cebuano, Waray, or Taglish.  
- Instruction following, chat special tokens, or identity SFT.  
- Beating GPT-2 CORE. CORE is an English DCLM suite. A Tagalog Wikipedia model that scores near chance on CORE has learned nothing relevant to RQ2.

---

## 2. Theoretical framing and related work

### 2.1 Language-model evaluation

Token-level cross-entropy is not comparable across tokenizers (Mielke et al.; see also nanochat’s own rationale for `token_bytes.pt`). Bits-per-byte normalizes the mean NLL by the UTF-8 byte length of the decoded tokens and is therefore the **only** likelihood number this protocol treats as primary. Perplexity MAY be reported in an appendix, always paired with `vocab_size` and the tokenizer SHA256.

### 2.2 Compute optimality

Hoffmann et al. (2022, “Chinchilla”) recommend on the order of 20 tokens per parameter for compute-optimal dense LMs. nanochat’s `--target-param-data-ratio` default is 12 (experimentally retuned for its stack); `runs/speedrun.sh` uses 8 for a slightly undertrained d24 on ClimbMix. WikiText-TL-39 contains on the order of \(4 \times 10^7\) Moses tokens. Even if BPE emits a similar count, a 20-token-per-parameter rule implies \(P \approx 2 \times 10^6\). A nanochat d24 with a 32k vocabulary is on the order of \(10^9\) parameters and is therefore a **many-epoch overparameterized** regime on this corpus. Treating d24 as the “default nanochat model” would answer a different question (“how fast can we overfit Tagalog Wikipedia?”). P1.0 answers the compute-appropriate question first.

### 2.3 Document-level leakage

WikiText-style corpora are article collections. A random *line* split puts the second paragraph of an article in train and the first in test. That leaks entity names, boilerplate, and local syntax. Cruz & Cheng split 70/15/15; the working Hugging Face parquet (`linkanjarad/Wikitext-TL39`) exposes a **single `train` split of 1.52 million rows**. P1.0 therefore **reconstructs articles and re-splits at document level**. The original 70/15/15 cut is the target *ratio*, not a claim that we recovered their exact document IDs.

### 2.4 Moses pretokenization

The released text is Moses-tokenized (Koehn et al. 2007): spaces around punctuation, `@-@` and `@,@` numeric/hyphen markers, original casing retained. P1.1 **preserves that surface form** in the canonical run (public-mirror reproduction). Detokenization is an exploratory ablation only.

### 2.5 Cheng lineage (what alignment means here)

| Work | Relation to P1.0 |
|---|---|
| Cruz & Cheng 2019, WikiText-TL-39 | **Direct data source and citation.** |
| Cruz & Cheng 2020, transformer baselines | Downstream motivation; not used as training data. |
| Cruz & Cheng 2022, TLUnified + RoBERTa | Methodological *next* project (P2/P4), not P1. |
| Livelo & Cheng 2018 dengue; Cabasag et al. 2019 hate-speech | Probe protocols after a P1 checkpoint exists. |

---

## 3. Hypotheses and success criteria

### 3.1 Hypotheses (P1.1, confirmatory)

**H1 (pipeline).** The current nanochat stack can train and evaluate WikiText-TL-39 after a small isolated data-directory change (`NANOCHAT_DATA_DIR` or documented isolated-cache fallback). Falsified if the loader cannot consume the packaged corpus without architectural changes beyond that hook.

**H2 (tokenizer).** A 32,768 Tagalog RustBPE trained on train documents only will reduce bytes/token on held-out Tagalog relative to a general English tokenizer (GPT-2 / default nanochat English tokenizer) on the same text and vocab-size-aware BPB comparison. Falsified if compression is equal or worse.

**H3 (depth under fixed data).** Under the primary fixed budget `D_3x`, held-out `val_bpb` improves with depth up to a point in {8, 12, 16, 20}, after which returns diminish or the train–val gap widens. Falsified if larger depths keep improving held-out BPB without a widening gap at the same token budget.

**H4 (native horizon).** The default positive `--target-param-data-ratio` (12) induces substantial data reuse (many source-corpus passes) on this dump. Falsified if measured passes stay low and train–val curves show no reuse concern.

**H5 (metric).** Tagalog held-out BPB is the informative primary number; English CORE is not. Falsified only if a validated Tagalog task suite later shows CORE tracks the relevant behavior (not expected; would be a new study).

**Secondary (not used to pick the primary tokenizer or depth):** train-only vs all-split tokenizer fertility gap; random-init and byte-unigram baselines (trained `val_bpb` MUST still beat both or the run is a scientific failure).

### 3.2 Success criteria (the run “works”)

A P1.0 run is **scientifically successful** if and only if all of the following hold:

1. No ClimbMix, FineWeb, OSCAR, or English shard appears in `NANOCHAT_BASE_DIR` for that run.  
2. SHA256 of the downloaded parquet matches the value recorded in the run card.  
3. Train / val / test document ID sets are disjoint. Hash overlap MUST be 0.  
4. Tokenizer was trained on **training documents only**.  
5. `scripts.base_train` and `scripts.base_eval` are the official nanochat entry points (wrappers MAY set flags; they MUST NOT reimplement the trainer).  
6. Primary table reports `val_bpb` and `test_bpb` with tokenizer id, depth, \(P\), \(T_{\text{seen}}\), \(\rho\), seed, and nanochat commit.  
7. `core_metric` is either disabled (`--core-metric-every=-1`) or reported in an appendix labeled “English DCLM CORE, not a Tagalog result.”

A run is **engineering-successful** (pipeline works) if a d4 smoke run finishes, writes a checkpoint, and produces a finite `val_bpb`. Engineering success is necessary but not sufficient for scientific success.

### 3.3 Failure criteria (stop and file a deviation)

Stop the primary GPU run if any of the following occur:

- `val_bpb` is NaN or Inf.  
- `val_bpb` increases for three consecutive evaluations after warmup while train BPB continues to fall (overfit tripwire for the *primary* one-epoch run — unexpected; check data leak).  
- Throughput drops to 0 tok/s or the job is preempted without a checkpoint.  
- Disk SHA256 of any shard changes mid-run.

---

## 4. Threats to validity (pre-registered)

Record each threat in the report even if you believe it is mitigated.

### 4.1 Internal validity

| Threat | Mitigation |
|---|---|
| Line-level leakage | Document reconstruction + document-level split (§10). |
| Tokenizer leakage | Train tokenizer on train docs only (§12). |
| Eval set too small / too large | `eval-tokens` MUST be ≤ 50% of val tokens and ≥ 10% or 50k tokens, whichever is smaller (§15). |
| Last-shard-is-val convention | nanochat treats the **lexicographically last** parquet as val. Shard naming MUST put val last (§11). |
| Checkpoint selection on test | Model selection uses val BPB only. Test is touched once, after freeze. |
| Moses markers as “language” | Default detokenize; Moses-as-is is an ablation. |
| Multiple-epoch unacknowledged | Log epoch index; \(\rho\) uses *tokens seen*, not unique tokens. |

### 4.2 External validity

| Threat | Mitigation |
|---|---|
| Wikipedia ≠ general Tagalog | State the domain. Do not claim “Filipino web performance.” |
| 2019 snapshot ≠ current tlwiki | Record parquet source date. A later Wikipedia dump is a different corpus (Run 2 in the corpus series). |
| Mirror ≠ original 70/15/15 IDs | Do not claim exact Cruz & Cheng split recovery unless document IDs are matched (§10.6). |
| BPE ≠ Moses vocabulary of 279,153 | Do not compare PPL to the 2019 paper without converting to BPB. |

### 4.3 Construct validity

| Threat | Mitigation |
|---|---|
| CORE as “quality” | Disabled. |
| Train loss as “quality” | Secondary log only. |
| Sample anecdotal quality | Three fixed prompts, two seeds; not a metric. |

### 4.4 Statistical conclusion validity

One seed is allowed for the *pipeline* paper. Any claim of the form “d8 beats d6” MUST use ≥ 3 seeds or be labeled exploratory. BPB differences smaller than \(0.01\) MUST NOT be interpreted without a seed sweep.

---

## 5. Materials

### 5.1 Hardware classes (pick one and write it on the run card)

| Class | Example | Allowed stages | Forbidden |
|---|---|---|---|
| C0 CPU/MPS | Apple Silicon, no CUDA | §5–§13 smoke with `runs/runcpu.sh`-style tiny flags | Primary d6+ one-epoch if wall time > 12 h without a written waiver |
| C1 single consumer GPU | 12–24 GB (3080, 4090, T4) | Smoke + primary d4/d6; reduce `--device-batch-size` | `--fp8` |
| C2 single datacenter GPU | 40–80 GB (A100, H100) | All primary depths | None |
| C3 8×H100 | nanochat native | All depths; still MUST NOT treat d24 as P1 primary | Claiming a GPT-2 speedrun on Tagalog wiki |

P1.0 is designed to complete on **C1**. C3 is optional luxury, not a requirement.

### 5.2 Software pin list (fill versions at lock time)

| Component | Pin policy |
|---|---|
| OS | Record `uname -a` |
| NVIDIA driver / CUDA | Record `nvidia-smi` |
| Python | The version `uv` selects for nanochat |
| nanochat | **Git commit SHA, not `master`** |
| `uv.lock` | Copy into `vendor/nanochat-lock/` |
| Hugging Face `datasets` | Pin in the data-prep environment |
| pyarrow | Same major as nanochat |
| wandb | Optional; if unused, `WANDB_RUN=dummy` |

### 5.3 Data sources (only these)

| Role | Source | URL | Status |
|---|---|---|---|
| **Primary corpus** | `linkanjarad/Wikitext-TL39` | https://huggingface.co/datasets/linkanjarad/Wikitext-TL39 | Working parquet, ~119 MB, 1.52M rows, one `train` split |
| Direct file | `data/train.parquet` | https://huggingface.co/datasets/linkanjarad/Wikitext-TL39/resolve/main/data/train.parquet | MUST use this or `huggingface-cli download` |
| Citation loader (optional audit) | `SEACrowd/wikitext_tl_39` | https://huggingface.co/datasets/SEACrowd/wikitext_tl_39 | MAY load for comparison; MUST NOT mix into training without a new protocol |
| Dead source | Original S3 zip | `s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/wikitext-tl-39/wikitext-tl-39.zip` | **HTTP 404. MUST NOT be listed as a download step.** |
| Paper | Cruz & Cheng 2019 | https://arxiv.org/abs/1907.00409 | Citation and Table 1 targets |

### 5.4 Published target statistics (Cruz & Cheng 2019, Table 1)

Use these as **audit targets**, not as a guarantee that the parquet matches.

| Split | Documents | Moses tokens | Unique tokens | Lines |
|---|---:|---:|---:|---:|
| Training | 120,975 | 39,267,089 | 279,153 | 1,403,147 |
| Validation | 25,919 | 8,356,898 | 164,159 | 304,006 |
| Testing | 25,921 | 8,333,288 | 175,999 | 298,974 |
| OOV in test | 28,469 (0.1020%) | | | |

**Known discrepancy (must be resolved in §9):** the parquet reports **1.52 million rows** and a single split. Table 1 train lines = 1,403,147; all three splits = 2,006,127. 1.52M is neither number. P1.0 therefore treats the parquet as an **imperfect mirror** and rebuilds splits from reconstructed documents. Record the measured \(N_{\text{line}}\), \(N_{\text{doc}}\), and \(T_{\text{Moses}}\) in the data card. Do not silently assume 39,267,089 tokens.

### 5.5 Directory layout (MUST)

```text
nanochat-filipino/
  README.md
  docs/PROTOCOL-project1-wikitext-tl39.md    # this file
  docs/run-cards/                            # one markdown per run
  docs/data-cards/                           # one markdown per corpus snapshot
  scripts/p1/                                # thin wrappers only
  data/raw/wikitext-tl39/                    # immutable download
  data/interim/wikitext-tl39/                # reconstructed docs, splits
  data/processed/wikitext-tl39/              # nanochat shards (copied into cache)
  artifacts/p1/<run_id>/                     # reports, samples, metrics json
  vendor/nanochat/                           # git clone, detached HEAD at pin
```

Runtime cache MUST be isolated:

```bash
export NANOCHAT_BASE_DIR="$PWD/data/cache/p1-${RUN_ID}"
```

MUST NOT use the default `~/.cache/nanochat` if that directory already contains ClimbMix shards.

---

## 6. Legal, ethical, and attribution requirements

### 6.1 License stack

| Artifact | License / terms | Obligation |
|---|---|---|
| Tagalog Wikipedia text | CC BY-SA 3.0 (or the dump’s stated version) | Attribution; share-alike if you redistribute a *corpus* derived from it |
| WikiText-TL-39 compilation | Cite Cruz & Cheng 2019 | Cite the paper in every report |
| HF mirror | Hugging Face dataset terms + upstream | Record dataset id and revision |
| nanochat code | MIT | Retain copyright notice in the clone |
| Trained weights | Inherit SA obligations if you release a corpus; weights trained on SA text are commonly released with a model card that attributes Wikipedia and the paper. Do not claim the weights are “unrestricted commercial” without legal review. |

### 6.2 Attribution block (MUST appear in the model card)

> This model was pretrained on WikiText-TL-39 (Cruz & Cheng, 2019), a Tagalog Wikipedia-derived language-modeling corpus. Wikipedia text is available under the Creative Commons Attribution-ShareAlike License. This is not an official De La Salle University, Cruz, or Cheng release.

### 6.3 Prohibited data uses

- MUST NOT scrape additional Wikipedia during P1.0.  
- MUST NOT add news, tweets, or OSCAR “to help the loss.” That is a different project.  
- MUST NOT include labeled dengue/hate-speech/NLI text in pretraining.  
- MUST NOT deanonymize or attempt to recover Wikipedia editor identities.

### 6.4 Dual use

A small Tagalog Wikipedia LM is not a high-risk system. Still MUST NOT fine-tune it in this protocol for harassment, doxxing, or political microtargeting. Those uses are out of scope.

---

## 7. Environment lock (Gate A)

### 7.1 Create the experiment identity

```bash
export P1_ROOT="/Users/paulpajo/Projects/nanochat-filipino"
cd "$P1_ROOT"
export RUN_ID="p1-$(date -u +%Y%m%dT%H%M%SZ)-$(git rev-parse --short HEAD 2>/dev/null || echo nogit)"
export NANOCHAT_BASE_DIR="$P1_ROOT/data/cache/${RUN_ID}"
mkdir -p "$NANOCHAT_BASE_DIR" \
  data/raw/wikitext-tl39 \
  data/interim/wikitext-tl39 \
  data/processed/wikitext-tl39 \
  docs/run-cards \
  docs/data-cards \
  artifacts/p1/${RUN_ID} \
  vendor
echo "$RUN_ID" | tee "artifacts/p1/${RUN_ID}/RUN_ID.txt"
```

### 7.2 Clone and pin nanochat

```bash
git clone https://github.com/karpathy/nanochat.git vendor/nanochat
cd vendor/nanochat
git rev-parse HEAD | tee "$P1_ROOT/artifacts/p1/${RUN_ID}/nanochat.sha"
# Record this SHA in the run card. Do not `git pull` again for this RUN_ID.
uv sync --extra cpu          # C0
# uv sync --extra gpu        # C1–C3
source .venv/bin/activate
python -c "import torch, nanochat; print(torch.__version__)"
```

MUST copy `vendor/nanochat/uv.lock` to `artifacts/p1/${RUN_ID}/uv.lock`.

### 7.3 Isolation test (acceptance)

```bash
# MUST print the isolated path, not ~/.cache/nanochat
python -c "from nanochat.common import get_base_dir; print(get_base_dir())"
```

If this prints `~/.cache/nanochat`, `NANOCHAT_BASE_DIR` was not exported. Stop.

### 7.4 MUST NOT download ClimbMix

Do **not** run `python -m nanochat.dataset -n 8` for P1.0. That command pulls English ClimbMix into the cache and will contaminate `list_parquet_files()` if your Tagalog shards share the default directory.

**Acceptance:** `ls "$NANOCHAT_BASE_DIR"` contains no `base_data_climbmix/` and no `base_data/` from a previous English run.

---

## 8. Data acquisition and integrity (Gate B)

### 8.1 Download the parquet (preferred)

```bash
cd "$P1_ROOT"
huggingface-cli download linkanjarad/Wikitext-TL39 \
  data/train.parquet \
  --repo-type dataset \
  --local-dir data/raw/wikitext-tl39
```

Alternative (no CLI):

```bash
curl -L --fail --retry 5 \
  -o data/raw/wikitext-tl39/train.parquet \
  https://huggingface.co/datasets/linkanjarad/Wikitext-TL39/resolve/main/data/train.parquet
```

### 8.2 Record provenance

Write `docs/data-cards/wikitext-tl39-${RUN_ID}.md` containing:

- Dataset id: `linkanjarad/Wikitext-TL39`  
- Hugging Face revision SHA (from `huggingface-cli download` output or the repo `refs/main`)  
- Download UTC timestamp  
- File size in bytes (`stat`)  
- SHA256:

```bash
shasum -a 256 data/raw/wikitext-tl39/train.parquet \
  | tee artifacts/p1/${RUN_ID}/train.parquet.sha256
```

- HTTP status of the legacy S3 URL (expected 404):

```bash
curl -sI https://s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/wikitext-tl-39/wikitext-tl-39.zip | head
```

### 8.3 Integrity acceptance tests

| ID | Test | Pass condition |
|---|---|---|
| B1 | File exists | `data/raw/wikitext-tl39/train.parquet` |
| B2 | Magic | First four bytes consistent with parquet (`PAR1`) |
| B3 | Size | Within 10% of 119 MB (card-reported). If not, stop and inspect. |
| B4 | Rows | `pyarrow.parquet.read_metadata(...).num_rows` recorded. Expected ~1.52e6. |
| B5 | Schema | A column named `text` of type string. No other required columns. |
| B6 | Empty rate | Fraction of rows with `strip()==""` < 5%. |
| B7 | Language sniff | Of 1,000 random non-empty rows, ≥ 80% contain at least one common Tagalog function word (`ang`, `ng`, `sa`, `mga`, `na`, `ay`) **or** a `= Title =` header. This is a sanity sniff, not LID. |
| B8 | Moses residue | Of 1,000 rows, count of `@-@` and `@,@`. If > 10% of rows contain them, the mirror is Moses-tokenized (expected). |

### 8.4 Optional SEACrowd audit (SHOULD)

```python
from datasets import load_dataset
sea = load_dataset("SEACrowd/wikitext_tl_39", trust_remote_code=True)
print(sea)
```

Compare row counts and a 20-line sample overlap (exact string match rate). Record: “mirror ⊆ SEACrowd / SEACrowd ⊆ mirror / incomparable.” Do not fail Gate B if SEACrowd requires extra trust flags and the parquet already passed B1–B8.

---

## 9. Corpus audit and descriptive statistics (Gate C)

### 9.1 Row-level census (MUST)

Compute and write to `artifacts/p1/${RUN_ID}/corpus_row_stats.json`:

- \(N_{\text{line}}\), empty lines, min/median/mean/p95/max line length in chars  
- Unicode category histogram (letters, marks, numbers, punctuation, separators)  
- Fraction of lines matching `^= [^=].* =$` (WikiText article headers)  
- Fraction containing Latin letters vs. digits vs. `@-@`  
- Top 50 whitespace tokens (Moses view)  
- SHA256 of the concatenation of the first and last 100 non-empty lines (canary)

### 9.2 Document reconstruction (MUST)

Deterministic; no mid-gate human choice of unit. Full algorithm: [EXECUTION-CLARIFICATIONS-p1.1.md](EXECUTION-CLARIFICATIONS-p1.1.md) §7.

A row is a header iff the line matches one compiled regex:

```text
(?m)^= [^=\n][^\n]*? =$
```

Walk rows in **file order**. A matched heading starts a new article (heading kept). Following lines concatenate until the next heading. Rows before the first heading form a documented preamble bucket. Article id = `sha256(utf-8 canonical_article_text)`.

**Acceptance C1 / automatic fallback:** Use reconstructed articles only if **all** §7.3 invariants hold (count ≥ 1,000 nonempty candidates; every nonempty row assigned to exactly one article or the preamble; no empty candidate after LF-normalize; stable SHA-256 ids; audit statistics present). If any invariant fails, do not inspect examples: automatically use `reconstructed_row_70_15_15` (row id = `sha256(utf-8 text)`, lex sort, 70/15/15). Do not mix article ids and row ids in one split.

### 9.3 Moses token census (MUST)

On reconstructed documents, whitespace-split and count tokens. Compare to Table 1. Write `T_moses_total`. A factor-of-two disagreement is a **warning**, not an automatic fail (mirror may include a different subset). A factor-of-ten disagreement is a **fail**.

### 9.4 Canonical text policy (P1.1 default = preserve source)

P1.0 detokenization is **revoked** for the confirmatory run. The canonical variant answers: what happens when nanochat is applied to the public mirror as released?

Canonical function (only):

1. Reject nulls.  
2. Convert CRLF/CR to LF.  
3. Optionally strip leading/trailing whitespace of the whole row if and only if recorded.  
4. Preserve internal whitespace, casing, punctuation, Moses `@-@` / `@,@` markers, markup remnants.  
5. Reject the row only if it is empty after that.  
6. Do **not** lowercase, detokenize, NFC-force, language-filter, or deduplicate in canonical.

Save `documents_canonical.jsonl`. A **clean ablation** (NFC, HTML entities, exact dedup, optional MinHash) MAY be packaged separately and MUST NOT overwrite canonical. Moses detokenize, if ever run, is exploratory (new run id), not P1.1 confirmatory.

Each line of the jsonl:

```json
{"doc_id": "...", "title": "...", "text": "...", "n_chars": 0, "n_moses_tokens": 0}
```

### 9.5 Length filters (MUST, conservative)

Drop a document if and only if:

- `n_chars < 40` (stubs / empty after detok), or  
- `n_chars > 200_000` (likely extraction error; log the title).

Do **not** drop short articles merely because they are short. Tagalog Wikipedia has many stubs; they are in-domain.

Record drop counts. If drops exceed 5% of documents, stop and inspect.

---

## 10. Split construction (Gate D)

### 10.1 Unit of split

Default unit is the **article**. If any §7.3 reconstruction invariant fails, the unit is the **parquet row** (automatic fallback; see §9.2). No mid-gate choice.

### 10.2 Algorithm (MUST)

1. Sort documents by `doc_id` (stable).  
2. **First** search the HF repo file tree, dataset card history, Filipino-Text-Benchmarks, and paper links for original train/val/test files. If found and statistics agree with Cruz & Cheng Table 1, use those hashes and set `historical_split_recovered: true`.  
3. If not recovered: identity = `sha256(canonical_utf8)`. Sort identities lexicographically. Assign first 70% train, next 15% val, last 15% test. Seed 42 is used only if a documented shuffle is substituted; the default lex-hash order needs no seed.  
4. **Split unit / label:** `original_2019` if recovered; else `reconstructed_article_70_15_15` if every §7.3 invariant holds; else automatic `reconstructed_row_70_15_15`. That label belongs in every title, manifest, table, and caption.  
5. Write `splits.json` / `split_manifest.json` with `historical_split_recovered`, unit, and assignment rule.

6. Write three jsonl files under `data/interim/wikitext-tl39/`.

This is a **hash split**, not a random shuffle in memory. It is deterministic across machines.

### 10.3 Leakage tests (acceptance)

| ID | Test | Pass |
|---|---|---|
| D1 | Set intersection train∩val, train∩test, val∩test | empty |
| D2 | Duplicate `sha256(text)` across splits | 0 (exact-document dupes). Near-dups MAY exist (Wikipedia boilerplate); record MinHash 5-gram Jaccard > 0.8 pairs if any. |
| D3 | Title overlap | 0 identical titles across splits |
| D4 | Ratio | train docs in [65%, 75%]; val, test in [12%, 18%] |
| D5 | Char ratio | same bands as D4 for characters, not only docs (avoid one split eating all long articles) |

If D5 fails (e.g. test is 5% of characters), re-split using stratified bins on `log(n_chars)` with the same seed (document-level, three length tertiles, 70/15/15 inside each tertile). Record “stratified hash split” in the run card.

### 10.4 Frozen test rule

After Gate D passes, **chmod a-w** the test jsonl (or set an ACL). Test may be read by the final eval script only.

### 10.5 Tokenizer / train contamination rule

Val and test documents MUST NOT be written into tokenizer training iterators or into any parquet except the dedicated val shard and a held-out test shard that nanochat never trains on.

nanochat’s loader only knows `train` (all but last parquet) and `val` (last parquet). **Test is extra.** Keep test shards **outside** `DATA_DIR` used by `base_train`. Evaluate test with a one-off BPB script that points at the test jsonl (§16.3).

### 10.6 Optional: attempt to recover the 2019 split

If SEACrowd or another source exposes official split labels, compute Cohen’s κ / agreement with the hash split. Report it. Do **not** switch to the official split mid-protocol unless you start a new `RUN_ID` labeled `P1.0-officialsplit`.

---

## 11. Shard packaging for nanochat (Gate E)

### 11.1 Why shards, not a .txt

`scripts.tok_train` and `scripts.base_train` iterate `parquets_iter_batched()`, which reads a `text` column from parquet files in `list_parquet_files()`. A single `.txt` is not native. The official packer is `dev/repackage_data_reference.py`:

- column: `text`  
- compression: zstd level 3  
- `row_group_size = 1024`  
- target ~250,000,000 characters per shard (ClimbMix scale)

WikiText-TL-39 is **smaller than one ClimbMix shard**. Using the 250M-character target would produce a single file, and nanochat would then treat that entire file as **validation** (last file = val) and train on **nothing**.

### 11.2 P1.0 sharding rule (MUST)

Create **at least three** parquet files in the training data directory:

| Filename | Content | Role |
|---|---|---|
| `shard_00000.parquet` | first ~half of train docs (by `doc_id` sort, then packed) | train |
| `shard_00001.parquet` | remaining train docs | train |
| `shard_00002.parquet` | **all val docs** | val (MUST be last lexicographically) |

If train characters exceed 250M (unlikely), add more `shard_0000k.parquet` files. Val MUST remain the last name.

**Test:** `shard_test.parquet` lives in `data/processed/wikitext-tl39/test/` and is **never** copied into the nanochat data dir.

### 11.3 Document packing

Each parquet row is **one document** (`text` = full article), not one original line. This preserves long-range context and matches nanochat’s “document” assumption (`doc_cap` in tokenizer training).

If a document exceeds 50,000 characters, split into non-overlapping chunks of 10,000 characters on newline boundaries. Chunks inherit `doc_id` with suffix `#k`. All chunks of a document stay in the same split.

### 11.4 Output directory wiring

nanochat 2026 default data dir is `$NANOCHAT_BASE_DIR/base_data_climbmix`. P1.0 MUST either:

**Option A (P1.1 publication path):** one-line hook in `nanochat/dataset.py` on commit `92d63d4e…`:

```python
DATA_DIR = os.environ.get(
    "NANOCHAT_DATA_DIR",
    os.path.join(base_dir, "base_data_climbmix"),
)
```

Preserve the ClimbMix default. Do not remove the downloader. Patch commit message: `project1: add explicit NANOCHAT_DATA_DIR override for custom corpora`. Add a unit test: unset env → default path; set env → Project 1 dir; last file is val.

**Option B (smoke only):** symlink shards into `$NANOCHAT_BASE_DIR/base_data_climbmix/` with no source edit. Less transparent. Not the preferred publication configuration.

MUST NOT run `python -m nanochat.dataset`. Export both `NANOCHAT_BASE_DIR` and `NANOCHAT_DATA_DIR` before every command. Preflight-print resolved base, tokenizer, and data dirs.

### 11.5 Packer implementation notes

Follow `repackage_data_reference.py`:

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.Table.from_pydict({"text": docs})
pq.write_table(
    table,
    path,
    row_group_size=1024,
    use_dictionary=False,
    compression="zstd",
    compression_level=3,
    write_statistics=False,
)
```

Pad the last row group by repeating empty strings **only if** you must hit a multiple of 1024 **and** you filter empty strings at load time. Prefer **not** padding; nanochat iterates row groups as-is.

### 11.6 Acceptance

| ID | Test | Pass |
|---|---|---|
| E1 | File names | `shard_00000.parquet`, `shard_00001.parquet`, `shard_00002.parquet` only in the data dir |
| E2 | Last file = val | Every `doc_id` in shard 2 is in the val set; none in train |
| E3 | Train files ⊆ train | 0 val/test docs in shards 0–1 |
| E4 | Round-trip | Read back 20 random docs; exact string match |
| E5 | Isolation | `python -m nanochat.dataset` was never run for this `NANOCHAT_BASE_DIR` |

---

## 12. Tokenizer training and evaluation (Gate F)

### 12.1 Why train a new tokenizer

The stock nanochat tokenizer is trained on ClimbMix English. Using it for Tagalog wastes the vocabulary on English words and inflates BPB. P1.0 trains `scripts.tok_train` on **Tagalog training documents only**.

### 12.2 Command (native)

From `vendor/nanochat` with `NANOCHAT_BASE_DIR` set and shards in place:

```bash
# WikiText-TL-39 is << 2B characters. Use all train characters.
# doc-cap 10000 matches nanochat default and our chunk size.
python -m scripts.tok_train \
  --max-chars 400000000 \
  --doc-cap 10000 \
  --vocab-size 32768
python -m scripts.tok_eval
```

`--max-chars 400000000` is an upper bound; the iterator stops at end of train shards.

### 12.3 Vocabulary choice

| Vocab | When |
|---|---|
| **32768 (default)** | Primary. Native nanochat, comparable to other nanochat papers. |
| 8192 | Optional ablation if embeddings dominate \(P\) and d4/d6 underfit the residual stream. New `RUN_ID`. |
| 279153 | MUST NOT. That is the 2019 word vocabulary, not BPE, and will break nanochat’s assumed vocab. |

### 12.4 Tokenizer leakage control

`parquets_iter_batched(split="train")` already skips the last shard. Confirm in a dry-run print that the last document titles seen by `tok_train` are train titles.

**H2 measurement (SHOULD, one extra run):** retrain a tokenizer on train+val+test (temporarily move test into a non-last shard — this is a *labeled ablation*, new `RUN_ID`), then evaluate BPB of a frozen d4 model? Simpler: compare fertility (tokens/word) of the train-only tokenizer vs. an all-data tokenizer on the test set. Report fertility gap. Do not use the all-data tokenizer for primary LM training.

### 12.5 Tokenizer metrics (MUST write `tokenizer_eval.json`)

On train / val / test (documents, not leaked into training of the tokenizer except train):

- bytes / token  
- chars / token  
- tokens / Moses-token  
- % of tokens that are single-byte  
- % of test characters that round-trip (`decode(encode(x)) == x`) — MUST be 100% for NFC text  
- fertility on a 20-document Tagalog news sample **held out from Wikipedia** is out of scope (would be a new corpus)

### 12.6 Sanity strings (MUST)

Encode/decode:

- `Ang mabilis na kayumangging fox ay tumalon sa tamad na aso.`  
- `Filipinas` / `Pilipinas`  
- `ng` `mga` `sa` `ang`  
- A line containing `ñ` and `ng`  
- The Moses form `artipisyal na itlog @-@ ng bayag` vs. detok form  

Record token ids. If `ñ` explodes into many tokens, that is acceptable but MUST be noted.

### 12.7 Artifacts

`$NANOCHAT_BASE_DIR/tokenizer/` MUST contain the official files (`tokenizer.pkl` / `tokenizer.json` as produced by this commit, plus `token_bytes.pt`). Copy that directory to `artifacts/p1/${RUN_ID}/tokenizer/`.

---

## 13. Compute-optimal depth selection (desk calculation, Gate G)

### 13.1 Measure \(T_{\text{BPE}}\) before choosing \(D\)

```text
T_train = sum(len(tokenizer.encode(doc)) for doc in train_docs)
```

This is the **unique training token inventory** (source BPE, no BOS in the sum, no packer crop). One epoch means \(T_{\text{seen}} = T_{\text{train}}\). Exact definition: [EXECUTION-CLARIFICATIONS-p1.1.md](EXECUTION-CLARIFICATIONS-p1.1.md) §4.1.

### 13.2 Parameter estimate

nanochat sets `model_dim = round_up(depth * 64, 128)` and `n_head = model_dim / 128`.

| \(D\) | dim | rough \(P\) (32k vocab, embeddings dominate at small \(D\)) |
|---:|---:|---|
| 4 | 256 | ~20M (mostly embeddings) |
| 6 | 384 | ~30M |
| 7 | 448 → 512 | ~40M |
| 8 | 512 | ~45M |
| 12 | 768 | ~90M+ |

Exact \(P\) MUST come from the trainer log. Record **both** `P_total` (all trainable) and `P_scaling` (horizon math). Use `R_scaling = D_3x / P_scaling`. Do not mix the two. The table is for planning only.

### 13.3 Decision rule (MUST)

Let \(T = T_{\text{train}}\).

P1.1 does **not** pick depth by a one-epoch Chinchilla cut. Depths are predeclared:

- Smoke: d4  
- Pilot: d8, d12 at `D_1x` then `D_3x`  
- Production (confirmatory fixed-data): **d8, d12, d16, d20** at `D_3x`  
- Optional: d24; native-horizon copies of the same depths (compatibility family, not equal-exposure)

After tokenizer training, measure `T_train` (BPE, pre-crop). Set `D_1x = T_train`, `D_3x = 3 * T_train`, `D_10x = 10 * T_train`. Primary budget is `D_3x`. For each depth:

```text
N_iterations = ceil(D_budget / B_total)
D_actual = N_iterations * B_total
R_scaling = D_budget / P_scaling(depth)   # keep this POSITIVE
```

Pass `--num-iterations`, `--total-batch-size`, and a **positive** `--target-param-data-ratio=R_scaling`. MUST NOT pass `--target-param-data-ratio=-1` (current `base_train.py` still uses the ratio in scaling math).

Report both source-corpus tokens and model-visible tokens. The BOS best-fit packer can crop (~35% at T=2048 on the English default); methods must say so.

### 13.4 Batch and eval tokens (MUST override defaults)

Defaults assume ClimbMix-scale data:

- `--eval-tokens` default `80 * 524288` ≈ 42M tokens — can exceed the entire Tagalog val set.  
- `--total-batch-size` default is huge relative to 39M tokens.

P1.0 flags:

```text
--eval-tokens     = min(262144, 0.5 * T_val)   # at least 8192 if T_val allows
--device-batch-size = 8 or lower until VRAM fits
--max-seq-len     = 2048 confirmatory; reduce device-batch-size on small VRAM, not T, unless a new run id
--core-metric-every = -1
--sample-every    = 200
--eval-every      = 50
--save-every      = 200
--warmup-steps    = min(40, 5% of iterations)
```

Set `--num-iterations` explicitly:

```text
tokens_per_step ≈ total_batch_size   # as resolved by nanochat
num_iterations_one_epoch = ceil(T_train / tokens_per_step)
```

Do **not** rely on `--target-param-data-ratio` alone: that ratio will demand more tokens than exist and will **repeat the corpus silently**. If you use it, you MUST log the implied epoch count.

### 13.5 Sequence length

Confirmatory `--max-seq-len=2048` (nanochat native T). The BOS best-fit packer may crop long documents; report source tokens vs model-visible tokens. A 1024 run is a hardware/ablation variant with a new run id.

---

## 14. Smoke test (Gate H) — d4, tiny

### 14.1 Purpose

Prove the wiring: isolated cache, Tagalog shards, Tagalog tokenizer, finite loss, checkpoint write. **Not** a result.

### 14.2 Command (single process; omit torchrun on one GPU)

```bash
cd "$P1_ROOT/vendor/nanochat"
export NANOCHAT_BASE_DIR="$P1_ROOT/data/cache/${RUN_ID}"
export OMP_NUM_THREADS=1
export WANDB_RUN=dummy

python -m scripts.base_train \
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
  --model-tag="p1-smoke-d4" \
  --run=dummy
```

On 8 GPUs, prefix `torchrun --standalone --nproc_per_node=8` and raise `--device-batch-size` only if VRAM allows.

### 14.3 Acceptance

| ID | Test | Pass |
|---|---|---|
| H1 | Loss finite | train loss is finite at step 30 |
| H2 | Loss moved | train loss at step 30 < train loss at step 1 |
| H3 | Checkpoint | `base_checkpoints/p1-smoke-d4` (or commit-typical path) exists |
| H4 | Language | a sample contains at least one Tagalog function word, **or** is garbage (allowed at 30 steps) but is **not** fluent English Wikipedia boilerplate from ClimbMix |
| H5 | No CORE download | no eval_bundle English files fetched, or fetch ignored |

If H4 produces fluent English about “the United States Congress,” the data dir is wrong. Stop. Destroy that cache.

---

## 15. Primary pretraining (Gate I)

### 15.1 Run matrix (pre-registered)

All runs share: same shards, same tokenizer, same `SPLIT_SEED`, same nanochat commit, `core-metric-every=-1`.

| Run name | \(D\) | Epochs | Seed | Status |
|---|---:|---:|---:|---|
| `p1-d4-smoke` | 4 | 20–100 steps | 42 | pipeline only |
| `p1-fixed-d8-1x` / `3x` | 8 | 1× then 3× T_train | 42 + 2 extra if feasible | pilot |
| `p1-fixed-d12-1x` / `3x` | 12 | 1× then 3× | 42 + 2 extra if feasible | pilot / baseline |
| `p1-fixed-d{8,12,16,20}-3x` | 8–20 | **3× T_train (primary)** | 1–2 | confirmatory |
| `p1-fixed-d*-10x` | winner or all | 10× | 1 | sensitivity, exploratory unless pre-declared |
| `p1-native-d{8,12,16,20}` | 8–20 | nanochat ratio 12 | 1 | compatibility; not equal-exposure |
| `p1-fixed-d24-3x` | 24 | 3× | 1 | optional |

Primary table = fixed-data `D_3x` depths 8/12/16/20. Do not rank native-horizon runs as if they saw the same tokens.

### 15.2 Launch template

```bash
python -m scripts.base_train \
  --depth=${D} \
  --max-seq-len=2048 \
  --device-batch-size=${B} \
  --num-iterations=${ITERS_FOR_EPOCHS} \
  --eval-tokens=${EVAL_TOKENS} \
  --eval-every=50 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --save-every=200 \
  --warmup-steps=${WARMUP} \
  --model-tag="${RUN_NAME}" \
  --run="${RUN_NAME}"
```

On C2/C3, `--fp8` MAY be enabled **only** on Hopper (H100+) as nanochat documents. A100 uses bf16 default. Record dtype.

### 15.3 Logging (MUST)

Every 50 steps, persist:

- step, wall time, tokens seen, epoch index = `tokens_seen / T_train`  
- train NLL, train BPB  
- val BPB (when eval runs)  
- tok/s, MFU, VRAM  
- learning rates (embedding, matrix, unembedding)

Prefer wandb **and** a local `metrics.jsonl` (wandb is not an archive).

### 15.4 Samples during training

Use three **fixed** prompts (do not cherry-pick later):

1. `Ang Pilipinas ay`  
2. `Noong ika-`  
3. `= Kasaysayan =`

Save samples to `artifacts/p1/${RUN_ID}/samples/step_XXXX.txt`. These are qualitative.

### 15.5 Early stopping (one-epoch runs)

Do not early-stop a one-epoch run except for NaN. For multi-epoch runs, stop if val BPB at epoch \(k\) > val BPB at epoch \(k-1\) + 0.02.

### 15.6 Checkpoint policy

**Confirmatory evaluation uses the final `D_3x` checkpoint only.** Do not select a mid-run val-best step. Mid-run val curves may be logged; they MUST NOT choose the checkpoint or `D*`. `D*` is the exact numerical minimum of the four **final** `val_bpb_full` values (`selection_rule = exact_minimum_final_val_bpb_full`). Gaps `< 0.01` BPB govern interpretation, not a second selection rule. See [EXECUTION-CLARIFICATIONS-p1.1.md](EXECUTION-CLARIFICATIONS-p1.1.md) §5.

Keep:

- last (this is the confirmatory checkpoint)  
- step 0 (optional, for the untrained baseline)

A mid-run “best val” file, if the trainer writes one, is diagnostic only. Delete intermediate checkpoints if disk is tight, after copying last (and optional step 0) to `artifacts/`.

---

## 16. Evaluation protocol (Gate J)

### 16.1 What `scripts.base_eval` is allowed to contribute

Official `base_eval` computes CORE, BPB, and samples. For P1.0:

- Use it for **BPB and samples** if the commit allows skipping CORE.  
- Pass `--core-metric-every=-1` at train time. If `base_eval` still runs CORE, ignore those numbers in the primary table.  
- `--device-batch-size` as in training.

### 16.2 Validation BPB (primary)

Compute BPB on the **val parquet** (last shard) with the official `loss_eval` path when possible. If `eval-tokens` truncated val, run a **full-val** BPB once at the end (all val tokens, no sampling).

Report:

- `val_bpb_full`  
- `val_nll_mean`  
- `val_bytes`  
- `val_tokens`

### 16.3 Test BPB (once)

After `D*` is frozen (lowest **final** `val_bpb_full` among the four depths):

1. Load tokenizer + that depth’s **final** `D_3x` checkpoint.  
2. Iterate test documents from `data/processed/wikitext-tl39/test/`.  
3. Compute BPB identically to val (same context length, same stride).  
4. Write `test_bpb` once. MUST NOT tune after this.

**Stride:** non-overlapping blocks of `max_seq_len`, or overlapping with stride `max_seq_len // 2` if the last block is short. Pick one, write it down, use it for val and test.

### 16.4 Random-init baseline (MUST, once per depth family)

Evaluate an untrained model of the same architecture on val. H1 requires `trained val_bpb < random val_bpb`. Random BPB should be near \(\log_2(\text{vocab}) / \text{bytes_per_token}\).

### 16.5 Byte unigram baseline (MUST)

Fitted on train canonical UTF-8 bytes only. Laplace add-1 over 256 bytes:

```text
p(b) = (c[b] + 1) / (N + 256)
BPB_unigram = - (1 / (M * ln 2)) * sum_i ln p(y_i)
```

No backoff, no skipping rare bytes, no excluding whitespace. Empty train (`N = 0`) is a gate failure. Write `c[0:256]`, `N`, smoothing constant, held-out byte count, NLL in nats, and `val_bpb_unigram`. The trained model MUST be strictly below this and below the untrained same-depth model, or that depth fails the baseline check (it may remain in the table with a fail flag; it cannot be `D*` if it fails).

### 16.6 Compression / bits comparison (SHOULD)

gzip -9 the val text and compute bits per byte of the compressor. An LM that cannot beat gzip on in-domain Wikipedia is weak; report the comparison without overclaiming (gzip is not a causal LM).

### 16.7 Qualitative protocol (fixed)

For each of the three prompts in §15.4, generate \(n=5\) continuations at temperature 0.8, top-p 0.95, max 100 tokens, two seeds (0 and 1). Do not filter. A native speaker SHOULD rate 15 random continuations on a 1–5 fluency scale. If no rater is available, say so; do not invent scores.

### 16.8 Forbidden tables

MUST NOT publish a leaderboard row that implies Tagalog WikiText d8 is “better than GPT-2” because CORE is lower or higher. Different language, different data, different construct.

---

## 17. Optional light probe (not required for P1.0 success)

A **frozen-encoder linear probe** on hate-speech or dengue is Protocol P9/P8. If you attach it here, label the section “exploratory, not P1.0.” MUST use the published HF splits and MUST NOT back-propagate into the base except as a separately named run.

Recommended order after P1.0 closes: P9 (binary) then P8 (multi-label).

---

## 18. Reporting (Gate K)

### 18.1 Run card (one per `RUN_ID`)

Copy this template to `docs/run-cards/${RUN_ID}.md`:

```markdown
# Run card ${RUN_ID}

- Protocol: P1.0
- Date (UTC):
- Operator:
- Hardware class / `nvidia-smi`:
- nanochat commit:
- NANOCHAT_BASE_DIR:
- Parquet SHA256:
- Split seed:
- Detokenize: yes/no
- Vocab size:
- Depth / dim / heads / P:
- max_seq_len / device_batch / total_batch / iterations / epochs:
- T_train / T_val / T_test (BPE):
- rho (tokens seen / P):
- dtype / fp8:
- val_bpb_full / test_bpb:
- random_val_bpb / byte_unigram_val_bpb:
- Deviations from P1.0:
- Pass/fail gates: A B C D E F G H I J
```

### 18.2 Primary result table (paper)

Columns: run name, \(D\), \(P\), \(T_{\text{seen}}\), \(\rho\), epochs, `val_bpb`, `test_bpb`, hours, GPU.

One footnote: tokenizer train-only, document hash split 70/15/15, detokenized Moses, nanochat commit `...`.

### 18.3 nanochat report

```bash
python -m nanochat.report generate
```

Copy `report.md` into `artifacts/p1/${RUN_ID}/`. Edit only to **strike** CORE numbers from the abstract claim.

### 18.4 Model card (if weights are released)

Sections: intended use (research LM for Tagalog Wikipedia-style text), out-of-scope (chat, safety, official government use), data, eval, carbon/GPU hours, citations (§23).

---

## 19. Statistical analysis plan

1. Primary comparison: `val_bpb` across depths at one epoch, seed 0. Exploratory unless ≥ 3 seeds.  
2. Secondary: test BPB of the val-best run only.  
3. H4: paired comparison of e1 vs e2 at \(D*\).  
4. No p-hacking: if you add d5 or vocab 16k after seeing results, mark **post hoc**.  
5. Confidence: with one seed, report point estimates only. With ≥ 3 seeds, report mean ± sample standard deviation.

---

## 20. Pre-registered ablations (separate RUN_IDs)

| ID | Change | Purpose |
|---|---|---|
| A1 | Moses-as-is (no detok) | H on marker waste |
| A2 | Tokenizer trained on all splits | H2 leakage |
| A3 | Line-level random split | Show document split matters (expected worse leakage, *better* BPB — interpret as contamination) |
| A4 | Official English nanochat tokenizer, Tagalog data | Show custom tokenizer value |
| A5 | `max_seq_len=2048` at \(D*\) | Context ablation |
| A6 | Vocab 8192 | Embedding-dominated \(P\) |
| A7 | Stratified vs plain hash split | Only if D5 failed |

A3 is ethically required if a reviewer asks “why not split lines?” Do it once at d4.

---

## 21. Failure modes and recovery

| Symptom | Likely cause | Action |
|---|---|---|
| Fluent English samples | ClimbMix still in data dir | Wipe `NANOCHAT_BASE_DIR`, restart from §7 |
| Train on 0 documents | Only one parquet; last=val | Add ≥ 2 train shards (§11) |
| OOM | `device-batch-size` / seq len | Halve batch; do not change depth mid-run (new RUN_ID) |
| val_bpb ≪ train_bpb | Val shard leaked into train or val is tiny/easy | Re-run D2, E2 |
| val_bpb ≈ random | LR, broken labels, empty texts | Check mean `len(text)`, LR, dtype |
| tok_train assert fail on English test string | Harmless if Unicode Tagalog round-trips; still run Tagalog round-trip |
| `get_base_dir()` wrong | Export not visible to torchrun | `torchrun` does not always inherit; use a wrapper script that exports |
| HF download checksum mismatch | Partial file | Delete and re-download |
| 1.52M rows but 200 documents | Header regex wrong | Fix §9.2; do not train |

---

## 22. Timeline (elapsed work, not GPU hours)

| Day | Gates | Deliverable |
|---|---|---|
| 0 | A–B | Pinned nanochat, parquet SHA256, data card |
| 1 | C–E | Documents, splits, shards, leakage report |
| 2 | F–H | Tokenizer metrics, d4 smoke |
| 3–4 | I (d4, d6) | Primary one-epoch runs |
| 5 | I (d8/d12 if allowed), J | Full val/test BPB, baselines |
| 6 | K, A1 or A3 | Report + one ablation |
| 7 | Buffer | Deviation cleanup |

GPU wall time on C1 for d6 one epoch should be hours, not days, given \(T \sim 10^7\)–\(10^8\). If it is days, `num_iterations` is wrong (ClimbMix-scale). Stop and recompute §13.

---

## 23. Citations (MUST)

```bibtex
@article{cruz2019evaluating,
  title={Evaluating Language Model Finetuning Techniques for Low-resource Languages},
  author={Cruz, Jan Christian Blaise and Cheng, Charibeth},
  journal={arXiv preprint arXiv:1907.00409},
  year={2019}
}

@misc{nanochat,
  author = {Andrej Karpathy},
  title = {nanochat: The best ChatGPT that \$100 can buy},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/karpathy/nanochat}
}

@inproceedings{merity2016wikitext,
  title={Pointer Sentinel Mixture Models},
  author={Merity, Stephen and Xiong, Caiming and Bradbury, James and Socher, Richard},
  booktitle={ICLR},
  year={2017}
}

@inproceedings{koehn2007moses,
  title={Moses: Open Source Toolkit for Statistical Machine Translation},
  author={Koehn, Philipp and others},
  booktitle={ACL Demo},
  year={2007}
}

@article{hoffmann2022chinchilla,
  title={Training Compute-Optimal Large Language Models},
  author={Hoffmann, Jordan and others},
  journal={arXiv preprint arXiv:2203.15556},
  year={2022}
}
```

Also cite Wikimedia / Tagalog Wikipedia and the Hugging Face dataset page for the mirror revision.

---

## 24. Reproducibility checklist (Gate L)

Print this, tick it, photograph or commit the ticks.

- [ ] nanochat commit recorded; working tree clean or diff saved  
- [ ] `NANOCHAT_BASE_DIR` isolated; no ClimbMix  
- [ ] Parquet SHA256 recorded  
- [ ] S3 zip not used  
- [ ] Document reconstruction count recorded  
- [ ] Detokenization on/off recorded  
- [ ] Hash split seed recorded; intersections empty  
- [ ] Test jsonl write-protected  
- [ ] ≥ 3 shards; last = val; test outside train dir  
- [ ] Tokenizer train-only  
- [ ] `token_bytes.pt` present  
- [ ] Depth chosen by §13, not by “speedrun.sh says d24”  
- [ ] `--core-metric-every=-1`  
- [ ] `--eval-tokens` ≤ half of val  
- [ ] `--num-iterations` matches intended epochs  
- [ ] Random-init and byte-unigram baselines  
- [ ] `val_bpb_full` and one `test_bpb`  
- [ ] Run card complete  
- [ ] Attribution block in any public model card  
- [ ] No downstream labels in pretraining  

---

## 25. Step-by-step execution list (granular)

Execute in order. Each line is one action. Do not batch-skip gates.

1. Read this protocol through §4.  
2. Fill hardware class in a blank run card.  
3. `cd` to `nanochat-filipino`.  
4. Create `RUN_ID` and directories (§7.1).  
5. Clone nanochat; record SHA (§7.2).  
6. `uv sync` for the hardware class.  
7. Export `NANOCHAT_BASE_DIR`; verify `get_base_dir()` (§7.3).  
8. Confirm ClimbMix download will not be run (§7.4).  
9. Download `linkanjarad/Wikitext-TL39` parquet (§8.1).  
10. SHA256 the parquet (§8.2).  
11. Confirm S3 404 (§8.2).  
12. Run B1–B8 (§8.3). Stop on fail.  
13. Optional SEACrowd compare (§8.4).  
14. Row census JSON (§9.1).  
15. Reconstruct documents (§9.2).  
16. Moses token census vs Table 1 (§9.3).  
17. Detokenize; write both jsonl (§9.4).  
18. Length filter; log drops (§9.5).  
19. Hash-split 70/15/15 (§10.2).  
20. Leakage tests D1–D5 (§10.3). Stratify if D5 fails.  
21. Freeze test file (§10.4).  
22. Pack train into `shard_00000` and `shard_00001` (§11).  
23. Pack val into `shard_00002` (§11).  
24. Pack test outside the train dir (§11).  
25. Symlink shards into `$NANOCHAT_BASE_DIR/base_data_climbmix/` (§11.4).  
26. E1–E5 (§11.6).  
27. `python -m scripts.tok_train` with P1 flags (§12.2).  
28. `python -m scripts.tok_eval` plus Tagalog round-trips (§12.5–12.6).  
29. Copy tokenizer to artifacts.  
30. Compute \(T_{\text{train}}\), \(T_{\text{val}}\), \(T_{\text{test}}\) (§13.1).  
31. Apply depth decision rule (§13.3). Write allowed depths on the run card.  
32. Compute `num_iterations` and `eval-tokens` (§13.4).  
33. d4 smoke, 30 steps (§14).  
34. H1–H5. Wipe cache if English ClimbMix symptoms.  
35. Launch `p1-d4-e1-s0` (§15).  
36. Launch additional one-epoch depths allowed by §13.  
37. Select \(D*\) on `val_bpb_full`.  
38. Optional e2 / seeds (§15.1).  
39. Random-init BPB (§16.4).  
40. Byte-unigram BPB (§16.5).  
41. Full val BPB (§16.2).  
42. Frozen test BPB once (§16.3).  
43. Fixed-prompt samples (§16.7).  
44. Generate nanochat report; strike CORE claims (§18.3).  
45. Complete run card and Gate L checklist (§18, §24).  
46. If releasing weights, write the model card (§6.2, §18.4).  
47. Do not start OSCAR or dengue until this checklist is green.

---

## 26. What you will claim in writing (allowed sentences)

**Allowed:**

- “We trained a nanochat depth-\(D\) GPT on a document-held-out split of the public WikiText-TL-39 mirror and obtained val/test BPB of …”  
- “A 32,768 BPE trained on the training documents compresses Tagalog Wikipedia at … bytes/token.”  
- “Under a one-epoch budget, depth \(D*\) minimized val BPB among {…}.”

**Not allowed:**

- “We reproduced Cruz & Cheng’s exact 2019 splits” (unless §10.6 succeeded).  
- “Our model is GPT-2 grade” (CORE / English).  
- “TLUnified performance” (wrong corpus).  
- “State of the art Filipino LLM.”  
- “OSCAR-quality web Tagalog.”  

---

## 27. Handoff to later projects

When Gate L is green:

| Next | Uses P1 checkpoint as | New data |
|---|---|---|
| Corpus Run 2 | same depth/tokenizer recipe, new shards | `tlwiki` or `wikimedia/wikipedia` `*.tl` |
| Corpus Run 3 | same | deduped mix of P1 + Run 2 |
| P9 hate-speech | init / frozen encoder | `jcblaise/hatespeech_filipino` |
| P8 dengue | same | `jcblaise/dengue_filipino` |
| P2 OSCAR | new protocol | gated; do not block on it |

Keep the P1 tokenizer if the new corpus is still Tagalog Wikipedia-like; retrain the tokenizer if you add CC-100/OSCAR (new protocol).

---

## 28. Appendix — Official nanochat facts this protocol depends on

Verified against `karpathy/nanochat` master as of the fetch date of this draft (August 2026). Re-verify on your pinned commit.

1. `NANOCHAT_BASE_DIR` defaults to `~/.cache/nanochat`.  
2. Pretraining data is parquet files with a `text` column.  
3. `list_parquet_files()` reads `base_data_climbmix` (legacy fallback `base_data`).  
4. `parquets_iter_batched("train")` uses **all files except the last**; `"val"` uses **only the last**.  
5. `python -m nanochat.dataset -n N` downloads ClimbMix. P1.0 never calls it.  
6. `scripts.tok_train`: `--max-chars`, `--doc-cap`, `--vocab-size` (default 32768).  
7. `scripts.base_train`: `--depth` is the complexity dial; `model_dim = depth * 64` rounded to `head_dim` (128).  
8. `--target-param-data-ratio` default 12; speedrun uses 8.  
9. `--core-metric-every` must be `-1` for P1.0.  
10. `--fp8` is H100+ only.  
11. Single GPU: omit `torchrun`; the trainer accumulates gradients.  
12. `token_bytes.pt` is required for BPB.  
13. `runs/speedrun.sh` is the English GPT-2 recipe, not the P1.0 recipe.

---

## 29. Appendix — Worked numerical example (replace with measured values)

Suppose after §9–§12 you measure:

- \(N_{\text{doc}} = 80{,}000\)  
- \(T_{\text{train}} = 3.5 \times 10^7\) BPE tokens  
- \(T_{\text{val}} = 7 \times 10^6\)  
- d4 \(P = 2.0 \times 10^7\)  
- d6 \(P = 3.0 \times 10^7\)  
- d8 \(P = 4.5 \times 10^7\)

Then \(\rho\) at one epoch is 1.75, 1.17, 0.78. **All are below 8.** The honest P1.0 move is:

- primary: d4, **2–4 epochs** so that \(\rho \approx 7\)–8, **or**  
- vocab 8192 to shrink embeddings, then re-estimate \(P\), **or**  
- report d4 one-epoch as an undertrained baseline and say so.

Do not “fix” this by downloading English data. Do not jump to d24.

*This example is illustrative. Your Gate G numbers override it.*

---

## 30. Document control

| Version | Date | Change |
|---|---|---|
| P1.0-draft | 2026-08-16 | Initial protocol: parquet mirror, S3 404, document split, shard-last-is-val, BPB primary, d24 demoted, CORE forbidden as claim |
| P1.1-draft | 2026-08-16 | Folded implementation plan: pin 92d63d4, NANOCHAT_DATA_DIR hook, canonical preserve-source, recover-then-reconstruct split, fixed-data D_3x primary, depths 8/12/16/20, never ratio=-1, BOS packing reported |
| P1.1-exec | 2026-08-16 | Pre-start execution clarifications only (not an AsPredicted edit): define `T_train`/`P_total`/`P_scaling`; evaluate final `D_3x` checkpoint; Laplace add-1 byte unigram; deterministic article reconstruction with automatic row fallback; machine-readable gate ledger |
| P1.1-exec-full | 2026-08-16 | Replaced short clarification draft with the full pre-Gate-A note; initialized ledger from `gate_ledger.template.json` (`not_started`/`pass`/`stop`/`blocked`); heading regex and multi-invariant fallback; budget and test-access stubs |

**End of protocol.** Execute §25 in order. Do not improvise a speedrun.
