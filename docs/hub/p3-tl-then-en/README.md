---
license: other
library_name: nanochat
tags:
  - nanochat
  - bits-per-byte
  - tagalog
  - english
  - continual-pretraining
  - reverse-direction
---

# nanochat-filipino P3 (TL then EN)

Matched-branch **research checkpoints**: frozen Tagalog parent **B0** plus children **B1**, **B2**, and **B3**. This is not a chat, instruction, or production model. **One seed.**

P3 is a matched branch study. Use the four files together; do not treat B2 as a standalone “English nanochat.”

## Identity and scope

**P3 only.** Not P1.1. Not P2. **Not trained from** `pageman/nanochat-filipino-p1-fixed-d20-3x` or `pageman/nanochat-filipino-p2-en-then-tl`.

- AsPredicted [#307342](https://aspredicted.org/wd2pc8.pdf)
- ResearchBox [8834](https://researchbox.org/8834)
- AsCollected [F36_C2C](https://ascollected.org/F36_C2C)
- Paper (ResearchGate v1.2): [Tagalog Retention and English Acquisition under Equal-Budget nanochat Continual Pretraining v1.2](https://www.researchgate.net/publication/412889563_Tagalog_Retention_and_English_Acquisition_under_Equal-Budget_nanochat_Continual_Pretraining_v12_-_A_Preregistered_Post-P2_Reverse-Direction_Study_on_WikiText-TL-39_and_WikiText-103)
- GitHub audit trail: [pageman/nanochat-filipino](https://github.com/pageman/nanochat-filipino) (`results/p3/`, `docs/p3/`, `docs/hub/p3-tl-then-en/`)
- Run ID `p3-20260819T192700Z-92d63d4`
- nanochat pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`

Do not upload these files onto P1.1 or P2 Hub repositories.

## Files

Ship **B0+B1+B2+B3 together**; do not treat B2 as a standalone model.

| Path | Role |
|---|---|
| [`b0/p3-tl0-d20-model_000294.pt`](b0/p3-tl0-d20-model_000294.pt) | B0 frozen Tagalog parent (step 294) |
| [`b0/meta_000294.json`](b0/meta_000294.json) | B0 trainer meta (`val_bpb` here is **not** `val_bpb_full`) |
| [`b1/p3-b1-extra-tl-d20-model_000294.pt`](b1/p3-b1-extra-tl-d20-model_000294.pt) | B1 extra-Tagalog control |
| [`b1/meta_000294.json`](b1/meta_000294.json) | B1 trainer meta |
| [`b2/p3-b2-en-d20-model_000294.pt`](b2/p3-b2-en-d20-model_000294.pt) | B2 English continuation (only tested arm) |
| [`b2/meta_000294.json`](b2/meta_000294.json) | B2 trainer meta |
| [`b3/p3-b3-mix-d20-model_000294.pt`](b3/p3-b3-mix-d20-model_000294.pt) | B3 50/50-document mix (trade-off, **not** mitigation) |
| [`b3/meta_000294.json`](b3/meta_000294.json) | B3 trainer meta |
| [`tokenizer.pkl`](tokenizer.pkl) | P3 Tagalog 32,768 BPE |
| [`token_bytes.pt`](token_bytes.pt) | Token UTF-8 bytes |

Optimizer states are not in this release. Load with custom nanochat (`scripts.base_train` / `scripts/p3/evaluate_bpb.py`), not `transformers` `from_pretrained` as a causal LM chat pipeline.

## Research purpose

Controlled, preregistered continual-pretraining evidence on Tagalog retention after English continuation (reverse of P2). Not a leaderboard, production deployment, or instruction-following claim.

## Branch map

All d20, same immutable Tagalog parent B0, same phase-2 budget \(N=294\), \(D=19{,}267{,}584\), fresh optimizer, P3 Tagalog 32,768 BPE.

- **B0** frozen Tagalog parent
- **B1** extra-Tagalog active control from B0
- **B2** English-only continuation from B0 (only tested branch)
- **B3** pre-frozen 50/50-document English–Tagalog mix from B0

## Data provenance

Frozen P1.1 WikiText-TL-39 train/val manifests and WikiText-103-raw English. **Raw protected holdout text is not released.**

## Evaluation table (sealed)

Full validation (`val_bpb_full`), Gate U. Machine-readable copies: [`evaluation/`](evaluation/) and GitHub `results/p3/`.

| Arm | Tagalog | English |
|---|---:|---:|
| B0 | (via P0-T) | 2.618891 |
| B1 | 1.468600 | 3.032277 |
| B2 | 2.492084 | 1.334322 |
| B3 | 1.193565 | 1.348593 |

Primary contrasts: \(C_{tl}=TL(B2)-TL(B1)=1.023484\) (**observed**); \(G_{en}=EN(B2)-EN(B1)=-1.697955\) (**observed**).

B2-only **secondary** tests (Gate V): English WT103-raw test BPB 1.357842; P1.1 legacy Tagalog holdout under P3 BPE 2.493197. P1.1 native-BPE test BPB 1.164768 and P2 Gate V numbers are **not** reused. B1/B3 were not tested.

## Interpretation boundary

Both registered primary patterns were **observed** in this **one-seed** fixed apparatus. No significance test, confidence interval, population effect, or universal-language claim. B3 is a 50/50-document trade-off arm (realized UTF-8 byte share English ≈0.961 / Tagalog ≈0.039; Gate E; \(K=28472\)), not mitigation.

## Checksums

See [`SHA256SUMS.txt`](SHA256SUMS.txt) and [`RELEASE_MANIFEST.json`](RELEASE_MANIFEST.json). Re-hash downloads before use.

| File | Role | SHA-256 |
|---|---|---|
| `b0/…model_000294.pt` | B0 | `ae621be2c90a3d295f8d21b0e53cb9d4b717803f5d5337fa68f3c3f84d57193c` |
| `b1/…model_000294.pt` | B1 | `3f98784bf6e6bdf78785f370140a0db2dd170a848f93897d75c88b44740e2c54` |
| `b2/…model_000294.pt` | B2 | `5ee34b20f6601b1753ee6338b5447e091964ddd1087ca66c57434011e6341cc1` |
| `b3/…model_000294.pt` | B3 | `521bea166f13a8eee57fef1ac381aa4f715037a3f3f60a85c74c05e02b55ae2d` |
| `tokenizer.pkl` | Tagalog BPE | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |

## License and use restrictions

YAML `license: other` because the training text is Wikipedia-derived. Research use of these small decoder checkpoints; not a deployment certification.
