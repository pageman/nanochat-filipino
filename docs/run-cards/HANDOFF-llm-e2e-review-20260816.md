# LLM hand-off — P1.1 end-to-end process and framework review

**Study:** NANOCHAT-FILIPINO P1.1 — WikiText-TL-39 fixed-budget depth vs held-out Tagalog BPB  
**Registration:** AsPredicted #306780 · https://aspredicted.org/6r6v4v.pdf  
**PDF SHA-256:** `a34f119df557d2e763aa154e02b76b0ebcbcba1f3fb32c3219d85ae6395cc5ca`  
**ResearchBox:** #8735 (not #5339)  
**RUN_ID:** `p1-20260816T025911Z-0067a57`  
**Session:** 2026-08-16 ~09:53–19:03 PHT (UTC+8)  
**Parent chat:** [P1.1 confirmatory day](5061b925-8dfb-4d47-bb47-f4b3274af5f3)  
**This file does not amend AsPredicted #306780.**  
**Do not put the ResearchBox passcode, `test.jsonl`, or API keys in public zips, GitHub, Colab, or Hugging Face.**

A mid-day snapshot of the same request exists as a Cursor canvas written at 11:54, before confirmatory training. **This file supersedes that snapshot.** Open the current canvas beside chat: the file `p11-e2e-closeout-arc-review.canvas.tsx` under the workspace canvases directory.

---

## 0. How a new LLM session should start

Read, in this order, before proposing any new run:

1. `docs/run-cards/AsPredicted-306780.pdf` (governing lock)
2. `docs/EXECUTION-CLARIFICATIONS-p1.1.md` (SHA `71c2b992…`)
3. `docs/run-cards/RESULTS-p1.1-aspredicted-306780.md`
4. `docs/run-cards/CLOSEOUT-aspredicted-306780.md`
5. `manifests/gate_ledger.json`
6. `manifests/selection_record.json`
7. `manifests/test_access_log.json`
8. `manifests/budget_manifest.json`
9. `manifests/execution_host.json`
10. This file

Then ask only the questions in §8 that are still open. Do not re-run Gates A–J. Do not read test again. Do not reopen `D*`.

---

## 1. Current state (as of 2026-08-16 19:03 PHT)

| Item | State |
|---|---|
| Confirmatory question | Frozen. Depth 8→20 at `D_3x` vs held-out Tagalog `val_bpb_full`. |
| Gates A–G | Pass on Mac (data, tokenizer, budget). |
| Official Gate H | Historical smoke on a separate Runpod host; I host later named. |
| Official Gate I | Complete. Seed-0 d8/d12/d16/d20 on Runpod Secure A40 `68bei7d3vx4krc` / `p1-gate-i`, EU-SE-1. |
| Official Gate J | Complete. Full val BPB all four; one test BPB on `D*=20` only. |
| `D*` | **20** by exact minimum `val_bpb_full=1.172248`. Margin to d8 = **0.006887** BPB. Not a ranking. |
| `test_bpb` | **1.164768**. `test_read_events=1`. Do not read again. |
| Falsification | Did **not** occur. Do not claim “deeper is always better.” |
| Weights on Mac | `artifacts/p1/p1-20260816T025911Z-0067a57/checkpoints/` (gitignored) |
| Weights on Hub | https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x (`d20/` `d16/` `d12/` `d8/`) |
| ResearchBox #8735 | Human bingo upload in progress. Labeled `.sav` Data zip prepared. |
| AsCollected | Design chosen (public data); provenance form may still be unfinished. |
| Git | `main` at `0067a57`. **No remote.** Do not `git add -A` (passcode file + `transfer/`). |
| Runpod | Pod stopped (`EXITED`). API key rotation **due**. Agent cannot rotate. |
| Native-speaker ratings | None. Do not invent. |

---

## 2. Dual arcs

Two stories ran in parallel all day. They must not be collapsed.

**Narrative arc** = who wanted what, what temptation appeared, what was refused, what was deposited, what a reader is allowed to believe.

**Methodological arc** = what was locked, measured, excluded, hashed, selected, and published, and which instrument may change which fact.

### 2.1 Narrative beats (story)

| # | Beat | What happened | Story function |
|---:|---|---|---|
| 0 | Catalog temptation | User ranked 25 Cheng-aligned nanochat projects. Project 1 (WikiText-TL-39 base) won as low-hanging fruit. | Choose one play, refuse the rest. |
| 1 | Lock before outcomes | AsPredicted #306780 filed 2026-08-15 19:34 PT. “It’s complicated” on prior data. Anonymous public PDF. New ResearchBox #8735, not #5339. | The lock is a character. It outranks the agent. |
| 2 | Clarify without amending | Execution clarifications + ledger **before Gate A**. Hierarchy: PDF > clarifications > ledger > deviation > exploratory. | Engineering may not rewrite the question. |
| 3 | Pin the instrument | Gate A: nanochat `92d63d4`, isolate cache, `NANOCHAT_DATA_DIR` hook, no ClimbMix. | ClimbMix is the antagonist. |
| 4 | Acquire the archive | Gate B: HF `train.parquet` only. S3 404. Original 2019 splits not recovered. | Loss of the 2019 files is a finding. |
| 5 | Refuse silent cleaning | Gate C: LF-only. Duplicates and stubs stay. | The study is this package, not a prettier one. |
| 6 | Reconstruct, then label | Gate D: `reconstructed_article_70_15_15`. Test write-protected. | Honesty in the caption is part of the claim. |
| 7 | Teach the trainer Tagalog | Gate E–F: shards + train-only 32768 BPE. Fertility vs GPT-2 is a side story. | Measuring stick must not choose the model. |
| 8 | Equal-exposure contract | Gate G: same `D_actual` for all depths. Mac may count, not train the series. | Depth may not buy more tokens. |
| 9 | Local temptation | Mac MPS pre-H and Gate I dry-runs, card-first. d20 MPS OOM. | Workshop ≠ stage. |
| 10 | False host (Spark) | DGX Spark offer packed, then not used as official I host. | Conditional eligibility is not a result. |
| 11 | Named CUDA host | Runpod Secure A40 `68bei7d3vx4krc` named. Key later exposed; rotation due. | Host is an eligibility variable. |
| 12 | The four-depth day | Seed-0 d8/d12/d16/d20 train to step 294. | The confirmatory cast performs. |
| 13 | Selection before test | Full val BPB; `D*=20` by exact min; then one test read. | The one-touch rule is the climax discipline. |
| 14 | Anti-climax result | d20 lowest by 0.0069 vs d8. Series is not fall-then-flatten. Gap widens 8→16. | The honest ending is “practically indistinguishable.” |
| 15 | Deposit ordeal | ResearchBox bingo: one-file Data, no mix, codebook 34/34, Dear Reader, AsCollected. | Institutional forms become a second experiment. |
| 16 | Public weights | HF `pageman/nanochat-filipino-p1-fixed-d20-3x` with `d20/d16/d12/d8`. YAML card fixed. | Weights are public; test text and passcode are not. |

### 2.2 Methodological beats (gates and instruments)

| Phase | Instrument | Method function | Status |
|---|---|---|---|
| Lock | AsPredicted PDF | Question, grid, DV, exclusions, one-test-touch | Frozen |
| Ops | Execution clarifications | `T_train`, `P`, final checkpoint, unigram, reconstruction, ledger | Frozen pre-A |
| A | Pin + isolate | Commit, hook, no ClimbMix, `P_scaling` method | Pass |
| B | Provenance | Parquet SHA, row count, S3 404 | Pass |
| C | Canonical text | LF-only; registered drops 0; article count | Pass |
| D | Split | Hash 70/15/15; overlap 0; test isolated | Pass |
| E | Shards | ≥3 zstd; last=val; test not in `active/` | Pass |
| F | Tokenizer | Train-only 32768; `token_bytes.pt` | Pass |
| G | Budget | `T_train`, `D_3x`, common `B`, `N=294`, `D_actual` | Pass |
| H | CUDA smoke | Named NVIDIA host; not Mac MPS | Historical / passed on I host path |
| I | Confirmatory train | Four depths, same `D_actual`, final ckpt only | Pass |
| J | Full eval + select + one test | `val_bpb_full` all four; `D*`; one `test_bpb` | Pass |
| L | Reproducibility checklist | Sign-off card | Filled |
| Deposit | ResearchBox / AsCollected / HF / git | What may be public | Partial (human) |

### 2.3 How the arcs couple

Every narrative temptation had a method box that either **absorbed** it (deviation card, exploratory label) or **refused** it (hard ban). A new session that satisfies a narrative desire without a method box is a protocol break.

| Temptation | Method absorption or refusal |
|---|---|
| “Just train on the Mac” | Deviation cards; MPS = infrastructure only |
| “Drop d20, it OOMed” | Ban: shrink `device-batch-size` only; keep `T=2048` and the grid |
| “Pick the pretty mid-run val” | Final checkpoint at step 294 only |
| “Peek at test to choose depth” | One-touch after sealed val selection |
| “Deeper won, say so” | 0.01 BPB interpretation rule; one seed |
| “Upload everything to ResearchBox” | One zip type per column; one file in Data; no test text |
| “Commit all and push” | No remote; do not stage passcode or `test.jsonl` |
| “Amend AsPredicted now that we know” | Ban. Exploratory only. |

---

## 3. Frozen execution facts (do not re-derive casually)

- nanochat pin: `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`
- Hook: `patches/nanochat-NANOCHAT_DATA_DIR.patch` SHA `faaded83…`
- Parquet: `linkanjarad/Wikitext-TL39` `data/train.parquet` SHA `706d7064…`
- Split label (every caption): **`reconstructed_article_70_15_15`**
- Tokenizer SHA: `04436b85…` · `token_bytes.pt` SHA `a5dbc1c8…`
- `T_train=6,401,013` · `D_3x=19,203,039` · `B=65,536` · `N=294` · `D_actual=19,267,584` · `T=2048`
- Official I host: Runpod Secure A40 `68bei7d3vx4krc` / `p1-gate-i`, EU-SE-1 (later stopped)
- Evaluator: `scripts/p1/gate_j_full_bpb.py` · official `evaluate_bpb` · BOS-bestfit · `T=2048`

### Official confirmatory table (seed 0, step 294)

| Depth | `val_bpb_full` | `train_bpb_full` | gap | untrained | unigram |
|---:|---:|---:|---:|---:|---:|
| 8 | 1.179135 | 0.836702 | 0.342432 | 3.289109 | 4.453225 |
| 12 | 1.180824 | 0.528818 | 0.652006 | 3.289358 | 4.453225 |
| 16 | 1.195546 | 0.458045 | 0.737501 | 3.289354 | 4.453225 |
| **20 = D\*** | **1.172248** | 0.672393 | 0.499855 | 3.289106 | 4.453225 |

One `test_bpb` (d20 only): **1.164768**. Test SHA `3bd19345…`.

Weight SHAs (model): d8 `9c407f4f…` · d12 `5dfccc27…` · d16 `525301eb…` · d20 `9e30fff3…`.

---

## 4. Super-exhaustive box catalog

Layers:

- **Explicit** — said in the PDF, clarifications, user commands, or sealed manifests.
- **Implicit** — required by the design but not always voiced as a rule.
- **Inferred** — warranted by evidence in this session (hashes, 404s, OOMs, Hub errors).
- **Extrapolated** — forecast or failure-mode; not a result. Mark as such.
- **Hidden** — easy to miss; a new session will break the study if it ignores these.

Each box has a **narrative (N)** and **method (M)** twin where the coupling matters. IDs are stable for citation in a new chat.

### 4.1 Explicit

| ID | Arc | Box | Content |
|---|---|---|---|
| N-E1 | N | Filed question | Does increasing nanochat depth from 8 to 20 reduce held-out Tagalog BPB when every depth sees `D_3x=3*T_train` on WikiText-TL-39? Prediction: val BPB falls then flattens, or the train–val gap widens. We will not claim deeper is always better. |
| N-E2 | N | Not that story | Not CORE, chat, SFT, classification, dengue, hate-speech, OSCAR/TLUnified/ClimbMix mixing. |
| N-E3 | N | Anonymous public lock | AsPredicted #306780; ResearchBox #8735; author Paul Pajo, DLS–CSB, `paulamerigo.pajojr@benilde.edu.ph`. Public PDF is anonymous until deanonymized. |
| N-E4 | N | “It’s complicated” | Prior data exist (public corpus, possibly engineering). Confirmatory BPB did not exist at filing. Q8 of the PDF explains why this is still a valid preregistration. |
| N-E5 | N | User voice: begin | Sequential “Begin Gate B/C/D/E/F/G”, then Mac infra asks, Spark offer, close-out, ResearchBox errors, HF publish. |
| N-E6 | N | User voice: do it from here | PATH in `~/.zshrc`; HF upload of all four depths; YAML fix. |
| N-E7 | N | Deposit destinations | GitHub `pageman` = code/manifests/results (no weights, no test, no passcode). HF `pageman` = weights + card. ResearchBox = prereg + materials/data/code/other. |
| M-E1 | M | Primary DV | `val_bpb_full` on the **full** packed val set after the **final** fixed-budget checkpoint. Not mid-run `--eval-tokens`. |
| M-E2 | M | Secondary DV | One `test_bpb` after validation-only `D*` selection. Not used to choose depth. |
| M-E3 | M | Grid and T | Depths 8, 12, 16, 20. Train-only 32768 BPE. `T=2048`. Same package, same split. |
| M-E4 | M | Budget identities | `T_train=sum(len(τ(doc)))` over frozen train articles, no BOS/pack/crop. `D_3x=3*T_train`. `D_actual=N*B`. Must pass `--num-iterations` explicitly. |
| M-E5 | M | `P` split | `P_total` ≠ `P_scaling`. `R_d=D_3x/P_scaling` must be positive. Never ratio `-1`. Never treat native ratio=12 as this experiment. |
| M-E6 | M | Checkpoint / selection | Final step 294. `D*` = exact lowest **final** `val_bpb_full`. Gaps `<0.01` BPB govern interpretation, not a second selection rule. |
| M-E7 | M | Baselines | Same-depth untrained model; train-fitted UTF-8 byte unigram, Laplace add-1: `p(b)=(c[b]+1)/(N+256)`. |
| M-E8 | M | Split rule | Recover 2019 files if possible; else `sha256(utf-8)`, lex sort, 70/15/15, no seed. Label `reconstructed_article_70_15_15` in every caption. |
| M-E9 | M | Exclusions / drop rules | Drop only null/empty after LF or length>200000. Stop if drops>5%. Exclude a run for NaN/Inf, ClimbMix, test-in-train, val/test in `tok_train`, ratio `-1`, silent depth/`T` change after OOM. |
| M-E10 | M | Never commands | Never `python -m nanochat.dataset`. Never `--target-param-data-ratio=-1`. Never shrink `T` to fit VRAM. Never launder MPS as official I. |
| M-E11 | M | Path | `tok_train` → `base_train` → `base_eval` (BPB only). Not chat SFT. |
| M-E12 | M | Official numbers | Table in §3. Evaluator `gate_j_full_bpb.py`. All four beat both baselines. |
| M-E13 | M | Extra seeds / `D_1x` | Secondary, val only, do not reopen `D*`. d8 mean 1.190892 (SD 0.010318); d12 mean 1.187442 (SD 0.008792). `D_1x` worse than `D_3x`. |
| M-E14 | M | Hub layout | One model repo named for D\*. Folders `d20/` `d16/` `d12/` `d8/` only. License YAML `other`. Not `transformers` `from_pretrained`. |

### 4.2 Implicit

| ID | Arc | Box | Content |
|---|---|---|---|
| N-I1 | N | Credibility is the plot | Hashes, dated cards, and refusal logs are the prose style. A hostile reviewer is the implied audience. |
| N-I2 | N | Workshop vs stage | Mac success teaches wiring. CUDA named host is the published comparison. |
| N-I3 | N | Classify before curiosity | Deviation/classification card before a new command class. |
| N-I4 | N | Smaller models are not lesser | d4 is pipeline-only. Pilots are secondary. The four `D_3x` depths are the main cast. |
| N-I5 | N | Forms are part of the science | ResearchBox/AsCollected constraints change what “the dataset” is allowed to be. |
| N-I6 | N | Two publics | Code public ≠ weights public ≠ test public ≠ passcode public. |
| M-I1 | M | Equal exposure is the treatment | Depth is the IV only if tokens, tokenizer, split, `T`, and `B` stay fixed. |
| M-I2 | M | Host is eligibility | Wrong device class ⇒ not the registered observation. |
| M-I3 | M | Reconstructed split is a limitation | Claiming “original 2019 splits” is false. |
| M-I4 | M | Low `R_d` is the design | 0.46→0.04 is not a Gate G failure. Do not skip depths for Chinchilla poverty. |
| M-I5 | M | Common `B` is a scientific choice | Changing `B` later changes the treatment. |
| M-I6 | M | Value embeddings ≠ horizon | `P_total` dominated by `value_embeds`. Scaling math uses `P_scaling`. |
| M-I7 | M | Fertility is not selection | Tagalog ~4.53 vs GPT-2 ~2.76 bytes/token is descriptive. |
| M-I8 | M | Sealed selection is time-ordered | `val_baselines_summary.json` at 07:56:24Z had `test_read_count=0`. Named `selection_record.json` was materialized later and must not be told as “we chose after test.” |
| M-I9 | M | Packed vs raw bytes | Packed `val_bpb_full` scores 5,868,797 target bytes; raw val UTF-8 is 6,771,275. Unigram uses the raw stream by registration. |
| M-I10 | M | Document bootstrap ≠ primary DV | Per-doc CIs all overlap. Different packing. Not used to choose `D*`. |

### 4.3 Inferred

| ID | Arc | Box | Content |
|---|---|---|---|
| N-F1 | N | Reviewer-proof process | The day’s requests were protocol-safe memos. Implied goal: a defensible Cheng-aligned confirmatory paper, not a Karpathy speedrun. |
| N-F2 | N | Fear of contamination | Repeated ClimbMix/test/label hygiene ⇒ main risk is a polluted claim. |
| N-F3 | N | Two conversations | Earlier catalog chat ≠ this execution thread. Do not merge conclusions. |
| N-F4 | N | Institutional friction | ResearchBox one-file Data + codebook pairing was learned by rejection, not by docs-first. |
| N-F5 | N | CLI vs browser login | User “logged in” on HF website / other Terminal env; Cursor agent could not see `HF_TOKEN` until a token **file** existed. |
| M-F1 | M | 2019 files gone for this mirror | HF listing + S3 404 + SEACrowd dead zip ⇒ reconstruction is the only honest split. |
| M-F2 | M | Article unit survived | 120,971 vs Table 1 120,975. Row fallback not triggered. |
| M-F3 | M | Moses mismatch is debt | ~36.56M Moses tokens vs Table 1 39.27M. Package is the registered HF file, not a byte-identical 2019 dump. |
| M-F4 | M | Title overlap ≠ leakage | Letter-index pages share titles; exact text-hash overlap is 0. |
| M-F5 | M | Series is not monotonic | Val BPB 8→12→16 rises, then d20 dips below d8 by <0.01. Prediction’s “fall then flatten” did not appear cleanly. Train–val gap widening 8→16 **did** appear. |
| M-F6 | M | Extra-seed noise scale | Sample SD ~0.01 at d8/d12. The 0.0069 d20–d8 gap is inside that noise scale. Supports the 0.01 rule. |
| M-F7 | M | Fine-grained HF token sufficed | Upload of 5.34 GB and repo create succeeded with a fine-grained write token named “My 2nd HF Token.” |
| M-F8 | M | Empty YAML was a Hub schema miss | Card body existed; Hub requires `---` metadata. `license: other` is consistent with “no legal clearance claimed.” |

### 4.4 Extrapolated (not results)

| ID | Arc | Box | Content |
|---|---|---|---|
| N-X1 | N | Paper drama is undertraining | Honest write-up: data-limited depth at `D_3x`, not “nanochat fails Tagalog.” |
| N-X2 | N | Later writer will launder Mac / mid-run / bootstrap | Known contamination paths into a draft. |
| N-X3 | N | Deanonymize is a later act | Public PDF is still anonymous unless the author scrolls/exports. |
| N-X4 | N | GitHub publish is still a decision | No remote. `git add -A` would leak the passcode file. |
| M-X1 | M | BOS packer crops long articles | ~35% crop is nanochat default; Tagalog crop already implied by packed vs raw byte counts. Report both. |
| M-X2 | M | More seeds would likely not crown d20 | Extrapolation from Q7 SDs. Not a new confirmatory table unless pre-specified and val-only. |
| M-X3 | M | Native-ratio=12 copies will look “more trained” | Compatibility family only. |
| M-X4 | M | Terminating the stopped pod loses extra-seed/`D_1x` files still only on volume | Confirmatory weights already on Mac/HF. Optional archive first. |
| M-X5 | M | A `transformers` widget will lie | Custom `.pt` + meta. Do not set `library_name: transformers`. |

### 4.5 Hidden

| ID | Arc | Box | Content |
|---|---|---|---|
| N-H1 | N | Passcode is on disk | `docs/run-cards/aspredicted-p1-submitted.txt` is untracked/sensitive. Never commit, zip, or caption it. Do not repeat it in chat. |
| N-H2 | N | Git author is a machine identity | Pre-gate-a commit author `PaulPajo <paulpajo@….local>`. Do not rewrite git config. |
| N-H3 | N | `vendor/nanochat` is gitignored | Pin exists on this Mac. A fresh clone cannot reproduce without the vendor checkout. |
| N-H4 | N | Tag `p1.1-pre-gate-a` is local | No remote implied. |
| N-H5 | N | Context was summarized | Prefer manifests over chat memory. This review is itself a summary. |
| N-H6 | N | Exposed Runpod key | Rotation **due**. Agent cannot rotate. Do not paste the new key into chat. |
| N-H7 | N | HF token now on disk | `~/.cache/huggingface/token` plus env `HF_TOKEN` in some Terminals. Do not commit. Do not print. |
| N-H8 | N | User pasted box code in chat once | Treat as compromised-to-the-transcript; still do not propagate. |
| M-H1 | M | Test was read for fertility before confirmatory BPB | Gate F bytes/token. Confirmatory test BPB events = 1 after selection. “Never touched test” is false if said absolutely. |
| M-H2 | M | Chunking ≠ `T_train` | 29 long articles newline-chunked for shards. Official `T_train` is full-article encode. |
| M-H3 | M | Duplicates collapsed at split | 120,971 lines → 53,718 unique texts. Near-duplicates not removed. |
| M-H4 | M | SSSL + SDPA vs FA3 | Mac used SDPA; CUDA/FA3 may differ numerically. Do not “fix” `window_pattern` on confirmatory cards. |
| M-H5 | M | Default ratio=12 still scales LR/WD | Even with `--num-iterations` set. Cards pass the small positive `R_d`, not 12 and not `-1`. |
| M-H6 | M | Warmup 14 vs default 40 | `min(40, 5% of 294)=14`. Forgetting it changes schedule, not `D_actual`. |
| M-H7 | M | `selection_record.json` is a reconstruction | Written after the test read; reconstructs the sealed 07:56:24Z decision. |
| M-H8 | M | Mid-run d12 min 1.084991 at step 200 was not used | Tempting number. Forbidden as `D*`. |
| M-H9 | M | Extra-seed / `D_1x` / optimizer / step-200 may remain only on the pod volume | Not required for the confirmatory claim. |
| M-H10 | M | `.gitignore` already excludes `artifacts/`, `*.pt`, `data/processed/` | Weights and `test.jsonl` are not committed by default — unless someone force-adds. |
| M-H11 | M | ResearchBox Data must be **one file** | Labeled SPSS `.sav` zip: `~/Downloads/Data/p1.1-confirmatory-val-bpb-full-labeled.zip`. Old CSV zip shows 0/34 descriptions. |
| M-H12 | M | Code zip cannot contain `.txt` next to `.py` | Hub/ResearchBox classifiers treat mixed zips as illegal. |
| M-H13 | M | `hf` was installed but not on PATH | `~/Library/Python/3.9/bin` added to `~/.zshrc` this session. Cursor shells ≠ user Terminal env. |
| M-H14 | M | d20 uploaded once, not twice | Root-level weights were restaged away. Hub paths are folders only. |
| M-H15 | M | `python -m nanochat.report` is not in the pin | RESULTS markdown is the report substitute. CORE remains omitted. |

---

## 5. Process framework (what kind of science this was)

This session implemented a **preregistered, gate-locked, hash-first, one-touch confirmatory** workflow with an explicit **deviation ontology**.

1. **Lock** the question before confirmatory outcomes.
2. **Clarify** operational definitions without adding hypotheses.
3. **Gate** irreversible steps (corpus, split, tokenizer, budget, host, train, eval, test).
4. **Classify** every off-protocol desire (Mac, Spark, extra seeds) before execution.
5. **Seal** selection before the test read.
6. **Interpret** with a pre-stated practical-indistinguishability rule (0.01 BPB, one seed).
7. **Deposit** under venue rules that are stricter than git (ResearchBox columns; HF card YAML; no secrets).

Framework failures that did **not** occur: second test read; `D*` reopen; ClimbMix; ratio `-1`; confirmatory SFT/CORE; AsPredicted amend; invented native-speaker scores.

Framework failures that **did** occur and were absorbed: original split unrecoverable; Mac used as workshop; Spark offered then unused; Runpod key exposed; ResearchBox classifier rejected mixed/multi-file zips; HF CLI PATH/token-file split; empty model-card YAML.

---

## 6. Still human-only / open

1. Finish ResearchBox #8735 bingo: one section `P1.1 confirmatory`; Preregistration #306780; Materials zip; **only** the labeled `.sav` Data zip; Code zip (`.py`+`.patch` only); Other as needed; codebook 34/34; Dear Reader without passcode; delete old CSV Data chip.
2. Finish AsCollected so “RESULTS PROVENANCE” is documented. Design: **Public data**. Source: `linkanjarad/Wikitext-TL39` revision `7c1a76c2…`, file SHA `706d7064…`, date 2026-08-16. Cleaning: with code. RAs: no.
3. Rotate the Runpod API key. Optionally terminate `68bei7d3vx4krc` after deciding whether leftover volume files matter.
4. Git commit/push only after unstaging the passcode file and probably `transfer/`. User must ask. No remote exists yet.
5. Native-speaker sample ratings: none; do not invent.
6. Optional: GitHub `pageman` code repo; HF dataset card cross-links; paper draft that does not launder secondary numbers.

---

## 7. Hard bans (copy into every new session)

- No second test read. No reopen `D*`.
- No ClimbMix. No `python -m nanochat.dataset`.
- No `--target-param-data-ratio=-1`.
- No confirmatory SFT, CORE, chat, classification.
- No amend AsPredicted.
- No commit unless asked. No git config edits. No force-push.
- No passcode, `test.jsonl`, or API keys in public artifacts.
- No “deeper is always better.”
- No claiming original 2019 splits.
- No treating Mac MPS or Spark as the official I host.

---

## 8. Meaningful questions for a new LLM session

Ask these. Prefer answers from files over memory. Each question names a **forbidden if**.

### 8.1 Authority and contamination

| ID | Ask | Why | Forbidden if |
|---|---|---|---|
| Q1 | What is the governing hierarchy, and which instrument am I allowed to change? | Stops design drift. | You “improve” the PDF, grid, DV, or one-touch rule. |
| Q2 | Has confirmatory `val_bpb_full` / `test_bpb` already been computed? What is `test_read_events`? | Outcomes exist. | You re-run Gate J or “just peek” at test. |
| Q3 | What is `D*`, on what sealed evidence, and what is the margin to d8? | Selection is closed. | You reopen using mid-run val, bootstrap, samples, or test. |
| Q4 | Which numbers are confirmatory vs secondary vs engineering-only? | Prevents laundering. | Mac MPS losses, d12 step-200, gzip, fertility, extra seeds enter the main table. |
| Q5 | What split label must appear in every caption? | Honesty. | You write “original 2019 splits.” |

### 8.2 Reproduction and files

| ID | Ask | Why | Forbidden if |
|---|---|---|---|
| Q6 | Which hashes must match before any new compute? | Provenance. | You re-download parquet or retrain the tokenizer. |
| Q7 | Where are the four final checkpoints and their SHAs? | Weights exist on Mac and HF. | You train a fifth “official” seed-0 `D_3x` run. |
| Q8 | What is in `selection_record.json` vs `val_baselines_summary.json` timestamps? | Reconstruction vs seal. | You tell the story as “we wrote selection after seeing test.” |
| Q9 | What does `.gitignore` already exclude? | Leakage. | You `git add -A` or force-add `test.jsonl` / `*.pt` / the passcode file. |
| Q10 | Is there a git remote? What would a first commit include? | No remote; dirty tree. | You push secrets or `transfer/` (306 MB) without review. |

### 8.3 Claims and writing

| ID | Ask | Why | Forbidden if |
|---|---|---|---|
| Q11 | What sentence is allowed about depth? | Result is sub-0.01. | “Deeper is always better” or “d20 significantly won.” |
| Q12 | Did falsification occur? | Registered alternative. | You rewrite the prediction after the fact. |
| Q13 | What limitations must stay visible? | Reconstructed split, one seed, 2019 Wikipedia, BOS crop, no chat. | You imply a general Filipino chatbot. |
| Q14 | May I add CORE, SFT, d24, `D_10x`, or detok as “also we found”? | Exploratory only. | They enter the confirmatory table or an AsPredicted amend. |
| Q15 | Are native-speaker ratings available? | None. | You invent scores or ask the model to role-play raters. |

### 8.4 Deposit and ops still open

| ID | Ask | Why | Forbidden if |
|---|---|---|---|
| Q16 | What is the ResearchBox bingo state, and which zip is the only legal Data chip? | Classifier rules. | You re-upload the multi-file or unlabeled CSV zip as Data. |
| Q17 | What goes in Dear Reader, and what must never go there? | Readers vs secrets. | Passcode, test text, API keys. |
| Q18 | Is AsCollected complete? What design and URL were chosen? | Provenance banner. | You file it as lab/online/private, or as “just code” only. |
| Q19 | Has the Runpod key been rotated? Is pod `68bei7d3vx4krc` still needed? | Security + leftover files. | You paste keys into chat or terminate before deciding on volume leftovers. |
| Q20 | What is the HF repo URL, layout, and license field? | Already published. | You upload optimizer states, `test.jsonl`, or set `library_name: transformers`. |
| Q21 | Should GitHub get code-only, and what is the exclude list? | Split of publics. | Weights, test, passcode, `.env`. |
| Q22 | Did the user ask me to commit? | User rule. | You commit proactively. |

### 8.5 If the user asks to “continue the experiment”

| ID | Ask | Why | Forbidden if |
|---|---|---|---|
| Q23 | Is the request confirmatory, deviation, or exploratory? | Ontology. | You silently extend the main table. |
| Q24 | Would this require a new AsPredicted or only a dated card? | Lock. | You treat a new depth/budget/corpus as P1.1 confirmatory. |
| Q25 | What is the single next legal action? | Forces one move. | You start a new official grid, or a second test read, “to be helpful.” |

---

## 9. Starter prompt to paste into a new LLM session

```text
You are continuing NANOCHAT-FILIPINO P1.1 (WikiText-TL-39; AsPredicted #306780).

Read first:
- docs/run-cards/HANDOFF-llm-e2e-review-20260816.md
- docs/run-cards/AsPredicted-306780.pdf
- docs/EXECUTION-CLARIFICATIONS-p1.1.md
- docs/run-cards/RESULTS-p1.1-aspredicted-306780.md
- docs/run-cards/CLOSEOUT-aspredicted-306780.md
- manifests/gate_ledger.json
- manifests/selection_record.json
- manifests/test_access_log.json

Hard facts: Gates A–J complete. D*=20 by exact min val_bpb_full=1.172248. Margin to d8=0.006887 (not a ranking). One test_bpb=1.164768; test_read_events=1. Do not claim deeper is always better. Split label reconstructed_article_70_15_15. Weights on HF pageman/nanochat-filipino-p1-fixed-d20-3x in d20/d16/d12/d8. ResearchBox #8735 deposit is human-incomplete. No git remote. Runpod key rotation due.

Do not: second test read; reopen D*; ClimbMix; ratio -1; confirmatory SFT/CORE; amend AsPredicted; commit unless asked; put passcode/test.jsonl/keys in public artifacts; invent native-speaker ratings.

Ask me only about still-open human work (ResearchBox bingo, AsCollected, key rotation, git publish) or a clearly labeled exploratory follow-on.
```

---

## 10. Source map

| Need | File |
|---|---|
| Governing PDF | `docs/run-cards/AsPredicted-306780.pdf` |
| Ops lock | `docs/EXECUTION-CLARIFICATIONS-p1.1.md` |
| Results | `docs/run-cards/RESULTS-p1.1-aspredicted-306780.md` |
| Close-out checklist | `docs/run-cards/CLOSEOUT-aspredicted-306780.md` |
| Model card | `docs/run-cards/MODEL-CARD-p1-fixed-d20-3x.md` |
| Gate L | `docs/run-cards/SIGNOFF-gate-l.md` |
| Ledger | `manifests/gate_ledger.json` |
| Selection | `manifests/selection_record.json` |
| Test log | `manifests/test_access_log.json` |
| Budget | `manifests/budget_manifest.json` |
| Host | `manifests/execution_host.json` |
| Bundle | `transfer/p1.1-closeout-bundle-20260816/` |
| Local weights | `artifacts/p1/p1-20260816T025911Z-0067a57/` (gitignored) |
| Hub | https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x |
| Mid-day stale canvas | `p11-session-handoff-review.canvas.tsx` (11:54; H/I not yet run) |
