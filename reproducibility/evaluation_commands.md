# Evaluation identity

Official confirmatory evaluator: [`scripts/p1/gate_j_full_bpb.py`](../scripts/p1/gate_j_full_bpb.py).

It wraps nanochat `evaluate_bpb` (mean token NLL / (ln 2 × UTF-8 bytes), special tokens excluded), one-pass BOS-bestfit, `T=2048`, device batch 8, final checkpoint `model_000294.pt` only.

Validation phase writes [results/full_validation.json](../results/full_validation.json) with `test_read_count=0`. Test phase is a later invocation on `D*` only and writes [results/selected_test_d20.json](../results/selected_test_d20.json).

Do not use `--eval-tokens=262144` card scores, or `val_bpb` inside Hub `meta_000294.json`, as `val_bpb_full`.

Never run `python -m nanochat.dataset`. Never pass `--target-param-data-ratio=-1`.
