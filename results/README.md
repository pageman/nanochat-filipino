# Machine-readable P1.1 results

Primary dependent variable is **`val_bpb_full`**: official `evaluate_bpb` on the full packed validation split after the final checkpoint.

Checkpoint metadata `val_bpb` is **not** the primary result. Those values used `--eval-tokens=262144` during training.

| File | What it is |
|---|---|
| [full_validation.json](full_validation.json) | Sealed Gate J validation bundle. `test_read_count=0`. NLL, bytes, excluded specials, and `val_bpb_full` for d8/d12/d16/d20. Also stores `card_eval_val_bpb_262144` so the loop metric cannot be mistaken for the primary DV. |
| [untrained_baselines.json](untrained_baselines.json) | Same-depth untrained validation BPB (AsPredicted Q5). |
| [byte_unigram.json](byte_unigram.json) | Train-fitted UTF-8 byte unigram, Laplace add-1, raw validation bytes. |
| [selected_test_d20.json](selected_test_d20.json) | One test BPB on `D*=20` after selection. Aggregate components only. No raw `test.jsonl`. |

Do not rank depths from `card_eval_val_bpb_262144` or from `meta_000294.json` `val_bpb`.

## P2 (separate tree)

P2 seals are in [`p2/`](p2/). Do not mix those files with this P1.1 folder. P2 primary DVs are in `p2/gate-u-seal.json`.
