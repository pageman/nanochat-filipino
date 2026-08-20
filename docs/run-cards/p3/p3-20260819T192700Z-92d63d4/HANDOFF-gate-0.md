# Gate 0 handoff — P3 #307342

**Host:** laptop. **GPU:** no. **No tok_train / smoke / TL0.**

| Item | Value |
|---|---|
| AsPredicted | [#307342](https://aspredicted.org/wd2pc8.pdf) |
| RUN_ID | `p3-20260819T192700Z-92d63d4` |
| Lockbox tests | **PASS** (dummy data only) |
| ResearchBox | [#8834](https://researchbox.org/8834) |

Env: `export NANOCHAT_FILIPINO_ROOT=...` then `source scripts/p3/env.sh`. Never `scripts/p1/env.sh` or `scripts/p2/env.sh`.

Rotate the dummy lockbox passphrase under gitignored `data/cache/$P3_RUN_ID/` before any real eval.

Next: **Gate A** (pin + sentinel). Then B–G on CPU.
