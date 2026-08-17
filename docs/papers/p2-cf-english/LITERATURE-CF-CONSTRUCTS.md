# WikiText-TL-39, WikiText-103, and catastrophic-forgetting constructs

**Date:** 16 August 2026  
**Does not amend AsPredicted #306780.**  
**Does not invent BPB.**  
**Does not treat** [`pageman/nanochat-filipino-p1-fixed-d20-3x`](https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x) **as an English parent.**

This note is the literature + retrieval lock for Paper 2. Interactive map: the companion canvas `wt103-tl39-cf-constructs.canvas.tsx`. Direction lock: [`DIRECTION-RECALIBRATION.md`](DIRECTION-RECALIBRATION.md).

North star: **P1.1 d20 cannot forget English. It never had English.** Scoring it on WikiText-103 is out-of-distribution language modeling (never-learned), not backward transfer.

---

## 0. Retrieval protocol

ArXiv-LLM retrieval (abstracts + HTML, 16 Aug 2026), plus Cruz & Cheng (2019) and Merity et al. (2016/2017) as primary corpus papers, plus P1.1 data card / Hub card as local instruments.

| Role | Paper | arXiv / venue | What was taken |
|---|---|---|---|
| English corpus | Merity, Xiong, Bradbury, Socher. *Pointer Sentinel Mixture Models* | [1609.07843](https://arxiv.org/abs/1609.07843) (ICLR 2017) | WikiText-103 construction |
| Tagalog analogue | Cruz & Cheng. *Evaluating Language Model Finetuning Techniques for Low-resource Languages* | [1907.00409](https://arxiv.org/abs/1907.00409) | WikiText-TL-39 construction; the only “catastrophic forgetting” sentence in that paper |
| Task CF (classifier) | Howard & Ruder. *ULMFiT* | ACL 2018 / [1801.06146](https://arxiv.org/abs/1801.06146) | Discriminative FT / gradual unfreezing to *avoid* CF of the LM during classification |
| Classical CF | McCloskey & Cohen 1989; French 1999 | — | Sequential-task definition |
| CL metrics | Lopez-Paz & Ranzato. *Gradient Episodic Memory* | [1706.08840](https://arxiv.org/abs/1706.08840) | BWT / FWT / \(R\) matrix. Large negative BWT = (catastrophic) forgetting |
| Regularization CL | Kirkpatrick et al. EWC | PNAS 2017 / [1612.00796](https://arxiv.org/abs/1612.00796) | Parameter-importance protection (not used in P1.1; optional later) |
| Language-shift CL | Gogoulou, Lesort, Boman, Nivre. *Continual Learning Under Language Shift* | [2311.01200](https://arxiv.org/abs/2311.01200) | EN then DA/IS/NO; FWT mostly +; BWT sign depends on contamination + syntax; Icelandic can raise English loss |
| Cross-lingual CPT | Zheng, Pan, Xu, Qin, Yue, Zhou. *Breaking Language Barriers* | [2407.02118](https://arxiv.org/abs/2407.02118) | CPT English → new language; 1.4B English val loss 2.40 → 3.68 without replay; smaller models forget *more*; 5–30% replay |
| Replay | Ibrahim et al. 2024; Scialom et al. 2022 | — | Mixing source-language data during CPT |
| LLM CFT | Luo et al. *Empirical Study of CF in LLMs During Continual Fine-tuning* | [2308.08747](https://arxiv.org/abs/2308.08747) | Instruction-tuning CF; scale *increases* CFT forgetting (do not mix with CPT scale) |
| Survey | Shi et al. *Continual Learning of Large Language Models* | [2404.16789](https://arxiv.org/abs/2404.16789) | CPT / DAP / CFT; language-level CPT is a named shift |
| Cross-lingual lifelong | M’hamdi et al. | [2205.11152](https://arxiv.org/abs/2205.11152) | Cross-lingual lifelong learning (task, not Wikipedia LM) |
| Massively multilingual CL | Winata et al. ACL Findings 2023 | — | Many-language CL; not this two-corpus stack |
| Scale vs forgetting (vision) | Ramasesh et al. ICLR 2022 | — | Not LM CPT; do not import blindly |

**Not found (negative retrieval, load-bearing):**

- No parallel WikiText-103 ↔ WikiText-TL-39 article alignment.
- No official “WikiText-TL-39 English” split.
- No official “WikiText-103 Tagalog” (raw or v1) split.
- No paper that trains nanochat, or any GPT-2-class decoder, sequentially on these two dumps.
- No recovery of Cruz & Cheng 2019 train/val/test files (P1.1 Gate B/D).

---

## 1. What the two corpora actually are

WikiText-TL-39 is a **recipe analogue** of WikiText, not a translation, not a subset, and not a later task in a continuum.

| Axis | WikiText-103 (Merity et al.) | WikiText-TL-39 (Cruz & Cheng) | P1.1 instrument |
|---|---|---|---|
| Stated relationship | Replacement for PTB; long-document English Wikipedia LM | “Inspired by the original WikiText Long Term Dependency Language Modeling Dataset” | Same analogue, reconstructed |
| Language | English | Tagalog / Filipino | Tagalog LM only |
| Article filter | **Good + Featured** only (human-reviewed) | **No** Good/Featured list; **all A–Z titles** on tl.wikipedia (~75k content pages vs ~5.8M English) | Same HF dump, reconstructed articles |
| Train documents | 28,475 articles | 120,975 documents | 120,971 reconstructed lines; 37,602 unique-text train units after hash collapse |
| Train tokens (word / Moses) | 103,227,021 | 39,267,089 | 36,562,228 Moses on reconstructed articles (ratio 0.93 vs Table 1) |
| Val / test | 60 / 60 articles (shared with WT-2) | 25,919 / 25,921 docs (70/15/15) | 8,058 / 8,058 unique-text units; label `reconstructed_article_70_15_15` |
| Vocab policy | Discard count \(< 3\); ~267,735 types; OOV ~0.4% | **Keep** count \(< 3\); 279,153 types; OOV 0.1020% | Train-only 32,768 BPE; \(T_{\mathrm{train}}=6{,}401{,}013\) |
| Tokenization | Moses; `@-@` hyphen artifacts in many redistributions | Moses + Unicode unescape | HF parquet still shows Moses residue (~27% of a 1k sample) |
| HF names | `Salesforce/wikitext` `wikitext-103-raw-v1` vs `wikitext-103-v1` | `linkanjarad/Wikitext-TL39` (P1.1 pin) | Not the 2019 S3 zip (HTTP 404) |
| License | CC BY-SA (Wikipedia) | CC BY-SA (Wikipedia) | Same; not a shared dump |

**Explicit Cruz sentence (the only CF mention in the TL-39 paper):** ULMFiT’s classifier finetuning uses gradual unfreezing etc. “to prevent catastrophic forgetting, wherein the model loses most (if not all) information and relations it has learned during the pretraining stage.” That is **LM → sentiment classifier** CF (Howard & Ruder), not English Wikipedia → Tagalog Wikipedia sequential LM.

Paper 2 English parent is **WikiText-103 raw**, same WikiText *family* as Cruz’s analogue, different language, different quality filter, different dump.

---

## 2. Six-layer CF constructs from the *corpus relationship alone*

Layer definitions used everywhere below:

| Layer | Meaning |
|---|---|
| **Explicit** | Stated in a paper, card, or ledger |
| **Implicit** | Entailed by those statements, not named as CF |
| **Inferred** | Valid conclusion from combining sources |
| **Extrapolated** | Transferred from another paper’s setting onto this pair; **not measured here** |
| **Residual** | Leftover after official construction (artifacts, reconstruction gaps, English inside Tagalog wiki) |
| **Hidden** | Easy to misread as CF or as identity; must be named so it is **not claimed** |

### 2.1 Explicit

1. **Inspired-by, not derived-from.** Cruz names Merity et al. as the recipe, not as a source dump.
2. **Same genre:** full-article Wikipedia language modeling (long-term dependency), not PTB, not 1B-word shuffled sentences.
3. **Shared Moses heritage.**
4. **Quality-filter break:** English Good/Featured vs Tagalog all A–Z because “Tagalog Wikipedia does not have a list of verified good articles.”
5. **Scale break:** ~2.6× fewer train word-tokens; ~4× more train documents (shorter pages).
6. **Split break:** 60/60 featured-style articles vs 70/15/15 random documents.
7. **Vocab-policy break:** discard rare vs keep rare.
8. **CF in Cruz is task-CF**, not language-shift CPT.
9. **P1.1 did not recover 2019 files.** The confirmatory Tagalog split is reconstructed.

### 2.2 Implicit

1. **Family resemblance ≠ parallel corpus.** Shared encyclopedia register, not aligned articles.
2. **A–Z title filter** over-represents Latin-script / English-titled pages on tl.wikipedia (countries, people, borrowed lemmas).
3. **Length mismatch:** many short Tagalog pages vs long featured English articles. Sequence modeling difficulty is not matched even before language.
4. **Named-entity overlap is possible** (Manila, United States, chemical formulas) without any translation pair.
5. **CC BY-SA identity of license** does not identify dumps.

### 2.3 Inferred

1. **Two static dumps are not a continual-learning continuum.** Lopez-Paz BWT requires a learner that saw \(t_1\) then \(t_2\). Corpora sitting on disk have no \(R\) matrix.
2. **If** a decoder is trained on WT103 then continued on TL-39, the literature class is **language-level continual pre-training** (Shi et al. CPT; Zheng et al.; Gogoulou et al.), **domain-matched** (both Wikipedia), **language-shifted**.
3. **TL-39 is not “WikiText-103 in Tagalog.”** It is a weaker-filter, smaller, more-fragmented analogue.
4. **Domain match removes the news-vs-wiki confound** that an English-news continuation would have introduced. Remaining confounds: language, dump, quality filter, article length, tokenizer, reconstruction.

### 2.4 Extrapolated (cite, do not treat as P1.1 results)

1. **Zheng et al.:** naive CPT into a new language raises source-language val loss; **smaller models forget more**. nanochat d8/d20 are far below 1.4B → expect **large** English loss movement *if* an English parent exists.
2. **Gogoulou et al.:** forward transfer into the new language is usually positive and order-robust; backward transfer on English can be + or −. Distant / low-contamination languages (their Icelandic) tend to **hurt** English. Tagalog is typologically farther from English than Danish/Norwegian → **prior: negative English BWT**.
3. **Replay 5–30%** source language (Zheng / Ibrahim / Scialom) is the literature analogue of Paper 2 **A3**, not of P1.1.
4. **Luo et al. CFT** (instruction tuning; larger models forget *more*) is a **different stage** (Shi’s CFT, not CPT). Do not use it to predict EN0→A2.
5. **Howard & Ruder / Cruz ULMFiT** predict CF when a *classifier* is finetuned on top of a Tagalog LM. That is **not** Paper 2 and **not** P1.1 (P1.1 never attached a classifier).

### 2.5 Residual

1. **Moses `@-@` / `@,@`** in WT103 redistributions and in the TL-39 parquet.
2. **P1.1 reconstruction gap:** 120,971 vs 120,975 documents; 36.56M vs 39.27M Moses tokens.
3. **Exact-duplicate extras** 1,205,434 counted, not removed (Gate C).
4. **Unique-text collapse** 53,718 distinct article texts.
5. **English Wikipedia dump date ≠ Tagalog Wikipedia scrape date** (Cruz scrape vs Salesforce WT103).
6. **raw vs v1** on the English side (`wikitext-103-raw-v1` vs Moses-heavier `v1`).

### 2.6 Hidden (false identity / false CF)

1. **The shared brand “WikiText”** invites treating TL-39 as WT103-translated.
2. **“TL-39 in English”** is not a dataset. At most: English residue, quotations, and A–Z titles *inside* Tagalog Wikipedia.
3. **“WT103 in Tagalog”** is not a dataset. Machine-translating WT103 would create a *new* corpus, not retrieve one.
4. **Word-token “39M” vs BPE \(T_{\mathrm{train}}=6.4\)M** — mixing these as “the same budget” is a hidden unit error.
5. **Cruz’s “catastrophic forgetting”** will be cited by reviewers as if it already studied EN↔TL sequential LMs. It did not.
6. **Good/Featured vs A–Z** is hidden as a language effect if ignored: English WT103 is a *quality-selected* encyclopedia; TL-39 is closer to a dump.

---

## 3. Six-layer constructs: Hub d20 × four evaluation surfaces

Checkpoint: [`pageman/nanochat-filipino-p1-fixed-d20-3x`](https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x) (`d20/`, nanochat `model_000294.pt`, commit pin `92d63d4`).  
Training distribution: **Tagalog-only** WikiText-TL-39 `reconstructed_article_70_15_15` train, equal-exposure \(D_{\mathrm{actual}}=19{,}267{,}584\) Tagalog-BPE tokens.  
Official Tagalog DV: `val_bpb_full` **1.172248** (AsPredicted #306780). Untrained ~3.289; byte unigram 4.453225.

Four surfaces the user named. Two of them **do not exist** as official corpora; they are still construct-bearing.

| Surface | Exists? | What a score would actually be |
|---|---|---|
| TL-39 Tagalog | Yes (P1.1 val) | In-distribution LM. Acquisition, not CF |
| TL-39 English | No official split | English residue / code-switch / loanwords inside Tagalog wiki, or English UTF-8 forced through the Tagalog BPE |
| WT103-raw English | Yes (`Salesforce/wikitext` raw) | Language-OOD Wikipedia LM. **Never-learned**, not forgotten |
| WT103-raw Tagalog | No | Undefined unless one invents a translation or re-encodes Tagalog UTF-8 with an English tokenizer and pretends the dump is WT103 |

GEM reminder (loss, not accuracy): forgetting is **negative BWT**, which for BPB is an **increase** after a later task. BWT is undefined if task 1 was never trained.

### 3.1 Hub d20 ↔ WikiText-TL-39 Tagalog

| Layer | Construct | CF status |
|---|---|---|
| Explicit | Official ID evaluation. `val_bpb_full=1.172248`. Beats untrained and unigram. Split `reconstructed_article_70_15_15`. | **Not CF.** This *is* \(R_{1,1}\) for a one-task learner |
| Implicit | Reconstruction ≠ 2019 Table 1 files. Duplicate extras kept. | Split residual, not forgetting |
| Inferred | One task only. Lopez-Paz BWT requires \(T\ge 2\). | CF **structurally undefined** |
| Extrapolated | If Paper 2 A2 later uses this split as \(t_2\), *this* surface becomes the **acquisition** benchmark, not the English retention benchmark | Future CPT, not P1.1 |
| Residual | Moses residue; 0.93 Moses-token ratio vs Table 1; unique-text collapse | Data residual |
| Hidden | Calling a high train-val gap “forgetting” (AsPredicted secondary). That is overfitting / depth, not sequential CF | Do not relabel P1.1 as CF |

### 3.2 Hub d20 ↔ WikiText-TL-39 English

| Layer | Construct | CF status |
|---|---|---|
| Explicit | Cruz did not release an English TL-39. Hub card does not claim English pretraining | Surface is **unofficial** |
| Implicit | A–Z titles, English quotations, loanwords (*computer*, *United States*), code-switch inside Tagalog articles | English **contamination**, not an English Wikipedia competence |
| Inferred | Scoring English strings with a Tagalog-only LM is OOD / code-switch LM. No \(t_{\mathrm{en}}\) was trained | **Not BWT** |
| Extrapolated | Gogoulou “language contamination” as a *moderator* of later BWT: English-in-TL-39 could *reduce* English forgetting **if** an English parent existed — it does not for d20 | Applies to Paper 2 A2, not to P1.1 |
| Residual | English named entities that also appear in WT103 (possible lexical overlap without parallel articles) | Overlap residual |
| Hidden | “The model still knows English because TL-39 has English words” = hidden **pseudo-pretraining** claim. P0 in Paper 2 exists to kill this | Do not claim English parentage |

### 3.3 Hub d20 ↔ WikiText-103 raw English

| Layer | Construct | CF status |
|---|---|---|
| Explicit | d20 train log / ledger: WikiText-TL-39 only. Never WT103 | No English \(t_1\) |
| Implicit | Shared Wikipedia genre may give weak register transfer (encyclopedia syntax, dates, lists) | That would be **FWT from Tagalog**, not BWT of English |
| Inferred | High English BPB relative to an English-trained twin is **never-learned + tokenizer mismatch**, Lopez-Paz \(R_{1,j}\) for a task never in the continuum | **Pseudo-forgetting / OOD** |
| Extrapolated | Paper 2 P0 item 2: EN0 must beat this d20-on-English control by ≥ 0.01 BPB. That uses this surface as a **negative control**, not as a CF measurement | Identification, not CF |
| Residual | Latin script, digits, punctuation, Moses `@-@` shared with Tagalog wiki; Tagalog BPE **shreds** English (high fertility) while BPB stays byte-fair | Tokenizer residual. Do not read token-NLL |
| Hidden | Publishing d20 English WT103 BPB under the title “catastrophic forgetting of English” | **Forbidden claim.** Never-trained ≠ forgotten |

### 3.4 Hub d20 ↔ WikiText-103 raw Tagalog

| Layer | Construct | CF status |
|---|---|---|
| Explicit | WT103-raw has no Tagalog partition | Surface **does not exist** |
| Implicit | The name “WikiText” + “raw” tempts a Tagalog re-dump labeled as WT103 | Identity theft of a benchmark |
| Inferred | Encoding P1.1 Tagalog val with an English WT103 BPE is a **tokenizer-OOD** score of the *same* Tagalog text, not a WT103 evaluation | Not CF; not even the WT103 distribution |
| Extrapolated | A human or MT “Tagalog WikiText-103” would be a **new DAP corpus** (Shi DAP), domain-matched to featured English Wikipedia, language-matched to P1.1 — still not CF unless sequenced after an English parent | Future work, not this Hub card |
| Residual | None from Salesforce WT103-raw | — |
| Hidden | Reporting “WT103-Tagalog BPB” for d20 as if Cruz already built that split | Fabricated benchmark |

---

## 4. Causality constructs from the CF lens

### 4.1 What CF *is* (identification)

Let \(t_1\) = English WikiText-103 LM, \(t_2\) = Tagalog WikiText-TL-39 LM.

Lopez-Paz: after finishing \(t_i\), fill \(R_{i,j}\) = performance on \(t_j\). For BPB (lower better):

\[
\mathrm{BWT}_{\mathrm{en}} \;=\; \mathrm{BPB}_{\mathrm{en}}(R_{T,1}) - \mathrm{BPB}_{\mathrm{en}}(R_{1,1})
\]

Positive \(\mathrm{BWT}_{\mathrm{en}}\) in **loss** = forgetting. Lopez-Paz’s original BWT is on *accuracy* (negative = forgetting). **Do not mix signs.**

Paper 2 identification (already locked):

\[
C_{\mathrm{en}} \;=\; \mathrm{val\_bpb\_full}^{\mathrm{en}}(\mathrm{A2}) - \mathrm{val\_bpb\_full}^{\mathrm{en}}(\mathrm{A1})
\]

A1 = same extra steps, English data (drift / optimization control). A2 = Tagalog data (treatment). \(C_{\mathrm{en}}>0\) = Tagalog continuation hurt English more than more English did.

**Necessary conditions for a CF causal claim:**

1. \(t_1\) was actually trained (provenance P0).
2. \(t_2\) is applied after \(t_1\) to the **same parameters**.
3. \(t_1\) is re-measured on a frozen English val that never entered \(t_2\) training.
4. A matched-steps English continuation (A1) exists so “more training” is not the treatment.

P1.1 Hub d20 fails (1). Therefore every arrow from d20 to an English dump is **not a CF arrow**.

### 4.2 Two causal graphs

**Graph A — P1.1 (observed). No CF node.**

```
scratch ──► Tagalog 32,768 BPE ──► base_train TL-39 ──► d20
                                      │
                                      ├─► TL-39 Tagalog val     = ID acquisition
                                      ├─► TL-39 English residue = code-switch OOD
                                      ├─► WT103-raw English     = never-learned OOD
                                      └─► WT103-raw Tagalog     = undefined
```

**Graph B — Paper 2 (designed, not yet run). CF node exists.**

```
scratch ──► English 32,768 BPE ──► EN0 on WT103-raw
                                      │
                                      ├─► P0 provenance (must pass)
                                      ├─► A0 freeze (English before, Tagalog before)
                                      ├─► A1 extra English          = drift control
                                      ├─► A2 TL-39 Tagalog train    = treatment (CF intervention)
                                      └─► A3 50/50 documents        = replay analogue
                                               │
                         A2 English val  ──►  BWT / C_en     = forgetting construct
                         A2 Tagalog val ──►  vs A0 and vs P1.1 Table 2 = acquisition
                         P1.1 d20 English ──► negative control (never-learned bound)
                         P1.1 d20 Tagalog ──► from-scratch ceiling
```

### 4.3 Causal inventory (all arrows worth naming)

| ID | Construct | Type | On P1.1 d20 | On Paper 2 |
|---|---|---|---|---|
| K1 | Sequential-task requirement (McCloskey & Cohen; Lopez-Paz) | Identification | **Fails** (no \(t_{\mathrm{en}}\)) | Holds if P0 passes |
| K2 | Treatment = language of phase-2 tokens | Intervention | N/A | A2 vs A1 |
| K3 | Outcome = English `val_bpb_full` | Outcome | N/A as CF | Primary |
| K4 | Acquisition outcome = Tagalog `val_bpb_full` | Outcome | Primary (already measured) | Secondary confirmatory |
| K5 | Never-learned vs forgotten | Alternative explanation | **This is the English story** | Ruled out by P0 |
| K6 | Extra-steps / LR / Adam reset as co-treatment | Confounder | N/A | Blocked by A1 |
| K7 | Wikipedia domain match | Shared cause of both languages looking “similar” | Makes OOD English *less* wild than news | Makes CPT language-shift, not DAP-to-news |
| K8 | Quality-filter mismatch (Good/Featured vs A–Z) | Confounder of “language” | Present if you score WT103 | Present in A2 (dump statistics ≠ language) |
| K9 | Article-length mismatch | Confounder of long-range LM | Present | Present |
| K10 | Tokenizer as mediator | Mediator / measurement | Tagalog BPE shreds English; BPB still byte-fair | English BPE shreds Tagalog on A0; do not mix tokenizers in one run |
| K11 | English contamination inside TL-39 | Hidden \(t_{\mathrm{en}}\) lite / moderator | Residual code-switch, not a parent | Can **attenuate** true BWT (Gogoulou) |
| K12 | Reconstruction vs 2019 files | Measurement residual | Locked in P1.1 | Frozen train split for A2 |
| K13 | Scale as moderator | Moderator | d20 tiny | Zheng: smaller CPT forgets more (prior). Luo CFT opposite — **wrong stage** |
| K14 | Replay / mixing | Intervention | Not done | A3 |
| K15 | Forward transfer English → Tagalog | FWT | N/A (no English \(t_1\)) | Tagalog A2 vs A0; also vs P1.1 ceiling |
| K16 | Backward transfer Tagalog → English | BWT | Undefined | \(C_{\mathrm{en}}\), \(\mathrm{BWT}_{\mathrm{en}}\) |
| K17 | Positive BWT possible | Sign | N/A | Gogoulou: not always catastrophic |
| K18 | Collapse vs bump | Severity | N/A | Paper 2: collapse = English BPB ≥ untrained or \(\Delta\ge 1.0\) or loses to English unigram — not a 0.02 bump |
| K19 | ULMFiT task-CF (LM → classifier) | Different estimand | Not in P1.1 | Not in Paper 2 primary table |
| K20 | Pseudo-CF from OOD scoring | Bias | **Active if English WT103 BPB is labeled CF** | Inactive after P0 |
| K21 | Fertility artifact labeled as forgetting | Measurement bias | Active if token-NLL used | Ban token-NLL; BPB only |
| K22 | “Deeper models forget less/more” from P1.1 depth dial | Invalid transport | P1.1 depth is equal-exposure Tagalog, not CL | Depth 8 vs 20 is a **moderator of CPT**, only after EN0 exists |
| K23 | ClimbMix / HF Trainer / CORE as hidden \(t_3\) | Protocol violation | Banned in P1.1 | Banned in Paper 2 |
| K24 | Using P1.1 `model_000294.pt` as English parent | Reversed arrow | Would measure Tagalog retention under English | **Retired** |
| K25 | Machine-translated WT103-Tagalog as if it were Cruz | Fabricated \(t_j\) | Hidden surface 3.4 | Do not create without a new prereg |

### 4.4 What may be claimed vs what may not

**May be claimed now (P1.1 sealed):**

- d20 is a Tagalog Wikipedia LM under equal exposure.
- TL-39 is a WikiText *analogue*, not WT103-translated.
- English WT103 scores of d20, if ever published, are **OOD / never-learned / negative-control** numbers.
- Cruz’s CF sentence is about classifier finetuning.

**May be claimed only after Paper 2 P0+A2 (not yet run):**

- English was forgotten because Tagalog was learned (\(C_{\mathrm{en}}\), with A1).
- Tagalog was acquired from an English parent (A2 vs A0 vs P1.1 ceiling).
- Replay (A3) mitigated BWT.

**Must not be claimed:**

- Hub d20 “catastrophically forgot English.”
- Hub d20 “forgot Tagalog” (nothing came after Tagalog).
- “WikiText-TL-39 in English” or “WikiText-103 in Tagalog” as existing official splits.
- Transport of Luo CFT scale-forgetting or Ramasesh vision-forgetting onto this CPT design without a stage label.

---

## 5. ArXiv-LLM synthesis (one paragraph)

The retrieval agrees on a single causal skeleton: **catastrophic forgetting is negative backward transfer after a later task** (Lopez-Paz; McCloskey & Cohen). For modern LMs the matching *stage* here is **continual pre-training under language shift** (Shi CPT; Zheng; Gogoulou), not ULMFiT classifier CF (Cruz / Howard & Ruder) and not instruction-tuning CFT (Luo). WikiText-TL-39 stands to WikiText-103 as a **same-genre, different-language, weaker-filter, smaller analogue**. That analogue relationship licenses Paper 2’s A alignment (WikiText family, two languages). It does **not** put P1.1 d20 on an English \(t_1\). Until EN0 exists and P0 passes, every English number on the Hub checkpoint is a **never-learned bound**, and every “WT103-Tagalog” number is a **non-corpus**. The only CF experiment the literature plus these two dumps actually underwrite is **English WT103-raw → continue on frozen P1.1 TL-39 train → dual BPB**, with A1 as the extra-English control and P1.1 d20 as the Tagalog ceiling / English negative control.

---

## 6. Pointers

- P1.1 paper: https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39
- P1.1 code: https://github.com/pageman/nanochat-filipino
- P1.1 weights: https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x
- Data card: `docs/data-cards/wikitext-tl39-p1-20260816T025911Z-0067a57.md`
- Paper 2 direction: `docs/papers/p2-cf-english/DIRECTION-RECALIBRATION.md`
- Paper 2 Stage-1 tex: `docs/papers/p2-cf-english/paper.tex`
