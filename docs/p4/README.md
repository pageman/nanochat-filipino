# P4 study record

**P4 only.** Token-share-locked English–Tagalog mixture trade-off after a **fresh** Tagalog parent. Does **not** amend AsPredicted #306780, #306935, or #307342. Does **not** reuse P1.1, P2, or P3 weights. **C3 is not P3 B3.**

**Filed:** AsPredicted [#307591](https://aspredicted.org/if84km.pdf). Local copy: [`docs/run-cards/p4/AsPredicted-307591.pdf`](../run-cards/p4/AsPredicted-307591.pdf). SHA256 `463b29fcff8d7c8099790325fa19d6bcf9ee29f64424c373a380566a6fe9011c`.

**Lock:** [`docs/papers/p4-token-share-mix/LOCK.json`](../papers/p4-token-share-mix/LOCK.json)  
**Protocol (SHA in PDF):** [`PROTOCOL-p4-token-share-mix.md`](../papers/p4-token-share-mix/PROTOCOL-p4-token-share-mix.md) `22c28f2bc632f132d9c95bbbcc9d1facbddf0b6b821445487e451c472ea58d4b`  
**Env:** [`scripts/p4/env.sh`](../../scripts/p4/env.sh) — never `scripts/p1/env.sh`, `scripts/p2/env.sh`, or `scripts/p3/env.sh`.

**Status:** Gates **0 / A–I / P0-T / Q–W** complete. Gate X unblinded / released. Sealed results: [`results/p4/`](../../results/p4/). Paper: [`docs/papers/p4-token-share-mix/`](../papers/p4-token-share-mix/). Hub: [`pageman/nanochat-filipino-p4-token-share-mix`](https://huggingface.co/pageman/nanochat-filipino-p4-token-share-mix). ResearchBox [#8869](https://researchbox.org/8869); AsCollected #2471 (`NANOCHAT-FILIPINO-P4`).

**Primary (one seed):** \(R_{\mathrm{TL}}=-1.316637\) **observed**; \(A_{\mathrm{EN}}=-1.375277\) **observed**. C3 is a token-share trade-off, not P3 B3, not a general mitigation.

P4 is a **post-P3** prospective study. Do not cite P1.1 `1.164768` or P2/P3 Gate V as P4.

## Paper and protocol

| Artifact | Path |
|---|---|
| Paper source | [`docs/papers/p4-token-share-mix/paper.tex`](../papers/p4-token-share-mix/paper.tex) |
| Current PDF | [`docs/papers/p4-token-share-mix/paper_outputs/paper.pdf`](../papers/p4-token-share-mix/paper_outputs/paper.pdf) |
| Protocol | [`docs/papers/p4-token-share-mix/PROTOCOL-p4-token-share-mix.md`](../papers/p4-token-share-mix/PROTOCOL-p4-token-share-mix.md) |
| Study lock (git) | [`docs/papers/p4-token-share-mix/LOCK.json`](../papers/p4-token-share-mix/LOCK.json) — passcode is null in-repo |
| Hub documentation pack | [`docs/hub/p4-token-share-mix/`](../hub/p4-token-share-mix/) |
| Run ID folder | [`docs/run-cards/p4/p4-20260821T060032Z-92d63d4/`](../run-cards/p4/p4-20260821T060032Z-92d63d4/) |

Do not publish `HOST-*.md` SSH/operator cards or raw holdout JSONL.

## Reproduction (code, not data)

| Artifact | Path |
|---|---|
| P4 env only | [`scripts/p4/env.sh`](../../scripts/p4/env.sh), [`scripts/p4/env.cuda.sh`](../../scripts/p4/env.cuda.sh) |
| Evaluator | [`scripts/p4/evaluate_bpb.py`](../../scripts/p4/evaluate_bpb.py) |
| P4 scripts | [`scripts/p4/`](../../scripts/p4/) |

## What this subtree does not contain

Raw WikiText-103 / P1.1 test text, optimizer states, `.env` / secrets, private SSH materials, caches, and P1.1/P2/P3 weights.
