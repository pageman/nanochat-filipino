# Protocol P3-TL→EN — Tagalog Retention after English Continuation (nanochat)

**Document type:** Pre-analysis execution protocol (sibling of Protocol P1.1 and Protocol P2-EN→TL).  
**Study short name:** P3-TL→EN  
**Proposed Hub (only after Gate I starts, never P1.1 or P2 Hub):** `pageman/nanochat-filipino-p3-tl-then-en`  
**Status as of 2026-08-20:** Draft execution protocol only. **P3 AsPredicted not filed.** No P3 tokenizer, no TL0, no child, no `val_bpb_full`, no test. **MUST NOT start Gate A until Gate 0 passes.**  
**Authority after filing:** filed P3 AsPredicted PDF ≫ this protocol ≫ `P3_LOCK.json` ≫ dated deviation card ≫ chat.  
**Does not amend:** AsPredicted #306780, ResearchBox #8735, AsPredicted #306935, ResearchBox #8763, P1.1 Gate J, P2 Gates A–W.  
**Recommended nanochat pin (file the actual pin in Gate 0):** `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` (same as P1.1/P2 unless the PDF names another commit).  
**Hook only:** `patches/nanochat-NANOCHAT_DATA_DIR.patch`. **MUST NOT** edit attention, loss, optimizer, or `evaluate_bpb` semantics without prefiling disclosure.  
**Primary DVs:** Tagalog `val_bpb_full` (retention) and English `val_bpb_full` (acquisition), official `evaluate_bpb`, `T=2048`, BOS-bestfit, **P3 Tagalog BPE for every P3 arm**.  
**Primary contrasts:** \(C_{\mathrm{tl}}=\mathrm{TL}(B2)-\mathrm{TL}(B1)\); \(G_{\mathrm{en}}=\mathrm{EN}(B2)-\mathrm{EN}(B1)\).  
**Critical disclosure (MUST be sentence 1 of the P3 form):** P3 is designed **after P2 Gate U/V unblinding (19 August 2026)**. It is a **post-P2, prospectively preregistered reverse-direction study**, not an outcome-independent mirror of P2.  
**TL0:** newly trained P3-specific parent from **fresh weights**, frozen P1.1 WikiText-TL-39 **train documents**, **new** P3 Tagalog BPE — not a new corpus/split.

This protocol is written so that a second experimenter, given only this document, the filed PDF, named Tagalog and English archives, and the pinned nanochat commit, can reproduce the artifact **without seeing P3 BPB until Gate X**. Every gate is a **hard stop**.

**Blinding (this lab):** operators may know P2. They **MUST NOT** know P3 BPB, contrasts, rankings, samples, or test scalars until Gate X (or a documented blocked-study release). Safe progress **MUST NOT** print `val_bpb`, `Validation bpb`, train-loss curves, or samples.

---

## 0. How to use this document

### 0.1 Reading order (do not skip)

1. Read §0–§5 on a laptop with **no GPU**. Freeze the claim, the post-P2 disclosure, filing blockers, lockbox, and bans.  
2. Execute **Gate 0** (file PDF + lockbox acceptance tests) before any P3 data mutation.  
3. Execute **Gates A–G** on CPU/Mac (same class as P1.1/P2 A–G).  
4. Execute **Gate H** on **CUDA NVIDIA** (A40-class proven in P1.1/P2). Not Mac MPS. Not Spark unless a **new labeled P3 smoke** beats init without an attention patch.  
5. Execute **Gate I** (TL0 d8 and d20).  
6. Execute **Gate P0-T**. Safe output is **only** `PASS` / `BLOCKED` / `TECHNICAL BLOCK`.  
7. If PASS: **Gate Q** (B0 freeze) → **R B1** → **S B2** → **T B3**.  
8. Execute **Gate U** (six full vals + lockbox seal, tests unread).  
9. Execute **Gate V** (one B2-only test event).  
10. Execute **Gate X** (formal unblinding).  
11. Execute **Gate W** (archive, paper, Hub, ResearchBox). **No new P3 science.**

### 0.2 Two naming systems (do not confuse them)

| Name | What it is | Example |
|---|---|---|
| **Gate 0, A–I, P0-T, Q–W, X** | Hard-stop checkpoints | Gate F = P3 Tagalog tokenizer |
| **Arm TL0, B0, B1, B2, B3** | Weight states | B2 = English continuation (intervention) |
| **P1.1 Gates A–J** | Finished Tagalog-from-scratch study | Never a P3 parent |
| **P2 Gates A–W / arms A0–A3** | Finished English-then-Tagalog study | Never a P3 parent |

**B0 is not Gate 0.** Gate 0 is filing. B0 is frozen TL0 d20.

### 0.3 Gate language

- **MUST** — required for confirmatory P3-TL→EN.  
- **MUST NOT** — forbidden; a violation invalidates the confirmatory label.  
- **SHOULD** — default; dated deviation card if skipped.  
- **MAY** — optional; exploratory unless the PDF already names it.

### 0.4 What this project is and is not

**This project is:** a **nanochat-only** reverse-direction sequential-pretraining (Shi **CPT**, language-shift) study. Train a **fresh** Tagalog parent with official `tok_train` → `base_train` → `evaluate_bpb` on **P3 Tagalog BPE**. After P0-T, continue **byte-identical B0** on extra Tagalog (B1), English (B2), or a **pre-frozen** mix (B3) for equal phase-2 tokens. Seal dual `val_bpb_full`, then one **B2-only** secondary test.

**This project is not:** P1.1. It is not P2. It is not “load `p1-fixed-d20-3x` then train English.” It is not P2.1. It is not confirmation of P2. It is not ULMFiT classifier CF. It is not CFT/SFT/chat. It is not HF `Trainer`. It is not an amendment of #306780 or #306935.

### 0.5 GPU wall

| Work | Host | GPU |
|---|---|---|
| Gate 0, literature, PDF, lockbox dry-run | Laptop | **No** |
| Gates A–G | Mac/CPU | **No** |
| Gate H d4 smoke | CUDA NVIDIA | **Yes** |
| Gate I TL0 d8 and d20 | CUDA NVIDIA | **Yes** |
| Gate P0-T full Tagalog val | CUDA (CPU only if it finishes) | **Yes in practice** |
| Gates Q–T | CUDA | **Yes** (Q is copy/hash; R–T train) |
| Gates U, V | CUDA | **Yes** |
| Gates X, W | Laptop | **No** |

**Confirmatory GPU class:** NVIDIA CUDA, official nanochat attention (FA2/3 as the pin selects, or **unpatched** SDPA). **Proven class (P1.1/P2):** Runpod A40 48 GB.

**Not confirmatory until a new P3-labeled smoke:** Apple MPS; DGX Spark GB10; any host that requires editing `nanochat/flash_attention.py`.

### 0.6 Frozen P1.1 facts (historical inputs only — never load weights)

Copy; **MUST NOT** re-measure to “confirm” P1.1 or to pick P3 thresholds after seeing P3 BPB.

| Item | Frozen value |
|---|---|
| AsPredicted | #306780 |
| ResearchBox | #8735 |
| RUN_ID | `p1-20260816T025911Z-0067a57` |
| Split label | `reconstructed_article_70_15_15` |
| Train documents | 84,679 |
| P1.1 Tagalog BPE SHA256 | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| Official d20 `val_bpb_full` | 1.172248 (**descriptive reference only**; different tokenizer if P3 trains a new BPE) |
| One P1.1 `test_bpb` | 1.164768 (**MUST NOT** publish as a P3 B2 number) |
| Hub | `pageman/nanochat-filipino-p1-fixed-d20-3x` |
| d20 `model_000294.pt` SHA256 | `9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38` — **never load as TL0/B0/B1/B2/B3** |

If P3 **reuses P1.1 document splits** but trains a **new** tokenizer, **recompute** \(T_{\mathrm{TL,train}}\) at Gate G. **Do not** copy P1.1 \(N=294\) for TL0 unless Gate G yields that integer.

### 0.7 Frozen P2 facts (disclosure only — never load weights, never retune P3)

P2 is **closed science**. P3 **MUST** disclose it. P3 **MUST NOT** use these numbers to choose mix, \(D\), cutoff, test, or depth after filing.

| Item | Frozen value |
|---|---|
| AsPredicted | #306935 |
| ResearchBox | #8763 |
| RUN_ID | `p2-20260817T150944Z-de99f8a` |
| Gate U unblinding | 2026-08-19 |
| \(C_{\mathrm{EN}}\) | \(-0.073991\) (filed ≥0.01: **not observed**) |
| \(G_{\mathrm{TL}}\) | \(-3.883048\) (filed ≤−0.01: **observed**, one seed) |
| A3 | 50/50-**document** mix; realized EN byte share ≈0.961; **not mitigation** |
| A2 tests | EN 1.392015; TL holdout under **English** BPE 1.160154 |
| Hub | `pageman/nanochat-filipino-p2-en-then-tl` |
| A0 SHA256 | `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d` — **never load** |

### 0.8 Environment (MUST)

```bash
# From $NANOCHAT_FILIPINO_ROOT after Gate 0 creates these files.
source scripts/p3/env.sh          # CPU gates
# source scripts/p3/env.cuda.sh   # CUDA only
# MUST NOT source scripts/p1/env.sh
# MUST NOT source scripts/p2/env.sh
```

Use generalized path `$NANOCHAT_FILIPINO_ROOT` in public logs (never `/Users/<name>/`).

### 0.9 Safe progress vs lockbox

| Root | Operator may see | MUST NOT contain |
|---|---|---|
| `$P3_SAFE_PROGRESS_ROOT` | job id, GPU name, step, file size, SHA256, `health=pass/block`, `finite/nonfinite`, `P0-T: PASS\|BLOCKED`, `seal created`, test **count** | BPB scalars, loss curves, samples, arm rankings, test text |
| `$P3_LOCKBOX_ROOT` | encrypted or mode-600 JSON | Released only at Gate X (or blocked-study path) |

**`meta_*.json` `val_bpb` is in-loop, not `val_bpb_full`.** If operators can `jq` checkpoint metadata, the lockbox is bypassed. **MUST** keep `meta_*.json` in the lockbox or strip `val_bpb` from operator-visible copies. Safe receipt: `{step, bytes, sha256, reload_ok}` only.

---

## 1. Scientific objective

### 1.1 One-sentence objective

After a **newly trained P3-specific** Tagalog nanochat (fresh weights, frozen P1.1 WikiText-TL-39 train documents, new P3 Tagalog BPE, depths 8 and 20) passes **P0-T**, freeze d20 as B0 and continue it for \(D_{\mathrm{phase2}}\) tokens on extra Tagalog (B1), English (B2), or a pre-frozen mix (B3), and test whether Tagalog held-out BPB rises by at least 0.01 more after English than after extra Tagalog (\(C_{\mathrm{tl}}\)), while English held-out BPB falls relative to B1 (\(G_{\mathrm{en}}\)).

### 1.2 Confirmatory questions (PDF MUST name these before any P3 BPB)

**RQ1 (retention / cost).** Is \(C_{\mathrm{tl}}\ge 0.01\)? Does English continuation raise Tagalog `val_bpb_full` more than matched extra Tagalog?

**RQ2 (acquisition / gain).** Is \(G_{\mathrm{en}}\le -0.01\)? Does English continuation lower English `val_bpb_full` more than extra Tagalog?

**RQ3 (B3, descriptive).** What EN/TL val trade-off does the **filed** B3 mix exhibit? **Not** mitigation unless a separate criterion is filed.

**RQ4 (P0-T).** Before any English **train** token: do TL0 d8 **and** d20 each beat untrained same-depth **and** Tagalog-train add-1 UTF-8 byte-unigram on **full Tagalog val** by the filed margin (default 0.01 BPB)? If either depth fails, **MUST NOT** run B1/B2/B3 under this registration.

### 1.3 Non-questions

- Reopening P1.1 D\* or P1.1/P2 test ledgers.  
- “P3 confirms P2.”  
- Switching B0 to d8 because TL0 d8 Tagalog val looks better.  
- SFT, CORE, EWC, replay grid, tokenizer swap, FilBench as confirmatory.  
- Loading P2 A2 as “already bilingual.”  
- Using P2’s realized A3 byte shares to pick B3 after filing.

### 1.4 Proposed filed-direction templates (lock in PDF; mechanical carry-over from P2 is allowed **with post-P2 disclosure**)

| Contrast | Template | After unblinding, say |
|---|---|---|
| \(C_{\mathrm{tl}}\) | \(\ge 0.01\) | observed / not observed **in this one-seed apparatus** |
| \(G_{\mathrm{en}}\) | \(\le -0.01\) | observed / not observed **in this one-seed apparatus** |

**MUST NOT** change these after any P3 BPB exists.

---

## 2. Notation

| Symbol | Meaning |
|---|---|
| TL0 | From-scratch Tagalog `base_train` on P3 Tagalog **train**, P3 Tagalog 32,768 BPE (unless PDF names another vocab) |
| B0 | Frozen TL0 **d20** final checkpoint; 0 additional train tokens |
| B1 | Extra Tagalog continuation from B0 for \(D_{\mathrm{phase2}}\) |
| B2 | English continuation from B0 for \(D_{\mathrm{phase2}}\) (treatment) |
| B3 | Mixed continuation from B0; recipe frozen at Gate E |
| \(T_{\mathrm{TL,train}}\) | P3 Tagalog BPE token count of Tagalog **train**, no BOS, no pack, no crop |
| \(D_{3x,\mathrm{TL}}\) | \(3\times T_{\mathrm{TL,train}}\) |
| \(N_{\mathrm{TL0}}\) | \(\lceil D_{3x,\mathrm{TL}}/B\rceil\) |
| \(B\) | 65,536 unless PDF says otherwise |
| \(T\) | 2048 |
| \(D_{\mathrm{phase2}}\) | Default \(294\times 65536=19{,}267{,}584\) **for directional comparability with P2 children**, unless PDF names another integer **before Gate A** |
| \(C_{\mathrm{tl}}\) | Tagalog `val_bpb_full`(B2) − Tagalog `val_bpb_full`(B1) |
| \(G_{\mathrm{en}}\) | English `val_bpb_full`(B2) − English `val_bpb_full`(B1) |
| P0-T | Tagalog parent eligibility (both depths, both floors) |
| 0.01 BPB | Not-a-ranking / practical cutoff **if filed** |

All P3 BPB **MUST** use the **same P3 Tagalog tokenizer**. P1.1 native-BPE 1.172248 is **incomparable** if the tokenizer differs.

---

## 3. Hypotheses (file these; do not peek at P3 outcomes)

**H1 (P0-T).** TL0 d8 and d20 Tagalog `val_bpb_full` each < untrained (same depth, same tok) by ≥0.01, **and** each < Tagalog-train add-1 byte-unigram on the same val UTF-8 by ≥0.01. If either depth fails either floor: **do not train B1/B2/B3**; report blocked parent-eligibility; no \(C_{\mathrm{tl}}\).

**H2 (cost).** \(C_{\mathrm{tl}}\ge 0.01\). Falsified if B2 Tagalog is not worse than B1 by 0.01 (including if B2 is better).

**H3 (gain).** \(G_{\mathrm{en}}\le -0.01\). Falsified if B2 English is not better than B1 by 0.01.

**H4 (B3).** Descriptive only: \(C_{\mathrm{tl}}(B3)=\mathrm{TL}(B3)-\mathrm{TL}(B1)\); \(G_{\mathrm{en}}(B3)=\mathrm{EN}(B3)-\mathrm{EN}(B1)\), plus mix shares. **Not** mitigation unless a separate criterion is filed.

Gaps with \(\lvert\Delta\rvert<0.01\) **MUST NOT** be called rankings. One seed: **MUST NOT** claim significance or a population law.

---

## 4. Threats (pre-register in the PDF or this protocol **dated before TL0 BPB**)

| Threat | Mitigation |
|---|---|
| Pretending P2 was unknown | Sentence 1 of the form + Gate 0 |
| Using P1.1/P2 `.pt` as parent | Gate C + child preflight reject listed SHA256s |
| Tokenizer mismatch | One P3 Tagalog BPE for TL0 and all children |
| Last-shard-is-val | Val parquet lexicographically last **or** filed packer; preflight hashes last shard |
| In-loop BPB used as DV | `eval-every` off or lockbox; caption; `meta.val_bpb` stripped |
| Wrong language stream | Preflight: B1 data-dir = Tagalog train only; B2 = English train only; B3 = Gate E mix only |
| Samples unblind B2 | `--sample-every -1` |
| Test peek | Gate U `test_access=0`; Gate V B2-only; raw test not in workspace |
| Fresh optimizer omitted | `load_optimizer=False`; no EN0/TL0 scheduler resume |
| `ratio -1` / warmup ≥ N | Gate G freeze |
| Changing B3 after BPB | Gate E read-only before Gate I |
| `meta` leak | Lockbox or strip |
| Operator sees P0-T table and switches to d8 | Script emits Boolean only |
| Combined unblinding skipped | Gate X after V |

---

## 5. Failure / stop criteria (any gate)

Stop confirmatory label (deviation card; do not silently continue) if:

- Any P3 BPB/sample/ranking is shown to the author before Gate X (except blocked-study P0-T scalars).  
- NaN/Inf loss or BPB.  
- ClimbMix / `python -m nanochat.dataset` / FineWeb / DCLM in a P3 train-visible path.  
- Val or test documents in a train directory.  
- New tokenizer after seeing confirmatory BPB.  
- `--target-param-data-ratio -1`.  
- P1.1 or P2 `model_*.pt` loaded as TL0 or child parent.  
- P1.1 `test_bpb=1.164768` or P2 Gate V numbers published as P3 B2.  
- P0-T fails and write-up still interprets B2 as reverse CF.  
- Attention kernel edited.  
- Shard SHA changes mid-run.  
- `--warmup-steps >= --num-iterations`.  
- B1 or B3 tested.  
- Second official val or test pass because a number was surprising.  
- Hub write to `p1-fixed-d20-3x` or `p2-en-then-tl`.  
- `scripts/p1/env.sh` or `scripts/p2/env.sh` sourced.

---

## 6. Filing blockers (MUST all be answered in the PDF or a **pre-Gate-A** dated addendum)

| ID | Decision |
|---|---|
| F-01 | **LOCKED:** reuse P1.1 `reconstructed_article_70_15_15` train/val/test **documents** (SHA256 in the PDF). **New P3 Tagalog 32768 BPE.** No rebuild or split substitution. |
| F-02 | **LOCKED:** WikiText-103-raw `Salesforce/wikitext` `wikitext-103-raw-v1`; HF revision SHA `b08601e04326c79dfdd32d625aee71d232d685c3` (raw-source archive identity). Official Merity train/valid/test. English **document-manifest** SHA256: val `874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b`; test `2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e`. These are not the raw HF archive hashes. Re-download and re-hash the archive; identity of confirmatory English val/test **documents** is the named manifests. |
| F-03 | **LOCKED:** train-only Tagalog, vocab 32768 |
| F-04 | **LOCKED:** \(D_{3x}=3\times T_{\mathrm{TL,train}}\) at the new BPE; \(B=65536\); \(T=2048\); \(N_{\mathrm{TL0}}=\lceil D_{3x}/B\rceil\); final ckpt |
| F-05 | **LOCKED:** 0.01; untrained and byte-unigram; joint d8 **and** d20; fail → no B1/B2/B3 |
| F-06 | **LOCKED:** B0 = d20 final only |
| F-07 | **LOCKED:** B1 extra TL train; B2 official WT103-raw train; B3 Gate E mix; tests never in train |
| F-08 | **LOCKED:** structural-mirror 50/50-**document** mix; seed 42; sha256-sort; \(K=\min(n_{\mathrm{en}},n_{\mathrm{tl}})\); interleave; freeze at Gate E before any TL0 val. Not mitigation. |
| F-09 | **LOCKED:** \(D_{\mathrm{phase2}}=294\times 65536=19267584\); **fresh pinned nanochat Muon+AdamW** (`load_optimizer=False`; no inherited optimizer/scheduler/scaler/resume); LR peak \(=0.3\times\) TL0 peak; warmup \(<N\) (default 14 if \(14<N\)) |
| F-10 | **LOCKED:** P1.1 val documents + official WT103-raw val **document manifest**; official `evaluate_bpb`; `bos_bestfit`; full val |
| F-11 | **LOCKED:** legacy external holdouts, **not** virgin P3 tests. English: WT103-raw **test document manifest** SHA256 `2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e`. Tagalog: P1.1 `test.jsonl` SHA256 `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf`. B2-only; `test_access=0` until one authorized touch (two component reads). **MUST NOT** cite 1.164768 or P2 Gate V numbers as P3. |
| F-12 | Lockbox: paths, roles (or documented one-person fallback), release = U seal + V complete unless blocked-P0-T |
| F-13 | Reporting grammar: post-P2, one-seed, B3 not mitigation, tests secondary |

**Six primary child val cells:** B1/B2/B3 × {Tagalog, English}. B0 Tagalog is P0-T. **B0 English `val_bpb_full` is evaluated once at Gate U** with the locked full evaluator, recorded descriptively in the seal, and **excluded** from \(C_{\mathrm{tl}}\), \(G_{\mathrm{en}}\), and B3 contrasts. **No** untrained-English confirmatory cell.

**AsPredicted related-studies field:** select **Overlapping** for #306780 and #306935. Do **not** select Independent or Draft. P3 does **not** amend them. Shared source observations: named frozen P1.1 Tagalog artifacts and named legacy holdouts. P3 weights, tokenizer, trajectories, and confirmatory BPB are new.

---

# STAGE 0 — FILING AND LOCKBOX (laptop, no GPU)

## Gate 0 — File P3, freeze hashes, install outcome lockbox

**Purpose.** Level-1 instrument. Without this PDF and passing lockbox tests, Gates A+ are wiring only.

**Host.** Laptop. **GPU: no.**

### 0.1 MUST before file

1. Read this protocol and `p3_blinding_and_outcome_lockbox_checklist.md`.  
2. Put the **post-P2 disclosure** in sentence 1 of the form.  
3. Resolve F-01–F-13 in the form or a hashed addendum.  
4. Cheng is **not** a coauthor; cite Cruz & Cheng 2019 for TL-39.  
5. Confirm **no** P3 `tok_train` / `base_train` / `evaluate_bpb` has run.

### 0.2 MUST after file

1. Save PDF to `docs/run-cards/AsPredicted-<P3ID>.pdf`. Record SHA256, page count, PT timestamps.  
2. Create ResearchBox **new** box (not 8735, not 8763). Passcode gitignored.  
3. Create:
   - `docs/papers/p3-reverse/LOCK.json`
   - `docs/run-cards/p3/<P3_RUN_ID>/`
   - `manifests/p3/`
   - `scripts/p3/env.sh`, `env.cuda.sh` (reviewed; **not** copies of P1/P2 env with P2_RUN_ID)
   - `$P3_SAFE_PROGRESS_ROOT` and `$P3_LOCKBOX_ROOT` with different Unix permissions
4. Hash: PDF, this protocol, pin commit, `scripts/p3/`, configs, seed/allocation table, `evaluate_bpb` (P3 copy), analysis/table script, lockbox tests.  
5. Define roles. If one person: document **weak fallback** (encrypted lockbox + time-lock or second-person key).  
6. Run lockbox acceptance tests (dummy data, **no** real val/test text):

| # | Test | Pass |
|---|---|---|
| 1 | Protocol/lock/config/evaluator/analysis hashes agree | |
| 2 | Steward cannot open dummy lockbox result | |
| 3 | Dummy BPB string absent from `safe_progress` and operator stdout | |
| 4 | If opacity selected, job labels do not contain B1/B2/B3 | |
| 5 | Train process cannot resolve test path | |
| 6 | P1.1/P2 weight SHA256s rejected as parent | |
| 7 | Dummy P0-T emits only PASS/BLOCKED outside lockbox | |
| 8 | Contrast script refuses until six child dummy val JSON plus dummy B0 EN descriptive exist | |
| 9 | Dummy test evaluator rejects B1/B3 and rejects missing U seal | |
| 10 | Release refuses incomplete inventory | |
| 11 | Dummy released hashes match manifest | |
| 12 | Break-glass dummy writes audit JSON without printing dummy BPB | |

7. Public pre-outcome snapshot: protocol + LOCK + scripts; **no** test JSONL, **no** `.pt`.

### 0.3 Pass evidence

- `gate-0-filing-lock.json`: AsPredicted ID, URL, PDF SHA256, `does_not_amend_306780=true`, `does_not_amend_306935=true`, `observation_independent_of_306780=false`, `observation_independent_of_306935=false`, `aspredicted_related=overlapping_306780_and_306935`, `designed_after_p2_gate_u=true`, `p2_gate_u_date=2026-08-19`, roles, lockbox tests, `no_p3_outcomes=true`.  
- `P3_LOCK.json`: immutable hashes and Gate X release condition (`U seal + V event complete` recommended).  
- `P3_PRE_OUTCOME_AUDIT.md`: F-01–F-13 checked.

### 0.4 Stop

Stop if any F-item is “decide later,” test text is in the training workspace, lockbox tests fail, or a P3 BPB file already exists.

---

# STAGE 1 — PIN AND HYGIENE (CPU)

## Gate A — Source pin and isolated P3 workspace

**Purpose.** Fresh namespace. No P1/P2 inheritance.

**Host.** CPU. **GPU: no.**

### A.1 Steps

1. `P3_RUN_ID=<UTC>-<short pin hash>`.  
2. Checkout filed nanochat commit under `$NANOCHAT_FILIPINO_ROOT/vendor/nanochat` **or** a P3-only clone if the PDF forbids sharing the vendor tree.  
3. Diff vs pin. Allowed: data-root / lockbox plumbing. **MUST NOT** change model/optimizer/attention/BPB.  
4. `mkdir -p data/cache/$P3_RUN_ID` and write `SENTINEL_P3_ONLY`.  
5. Scan: no `NANOCHAT_BASE_DIR` pointing at `p1-` or `p2-` cache; no `source scripts/p1/env.sh`.  
6. Confirm no `python -m nanochat.dataset`, `ratio=-1`, HF Trainer.

### A.2 Receipt

`gate-a-source-pin.json`: commit, allowed-diff SHA256, sentinel path, prohibited-path scan, `no_p3_outcomes=true`.

### A.3 MUST NOT

Start `tok_train` or `base_train`.

---

## Gate B — Named source acquisition

**Purpose.** Exact Tagalog and English raw identity.

**Host.** CPU.

### B.1 Steps

1. Download **only** F-01 and F-02 assets. Record URL, config, revision, license, bytes, SHA256, UTC.  
2. `chmod` raw archives read-only.  
3. English **MUST NOT** be P2’s `english_test.jsonl` copied as “train.” Re-hash official WT103-raw.  
4. Tagalog: either reconstruct per PDF or copy **P1.1 frozen split files** with explicit `p11_split_reuse=true` and those files’ SHA256s.

### B.2 Receipt

`gate-b-raw-assets.json`, one row per artifact, `no_train_or_eval_started=true`.

---

## Gate C — Hygiene, leakage, lineage

**Purpose.** Clean apparatus.

### C.1 Checks (all MUST be true)

| ID | Check |
|---|---|
| C1 | P3 cache = sentinel + allowed raw only |
| C2 | No ClimbMix/FineWeb/DCLM/OSCAR in P3 train-visible paths |
| C3 | No P1.1/P2 checkpoint in parent candidate list |
| C4 | Future test inputs absent from tok/train/val roots; not resolvable by train process |
| C5 | No secrets in git |
| C6 | Filed PDF not writable as “working copy” for silent edits |
| C7 | P1/P2 Hub not a write target |
| C8 | Lockbox vs safe-progress permissions pass |

### C.2 Receipt

`gate-c-hygiene.json`: per-check Boolean, `test_access_count=0`, `p3_outcome_access_count=0`.

---

# STAGE 2 — SPLITS AND MIX (CPU)

## Gate D — Document reconstruction and split freeze

**Purpose.** Freeze IDs before packing/tok/TL0.

### D.1 Tagalog

1. Apply F-01 reconstruction/split.  
2. Freeze document IDs, hashes, UTF-8 bytes, row counts, split SHA256s.  
3. Exact-document and exact-hash overlap **MUST** be 0 across train/val/test.  
4. Record `split_origin=p11_reuse|p3_new`.

### D.2 English

1. Apply F-02 (recommended: Merity **official** WT103-raw train/valid/test, as P2).  
2. Freeze hashes. Isolation train/val/test.  
3. If using a previously scored test, `legacy_external_holdout=true`.

### D.3 Receipt

`gate-d-split-freeze.json` + read-only JSONL/parquet. **No BPB.**

### D.4 MUST NOT

Reshuffle after this gate. **MUST NOT** put test JSONL in the train/val data-dir.

---

## Gate E — Pack streams and **pre-freeze B3**

**Purpose.** B3 frozen **before Gate I / any TL0 full val BPB**, not merely before Gate T.

**Host.** CPU.

### E.1 Steps

1. Pack Tagalog train/val in filed order; val last lexicographically **or** document the packer.  
2. Pack English train/val likewise.  
3. Read-only copies: B1 root = Tagalog train only; B2 root = English train only.  
4. Build B3 **once** from F-08:
   - Mirror: 50/50 **documents**, seed, K, interleave/cycle; **or**
   - Redesign: full rule + post-P2 rationale **already in PDF**.  
5. Record seed, K, n_docs, UTF-8 bytes, **later** BPE tokens (after Gate F), mix-order SHA256, construction UTC.  
6. `chmod` mix + manifest read-only.

### E.2 Receipt

`gate-e-packed-streams-and-b3-freeze.json`, `p3_outcome_access_count=0`, `b3_frozen_before_tl0_val=true`.

### E.3 MUST NOT

Rebalance B3 after seeing P2 byte shares **unless that redesign is F-08**. **MUST NOT** wait until after P0-T to freeze B3.

---

# STAGE 3 — TOKENIZER AND BUDGET (CPU)

## Gate F — P3 Tagalog tokenizer

**Purpose.** One BPE for **all** P3 BPB.

**Host.** CPU.

### F.1 Steps

1. `NANOCHAT_DATA_DIR` = **Tagalog train parquets only**.  
2. Filed vocab and caps.  
3. **MUST NOT** feed English, val, test, B3 mix, P1.1 `tokenizer.pkl`, or P2 `tokenizer.pkl`.  
4. Save `tokenizer.pkl`, `token_bytes.pt`; SHA256; read-only.  
5. Fertility on val UTF-8 (TL and EN) **MAY** be computed; store in **lockbox** if it could tempt redesign; release at Gate X as diagnostics, **not** DVs.

### F.2 Receipt

`gate-f-tokenizer.json`, artifact hashes, input manifest, `no_p3_bpb=true`.

### F.3 MUST NOT

Train a second tokenizer after Gate I.

---

## Gate G — Budget, hyperparameter, and command freeze

**Purpose.** Integers and argv **immutable**.

### G.1 Compute

| Quantity | Definition |
|---|---|
| \(T_{\mathrm{TL,train}}\) | Sum of P3 BPE tokens over Tagalog **train** docs, no BOS, no pack, no crop |
| \(D_{3x,\mathrm{TL}}\) | \(3\times T_{\mathrm{TL,train}}\) |
| \(N_{\mathrm{TL0}}\) | \(\lceil D_{3x,\mathrm{TL}}/B\rceil\) |
| \(D_{\mathrm{actual,TL0}}\) | \(N_{\mathrm{TL0}}\times B\) |
| \(N_{\mathrm{phase2}}\) | \(D_{\mathrm{phase2}}/B\) (294 if \(D_{\mathrm{phase2}}=19267584\) and \(B=65536\)) |
| Warmup TL0 | Filed; **MUST** be \(< N_{\mathrm{TL0}}\) |
| Warmup phase-2 | Filed; **MUST** be \(< N_{\mathrm{phase2}}\) (P2 used 14) |
| Phase-2 LR | Filed, e.g. 0.3 × TL0 peak |

### G.2 Freeze commands (write exact argv into `gate-g-budget-command-freeze.json`)

1. TL0 d8 and d20: `--num-iterations $N_TL0`, `--depth`, `--max-seq-len 2048`, `--window-pattern SSSL`, `--device-batch-size 8`, `--total-batch-size 65536`, `--eval-every` **off or lockbox**, `--core-metric-every -1`, `--sample-every -1`, `--save-every -1`, `--model-tag p3-tl0-d{8,20}`.  
2. B1/B2/B3: `--num-iterations $N_phase2`, same T/B/window, fresh opt, `--init` from B0, **no** optimizer load.  
3. Evaluator: full val; stdout to lockbox.  
4. Test wrapper: B2 SHA must match U seal; reject B1/B3 paths.

### G.3 MUST NOT

`ratio=-1`; implicit N; warmup ≥ N; unlogged argv edits.

### G.4 Receipt

`gate-g-budget-command-freeze.json` + human command manifest. **No BPB visible.**

---

# STAGE 4 — CUDA SMOKE

## Gate H — Official CUDA smoke (not TL0)

**Purpose.** Path works. **MUST NOT** start confirmatory TL0.

**Host.** CUDA NVIDIA. **GPU: yes.** Authorization: **MUST**.

### H.1 Conditions

1. `nvidia-smi`; filed GPU class; disk; P3 hashes.  
2. **d4 only**, 30 iterations, warmup **10% of 30 or 3**, tag `p3-smoke-d4-*` **not** `p3-tl0-*`.  
3. Safe telemetry: `health=pass` if loss **below same-run init** (P1.1/P2 Gate H rule) **without** printing the loss curve to the author; or `finite` + `reload_ok` if the PDF files that weaker rule.  
4. In-loop eval if used: lockbox or `finite/nonfinite` only.

### H.2 Receipt

`gate-h-cuda-smoke.json`: hardware, pin, command, `finite`, `reload_ok`, `below_init` if filed, `no_confirmatory_training=true`.

### H.3 MUST NOT

Mac MPS; Spark unless new P3 smoke card; attention patch; reuse P2 smoke checkpoint.

---

# STAGE 5 — PARENT

## Gate I — TL0 d8 and d20

**Purpose.** Fresh Tagalog parents. **No English train token.**

**Host.** CUDA. **GPU: yes.** Authorization: **MUST**.

### I.1 Steps

1. Preflight: tokenizer SHA, Tagalog train SHA, empty output dirs, P1/P2 SHAs **rejected**, tests unmounted.  
2. Train d8 for **exactly** \(N_{\mathrm{TL0}}\).  
3. Train d20 for **exactly** \(N_{\mathrm{TL0}}\).  
4. **Final checkpoint only** (not min in-loop val).  
5. Metrics/samples → lockbox. Safe: step, `health`, checkpoint bytes, SHA, `reload_ok`.  
6. Copy to local `data/cache/$P3_RUN_ID/`; verify SHA; read-only.

### I.2 Receipt

`gate-i-tl0-d8.json`, `gate-i-tl0-d20.json`: step, SHA256, size, `tokens_seen=N_TL0*B`, `test_access=0`, **no BPB field**.

### I.3 MUST NOT

Start English continuation. Rank d8 vs d20 from in-loop. Early-stop.

---

## Gate P0-T — Tagalog parent eligibility

**Purpose.** Both depths beat both Tagalog floors **before any English child token**.

**Host.** CUDA. **GPU: yes in practice.**

### P0-T.1 Evaluate (outputs → **lockbox only**)

For TL0 d8 **and** d20 **final** ckpts:

1. Full P3 Tagalog val `val_bpb_full` (P3 BPE, official packing).  
2. Untrained same-depth, same tok, same val.  
3. Byte-unigram: add-1 on **P3 Tagalog train UTF-8**, score **Tagalog val UTF-8**.

**MUST NOT** use English val to pass/fail P0-T.  
**MUST NOT** use P1.1 1.172248 as a floor.  
**MUST NOT** use P2 A2 Tagalog val as a floor.

### P0-T.2 Automated rule (no human discretion)

| Condition | Safe emit |
|---|---|
| Both depths beat both floors by filed margin | `P0-T: PASS` |
| Either depth fails either floor | `P0-T: BLOCKED` — **MUST NOT** run R/S/T |
| Hash/eval crash | `P0-T: TECHNICAL BLOCK` — no scalars on safe log |

### P0-T.3 Blinding

Lockbox holds all scalars and gaps. Safe file `gate-p0-t-status.json` = status + seal hash of lockbox JSON **only**.

If **BLOCKED**: Gate X/W **blocked-study path** **MAY** release P0-T scalars (children will not exist).  
If **PASS**: P0-T scalars wait for **Gate X**.

### P0-T.4 Receipt

Lockbox `gate-p0-t-eligibility.json` (full). Safe `gate-p0-t-status.json` (Boolean).

### P0-T.5 MUST NOT at this gate

Evaluate B0 English `val_bpb_full` here. That descriptive cell is evaluated **once** at Gate U with the locked full evaluator.

---

## Gate Q — Immutable B0 freeze

**Purpose.** Only legal child parent = TL0 **d20** final.

**Host.** CPU or CUDA (copy). **No extra train.**

### Q.1 Steps

1. Copy d20 `model_*.pt` to `data/cache/$P3_RUN_ID/b0/frozen/p3-tl0-d20/`.  
2. SHA match Gate I.  
3. Read-only. Permissions are **not** lineage; SHA is.  
4. Record architecture, step, tokenizer SHA, pin, `p0_t_status=PASS`.  
5. Child wrappers: `--load` B0; `load_optimizer=False`; **MUST NOT** `--resume` TL0 optimizer. Fresh pinned **Muon+AdamW** (Muon matrices; AdamW embeddings/unembeddings/scalars). No inherited optimizer, scheduler, scaler, or resume state.  
6. **MUST NOT** parent = d8, P1.1, P2 A0–A3, or another B child.

### Q.2 Receipt

`gate-q-b0-freeze.json`: B0 SHA, `immutable=true`, `additional_train_tokens=0`, whitelist.

---

# STAGE 6 — MATCHED CHILDREN (CUDA)

Shared child preflight (R, S, T each **MUST**):

1. B0 SHA = Gate Q.  
2. P3 tokenizer SHA = Gate F.  
3. Fresh optimizer.  
4. Exact Gate G argv.  
5. Empty output tag.  
6. Tests unmounted.  
7. Data-dir last shard hashed; language identity matches the arm.  
8. Operator-visible `meta` stripped or lockboxed.  
9. Explicit human authorization JSON.

## Gate R — B1 extra-Tagalog control

**Purpose.** Matched non-English continuation. **Without B1, \(C_{\mathrm{tl}}\) is not causal.**

**Host.** CUDA. Authorization: **MUST**.

### R.1

- Data-dir: **B1 Tagalog train only** (not val, not test, not English, not B3).  
- \(N=N_{\mathrm{phase2}}\), same B, T, warmup, LR as S/T.  
- Safe log: steps, health, SHA. Metrics → lockbox.

### R.2 Receipt

`gate-r-b1.json`: B0 SHA, B1 SHA, `D_phase2`, stream id, `reload_ok`, `test_access=0`, **no BPB**.

### R.3 MUST NOT

Start S on the same GPU without B1 hash snapshot. Use B1 as parent of B2.

---

## Gate S — B2 English intervention

**Purpose.** First English **train** token on this parent.

**Host.** CUDA. Authorization: **MUST**.

### S.1 Preconditions

Gate R passed; B1 read-only; **not** a parent.

### S.2

- Data-dir: **English train only**.  
- Same B0, tokenizer, N, B, T, opt as B1 except data.  
- **MUST NOT** Tagalog train, B3, or test in the data-dir.

### S.3 Receipt

`gate-s-b2.json`: hashes, stream, budget, `test_access=0`, **no BPB**.

---

## Gate T — B3 frozen mix

**Purpose.** Filed trade-off arm. **Not mitigation during execution.**

**Host.** CUDA. Authorization: **MUST**.

### T.1 Preconditions

R and S passed; B1/B2 read-only; Gate E mix SHA unchanged.

### T.2

Train **only** on frozen B3 input for exact \(D_{\mathrm{phase2}}\).

### T.3 Receipt

`gate-t-b3.json`: mix-order SHA, K, realized doc/byte shares (tokens if counted at E/F), B3 SHA, `test_access=0`, **no BPB**.

---

# STAGE 7 — PROTECTED MEASUREMENT

## Gate U — Six child validations + B0 English descriptive + lockbox seal

**Purpose.** Official `evaluate_bpb` on **val only**. Compute \(C_{\mathrm{tl}}\) and \(G_{\mathrm{en}}\) **once** after all six **child** cells. Record B0 English once as descriptive. Tests unread.

**Host.** CUDA. Authorization: **MUST**.

### U.1 Preconditions

B0/B1/B2/B3 SHA reloadable; children all from B0; evaluator/tok/val hashes = LOCK; tests unmounted.

### U.2 Order (lockbox files)

| # | Ckpt | Split | Role | Output |
|---|---|---|---|---|
| 1 | B1 | English val | primary child | `b1_en_val_bpb_full.json` |
| 2 | B1 | Tagalog val | primary child | `b1_tl_val_bpb_full.json` |
| 3 | B2 | English val | primary child | `b2_en_val_bpb_full.json` |
| 4 | B2 | Tagalog val | primary child | `b2_tl_val_bpb_full.json` |
| 5 | B3 | English val | primary child | `b3_en_val_bpb_full.json` |
| 6 | B3 | Tagalog val | primary child | `b3_tl_val_bpb_full.json` |
| 7 | B0 | English val | descriptive only | `b0_en_val_bpb_full.json` |

**MUST NOT** add an untrained-English confirmatory cell. Copy **B0 Tagalog** from the P0-T lockbox into the seal (not a new confirmatory look). **MUST** evaluate B0 English **once** at Gate U with the same locked full evaluator; record it in the seal **separate** from the six child cells; **MUST NOT** use it in \(C_{\mathrm{tl}}\), \(G_{\mathrm{en}}\), or B3 contrasts.

### U.3 Seal script (MUST be frozen at Gate 0)

1. Require the six child files plus `b0_en_val_bpb_full.json`; matching ckpt/input/eval/tok hashes.  
2. \(C_{\mathrm{tl}}=\mathrm{TL}(B2)-\mathrm{TL}(B1)\); \(G_{\mathrm{en}}=\mathrm{EN}(B2)-\mathrm{EN}(B1)\). Exclude B0 English from both and from B3 contrasts.  
3. B3 row + Gate E shares; `not_mitigation=true` unless PDF filed otherwise.  
4. Write immutable `p3-validation-seal.json` in lockbox.  
5. Safe: `seven Gate U val outputs complete (six child + B0 EN descriptive); validation seal created; P3 test access = 0`.

### U.4 MUST NOT

Print BPB to stdout; rank arms; rerun a cell; touch test; compute a test contrast.

### U.5 Receipt

Lockbox seal + safe `gate-u-status.json` (hashes/status only).

---

## Gate V — One B2-only secondary test event

**Purpose.** After U, exactly one authorized touch: filed English test + filed Tagalog test on **B2 only**.

**Host.** CUDA. **Separate authorization MUST.**

### V.1 Preconditions

U seal exists; `test_access=0`; B2 SHA matches seal; test wrapper rejects B1/B3; raw text not in normal workspace.

### V.2 Execution

1. Log `docs/run-cards/p3/test_access_log.json` (P3 ledger, **not** P1.1 or P2).  
2. Evaluate B2 English test → lockbox.  
3. Evaluate B2 Tagalog test → lockbox.  
4. `authorized_touches=1`, `component_evaluations=2`.  
5. **MUST NOT** test B1/B3; **MUST NOT** second B2 read; **MUST NOT** echo test text; **MUST NOT** revise \(C_{\mathrm{tl}}\)/\(G_{\mathrm{en}}\).

### V.3 Strong default (recommended in LOCK)

**Do not unblind U scalars until V is also in the lockbox** (Gate X). Minimum legal: unblind U then run V with test rule already frozen (P2-like).

### V.4 Receipt

Lockbox `gate-v-test.json`. Safe: `one authorized B2-only test event completed`.

---

## Gate X — Formal P3 unblinding

**Purpose.** Single timestamped release of **all** planned P3 scalars.

**Host.** Laptop. **GPU: no.**

### X.1 Release condition (all MUST)

| Requirement | State |
|---|---|
| P0-T | PASS, or BLOCKED path fully reported |
| B0–B3 | Hashes + lineage |
| U | Six child cells + B0 EN descriptive + immutable seal |
| V | One B2-only event; no B1/B3 test |
| Test access | 1 |
| Source | Matches LOCK or deviation card |
| Break-glass | None, or documented |
| `meta`/logs | No unlogged public BPB leak |

### X.2 Actions

1. Write `P3_UNBLINDING_EVENT.json`: UTC, releaser, condition, artifact list, SHA256s, `raw_test_still_restricted=true`.  
2. Release **simultaneously:** P0-T scalars, six val cells, \(C_{\mathrm{tl}}\), \(G_{\mathrm{en}}\), B3 table, B2 tests, B0 baselines if collected.  
3. Run **pre-frozen** table/paper script. **MUST NOT** add metrics.  
4. Grammar: observed / not observed / blocked; one-seed; post-P2; B3 not mitigation; tests secondary.

### X.3 Receipt

Released bundle SHA = lockbox manifest.

---

# STAGE 8 — CLOSE-OUT

## Gate W — Archive, paper, ResearchBox, code, Hub, site

**Purpose.** Audit trail. **No new P3 computation.**

**Host.** Laptop.

### W.1 Archive

`p3_closeout_manifest.json`: every artifact role, bytes, SHA256, UTC. Exclude: raw tests, secrets, SSH, `.env`, optimizer states unless PDF says otherwise.

### W.2 ResearchBox

New box: protocol, PDF, code, non-sensitive receipts, sealed JSON (after X), paper. **No** `test.jsonl`. **No** passcode in git.

### W.3 GitHub

Subtree `docs/p3/`, `results/p3/`, `scripts/p3/` on `pageman/nanochat-filipino`. **MUST NOT** mix into `results/` P1.1 files or `results/p2/` seals. Logs: `$NANOCHAT_FILIPINO_ROOT`; trainer logs caption **in-loop BPB is not the primary DV**.

### W.4 Hub

If weights released: **B0+B1+B2+B3 together** + `meta` + tokenizer. Never B2 alone. Never P1.1/P2 Hub. Card: post-P2, one-seed, not chat.

### W.5 Paper

Compile from frozen source; check decimals against seal. **MUST NOT** say P3 confirmed P2.

### W.6 Infra

Terminate GPU/volume only after local + external hash verification.

### W.7 Reporting substitutions

| Required | Prohibited |
|---|---|
| Designed after P2 unblinding; locked before P3 outcomes | Independently confirmed P2 |
| Pattern observed/not observed, one seed | Universal reverse forgetting law |
| B3 predeclared trade-off | B3 mitigates (unless filed and met) |
| B2 tests secondary | Tests are a B2−B1 causal contrast |

---

## Deviation / break-glass

| Incident | Allowed | Forbidden |
|---|---|---|
| Crash before terminal ckpt | Resume **as filed**; deviation card | Change N because of cost |
| SHA mismatch | Retransfer; stop if unverified | Silent retrain |
| NaN/Inf | Stop; preserve logs | New LR, still call it B2 |
| Lockbox key failure | Restore; record if scalars exposed | Quietly read BPB and continue “blind” |
| Test-path leak | Stop | Hide and continue |
| Surprising number | Wait for Gate X | Rerun val; test B1 |

Every event: `P3_BREAK_GLASS_<UTC>.json`.

---

## Readiness checklist (Gate A starts only if all true)

| # | Assertion | ☐ |
|---|---|---|
| 1 | P3 filed as post-P2 prospective; no false independence | |
| 2 | F-01–F-13 resolved | |
| 3 | LOCK, pin, evaluator, commands, analysis frozen | |
| 4 | Isolated from P1.1/P2 weights and env | |
| 5 | B3 identity frozen before any P3 BPB | |
| 6 | Raw tests restricted | |
| 7 | P0-T emits only PASS/BLOCKED before X (unless blocked path) | |
| 8 | Safe logs have no BPB/loss/samples/rankings; `meta.val_bpb` cannot leak | |
| 9 | U requires six child vals + B0 EN descriptive + lockbox seal | |
| 10 | V is B2-only and requires U seal | |
| 11 | X release condition tested | |
| 12 | Break-glass template exists | |
| 13 | No P3 tok/train/eval/test has run | |

---

## Definition of done

P3 is complete iff: the filed design ran without unlogged material deviation; P0-T was PASS or an honest BLOCKED report; B1/B2/B3, U, and V followed the filed path; `P3_UNBLINDING_EVENT.json` exists; results are reported with post-P2 and one-seed limits; and the archive is deposited **without** raw test text or secrets.

---

## Absolute hard stops (copy)

| ID | Prohibited |
|---|---|
| HS-01 | P3 compute before form + lockbox freeze |
| HS-02 | Claiming P3 independent of P2 |
| HS-03 | P1.1/P2 weights as parent |
| HS-04 | Changing B3 after any P3 BPB |
| HS-05 | Viewing P3 BPB/samples/rankings before X |
| HS-06 | Raw test in ordinary workspace or train |
| HS-07 | Testing B1 or B3 |
| HS-08 | Rerunning official val/test because surprising |
| HS-09 | SFT/replay/EWC/CORE/tokenizer-swap in confirmatory table |

---

## References

1. AsPredicted #306780 (P1.1); #306935 (P2).  
2. `docs/PROTOCOL-project1-wikitext-tl39.md`; `docs/papers/p2-cf-english/PROTOCOL-p2-en-then-tl.md`.  
3. Staged source: `P3 Comprehensive Staged Execution Protocol.md`.  
4. Lockbox: `p3_blinding_and_outcome_lockbox_checklist.md`.
