# P2 Gate R — A1 extra English **pass**

- Date (UTC): 2026-08-19T03:33:00Z launch → 2026-08-19T03:50:48Z terminal save
- Pod: `8ik4ix7j8iju9u`, NVIDIA A40, pid 1440
- **Status: pass.** Terminal step **294**. Visible tokens **19,267,584**.
- Parent A0 d20 SHA unchanged: `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d`
- A1 checkpoint SHA: `e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d`
- Test access: **0**. Tagalog continuation: **not started**.
- In-loop val is **not** `val_bpb_full`. Do not compute \(C_{EN}\) / \(G_{TL}\).

Command: `continue_from_frozen.py` → pin `base_train` with `--num-iterations=294 --warmup-steps=14`, fresh optimizer, English `en-active` only, `--core-metric-every=-1`, `--save-every=-1`, `resume_from_step=-1`. Comment-compatibility addendum applied as provenance only (A3 kept; d20 parent kept; no P2.1).

## Integrity

| Check | Result |
|---|---|
| Final step | 294 |
| `D_phase2` | 19,267,584 |
| Reload | ok, 147 keys |
| A0 frozen after A1 | same SHA; still `444` |
| No `--resume-from-step` | `0` “Resuming optimization” lines |
| Log SHA | `b452cd3b…` |

## Next

Archive is on host under `base_checkpoints/p2-a1-extra-en-d20/` plus local log/meta. **Stop and request explicit authorization for Gate S (A2).** Do not start Tagalog training until that authorization.
