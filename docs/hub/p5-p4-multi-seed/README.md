---
license: other
library_name: nanochat
tags:
  - nanochat
  - bits-per-byte
  - tagalog
  - english
  - continual-pretraining
  - token-share
  - multi-seed
  - post-p4
---

# nanochat-filipino P5 (closed three-seed panel)

Matched-branch **research checkpoints** for a **closed panel** of unused parent-init seeds `{1,2,3}`. For each eligible seed: frozen Tagalog parent **C0** plus children **C1**, **C2**, and **C3**. This is not a chat, instruction, or production model.

**Ship C0+C1+C2+C3 together per eligible seed.** Never present one seed's C3 as “the P5 model.” **C3 is not P3 B3.** P4 seed 0 is historical, not a P5 confirmatory cell.

**Weight upload status: uploading** (C0+C1+C2+C3 per eligible seed `{1,2,3}` together). Do not write these files onto `pageman/nanochat-filipino-p4-token-share-mix`.

## Identity and scope

**P5 only.** Not P1.1. Not P2. Not P3. Not P4. **Not trained from** prior Hub IDs.

- AsPredicted [#307836](https://aspredicted.org/k6ib64.pdf)
- ResearchBox [#8904](https://researchbox.org/8904) · AsCollected [#2503 v1](https://ascollected.org/HC8_G2F)
- GitHub audit trail: [pageman/nanochat-filipino](https://github.com/pageman/nanochat-filipino) (`results/p5/`, `docs/p5/`, `docs/hub/p5-p4-multi-seed/`)
- Run ID `p5-20260823T160632Z-439d1de5`
- nanochat pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`

## GitHub vs this Hub

| Surface | Put here | Do not put here |
|---|---|---|
| **GitHub** `pageman/nanochat-filipino` | `scripts/p5/`, paper, `LOCK.json`, manifests, run-card receipts, sealed JSON, this documentation pack | `.pt` weight blobs, raw `test.jsonl`, SSH/`.env`, optimizer states, HOST operator cards |
| **Hugging Face** this repo | Per eligible seed: `seed-{s}/c0`–`c3` checkpoints + tokenizer + `evaluation/` JSON + SHA256SUMS | Protocol markdown as the only copy of the paper; C3 alone; P4 weights; holdout text |

## Intended files (when weights are staged)

Carry-forward P4 tokenizer at repo root. Then, for each eligible seed:

| Path | Role |
|---|---|
| `seed-{s}/c0/p5-s{s}-c0-tl-d20-model_000294.pt` | Frozen Tagalog parent |
| `seed-{s}/c1/p5-s{s}-c1-tl-d20-model_000294.pt` | Extra-Tagalog control |
| `seed-{s}/c2/p5-s{s}-c2-en-d20-model_000294.pt` | Pure-English continuation |
| `seed-{s}/c3/p5-s{s}-c3-mix-d20-model_000294.pt` | P4-frozen token-share mix |
| `tokenizer.pkl` / `token_bytes.pt` | Carry-forward P4 pair |

Optimizer states are not released. Load with custom nanochat (`scripts.base_train` / `scripts/p5/evaluate_bpb.py`), not `transformers` chat pipelines.

## Primary panel result

Count table only (`K=3`): eligible 3; both 3; only-R 0; only-A 0; neither 0; ineligible 0. Machine-readable: GitHub `results/p5/`.

No mean, CI, $p$-value, or “P5 confirms P4.” Tests are C3-only and secondary.

## Checksums (checkpoints)

| Seed | Arm | SHA-256 |
|---|---|---|
| 1 | C0 | `c5bf0f495f7cb296374105c62b5946aa30cfb33fa86c58c08434c37862631ac6` |
| 1 | C1 | `8d474aa88a250895dd410b0027277dd19a2b8f41a77544902ec4bbc774c33f14` |
| 1 | C2 | `f9701fae3277f5c379d69d97dd3ba9b706324bf72660731b0a4fbb34371e628e` |
| 1 | C3 | `f7c080048d4311863836fb6cf2c06d9d555514bcce7e30a5d8b819aa0dd15252` |
| 2 | C0 | `e4c4cc7bcdf5033a97f9eedd97f7818d3c8e3ddca2b46fffc8b8c78d6137c4b1` |
| 2 | C1 | `aaee36fd5ceb53c2e92138eb2dfa8b169bd000caf5b804d9c8645d6ad56c4f22` |
| 2 | C2 | `e75b4c61bf3dd2cd661d931dfc63526c810dd96bf8db2fcac0f2cadb5e29c102` |
| 2 | C3 | `0801f1437b334a68ee155623111ecba2dc03cfc49c46e8630f023c41aa21ac77` |
| 3 | C0 | `7643b12645f487b4f38034f14985c624804ac43534cfafc723bae83edc4c3c26` |
| 3 | C1 | `edfabbf8dbb38aefbfd61850f30efba40d8d77c8dffc02ce4db403969787b66f` |
| 3 | C2 | `e3cd58a5fa549b62c60c568a551f3d471df5b77698208a4727c0a52266d3f58a` |
| 3 | C3 | `1759110154b2a4176e584bcd675d4b21d10cda0f9936e8f6a188aa32ba8f2ab7` |
| — | `tokenizer.pkl` | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| — | `token_bytes.pt` | `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132` |

## License

YAML `license: other` because the training text is Wikipedia-derived. Research use of small decoder checkpoints; not a deployment certification.
