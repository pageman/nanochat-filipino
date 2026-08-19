# P2 Gate Q — A0 freeze

- Date (UTC): 2026-08-18T13:11:44Z (copies) → 2026-08-18T15:20:29Z (Tagalog d20 eval)
- **Status: pass.** `immutable: true`. Additional train tokens: **0**.
- Confirmatory parent for A1/A2/A3: **EN0 d20** only. d8 is provenance companion.

## Q.1 Frozen copies

Hashes match Gate I.

| Arm | Frozen path | SHA-256 |
|---|---|---|
| d8 | `data/cache/p2-20260817T150944Z-de99f8a/a0/frozen/p2-en0-d8/model_005415.pt` | `5e1db47f0609995e2309a2c04ede4cd330aa0f2d113e07d6498790d5ca707a8c` |
| d20 | `data/cache/p2-20260817T150944Z-de99f8a/a0/frozen/p2-en0-d20/model_005415.pt` | `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d` |

## Q.2 Dual `val_bpb_full`

English copied from P0-E (checksum `3fe37fe9…`). Tagalog scored once on frozen weights, P2 English BPE, P1.1 val shard `shard_00002.parquet`.

| Arm | English `val_bpb_full` | Tagalog `val_bpb_full` (English BPE) |
|---|---|---|
| A0 d8 | **0.983292** (P0, CUDA) | **4.082488** (Mac CPU) |
| A0 d20 | **1.389990** (P0, CUDA) | **4.917650** (pod CUDA) |

Packed UTF-8 bytes under English BPE: **5,205,755**. P1.1 Tagalog-BPE packed-byte invariant is 5,868,797; that number is **not** required here because A0 uses the English tokenizer.

A late Mac CPU rerun (2026-08-18T15:57:42Z) scored d20 Tagalog **4.921200** and briefly overwrote the official JSON. Official A0 remains the CUDA number **4.917650** (file SHA restored to `409e19b1…`). CPU–CUDA gap **0.003550** is below 0.01. CPU file kept as `p2-en0-d20_a0_tagalog_val.cpu-diagnostic.json` only.

`test_read_count = 0`. `started_tagalog_continuation = false`.

## Still banned

- Optimizer steps on A0 copies
- Loading P1.1 `model_000294.pt` as start weights
- Reading English or Tagalog test
- Ranking d8 vs d20

## Next

**Gate R — A1 extra English** at d20, `N=294`, fresh Adam, LR peak = 0.3×EN0, `NANOCHAT_DATA_DIR_EN`. Snapshot A1 hashes before A2.
