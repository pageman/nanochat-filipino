# ResearchBox 8763 — bingo table placement

**Box:** https://researchbox.org/8763  
**Study:** P2 — English retention after Tagalog continuation (nanochat)  
**AsPredicted:** #306935  
**Does not amend:** #306780 / ResearchBox 8735 / P1.1 Hub

This deposit is **run documentation and reproducibility metadata**. It does **not** contain raw protected holdout text (`test.jsonl` / WikiText-103 test articles), ResearchBox passcodes, SSH keys, API tokens, or model `.pt` weights.

Local upload bundle (gitignored): `transfer/p2-researchbox-8763-bingo/`

## If a previous Data file was auto-moved to Other

ResearchBox treats prose `.txt` as Other, and rejects a Data zip with more than one file. Leave those in Other. Upload the four **tables** below into Data, one file at a time.

## Preregistration (already on the page)

Drag the unassigned file **AsPredicted #306,935** into the **Preregistration** cell of section `P2`.  
Do not upload a second AsPredicted PDF unless ResearchBox failed to attach the import.

## Drag map

| Bingo column | Upload | What it is |
|---|---|---|
| **Materials** | `Materials.zip` | Protocol, current paper, model card, public summaries, data cards |
| **Data** | Four tables in `Data/`, each uploaded separately | Crosstab + long facts + codebook CSV + hashes |
| **Code** | `Code.zip` | P2 scripts and env files used for gates and evaluation |
| **Other** | `Other.zip` | Gate receipts A–W, JSON receipts zip, prose codebook `.txt` |

Suggested **Section** name: `P2`

### Data files (upload individually; all have header rows)

1. `p2_arm_language_crosstab.csv` — one row per arm; English/Tagalog val, A2 tests, exposure, A3 shares
2. `p2_facts_long.csv` — same facts as the TSV; `description` sits after `value`
3. `p2_codebook.csv` — variable definitions (this is the codebook table)
4. `p2_hashes.csv` — corpus/tokenizer/checkpoint file digests (`sha2-256:` prefix; not participant IDs)

ResearchBox may flag 64-character hex columns as Prolific IDs. Those cells are SHA-2-256 of **files**, not people. P2 has no human participants. If flagged on an old upload, certify the false positive or replace with this renamed version.

Do not classify `.md`, `.txt` prose, or `.json` as Data.

## After upload

1. Open `p2_arm_language_crosstab.csv` and check A2 `C_en_vs_A1` ≈ −0.073991 and `G_tl_vs_A1` ≈ −3.883048.
2. Confirm no file named `test.jsonl` appears in the inventory.
3. Record deposit version, UTC time, and uploader in the paper availability statement.
