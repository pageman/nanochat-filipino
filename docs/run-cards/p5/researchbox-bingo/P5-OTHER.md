# P5 Other (ResearchBox)

**Column:** Other  
**Section:** P5 Confirmatory Close-out (2026-08-24)  
**Role:** Gate receipts, released seals, unblinding event, close-out ledgers.

## Files in this packet

| File | Role |
|---|---|
| `P5-OTHER.md` | This cover |
| `00-BINGO-PLACEMENT.md` | Filing map |
| `gate-*.json` | Shared gates 0 / A–H / X |
| `seed-{1,2,3}/*.json` | Per-seed I–V receipts |
| `released/seed-{1,2,3}/*.json` | Gate X simultaneous scalar release |
| `P5_UNBLINDING_EVENT.json` | Formal panel unblinding |
| `p5_closeout_manifest.json` + `SHA256SUMS` | Local archive |
| Manifests + audit copies | Frozen identity |

JSON belongs in **Other**, not Data.

## Test-access final state

- One C3-only test event per eligible seed (3 total)
- C1/C2: never tested on holdout
- Raw test text: **not** in this box
