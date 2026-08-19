# EN0 d20 stopped mid-run — volume full at step 2600

- Date (UTC): 2026-08-17T21:57Z save / 22:04Z noticed
- Pod: `8ik4ix7j8iju9u` still RUNNING, GPU idle
- Process pid 436: **not running**
- Last complete train step in log: **2599 / 5415** (loss 2.036, in-loop val 1.071 at 2600)
- No traceback, no CUDA OOM, no dmesg OOM

## Cause

80 GB volume filled (~75 GB in `p2-en0-d20`). Each save is ~2.5 GB model + ~3.5 GB optimizer.

`model_002600.pt` wrote fully. `optim_002600_rank0.pt` is **128 MiB** (should be 3.50 GiB) — truncated. Last **complete** bundle is **step 2400**.

## Recovery (not executed)

Official nanochat: `--resume-from-step=2400` (not 2600). Free space first (drop 200–2200 and the truncated 2600, or grow volume past 80 GB). Then same `N=5415` command. Record wall-clock gap. Do not start Tagalog.
