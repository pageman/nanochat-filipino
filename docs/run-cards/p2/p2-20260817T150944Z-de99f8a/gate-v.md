# P2 Gate V — A2-only test **pass**

- Date (UTC): 2026-08-19T07:47:24Z English → 2026-08-19T07:49:00Z Tagalog holdout
- **Status: pass.** One authorized touch, two component evaluations. A1/A3 not tested.
- A2 SHA still `2b01acf8…76026` (matches Gate U).
- P2 ledger: `docs/run-cards/p2/test_access_log.json` (`authorized_touches=1`). P1.1 ledger untouched.
- These numbers are **secondary treatment outcomes**. They do **not** alter sealed \(C_{EN}\)/\(G_{TL}\).

| Component | Role | `test_bpb` |
|---|---|---:|
| English | WT103-raw official test | **1.392015** |
| Tagalog | P1.1 `test.jsonl` as legacy external holdout (P2 English BPE) | **1.160154** |

Do **not** reuse or equate P1.1 `test_bpb=1.164768` (native Tagalog BPE).

## P3

See `p3-post-unblinding.md`. A P3 filed after Gate U was viewed is a post-P2 follow-up, not an outcome-independent mirror.

## Next

Gate W (deposit/paper) is laptop-side. Idle A40 should be stopped; volume may still incur storage cost.
