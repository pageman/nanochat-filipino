# Gate S launch — A2 Tagalog continuation (authorization-readiness)

Does **not** amend #306780 or #306935. Integrity preflight only; no new science.

User authorization in the same message as the attached Gate S review: **do Gate S**.

## Preflight table (local + host)

| Check | Result |
|---|---|
| A1 archived `model_000294.pt` SHA | `e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d` (Mac = host) |
| A1 not A2 parent | wrapper refuses A1 `init-from`; `--allowed-model-tag p2-a2-tagalog-d20` refuses A1 tag |
| A1 dir read-only after hash | local + host chmod 555/444; SHA unchanged |
| A0 parent re-hash | `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d` Mac = host |
| A0 still frozen | wrapper writes only `base_checkpoints/<tag>/` |
| Wrapper SHA (same as A1) | `7e6719544237f54fc75fc3770f587ba3ed929011b9f68627f398f3ed87b6552f` |
| Tagalog train-visible dir | `data/processed/p2-tl39-readonly` only `shard_00000/00001/00002.parquet` |
| Train shards SHA (Gate E) | `aaf81d95…` / `c57c11a2…` |
| Last shard val in-loop only | `shard_00002.parquet` `13409b3c…` (not train-selected) |
| Test / English / A3 / mix names | absent from train-visible listing |
| Host restore | host initially had **only** val shard; frozen train shards copied from Mac, re-hashed, chmod 444 |
| Shared child invariants | d20, T=2048, SSSL, device-batch 8, B=65536, N=294, warmup 14, 0.3× EN0 LRs, fresh optimizer |
| `--core-metric-every=-1` `--save-every=-1` | same as A1; pin still saves `model_000294.pt` at last_step |
| Output tag | `p2-a2-tagalog-d20`; dir absent before launch |
| Expected terminal | `base_checkpoints/p2-a2-tagalog-d20/model_000294.pt` |
| GPU / no trainer / test access | A40 idle; no trainer; P2 test_read_count = 0 |
| `--validate-only` A2 | pass, no train |
| Not added | no Tagalog floor, no d8 branch, no new mixture, no C_EN/G_TL, no test read |

In-loop A2 val is Tagalog last-shard **diagnostic**. Confirmatory English/Tagalog `val_bpb_full` is Gate U. Do not put English val into the A2 train-visible directory.
