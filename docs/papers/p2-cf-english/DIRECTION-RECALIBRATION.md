# Paper 2 direction recalibration

**Date:** 16 August 2026  
**Does not amend AsPredicted #306780.**  
**Does not change P1.1 scores, weights, or claims.**

P1.1 stays the pure Tagalog base (WikiText-TL-39, unsupervised nanochat, depth-dial only). Rated A/P/C/L/N = 5/5/5/5/5. Paper 2 must not dilute that.

## What Paper 2 is actually asking

Not: a Tagalog-only model “forgot English.” It never had English.

Yes: **an English-pretrained nanochat, then continued on WikiText-TL-39, forgets English while (or without) learning Filipino.**

WikiText-TL-39 is the **Filipino tuning corpus**, not a model that was “pretrained in English.” The English pretraining corpus is WikiText-103 raw (same WikiText family as Cruz & Cheng’s Tagalog analogue).

| Question | Instrument |
|---|---|
| Was the parent really English-pretrained? | **Provenance battery P0** before any Tagalog token |
| Did it forget English? | English `val_bpb_full` after Tagalog continuation minus matched extra-English continuation |
| Did it learn Filipino? | Tagalog `val_bpb_full` after continuation, compared to P1.1 from-scratch ceiling |

Both languages are scored with official nanochat `evaluate_bpb` (bits per UTF-8 byte). CORE/chat/SFT stay out so P stays 5.

## nanochat-only contract (non-negotiable)

Paper 2 is the same stack as Paper 1, twice: English WikiText then Tagalog WikiText. No other trainer.

| Step | nanochat entrypoint | Pin |
|---|---|---|
| English BPE | `scripts.tok_train` on WT103-raw **train only** | commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` |
| English pretrain EN0 | `scripts.base_train` `--depth` `{8,20}` `--max-seq-len=2048` | same clone + `NANOCHAT_DATA_DIR` hook |
| Tagalog continuation A2 | `scripts.base_train` loading EN0 `model_*.pt`, data = P1.1 train shards | same |
| Extra-English A1 / joint A3 | `scripts.base_train` | same |
| English BPB | official `evaluate_bpb` via a copy of `scripts/p1/gate_j_full_bpb.py` | same packing, `T=2048` |
| Tagalog BPB | same evaluator, P1.1 val JSONL | same |
| P1.1 negative control | already-trained nanochat d20, English UTF-8 encoded with **P1.1** Tagalog BPE | do not retrain P1.1 |

**Allowed data-dir hook:** `patches/nanochat-NANOCHAT_DATA_DIR.patch` only. No edits to attention, loss, or optimizer “to make CF work.”

**Forbidden:** Hugging Face `Trainer` / `from_pretrained` as the LM; llama.cpp; a second GitHub LM; `python -m nanochat.dataset` (ClimbMix); CORE (`--core-metric-every=-1`); SFT/chat scripts; a new tokenizer after seeing BPB; loading P1.1 `model_000294.pt` as the English parent.

GitHub `p2-en-then-tl` vendors or submodules that exact nanochat commit. Hub folders are nanochat `model_*.pt` + `meta_*.pt` JSON, not `safetensors` transformers weights.

## Why P1.1 Hub weights are not the English parent

`pageman/nanochat-filipino-p1-fixed-d20-3x` is Tagalog-from-scratch. Using it as the CF parent answers the opposite question (Tagalog retention under English data). That design is **retired** for Paper 2.

P1.1 weights remain:

1. **Tagalog acquisition ceiling** (Table 2 `val_bpb_full`).
2. **English negative control**: the same English val set, encoded with the P1.1 Tagalog BPE. A true English parent must beat this control by a predeclared margin before phase 2 starts.
3. Frozen Tagalog split + evaluator (Filipino benchmark).

## Target A/P/C/L/N for Paper 2

| Axis | Target | How |
|---|---|---|
| A Alignment | 5 | WikiText-103 (English WikiText) → WikiText-TL-39 (Cheng 2019 analogue). Same family, two languages. |
| P Purity | 5 | Unsupervised nanochat LM only. Dual **BPB**, not chat, not CORE as primary. |
| C Continuity | 5 | Same pin `92d63d4`, `T=2048`, equal-exposure arithmetic, P1.1 split/evaluator for Tagalog. |
| L Lock | 5 | New AsPredicted. New GitHub. New Hub. P1.1 read-only. |
| N Novelty | 5 | Provenance test + dual BPB CF on this stack, not a generic EWC demo. |

## Pipeline (replaces the old A2 = English continuation grid)

```
P2-EN0   Train English nanochat on WT103-raw (English-only 32,768 BPE,
         depths 8 and 20 minimum, D_3x on English T_train, T=2048).
P2-P0    Provenance battery. No Tagalog tokens yet.
P2-A0    Freeze EN parent; score English val + Tagalog val (befores).
P2-A1    Extra English continuation, D_phase2 (drift control).
P2-A2    Tagalog continuation on frozen P1.1 train split, D_phase2  ← CF intervention
P2-A3    Joint 50/50 documents (retention ceiling).
```

`D_phase2 = 294 × 65536 = 19,267,584` tokens counted in the **English-parent BPE** (phase-2 unit), unless the new PDF names English `D_3x` instead. Pick one in the PDF and do not switch after seeing BPB.

**Primary contrast** \(C_{\mathrm{en}} =\) English `val_bpb_full`(A2) − English `val_bpb_full`(A1).  
Positive \(C_{\mathrm{en}}\) = Tagalog data hurt English more than more English did.

**Acquisition** \(A_{\mathrm{tl}} =\) Tagalog `val_bpb_full`(A2) versus P1.1 Table 2 (from-scratch ceiling) and versus A0 (English parent before Tagalog).

BPB remains comparable across tokenizers because it is bits per UTF-8 byte. Do not mix tokenizers inside one training run.

## Provenance battery P0 (must pass before A2)

All of these use the **English val** split, frozen, no Tagalog train text.

1. English `val_bpb_full`(EN0) is finite and **strictly below** same-depth untrained.
2. English `val_bpb_full`(EN0) is **strictly below** P1.1 d20 scored on the same English UTF-8 (P1.1 Tagalog BPE). Predeclare margin ≥ 0.01 BPB or fail provenance.
3. Tagalog `val_bpb_full`(EN0) is **worse** than P1.1 d20 on Tagalog val (has not yet learned Filipino).
4. English-train BPE fertility on English val is recorded; on Tagalog val it will look shredded. That is expected, not a reason to retrain BPE.
5. Hashes: English parquet/raw file, English tokenizer, EN0 checkpoint, train command. Train log shows WikiText-103 only.

If P0 fails, the run is not an English-pretrained parent. Do not continue to A2.

## Dual benchmarks (confirmatory)

| Language | Split | When | Role |
|---|---|---|---|
| English | WT103-raw val, article-hash 70/15/15 | A0, A1, A2, A3 | Retention / forgetting |
| Filipino | P1.1 `reconstructed_article_70_15_15` val | A0, A2, A3 (A1 optional) | Acquisition |
| English test | WT103-raw test | Once, after English val $C_{\mathrm{en}}$ sealed | Secondary |
| Filipino test | P1.1 test JSONL | At most once, after Tagalog val sealed; do not spend P1.1’s historical `test_bpb` as an after-Tagalog number | Secondary |

Loop `eval-tokens=262144` stays diagnostic.

## New repos (do not write onto P1.1)

| | Name |
|---|---|
| GitHub | `pageman/nanochat-filipino-p2-en-then-tl` |
| Hugging Face | `pageman/nanochat-filipino-p2-en-then-tl` |
| Hub layout | `en0/d8/` `en0/d20/` (parents) · `a1/` `a2/` `a3/` per depth · never `p1-fixed-d20-3x` |
| Parent citation | ResearchGate 412302216 · github.com/pageman/nanochat-filipino · Hub p1-fixed-d20-3x as **reference**, not parent weights |

## Retired (old Paper 2 draft)

Tagalog P1.1 checkpoint as CF parent; A2 = English continuation; “forgot Tagalog because it learned English”; EN0 as a post-hoc English-from-scratch after a Tagalog parent. Those documents remain in `docs/papers/p2-cf-english/` as superseded drafts until rewritten.

## Critical path

**Gate-level protocol (authoritative for execution):** [`PROTOCOL-p2-en-then-tl.md`](PROTOCOL-p2-en-then-tl.md).

File **new AsPredicted first** (Gate 0). Then Mac Gates A–G → CUDA Gate H smoke → Gate I EN0 → P0 → A0/A1/A2/A3 → val seal \(C_{\mathrm{en}}\) at P2 test-count 0 → one P2 test touch → new GitHub/Hub/ResearchBox close-out.

Do **not** start confirmatory EN0 `val_bpb_full` before the PDF. Do **not** amend #306780. EWC/replay grid is confirmatory only if named in that PDF. Design B (Cebuano) still later.
