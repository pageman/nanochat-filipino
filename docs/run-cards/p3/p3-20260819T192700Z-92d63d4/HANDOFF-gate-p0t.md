# Gate P0-T handoff — P3 #307342

**Status:** **P0-T: PASS** on Runpod A40 pod `bef5h2lzy6f3mp`.

Both TL0 depths (d8, d20) beat untrained and Tagalog byte-unigram floors by the filed 0.01 BPB margin. Scalar BPB values remain in lockbox until Gate X.

| Depth | pass_both_floors | checkpoint SHA256 |
|---|---|---|
| d8 | true | `feaf7017…f462e2` |
| d20 | true | `ae621be2…7193c` |

**Safe operator output:** `P0-T: PASS`  
**Safe file:** `data/cache/p3-…/safe_progress/gate-p0-t-status.json`  
**Receipt:** `gate-p0-t.json`  
**Preflight:** `gate-p0t-preflight.json`

Lockboxed (gitignored):
- `lockbox/gate-p0-t-eligibility.json`
- `lockbox/gate-p0-t-eval-detail.json`
- `lockbox/gate-p0-t-eval-full.log`

Scripts: `gate_p0t_preflight.py`, `gate_p0t.sh`, `gate_p0t_accept.py`, `evaluate_bpb.py`

**Next:** Gate **Q** — immutable B0 freeze (copy TL0 d20 final checkpoint). English train and B1/B2/B3 are now authorized.
