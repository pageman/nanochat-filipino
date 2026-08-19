# P2 Gate T — A3 mix continuation **pass**

- Date (UTC): 2026-08-19T05:31:00Z launch → 2026-08-19T05:46:30Z terminal save
- Pod: `8ik4ix7j8iju9u`, NVIDIA A40, pid 9134
- **Status: pass.** Terminal step **294**. Visible tokens **19,267,584**.
- Parent A0 d20 SHA unchanged: `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d`
- A1 SHA unchanged (not parent): `e2881049…2385d`
- A2 SHA unchanged (not parent): `2b01acf8…76026`
- A3 checkpoint SHA: `d6c62bb793a57c7c23d98c5bd62ec36b41606234524f76855b4459d98c42b368`
- Mix: Gate E 50/50 **documents**, seed 42, K=28472, order SHA `b6ae432b…` (not regenerated)
- Test access: **0**.
- In-loop val is **not** `val_bpb_full`. Do not compute \(C_{EN}\) / \(G_{TL}\).

Command: `continue_from_frozen.py` → pin `base_train` with `--num-iterations=294 --warmup-steps=14`, fresh optimizer, `p2-mix-a3-50-50` only, `--allowed-model-tag p2-a3-mix-d20`, `--core-metric-every=-1`, `--save-every=-1`, `resume_from_step=-1`. Wrapper SHA same as A1/A2. Does not amend #306780 or #306935.

## Integrity

| Check | Result |
|---|---|
| Final step | 294 |
| `D_phase2` | 19,267,584 |
| Reload | ok, 147 keys |
| A0 frozen after A3 | same SHA; still `444` |
| A1/A2 not parents | same SHAs; wrapper loaded A0 only; 0 “Resuming optimization” lines |
| Mix hashes | Gate E train `3be332f5…` / `36814536…` / `c6ee0054…` / `9d8662f0…`; last-shard val `b20942ae…` (English val copy) |
| Only terminal model | `model_000294.pt` (plus meta/optim) |
| Log SHA | `e5d922f8…` |

## Next

Archive is on host under `base_checkpoints/p2-a3-mix-d20/` plus local log/meta/ckpt. **Stop and request explicit authorization for Gate U** (validation seal, confirmatory `val_bpb_full`, then \(C_{EN}\) / \(G_{TL}\)). Do not read test.
