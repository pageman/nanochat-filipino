# Machine-readable P2 results

**P2 only.** Does not amend AsPredicted #306780 / ResearchBox 8735 / Hub `p1-fixed-d20-3x`.

Primary DVs are full-split `val_bpb_full` in `gate-u-seal.json` (test_read_count=0 at seal). In-loop trainer BPB is not confirmatory.

| File | Role |
|---|---|
| `sealed_val_table.csv` | A0/A1/A2/A3 English and Tagalog val BPB |
| `gate-u-seal.json` | Sealed table, contrasts, packing |
| `evaluation/a{1,2,3}_{english,tagalog}_val.json` | Six underlying Gate U full-val eval objects |
| `gate-v-test.json` | A2-only secondary tests |
| `test_access_log.json` | One authorized touch; two component reads |
| `gate_p0_val_baselines.json`, `p2-en0-d8_p0e_val.json`, `p2-en0-d20_p0e_val.json` | P0-E floors |
| `gate-q-a0.json`, `p2-en0-d20_a0_tagalog_val.json` | A0 freeze; official CUDA A0 Tagalog val |
| `gate-r-a1.json`, `gate-s-a2.json`, `gate-t-a3.json` | Branch lineage and checkpoint hashes |
| `gate-e-shards.json`, `a3_realized_shares.json`, `exposure_by_arm.csv` | Mix and exposure |
| `registered-reporting-q3-q8.json` | Q3–Q8 reconstruction (no test read) |
| `gate-i-en0-d20.json` | EN0 d20 training receipt (parent before freeze) |
| `LOCK.sanitized.json` | Study lock without ResearchBox passcode |
| `meta/` | Matching nanochat `meta_*.json` for A0–A3 (in-loop `val_bpb` is **not** `val_bpb_full`) |

Do not commit `*.pt`, `test.jsonl`, HOST SSH cards, or passcodes. CPU diagnostic A0 Tagalog 4.921200 is **not** official (CUDA 4.917650 is).
