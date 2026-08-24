# P5 study record

**P5 only.** Closed three-seed panel of the frozen P4 token-share apparatus after **fresh unused** Tagalog parents. Does **not** amend AsPredicted #306780, #306935, #307342, or **#307591**. Does **not** load P1.1 / P2 / P3 / P4 weights. **C3 is not P3 B3.** P4 seed 0 is historical, not a P5 confirmatory cell.

**Filed:** AsPredicted [#307836](https://aspredicted.org/k6ib64.pdf). Local copy: [`docs/run-cards/p5/AsPredicted-307836.pdf`](../run-cards/p5/AsPredicted-307836.pdf). SHA256 `439d1de5ff9fd18e466f33192c5ac9c5c36b020ca72942ae218b9e69a8f5bbf3`.

**Lock:** [`docs/papers/p5-multi-seed-p4/LOCK.json`](../papers/p5-multi-seed-p4/LOCK.json)  
**Env:** [`scripts/p5/env.sh`](../../scripts/p5/env.sh) — never `scripts/p1/`, `scripts/p2/`, `scripts/p3/`, or `scripts/p4/` at runtime.

**Status:** Gates **0 / A–H / I₁–V₃ / X / W** complete. One panel unblinding. Sealed results: [`results/p5/`](../../results/p5/). Paper: [`docs/papers/p5-multi-seed-p4/`](../papers/p5-multi-seed-p4/). Hub (weights deferred): [`pageman/nanochat-filipino-p5-p4-multi-seed`](https://huggingface.co/pageman/nanochat-filipino-p5-p4-multi-seed). ResearchBox [#8904](https://researchbox.org/8904) (FOR PEER REVIEW). AsCollected [#2503 v1](https://ascollected.org/HC8_G2F).

**Primary panel result:** $k_{\mathrm{both}}=3$ of $K_{\mathrm{elig}}=3$. Count table, not a CI, not “P5 confirms P4.”

## Paper and protocol

| Artifact | Path |
|---|---|
| Paper source | [`docs/papers/p5-multi-seed-p4/paper.tex`](../papers/p5-multi-seed-p4/paper.tex) |
| Current PDF | [`docs/papers/p5-multi-seed-p4/paper_outputs/paper.pdf`](../papers/p5-multi-seed-p4/paper_outputs/paper.pdf) |
| Study lock (git) | [`docs/papers/p5-multi-seed-p4/LOCK.json`](../papers/p5-multi-seed-p4/LOCK.json) |
| Hub documentation pack | [`docs/hub/p5-p4-multi-seed/`](../hub/p5-p4-multi-seed/) |
| Run ID folder | [`docs/run-cards/p5/p5-20260823T160632Z-439d1de5/`](../run-cards/p5/p5-20260823T160632Z-439d1de5/) |

Do not publish `HOST-*.md` SSH/operator cards or raw holdout JSONL.

## What this GitHub subtree contains vs Hugging Face

See the paper appendix and [`docs/hub/p5-p4-multi-seed/README.md`](../hub/p5-p4-multi-seed/README.md). GitHub: scripts, paper, receipts, sealed JSON. Hugging Face: optional C0+C1+C2+C3 weight bundles per eligible seed.

## What this subtree does not contain

Raw WikiText-103 / P1.1 test text, optimizer states, `.env` / secrets, private SSH materials, caches, and P1.1/P2/P3/P4 weights.
