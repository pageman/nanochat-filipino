# Protocol P4 — Token-Share-Locked English–Tagalog Mixture Trade-Off after a Fresh Tagalog Parent (nanochat)

**Document type:** Pre-analysis execution protocol (sibling of P1.1, P2-EN→TL, P3-TL→EN).  
**Study short name:** P4-C3-TOKEN-SHARE  
**Provisional Hub (only after Gate I starts; never P1.1/P2/P3 Hub):** `pageman/nanochat-filipino-p4-token-share-mix`  
**Status as of 2026-08-21:** Draft execution protocol **only**. **P4 AsPredicted not filed.** No `P4_RUN_ID`. No P4 parent. No C1/C2/C3. No `val_bpb_full`. No test. **MUST NOT start Gate A until Gate 0 passes.**  
**Authority after filing:** filed P4 AsPredicted PDF ≫ dated pre-start execution clarifications ≫ this protocol ≫ `docs/papers/p4-token-share-mix/LOCK.json` ≫ gate ledger and run cards ≫ dated deviation card ≫ exploratory work ≫ chat.  
**Does not amend:** AsPredicted #306780, #306935, #307342; ResearchBox #8735, #8763, #8834; P1.1, P2, or P3 Hub repos.  
**Recommended nanochat pin (file the actual pin in Gate 0):** `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` (same as P1.1/P2/P3 unless the PDF names another commit).  
**Hook only:** `patches/nanochat-NANOCHAT_DATA_DIR.patch`. **MUST NOT** edit attention, loss, optimizer, or `evaluate_bpb` semantics without prefiling disclosure.  
**This document does not authorize:** training, evaluation, test access, a new registration filing, cloud rental, model release, or any modification of P1.1, P2, or P3 artifacts.

> **C3 is a newly constructed P4 tokenizer-token-share-locked mixture. It is not P3 `B3`, which was a separate pre-frozen equal-document mixture.**

---

## 1. Executive protocol summary

P4 is a **post-P3, outcome-informed, exposure-matched mixture trade-off study**. After a **newly trained** P4 Tagalog parent (fresh random initialization; frozen P1.1/P3-eligible WikiText-TL-39 train documents) passes **P0-T**, freeze d20 as immutable **C0** and continue it for one shared phase-two model-visible token budget on three child streams: **C1** extra Tagalog, **C2** pure English, **C3** a prospectively frozen mixture whose **P4-tokenizer-encoded token share** is locked at a single filed \(q_{\mathrm{TL}}\). Co-primary confirmatory estimands are full-split validation BPB contrasts \(R_{\mathrm{TL}}=\mathrm{TL}(C3)-\mathrm{TL}(C2)\le -\delta\) and \(A_{\mathrm{EN}}=\mathrm{EN}(C3)-\mathrm{EN}(C1)\le -\delta\). C3 is frozen **before any P4 confirmatory BPB**. Validation seals **before** any test. Default recommended test policy is **C3-only, one authorized event**. One seed. NVIDIA CUDA for confirmatory GPU gates. The word **mitigation** is prohibited in title, abstract, and preregistration until after unblinding, and then only with the narrow filed meaning.

**One exposure clock:** P4 tokenizer-encoded model-visible tokens. P4 **does not claim byte balancing**. Byte share and document share are descriptive.

**This protocol does not start a process.** Several scientific choices remain **UNRESOLVED BEFORE FILING** (§18). Recommended values below are **not frozen** until signed into the AsPredicted PDF.

---

## 2. Study identity and authority hierarchy

### 2.1 Identity (frozen after Gate 0)

| Item | Value / freeze class |
|---|---|
| Study | `p4_token_share_locked_mix` |
| Short name | P4-C3-TOKEN-SHARE |
| Registration ID | **UNRESOLVED BEFORE FILING** (AsPredicted number after PDF exists) |
| ResearchBox | **UNRESOLVED BEFORE FILING** |
| AsCollected | **UNRESOLVED BEFORE FILING** |
| `P4_RUN_ID` | **Forbidden until Gate 0.** Format after filing: `p4-<UTC>Z-<7-char pin>` |
| Protocol path | `docs/papers/p4-token-share-mix/PROTOCOL-p4-token-share-mix.md` |
| Protocol SHA-256 | **Frozen at Gate 0** after last pre-filing edit |
| Code commit | File exact pin in Gate 0; recommended `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` |
| Author | Paul Pajo |
| Operator roles | Operator (gates); lockbox custodian (distinct if possible); unblinding officer at Gate X |

### 2.2 Authority stack (verbatim)

> Filed P4 registration PDF > dated pre-start execution clarifications > `LOCK.json` > gate ledger and run cards > dated deviation card > exploratory work > chat.

No document may silently override a higher-authority document. Chat **MUST NOT** rewrite sealed numbers or filed constants.

### 2.3 Gate language

Status labels **MUST** be only: `not_started`, `prepared`, `pass`, `blocked`, `technical_stop`, `protocol_stop`, `awaiting_authorization`.

- **MUST** — required for confirmatory P4.  
- **MUST NOT** — forbidden; a violation invalidates the confirmatory label.  
- **SHOULD** — default; dated deviation if skipped.  
- **MAY** — optional; exploratory unless the PDF already names it.

### 2.4 Two naming systems

| Name | What it is | Example |
|---|---|---|
| Gates 0, A–I, P0-T, Q–W, X | Hard-stop checkpoints | Gate E = pack streams + freeze C3 |
| Arms C0, C1, C2, C3 | Weight states | C3 = token-share-locked mix continuation |
| P3 arms B0–B3 | Finished study | **Never** a P4 parent or C3 source |

**C0 is not Gate 0.** Gate 0 is filing. C0 is frozen P4 d20 parent.

---

## 3. Background and post-P3 disclosure

### 3.1 What prior studies established for P4’s *design logic* (not as P4 evidence)

| Prior study | What it established for P4’s design logic |
|---|---|
| **P1.1** (#306780 / RB #8735) | Protected Tagalog LM apparatus: frozen WikiText-TL-39-derived splits, train-only tokenizer, fixed model-visible exposure, full held-out validation, restricted test. |
| **P2** (#306935 / RB #8763) | Forward EN→TL matched-branch study. Acquisition and old-language cost need an **active continuation control**, not a raw before/after. |
| **P3** (#307342 / RB #8834) | Reverse TL→EN matched-branch study: B1 extra Tagalog, B2 pure English, B3 equal-**document** mix. B3 was ≈50% by document count and ≈96% English by UTF-8 bytes, so it **cannot** answer a tokenizer-token-share mixture question. |

### 3.2 Mandatory public grammar (sentence 1 of the P4 AsPredicted form)

P4 was designed **after the released P3 findings and after the P3 B3 document/byte-share ambiguity were known** (P3 Gate X 2026-08-20). It is a **post-P3, prospectively preregistered exposure-matched mixture trade-off study**. It is **not** an amendment, correction, rescue, replication, or reinterpretation of P3. It is **not** “P3 B3 fixed.”

P3 sealed magnitudes (\(C_{\mathrm{tl}}=1.023484\), \(G_{\mathrm{en}}=-1.697955\), B3 cells, Gate V tests) **MUST NOT** be used as calibration targets, selection rules, or success-threshold tuners for \(q_{\mathrm{TL}}\), \(\delta\), mix construction, depth, or budget.

### 3.3 What P4 is not

- not an amendment of #306780, #306935, or #307342;  
- not “50/50 documents should mean 50/50 exposure”;  
- not a general test of bilingual training, an optimal mixture ratio, or a general solution to catastrophic forgetting;  
- not SFT, instruction-tuning, replay, EWC, CORE, FilBench, or chat;  
- not an opportunity to tune a mixture ratio after examining fertility, loss, validation BPB, samples, or tests;  
- not a claim that a document-balanced stream is token-balanced.

---

## 4. Research question, estimands, hypotheses, and claim grammar

### 4.1 Substantive question

After a newly trained, P0-T-eligible Tagalog parent, and under the same fixed phase-two model-visible token budget for every child branch, does a prospectively frozen English–Tagalog mixture with a locked share of **P4 model-tokenizer encoded tokens** reduce held-out Tagalog BPB relative to pure English continuation while still improving held-out English BPB relative to extra Tagalog continuation?

### 4.2 Branches (new family; not P3 B labels)

| P4 branch | Stream | Role |
|---|---|---|
| C0 | Frozen P4 TL d20 parent | Immutable parent; 0 additional train tokens at freeze |
| C1 | Extra Tagalog only | Source-language active continuation control |
| C2 | Pure English only | English intervention / pure-stream retention-cost comparator |
| C3 | Pre-frozen token-share-locked EN/TL mix | New mixture intervention |

> **C3 is a newly constructed P4 tokenizer-token-share-locked mixture. It is not P3 `B3`, which was a separate pre-frozen equal-document mixture.**

### 4.3 Outcome definition

Official DV is **full-split held-out validation BPB** after the **terminal** checkpoint, using the frozen P4 evaluator:

\[
\mathrm{BPB}=\frac{\overline{\mathrm{NLL}}_{\mathrm{token}}}{\ln 2\cdot \overline{\mathrm{UTF8\ bytes\ per\ evaluated\ token}}}.
\]

In-loop trainer `val_bpb` / `meta_*.json` `val_bpb` is **monitoring only** and has **no confirmatory or selection role**.

\(\mathrm{TL}(X)\) = Tagalog `val_bpb_full` for branch \(X\).  
\(\mathrm{EN}(X)\) = English `val_bpb_full` for branch \(X\).

### 4.4 Co-primary contrasts

| Symbol | Formula | Question answered | Required direction |
|---|---|---|---|
| \(R_{\mathrm{TL}}\) | \(\mathrm{TL}(C3)-\mathrm{TL}(C2)\) | Does C3 retain more Tagalog than pure English continuation? | \(R_{\mathrm{TL}}\le -\delta\) |
| \(A_{\mathrm{EN}}\) | \(\mathrm{EN}(C3)-\mathrm{EN}(C1)\) | Does C3 still acquire more English than extra Tagalog continuation? | \(A_{\mathrm{EN}}\le -\delta\) |

Equality at \(-\delta\) **counts as meeting** the threshold (closed interval). Reporting precision: six decimal places, matching P1.1/P2/P3.

\(\delta\) is **both** a practical-significance rule **and** the confirmatory success boundary, once filed. **Recommended (not frozen):** \(\delta=0.01\) BPB (carry-forward of the existing cutoff family; **not** tuned to P3 magnitudes). **Status:** UNRESOLVED BEFORE FILING until signed.

**MUST NOT** create a weighted composite, Pareto score, utility, normalized rank, or post-hoc “best arm” rule. A descriptive 2-D trade-off figure **MAY** be planned; it has **no decision authority** beyond the two predeclared contrasts.

Descriptive (not success criteria): \(\mathrm{TL}(C1)\), \(\mathrm{TL}(C2)\), \(\mathrm{EN}(C2)\), C0 English val if filed, byte/document shares, fertility.

### 4.5 Outcome grammar (file before any P4 BPB)

| Condition | Allowed conclusion |
|---|---|
| Both \(R_{\mathrm{TL}}\) and \(A_{\mathrm{EN}}\) meet thresholds | “Under this preregistered token-share-locked mixture, P4 observed lower Tagalog BPB than pure English continuation and lower English BPB than extra Tagalog continuation in the stated apparatus.” |
| Only \(R_{\mathrm{TL}}\) | “The specified mixture improved Tagalog retention relative to pure English continuation but did not meet the preregistered English-acquisition criterion.” |
| Only \(A_{\mathrm{EN}}\) | “The specified mixture improved English acquisition relative to extra Tagalog continuation but did not meet the preregistered Tagalog-retention criterion.” |
| Neither | “The specified mixture did not meet either preregistered trade-off criterion.” |

**Mitigation** is prohibited in preregistration, title, and abstract until after unblinding. After unblinding it **MAY** be used **only if both co-primary criteria are met**, and only with this meaning:

> A measured reduction in the P3-style relative Tagalog retention cost within this frozen P4 apparatus, not a general mitigation of catastrophic forgetting.

One seed: **MUST NOT** claim significance, CI, or a population law.

### 4.6 Parent-eligibility hypothesis (P0-T)

P4 d8 and d20 Tagalog `val_bpb_full` each beat (i) untrained same-depth same-tokenizer and (ii) Tagalog-train add-1 UTF-8 byte-unigram on full Tagalog val by \(\ge\delta_{\mathrm{P0T}}\). **Recommended:** \(\delta_{\mathrm{P0T}}=\delta=0.01\). If either depth fails either floor: **MUST NOT** run C1/C2/C3; report blocked parent-eligibility.

---

## 5. Frozen design table

### 5.1 Exposure clock (one clock)

**Primary exposure clock:** proportion of C3 phase-two **source-content tokens** after encoding each eligible train document with the frozen P4 Tagalog tokenizer (**no BOS, no padding, no pack, no crop**). Target share is \(q_{\mathrm{TL}}\) Tagalog tokens and \(1-q_{\mathrm{TL}}\) English tokens across the complete C3 construction stream (after integer rounding). Trainer packing **MUST NOT** redefine this quota. “Model-visible” in child **step budget** \(D_{\mathrm{phase2}}=N\times B\) is the trainer consumption clock; it is not a license to count BOS/pad positions in \(q_{\mathrm{TL}}\).

| Quantity | Function | Confirmatory authority |
|---|---|---|
| P4 tokenizer-encoded token share | Defines the C3 treatment dose | **Yes** |
| UTF-8 byte share | Describes corpus exposure | No |
| Document share | Describes corpus composition | No |
| P4 tokenizer fertility by language | Descriptive diagnostic | No |
| English-tokenizer fertility, if computed | Optional descriptive diagnostic | No |
| Unique-document count / revisit rate | Describes stream construction | No |

P4 **does not claim byte balancing**. Byte share **MUST** be reported, not optimized. A byte-balanced study is a **separate later registration** (`P6-B`). **MUST NOT** add a byte-balanced C4 arm after filing.

**Recommended \(q_{\mathrm{TL}}=0.50\).** **Status:** UNRESOLVED BEFORE FILING.

### 5.2 P4 Frozen Constants and Decision Register

Freeze class: **F** = frozen before filing (or recommended carry-forward awaiting signature); **G** = frozen after filing but before the named gate; **R** = recorded during execution without influencing a decision; **X** = forbidden from influencing the study.

| Category | Item | Value / status | Authority | Freeze | Hash | Change class |
|---|---|---|---|---|---|---|
| Identity | Registration ID | UNRESOLVED BEFORE FILING | PDF | Gate 0 | PDF SHA | Amendment |
| Identity | `P4_RUN_ID` | Forbidden until Gate 0 | LOCK | Gate 0 | — | Stop if invented early |
| Identity | Protocol SHA | At Gate 0 | Protocol | Gate 0 | SHA-256 | Amendment if after A |
| Code | nanochat pin | Rec. `92d63d4…` | PDF | Gate 0/A | commit | Amendment |
| Code | Env | `scripts/p4/env.sh` only | Protocol | Gate A | script SHA | Deviation/stop |
| Hardware | Confirmatory device | NVIDIA CUDA only | Protocol | Gate 0 | host card | Protocol stop if MPS/CPU/TPU used for H–V |
| Hardware | Device class | Rec. A40 48 GB | PDF | Gate 0 | nvidia-smi | Deviation if other NVIDIA class filed |
| Corpora | TL train jsonl | SHA `2b0474c5…` (full §6) | P1.1/P3 freeze | Gate D | SHA-256 | Protocol stop |
| Corpora | TL val | SHA `4d51644b…` | P1.1/P3 | Gate D | SHA-256 | Protocol stop |
| Corpora | TL test | SHA `3bd19345…` | P1.1/P3 | Gate D | SHA-256 | Unmount from train |
| Corpora | EN train | SHA `09ae691c…` | P3 freeze | Gate D | SHA-256 | Protocol stop |
| Corpora | EN val | SHA `874dec29…` | P3 | Gate D | SHA-256 | Protocol stop |
| Corpora | EN test | SHA `2bccabc0…` | P3 | Gate D | SHA-256 | Unmount from train |
| Tokenizer | Policy | Rec. **carry-forward** P3 pair | PDF | Gate 0 | both SHAs | Amendment if switched |
| Tokenizer | `tokenizer.pkl` | Rec. `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` | P3 | Gate F | SHA-256 | Protocol stop if mismatch |
| Tokenizer | `token_bytes.pt` | Rec. `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132` | P3 | Gate F | SHA-256 | Protocol stop if mismatch; **do not** carry-forward without this hash |
| Parent | Depths | Rec. d8 + d20; C0 = d20 | PDF | Gate 0 | — | Amendment |
| Parent | \(T\) | 2048 | Carry-forward | Gate G | — | Amendment |
| Parent | \(B\) | 65536 | Carry-forward | Gate G | — | Amendment |
| Parent | \(N_{\mathrm{TL0}}\) | Rec. 294 if tokenizer carried forward | Gate G compute | Gate G | — | Deviation if Gate G integer differs **and** PDF said “use Gate G integer” |
| Phase two | \(N\) | Rec. 294 | PDF | Gate G | — | Amendment |
| Phase two | \(D_{\mathrm{phase2}}\) | Rec. \(294\times 65536=19{,}267{,}584\) | PDF | Gate G | — | Amendment |
| Phase two | Optimizer | Fresh Muon+AdamW; `load_optimizer=False` | Protocol | Gate G | — | Protocol stop if resume parent opt |
| Phase two | Peak LR | Rec. \(0.3\times\) parent peak; warmup 14 | Carry-forward mechanics | Gate G | — | Amendment |
| Phase two | Checkpoint | Terminal only; no mid-run selection | Protocol | Gate G | — | Protocol stop |
| C3 | \(q_{\mathrm{TL}}\) | UNRESOLVED; rec. 0.50 | PDF | Gate 0 | manifest | Amendment / stop after outcomes |
| C3 | Rounding | See §7; residual language filed | PDF | Gate E | manifest | Amendment |
| C3 | Construction seed | UNRESOLVED; rec. 42 | PDF | Gate E | manifest | Amendment |
| C3 | Interleave | Rec. deterministic block schedule | PDF | Gate E | digest | Amendment |
| C3 | Tolerance | Rec. exact integer match (0 token slack if \(D q\) integer) | PDF | Gate E | — | Protocol stop if outside |
| Eval | Formula | §4.3 | Protocol | Gate 0 | evaluator SHA | Amendment |
| Eval | Device | CUDA for official U/V | Protocol | Gate U | — | Protocol stop |
| Thresholds | \(\delta\) | UNRESOLVED; rec. 0.01 | PDF | Gate 0 | — | Amendment / stop after outcomes |
| Testing | Policy | UNRESOLVED; rec. **A** C3-only one event | PDF | Gate 0 | — | Amendment |
| Release | Hub | C0+C1+C2+C3 together or all deferred | Protocol | Gate W | SHA256SUMS | Protocol stop if C3 alone |

**MUST NOT** select by mid-run min val, sample quality, preferred loss curve, wall-clock, GPU util, fertility, or post-hoc linguistic plausibility.

---

## 6. Data, split, tokenizer, and hygiene

### 6.1 Sources (historical freeze; copy hashes, do not re-split)

Tagalog: frozen P1.1 reconstructed-article `70/15/15` (`reconstructed_article_70_15_15`).  
English: WikiText-103-raw, Hugging Face `Salesforce/wikitext`, config `wikitext-103-raw-v1` (P3 freeze).

| Split | Path (logical) | SHA-256 |
|---|---|---|
| TL train | `data/interim/wikitext-tl39/splits/train.jsonl` | `2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687` |
| TL val | `data/interim/wikitext-tl39/splits/val.jsonl` | `4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c` |
| TL test | `data/processed/wikitext-tl39/test/test.jsonl` | `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf` |
| EN train | `data/interim/wikitext-103/english_train.jsonl` | `09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a` |
| EN val | `data/interim/wikitext-103/english_val.jsonl` | `874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b` |
| EN test | `data/interim/wikitext-103/english_test.jsonl` | `2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e` |

Cleaning: **not used on official P4 confirmatory JSONLs.** Those files are byte-identical copies of the named frozen splits; mismatch = protocol stop. The historical LF / drop-null / \(>200{,}000\)-char rule applies only to a separately named raw-source reconstruction path, which P4 does not use. Tests stay outside train/tokenizer mounts.

### 6.2 Tokenizer policy (choose one before filing)

| Policy | Meaning | Recommendation |
|---|---|---|
| **Carry-forward** | Reuse exact P3 Tagalog tokenizer artifact/hash; train a **fresh P4 parent** | **Recommended.** Isolates the new mixture treatment from tokenizer variation. Reusing a tokenizer is **not** reusing P3 weights. |
| **Fresh P4 tokenizer** | Retrain on frozen Tagalog train with a fully locked recipe | Allowed only if determinism, seed, command, and hash policy are fully specified **before filing**. Changes the treatment unit. |

**Status:** UNRESOLVED BEFORE FILING. This protocol **recommends carry-forward** (`04436b85…`).

Token accounting for C3 quotas: encode each eligible **train** document with the frozen tokenizer, **no BOS, no padding, no pack, no crop** (same class as P3 \(T_{\mathrm{TL,train}}\) accounting). Packing for the trainer is a later step and **MUST NOT** redefine the quota.

### 6.3 Hygiene (MUST)

1. No ClimbMix, FineWeb, DCLM, OSCAR, scraped web, synthetic instruction, or undeclared auxiliary corpora in parent or continuation streams.  
2. No P1.1/P2/P3 `.pt` in P4 cache, parent directory, initializer path, or load command.  
3. P4 test files absent/unmounted from all parent and child **training** directories.  
4. P1.1/P2/P3 test values **never** read to calibrate P4 \(\delta\) or \(q_{\mathrm{TL}}\).  
5. P3 B3 is never regenerated or used as a live P4 training arm.  
6. P3 B3 metadata may be cited only as **historical motivation**, not P4 evidence.  
7. C3 mix is created only from frozen P4-eligible **training** documents.  
8. English and Tagalog **validation** documents are never C3 construction inputs.  
9. P4 test sources are not accessed before Gate V.  
10. Secrets, passcodes, API tokens, SSH private keys, and ResearchBox credentials are excluded from repo, paper, archive, and manifest.  
11. Submitted registration forms and ResearchBox passcodes stay gitignored.  
12. Every source file, stream, tokenizer, parent, branch, evaluator, and report has a hash and a provenance path.

Also: document-overlap, split-identity, source-revision, and permission (read-only after freeze) checks at Gates C–E.

### 6.4 Environment isolation (verbatim prohibitions)

```text
scripts/p4/env.sh
scripts/p4/env.cuda.sh
data/cache/<P4_RUN_ID>/
docs/run-cards/p4/<P4_RUN_ID>/
docs/papers/p4-token-share-mix/LOCK.json
```

```text
Never source scripts/p1/env.sh.
Never source scripts/p2/env.sh.
Never source scripts/p3/env.sh.
Never load P1.1, P2, or P3 model weights as a P4 parent.
Never use ratio=-1.
Never run python -m nanochat.dataset.
Never write P4 outputs to P1.1, P2, or P3 cache paths.
```

Non-CUDA systems **MAY** perform static Gates 0, A–G, X, W only. Confirmatory Gates **H, I, P0-T, R, S, T, U, V** **MUST** use NVIDIA CUDA.

CUDA preflight: GPU model, `nvidia-smi`, CUDA visibility, torch version, CUDA runtime, disk space, free VRAM, code commit, data/tokenizer/parent hashes, tests absent from training dirs, no stray training process.

---

## 7. Exact C3 token-share construction specification

Full algorithm also lives in `P4-MIX-CONSTRUCTION-SPEC.md`. Summary here is binding.

### 7.1 Proof that C3 is not P3 B3

| Axis | P3 B3 | P4 C3 |
|---|---|---|
| Treatment definition | 50/50 **documents** | Locked **P4-tokenizer token share** \(q_{\mathrm{TL}}\) |
| Share unit | Documents (bytes descriptive) | Model tokens (bytes descriptive) |
| Manifest identity | P3 mix-order SHA `b6ae432b…` | New `p4_mix_manifest.json` / `full_stream_sha256` |
| Parent | P3 B0 | Fresh P4 C0 |
| Ledger | P3 Gate E | Fresh P4 Gate E |
| Label | B3 | C3 |

### 7.2 Construction steps (MUST complete before parent confirmatory BPB)

1. Freeze eligible EN and TL **training** document lists by hash (Gate D).  
2. Encode each eligible document with the frozen P4 Tagalog tokenizer under no-BOS / no-padding accounting. Persist per-document token counts.  
3. Freeze PRNG algorithm and integer seeds (document order; interleave). **Recommended algorithm:** Python 3 `random.Random` with documented version, or `numpy.random.Generator(PCG64)` — **UNRESOLVED BEFORE FILING** which library; **MUST** pick one before Gate E. **Recommended seed:** 42.  
4. Target totals from \(D_{\mathrm{phase2}}\) and \(q_{\mathrm{TL}}\). Let \(T_{\mathrm{TL}}^{\star}=\mathrm{round}(q_{\mathrm{TL}} D_{\mathrm{phase2}})\) with **round-half-to-even**, then \(T_{\mathrm{EN}}^{\star}=D_{\mathrm{phase2}}-T_{\mathrm{TL}}^{\star}\) (English receives residual so the sum is exact). If \(q_{\mathrm{TL}}=0.5\) and \(D_{\mathrm{phase2}}\) is even, both targets are exact halves (\(9{,}633{,}792\) each at recommended \(D\)).  
5. Fill quotas **without** inspecting loss or BPB. Walk SHA-sorted-then-seed-shuffled document lists independently per language. Concatenate encoded tokens until the language quota is met.  
6. **Truncation:** the last document of a language **MAY** be truncated at a token boundary to hit the integer quota exactly. Truncation offset **MUST** be recorded. **Revisit:** if a language’s unique documents exhaust before quota, **revisit** from the start of that language’s shuffled list (cyclic). Skip empty encodings. **MUST NOT** skip documents to chase a byte share.  
7. **Interleave (recommended):** deterministic **block schedule**. Let block size \(K_{\mathrm{blk}}\) be **UNRESOLVED BEFORE FILING**; recommended \(K_{\mathrm{blk}}=2048\) tokens (one context). Alternate EN/TL blocks in a predeclared pattern that keeps cumulative \(|\hat q_{\mathrm{TL}}(t)-q_{\mathrm{TL}}|\le \varepsilon_{\mathrm{path}}\) at every prefix \(t\). Recommended \(\varepsilon_{\mathrm{path}}=K_{\mathrm{blk}}/D_{\mathrm{phase2}}\) (one block). Do **not** leave the stream as “mixed randomly.”  
8. Freeze packed shards, lexicographic last = val (or filed packer), full byte SHA-256, encoded-token digest, token/byte/document totals by language, selected-document ledger.  
9. C3 read-only before P4 parent validation; write-probe negative test.  
10. Manifest generated **once**. A second construction is allowed only if the original fails a **predeclared technical integrity check**, under a documented rebuild rule that **does not inspect outcomes**. New construction ⇒ new manifest identity.

### 7.3 `p4_mix_manifest.json` required fields

See `schemas/p4_mix_manifest.template.json`. Required keys include: `protocol_sha256`, `code_commit`, `tokenizer_sha256`, `token_bytes_sha256`, `mix_construction_version`, `q_tl_target`, `q_en_target`, `d_phase2_target`, `target_tl_tokens`, `target_en_tokens`, `achieved_tl_tokens`, `achieved_en_tokens`, `rounding_rule`, `token_accounting_function_sha256`, `english_source_split_hashes`, `tagalog_source_split_hashes`, `english_document_order_seed`, `tagalog_document_order_seed`, `interleave_seed`, `interleave_algorithm`, `block_schedule_digest`, `document_revisit_policy`, `document_truncation_policy`, `english_document_count`, `tagalog_document_count`, `english_utf8_bytes`, `tagalog_utf8_bytes`, `english_model_tokens`, `tagalog_model_tokens`, `english_share_by_tokens`, `tagalog_share_by_tokens`, `english_share_by_bytes`, `tagalog_share_by_bytes`, `packed_shard_paths`, `packed_shard_sha256`, `full_stream_sha256`, `created_utc`, `created_by`.

Pass condition at Gate E: `achieved_*_tokens` match targets within filed tolerance; `tagalog_share_by_tokens` equals \(q_{\mathrm{TL}}\) after rounding; packed last shard is val; tests absent.

---

## 8. Parent and child training specification

### 8.1 Lineage

```text
fresh P4 Tagalog initialization
        -> P4 d8 parent (eligibility evidence only)
        -> P4 d20 parent -> P0-T pass -> immutable C0
                                           -> C1 extra Tagalog
                                           -> C2 pure English
                                           -> C3 frozen token-share mix
```

### 8.2 Parent (phase one)

- Random initialization; **not** P3 B0.  
- Tagalog train only; P4 tokenizer; \(T=2048\); \(B=65536\).  
- \(N_{\mathrm{TL0}}=\lceil 3 T_{\mathrm{TL,train}}/B\rceil\). If carry-forward tokenizer, this **SHOULD** be 294; Gate G records the integer. If PDF freezes 294 regardless, Gate G **MUST** match or **protocol_stop**. **Recommended PDF language:** freeze \(N_{\mathrm{TL0}}=294\) **and** require Gate G equality under carry-forward tokenizer.  
- Warmup 14; eval/sample/core-metric off for operator view; metrics lockboxed.  
- Terminal checkpoint only.

### 8.3 P0-T

Both d8 and d20 beat untrained (seed **0**) and add-1 byte-unigram by \(\ge\delta_{\mathrm{P0T}}\) on full Tagalog val. **Authoritative P0-T is CUDA-only** on the filed class. A CPU evaluation, if run, is diagnostic and **MUST NOT** set status. Safe output: `PASS` / `BLOCKED` / `TECHNICAL BLOCK` only. No child until d20 eligible. Copy d20 to frozen C0 path; SHA match source/host/local.

### 8.4 Children (phase two)

From identical C0, `load_optimizer=False`, fresh Muon+AdamW, peak LR \(=0.3\times\) parent peak, warmup 14, `resume_from_step=-1` or equivalent **no-resume**, exactly \(N=294\) new steps, terminal checkpoint only.

**Hard prohibition:** C1, C2, or C3 **MUST NOT** be used as another child’s parent.

Partial child after technical failure: **quarantine**; default **clean restart from immutable C0** with fresh optimizer and the **full** phase-two budget. No outcome-informed arm/budget change.

Model tags (recommended): `p4-c0-tl-d20`, `p4-c1-extra-tl-d20`, `p4-c2-en-d20`, `p4-c3-mix-d20`.

---

## 9. Gate-by-gate protocol

**Exhaustive operator bible (preconditions, argv class, receipts, stops, F-before-E order):** [`PROTOCOL-p4-GATES-EXHAUSTIVE.md`](PROTOCOL-p4-GATES-EXHAUSTIVE.md). This section is the compressed map. If they conflict, this master ≫ the bible on science; the bible ≫ this section on missing operational detail **unless** it would change a filed constant.

| Gate | Purpose | GPU | Safe public output |
|---|---|---|---|
| 0 | File P4; archive PDF; lock protocol SHA; create lockbox; no outcome paths | No | Filing/hash status only |
| A | Pin code; isolate P4 cache; forbid P1/P2/P3 env and weights | No | Hashes/status only |
| B | Acquire/archive named TL and EN raw sources | No | Archive/split hashes only |
| C | Hygiene and forbidden-artifact scan | No | PASS/BLOCKED only |
| D | Freeze eligible document splits and test exclusion | No | Counts/hashes only |
| E | Pack pure streams; construct/freeze C3 **after F**; before any P4 confirmatory BPB | No | Manifest hashes/counts only |
| F | Verify/prepare frozen tokenizer **before E-mix** | No | Tokenizer hash; fertility only if designated descriptive |
| G | Freeze budgets, argv, mix quota, cost estimate | No | Constants/hashes only |
| H | CUDA d4 smoke, not parent training | CUDA | Finite/descent/reloadability only |
| I | Train fresh P4 Tagalog parent at filed depths | CUDA | Process health only; no confirmatory values |
| P0-T | Parent eligibility against two filed floors | CUDA | PASS/BLOCKED/TECHNICAL BLOCK only |
| Q | Freeze eligible P4 d20 as C0 | Copy | Parent SHA only |
| R | Train C1 extra Tagalog | CUDA | Health/terminal checkpoint hash only |
| S | Train C2 pure English | CUDA | Health/terminal checkpoint hash only |
| T | Train C3 token-share-locked mix | CUDA | Health/terminal checkpoint hash only |
| U | Full validation and seal | CUDA | Completion/seal/count status only; **no BPB** |
| V | Exactly one C3-only secondary test, if Policy A | CUDA | Test counter / named branch only; **no scalars** |
| X | Formal unblinding | No | Release scalars together |
| W | Archive, paper, Hub, ResearchBox | No | No new science |

### 9.1 Common gate contract

Every gate **MUST** specify: preconditions; hashed inputs; permitted command class; prohibited actions; expected artifacts; pass / blocked / technical_stop / protocol_stop; terminal vs lockbox; quarantine after fault; next gate; authorization.

**Prohibited at all pre-X gates:** printing BPB, contrasts, rankings, “best,” sample text used to infer quality, filenames embedding scalars, paper sentences implying pass/fail of outcomes.

### 9.2 Gate notes (compressed; scripts to implement after filing)

**0.** Preconditions: protocol complete; decision register signed. Inputs: PDF. Pass: `aspredicted_id` set; protocol SHA in LOCK; lockbox acceptance tests; counters = 0. **MUST NOT** allocate `P4_RUN_ID` before PDF. Next: A.

**A.** Pin commit; create `data/cache/<P4_RUN_ID>/`; reject listed P1/P2/P3 weight SHAs; env is p4-only.

**B–D.** Copy P3-class archive/split freeze; tests chmod/unmounted.

**F then E (operational; LOCK letters stay E, F).** C3 is token-share-locked, so the tokenizer **MUST** be frozen **before** C3 construction. Alphabetical E-before-F is illegal for the mix half of E.

**F.** If carry-forward: verify tok SHA. If fresh-tok policy filed: `tok_train` on TL train only; freeze hash.

**E.** After F: pack C1/C2 pure streams + construct/freeze C3; last-is-val; write-probe; C3 read-only. **MUST** complete before Gate I confirmatory parent val (P0-T). Fertility **MAY** be recorded as descriptive **after** mix freeze, never to retune \(q_{\mathrm{TL}}\).

**G.** Freeze \(N\), \(B\), \(D_{\mathrm{phase2}}\), C3 integer quotas, argv, cost estimate. **MUST NOT** use `ratio=-1`.

**H.** d4 smoke on CUDA; not `p4-c0-*` tag; no BPB.

**I.** d8 then d20; lockbox metrics.

**P0-T.** Boolean only.

**Q.** Copy/hash C0; `load_optimizer` path documented false for children.

**R–T.** Order **R then S then T** unless PDF files parallel **after** C0 freeze with no shared writable cache. Technical fault: quarantine; clean restart from C0.

**U.** Six child cells C1/C2/C3 × {TL, EN} **plus** C0 EN descriptive (filed collect-once); seal; `test_access_count=0` at commit.

**V.** Policy A: C3 only; two named holdouts = **one** event; `test_access_count=1`; lockbox.

**X.** Status-only preflight; then one-time scalar release.

**W.** No new science; Hub all four weights together or all deferred.

---

## 10. Validation, lockbox, unblinding, and test policy

### 10.1 Evaluator

Same frozen `scripts/p4/evaluate_bpb.py` (fork of P3 evaluator **after filing**, hash frozen at Gate A/U). CUDA official. Full split, \(T=2048\), BOS-best-fit packing as in P3. Byte accounting = UTF-8 bytes of evaluated tokens via `token_bytes.pt`.

### 10.2 Gate U seal contents

Six full vals **plus C0 English descriptive** (collect once); checkpoint SHAs; evaluator/data/tok hashes; timestamps; **recomputed** \(R_{\mathrm{TL}}\), \(A_{\mathrm{EN}}\) inside lockbox; `test_access_count=0`. C0 EN is excluded from both contrasts.

### 10.3 Test policy (choose before filing)

| Policy | Treatment | Recommendation |
|---|---|---|
| **A** | One authorized C3-only test event on two named legacy holdouts (EN WT103-raw test; TL P1.1 `test.jsonl`) | **Recommended.** Mixture intervention is the only secondary tested model. |
| B | No test event | Allowed for validation-only closure. |
| C | Test more than C3 | **Prohibited** unless fully justified **before filing**. |

If A: C1/C2 never on P4 test files; C3 once; event logs as `test_access_count=1` even though two component evals; lockboxed until X; descriptive secondary, not arm selection.

### 10.4 Counters

```text
test_access_count                 # 0 at U; 1 after V if A
p4_outcome_access_count           # 0 until X
validation_scalar_access_count    # 0 until X
lockbox_open_events               # append-only
```

Initial all 0. Append-only JSONL access log. Write mode 600. Lawful transitions only at named gates.

### 10.5 Safe vs forbidden pre-X

**Safe:** gate status; hashes; artifact existence; file/byte counts; liveness; finite/nonfinite; smoke “loss decreased” / reloadable; terminal ckpt existence; counter **status**; P0-T PASS/BLOCKED/TECHNICAL BLOCK.

**Forbidden:** any BPB; any contrast or sign; any ranking; “best”; samples as quality evidence; metric screenshots; result scalars in filenames; paper sentences implying whether an outcome passed; chat/issue updates with interpreted outcomes.

### 10.6 Gate X preflight (status only; do not open scalars)

| Check | Required state |
|---|---|
| Prerequisite gates | `pass` or documented lawful stop |
| C0/C1/C2/C3 hashes | Match locked manifests |
| C3 mix manifest | Target and stream hash match |
| U before V | Timestamp order |
| Test counter at U | 0 |
| After V if A | 1 |
| Tested branch | C3 only |
| C1/C2 test records | Absent |
| Outcome access before X | 0 |
| Safe logs | No scalar leakage |
| Incidents | Recorded and quarantined/resolved |

Then one-time release: timestamp, operator, files opened, counter transitions.

---

## 11. Artifact schemas and naming conventions

| Path | Role | Update authority | Post-freeze edit |
|---|---|---|---|
| `manifests/p4_gate_ledger.json` | Gate statuses | Operator at each gate | Status only; no scalars |
| `manifests/p4_budget_manifest.json` | \(N,B,D,q\) | Gate G | Forbidden |
| `manifests/p4_test_access_log.json` | Test events | Gate V/X | Append-only |
| `manifests/p4_mix_manifest.json` | C3 treatment | Gate E | Forbidden except rebuild card |
| `docs/papers/p4-token-share-mix/LOCK.json` | Study lock | Gate 0/X | Counters at X |
| `docs/run-cards/p4/<P4_RUN_ID>/p4_closeout_manifest.json` | Closeout | Gate W | No new science |
| `docs/run-cards/p4/<P4_RUN_ID>/deviations/<ts>-<slug>.md` | Incidents | At event | Append |

Templates: `LOCK.template.json`, `schemas/*.json`. Placeholders only; **do not** invent a run ID.

LOCK **MUST** include: `study`, `registration_id`, `registration_url`, `protocol_sha256`, `code_commit`, `p4_run_id`, `tokenizer_policy`, `tokenizer_sha256`, `mix_manifest_sha256`, `mix_target_share`, `parent_status`, `gate_statuses`, `test_access_count`, `p4_outcome_access_count`, `unblinding_status`, `deviation_cards`, `authority_hierarchy`, `designed_after_p3_gate_x`, `does_not_amend_307342`.

---

## 12. Technical incident / deviation rules

Modeled on the P3 Gate S *lesson* (quarantine + clean restart), **not** as P4 evidence.

| Incident | Immediate safe action | Official trajectory continue? | Record |
|---|---|---|---|
| Missing stream / wrong path before step 0 | Block, repair, re-preflight | Yes, after hash proof | Technical incident card |
| Wrong stream after any official child step | Stop; quarantine output | Default **no**; clean restart | Deviation + quarantine manifest |
| Parent SHA mismatch | Stop | No until resolved; else protocol_stop | Integrity report |
| Token-share mismatch **before** C3 training | Stop; rebuild only under frozen construction | Yes if no outcomes observed | Rebuild card + new manifest identity |
| Token-share mismatch **after** C3 begins | Stop | No automatic resume; assess protocol_stop | Incident report |
| Missing CUDA / non-NVIDIA | Block | No | Host preflight card |
| Nonfinite loss / ckpt failure | Stop and quarantine | No automatic tuning | Technical stop card |
| Unauthorised val/test access | Protocol stop | No | Access incident report |
| Lockbox scalar leakage | Protocol stop / disclosure | No silent continuation | Leakage report |

Every incident card **MUST** contain: UTC timestamps, command hashes, PIDs, input/output paths, safe symptom, whether official steps completed, quarantine disposition, whether outcomes were accessed, authority sign-off.

Template: `P4-DEVIATION-TEMPLATE.md`.

---

## 13. AsPredicted-ready concise draft

See `P4-AsPredicted-draft.md` (1–2 pages). Do not force implementation detail into the form.

---

## 14. Paper / reporting / release outline

See `P4-PAPER-OUTLINE.md`, `P4-REPORTING-GRAMMAR.md`, `P4-RELEASE-PLAN.md`.

Provisional title (no “mitigation”):

> **Token-Share-Locked English–Tagalog Mixtures after a Fresh Tagalog Parent: A Preregistered Trade-Off Study with nanochat**

Hub: **C0+C1+C2+C3 together**, or all deferred with an explicit reason. **MUST NOT** release C3 alone as “the final P4 model.”

---

## 15. Explicit compliance matrix

| Promise | Implementation artifact | Freeze gate | Verification | Pass | Report |
|---|---|---|---|---|---|
| Post-P3 disclosure | PDF sentence 1; LOCK `designed_after_p3_gate_x` | 0 | PDF SHA | PDF contains sentence | Paper intro |
| Does not amend P3 | LOCK flags | 0 | Checklist | Flags true | Paper / RB |
| Fresh parent | `base_train` from init; SHA reject list | A,I,Q | Forbidden SHA scan | No P3 ckpt loaded | Methods |
| One token-share clock | mix manifest `english_share_by_tokens` | E | Quota equality | Within tolerance | Methods + appendix |
| C3 frozen before P4 BPB | Gate E before I/P0-T/U | E | Timestamp order | E < I | Run cards |
| Equal \(D_{\mathrm{phase2}}\) | budget manifest | G,R–T | Step=294 all children | Hashes | Methods |
| Co-primary \(R_{\mathrm{TL}},A_{\mathrm{EN}}\) | seal JSON | U,X | Recompute | Filed signs/δ | Results |
| Val before test | counters | U,V | test=0 at U | Log | Methods |
| C3-only test if A | Gate V | V | No C1/C2 test files | Log | Results secondary |
| CUDA confirmatory | host cards | H–V | nvidia-smi | Class match | Methods |
| Hub together | RELEASE_MANIFEST | W | Four `.pt` present or all absent | Manifest | Availability |
| No mitigation in title pre-X | paper outline | W | String check | Absent unless both met | Paper |

---

## 16. Six-layer forecast and hidden-risk register

### Explicit

Filed question, C1/C2/C3, \(R_{\mathrm{TL}}\)/\(A_{\mathrm{EN}}\), \(\delta\), \(q_{\mathrm{TL}}\), P0-T, lockbox, C3-only test, post-P3 disclosure, no-amendment.

### Implicit

Equal tokens ≠ equal bytes; Hub-together morality; tokenizer carry-forward ≠ weight reuse; fresh optimizer encodes new phase; terminal ckpt only; bingo CSV vs JSON seals if RB used.

### Inferred

P4 exists because P3 B3 could not answer token-share; d8+d20 P0-T blocks lucky-deep-parent stories; C3-only test mirrors P3 intervention-only discipline.

### Extrapolated / reproducibility

Outsiders: clone GitHub P4 trees + Hub C0–C3 + frozen manifests; no HOST SSH. Byte-balanced P6-B is a later filing. Multi-seed is not P4.

### Residual closeout

AsPredicted number, RB box, protocol SHA, env scripts not yet written, CUDA host unnamed, mix construction code not yet implemented.

### Hidden risks

| Risk | Why hidden | Mitigation |
|---|---|---|
| HOST SSH cards | Secrets | gitignore; never Hub |
| Raw test text | Holdout | Unmount; Gate V only |
| `meta.val_bpb` leak | Operators can jq | Strip or lockbox |
| Chat as authority | Drafting | Stack: PDF ≫ protocol ≫ LOCK |
| Outcome-tuning \(q_{\mathrm{TL}}\) via fertility | Tempting | Fertility descriptive after freeze only |
| Calling C3 “fixed B3” | Citation risk | Verbatim sentence in PDF and paper |
| Quarantine partial used as official | P3 S lesson | Clean restart default |

---

## 17. Hard-stop table

| Condition | Stop type |
|---|---|
| No finalized registration | Gate 0 block |
| Unchosen exposure clock or dual “byte or token” language | Gate 0 protocol_stop |
| Missing C3 manifest hash | Gate E/I block |
| P1/P2/P3 weight contamination | Protocol stop |
| Test present in a training path | Protocol stop |
| P0-T failure | No C1/C2/C3 |
| C3 token share outside filed tolerance | Protocol stop |
| Parent SHA mismatch | Integrity stop |
| Continue from another child branch | Protocol stop |
| Scalar leak before Gate X | Protocol stop / disclosure |
| Test access before validation seal | Protocol stop |
| Test access of C1/C2 | Protocol stop |
| Revise \(q_{\mathrm{TL}}\), \(\delta\), or C3 construction after outcomes | Protocol stop / amendment (forbidden as silent) |
| MPS/TPU/CPU for official confirmatory GPU gates | Protocol stop |
| `ratio=-1` or `python -m nanochat.dataset` | Protocol stop |
| Sourcing `scripts/p{1,2,3}/env.sh` | Protocol stop |

---

## 18. Pre-filing decision register

Every item **MUST** be answered before filing. **MUST NOT** defer a scientific choice to “implementation.” Recommended values are **unsigned**.

| # | Decision | Recommended | Status |
|---|---|---|---|
| 1 | P4 label and scope | P4-C3-TOKEN-SHARE; post-P3 token-share mix; not P3 amendment | Sign in PDF |
| 2 | Tokenizer policy | Carry-forward P3 `04436b85…` | **UNRESOLVED BEFORE FILING** |
| 3 | Exact \(q_{\mathrm{TL}}\) | `0.50` | **UNRESOLVED BEFORE FILING** |
| 4 | Exact \(\delta\) | `0.01` BPB; practical + confirmatory | **UNRESOLVED BEFORE FILING** |
| 5 | C3 interleave algorithm | Deterministic blocks, \(K_{\mathrm{blk}}=2048\); PCG64 or `random.Random` — pick one | **UNRESOLVED BEFORE FILING** |
| 6 | C3 token-share tolerance | Exact integer match | **UNRESOLVED BEFORE FILING** |
| 7 | Child test policy | **A** C3-only one-touch | **UNRESOLVED BEFORE FILING** |
| 8 | Parent budget/depth | d8+d20; \(N_{\mathrm{TL0}}=N=294\); \(B=65536\); \(T=2048\) | **UNRESOLVED BEFORE FILING** (carry-forward rec.) |
| 9 | Named CUDA host class | NVIDIA A40 48 GB (Runpod Secure Cloud class as in P2/P3) | **UNRESOLVED BEFORE FILING** (do not name a live pod) |
| 10 | ResearchBox / deposit | New box; do not write #8834; AsCollected new version or project | **UNRESOLVED BEFORE FILING** |
| 11 | PRNG library | **UNRESOLVED BEFORE FILING** | Sign with item 5 |
| 12 | C0 English val at U | **Collect once** (descriptive; not a contrast input) | **UNRESOLVED BEFORE FILING** |
| 13 | Residual-token language | English receives residual after round-half-to-even on TL target | **UNRESOLVED BEFORE FILING** |
| 14 | Parallel R/S/T vs serial | Serial R→S→T | **UNRESOLVED BEFORE FILING** |
| 15 | \(\delta_{\mathrm{P0T}}\) | Equal to \(\delta\) | **UNRESOLVED BEFORE FILING** |

```
┌─────────────────────────────────────────────────────────────────┐
│ UNRESOLVED BEFORE FILING — scientific parameters not signed:    │
│ tokenizer policy · q_TL · delta · interleave/PRNG · tolerance · │
│ test policy A/B · parent N/depths · CUDA class · deposit IDs    │
│ Do not train. Do not invent a P4_RUN_ID. Do not file yet.       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 19. What This Protocol Does Not Claim

This protocol does not claim that P4 has been filed, trained, or unblinded. It does not authorize GPU rental or Hub upload. It does not amend P1.1, P2, or P3. It does not treat P3 B3 as a P4 arm. It does not claim that 50/50 documents equal 50/50 exposure. It does not claim byte balancing. It does not claim a general bilingual optimum, a universal mitigation of catastrophic forgetting, a chat or CORE result, a multi-seed population effect, or that P4 confirms P3. It does not allow \(q_{\mathrm{TL}}\) or \(\delta\) to be chosen after fertility, loss, validation BPB, samples, or tests. It does not use P3 sealed magnitudes as P4 success targets. Until the decision register is signed into an AsPredicted PDF, **no confirmatory P4 token may be consumed**.

---

## Internal consistency audit (author)

| Check | Result |
|---|---|
| C3 defined by exactly one exposure clock | Yes: P4-tokenizer tokens |
| No P3 result decides a P4 parameter | Yes: P3 used only as motivation; \(\delta\)/\(q\) unsigned rec. from *family*, not P3 magnitudes |
| P4 does not amend P3 | Yes |
| C1/C2/C3 share one fresh immutable P4 parent | Yes |
| All official children same \(D_{\mathrm{phase2}}\) | Yes |
| C3 frozen before any P4 confirmatory BPB | Yes: Gate E before I/U |
| Full validation seals before any test | Yes |
| Pre-X output contains no scalar outcomes | Yes |
| Fresh P4 ledger/lockbox/cache | Yes |
| Does not call a document-balanced stream token-balanced | Yes |
| Proposed test C3-only | Yes if Policy A signed |
| “Mitigation” conditional and narrow | Yes |
