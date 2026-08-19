# P2 Code (ResearchBox 8763)

**Column:** </> Code  
**Section:** P2  
**Role:** Scripts that implemented Gates A–W on the pinned nanochat tree. Vendor nanochat itself is Karpathy commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` (clone separately; not duplicated here).

Use `scripts/p2/env.sh` / `env.cuda.sh` only. Never `scripts/p1/env.sh`.

## Files in this packet

| File | Role |
|---|---|
| `P2-CODE.md` | This cover |
| `env.sh` | Laptop/CPU P2 environment |
| `env.cuda.sh` | CUDA host environment |
| `continue_from_frozen.py` | Child A1/A2/A3 wrapper; `load_optimizer=False`; child step 0 |
| `evaluate_bpb.py` | Official full `val_bpb_full` / test BPB (BOS-best-fit, T=2048) |
| `gate_c_hygiene.py` … `gate_g_budget.py` | Gates C–G |
| `gate_h_preflight.py` | Gate H preflight |
| `gate_q_a0_freeze.py` | A0 freeze |
| `gate_u_seal.py` | Gate U validation seal (no test) |
| `gate_v_test.py` | Gate V A2-only test (requires `GATE_V_AUTHORIZED=1`; **do not re-run**) |
| `report_registered_exposure.py` | Post-seal exposure/A3 token-share reconstruction on **train** files only |
| `build_closeout_archive.py` | Hash/archive builder (no BPB) |

`gate_v_test.py` is deposited for audit. Re-running it would violate the closed P2 test boundary.

## Pin and documented vendor drift

- nanochat pin: `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`
- Documented hook: `NANOCHAT_DATA_DIR` only
- Confirmatory path: unpatched SDPA (`flash_attn` not installed)
- Pinned `base_train` has no `--load`; children use the P2 wrapper
