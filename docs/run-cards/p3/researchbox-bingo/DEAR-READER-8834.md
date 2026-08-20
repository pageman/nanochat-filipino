# Dear Reader — ResearchBox #8834 (P3 only)

**Paste this into the ResearchBox “Dear Reader” field for box [#8834](https://researchbox.org/8834).**  
Not for P1.1 (#8735). Not for P2 (#8763). Not included in download zips—online display only.

---

Dear Reader,

Thank you for opening **ResearchBox #8834**, the deposit box for **NANOCHAT-FILIPINO P3** (“TL retention after EN continuation”).

This note exists because (1) P3 is easy to confuse with P1.1 and P2, (2) ResearchBox’s bingo columns are awkward for a computational LM study, (3) several absences are intentional, (4) P3 was **designed after P2 was unblinded** and must never be sold as an independent confirmation of P2, and (5) a Gate S data-staging incident was recovered in a documented way that must not be misread as result-informed arm selection. Please read this before citing any CSV cell or JSON field as “the P3 result.”

---

## 1. What this box is (and is not)

### 1.1 This box is

- The **results-provenance and reproducibility metadata deposit** for one preregistered computational study:
  - **AsPredicted #307342** — https://aspredicted.org/wd2pc8.pdf  
  - PDF SHA-256: `6cfad0386dff689ad73fa2bf80b70dd4ad191dc44e21e3e4c11c06825ae550b1`
- A **one-seed**, fixed-parent, fixed-budget **continual-pretraining** experiment on **nanochat**, pinned commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`.
- Documentation for run ID **`p3-20260819T192700Z-92d63d4`**, Gates **0 / A–X** complete (`gate_x_unblinded`).
- A place to find **tables, hashes, scripts, protocol, sealed validation/test JSON, and (when ready) paper** consistent with the filing.
- Linked results-provenance on AsCollected: https://ascollected.org/F36_C2C (project **#2440**, Version 1).

### 1.2 This box is not

- **Not** ResearchBox **#8735** (P1.1, AsPredicted **#306780** — equal-budget Tagalog depth study).
- **Not** ResearchBox **#8763** (P2, AsPredicted **#306935** — EN→TL continual pretraining).
- **Not** a human-subjects study. No participants, Prolific IDs, surveys, or consent forms.
- **Not** a redistribution of raw held-out `test.jsonl` / WikiText-103 test article text.
- **Not** where model **`.pt` weights** live (Hub release is separate/optional; if released, B0+B1+B2+B3 together).
- **Not** an amendment to P1.1 or P2. P3 does **not** rewrite #306780, #306935, #8735, #8763, or prior Hubs.
- **Not** “P2 confirmed in reverse.” It is a **post-P2 reverse-direction** preregistration.

If you arrived expecting P1.1 depth selection or P2 EN→TL contrasts, switch boxes.

---

## 2. Critical disclosure (post-P2 timing)

P3 was **designed after P2 Gate U/V unblinding on 19 August 2026**. Operators may know P2 outcomes.  

What did **not** exist at P3 filing: P3-specific tokenizer, TL0/B0–B3 trajectories, P3 `val_bpb_full`, or P3 test BPB.

Required public grammar:

- Say **post-P2 reverse-direction preregistration**.
- Do **not** say independently chosen without P2 knowledge.
- Do **not** say P3 confirms P2.
- Report **observed / not observed** for filed directional patterns; one seed; no CI/p-value/population claim.

---

## 3. How the bingo table is organized (nonintuitive layout)

| Column | What we put there | What we deliberately did *not* |
|---|---|---|
| **Preregistration** | AsPredicted **#307342** (imported chip) | A second PDF unless import failed |
| **Materials** | Protocol, sanitized LOCK, study README, AsCollected note, paper when ready | Raw corpora; weights; HOST SSH cards |
| **Data** | Small **CSV tables only**, uploaded **one file at a time** | Multi-file Data zips; `.json` seals; prose `.md` as Data |
| **Code** | `scripts/p3/` and/or `p3_code_crosswalk*.csv` | Secrets; P1/P2 env scripts; `.pt` |
| **Other** | Gate receipts 0/A–X, `released/*.json`, unblinding event, closeout manifest | The sole confirmatory “Data” chip |

Suggested sections: keep the AsPredicted chip on a **Preregistration** row; put Materials/Data/Code/Other under **P3 Confirmatory Close-out**.

### 3.1 Why Data looks “too small”

Confirmatory objects of record are **JSON seals + hashes + scripts**. ResearchBox prefers tidy tables for Data, so:

1. Point estimates and contrasts appear in CSV under Data.  
2. Machine-readable seals live under **Other** (and locally under `released/`).  
3. Public training corpora are obtained elsewhere (HF / frozen P1.1 splits); they are not re-uploaded as raw text Data.

### 3.2 Hex strings are file hashes, not people

64-character hex columns (often prefixed `sha2-256:`) are **SHA-256 of files**. ResearchBox may flag them as Prolific IDs. **False positive.** P3 has no human participants.

### 3.3 Code codebook shape

If you see `p3_code_crosswalk_3_columns.csv`, it is **17 rows × 3 columns** (`Variable` = var1…var17, `Variable Name`, `Description`) documenting the columns of the full code inventory—not three rows.

---

## 4. Study design in one paragraph

P3 starts from a **fresh Tagalog parent** (TL0; new weights; frozen P1.1 WikiText-TL-39 train docs; **new P3 Tagalog 32,768 BPE**). After **P0-T** PASS at d8 and d20, freeze d20 as **B0**, then compare three **equal-budget** continuations from that **immutable common parent**:

| Arm | Treatment | Role |
|---|---|---|
| **B1** | Extra Tagalog | Active control |
| **B2** | English continuation (WikiText-103-raw) | Intervention |
| **B3** | Pre-frozen **50/50-document** EN+TL mix | **Trade-off / descriptive**, **not mitigation** |

Primary DVs: full-validation **`val_bpb_full`** (locked `evaluate_bpb.py`), **not** in-loop `meta.val_bpb`.

Registered primary contrasts (signs matter):

- \(C_{TL} = TL(B2) - TL(B1)\) — predicted \(\ge 0.01\)
- \(G_{EN} = EN(B2) - EN(B1)\) — predicted \(\le -0.01\)

Practical cutoff: **0.01 BPB**. One seed. Point estimates only.

Budget (filed/frozen): \(N=294\), \(B=65536\), \(T=2048\), \(D_{\mathrm{phase2}}=19{,}267{,}584\); fresh optimizer (`load_optimizer=False`); peak LR \(= 0.3 \times\) TL0; warmup 14.

---

## 5. What the sealed numbers say (narrow claims)

Gate X released the precommitted package. From the validation seal (primary):

| Contrast | Approximate sealed value | Filed rule | Call |
|---|---|---|---|
| \(C_{TL}\) | **+1.023484** | \(\ge 0.01\) | **Observed** |
| \(G_{EN}\) | **−1.697955** | \(\le -0.01\) | **Observed** |
| \(C_{TL}(B3)\) | **−0.275035** | report only | Trade-off; **not mitigation** |
| \(G_{EN}(B3)\) | **−1.683684** | report only | Trade-off; **not mitigation** |

B0 English `val_bpb_full` ≈ **2.618891** is **descriptive only** and **excluded** from contrasts.

Interpretation boundaries:

- This estimates the registered English-vs-extra-Tagalog continuation contrast in **this apparatus**, not a universal law of languages or models.
- Do **not** call B3 “mitigation,” “best,” or a replacement primary arm.
- Do **not** rank arms by \(|\Delta|\) or crown a “winner.”
- Do **not** claim P3 confirmed P2.

### Secondary Gate V (after seal; one touch; B2 only)

| Holdout | Approx. `test_bpb` | Notes |
|---|---|---|
| English WT103-raw test manifest | **≈ 1.357842** | Secondary; not a test-set \(C_{TL}\) |
| Legacy Tagalog P1.1 `test.jsonl` | **≈ 2.493197** | Legacy external holdout under **P3** Tagalog BPE; **not** virgin P3 test; **do not** reuse P1.1 **1.164768** or P2 Gate V numbers |

A1/B1 and B3 were **not** tested. `test_access`: **0** at U seal → **1** after V. Gate V does not alter sealed \(C_{TL}\)/\(G_{EN}\).

---

## 6. Idiosyncratic files and reading traps

### 6.1 `val_bpb_full` vs in-loop `val_bpb`

Confirmatory DV is full-split `val_bpb_full` from `scripts/p3/evaluate_bpb.py`. Trainer logs / `meta_*.json` in-loop values are diagnostics only.

### 6.2 Tokenizer coordinate system

All confirmatory P3 cells use the **same P3 Tagalog BPE**. P1.1 native-BPE numbers (e.g. val ≈ 1.172248) are **incomparable** if treated as the same metric space.

### 6.3 B3 “50/50”

Means **document count** in the mix frozen **before** TL0 validation (seed 42, `K=28472`), **not** equal byte/token exposure. Report realized shares; do not call token exposure equal.

### 6.4 Gate S incident (read this)

Early Gate S attempts failed because English training data were missing/corrupt (including AppleDouble junk), producing a **non-official** zero-step / partial path.  

**Official disposition (Gate X preflight):** partial attempt **quarantined**; **clean restart from frozen B0** with fresh optimizer on `data/staging/en-clean`, 294 steps, exit 0. No result-informed choice of arm or metric. Documented in `gate-x-preflight.json` / Other receipts.

### 6.5 Parent lineage

B1/B2/B3 share byte-identical **B0** (`ae621be2…`). P1.1/P2 weights are **never** the P3 parent.

### 6.6 Intentional absences

| Missing here | Why |
|---|---|
| Raw `test.jsonl` / WT103 test text | Holdout integrity; hashes identify files |
| `.pt` checkpoints | Size; optional Hub host; never B2 alone |
| Passcodes / API keys / SSH cards | Secrets |
| Paper PDF | May still be in progress; seal is authoritative for numbers |

### 6.7 Authority hierarchy

1. Filed AsPredicted **#307342** PDF  
2. Locked P3 protocol / scripts consistent with the filing  
3. Gate receipts / `released/` / `LOCK` / unblinding event  
4. Dated deviation cards  
5. Paper / website / Hub / this Dear Reader note  

---

## 7. Where large artifacts live

| Artifact | Location |
|---|---|
| Code + run cards | https://github.com/pageman/nanochat-filipino (`scripts/p3/`, `docs/run-cards/p3/…`) |
| This deposit | https://researchbox.org/8834 |
| AsCollected | https://ascollected.org/F36_C2C |
| Preregistration | https://aspredicted.org/wd2pc8.pdf |
| Protocol SHA-256 | `899ba83f0b36f2b4bf4c16b3c675e58788d7763cb439f8a8c3a3c061bda2b986` |
| Weights (if/when released) | Separate Hub repo; **B0+B1+B2+B3 together** |

---

## 8. Suggested reading order

1. AsPredicted #307342 — hypotheses, cutoffs, exclusions, lockbox/test-touch rules.  
2. This Dear Reader note.  
3. Data CSV crosstab — cells, contrasts, B2 tests at a glance.  
4. `released/p3-validation-seal.json` + child cell JSONs (Other).  
5. `released/gate-v-test.json` + `test_access_log.json`.  
6. Gate R/S/T receipts — common B0 parent, step 294.  
7. `P3_UNBLINDING_EVENT.json` + `gate-x-preflight.json`.  
8. Code crosswalk / `evaluate_bpb.py`.  
9. Paper (when present) — must keep post-P2 / one-seed / observed grammar.

---

## 9. Related studies (separate boxes)

| Study | AsPredicted | ResearchBox | Relation to P3 |
|---|---|---|---|
| **P1.1** | [#306780](https://aspredicted.org/6r6v4v.pdf) | [#8735](https://researchbox.org/8735) | Overlapping Tagalog split observations; **not** P3 parent; do not reuse `test_bpb=1.164768` as P3 |
| **P2** | [#306935](https://aspredicted.org/xa56bs.pdf) | [#8763](https://researchbox.org/8763) | Prior EN→TL study; P3 is reverse and **post-P2**; not confirmation |
| Future multi-seed / task / SFT work | new filings | new boxes | Not this confirmatory package |

---

## 10. What you should never do with these files

1. Describe P3 as an outcome-independent mirror or confirmation of P2.  
2. Treat in-loop training BPB as primary.  
3. Call B3 mitigation or replace B2-vs-B1 with B3-vs-B1 as the primary test.  
4. Reuse P1.1 `1.164768` or P2 Gate V numbers as P3 B2 tests.  
5. Test B1/B3 or add a second confirmatory test touch.  
6. Load P1.1/P2 weights as the P3 parent.  
7. Rank arms by absolute delta or declare a deployable “winner.”  
8. Publish raw holdout text, passcodes, or SSH material.  
9. Quietly treat the Gate S partial attempt as the official B2 run.  
10. Run more confirmatory val/test after Gate X and fold it into the primary claim.

---

## 11. Contact / roles

One-person lab execution with automated gate scripts and hash receipts. Scholarly contact appears on the ResearchBox author fields (De La Salle – College of Saint Benilde). For replication questions, use GitHub issues on `pageman/nanochat-filipino` and cite run ID `p3-20260819T192700Z-92d63d4`.

---

## 12. One-sentence takeaway

**P3 is a post-P2, preregistered, one-seed TL→EN continual-pretraining study whose sealed validation showed the filed Tagalog-cost and English-gain patterns both observed; this box documents that study alone—not P1.1, not P2, not raw tests, and not weights—and must be cited with the post-P2 disclosure intact.**

Thank you for reading carefully before citing or reanalyzing.

— End of Dear Reader message for ResearchBox #8834 (P3) —
