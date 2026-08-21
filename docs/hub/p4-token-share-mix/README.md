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
  - post-p3
---

# nanochat-filipino P4 (token-share mix)

Matched-branch **research checkpoints**: frozen Tagalog parent **C0** plus children **C1**, **C2**, and **C3**. This is not a chat, instruction, or production model. **One seed.**

P4 is a matched branch study. Use the four files together; do not treat C3 as a standalone “bilingual nanochat.” **C3 is not P3 B3.**

## Identity and scope

**P4 only.** Not P1.1. Not P2. Not P3. **Not trained from** `pageman/nanochat-filipino-p1-fixed-d20-3x`, `pageman/nanochat-filipino-p2-en-then-tl`, or `pageman/nanochat-filipino-p3-tl-then-en`.

- AsPredicted [#307591](https://aspredicted.org/if84km.pdf)
- ResearchBox [8869](https://researchbox.org/8869) (FOR PEER REVIEW; not Make Public)
- AsCollected #2471 (`NANOCHAT-FILIPINO-P4`)
- GitHub audit trail: [pageman/nanochat-filipino](https://github.com/pageman/nanochat-filipino) (`results/p4/`, `docs/p4/`, `docs/hub/p4-token-share-mix/`)
- Run ID `p4-20260821T060032Z-92d63d4`
- nanochat pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`

Do not upload these files onto P1.1, P2, or P3 Hub repositories. Never present C3 alone as “the P4 model.”

## Files

Ship **C0+C1+C2+C3 together** with the carry-forward P3 tokenizer.

| Path | Role |
|---|---|
| [`c0/p4-c0-tl-d20-model_000294.pt`](c0/p4-c0-tl-d20-model_000294.pt) | C0 frozen Tagalog parent (step 294) |
| [`c0/checkpoint_identity.json`](c0/checkpoint_identity.json) | C0 identity (not trainer in-loop `val_bpb`) |
| [`c1/p4-c1-tl-d20-model_000294.pt`](c1/p4-c1-tl-d20-model_000294.pt) | C1 extra-Tagalog control |
| [`c1/checkpoint_identity.json`](c1/checkpoint_identity.json) | C1 identity |
| [`c2/p4-c2-en-d20-model_000294.pt`](c2/p4-c2-en-d20-model_000294.pt) | C2 pure-English continuation |
| [`c2/checkpoint_identity.json`](c2/checkpoint_identity.json) | C2 identity |
| [`c3/p4-c3-mix-d20-model_000294.pt`](c3/p4-c3-mix-d20-model_000294.pt) | C3 token-share mix (`q_{\mathrm{TL}}=0.50`) |
| [`c3/checkpoint_identity.json`](c3/checkpoint_identity.json) | C3 identity |
| [`tokenizer.pkl`](tokenizer.pkl) | Carry-forward P3 Tagalog 32,768 BPE |
| [`token_bytes.pt`](token_bytes.pt) | Token UTF-8 bytes |

Optimizer states are not in this release. Trainer `meta_*.json` was not copied off the GPU host; official BPB is [`evaluation/`](evaluation/), not in-loop `val_bpb`. Load with custom nanochat (`scripts.base_train` / `scripts/p4/evaluate_bpb.py`), not `transformers` `from_pretrained` as a causal LM chat pipeline.

## Research purpose

Controlled, preregistered token-share mixture trade-off after a **fresh** Tagalog parent. Not a confirmation of P3, not “P3 B3 fixed,” not a leaderboard, production deployment, or instruction-following claim.

## Branch map

All d20, same immutable Tagalog parent C0, same phase-2 budget \(N=294\), \(D=19{,}267{,}584\), fresh optimizer, carry-forward P3 Tagalog 32,768 BPE.

- **C0** frozen Tagalog parent (P0-T PASS)
- **C1** extra-Tagalog active control from C0
- **C2** English-only continuation from C0
- **C3** pre-frozen source-content token-share mix \(q_{\mathrm{TL}}=0.50\) from C0 (only tested branch)

## Data provenance

Frozen P1.1 WikiText-TL-39 train/val manifests and WikiText-103-raw English. **Raw protected holdout text is not released.**

## Evaluation table (sealed)

Full validation (`val_bpb_full`), Gate U. Machine-readable copies: [`evaluation/`](evaluation/) and GitHub `results/p4/`.

| Arm | Tagalog | English |
|---|---:|---:|
| C0 | (via P0-T) | 2.615645 |
| C1 | 0.785486 | 2.878106 |
| C2 | 2.517909 | 1.333106 |
| C3 | 1.201273 | 1.502828 |

Primary contrasts: \(R_{\mathrm{TL}}=\mathrm{TL}(C3)-\mathrm{TL}(C2)=-1.316637\) (**observed**); \(A_{\mathrm{EN}}=\mathrm{EN}(C3)-\mathrm{EN}(C1)=-1.375277\) (**observed**). C0 English is descriptive and excluded from the contrasts.

C3-only **secondary** tests (Gate V): English WT103-raw test BPB 1.513698; Tagalog holdout 1.202140. P1.1, P2, and P3 Gate V numbers are **not** reused. C1 and C2 were not tested.

## Interpretation boundary

Both registered co-primary patterns were **observed** in this **one-seed** fixed apparatus. No significance test, confidence interval, population effect, or universal-mixture claim. C3 is a token-share trade-off arm (descriptive UTF-8 byte share Tagalog ≈0.566 / English ≈0.434; Gate E), not a byte-balanced mix and not P3 B3.

## Checksums

See [`SHA256SUMS.txt`](SHA256SUMS.txt) and [`RELEASE_MANIFEST.json`](RELEASE_MANIFEST.json). Re-hash downloads before use.

| File | Role | SHA-256 |
|---|---|---|
| `c0/…model_000294.pt` | C0 | `34e069646be4158979809c023691188439047d6cbee08a141db432c78bcf02e2` |
| `c1/…model_000294.pt` | C1 | `87b9f55146de72dd6ae53598b9aea8d99079ff0f9492b7f9ea4fdce550664c55` |
| `c2/…model_000294.pt` | C2 | `0787aed0f13a0ab3ec144baf6802b144a18412780a2d00a64ca7adcb67a4a375` |
| `c3/…model_000294.pt` | C3 | `eef9a4e11c4840ac036d42c3bf4d87a2139ea1fa5809e1c756df2770fe0609f3` |
| `tokenizer.pkl` | Tagalog BPE | `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| `token_bytes.pt` | Token bytes | `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132` |

## License and use restrictions

YAML `license: other` because the training text is Wikipedia-derived. Research use of these small decoder checkpoints; not a deployment certification.
