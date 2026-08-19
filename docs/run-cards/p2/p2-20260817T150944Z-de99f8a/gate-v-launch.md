# Gate V launch — A2-only test (pre-test receipt)

Does **not** amend #306780 or #306935. Integrity + interpretation only; **no test evaluation yet**.

Narrow Gate U reading (unchanged numbers): registered English-cost pattern **not observed**; registered Tagalog-gain pattern **observed**. Tests cannot alter those sealed contrasts. A3 remains a mix trade-off, not mitigation. P1.1 `test.jsonl` is a **legacy external holdout**, not a virgin P2 test. Do not reuse P1.1 `test_bpb=1.164768`.

## Pre-test receipt

| Pin | Value |
|---|---|
| A2 SHA (Mac = host = Gate U) | `2b01acf8…76026` |
| Tokenizer / token_bytes | `946a04ef…ace6` / `5ae2ea1d…2d42` |
| English test (WT103-raw) | `2bccabc0…434e` |
| Tagalog test (P1.1 holdout) | `3bd19345…3baf` |
| `evaluate_bpb.py` | `eebbcd99…8b94` (Mac = host) |
| `gate_v_test.py` | `6e1bb336…48f5` |
| P2 test_access_count | **0** |
| Test files on A40 | **absent** (copy only after authorization, then hash-verify) |

Evaluator command sees **only** A2 `p2-a2-tagalog-d20` and one named test file per invocation. A1/A3 tags are refused. `GATE_V_AUTHORIZED=1` is required. Unauthorized `--phase english` already refused.

## Sealed sequence (after authorization; once)

1. Copy the two hashed test files to the host (not into any train-visible dir). Re-hash.
2. `GATE_V_AUTHORIZED=1 python scripts/p2/gate_v_test.py --phase english`
3. Hash/archive that JSON immediately.
4. `GATE_V_AUTHORIZED=1 python scripts/p2/gate_v_test.py --phase tagalog`
5. Hash/archive that JSON immediately.
6. Write `gate-v-test.json`. Do not rerun. Do not test A1/A3. Do not recompute \(C_{EN}\)/\(G_{TL}\).
7. If a technical failure occurs before a valid output, keep the log and write a dated recovery record — no silent repeat.
8. Freeze/archive the P2 record. Stop the idle A40 unless another authorized task remains.

P2 ledger: `docs/run-cards/p2/test_access_log.json` (not P1.1 `manifests/test_access_log.json`).
