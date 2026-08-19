# P2 Gate S — A2 Tagalog continuation **pass**

- Date (UTC): 2026-08-19T04:56:00Z launch → 2026-08-19T05:08:23Z terminal save
- Pod: `8ik4ix7j8iju9u`, NVIDIA A40, pid 5670
- **Status: pass.** Terminal step **294**. Visible tokens **19,267,584**.
- Parent A0 d20 SHA unchanged: `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d`
- A1 SHA unchanged (not parent): `e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d`
- A2 checkpoint SHA: `2b01acf8fac0e8c783162582cbb384e8ce1c37795aae2f7dd4ae34c2a5c76026`
- Test access: **0**.
- In-loop val is **not** `val_bpb_full`. Do not compute \(C_{EN}\) / \(G_{TL}\).

Command: `continue_from_frozen.py` → pin `base_train` with `--num-iterations=294 --warmup-steps=14`, fresh optimizer, Tagalog `p2-tl39-readonly` only, `--allowed-model-tag p2-a2-tagalog-d20`, `--core-metric-every=-1`, `--save-every=-1`, `resume_from_step=-1`. Wrapper SHA same as A1. Does not amend #306780 or #306935.

## Integrity

| Check | Result |
|---|---|
| Final step | 294 |
| `D_phase2` | 19,267,584 |
| Reload | ok, 147 keys |
| A0 frozen after A2 | same SHA; still `444` |
| A1 not parent | same SHA; wrapper loaded A0 only; 0 “Resuming optimization” lines |
| Only terminal model | `model_000294.pt` (plus meta/optim) |
| Log SHA | `084f6c61…` |

## Next

Archive is on host under `base_checkpoints/p2-a2-tagalog-d20/` plus local log/meta/ckpt. **Stop and request explicit authorization for Gate T (A3).** Do not start mix training until that authorization. Do not seal validation or read test.
