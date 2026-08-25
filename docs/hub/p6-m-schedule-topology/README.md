---
license: other
library_name: nanochat
tags:
  - nanochat
  - bits-per-byte
  - tagalog
  - english
  - schedule-topology
  - continual-pretraining
  - one-seed
---

# nanochat-filipino P6-M (schedule topology, seed 4)

Matched-branch **research checkpoints** for one unused parent-init seed **4**. Frozen Tagalog parent **C0**, controls **C1** / **C2**, and four schedule-topology children **M-fine**, **M-coarse**, **M-blocked**, **M-rand**. Not a chat, instruction, or production model.

**Ship C0+C1+C2+all four topology arms together.** Never present one topology child as “the P6-M model.” Never write onto P1.1–P5 Hub IDs.

**Weight upload status: uploaded** (commit [`5d3872b0`](https://huggingface.co/pageman/nanochat-filipino-p6-m-schedule-topology/commit/5d3872b000fe3aa7ed2d25e2e73927330002cb9b)).

### Weight lineage (important)

| Objects | Lineage |
|---|---|
| C0, C1, C2, `tokenizer.pkl`, `token_bytes.pt` | Original study artifacts (filed Gate Q–S receipts) |
| M-fine, M-coarse, M-blocked, M-rand | **Technical recreate** (2026-08-25) after original Gate T terminals were lost from the sticky study volume. **New SHA-256 values**; not bitwise identical to the original Gate T filings |

Science claims remain AsPredicted #307969 / Gate X / released contrasts. Hub topology weights are the deposit sibling set under the recreate lineage documented in `RELEASE_MANIFEST.json`.

## Paper and code

- **GitHub** [pageman/nanochat-filipino](https://github.com/pageman/nanochat-filipino) P6-M subtrees (study record; push when authorized):
  - [`scripts/p6/`](https://github.com/pageman/nanochat-filipino/tree/main/scripts/p6)
  - [`docs/papers/p6-m-schedule-topology/`](https://github.com/pageman/nanochat-filipino/tree/main/docs/papers/p6-m-schedule-topology)
  - [`docs/run-cards/p6/`](https://github.com/pageman/nanochat-filipino/tree/main/docs/run-cards/p6)
  - [`manifests/p6/`](https://github.com/pageman/nanochat-filipino/tree/main/manifests/p6)
  - [`results/p6/`](https://github.com/pageman/nanochat-filipino/tree/main/results/p6)
  - [`docs/hub/p6-m-schedule-topology/`](https://github.com/pageman/nanochat-filipino/tree/main/docs/hub/p6-m-schedule-topology)

## Identity

- AsPredicted [#307969](https://aspredicted.org/bk6m9d.pdf)
- ResearchBox [#8918](https://researchbox.org/8918) · AsCollected [#2541 v1](https://ascollected.org/XZ8_TI5) (`NANOCHAT-FILIPINO P6-M`; Box #8918 link updated)
- Run ID `p6-20260824T155226Z-769f807a`
- nanochat pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`

## GitHub vs this Hub

| Surface | Put here | Do not put here |
|---|---|---|
| **GitHub** `pageman/nanochat-filipino` | P6 scripts, paper, LOCK, manifests, run-card receipts, `results/p6/`, this Hub documentation pack | `.pt` weight blobs, raw `test.jsonl`, SSH/`.env`, optimizer states, lockbox passcodes |
| **Hugging Face** this repo | Nine weightish siblings + tokenizer + `evaluation/` + SHA256SUMS + this card | Protocol as sole paper copy; a single topology arm; P1–P5 Hub IDs; holdout text |

## Layout (Hub paths)

| Hub path | Role |
|---|---|
| `seed-4/c0/p6-s4-c0-tl-d20-model_000294.pt` | Frozen Tagalog parent |
| `seed-4/c1/p6-s4-c1-tl-d20-model_000294.pt` | Extra-Tagalog control |
| `seed-4/c2/p6-s4-c2-en-d20-model_000294.pt` | Pure-English continuation |
| `seed-4/m-fine/p6-s4-m-fine-d20-model_000294.pt` | Fine interleave (recreate) |
| `seed-4/m-coarse/p6-s4-m-coarse-d20-model_000294.pt` | Coarse block (recreate) |
| `seed-4/m-blocked/p6-s4-m-blocked-d20-model_000294.pt` | Blocked schedule (recreate) |
| `seed-4/m-rand/p6-s4-m-rand-d20-model_000294.pt` | Random schedule (recreate) |
| `tokenizer.pkl` / `token_bytes.pt` | Study tokenizer pair |

Optimizer states are not released. Load with custom nanochat (`scripts/p6/`), not `transformers` chat pipelines.

## Checksums (SHA-256)

| Object | SHA-256 |
|---|---|
| C0 | `7fbd24de792aa4ee27d841866db2114e0fb45b1fdcaa4edcc9b24582220123c9` |
| C1 | `6223c116779ce3128c1e4cae0f2e03744b3068169ad7bb88f75a5146671a99bd` |
| C2 | `04c06c195e513c7b30752637b80591c29e740879d91c35c323fb75fafca8747d` |
| M-fine (recreate) | `69a5046ee756faba84f0f5e9c6a0f1330f886f9dd0344f02797798d1d2d0bfe7` |
| M-coarse (recreate) | `c09072fe764f1debd9607f697e2aa8484ef394a96d2ef096f05bb1f0d6c518f7` |
| M-blocked (recreate) | `ebfc4853b51cc8c81480ffb57640487d3fe344d38ec51ad5bb1eb7cf159272d2` |
| M-rand (recreate) | `16f6679310c379ce2403e587620eb0ef7d162d6e92ddfc9589d272915eff981d` |
| `tokenizer.pkl` | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| `token_bytes.pt` | `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132` |

Also in `RELEASE_MANIFEST.json` / `SHA256SUMS-weights.txt`.

## Primary result

Topology contrasts vs M-fine (`δ=0.01`): see `evaluation/primary_contrasts.json`. Policy A: M-fine test is secondary only.

## License

YAML `license: other` because training text is Wikipedia-derived. Research use of small decoder checkpoints; not a deployment certification. Not an official Cruz/Cheng/DLSU release.
