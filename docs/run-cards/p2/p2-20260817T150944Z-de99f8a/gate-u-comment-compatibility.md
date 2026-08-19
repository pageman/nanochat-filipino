# P2 Gate U/V — comment compatibility addendum

- Date (UTC): 2026-08-19T07:35:00Z
- Source: informal Gate V readiness comment (not an AsPredicted amendment)
- **Does not amend #306780 or #306935.**

Gate U is treated as a protocol-clean val seal. The conclusion stays narrow: **the registered English-cost pattern was not observed in this one-seed apparatus, whereas the registered Tagalog-gain pattern was observed.**

## Sealed interpretation (primary = Gate U val only)

| Registered result | Sealed value | Protocol-safe reading |
|---|---:|---|
| \(C_{EN}=\) EN(A2)−EN(A1) | −0.073991 | Filed prediction ≥ 0.01 **not met**. Opposite sign; \|Δ\| ≥ 0.01 so it is material, not a below-cutoff skip. Does **not** establish a general “Tagalog improves English” claim beyond this one-seed, fixed-data, fixed-budget apparatus. |
| \(G_{TL}=\) TL(A2)−TL(A1) | −3.883048 | Filed prediction ≤ −0.01 **met**. |
| A3 vs A1, English | −0.180242 | Predeclared mix-arm English trade-off. |
| A3 vs A1, Tagalog | −3.525806 | Predeclared mix-arm Tagalog trade-off. |

A3 vs A2 (English −0.106251, Tagalog +0.357242) is informative. It does **not** turn A3 into mitigation: the mix is 50/50 **documents**, not token-equated, and no joint mitigation criterion was preregistered.

## What was factored in (operational only)

| Comment | P2 action |
|---|---|
| Keep conclusion narrow | This addendum; do not generalize beyond the apparatus |
| A3 is trade-off, not mitigation | Unchanged from Gate U seal note |
| Gate V = A2 d20 only; two secondary test outcomes | Pre-test receipt + A2-only evaluator; A1/A3 never tested |
| Tests cannot alter sealed \(C_{EN}\)/\(G_{TL}\) | Evaluator does not recompute those contrasts |
| P1.1 `test.jsonl` is a legacy external holdout | Logged as such; do not reuse P1.1 `test_bpb=1.164768` |
| One authorized touch, two component reads | P2 ledger (`docs/run-cards/p2/test_access_log.json`), not P1.1 `manifests/test_access_log.json` |
| Pre-test receipt before first evaluation | `gate-v-pretest-receipt.json` |
| Technical failure → dated recovery, no silent rerun | Required in Gate V launch record |
| After V, freeze record; stop idle A40 | Next after authorized V |
| P3 after viewing Gate U | **Post-P2 follow-up** unless its design was frozen before these results were seen. Not an outcome-independent mirror. |

## What was not added

No new primary DV, no test-set \(C_{EN}\)/\(G_{TL}\), no A1/A3 test, no second test touch, no P2.1, no #306935 amendment.
