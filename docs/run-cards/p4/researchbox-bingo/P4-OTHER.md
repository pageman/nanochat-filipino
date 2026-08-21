# P4 Other (ResearchBox #8869)

**Column:** Other  
**Section:** P4 Confirmatory Close-out (2026-08-21)  
**Role:** Gate receipts, released seals, unblinding event, close-out ledgers. Not primary Data tables and not protected tests.

## Files in this packet

| File | Role |
|---|---|
| `P4-OTHER.md` | This cover |
| `00-BINGO-PLACEMENT.md` | How this box was meant to be filed |
| `gate-*.json` | Gates 0 / A–I / P0-T / Q–X receipts (no HOST SSH cards) |
| `released/*.json` | Gate X simultaneous scalar release |
| `P4_UNBLINDING_EVENT.json` | Formal unblinding |
| `p4_closeout_manifest.json` + `SHA256SUMS` | Local archive |
| `p4_test_access_log.json` | Policy A: one C3-only event, two components |
| `p4_gate_ledger.json` / mix / budget manifests | Frozen identity |
| Close-out checklists / six-layer audit | Execution-control copies |

JSON belongs in **Other**, not Data. ResearchBox may auto-move `.md`/`.txt` here; leave them.

## Test-access final state

- Authorized P4 test touches: **1** (Gate V only)
- Component reads: English WT103-raw test; P1.1 legacy Tagalog holdout
- C1/C2: never tested
- Future P4 test reads: prohibited
- Raw test text: **not** in this box

## Future studies (not this box)

P1.1 remains #8735 / #306780. P2 remains #8763 / #306935. P3 remains #8834 / #307342. Byte-balanced mix is **P6-B**. Multi-seed is **P5**. None of those reopen P4’s sealed \(R_{\mathrm{TL}}\)/\(A_{\mathrm{EN}}\).
