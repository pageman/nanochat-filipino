# Dear Reader — P6-M (schedule topology)

**Paste this into the ResearchBox “Dear Reader” field for box [#8918](https://researchbox.org/8918).** Not for P1.1 (#8735), P2 (#8763), P3 (#8834), P4 (#8869), or P5 (#8904). Do **not** paste the box passcode here or into git.

---

Dear Reader,

Thank you for opening **ResearchBox #8918**, the deposit box for **NANOCHAT-FILIPINO P6-M** (“Block Order under a Fixed English–Tagalog Token Budget: A One-Seed Schedule-Topology Study with nanochat”).

Results provenance on AsCollected: **not yet documented** in this box — please create/link an AsCollected record before any Make Public step.

This note exists because (1) P6-M is easy to confuse with P4/P5, (2) ResearchBox’s bingo columns are awkward for a computational LM study, (3) several absences are intentional, and (4) **P6-M does not confirm P4 or P5** — it reports filed schedule-topology contrasts on one seed under a fixed token budget.

---

## What this box is

- **AsPredicted #307969** — https://aspredicted.org/bk6m9d.pdf  
- A **one-seed** (seed 4) comparison of **M-fine / M-coarse / M-blocked / M-rand** with locked per-language quotas.  
- Run ID **`p6-20260824T155226Z-769f807a`**, Gates **0 / A–W / X** complete locally.  
- **Primary result:** six ΔTL/ΔEN classifications versus M-fine at δ=0.01 (no mean, CI, or p-value).

## What this box is not

- **Not** ResearchBox #8904 (P5 recurrence panel) or #8869 (P4 token-share trade-off).  
- **Not** a human-subjects study.  
- **Not** raw held-out `test.jsonl` text.  
- **Not** model `.pt` weights (Hub deferred: C0+C1+C2+four topologies + tokenizer together).  
- **Not** an amendment to P1.1–P5 registrations.

## Bingo column map

| Column | Contents |
|---|---|
| **Preregistration** | AsPredicted #307969 only |
| **Materials** | Protocol, LOCK (sanitized), paper |
| **Data** | CSV tables (primary contrasts + crosstab + hashes); **one file per chip** |
| **Code** | `scripts_p6/*.py` and `*.sh` only |
| **Other** | JSON gate receipts and released seals |

## How to read the primary claim

Upload order for Data: primary contrasts → arm crosstab → contextual → facts → codebook → hashes → code crosswalk (+ 3-column codebook). Spot-check: M-rand within δ on both languages; M-blocked worse on both; M-coarse better on Tagalog and worse on English.

Thank you,  
Paul Pajo  
De La Salle – College of Saint Benilde  
paulamerigo.pajojr@benilde.edu.ph
