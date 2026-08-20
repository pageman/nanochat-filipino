# P3 sealed results (`results/p3/`)

**P3 only.** AsPredicted [#307342](https://aspredicted.org/wd2pc8.pdf) · ResearchBox [#8834](https://researchbox.org/8834) · AsCollected [F36_C2C](https://ascollected.org/F36_C2C).

Run ID: `p3-20260819T192700Z-92d63d4` · pin `92d63d4`.

## Contents

| Path | Role |
|---|---|
| `released/` | Gate X released BPB cells, seal, Gate V, P0-T eligibility |
| `evaluation/` | Convenience copies of seal / Gate V / P0-T |
| `gate-e-shards.json` | Gate E packed streams + B3 freeze (byte shares) |
| `LOCK.sanitized.json` | Sanitized lock snapshot (no secrets) |
| `released_manifest.json` / `p3_closeout_manifest.json` | Manifests |

## Primary sealed contrasts (Gate X)

- \(C_{tl}=\mathrm{TL}(B2)-\mathrm{TL}(B1)=1.023484\) → **observed** (filed \(\ge 0.01\))
- \(G_{en}=\mathrm{EN}(B2)-\mathrm{EN}(B1)=-1.697955\) → **observed** (filed \(\le -0.01\))

Do **not** cite P1.1 `1.164768` or P2 Gate V as P3. Raw test text is not here.

Hub weights: [`pageman/nanochat-filipino-p3-tl-then-en`](https://huggingface.co/pageman/nanochat-filipino-p3-tl-then-en) (B0+B1+B2+B3 together).
