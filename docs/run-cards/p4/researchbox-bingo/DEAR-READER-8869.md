# Dear Reader — ResearchBox #8869 (P4 only)

**Paste this into the ResearchBox “Dear Reader” field for box [#8869](https://researchbox.org/8869).**  
Not for P1.1 (#8735). Not for P2 (#8763). Not for P3 (#8834). Not included in download zips if you prefer online display only. Do **not** paste the box passcode here or into git.

---

Dear Reader,

Thank you for opening **ResearchBox #8869**, the deposit box for **NANOCHAT-FILIPINO P4** (“token-share mix after a fresh Tagalog parent”).

This note exists because (1) P4 is easy to confuse with P1.1, P2, and especially P3, (2) ResearchBox’s bingo columns are awkward for a computational LM study, (3) several absences are intentional, (4) P4 was **designed after P3 was unblinded** and must never be sold as an independent confirmation of P3 or as “P3 B3 fixed,” and (5) **C3 is not P3 B3**. Please read this before citing any CSV cell or JSON field as “the P4 result.”

---

## 1. What this box is (and is not)

### 1.1 This box is

- The **results-provenance and reproducibility metadata deposit** for one preregistered computational study:
  - **AsPredicted #307591** — https://aspredicted.org/if84km.pdf  
  - PDF SHA-256: `463b29fcff8d7c8099790325fa19d6bcf9ee29f64424c373a380566a6fe9011c`
- A **one-seed**, fixed-parent, fixed-budget **token-share mixture trade-off** experiment on **nanochat**, pinned commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`.
- Documentation for run ID **`p4-20260821T060032Z-92d63d4`**, Gates **0 / A–I / P0-T / Q–W** complete (`gate_x_unblinded` / `gate_w_pass`).
- A place to find **tables, hashes, scripts, protocol, sealed validation/test JSON, and paper** consistent with the filing.
- Linked results-provenance on AsCollected **#2471** (`NANOCHAT-FILIPINO-P4`). Gate 0 also recorded #2455 v1 at https://ascollected.org/DJ6_FL3.

### 1.2 This box is not

- **Not** ResearchBox **#8735** (P1.1, AsPredicted **#306780**).
- **Not** ResearchBox **#8763** (P2, AsPredicted **#306935**).
- **Not** ResearchBox **#8834** (P3, AsPredicted **#307342** — reverse-direction study with a 50/50-*document* B3 arm).
- **Not** a human-subjects study. No participants, Prolific IDs, surveys, or consent forms.
- **Not** a redistribution of raw held-out `test.jsonl` / WikiText-103 test article text.
- **Not** where model **`.pt` weights** live (Hub, if ever, must be C0+C1+C2+C3 together; currently **deferred**).
- **Not** an amendment to P1.1, P2, or P3. P4 does **not** rewrite #306780, #306935, #307342, or prior boxes/Hubs.
- **Not** “P3 B3 fixed.” C3 is a **new** token-share mixture.

If you arrived expecting P3 B3 document-mix numbers, switch boxes.

---

## 2. Critical disclosure (post-P3 timing)

P4 was **designed after P3 Gate X unblinding on 20 August 2026**. Operators may know P3 outcomes. P3 magnitudes were **not** P4 calibration targets.

What did **not** exist at P4 filing: P4 parent, children, P4 `val_bpb_full`, or P4 test BPB. The C3 identity was frozen **before** any P4 confirmatory BPB.

Required public grammar:

- Say **post-P3 prospectively preregistered token-share trade-off**.
- Do **not** say independently chosen without P3 knowledge.
- Do **not** say P4 confirms P3.
- Report the filed four-way conclusion (both / only-\(R\) / only-\(A\) / neither); one seed; no CI/p-value/population claim.

---

## 3. How the bingo table is organized (nonintuitive layout)

| Column | What we put there | What we deliberately did *not* |
|---|---|---|
| **Preregistration** | AsPredicted **#307591** (imported chip) | A second PDF unless import failed |
| **Materials** | Protocol, sanitized LOCK, study README, paper, Hub deferral stub | Raw corpora; weights; HOST SSH cards; passcode |
| **Data** | Small **CSV tables only**, uploaded **one file at a time** | Multi-file Data zips; `.json` seals; prose `.md` as Data |
| **Code** | `Code.zip` with `scripts_p4/*.py` and `*.sh` only | CSV inventories (those go in Data); secrets; P1/P2/P3 env; `.pt` |
| **Other** | Gate receipts, `released/*.json`, unblinding event, closeout | The sole confirmatory “Data” chip |

Suggested sections: keep the AsPredicted chip on a **Preregistration** row; put Materials/Data/Code/Other under **P4 Confirmatory Close-out (2026-08-21)**.

### 3.1 Why Data looks “too small”

Confirmatory objects of record are **JSON seals + hashes + scripts**. ResearchBox prefers tidy tables for Data, so:

1. Point estimates and contrasts appear in CSV under Data.  
2. Machine-readable seals live under **Other** (and locally under `released/`).  
3. Public training corpora are obtained elsewhere (HF / frozen P1.1 splits); they are not re-uploaded as raw text Data.

### 3.2 Hex strings are file hashes, not people

64-character hex columns (often prefixed `sha2-256:`) are **SHA-256 of files**. ResearchBox may flag them as Prolific IDs. **False positive.** P4 has no human participants.

---

## 4. Study design in one paragraph

P4 starts from a **fresh Tagalog parent** (TL0; new weights; frozen P1.1 WikiText-TL-39 train docs; **carry-forward P3 tokenizer**, both artifacts). After **P0-T** PASS at d8 and d20, freeze d20 as **C0**, then compare three **equal-budget** continuations from that **immutable common parent**:

| Arm | Treatment | Role |
|---|---|---|
| **C1** | Extra Tagalog | Active control (source-language retention) |
| **C2** | Pure English (WikiText-103-raw) | Comparator |
| **C3** | Pre-frozen **token-share** mix at \(q_{\mathrm{TL}}=0.50\) source-content tokens | Registered intervention; **not** P3 B3; **not** byte-balanced |

Primary DVs: full-validation **`val_bpb_full`** (locked `evaluate_bpb.py`), **not** in-loop `meta.val_bpb`.

Registered co-primary contrasts (\(\delta=0.01\); equality at \(-\delta\) counts):

- \(R_{\mathrm{TL}}=\mathrm{TL}(C3)-\mathrm{TL}(C2)\) — predicted \(\le -0.01\)
- \(A_{\mathrm{EN}}=\mathrm{EN}(C3)-\mathrm{EN}(C1)\) — predicted \(\le -0.01\)

One seed. Point estimates only. C0 English is descriptive and excluded from the contrasts. Tests are C3-only, secondary, and do not create a test-set \(R_{\mathrm{TL}}\)/\(A_{\mathrm{EN}}\).

Budget (filed/frozen): \(N=294\), \(B=65536\), \(T=2048\), \(D_{\mathrm{phase2}}=19{,}267{,}584\); C3 quotas \(9{,}633{,}792\) / \(9{,}633{,}792\); fresh optimizer (`load_optimizer=False`); warmup 14.

---

## 5. What the sealed numbers say (narrow claims)

Gate X released the precommitted package. From the validation seal (primary):

| Contrast | Approximate sealed value | Filed rule | Call |
|---|---|---|---|
| \(R_{\mathrm{TL}}\) | **−1.316637** | \(\le -0.01\) | **Observed** |
| \(A_{\mathrm{EN}}\) | **−1.375277** | \(\le -0.01\) | **Observed** |

Conclusion category: **both**. One authorized C3-only secondary test event is in the Data CSV and Other JSON; C1 and C2 were not tested.

Always append: one seed; no CI/p-value/population claim; C3 is not P3 B3; P4 does not amend #307342.

Permitted extra sentence because both criteria were met: “A measured reduction in the P3-style relative Tagalog retention cost within this frozen P4 apparatus, not a general mitigation of catastrophic forgetting.”

---

## 6. Intentional absences

- No raw `test.jsonl`.
- No `.pt` weights in this box.
- No ResearchBox passcode in any uploaded file.
- No C1/C2 test rows.
- No byte-balanced C4 (that would be a new filing).

---

## 7. Contact

One-person lab execution with automated gate scripts and hash receipts. Scholarly contact appears on the ResearchBox author fields (De La Salle – College of Saint Benilde). For replication questions, use GitHub issues on `pageman/nanochat-filipino` and cite run ID `p4-20260821T060032Z-92d63d4`.

— End of Dear Reader message for ResearchBox #8869 (P4) —
