# Gate I handoff — P3 #307342

**Status:** **PASS** on Runpod A40 pod `bef5h2lzy6f3mp`.

| Depth | health | step | reload_ok | finite | forbidden_parent |
|---|---|---|---|---|---|
| TL0 d8 | pass | 294 | true | true | false |
| TL0 d20 | pass | 294 | true | true | false |

Both arms: `N_TL0=294`, warmup 14, Tagalog-only `p3-tl39-active`, eval/sample/core-metric off. Metrics in lockbox.

Receipts: `gate-i-tl0.json`, `gate-i-tl0-d8.json`, `gate-i-tl0-d20.json`  
Preflight: `gate-i-preflight.json`  
Host card: `HOST-bef5h2lzy6f3mp.md`  
Lockboxed logs: `data/cache/p3-…/lockbox/gate-i-tl0-d{8,20}-full.log` (gitignored)

Checkpoint SHA256 (safe):
- d8: `feaf7017cd55fab48a8acf9087b9f444b015167c7725c0d695278c20dbf462e2` (335570367 bytes)
- d20: `ae621be2c90a3d295f8d21b0e53cb9d4b717803f5d5337fa68f3c3f84d57193c` (2663446486 bytes)

**Next:** Gate **P0-T** (Tagalog parent eligibility — emit PASS/BLOCKED only). Rotate lockbox passphrase before real eval if not done. Do not start English train or B1/B2/B3 until P0-T authorizes.
