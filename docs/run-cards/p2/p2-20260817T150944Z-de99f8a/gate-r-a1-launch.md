# P2 Gate R — A1 launch card (awaiting authorization)

- Date (UTC): 2026-08-19T02:27:53Z (launch card) / 2026-08-19T03:02:39Z (prelaunch integrity)
- **Status: prelaunch integrity complete; awaiting `Yes, launch Gate R / A1.`** No A1 training token has been consumed.
- Arm: **A1** matched extra-English continuation · tag `p2-a1-extra-en-d20`
- Parent: immutable **A0 d20** only
- Host: `8ik4ix7j8iju9u` (NVIDIA A40 48 GB, EU-SE-1, $0.44/hr), GPU **idle**
- Test access: **0** (P1.1 `manifests/test_access_log.json` is not a P2 event)

Pin `scripts.base_train` has **no** `--load`. `--resume-from-step` loads optimizer state and is forbidden. The requested command uses P2-only `scripts/p2/continue_from_frozen.py` (does not edit vendor files): load frozen A0 weights with `load_optimizer=False`, then let the pin create a **fresh** optimizer and run exactly **N=294** new steps.

## Preflight table

| Item | Value |
|---|---|
| A0 SHA-256 (local = host = LOCK/Q) | `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d` |
| A0 path | `a0/frozen/p2-en0-d20/model_005415.pt` (not the writable EN0 tag as sole parent) |
| A0 mode | local `444`; host file `444`, d20 dir `555`; parent `a0/frozen/` still `777` (ops residual; hash is authoritative) |
| EN train SHAs | `9bdee964…` / `7331e621…` / `59bc144b…` / `ac693bfc…` (Gate E; host match) |
| EN val (last shard, in-loop only) | `b20942ae…` — not train-selected; test absent |
| Tagalog in A1 train-visible dir | none |
| Tokenizer / `token_bytes.pt` | `946a04ef…` / `5ae2ea1d…` · vocab 32768 · mode 444 |
| Depth / T / B / N | d20 / 2048 / 65536 / **294** (`D=19,267,584`) |
| Optimizer / LR / warmup | fresh; CLI LRs = 0.3× EN0 CLI; warmup **14** |
| `--core-metric-every` | `-1` |
| `--target-param-data-ratio` | omitted (never `-1`) |
| Output dir `p2-a1-extra-en-d20` | **absent** locally and on host (new/empty) |
| Device | A40, 0% util, 0 MiB used; workspace 80 GB; no training process |
| Training `.venv` on host | restored with `uv sync --frozen` (Python 3.10.19, torch 2.9.1+cu128) |
| P1.1 `model_000294.pt` in P2 cache | absent |
| `flash_attention.py` | unpatched |

## Requested command (not executed)

On host, after copying `scripts/p2/continue_from_frozen.py`, chmod of frozen A0, and `uv sync`:

```bash
source scripts/p2/env.cuda.sh   # unsets NANOCHAT_DATA_DIR; never source scripts/p1/env.sh
cd "$P2_ROOT/vendor/nanochat"
export NANOCHAT_BASE_DIR="$P2_ROOT/data/cache/p2-20260817T150944Z-de99f8a"
export NANOCHAT_DATA_DIR="$NANOCHAT_DATA_DIR_EN"
export WANDB_MODE=disabled
export OMP_NUM_THREADS=1

python "$P2_ROOT/scripts/p2/continue_from_frozen.py" \
  --init-from "$NANOCHAT_BASE_DIR/a0/frozen/p2-en0-d20" \
  --init-step 5415 \
  --expected-sha bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d \
  --allowed-model-tag p2-a1-extra-en-d20 \
  -- \
  --device-type=cuda \
  --depth=20 \
  --max-seq-len=2048 \
  --window-pattern=SSSL \
  --device-batch-size=8 \
  --total-batch-size=65536 \
  --num-iterations=294 \
  --warmup-steps=14 \
  --embedding-lr=0.09 \
  --unembedding-lr=0.0024 \
  --matrix-lr=0.006 \
  --scalar-lr=0.15 \
  --weight-decay=0.28 \
  --eval-tokens=124438 \
  --eval-every=50 \
  --core-metric-every=-1 \
  --sample-every=200 \
  --save-every=-1 \
  --model-tag=p2-a1-extra-en-d20 \
  --run=p2-a1-extra-en-d20
```

Expected wall ~25–40 min at EN0’s ~5.3 s/step plus evals. Monitor only CUDA/OOM, finite loss, expected outputs, and terminal step 294. In-loop val is **not** `val_bpb_full`.

Comment compatibility (informal sources only; not an amendment): `gate-r-comment-compatibility.md`. Do not skip A3. Do not switch to d8. Do not create P2.1 before A1.

## Still banned until this command is authorized

- Launching the 294-step job because the pod is idle
- Gate S / T / U
- Test evaluation
- Loading P1.1 weights or mutating A0
- Interpreting partial validation as a result

## Next after a normal A1 finish

Archive A1 checkpoint + hashes + logs + run card. Then **stop and request authorization for Gate S** (A2). Do not compute `C_EN` / `G_TL`.
