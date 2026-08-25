# ResearchBox P6-M — bingo table placement

**Study:** P6-M — schedule topology under a fixed English–Tagalog token budget (one seed)  
**AsPredicted:** #307969 — https://aspredicted.org/bk6m9d.pdf  
**Box:** https://researchbox.org/8918 (CODE `RAOZFR`; FOR PEER REVIEW; not Make Public)  
**AsCollected:** not yet linked (Results Provenance currently NOT DOCUMENTED — create/link before Make Public)  
**Does not amend:** #306780 / #8735 / #306935 / #8763 / #307342 / #8834 / #307591 / #8869 / #307836 / #8904

This deposit is **documentation + sealed tables**. It does **not** contain raw `test.jsonl`, ResearchBox passcodes, SSH keys, API tokens, or model `.pt` weights. **Not a P5 recurrence-count study.** Keep the box **FOR PEER REVIEW**, passcode-protected, and anonymous.

Local files: `docs/run-cards/p6/researchbox-bingo/`  
Upload zips: `transfer/p6-researchbox-8918-bingo/` and `~/Downloads/p6-researchbox-8918-bingo/`

---

## Section layout

| Section row | What goes where |
|---|---|
| **Preregistration** | Keep **AsPredicted #307969** in the **Preregistration** column only. |
| **P6-M Confirmatory Close-out (2026-08-25)** | Put Materials, Data, Code, and Other in this section row. |

---

## Drag map

| Column | Upload | Contents |
|---|---|---|
| **Materials** | `Materials.zip` | Protocol, sanitized LOCK, paper, Dear Reader, Hub deferral stub. |
| **Data** | **Eight uploads, one at a time** — each file in `Data/*.zip` (single CSV inside) or bare `Data/*.csv` | Never a multi-file `Data.zip`. |
| **Code** | `Code.zip` (`.py` / `.sh` only) | `scripts_p6/` gate scripts. |
| **Other** | `Other.zip` | Gate receipts, released JSON, unblinding event, closeout, audits. |

### Data files (upload individually)

From `transfer/p6-researchbox-8918-bingo/Data/` — **one chip per file**:

1. `p6_primary_contrasts.zip` — six primary ΔTL/ΔEN classifications vs M-fine  
2. `p6_arm_language_crosstab.zip` — seed-4 arms × languages (+ M-fine test)  
3. `p6_contextual_contrasts.zip` — R_TL / A_EN for four mixed topologies  
4. `p6_facts_long.zip`  
5. `p6_codebook.zip` — variable definitions  
6. `p6_hashes.zip`  
7. `p6_code_crosswalk.zip` — script inventory (ResearchBox classifies as Data)  
8. `p6_code_crosswalk_3_columns.zip` — column codebook for the inventory  

**Spot-check:** M-rand within δ both; M-blocked worse both; M-coarse better TL / worse EN; one seed only.

### Hard exclusions

- Raw Tagalog/English **test** text  
- Model weights (Hub deferred; C0+C1+C2+M-fine+M-coarse+M-blocked+M-rand + tokenizer together)  
- Passcodes / API keys / SSH private material  
- P5 recurrence-count tables as primary  
- Writing onto P4/P5 Hub IDs  
