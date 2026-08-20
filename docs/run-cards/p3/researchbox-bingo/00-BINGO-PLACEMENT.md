# ResearchBox #8834 — bingo table placement (P3)

**Box:** https://researchbox.org/8834  
**Study:** P3 — TL retention after EN continuation (nanochat)  
**AsPredicted:** #307342  
**AsCollected:** https://ascollected.org/F36_C2C  
**Does not amend:** #306780 / #8735 / #306935 / #8763 / P1.1–P2 Hubs

This deposit is **documentation + sealed tables**. It does **not** contain raw `test.jsonl`, ResearchBox passcodes, SSH keys, API tokens, or model `.pt` weights.

Local Data CSVs (ready to upload): `docs/run-cards/p3/researchbox-bingo/`

---

## Section layout (matches your screenshot)

| Section row | What goes where |
|---|---|
| **Preregistration** | Keep **AsPredicted #307,342** in the **Preregistration** column only. Leave Materials/Data/Code/Other empty on this row. |
| **P3 Confirmatory Close-out (2026-08-20)** | Put **all** Materials, Data, Code, and Other uploads in **this** row. |

Do not add a second AsPredicted PDF unless the import chip is broken.

---

## Drag map

| Column | Upload | Contents |
|---|---|---|
| **Materials** | One `Materials.zip` (or loose PDFs/MD) | Protocol, LOCK (sanitized), study README, AsCollected note, Dear Reader source (optional duplicate of online field), paper when ready, public status / data cards. **No** HOST SSH cards. |
| **Data** | **Four CSVs, one at a time** (not one zip) | See files below. Header row required. |
| **Code** | Prefer single CSV `p3_code_crosswalk.csv` (41 rows: file ↔ gate ↔ purpose ↔ `sha2-256`), **or** `Code.zip` (scripts + that CSV). Optional: `Code-crosswalk-only.zip`. No `.env`/secrets. |
| **Other** | One `Other.zip` | Gate receipts 0/A–X JSON, `released/*.json`, `P3_UNBLINDING_EVENT.json`, `p3_closeout_manifest.json`, prose codebook `.txt`, filled compliance audits. JSON belongs here, **not** in Data. |

### Data files (upload individually)

From `docs/run-cards/p3/researchbox-bingo/`:

1. `p3_arm_language_crosstab.csv` — B0–B3 rows; vals; B2 tests; contrasts  
2. `p3_facts_long.csv` — key facts + descriptions  
3. `p3_codebook.csv` — variable definitions  
4. `p3_hashes.csv` — file digests with `sha2-256:` prefix (**not** participant IDs)

**Spot-check after upload:** `C_tl` ≈ **1.023484**; `G_en` ≈ **−1.697955**; both filed patterns **observed**; B3 `not_mitigation=true`.

### Materials checklist (suggested)

| File | Role |
|---|---|
| `PROTOCOL-p3-tl-then-en.md` | Locked protocol |
| `LOCK.json` or `LOCK.sanitized.json` | Study lock **without** passcode |
| `docs/p3/README.md` | Study index (update status to Gate X complete before upload) |
| `ASCOLLECTED-2440.md` | Provenance pointer |
| `AsPredicted-307342.pdf` | Optional local copy (chip already linked) |
| Paper PDF/tex | When compiled from frozen seal |
| Dear Reader text | Optional; primary Dear Reader is the online field |

### Code checklist

Zip `scripts/p3/` (gate scripts + `evaluate_bpb.py` + env). Exclude: `__pycache__`, `.pyc`, anything with tokens.

### Other checklist

Zip (no secrets):

- `docs/run-cards/p3/p3-20260819T192700Z-92d63d4/gate-*.json`
- `…/released/*.json`
- `P3_UNBLINDING_EVENT.json`, `gate-x-preflight.json`, `p3_closeout_manifest.json`
- `docs/run-cards/p3/test_access_log.json`
- Filled compliance audits (optional)

**Never include:** `HOST-*.md` with live SSH, `test.jsonl`, `.pt`, passcodes, AppleDouble junk.

---

## Hard exclusions

- Raw Tagalog/English **test** text  
- Model weights (Hub later, B0+B1+B2+B3 together if released)  
- Passcodes / API keys / SSH private material  
- P1.1 or P2 result files mixed into this box’s confirmatory story  

---

## After upload

1. Confirm AsPredicted chip sits under **Preregistration**.  
2. Confirm four Data CSVs sit under **P3 Confirmatory Close-out → Data**.  
3. Confirm inventory has **zero** `test.jsonl` / `.pt`.  
4. Paste Dear Reader (generate next if needed) into the online field.  
5. Record deposit time in the paper availability statement.
