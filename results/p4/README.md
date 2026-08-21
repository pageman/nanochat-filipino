# P4 sealed results (`results/p4/`)

**P4 only.** AsPredicted [#307591](https://aspredicted.org/if84km.pdf) · ResearchBox [#8869](https://researchbox.org/8869) · AsCollected #2471 (`NANOCHAT-FILIPINO-P4`).

Run ID: `p4-20260821T060032Z-92d63d4` · pin `92d63d4`. **C3 is not P3 B3.**

## Contents

| Path | Role |
|---|---|
| `released/` | Gate X released BPB cells, seal, Gate V, P0-T eligibility |
| `evaluation/` | Convenience copies of seal / Gate V / P0-T / Hub tables |
| `tables.json` | Six-decimal paper cells from released seals only |
| `gate-e-packed-streams-and-c3-freeze.json` | Gate E packed streams + C3 freeze (byte shares descriptive) |
| `LOCK.sanitized.json` | Sanitized lock snapshot (no secrets) |
| `released_manifest.json` / `p4_closeout_manifest.json` | Manifests |

## Primary sealed contrasts (Gate X)

- \(R_{\mathrm{TL}}=\mathrm{TL}(C3)-\mathrm{TL}(C2)=-1.316637\) → **observed** (filed \(\le -0.01\))
- \(A_{\mathrm{EN}}=\mathrm{EN}(C3)-\mathrm{EN}(C1)=-1.375277\) → **observed** (filed \(\le -0.01\))

Do **not** cite P1.1 `1.164768` or P2/P3 Gate V as P4. Raw test text is not here.

Hub weights: [`pageman/nanochat-filipino-p4-token-share-mix`](https://huggingface.co/pageman/nanochat-filipino-p4-token-share-mix) (C0+C1+C2+C3 together).
