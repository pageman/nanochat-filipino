# P4 AsPredicted draft (1–2 pages)

**Status:** Draft only. Not filed. No outcomes. No run ID.  
**Form sentence 1 (MUST):** P4 is designed after released P3 findings and after the P3 B3 document/byte-share ambiguity were known. It is a post-P3, prospectively preregistered exposure-matched mixture trade-off study. It does not amend AsPredicted #306780, #306935, or #307342.

## 1. Hypothesis / question

After a newly trained, P0-T-eligible Tagalog nanochat parent, under the same fixed phase-two model-visible token budget for every child, does a prospectively frozen English–Tagalog mixture with a locked share of P4-tokenizer-encoded tokens reduce held-out Tagalog BPB relative to pure English continuation while still improving held-out English BPB relative to extra Tagalog continuation?

C3 is a newly constructed P4 tokenizer-token-share-locked mixture. It is not P3 B3, which was a separate pre-frozen equal-document mixture.

## 2. Dependent variables

Full-split held-out validation bits-per-byte after the terminal checkpoint: mean token NLL / (ln 2 × mean UTF-8 bytes per evaluated token). Same frozen P4 Tagalog tokenizer and evaluator for all arms and both languages. In-loop trainer BPB is not confirmatory.

## 3. Conditions

From one immutable fresh P4 d20 parent (C0):

- **C1** extra Tagalog only (active control).  
- **C2** pure English only (pure-stream comparator).  
- **C3** pre-frozen token-share-locked EN/TL mix (intervention).

## 4. Parent and stop rule

P4 parent trained from random initialization on frozen WikiText-TL-39 train documents. Not P1.1/P2/P3 weights. P0-T: depths 8 and 20 must each beat untrained same-depth and Tagalog-train add-1 byte-unigram floors by ≥ δ_P0T on full Tagalog val before any child token. If either depth fails, do not run C1/C2/C3.

## 5. C3 treatment

Exposure clock: proportion of phase-two **model-visible tokens** after P4 Tagalog tokenizer encoding. Target \(q_{\mathrm{TL}}\) Tagalog tokens (unsigned at draft time; **sign before filing**; recommended 0.50). Deterministic construction from frozen train documents only; integer rounding rule filed; no tuning after fertility, loss, val BPB, samples, or tests. Byte share and document share are descriptive. P4 does not claim byte balancing.

## 6. Budget and checkpoints

Context T=2048; batch B=65,536; phase-two N=294 steps (D=19,267,584) for all children unless the PDF names another integer **before Gate A**. Fresh optimizer; no resume; terminal checkpoint only; no mid-run selection.

## 7. Co-primary contrasts and threshold

\(R_{\mathrm{TL}}=\mathrm{TL}(C3)-\mathrm{TL}(C2)\le -\delta\)  
\(A_{\mathrm{EN}}=\mathrm{EN}(C3)-\mathrm{EN}(C1)\le -\delta\)  

δ unsigned at draft; **recommended 0.01 BPB** as practical-significance and confirmatory boundary (carry-forward family; not tuned to P3 magnitudes). Sign before filing. Both / only-R / only-A / neither use the four predeclared conclusion sentences. No composite score. “Mitigation” not in title/abstract until after unblinding, and then only if both criteria met, narrowly.

## 8. Data, split, tokenizer, exclusions

Frozen P1.1 Tagalog 70/15/15 manifests and P3-frozen WikiText-103-raw splits. Tests unmounted from training. Recommended tokenizer: carry-forward P3 Tagalog 32,768 BPE (hash filed); alternatively a fully specified fresh tok_train — choose one before filing. No ClimbMix/FineWeb/instruction data. No P3 B3 as a live arm.

## 9. Validation before test

Gate U seals six child validation cells (C1/C2/C3 × TL/EN) with test_access=0. Optional descriptive C0 English val if filed.

## 10. Optional test (recommended Policy A)

One authorized C3-only event on named English WT103-raw test and Tagalog P1.1 test.jsonl. C1 and C2 never tested. test_access becomes 1. Secondary/descriptive. Alternative: no test (Policy B). Policy C (test more than C3) not used unless justified before filing.

## 11. Post-P3 disclosure

Operators may know P3. They must not see P4 BPB until Gate X. P3 numbers are not P4 calibration targets.

## 12. No-amendment

This study does not amend #306780, #306935, #307342, or ResearchBox #8735/#8763/#8834. One seed; no population claim.

**Related studies checkboxes:** overlapping observations with #306780, #306935, and #307342 (not independent of them).
