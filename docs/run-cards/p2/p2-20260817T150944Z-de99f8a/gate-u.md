# P2 Gate U — validation seal **pass** (val only; no test)

- Date (UTC): 2026-08-19T07:17:00Z (CUDA on `8ik4ix7j8iju9u`)
- Evaluator: `scripts/p2/gate_u_seal.py` → `evaluate_bpb.py` packing / official `evaluate_bpb` components
- **Status: pass.** Full-split `val_bpb_full`, T=2048, BOS-bestfit, device batch 8.
- Test access: **0** (`test_read_events_p2_english=0`, `test_read_events_p2_tagalog=0`).
- A0 English copied from P0-E (not recomputed). A0 Tagalog copied from Gate Q CUDA (not recomputed).
- Packed bytes match priors: English 624360; Tagalog 5205755.
- Does not amend #306780 or #306935. One-seed point estimates. 0.01 is a practical cutoff, not a ranking license.

## d20 confirmatory table

| Arm | English `val_bpb_full` | Tagalog `val_bpb_full` |
|---|---|---|
| Untrained | 3.246978 (P0-E) | — |
| A0 | 1.389990 (P0-E) | 4.917650 (Gate Q CUDA) |
| A1 | 1.459675 | 5.054664 |
| A2 | 1.385684 | 1.171616 |
| A3 | 1.279433 | 1.528858 |
| P1.1 d20 (descriptive, native tok) | n/a | 1.172248 (different tokenizer) |

## Registered contrasts

| Contrast | Formula | Value | \|Δ\| ≥ 0.01 | Filed prediction |
|---|---|---|---|---|
| \(C_{\mathrm{en}}\) | EN(A2) − EN(A1) | **−0.073991** | yes | ≥ 0.01 (not met; opposite sign) |
| \(G_{\mathrm{tl}}\) | TL(A2) − TL(A1) | **−3.883048** | yes | ≤ −0.01 (met) |
| \(C_{\mathrm{en}}\)(A3) | EN(A3) − EN(A1) | −0.180242 | yes | trade-off arm; **not mitigation** |
| \(G_{\mathrm{tl}}\)(A3) | TL(A3) − TL(A1) | −3.525806 | yes | trade-off arm; **not mitigation** |
| A0 − A2 Tagalog | TL(A0) − TL(A2) | 3.746034 | yes | **descriptive only** (AsPredicted Q2) |

Do not treat A2 Tagalog 1.171616 vs P1.1 1.172248 as a confirmatory match (cross-tokenizer). Do not rank gaps below 0.01. Do not read test.

## Next

**Stop and request authorization for Gate V** (A2-only: one English WT103-raw test + one P1.1 Tagalog `test.jsonl` under P2 English BPE). A1 is not tested. Do not reuse P1.1 `test_bpb=1.164768`.
