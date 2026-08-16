---
language:
- tl
license: other
tags:
- nanochat
- tagalog
- filipino
- language-modeling
- bits-per-byte
datasets:
- linkanjarad/Wikitext-TL39
---

# Model card — `p1-fixed-d20-3x`

**Code:** https://github.com/pageman/nanochat-filipino

**Intended use:** research base language model for Tagalog Wikipedia-style text. Primary reported number is held-out bits-per-byte on WikiText-TL-39 (`reconstructed_article_70_15_15`).

**Out of scope:** chat, instruction following, safety filtering, official government or medical use, English CORE comparison, classification.

**Data:** public WikiText-TL-39 (`linkanjarad/Wikitext-TL39`, parquet SHA-256 `706d7064…`). Canonical text is source text with LF line endings only. Tokenizer is a 32,768 BPE trained on train documents only.

**Training:** nanochat commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`, depth 20, `T=2048`, `D_actual=19,267,584` tokens, Runpod A40, about 0.20 GPU-hours for this depth. No SFT.

**Eval:** registered primary is `val_bpb_full=1.172248` from official full-split `evaluate_bpb` ([results/full_validation.json](../../results/full_validation.json)). One `test_bpb=1.164768` after validation-only selection. One seed. Margin to depth 8 is 0.0069 BPB and is not interpreted as a ranking.

**Not the primary metric:** `val_bpb` inside Hub `meta_000294.json` (d20 `1.117213`) used `--eval-tokens=262144` during training. Do not rank depths from that loop slice. Mid-run d12 min `1.084991` was not selected.

**Carbon / compute:** one A40 at $0.44/hr; the four-depth seed-0 series was under 0.5 GPU-hours of training. Extra seeds and pilots are separate.

**Citations:** Cruz & Cheng (2019), arXiv:1907.00409; Karpathy nanochat; AsPredicted #306780. Study repository: https://github.com/pageman/nanochat-filipino

**License:** Hub field is `other`. These are research checkpoints trained on WikiText-TL-39 (Wikipedia-derived Tagalog text). This is not a legal clearance; check the source dataset and nanochat terms before reuse.
