# P2 Gate P0-E — provenance pass

- Date (UTC): 2026-08-18T12:57:57Z → 2026-08-18T12:58:12Z
- Pod: `8ik4ix7j8iju9u`, NVIDIA A40 48 GB, EU-SE-1, $0.44/hr (stopped after eval; status `EXITED`)
- Evaluator: `scripts/p2/evaluate_bpb.py --phase val_baselines`
- Step: 5415 · T=2048 · BOS-bestfit · device-batch-size 8
- **P0-E PASS for both d8 and d20. Do not start Tagalog until Gate Q.**

Filed criterion (AsPredicted #306935): EN0 English `val_bpb_full` is ≥ 0.01 below **both** an untrained same-depth model **and** a train-fitted add-one UTF-8 byte unigram on the same WT103 val. If either floor fails, do not call the parent English-pretrained.

## Results

| Model | `val_bpb_full` | Untrained | Gap vs untrained | Byte unigram | Pass |
|---|---|---|---|---|---|
| EN0 d8 | **0.983292** | 3.246994 | 2.263702 | 4.582801 | YES |
| EN0 d20 | **1.389990** | 3.246978 | 1.856988 | 4.582801 | YES |

Byte unigram is Laplace add-one on hashed train parquet UTF-8, scored on hashed val parquet (`source: parquet_shards`; JSONL was not on the pod). Unigram is a floor, not a ranking statistic.

In-loop val from Gate I is **not** `val_bpb_full`. These full-split numbers are the confirmatory English parent scores.

Do **not** rank d8 vs d20 from this table. A1/A2/A3 confirmatory continuation is d20 only; d8 continuation is exploratory.

## Checkpoints

| Arm | Path | SHA-256 |
|---|---|---|
| d8 | `data/cache/p2-20260817T150944Z-de99f8a/base_checkpoints/p2-en0-d8/model_005415.pt` | `5e1db47f0609995e2309a2c04ede4cd330aa0f2d113e07d6498790d5ca707a8c` |
| d20 | `data/cache/p2-20260817T150944Z-de99f8a/base_checkpoints/p2-en0-d20/model_005415.pt` | `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d` |

d8 was copied onto this pod from the Mac (trained on `xk8orhscuk2jsu`) before eval; SHA matched LOCK after rsync.

## Artifacts

- Summary: `docs/run-cards/p2/p2-20260817T150944Z-de99f8a/gate_p0_val_baselines.json` (SHA `3fe37fe9…`)
- Per-depth: `p2-en0-d8_p0e_val.json`, `p2-en0-d20_p0e_val.json`
- Unigram: `byte_unigram_english_val.json`
- Log: `p2-gate-p0e.log`

`test_read_count = 0`. `started_tagalog = false`.

## Still banned

- Starting Tagalog continuation before Gate Q (A0 freeze)
- Reading English or Tagalog test set
- Loading P1.1 `model_000294.pt` as an English parent
- Treating in-loop 124438-token val as `val_bpb_full`

## Next step

**Gate Q — A0 freeze:** copy EN0 d20 (and d8) to `a0/frozen/` with SHA-256, stamp `immutable: true`. Then A1/A2/A3 at d20 only (`N=294`). Empty HF repo `pageman/nanochat-filipino-p2-en-then-tl` (protocol I.1.3) still open.
