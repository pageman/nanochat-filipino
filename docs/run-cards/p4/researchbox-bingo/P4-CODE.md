# P4 Code (ResearchBox #8869)

**Column:** </> Code  
**Section:** P4 Confirmatory Close-out (2026-08-21)  
**Role:** Scripts that implemented Gates 0 / A–I / P0-T / Q–W on the pinned nanochat tree. Vendor nanochat itself is Karpathy commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` (clone separately; not duplicated here).

Use `scripts/p4/env.sh` / `env.cuda.sh` only. Never `scripts/p1/env.sh`, `scripts/p2/env.sh`, or `scripts/p3/env.sh`.

## Files in this packet

| File | Role |
|---|---|
| `Code.zip` | **`.py` / `.sh` only** under `scripts_p4/` |
| `p4_code_crosswalk.csv` | Upload under **Data** (not inside Code.zip) |
| `p4_code_crosswalk_3_columns.csv` | Upload under **Data** (column codebook) |
| `P4-CODE.md` | Cover note in **Other** |

`gate_v_c3_test.py` is deposited for audit. Re-running it would violate the closed P4 test boundary (Policy A: one C3-only event).

Official evaluator SHA-256 (do not edit): `9afebdb405aaac0bb4287051d9b6f5d16f56d6dd9269a1e6c2c5df29becbced1`.

## Pin

- nanochat pin: `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`
- Run ID: `p4-20260821T060032Z-92d63d4`
- Tokenizer: carry-forward P3 pair (both artifacts); C3 constructed **after** tokenizer freeze
