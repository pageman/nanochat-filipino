# ResearchBox #8869 — bingo table placement (P4)

**Box:** https://researchbox.org/8869  
**Study:** P4 — token-share mix after fresh TL parent (nanochat)  
**AsPredicted:** #307591  
**AsCollected:** #2471 (`NANOCHAT-FILIPINO-P4`); Gate-0 prior record #2455 v1 at https://ascollected.org/DJ6_FL3  
**Does not amend:** #306780 / #8735 / #306935 / #8763 / #307342 / #8834

This deposit is **documentation + sealed tables**. It does **not** contain raw `test.jsonl`, ResearchBox passcodes, SSH keys, API tokens, or model `.pt` weights. **C3 is not P3 B3.** Keep the box **FOR PEER REVIEW**, passcode-protected, and anonymous. Do **not** Make Public unless a later explicit operator instruction says so.

Local files: `docs/run-cards/p4/researchbox-bingo/`  
Upload zips (gitignored): `transfer/p4-researchbox-8869-bingo/` and `~/Downloads/p4-researchbox-8869-bingo/`

---

## Section layout

| Section row | What goes where |
|---|---|
| **`__new__` / Preregistration** | Keep **AsPredicted #307,591** in the **Preregistration** column only. Leave Materials/Data/Code/Other empty on that row. |
| **P4 Confirmatory Close-out (2026-08-21)** | Put **all** Materials, Data, Code, and Other uploads in **this** new section row. |

Do not add a second AsPredicted PDF unless the import chip is broken.

---

## Drag map

| Column | Upload | Contents |
|---|---|---|
| **Materials** | `Materials.zip` | Protocol package, sanitized LOCK, study README, paper, Dear Reader source, AsCollected note, Hub deferral card. **No** HOST SSH cards. |
| **Data** | **Six CSVs, one at a time** (not one zip) | See files below. Header row required. |
| **Code** | `Code.zip` (**`.py` / `.sh` only**) | `scripts_p4/` gate scripts. No CSV, no `.md`, no `.json`. |
| **Other** | `Other.zip` | Gate receipts, `released/*.json`, unblinding event, closeout, audits. JSON belongs here, **not** in Data. |

### Data files (upload individually)

From `docs/run-cards/p4/researchbox-bingo/`:

1. `p4_arm_language_crosstab.csv` — C0–C3 rows; vals; C3 tests; co-primary contrasts  
2. `p4_facts_long.csv` — key facts + descriptions  
3. `p4_codebook.csv` — variable definitions  
4. `p4_hashes.csv` — file digests with `sha2-256:` prefix (**not** participant IDs)  
5. `p4_code_crosswalk.csv` — script inventory (ResearchBox classifies this as **Data**, not Code)  
6. `p4_code_crosswalk_3_columns.csv` — codebook for the inventory columns

**Spot-check after upload:** `R_TL` ≈ **−1.316637**; `A_EN` ≈ **−1.375277**; both filed criteria **observed**; `c3_is_not_p3_b3=true`.

### Hard exclusions

- Raw Tagalog/English **test** text  
- Model weights (Hub later, C0+C1+C2+C3 together if released; currently **deferred**)  
- Passcodes / API keys / SSH private material  
- P1.1 / P2 / P3 result files mixed into this box’s confirmatory story  

---

## After upload

1. Confirm AsPredicted chip sits under **Preregistration**.  
2. Confirm four Data CSVs sit under **P4 Confirmatory Close-out → Data**.  
3. Confirm inventory has **zero** `test.jsonl` / `.pt`.  
4. Paste Dear Reader into the online field (not into a download zip if you prefer display-only).  
5. Leave **FOR PEER REVIEW**; do not Make Public.  
