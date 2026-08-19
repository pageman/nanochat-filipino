# P2 study record (human-readable)

**P2 only.** Canonical GitHub audit trail for AsPredicted [#306935](https://aspredicted.org/xa56bs.pdf). Does **not** amend #306780, ResearchBox 8735, or Hub `pageman/nanochat-filipino-p1-fixed-d20-3x`.

Machine-readable seals live in [`results/p2/`](../../results/p2/). Weights are **not** in this git tree (`*.pt` gitignored). Hub: [pageman/nanochat-filipino-p2-en-then-tl](https://huggingface.co/pageman/nanochat-filipino-p2-en-then-tl).

## Paper and protocol

| Artifact | Path |
|---|---|
| Paper source | [`docs/papers/p2-cf-english/paper.tex`](../papers/p2-cf-english/paper.tex) |
| Current PDF | [`docs/papers/p2-cf-english/paper_outputs/paper.pdf`](../papers/p2-cf-english/paper_outputs/paper.pdf) |
| Protocol | [`docs/papers/p2-cf-english/PROTOCOL-p2-en-then-tl.md`](../papers/p2-cf-english/PROTOCOL-p2-en-then-tl.md) |
| Study lock (git) | [`docs/papers/p2-cf-english/LOCK.json`](../papers/p2-cf-english/LOCK.json) — passcode is not a real secret in-repo; sanitized copy in `results/p2/LOCK.sanitized.json` |
| Obsolete Stage-1 PDF | Quarantined: `docs/papers/p2-cf-english/paper_outputs/paper-OBSOLETE-stage1-20260816.pdf` |

## Model card, website, close-out

| Artifact | Path |
|---|---|
| Model card source | [`HF-MODEL-CARD-p2.md`](../run-cards/p2/HF-MODEL-CARD-p2.md) |
| Public status | [`PUBLIC-STATUS.md`](../run-cards/p2/PUBLIC-STATUS.md) |
| Close-out checklist | [`CLOSEOUT-CHECKLIST.md`](../run-cards/p2/CLOSEOUT-CHECKLIST.md) |
| Six-layer close-out | [`SIX-LAYER-CLOSEOUT.md`](../run-cards/p2/SIX-LAYER-CLOSEOUT.md) |
| Prereg reporting audit | [`PREREG-REPORTING-AUDIT.md`](../run-cards/p2/PREREG-REPORTING-AUDIT.md) |
| Run ID folder | [`docs/run-cards/p2/p2-20260817T150944Z-de99f8a/`](../run-cards/p2/p2-20260817T150944Z-de99f8a/) |

Do not publish `HOST-*.md` SSH/operator cards, `aspredicted-p2-submitted.txt`, or raw holdout JSONL.

## Reproduction (code, not data)

| Artifact | Path |
|---|---|
| P2 env only | [`scripts/p2/env.sh`](../../scripts/p2/env.sh), [`scripts/p2/env.cuda.sh`](../../scripts/p2/env.cuda.sh) — never `scripts/p1/env.sh` |
| Evaluator | [`scripts/p2/evaluate_bpb.py`](../../scripts/p2/evaluate_bpb.py) |
| Allowed nanochat patch | [`patches/nanochat-NANOCHAT_DATA_DIR.patch`](../../patches/nanochat-NANOCHAT_DATA_DIR.patch) |
| P2 scripts | [`scripts/p2/`](../../scripts/p2/) |
| Hub documentation pack | [`docs/hub/p2-en-then-tl/`](../hub/p2-en-then-tl/) |

## What this subtree does not contain

Raw WikiText-103 / P1.1 test text, protected validation/test packages, P1.1 weights under P2 paths, optimizer states, `.env` / secrets, private SSH materials, caches, and the uncorrected “A3 mitigated BWT” planning note.
