# Protocol P2-EN→TL — English Retention after Tagalog Continuation (nanochat)

**Document type:** Pre-analysis execution protocol (sibling of Protocol P1.1).  
**Study short name:** P2-EN→TL  
**Hub / HF repo (after Gate I starts):** `pageman/nanochat-filipino-p2-en-then-tl`  
**Status as of 2026-08-17:** Stage-1 manuscript exists. AsPredicted **not filed**. No confirmatory English `val_bpb_full`. **Do not start Gate I until a new AsPredicted PDF exists.**  
**Authority after filing:** new AsPredicted PDF ≫ this protocol ≫ `DIRECTION-RECALIBRATION.md` ≫ `paper.tex` ≫ any chat.  
**Does not amend:** AsPredicted #306780, ResearchBox #8735, P1.1 Gate J, P1.1 `test_bpb = 1.164768`.  
**nanochat pin:** `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`  
**Hook only:** `patches/nanochat-NANOCHAT_DATA_DIR.patch` (already applied in the P1.1 vendor tree).  
**Primary DVs:** English `val_bpb_full` (forgetting) and Tagalog `val_bpb_full` (acquisition), official `evaluate_bpb`, `T=2048`, BOS-bestfit.  
**Primary contrast:** \(C_{\mathrm{en}} =\) English `val_bpb_full`(A2) − English `val_bpb_full`(A1).  
**Corresponding papers:** Merity et al. 2016 WikiText-103 (arXiv:1609.07843); Cruz & Cheng 2019 WikiText-TL-39 (arXiv:1907.00409); Karpathy nanochat; Ibrahim et al. 2024 CPT (arXiv:2403.08763); Zheng et al. 2024 language-shift CPT (arXiv:2407.02118); Bethune et al. ICML 2025 replay; Shi et al. CFT survey (arXiv:2508.00614) for **stage naming only**.

This protocol is written so that a second experimenter, given only this document, the frozen P1.1 Tagalog package, a WikiText-103 raw archive, and the pinned nanochat commit, can reproduce the artifact and the numbers. Every gate below is a **hard stop**: do not proceed if the acceptance test fails.

---

## 0. How to use this document

### 0.1 Reading order (do not skip)

1. Read §0–§4 on a laptop with **no GPU required**. These sections freeze the scientific claim, the frozen P1.1 facts, the GPU wall, and the bans.  
2. Execute **Gate 0** (lock the PDF) before any confirmatory English BPB.  
3. Execute **Gates A–G** on a CPU/Mac machine (same class as P1.1 A–G).  
4. Execute **Gate H** on a **CUDA NVIDIA** host (A40-class proven). Not Mac MPS. Not DGX Spark until a labeled Spark smoke beats init **without** an attention-kernel patch.  
5. Execute **Gate I** (EN0) on CUDA. This is the expensive wall.  
6. Execute **Gate P0** before any Tagalog continuation token.  
7. Execute **Gates Q–T** (arms A0–A3) on CUDA.  
8. Execute **Gates U–W** (seal, one test touch, deposit) before writing a results paper, README, or tweet.

### 0.2 Two naming systems (do not confuse them)

| Name | What it is | Example |
|---|---|---|
| **Gate A, B, … W** | Hard-stop engineering/science checkpoints in this protocol | Gate F = English tokenizer |
| **Arm EN0, A0, A1, A2, A3** | Weight states / training interventions | A2 = Tagalog continuation (the CF intervention) |
| **P1.1 Gate A–J** | Already finished Tagalog-from-scratch study | P1.1 Gate J is frozen |

Arm **A0** is not Gate A. Gate A is the nanochat pin. Arm A0 is the frozen English parent evaluated on both languages.

### 0.3 Gate language

- **MUST** — required for the run to count as Protocol P2-EN→TL confirmatory.  
- **MUST NOT** — forbidden; a violation invalidates the confirmatory label.  
- **SHOULD** — default; record a deviation card if skipped.  
- **MAY** — optional; must be labeled exploratory unless the filed PDF already names it.

### 0.4 What this project is and is not

**This project is:** a **nanochat-only** sequential-pretraining (Shi **CPT**, language-shift) study. Train an English WikiText-103 parent with official `tok_train` → `base_train` → `evaluate_bpb`. Continue that parent on the **frozen P1.1 WikiText-TL-39 train split**. Measure whether English held-out BPB rises more than after extra English at the same budget, and whether Tagalog held-out BPB falls.

**This project is not:** P1.1. It is not Tagalog-parent English continuation. It is not ULMFiT classifier CF (Cruz 2019). It is not CFT (instruction/safety). It is not a Hugging Face Trainer run. It is not Llama-2/FiLLM. It is not a claim that P1.1 d20 forgot English. It is not an amendment of AsPredicted #306780.

### 0.5 GPU wall (read before renting)

| Work | Host | GPU required? |
|---|---|---|
| Gate 0 lock, literature, PDF, paper edits | Laptop | **No** |
| Gates A–G: pin, English archive, hygiene, split, shards, `tok_train`, budget | Mac/CPU | **No** |
| Gate H smoke: English d4, short `base_train`, loss **below init** | CUDA NVIDIA | **Yes** |
| Gate I EN0 d8 and d20 at English \(D_{3x}\) | CUDA NVIDIA | **Yes** |
| Gate P0 dual `evaluate_bpb` | CUDA (or CPU if it finishes; CUDA preferred) | **Yes in practice** |
| Gates Q–T arms A0–A3 | CUDA NVIDIA | **Yes** |
| Gate U full BPB seal | CUDA | **Yes in practice** |
| Gate V one test touch | CUDA | **Yes in practice** |
| Gate W deposit / paper numbers | Laptop | **No** |

**Confirmatory GPU class:** NVIDIA CUDA with official nanochat attention (Flash Attention 2/3 as the pin selects, or **unpatched** SDPA). **Proven:** Runpod A40 48 GB (P1.1 Gate H `p7e5zk3njnglgy`, Gate I `68bei7d3vx4krc`).

**Not confirmatory hosts until a new labeled smoke passes:**

- Apple MPS (P1.1 d20 OOM; not the filed GPU class).  
- DGX Spark GB10 SM121 (`spark-a9f0`): pin FA3 detector + `torch.compile` crash; SDPA source patch is a **code change** = blocked for official H; 2026-08-17 d4/30-step smoke **rose above init** after step 20 and used default `--warmup-steps 40` on a 30-step run. See `docs/run-cards/deviations/2026-08-17-dgx-spark-gate-h-h2.md`.  
- Any host that requires editing `nanochat/flash_attention.py` or disabling compile to train.

**Spark re-entry rule (optional later):** kill ollama first; `TORCHDYNAMO_DISABLE=1`; **unpatched** SDPA; `--warmup-steps` strictly less than `--num-iterations`; labeled `p2-spark-smoke-*`; loss and val BPB **below the same-run step-0/init**. Until that card exists, Spark is workshop only.

### 0.6 Frozen P1.1 facts (copy; do not re-measure to “confirm”)

These numbers are **historical**. P2 consumes the Tagalog **train** split and tokenizer hashes as **inputs**. P2 does **not** reopen P1.1 D\* or P1.1 test.

| Item | Frozen value |
|---|---|
| AsPredicted | #306780, https://aspredicted.org/6r6v4v.pdf |
| PDF SHA256 | `a34f119df557d2e763aa154e02b76b0ebcbcba1f3fb32c3219d85ae6395cc5ca` (re-hash the local `docs/run-cards/AsPredicted-306780.pdf` at Gate 0; if mismatch, **stop**) |
| ResearchBox | #8735 |
| RUN_ID | `p1-20260816T025911Z-0067a57` |
| nanochat | `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` |
| Split label | `reconstructed_article_70_15_15` |
| Train documents | 84,679 |
| `T_train` (Tagalog BPE, no BOS, no pack) | 6,401,013 |
| `D_3x` | 19,203,039 |
| `B` | 65,536 |
| `N` | 294 |
| `D_actual` | 19,267,584 |
| Tokenizer SHA256 | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| Train split SHA256 | `2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687` |
| Packed val bytes | 5,868,797 |
| Official d20 `val_bpb_full` | 1.172248 |
| Official d8 | 1.179135 |
| Official d12 | 1.180824 |
| Official d16 | 1.195546 |
| One P1.1 `test_bpb` | 1.164768 (**do not reuse as a P2 after-Tagalog number**) |
| Untrained Tagalog ~ | 3.289 |
| Byte unigram | 4.453225 |
| d20 weights | https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x |
| d20 `model_000294.pt` SHA256 | `9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38` — **never load this file as EN0 or A2 start weights** |

If any of these disagrees with the P1.1 Gate J card, **the Gate J card wins** and this table is wrong.

---

## 1. Scientific objective

### 1.1 One-sentence objective

After an English-pretrained nanochat (WikiText-103 raw, English 32,768 BPE, depths 8 and 20) passes provenance **P0**, continue it on frozen P1.1 WikiText-TL-39 train for \(D_{\mathrm{phase2}}\) English-BPE tokens, and test whether English held-out BPB rises by at least 0.01 more than after extra English (A1), while Tagalog held-out BPB falls relative to the frozen parent (A0).

### 1.2 Research questions (confirmatory, PDF must name these)

**RQ1 (forgetting / retention).** Is \(C_{\mathrm{en}} \ge 0.01\)? That is: does Tagalog continuation raise English `val_bpb_full` more than matched extra English?

**RQ2 (acquisition).** Does A2 Tagalog `val_bpb_full` fall relative to A0 (and, descriptively, relative to P1.1 Table 2 d20 — **not required to match**, different BPE and init)?

**RQ3 (specificity).** Does A3 (replay / mix) reduce \(C_{\mathrm{en}}\) relative to A2 at the same \(D_{\mathrm{phase2}}\)?

**RQ4 (provenance).** Before any Tagalog train token: is EN0 better at English than untrained and than P1.1 d20 by \(\ge 0.01\) BPB, and worse at Tagalog than P1.1 d20 by \(\ge 0.01\) BPB? If P0 fails, **stop calling the parent English-pretrained.**

### 1.3 Non-questions (out of scope for confirmatory P2)

- Reopening P1.1 D\* or a second P1.1 test read in the P1.1 ledger.  
- CORE, MMLU, GSM8K, ARC as primary.  
- Chat / SFT / identity.  
- EWC, LoRA, model merging as confirmatory (MER 2508.01908 is exploratory + code deviation).  
- Hugging Face `Trainer`, ClimbMix, `python -m nanochat.dataset`.  
- Loading `p1-fixed-d20-3x` `model_000294.pt` as the English parent.  
- Scoring P1.1 d20 on WikiText-103 and calling the number BWT (that is never-learned OOD).  
- FilBench as Table 1 (exploratory appendix after a bilingual parent exists).  
- Tokenizer swap mid-study (Yoon 2311.05741) as confirmatory.  
- Infinite-LR / WSD (2503.02844) as confirmatory.  
- High-PPL token masking as confirmatory.

### 1.4 SOTA amendments that MUST be in the PDF **before filing** if they are confirmatory

These are **the same paper**, not Paper 2b. If they are not in the filed PDF, they are exploratory even if you run them.

| Amendment | Confirmatory if named in PDF | Default if you file the current short draft |
|---|---|---|
| A3 50/50 document mix | Yes (already in draft) | Confirmatory |
| Replay grid 1% / 5% / 10% English docs in A2-class runs (Bethune; Ibrahim) | Only if PDF names the ratios | Exploratory unless added |
| Log English `val_bpb_full` **along** A2 (trajectory; 2505.07796) | Only if PDF says trajectory is a DV or planned descriptive | Descriptive SHOULD even if not a hypothesis |
| \(C_{\mathrm{en}}\) vs PTPP \(R_d\) (2510.23198) | Only if PDF names \(R_d\) | Report \(R_d\) in the card anyway; hypothesis only if filed |
| Entity / overlap / contamination slice BPB | Only if PDF names the slice rule | SHOULD as robustness; confirmatory if filed |
| Capacity prior (d20 vs d8 forget more) | Secondary if PDF names it | d8 and d20 are already required parents |

**Do not add to the PDF as confirmatory:** Llama parent, EWC primary, CORE/SFT primary, Spark attention patch, FilBench Table 1.

---

## 2. Notation

| Symbol | Meaning |
|---|---|
| EN0 | From-scratch English `base_train` on WikiText-103 raw train, English 32,768 BPE |
| A0 | Frozen EN0 weights; no further train tokens |
| A1 | Extra English continuation from EN0 for \(D_{\mathrm{phase2}}\) |
| A2 | Tagalog continuation from EN0 for \(D_{\mathrm{phase2}}\) (treatment) |
| A3 | Mixed continuation (50/50 documents unless PDF names other ratios) |
| \(T_{\mathrm{en,train}}\) | English BPE token count of WikiText-103 **train**, no BOS, no packing, no crop (P1.1 Gate G definition) |
| \(D_{3x,\mathrm{en}}\) | \(3 \times T_{\mathrm{en,train}}\) |
| \(N_{\mathrm{EN0}}\) | \(\lceil D_{3x,\mathrm{en}} / B \rceil\) unless the PDF names a different English budget |
| \(D_{\mathrm{phase2}}\) | Default \(294 \times 65536 = 19{,}267{,}584\) English-BPE tokens (P1.1 `D_actual`), unless the PDF names English \(D_{3x}\) instead |
| \(B\) | 65,536 (keep unless Gate G proves it illegal for English \(N\)) |
| \(T\) | 2048 |
| \(C_{\mathrm{en}}\) | English `val_bpb_full`(A2) − English `val_bpb_full`(A1) |
| P0 | Provenance inequalities in §1.2 RQ4 |
| 0.01 BPB | Not-a-ranking threshold (same as P1.1) |

---

## 3. Hypotheses (file these; do not peek)

**H1 (P0).** EN0 English BPB < untrained English BPB, and EN0 English BPB + 0.01 ≤ P1.1 d20 English BPB on the **same** WikiText-103 val UTF-8, and EN0 Tagalog BPB ≥ P1.1 d20 Tagalog BPB + 0.01. Falsified → parent is not English-pretrained; **do not interpret A2 as CF.**

**H2 (forgetting).** \(C_{\mathrm{en}} \ge 0.01\). Falsified if A2 English BPB is not worse than A1 by 0.01 (including if A2 is better).

**H3 (acquisition).** A2 Tagalog `val_bpb_full` < A0 Tagalog `val_bpb_full` by ≥ 0.01. Falsified if Tagalog does not improve. Matching P1.1 1.172248 is **not** required.

**H4 (replay, if A3 is in the PDF).** A3 \(C_{\mathrm{en}}\) < A2 \(C_{\mathrm{en}}\). Falsified if 50/50 (or the filed replay ratio) does not reduce English degradation.

**H5 (depth, secondary).** If the PDF names it: d20 shows larger \(C_{\mathrm{en}}\) than d8 (capacity / overwriting prior). Gaps < 0.01 are not rankings.

Gaps with absolute value below 0.01 BPB **MUST NOT** be called rankings. Seed intervals containing 0 **MUST NOT** be called rankings.

---

## 4. Threats (pre-register by putting them in the PDF or this protocol dated before EN0 BPB)

| Threat | Mitigation |
|---|---|
| Never-learned OOD scored as BWT | P0 required; P1.1 d20 on English is a **negative control**, not a parent |
| Tokenizer mismatch | One English 32,768 BPE for **all** P2 arms; P1.1 Tagalog BPE is **reference only** |
| Different \(D_{\mathrm{phase2}}\) across arms | Same \(N\), \(B\), seed offsets recorded |
| Warmup ≥ iterations (Spark 2026-08-17) | `--warmup-steps` MUST be < `--num-iterations`; for short smokes use 10% of \(N\) or 14, whichever is smaller and ≥ 0 |
| `ratio -1` | MUST NOT |
| Last-shard-is-val | English val parquet lexicographically last |
| Test peek | Separate P2 `test_access_log`; Tagalog test after Tagalog val seal; English test after English val seal |
| Contamination / entity overlap EN↔TL Wikipedia | Slice BPB SHOULD; confirmatory only if PDF names the slice rule |
| Optimizer state from EN0 | Fresh Adam at A1/A2/A3 (Ibrahim-style new phase); LR peak = 0.3 × EN0 peak unless PDF says otherwise |
| Code change (attention patch) | Blocked for confirmatory |
| Writing into `p1-fixed-d20-3x` | New HF repo only |

---

## 5. Failure / stop criteria (any gate)

Stop the confirmatory label (file a deviation; do not silently continue) if:

- NaN / Inf loss or BPB.  
- ClimbMix / `python -m nanochat.dataset` / FineWeb appears in the cache.  
- Val or test documents appear in the train directory.  
- New tokenizer trained after seeing confirmatory BPB.  
- `--target-param-data-ratio -1`.  
- CORE/SFT used as a selection rule.  
- Hugging Face Trainer is the LM loop.  
- Any file is written into `pageman/nanochat-filipino-p1-fixed-d20-3x`.  
- P1.1 `model_000294.pt` is loaded as `base_train --load` for EN0/A1/A2/A3.  
- P1.1 `test_bpb = 1.164768` is reported as an A2 number.  
- P0 fails and the write-up still says “English-pretrained.”  
- Attention kernel / `flash_attention.py` edited.  
- Shard SHA256 changes mid-run.  
- `--warmup-steps >= --num-iterations`.

---

# STAGE 0 — LOCK (laptop, no GPU)

## Gate 0 — File the AsPredicted PDF (hard start of confirmatory science)

**Purpose.** Create the Level-1 instrument for P2. Without this PDF, Gates I+ are wiring / exploratory only.

**Host.** Laptop. **GPU: no.**

### 0.1 Pre-file checklist (MUST)

1. Read `DIRECTION-RECALIBRATION.md` and this protocol.  
2. Decide, **in writing in the PDF**, every confirmatory arm: EN0 d8/d20, A0, A1, A2, A3 50/50, and whether 1/5/10% replay is confirmatory.  
3. Name \(D_{\mathrm{phase2}}\): default `19267584` **or** English \(D_{3x}\) — pick one sentence.  
4. Name LR: `0.3 × EN0 peak`, warmup 14 (or `min(14, 10% N)`), fresh Adam.  
5. Name P0 inequalities and the 0.01 not-a-ranking rule.  
6. Name official `evaluate_bpb` (copy of `scripts/p1/gate_j_full_bpb.py`), `T=2048`, BOS-bestfit.  
7. Name exclusions (ClimbMix, ratio −1, CORE/SFT/EWC confirmatory, HF Trainer, P1.1 weights as parent, amend #306780).  
8. State: P1.1 weights are Tagalog-from-scratch **reference** and English **negative control**.  
9. State: WikiText-TL-39 is a **recipe analogue** of WikiText-103, not a translation.  
10. Do **not** put the ResearchBox #8735 passcode, `test.jsonl`, or API keys in the PDF.

### 0.2 File

- New AsPredicted (new number).  
- **MUST NOT** amend #306780.  
- Save PDF to `docs/run-cards/aspredicted-p2-submitted.pdf` (gitignored if it contains emails you do not want public — follow P1.1 pattern).  
- Record SHA256 of the **anonymous PDF**.  
- Create ResearchBox **new** box (not #8735 overwrite).  
- Update `paper.tex` registration URL **after** the number exists.

### 0.3 Acceptance

- Anonymous PDF URL resolves.  
- SHA256 recorded in `docs/papers/p2-cf-english/LOCK.json` (create this file).  
- `LOCK.json` contains: aspredicted_id, url, pdf_sha256, filed_timestamp, nanochat_pin, p1_run_id, statement `does_not_amend_306780: true`.

### 0.4 Failure

- Filing while EN0 `val_bpb_full` already exists in a notebook you intend to call confirmatory → those numbers are **exploratory**; confirmatory EN0 must be a **new** run after the PDF, or you must disclose that BPB existed (HARKing). **Preferred:** file first, then Gate I.

**STOP.** Do not start Gate I until Gate 0 acceptance is true.

---

# STAGE 1 — ENVIRONMENT AND PIN (Mac/CPU, no GPU)

## Gate A — Pin nanochat and isolate the P2 cache

**Purpose.** Same pin as P1.1. New cache. No ClimbMix.

**Host.** Mac/CPU. **GPU: no.**

### A.1 Inputs

- Repo `/Users/paulpajo/Projects/nanochat-filipino`  
- `vendor/nanochat` at `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`  
- Hook patch already applied

### A.2 Commands (sketch; wrap in `scripts/p2/` later, do not invent a second trainer)

```bash
# New P2 env — NEVER source scripts/p1/env.sh for confirmatory P2 runs
export P2_ROOT="/Users/paulpajo/Projects/nanochat-filipino"
export P2_RUN_ID="p2-$(date -u +%Y%m%dT%H%M%SZ)-$(git -C "$P2_ROOT" rev-parse --short HEAD)"
export NANOCHAT_BASE_DIR="$P2_ROOT/data/cache/${P2_RUN_ID}"
export PATH="/opt/homebrew/bin:$PATH"
export VIRTUAL_ENV="$P2_ROOT/vendor/nanochat/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
cd "$P2_ROOT/vendor/nanochat"
git rev-parse HEAD   # MUST equal 92d63d4e8bb4df75c3b71618f31ddde2378b2bcd
git status --porcelain  # MUST be empty of uncommitted trainer/attention edits
```

### A.3 MUST

- Create `docs/run-cards/p2/${P2_RUN_ID}/gate-a.json`.  
- Record `git rev-parse HEAD`, `git diff --stat`, Python version, torch version **on this Mac**.  
- Confirm `NANOCHAT_DATA_DIR` hook exists and P1.1 `python -m nanochat.dataset` is still banned.  
- Create empty `NANOCHAT_BASE_DIR`.  
- Confirm **no** `flash_attention.py` local mods vs pin.

### A.4 MUST NOT

- `python -m nanochat.dataset`  
- `WANDB` live project that becomes a selection dashboard  
- Copying P1.1 `NANOCHAT_BASE_DIR` into P2 cache  
- Starting EN0 here (no GPU / not Gate I)

### A.5 Acceptance

- Pin hash exact.  
- Hook present.  
- New `P2_RUN_ID` and empty cache.  
- `gate-a.json` status `pass`.

**STOP if pin dirty or attention file differs.**

---

## Gate B — English archive (WikiText-103 raw)

**Purpose.** Obtain **raw** WikiText-103 (not word-level only if the PDF says raw; the draft says **raw**). Record SHA256. This is Merity et al. 2016, English Good+Featured Wikipedia.

**Host.** Mac/CPU. **GPU: no.** Network needed.

### B.1 Source rule

- Prefer the **canonical** WikiText-103 raw distribution named in the PDF (Salesforce / Merity pointer).  
- Hugging Face mirrors MAY be used **if and only if** the PDF names the dataset id and you record file SHA256s.  
- **MUST NOT** use WikiText-2 as a substitute.  
- **MUST NOT** use WikiText-TL-39 as English.  
- **MUST NOT** use ClimbMix / FineWeb / DCLM.

### B.2 Steps (granular)

1. Create `data/raw/wikitext-103-raw/` (or the path named in `LOCK.json`).  
2. Download train/valid/test **raw** files.  
3. `shasum -a 256` every file; write `gate-b-english-archive.json`.  
4. Record byte sizes, line counts, and whether Moses-like tokenization is present (WikiText-103 raw is **not** the same surface as WikiText-TL-39 Moses).  
5. Write a one-page `DATA-CARD-wikitext-103.md` in the P2 run-card folder: license, citation 1609.07843, Good+Featured vs TL-39 all A–Z (recipe analogue, not translation).  
6. **Do not** mix these files into `data/processed/wikitext-tl39/`.

### B.3 Acceptance

- All three splits present.  
- SHA256s in git (JSON).  
- No Tagalog parquet in this directory.  
- Independent `wc -c` matches recorded sizes.

**STOP if files are word-level when the PDF required raw, or vice versa.**

---

## Gate C — Hygiene (no leak, no ClimbMix, no P1.1 overwrite)

**Purpose.** Same spirit as P1.1 Gate C.

**Host.** Mac/CPU. **GPU: no.**

### C.1 Checks (every one MUST be scripted and logged)

1. `NANOCHAT_BASE_DIR` contains only P2 artifacts.  
2. `find` for `climbmix`, `fineweb`, `dclm`, `oscar` under `NANOCHAT_BASE_DIR` → 0 hits.  
3. P1.1 `data/processed/wikitext-tl39/active` is **read-only** for P2 (copy or bind; never write).  
4. P1.1 `test.jsonl` is **not** in the P2 train dir.  
5. Hugging Face token / Runpod key / ResearchBox passcode not in any file that will be committed.  
6. `git status` does not show `aspredicted-p1-submitted.txt` staged.  
7. Confirm `pageman/nanochat-filipino-p1-fixed-d20-3x` will not be `git lfs push` target for P2 ckpts.

### C.2 Acceptance

- `gate-c-hygiene.json` all checks `true`.

**STOP on any false.**

---

# STAGE 2 — ENGLISH PACKAGING (Mac/CPU, no GPU)

## Gate D — English document split (train/val/test)

**Purpose.** Produce a **frozen** English split. WikiText-103 **already has** canonical train/valid/test. **MUST use the canonical WT103 splits** unless the PDF explicitly says otherwise.

**Host.** Mac/CPU. **GPU: no.**

### D.1 Rule

- **Default:** keep Merity train / valid / test article boundaries.  
- **MUST NOT** reshuffle WT103 with the Tagalog 70/15/15 hash (that would be a new corpus).  
- Record article counts vs literature: WT103 train 28,475 articles / ~103M Moses tokens (word-level paper Table 1). Raw BPE counts will differ — that is Gate G.

### D.2 Steps

1. Parse raw files into one document per article (WikiText `=` headers), LF normalize only.  
2. Write `english_train.jsonl`, `english_val.jsonl`, `english_test.jsonl`.  
3. SHA256 each.  
4. Assert train/val/test document-id overlap = 0.  
5. **Do not** touch Tagalog `test.jsonl`.  
6. Write `gate-d-english-split.json` with document counts and hashes.

### D.3 Acceptance

- Disjoint IDs.  
- Hashes recorded.  
- Canonical WT103 split identity stated (`wikitext103_official_raw_splits`).

**STOP if overlap > 0 or if you “improved” the split after a pilot BPB.**

---

## Gate E — Parquet shards (English train/val + Tagalog train **copy**)

**Purpose.** nanochat last-shard-is-val. English and Tagalog live in **different** `NANOCHAT_DATA_DIR`s.

**Host.** Mac/CPU. **GPU: no.**

### E.1 English shards

1. Pack `english_train` → `train_*.parquet` (lexicographic names **before** val).  
2. Pack `english_val` → `val.parquet` or a name that sorts **last**.  
3. **MUST NOT** put English test in the train/val directory.  
4. SHA256 every parquet.  
5. Point `NANOCHAT_DATA_DIR_EN` at this directory.

### E.2 Tagalog shards (reuse P1.1; do not rebuild)

1. **Copy** (do not rewrite) P1.1 frozen train shards / jsonl used for P1.1 `base_train`.  
2. Verify train split SHA256 = `2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687`.  
3. Point `NANOCHAT_DATA_DIR_TL` at a **read-only** copy.  
4. Val Tagalog for P2 acquisition = P1.1 val (same packed bytes 5,868,797).  
5. **MUST NOT** re-run article reconstruction.  
6. **MUST NOT** detokenize Moses for confirmatory.

### E.3 A3 mix shards (prepare now, train later)

1. Build a **document-level** mixer: sample English train docs and Tagalog train docs at the PDF ratio (default 50/50 **documents**, not bytes — **say which in the PDF**).  
2. Freeze the mix with a seed named in the card **before** Gate I BPB.  
3. If PDF also names 1/5/10% English replay: build those three mix directories now, hashes now.  
4. **MUST NOT** change mix after seeing \(C_{\mathrm{en}}\).

### E.4 Acceptance

- `gate-e-shards.json` with every parquet SHA256.  
- Tagalog train hash match.  
- Mix seeds recorded.  
- Test files absent from train dirs.

**STOP if Tagalog hash mismatch (you are not on P1.1 data).**

---

## Gate F — English `tok_train` (32,768 BPE)

**Purpose.** One English tokenizer for **all** P2 arms. Official `scripts.tok_train`.

**Host.** Mac/CPU. **GPU: no.**

### F.1 Steps

1. `NANOCHAT_DATA_DIR=$NANOCHAT_DATA_DIR_EN`  
2. Train vocab 32768 on **English train only**.  
3. Save `tokenizer.pkl` (or nanochat’s actual artifact names) under `NANOCHAT_BASE_DIR`.  
4. SHA256 the tokenizer.  
5. Compute bytes/token on English val and on Tagalog val (**descriptive**; do not pick a different vocab size after this).  
6. **MUST NOT** train a second tokenizer after Gate I.  
7. **MUST NOT** reuse P1.1 tokenizer `04436b85…` as the P2 LM tokenizer (that is a Tagalog BPE; using it would confound CF with tokenizer shift).  
8. P1.1 tokenizer remains the **reference** for P1.1 Table 2 numbers only.

### F.2 Acceptance

- Vocab size 32768.  
- Train-only.  
- Hash in `gate-f-tokenizer.json`.  
- Fertility table written (English val vs Tagalog val).

**STOP if tokenizer saw English val/test or Tagalog train (leak / bilingual BPE is a different study).**

---

## Gate G — Budget (EN0 \(N\) and \(D_{\mathrm{phase2}}\))

**Purpose.** Same definition as P1.1 Gate G: \(T_{\mathrm{en,train}} = \sum_d \mathrm{len}(\tau(x_d))\), no BOS, no packing, no crop.

**Host.** Mac/CPU. **GPU: no.** This gate **sizes the GPU bill**. Do not rent until it passes.

### G.1 Compute

1. Encode every English **train** document with the Gate F tokenizer.  
2. Sum token lengths → \(T_{\mathrm{en,train}}\).  
3. \(D_{3x,\mathrm{en}} = 3 \times T_{\mathrm{en,train}}\).  
4. \(B = 65536\) unless \(D_{3x,\mathrm{en}}/B < 200\) steps — then follow P1.1 power-of-two rule and **write a deviation**.  
5. \(N_{\mathrm{EN0}} = \lceil D_{3x,\mathrm{en}} / B \rceil\).  
6. **Expect \(N_{\mathrm{EN0}} \gg 294\)** (WT103 is much larger than TL-39). Record wall-clock estimate: use P1.1 A40 d20 tok/s if available from Gate I cards; else run a 20-step probe at Gate H and extrapolate.  
7. \(D_{\mathrm{phase2}}\): if PDF says P1.1 `D_actual`, then \(N_{\mathrm{phase2}} = 294\), \(D_{\mathrm{phase2}} = 19267584\). If PDF says English \(D_{3x}\), then \(N_{\mathrm{phase2}} = N_{\mathrm{EN0}}\). **Do not mix.**  
8. Write `gate-g-budget.json` analog of `manifests/budget_manifest.json`.  
9. Estimate A40-hours: \(N_{\mathrm{EN0}}\) steps × (d8 + d20) + 3 × 294 (A1/A2/A3 at d20) + d8 copies if the PDF requires both depths on all arms.  
10. **SHOULD** require both depths on A2 if the PDF names the capacity prior; otherwise A2 on **d20 required**, d8 A2 **SHOULD**.

### G.2 MUST pass flags for later `base_train`

- `--num-iterations` **explicit** (never omit; never `ratio -1`).  
- `--core-metric-every -1`  
- `--total-batch-size 65536` (or the Gate G value)  
- `--sequence-len 2048`  
- `--warmup-steps` < `--num-iterations`

### G.3 Acceptance

- JSON written.  
- \(N_{\mathrm{EN0}}\) finite and ≥ 200.  
- Cost estimate in the card (hours × GPU class).  
- User has read the estimate **before** Gate H rental.

**STOP if you skip this and “just train until loss looks good.”**

---

# STAGE 3 — CUDA SMOKE (GPU required)

## Gate H — English d4 smoke on confirmatory GPU class

**Purpose.** Prove **this host + this pin + this English data** can descend. Engineering gate, not a paper table.

**Host.** NVIDIA CUDA (A40-class default). **GPU: yes.**  
**MUST NOT** be Mac MPS. **MUST NOT** be Spark until Spark re-entry rule in §0.5.

### H.1 Preflight (on the GPU host)

1. `nvidia-smi`  
2. `python -c "import torch; print(torch.cuda.get_device_capability())"` — record SM.  
3. `git -C vendor/nanochat rev-parse HEAD` = pin.  
4. `diff` `nanochat/flash_attention.py` vs pin = empty.  
5. Kill competing GPU users (on Spark: ollama; on shared A40: other pods).  
6. `export WANDB_MODE=disabled` or dummy.  
7. Copy tokenizer + English shards + `NANOCHAT_DATA_DIR`.  
8. Confirm `--warmup-steps` for this smoke is **<** `--num-iterations`.

### H.2 Smoke recipe (default)

- `--depth 4`  
- `--num-iterations 30` **or more**  
- `--warmup-steps 3` (10% of 30; **never 40**)  
- `--device-batch-size` start 8; drop only if OOM  
- `--core-metric-every -1`  
- `T=2048` unless OOM — if you drop T for smoke, **label** `smoke_T=512` and **do not** treat as H-pass for d20 EN0. A **confirmatory-path** smoke SHOULD keep `T=2048` even if steps are few.  
- Record step-0 / init val BPB **in the same process**.

### H.3 Acceptance (H2 analogue)

- Train loss at last step **<** train loss at step 0.  
- Val BPB at last eval **<** val BPB at first eval (or < untrained if you logged untrained).  
- No NaN.  
- Checkpoint reloadable.  
- Card named `p2-gate-h-<gpu-id>-<timestamp>.md`.  
- **Do not** merge this card into P1.1 `execution_host.json`.

### H.4 If it fails

- File deviation.  
- **MUST NOT** start Gate I.  
- **MUST NOT** patch attention to make it pass.  
- Try A40 if the host was Spark/MPS.

### H.5 Optional: P1.1-style Tagalog d4 on the **same** A40

Not required for P2 science. Only to prove the box matches P1.1 H (`p7e5zk3njnglgy` smoke val BPB 2.915 is **historical**, do not chase it). If you rerun Tagalog smoke, new numbers are **not** P1.1.

**STOP until H2 acceptance is true on the host that will run EN0.**

---

# STAGE 4 — ENGLISH PARENT (GPU required; PDF must already exist)

## Gate I — EN0 `base_train` depths 8 and 20

**Purpose.** The English parent. This is the long job.

**Host.** Same CUDA class that passed Gate H. **GPU: yes.**

### I.1 Before launch

1. Gate 0 PDF exists.  
2. Gates A–H pass.  
3. Create HF repo `pageman/nanochat-filipino-p2-en-then-tl` (empty).  
4. **MUST NOT** upload to `p1-fixed-d20-3x`.  
5. Launch script passes `--num-iterations $N_EN0` explicitly.  
6. `--eval-every` set so you can see descent; **MUST NOT** early-stop on English val to pick a “lucky” EN0 unless the PDF names a selection rule (default: **final checkpoint** like P1.1).  
7. Seed named.  
8. `device-batch-size`: start 8 on A40; P1.1 d20 used this class.

### I.2 Order

1. d8 EN0 first (cheaper; proves data).  
2. d20 EN0 second (paper parent unless PDF says both are co-primary).  
3. **Do not** start A2 until **both** required EN0 runs finish and Gate P0 passes.

### I.3 During the run

- If loss NaN: stop, deviation, do not continue with a patched kernel.  
- If preempted: resume from last ckpt **only if** the trainer resume is official nanochat; record wall-clock gap.  
- Do not watch CORE.

### I.4 Artifacts

- `model_NNNNNN.pt` for each depth  
- SHA256  
- optimizer not needed after freeze if A1–A3 use fresh Adam  
- `gate-i-en0-d8.json`, `gate-i-en0-d20.json`  
- Upload to **p2** HF repo under `en0/d8/` and `en0/d20/`

### I.5 Acceptance

- Both depths finished \(N_{\mathrm{EN0}}\) steps.  
- Finite train loss.  
- Checkpoints reload.  
- Hashes recorded.

**STOP. Do not continue Tagalog until Gate P0.**

---

## Gate P0 — Provenance (dual `evaluate_bpb` before any Tagalog train token)

**Purpose.** Prove EN0 is English-pretrained **relative to untrained and to P1.1 d20**.

**Host.** CUDA. **GPU: yes in practice.**

### P0.1 Evaluations (official `evaluate_bpb` only)

Copy `scripts/p1/gate_j_full_bpb.py` into `scripts/p2/evaluate_bpb.py` **before** Gate I (code freeze). Same formula, `T=2048`, BOS-bestfit.

Run, with the **P2 English tokenizer** and **P2 English val UTF-8**:

| Model | English val | Tagalog val (P1.1 val UTF-8) |
|---|---|---|
| Untrained same depth | required | required |
| EN0 d8 | required | required |
| EN0 d20 | required | required |
| P1.1 d20 `model_000294.pt` | required (negative control) | already known 1.172248; **MAY** re-score with **P2 tokenizer** as a **separate** number labeled `p1d20_on_p2_bpe` — do **not** overwrite 1.172248 |

**Critical:** P1.1 Table 2 used the **Tagalog** BPE. P0 inequalities that compare EN0 vs P1.1 d20 on English MUST use the **same tokenizer and same UTF-8** for both models in that inequality. The PDF MUST say which tokenizer is used for the cross-model English comparison.

**Recommended PDF sentence:** “P0 English comparisons use the P2 English tokenizer and WikiText-103 val UTF-8 for EN0, untrained, and for a forward pass of P1.1 d20 weights **without** claiming that number is P1.1 Table 2.” P1.1 d20 on English BPE may be terrible; that is the point of the negative control.

**Alternative (cleaner):** P0 English test is only EN0 vs untrained on English BPE, and EN0 vs P1.1 d20 on English UTF-8 with **each model’s native tokenizer** reported as two incomparable columns — then the ≥ 0.01 gap is **only** EN0 vs untrained, plus a **qualitative** “P1.1 d20 is not an English LM.” **Pick one in the PDF at Gate 0.** Do not pick after seeing numbers.

### P0.2 Pass inequalities (if PDF uses the draft)

- EN0 English `val_bpb_full` < untrained English (same depth, same tok).  
- EN0 English + 0.01 ≤ [P1.1 d20 English on the **named** comparable setup].  
- EN0 Tagalog ≥ P1.1 d20 Tagalog + 0.01, where Tagalog P1.1 number 1.172248 uses Tagalog BPE — so EN0 Tagalog MUST be scored with **P1.1 tokenizer** for this inequality, **or** both with P2 tokenizer. **PDF must pick.**  
  **Recommended:** acquisition P0 uses **P1.1 tokenizer + P1.1 val** for P1.1 d20 (frozen 1.172248, do not recompute as Table 2) and a **new** EN0 score with **P1.1 tokenizer** on the same val UTF-8 so the inequality is tokenizer-matched. That requires loading EN0 weights with the **Tagalog** BPE — embedding size is 32768 both, but **token ids differ**. **You cannot** score EN0 with P1.1 tokenizer without a **different study** (tied embeddings trained on English ids).  

**Therefore the only coherent P0 is:**

1. **English P0:** EN0 vs untrained, P2 English BPE, WT103 val.  
2. **English negative control:** P1.1 d20 vs EN0 on WT103 val UTF-8 **each with its own tokenizer** (incomparable BPB) **or** both as raw UTF-8 byte-NLL (if you add a byte metric — only if PDF names it).  
3. **Tagalog P0:** EN0 vs P1.1 d20 on P1.1 val UTF-8, **each with its own tokenizer** (EN0 will look like a bad Tagalog LM under English BPE). The ≥ 0.01 claim is then: EN0 Tagalog BPB (English BPE) is worse than P1.1 d20 Tagalog BPB (Tagalog BPE) — **incomparable**.  

**Coherent confirmatory P0 (MUST put this in the PDF):**

- **P0-E:** EN0 English val BPB < untrained, same English BPE, gap ≥ 0.01.  
- **P0-X:** P1.1 d20 is **not** used as an English parent; report its English-BPE BPB only as “never-trained-on-English OOD” if you run it.  
- **P0-T:** EN0 Tagalog val BPB (English BPE, P1.1 val UTF-8) > untrained-or-random **wait** — acquisition baseline is A0 vs A2 with the **same** English BPE. P1.1 Table 2 is a **descriptive** reference only, not a P0 inequality.

**Action for Gate 0:** replace the draft’s cross-tokenizer 0.01 inequalities with **P0-E** (EN0 beats untrained English) plus **P0-T0** (EN0 Tagalog BPB exists as A0). Do **not** require EN0 Tagalog BPB − 1.172248 ≥ 0.01 across tokenizers.

This protocol **overrides the draft** on this point until the PDF is filed. The PDF must use tokenizer-matched inequalities only.

### P0.3 Acceptance

- P0-E pass for d8 and d20.  
- A0 numbers written (`gate-p0.json`).  
- P1.1 d20 **not** loaded as train start.  
- No Tagalog `base_train` yet.

**If P0-E fails:** EN0 is not an English LM. **Stop.** Debug data/tokenizer/train. Do not run A2 as CF.

---

# STAGE 5 — CONTINUATION ARMS (GPU required)

## Gate Q — Arm A0 freeze

**Purpose.** Freeze EN0. Dual eval is Gate P0. This gate is a **ledger stamp**.

**Host.** Laptop or GPU. **GPU: no extra train.**

### Q.1 Steps

1. Copy EN0 d20 (and d8) checkpoints to `a0/frozen/` with SHA256.  
2. Set `immutable: true` in `gate-q-a0.json`.  
3. Record A0 English and Tagalog `val_bpb_full` from P0 (do not recompute unless checksum).  
4. **MUST NOT** run more optimizer steps.

### Q.2 Acceptance

- Hashes match Gate I.  
- Ledger shows 0 additional tokens.

---

## Gate R — Arm A1 extra English

**Purpose.** Matched-budget continuation **on English** so \(C_{\mathrm{en}}\) is not “more training vs less.”

**Host.** CUDA. **GPU: yes.**

### R.1 `base_train` from EN0

- `--load` EN0 final ckpt  
- Fresh Adam  
- LR peak = 0.3 × EN0 peak  
- `--warmup-steps 14` or `min(14, max(1, N_phase2//10))`  
- `--num-iterations` = \(N_{\mathrm{phase2}}\) (294 if PDF uses P1.1 `D_actual`)  
- `NANOCHAT_DATA_DIR=$NANOCHAT_DATA_DIR_EN`  
- `--core-metric-every -1`  
- **MUST NOT** `--target-param-data-ratio -1`

### R.2 During A1

- SHOULD log English val BPB along the run if the PDF names trajectory.  
- Final ckpt SHA256.  
- Upload `a1/d20/` to p2 HF repo.

### R.3 Acceptance

- \(D_{\mathrm{phase2}}\) tokens seen (iteration × \(B\)).  
- Finite BPB.  
- Card `gate-r-a1.json`.

**Do not start A2 on the same GPU without a snapshot of A1 hashes.**

---

## Gate S — Arm A2 Tagalog continuation (treatment)

**Purpose.** The CF intervention.

**Host.** CUDA. **GPU: yes.**

### S.1 `base_train` from the **same** EN0 as A1

- Same load, LR, warmup, \(N\), \(B\), seed policy as A1 except data  
- `NANOCHAT_DATA_DIR=$NANOCHAT_DATA_DIR_TL` (P1.1 train)  
- **MUST NOT** load P1.1 `model_000294.pt`  
- **MUST NOT** train a new tokenizer  
- SHOULD eval English val **during** A2 (trajectory) every \(k\) steps named in PDF (e.g. every 49 steps = 6 points)

### S.2 Replay grid (only if in PDF)

If 1/5/10% named: these are **additional** A2-class runs (`A2-r1`, `A2-r5`, `A2-r10`) with mix shards from Gate E. A2 0% English remains the primary treatment unless the PDF says otherwise.

### S.3 Acceptance

- Same \(D_{\mathrm{phase2}}\) as A1.  
- Trajectory logs if required.  
- `gate-s-a2.json`  
- Upload `a2/d20/`

**STOP if A2 used different \(N\) or LR than A1 without a PDF sentence.**

---

## Gate T — Arm A3 mix (50/50 or filed ratios)

**Purpose.** Replay / specificity.

**Host.** CUDA. **GPU: yes.**

### T.1

- Same optimizer recipe as A1/A2  
- Mix dir from Gate E  
- If 50/50 is confirmatory and 1/5/10 are too, finish **all named** before looking at \(C_{\mathrm{en}}\) as a family (or accept that order is temporal — **SHOULD** precommit analysis order in PDF)

### T.2 Acceptance

- `gate-t-a3.json`  
- Upload `a3/`

---

# STAGE 6 — SEAL, TEST, DEPOSIT

## Gate U — Seal validation BPB (P2 analogue of P1.1 Gate J)

**Purpose.** Official `evaluate_bpb` on **val only**. Compute \(C_{\mathrm{en}}\). No test.

**Host.** CUDA. **GPU: yes in practice.**

### U.1 Table (confirmatory)

For each required depth and arm:

| Arm | English `val_bpb_full` | Tagalog `val_bpb_full` |
|---|---|---|
| Untrained | | |
| A0 | | |
| A1 | | |
| A2 | | |
| A3 | | |
| P1.1 d20 (descriptive, native tok / native val) | n/a or OOD labeled | 1.172248 frozen |

### U.2 Compute

- \(C_{\mathrm{en}} =\) English(A2) − English(A1)  
- Acquisition \(= \) Tagalog(A0) − Tagalog(A2)  
- Apply 0.01 rule  
- If trajectory named: plot English BPB vs PTPP \(R_d = D_{\mathrm{seen}}/D_{\mathrm{phase2}}\)  
- Contamination slices if named

### U.3 MUST NOT

- Touch English test  
- Touch Tagalog test  
- Reopen P1.1 test ledger  
- Rank gaps < 0.01  
- Call A2 “forgetting” if P0-E failed

### U.4 Acceptance

- `gate-u-seal.json` with all val numbers and hashes  
- `test_read_events_p2_english: 0`  
- `test_read_events_p2_tagalog: 0`

**STOP. Choose D\* analogue if any** (default: no depth selection; both d8 and d20 reported). If PDF says pick one parent by A0 English BPB, pick **now** using val only.

---

## Gate V — One test touch (after val seal)

**Purpose.** Generalization check. New P2 ledger, not P1.1’s.

**Host.** CUDA.

### V.1 Order

1. English test **once** on the **precommitted** arms (PDF: A0/A1/A2 or only A2).  
2. Tagalog test **once** on A2 (and A0 if named) using P1.1 `test.jsonl` as **P2 first read**.  
3. Log `docs/run-cards/p2/test_access_log.json` with timestamps.  
4. **MUST NOT** write into P1.1 `test_access_log`.  
5. **MUST NOT** publish P1.1 1.164768 as the A2 test number.  
6. **MUST NOT** a second P2 test read.

### V.2 Acceptance

- One English test batch, one Tagalog test batch, as named.  
- Numbers in `gate-v-test.json`.

---

## Gate W — Deposit, paper, weights

**Purpose.** Make the run auditable.

**Host.** Laptop. **GPU: no.**

### W.1 Deposit

- ResearchBox **new** box: tokenizer, shards hashes, `evaluate_bpb` script, gate JSON, AsPredicted PDF, this protocol.  
- **MUST NOT** deposit `test.jsonl` if P1.1 policy was to keep test isolated — follow the PDF; default **hashes only** for test.  
- HF: all EN0/A1/A2/A3 ckpts on **p2** repo.  
- Model cards: “Not P1.1. Not trained from `p1-fixed-d20-3x`.”

### W.2 Paper

- Fill Stage-1 empty results.  
- Cheng still **not** a coauthor; Cruz & Cheng 2019 cited for TL-39.  
- Shi CPT stage named.  
- Literature lock: analogue not translation; Cruz CF sentence is classifier FT.  
- Spark / MPS in appendix as **non-confirmatory** if mentioned at all.

### W.3 Acceptance

- Public hashes match local.  
- Passcode still gitignored.  
- P1.1 HF repo unchanged.

---

# STAGE 7 — OPTIONAL / EXPLORATORY (label or do not run in confirmatory window)

Do these **after** Gate V, or in parallel on **different** RUN_IDs labeled `p2-exp-*`.

| ID | Item | Allowed as confirmatory? |
|---|---|---|
| X1 | FilBench (EMNLP 2025) | No (appendix) |
| X2 | Tokenizer swap (2311.05741) | No |
| X3 | Infinite LR / WSD (2503.02844) | No |
| X4 | High-PPL mask | No |
| X5 | CKA / layer drift | No |
| X6 | MER merge (2508.01908) | No (code deviation) |
| X7 | EWC (2605.10640: may not move attractor) | No |
| X8 | Llama/FiLLM parent | **Different paper** |
| X9 | Spark unpatched smoke | Host qualification only |
| X10 | House-style probes (dengue, hate-speech) | Later protocol after bilingual parent |

---

## Appendix 1 — Command templates (do not run until the matching gate)

### A1.1 Banned everywhere

```bash
python -m nanochat.dataset
# --target-param-data-ratio -1
# huggingface Trainer
# writing to pageman/nanochat-filipino-p1-fixed-d20-3x
```

### A1.2 `base_train` skeleton (Gate I / R / S / T)

```bash
# source scripts/p2/env.sh   # does not exist until you write it; MUST NOT source scripts/p1/env.sh
export NANOCHAT_BASE_DIR=...
export NANOCHAT_DATA_DIR=...   # EN or TL or MIX
cd vendor/nanochat
python -m scripts.base_train \
  --depth 20 \
  --num-iterations "$N" \
  --total-batch-size 65536 \
  --sequence-len 2048 \
  --warmup-steps "$WARMUP" \
  --core-metric-every -1 \
  --device-batch-size 8
# plus official --load for A1/A2/A3
```

Verify flag names against pinned `scripts/base_train.py` **at Gate A** (do not trust this sketch over the pin).

### A1.3 Full BPB

```bash
python scripts/p2/evaluate_bpb.py --ckpt ... --split val --device cuda
```

---

## Appendix 2 — P1.1 → P2 gate map

| P1.1 | P2-EN→TL |
|---|---|
| Gate A pin | Gate A pin (new cache) |
| Gate B TL parquet | Gate B English archive |
| Gate C hygiene | Gate C hygiene + no P1 overwrite |
| Gate D TL split | Gate D English official splits |
| Gate E shards | Gate E EN + frozen TL copy + mix |
| Gate F Tagalog BPE | Gate F English BPE |
| Gate G \(D_{3x}\) \(N=294\) | Gate G English \(N_{\mathrm{EN0}}\) ≫ 294; phase2 default 294 |
| Gate H Tagalog d4 A40 | Gate H English d4 A40 |
| Gate I d8/12/16/20 Tagalog | Gate I d8/d20 English EN0 |
| Gate J val+test Tagalog | Gate P0 → Q–T → U val seal → V test |
| HF `p1-fixed-d20-3x` | HF `p2-en-then-tl` |

---

## Appendix 3 — Decision tree (one page)

```
PDF filed? --no--> Gate 0 only; wiring pilots unlabeled confirmatory
     |
    yes
Pin clean + no attention patch? --no--> stop
     |
    yes
English archive hashed? --no--> Gate B
     |
    yes
Tagalog train hash = 2b0474c5...? --no--> stop (not P1.1 data)
     |
    yes
English BPE frozen? --no--> Gate F
     |
    yes
Gate G N_EN0 estimated and funded? --no--> do not rent
     |
    yes
CUDA H smoke loss < init, warmup < N, unpatched? --no--> do not start I
     |
    yes
EN0 d8+d20 done? --no--> Gate I
     |
    yes
P0-E pass? --no--> not English-pretrained; no CF claim
     |
    yes
A1 then A2 (same N, LR, load)? --no--> invalid C_en
     |
    yes
Val seal C_en, no test? --no--> Gate U
     |
    yes
One P2 test touch? --then--> deposit on NEW box/repo
```

---

## Appendix 4 — What “previous experiment” looked like (P1.1 actual)

P1.1 executed A–G on Mac; H smoke A40 `p7e5zk3njnglgy` (d4, 30 steps, warmup compatible, H2 10.397→10.084, smoke val BPB 2.915); I A40 `68bei7d3vx4krc` d8/d12/d16/d20 at \(N=294\); J official full BPB; D\*=d20; one test. Spark 2026-08-17 is **not** in that chain.

P2 copies that **shape**: Mac lock and data, A40-class smoke, A40-class long train, official full BPB, one test, new deposit. P2 **adds** P0 and matched A1/A2/A3 and **forbids** using the P1.1 d20 weights as the parent.

---

## Appendix 5 — Materials (P1.1 §5 analogue)

### A5.1 Hardware classes

| Class | Example | Allowed P2 stages | Forbidden |
|---|---|---|---|
| C0 CPU/MPS | Apple Silicon | Gates 0, A–G, W; tokenizer; budget math | Confirmatory H/I/P0/A1–A3; d20 MPS (P1.1 OOM) |
| C1 consumer CUDA | 12–24 GB | Gate H with reduced `--device-batch-size`; maybe EN0 d8 | Do not claim C1 d20 EN0 without an OOM card |
| C2 datacenter CUDA | A40 48 GB (proven P1.1 H/I) | All confirmatory GPU gates | Attention-kernel patches |
| C2b Spark GB10 | `spark-a9f0` SM121 | Workshop only until unpatched smoke < init | Official H/I; ollama left running; `--warmup-steps >= N` |
| C3 8×H100 | nanochat native | Allowed if pin+unpatched; still nanochat-only | ClimbMix speedrun identity |

**Default confirmatory class: C2 A40.** Record `nvidia-smi`, SM capability, torch CUDA version on every GPU card.

### A5.2 Software pin list (fill at Gate A / H)

| Component | Pin policy |
|---|---|
| OS | `uname -a` on Mac and on GPU host |
| NVIDIA driver / CUDA | `nvidia-smi` |
| Python | `uv` / `.venv` in `vendor/nanochat` |
| nanochat | `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` |
| Hook | `patches/nanochat-NANOCHAT_DATA_DIR.patch` only |
| `uv.lock` | Copy into `artifacts/p2/<P2_RUN_ID>/` |
| wandb | `WANDB_RUN=dummy` or disabled |
| P1.1 package | read-only; hashes in §0.6 |

### A5.3 Data sources (only these for confirmatory)

| Role | Source | Status |
|---|---|---|
| English pretrain | WikiText-103 **raw** (Merity et al. 2016, arXiv:1609.07843). PDF MUST name the exact dump (recommended: Hugging Face `Salesforce/wikitext`, config `wikitext-103-raw-v1`, or the Salesforce research zip). | Gate B hashes |
| English literature targets | WT103 train 28,475 articles / 103M Moses tokens (word-level Table 1) | Audit only; BPE \(T_{\mathrm{en,train}}\) is Gate G |
| Tagalog continuation | Frozen P1.1 `reconstructed_article_70_15_15` train | Hash `2b0474c5…7687` |
| Tagalog val | Frozen P1.1 val; packed bytes 5,868,797 | Do not rebuild |
| Tagalog test | Frozen P1.1 `test.jsonl` | P2 Gate V first read; new ledger |
| P1.1 weights | `pageman/nanochat-filipino-p1-fixed-d20-3x` | Reference + optional OOD English control; **not** a parent |
| Dead / banned | ClimbMix, FineWeb, DCLM, OSCAR, TLUnified mix, WikiText-2 substitute, `python -m nanochat.dataset` | Stop |

### A5.4 Directory layout (MUST)

```text
nanochat-filipino/
  docs/papers/p2-cf-english/
    PROTOCOL-p2-en-then-tl.md    # this file
    DIRECTION-RECALIBRATION.md
    paper.tex
    LOCK.json                    # created at Gate 0
    aspredicted-draft-p2.txt     # not the filed PDF
  docs/run-cards/p2/<P2_RUN_ID>/
  scripts/p2/                    # env.sh, evaluate_bpb.py; thin wrappers only
  data/raw/wikitext-103-raw/     # immutable English download
  data/interim/wikitext-103/     # parsed articles
  data/processed/wikitext-103/   # English parquets
  data/processed/wikitext-tl39/  # P1.1; READ-ONLY
  data/processed/p2-mix-*/       # A3 / replay mixes, hashed before Gate I
  data/cache/<P2_RUN_ID>/        # NANOCHAT_BASE_DIR
  artifacts/p2/<P2_RUN_ID>/
  vendor/nanochat/               # detached HEAD at pin
```

```bash
export NANOCHAT_BASE_DIR="$PWD/data/cache/${P2_RUN_ID}"
# MUST NOT use ~/.cache/nanochat if it contains ClimbMix
# MUST NOT source scripts/p1/env.sh
```

### A5.5 License / attribution (MUST on model card)

- WikiText-103: cite Merity et al. 2016; Wikipedia CC BY-SA.  
- WikiText-TL-39: cite Cruz & Cheng 2019; Wikipedia CC BY-SA.  
- nanochat: MIT, retain copyright.  
- Cheng is **not** a coauthor.  
- Attribution block:

> English stage: WikiText-103 (Merity et al., 2016). Filipino continuation: WikiText-TL-39 (Cruz & Cheng, 2019), frozen P1.1 split `reconstructed_article_70_15_15`. This is sequential CPT on nanochat, not a De La Salle / Cruz / Cheng release. P1.1 weights were not used as the English parent.

---

## Appendix 6 — Per-gate launch templates and acceptance tables

Flag names MUST be verified against pinned `scripts/base_train.py` at Gate A. If a flag below does not exist on the pin, the pin wins.

### A6.1 Gate H smoke (confirmatory-path: keep `T=2048` if VRAM allows)

```bash
cd "$P2_ROOT/vendor/nanochat"
export NANOCHAT_BASE_DIR="$P2_ROOT/data/cache/${P2_RUN_ID}"
export NANOCHAT_DATA_DIR="$NANOCHAT_DATA_DIR_EN"
export OMP_NUM_THREADS=1
export WANDB_RUN=dummy

python -m scripts.base_train \
  --depth=4 \
  --max-seq-len=2048 \
  --device-batch-size=8 \
  --total-batch-size=65536 \
  --num-iterations=30 \
  --warmup-steps=3 \
  --eval-tokens=8192 \
  --eval-every=10 \
  --core-metric-every=-1 \
  --sample-every=15 \
  --save-every=30 \
  --model-tag="p2-smoke-en-d4" \
  --run=dummy
```

If OOM: halve `--device-batch-size`, not `--depth`. If still OOM at batch 1, a **labeled** `T=512` smoke MAY prove wiring but **does not** pass confirmatory H for d20 EN0.

| ID | Test | Pass |
|---|---|---|
| H0 | Pin + unpatched `flash_attention.py` | `git rev-parse` + empty diff |
| H1 | Loss finite | train loss finite at last step |
| H2 | Loss moved | last train loss < step-0 train loss |
| H3 | Val moved | last val BPB < first val BPB or < untrained |
| H4 | Checkpoint | reloadable `model_*.pt` |
| H5 | Warmup legal | `--warmup-steps` < `--num-iterations` |
| H6 | No CORE fetch | no DCLM bundle |
| H7 | Language | samples are English-ish or garbage; **not** Tagalog Wikipedia boilerplate from a wrong `NANOCHAT_DATA_DIR` |

If H7 is fluent Tagalog about Philippine history at step 30 on an “English” smoke: **wrong data dir**. Wipe cache. Stop.

### A6.2 Gate I EN0 (d8 then d20)

```bash
python -m scripts.base_train \
  --depth=${D} \
  --max-seq-len=2048 \
  --device-batch-size=8 \
  --total-batch-size=65536 \
  --num-iterations=${N_EN0} \
  --warmup-steps=${WARMUP_EN0} \
  --eval-tokens=${EVAL_TOKENS_EN} \
  --eval-every=50 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --save-every=200 \
  --model-tag="p2-en0-d${D}" \
  --run="p2-en0-d${D}"
```

`--eval-tokens` MUST be `min(262144, 0.5 * T_en_val)` and at least 8192 if val allows (P1.1 rule).  
`--warmup-steps` SHOULD be `min(40, 5% of N_EN0)` and MUST be `< N_EN0`.  
`--target-param-data-ratio` if passed MUST be positive; MUST NOT be `-1`. Prefer omitting it and passing `--num-iterations` only if the pin allows.

**Logging every 50 steps (MUST):** step, wall time, tokens seen, epoch index `tokens_seen / T_en_train`, train NLL/BPB, val BPB when eval runs, tok/s, MFU, VRAM, LRs. Local `metrics.jsonl` is the archive; wandb is not.

**Checkpoint policy:** confirmatory EN0 = **final** step \(N_{\mathrm{EN0}}\), not mid-run val-best, unless the PDF names otherwise.

**Fixed English sample prompts (do not cherry-pick later):**

1. `The history of`  
2. `= United States =`  
3. `In 1991,`

### A6.3 Gate R/S/T continuation

Same template as A6.2 plus official load of EN0 final ckpt, fresh Adam, LR peak `0.3 * EN0_peak`, `--num-iterations=${N_PHASE2}`, `--warmup-steps` = `min(14, max(1, N_PHASE2//10))`.

A2 sample prompts (qualitative only):

1. `Ang Pilipinas ay`  
2. `Noong ika-`  
3. `= Kasaysayan =`

A2 English trajectory eval (SHOULD / confirmatory if PDF): every `max(1, N_PHASE2//6)` steps, English `val_bpb_full` on a **fixed** eval-token budget named before the run.

### A6.4 Gate U evaluator

`scripts/p2/evaluate_bpb.py` is a copy of `scripts/p1/gate_j_full_bpb.py` frozen **before** Gate I. Same packing, `T=2048`, BOS-bestfit.

Report: `val_bpb_full`, `val_nll_mean`, `val_bytes`, `val_tokens` for each arm × language.

Untrained same-depth and, for Tagalog columns, P1.1 byte-unigram 4.453225 is a **P1.1 historical** number (Tagalog BPE). P2 SHOULD fit a **new** byte unigram on English train UTF-8 for the English table.

### A6.5 Run card template (one per arm)

Copy to `docs/run-cards/p2/${P2_RUN_ID}/${ARM}.md`:

```markdown
# P2 run card ${P2_RUN_ID} / ${ARM}

- Protocol: P2-EN→TL
- AsPredicted (new id / URL / PDF SHA256):
- Date (UTC):
- Operator:
- Hardware class / nvidia-smi / SM:
- nanochat commit:
- flash_attention.py diff vs pin: empty / NOT EMPTY (fail)
- NANOCHAT_BASE_DIR:
- NANOCHAT_DATA_DIR:
- English archive SHA256s:
- Tagalog train SHA256: 2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687
- English tokenizer SHA256:
- Depth / P_total / P_scaling:
- max_seq_len / device_batch / total_batch / iterations / warmup:
- T_en_train / D_3x_en / D_phase2 / D_actual:
- load ckpt SHA256 (empty for EN0):
- LR peak / 0.3 rule:
- English val_bpb_full / Tagalog val_bpb_full:
- C_en (after A1 and A2 exist):
- Deviations:
- Pass/fail: 0 A B C D E F G H I P0 Q R S T U V W
```

---

## Appendix 7 — Statistical analysis plan

1. **Primary:** \(C_{\mathrm{en}}\) from **final** English `val_bpb_full` of A2 vs A1, same depth, seed 0. Gaps \(< 0.01\) BPB are not rankings.  
2. **Primary acquisition:** Tagalog `val_bpb_full` A0 vs A2, same English BPE, same P1.1 val UTF-8. Gaps \(< 0.01\) not rankings. P1.1 Table 2 (1.172248) is **descriptive**, different tokenizer.  
3. **P0-E:** EN0 vs untrained English, same English BPE, gap ≥ 0.01 required to call the parent English-pretrained.  
4. **A3 / replay:** if named in PDF, compare \(C_{\mathrm{en}}\) across replay ratios; if not named, exploratory.  
5. **Trajectory:** if named, English BPB vs \(R_d = D_{\mathrm{seen}}/D_{\mathrm{phase2}}\) on A2; descriptive SHOULD even if not a hypothesis.  
6. **Seeds:** one seed allowed for the pipeline paper. Any “d20 forgets more than d8” claim MUST be labeled secondary; with one seed, point estimates only.  
7. **Test:** English and Tagalog test once after Gate U; MUST NOT retune.  
8. **No HARKing:** adding 1/5/10% replay, FilBench, EWC, or tokenizer swap after seeing \(C_{\mathrm{en}}\) is post hoc / exploratory.  
9. **Cross-tokenizer inequalities are invalid.** Do not test EN0 English-BPE BPB against 1.172248.

---

## Appendix 8 — Failure modes and recovery

| Symptom | Likely cause | Action |
|---|---|---|
| Fluent Tagalog in English smoke | Wrong `NANOCHAT_DATA_DIR` | Wipe P2 cache; restart Gate E/H |
| Fluent English about ClimbMix-style web crawl | ClimbMix in cache | Wipe; never `python -m nanochat.dataset` |
| Loss rose after step 20 on 30-step smoke | `--warmup-steps` default 40 ≥ \(N\) | Set warmup `< N`; see Spark 2026-08-17 card |
| Compile / FA3 crash on SM121 | Pin FA3 detector | Do not patch attention; move to A40 |
| Val BPB ≪ train | Val leaked into train or last-shard wrong | Re-run Gate E |
| EN0 English BPB ≈ untrained | Broken train, empty texts, LR | Fail P0-E; do not run A2 as CF |
| A2 English BPB using P1.1 tokenizer | Wrong tok | Stop; all P2 arms use Gate F English BPE |
| Loaded `9e30fff3…` as `--load` | P1.1 parent mistake | Invalidate arm; new RUN_ID |
| OOM d20 | `device-batch-size` | Halve batch; new card; do not drop T on confirmatory EN0 |
| `get_base_dir()` wrong under torchrun | Export not inherited | Wrapper script exports all vars |
| Hash mismatch Tagalog train | Not P1.1 data | Stop |
| Second P1.1 test read in P1.1 ledger | Ledger confusion | P2 uses its own `test_access_log` |

---

## Appendix 9 — Timeline (elapsed work, not GPU hours)

| Day | Gates | Host | Deliverable |
|---|---|---|---|
| 0 | Gate 0 | Laptop | Filed AsPredicted PDF, `LOCK.json`, ResearchBox empty box |
| 0–1 | A–C | Mac | Pin, English download hashes, hygiene |
| 1–2 | D–E | Mac | English splits/shards; TL copy verified; mix shards hashed |
| 2 | F–G | Mac | English BPE; \(T_{\mathrm{en,train}}\); \(N_{\mathrm{EN0}}\); **cost estimate** |
| 3 | H | A40 | English d4 smoke H0–H7 |
| 3–? | I | A40 | EN0 d8 then d20; duration = \(N_{\mathrm{EN0}}\) / measured tok/s (**may be many days**; WT103 ≫ TL-39) |
| +1 | P0, Q | A40 | Provenance; A0 freeze |
| +1–2 | R, S, T | A40 | A1, A2, A3 at \(N_{\mathrm{phase2}}=294\) default (hours, not days, if 294) |
| +1 | U | A40 | Val seal, \(C_{\mathrm{en}}\) |
| +0 | V | A40 | One English test, one Tagalog test |
| +1 | W | Laptop | HF p2 repo, new ResearchBox, fill `paper.tex` |

Do not start Day-3 rental until Gate G cost is written. If EN0 is quoted in weeks of A40, that is a **scientific cost**, not a reason to switch to Llama.

---

## Appendix 10 — Confirmatory vs exploratory checklist (print at Gate 0)

Tick **only** what the filed PDF names. Unticked items that you run anyway are exploratory.

- [ ] EN0 d8 + d20, WikiText-103 raw, English 32768 BPE  
- [ ] P0-E (EN0 English beats untrained by ≥ 0.01)  
- [ ] A0 freeze dual val BPB  
- [ ] A1 extra English \(D_{\mathrm{phase2}}\)  
- [ ] A2 Tagalog \(D_{\mathrm{phase2}}\) from EN0 (not from P1.1 d20)  
- [ ] A3 50/50 documents  
- [ ] Replay 1%  
- [ ] Replay 5%  
- [ ] Replay 10%  
- [ ] A2 English BPB trajectory  
- [ ] \(C_{\mathrm{en}}\) vs PTPP \(R_d\) as a hypothesis (else descriptive)  
- [ ] Entity / overlap slice BPB as a hypothesis (else SHOULD robustness)  
- [ ] d20 vs d8 \(C_{\mathrm{en}}\) capacity prior  
- [ ] \(D_{\mathrm{phase2}} = 19267584\) **xor** English \(D_{3x}\) (circle one in PDF)

Never tick: CORE primary, SFT, EWC primary, HF Trainer, FilBench Table 1, Spark patch, amend #306780.

---

## Appendix 11 — Exact P1.1 hashes this protocol consumes

| Object | SHA256 |
|---|---|
| AsPredicted #306780 PDF | `a34f119df557d2e763aa154e02b76b0ebcbcba1f3fb32c3219d85ae6395cc5ca` |
| P1.1 tokenizer | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| P1.1 train split | `2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687` |
| P1.1 d20 `model_000294.pt` | `9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38` |
| nanochat pin | `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` |

English WT103 file hashes: **unknown until Gate B**. Do not invent them.

---

**Document status:** execution protocol, 2026-08-17. Not an AsPredicted amendment. Not a results paper. Fill `LOCK.json` at Gate 0. Write `scripts/p2/env.sh` at Gate A (do not source P1 env). File the PDF before Gate I. Authority after filing: new PDF ≫ this protocol ≫ `DIRECTION-RECALIBRATION.md` ≫ `paper.tex`.
