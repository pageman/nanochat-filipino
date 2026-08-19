---
license: other
library_name: nanochat
tags:
  - nanochat
  - bits-per-byte
  - tagalog
  - english
  - continual-pretraining
---

# Documentation-only release; complete A0/A1/A2/A3 checkpoint bundle pending

Until the four final `.pt` files, matching `meta_*.json`, and tokenizer files are on the Hub **together**, `pageman/nanochat-filipino-p2-en-then-tl` is a documentation pack, not a downloadable model.

# nanochat-filipino P2 (EN then TL)

## Identity and scope

**P2 only.** Not P1.1. **Not trained from** `pageman/nanochat-filipino-p1-fixed-d20-3x`. These weights are not an instruction-tuned, chat, or SFT model.

- AsPredicted [#306935](https://aspredicted.org/xa56bs.pdf)
- ResearchBox [8763](https://researchbox.org/8763)
- Run ID `p2-20260817T150944Z-de99f8a`
- nanochat pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`

Do not upload these files onto `pageman/nanochat-filipino-p1-fixed-d20-3x`.

## Research purpose

Controlled, preregistered continual-pretraining evidence on English retention after Tagalog continuation. Not a leaderboard, production deployment, or instruction-following claim.

## Branch map

All d20, same immutable English parent A0, same phase-2 budget \(N=294\), \(D=19{,}267{,}584\), fresh optimizer, English 32,768 BPE.

- **A0** frozen English parent (`model_005415.pt`)
- **A1** extra-English active control from A0
- **A2** Tagalog-only continuation from A0 (only tested branch)
- **A3** pre-frozen 50/50-document English–Tagalog mix from A0 (trade-off arm, not mitigation)

## Data provenance

WikiText-103 raw English train/val and a documented frozen copy of the P1.1 Tagalog train input. **Raw protected holdout text is not released.**

## Evaluation table (sealed)

Full validation (`val_bpb_full`), Gate U:

| Arm | English | Tagalog |
|---|---:|---:|
| Untrained | 3.246978 | — |
| A0 | 1.389990 | 4.917650 |
| A1 | 1.459675 | 5.054664 |
| A2 | 1.385684 | 1.171616 |
| A3 | 1.279433 | 1.528858 |

Primary contrasts: \(C_{EN}=EN(A2)-EN(A1)=-0.073991\); \(G_{TL}=TL(A2)-TL(A1)=-3.883048\).

A2-only **secondary** tests (Gate V): English WT103-raw test BPB 1.392015; P1.1 legacy Tagalog `test.jsonl` under P2 English BPE 1.160154. P1.1 native-BPE test BPB 1.164768 is **not** reused. A1/A3 were not tested.

## Interpretation boundary

The registered English-retention-cost pattern was **not observed**. The registered Tagalog-gain pattern **was observed** in this **one-seed** fixed apparatus. No significance test, confidence interval, population effect, or universal-language claim. Do not say “Tagalog improves English” in general. A3 is a 50/50-document trade-off arm (realized UTF-8 byte share English 0.961 / Tagalog 0.039; BPE-token share English 0.933 / Tagalog 0.067), not mitigation.

Question 8 descriptive statuses: exposure table published; A2 English trajectory not collected (A2 in-loop val was Tagalog); PTPP \(R_d=\mathrm{step}/294\) defined, English-BPB plot not made; fertility from Gate F (EN 4.603 / TL 2.574 bytes/token); P1.1-on-English OOD not run and not BWT.


## Checksums

Release only as a complete A0/A1/A2/A3 set. Filenames must keep the four branches distinct.

| File | Role | SHA-256 |
|---|---|---|
| `a0/p2-en0-d20-model_005415.pt` | A0 frozen English parent | `bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d` |
| `a1/p2-a1-extra-en-d20-model_000294.pt` | A1 extra-English child | `e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d` |
| `a2/p2-a2-tagalog-d20-model_000294.pt` | A2 Tagalog child | `2b01acf8fac0e8c783162582cbb384e8ce1c37795aae2f7dd4ae34c2a5c76026` |
| `a3/p2-a3-mix-d20-model_000294.pt` | A3 document-mix child | `d6c62bb793a57c7c23d98c5bd62ec36b41606234524f76855b4459d98c42b368` |
| `tokenizer.pkl` | English BPE | `946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6` |
| `token_bytes.pt` | token bytes | `5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42` |

Byte sizes must be recorded in the close-out manifest at upload time. Optimizer states and intermediate checkpoints are not part of the default release.

## License and use restrictions

YAML `license: other` matches the existing P2 Hub card. Research use of these small decoder checkpoints; not a deployment certification. Confirm data/code license compatibility before commercial reuse.

## Reproduction

Code: https://github.com/pageman/nanochat-filipino  
Protocol: `docs/papers/p2-cf-english/PROTOCOL-p2-en-then-tl.md`  
Environment: `scripts/p2/env.sh` / `scripts/p2/env.cuda.sh` only (never `scripts/p1/env.sh`).  
ResearchBox metadata deposit: https://researchbox.org/8763 (human upload may still be pending).
