# Gate L — reproducibility checklist

- Date (UTC): 2026-08-16
- Operator: Paul Pajo
- RUN_ID: `p1-20260816T025911Z-0067a57`
- AsPredicted: #306780

- [x] nanochat commit recorded (`92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`); working tree has uncommitted study artifacts (not claimed clean)
- [x] `NANOCHAT_BASE_DIR` isolated; no ClimbMix; `python -m nanochat.dataset` not run
- [x] Parquet SHA-256 recorded (`706d706496e3a085cf4506f97aa8b03faa20d4773d69453eaab4e3ca8f33caf9`)
- [x] S3 zip not used
- [x] Document reconstruction count recorded (120,971 articles; 53,718 unique texts)
- [x] Detokenization off for the canonical package
- [x] Hash split is lexicographic `sha256(utf-8)`; no shuffle seed; intersections empty
- [x] Test jsonl write-protected on the Mac; absent from the active train dir on the I host
- [x] ≥ 3 shards; last = val; test outside train dir
- [x] Tokenizer train-only
- [x] `token_bytes.pt` present
- [x] Depths chosen by the registered grid {8,12,16,20}, not speedrun d24
- [x] `--core-metric-every=-1`
- [x] `--eval-tokens=262144` ≤ half of `T_val`; final DV is `val_bpb_full`
- [x] `--num-iterations=294` matches the frozen budget
- [x] Random-init and byte-unigram baselines
- [x] `val_bpb_full` and one `test_bpb`
- [x] Run cards have execution records
- [x] Attribution block in the model card
- [x] No downstream labels in pretraining
