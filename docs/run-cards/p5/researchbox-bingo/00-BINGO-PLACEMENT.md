# ResearchBox P5 — bingo table placement

**Study:** P5 — closed three-seed panel of the frozen P4 token-share apparatus  
**AsPredicted:** #307836  
**Box:** https://researchbox.org/8904  
**AsCollected:** #2503 v1 — https://ascollected.org/HC8_G2F  
**Does not amend:** #306780 / #8735 / #306935 / #8763 / #307342 / #8834 / #307591 / #8869

This deposit is **documentation + sealed tables**. It does **not** contain raw `test.jsonl`, ResearchBox passcodes, SSH keys, API tokens, or model `.pt` weights. **C3 is not P3 B3.** Keep the box **FOR PEER REVIEW**, passcode-protected, and anonymous.

Local files: `docs/run-cards/p5/researchbox-bingo/`  
Upload zips: `transfer/p5-researchbox-bingo/` and `~/Downloads/p5-researchbox-bingo/`

---

## Section layout

| Section row | What goes where |
|---|---|
| **Preregistration** | Keep **AsPredicted #307,836** in the **Preregistration** column only. |
| **P5 Confirmatory Close-out (2026-08-24)** | Put Materials, Data, Code, and Other in this section row. |

---

## Drag map

| Column | Upload | Contents |
|---|---|---|
| **Materials** | `Materials.zip` | Protocol, sanitized LOCK, study README, paper, Dear Reader source, Hub deferral card. |
| **Data** | **Seven uploads, one at a time** — each file in `Data/*.zip` (single CSV inside) or bare `Data/*.csv` | Never a multi-file `Data.zip`. |
| **Code** | `Code.zip` (`.py` / `.sh` only) | `scripts_p5/` gate scripts. |
| **Other** | `Other.zip` | Gate receipts, `released/*.json`, unblinding event, closeout, audits. |

### Data files (upload individually)

From `transfer/p5-researchbox-bingo/Data/` — **one chip per file**:

1. `p5_panel_count_table.zip` (or `.csv`) — primary panel count  
2. `p5_arm_language_crosstab.zip` — 12 rows (3 seeds × 4 arms)  
3. `p5_facts_long.zip`  
4. `p5_codebook.zip` — variable definitions for table columns  
5. `p5_hashes.zip`  
6. `p5_code_crosswalk.zip` — script inventory (ResearchBox classifies as Data)  
7. `p5_code_crosswalk_3_columns.zip` — column codebook for the inventory  

**Spot-check:** `k_both=3`, `K_eligible=3`, all per-seed classes `both`.

### Hard exclusions

- Raw Tagalog/English **test** text  
- Model weights (Hub deferred; C0+C1+C2+C3 per seed together)  
- Passcodes / API keys / SSH private material  
- P4 seed 0 treated as a P5 confirmatory cell  
