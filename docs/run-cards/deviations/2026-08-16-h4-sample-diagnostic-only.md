# Record correction — Gate H H4 sample wording

- Date (UTC): 2026-08-16
- Operator: Paul Pajo
- Source: Gate I pre-launch checklist

## Correction

The presence of Tagalog function words in `p1-smoke-d4` samples is **diagnostic only**. It is not proof of corpus identity.

Binding H evidence remains: host preflight hashes, `NANOCHAT_DATA_DIR` ending in `wikitext-tl39/active`, active-shard inventory (`shard_00000`, `shard_00001`, val `shard_00002`), absent test payload, finite decreasing train loss, checkpoint, fresh-process finite smoke BPB, CORE off, CUDA A40.

This does not invalidate official H. Smoke BPB is not `val_bpb_full` and must not select a depth.
