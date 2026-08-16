# Confirmatory results — AsPredicted #306780

**Study:** NANOCHAT-FILIPINO P1.1 — WikiText-TL-39 fixed-budget depth vs held-out Tagalog BPB  
**Registration:** https://aspredicted.org/6r6v4v.pdf  
**PDF SHA-256:** `a34f119df557d2e763aa154e02b76b0ebcbcba1f3fb32c3219d85ae6395cc5ca`  
**RUN_ID:** `p1-20260816T025911Z-0067a57`  
**Split label (every caption):** `reconstructed_article_70_15_15`  
**This file does not amend AsPredicted #306780.**

Statement classes are marked: **Fact** (verified execution), **Confirmatory** (registered analysis), **Secondary** (not used to pick `D*`), **Limitation**.

---

## 1. Registered question and prediction

**Confirmatory.** Does increasing nanochat depth from 8 to 20 reduce held-out Tagalog bits-per-byte when every depth sees `D_3x = 3 * T_train` on WikiText-TL-39?

Registered prediction: validation BPB falls from depth 8 to a minimum in {8, 12, 16, 20}, then flattens, or the train–validation BPB gap widens. We will not claim “deeper is always better.” This is not a CORE, chat, or classification test.

---

## 2. Primary table (one seed, final step 294)

**Confirmatory.** Primary DV is `val_bpb_full` on the full packed validation split after training, not the 262,144-token in-training `--eval-tokens` stream. Evaluator: official `evaluate_bpb` (mean token NLL / (ln 2 × UTF-8 bytes), special tokens excluded) with one-pass BOS-bestfit packing, `T=2048`, `device-batch-size=8`. Checkpoint rule: `final_checkpoint_at_fixed_budget`. Selection rule: `exact_minimum_final_val_bpb_full`.

| Run | D | Seed | `P_total` | `P_scaling` | `R_d` | `T_seen` (`D_actual`) | `val_bpb_full` | `train_bpb_full` | val−train gap | untrained val | unigram val | Hours | GPU |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `p1-fixed-d8-3x` | 8 | 0 (torch 42) | 125,829,354 | 41,943,232 | 0.457834 | 19,267,584 | 1.179135 | 0.836702 | 0.342432 | 3.289109 | 4.453225 | 0.027 | A40 |
| `p1-fixed-d12-3x` | 12 | 0 (torch 42) | 286,261,730 | 110,100,912 | 0.174413 | 19,267,584 | 1.180824 | 0.528818 | 0.652006 | 3.289358 | 4.453225 | 0.061 | A40 |
| `p1-fixed-d16-3x` | 16 | 0 (torch 42) | 536,871,738 | 234,881,792 | 0.081756 | 19,267,584 | 1.195546 | 0.458045 | 0.737501 | 3.289354 | 4.453225 | 0.119 | A40 |
| `p1-fixed-d20-3x` | 20 | 0 (torch 42) | 896,533,746 | 435,160,240 | 0.044129 | 19,267,584 | **1.172248** | 0.672393 | 0.499855 | 3.289106 | 4.453225 | 0.204 | A40 |

Shared **Fact** row: nanochat `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; tokenizer SHA `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8`; `token_bytes.pt` SHA `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132`; `T=2048`; `B=65536`; `N=294`; `D_3x=19,203,039`; host Runpod Secure A40 48 GB, EU-SE-1, pod `68bei7d3vx4krc`; CORE off.

All four trained `val_bpb_full` values are strictly below both baselines (**Confirmatory** Q5).

### `D*` and the 0.01 rule

**Confirmatory.** `D* = 20` by exact numerical minimum (`val_bpb_full = 1.172248`). Margin to d8 is **0.006887 BPB**; to d12 is **0.008576 BPB**. With one seed, gaps `< 0.01` BPB are not interpreted as a depth ranking. d20 and d8 are practically indistinguishable. Test BPB was not used to break the gap.

### Secondary confirmatory DV

**Confirmatory.** One `test_bpb` after validation-only selection, same formula/packing/`T=2048`:

| Model | `test_bpb` | Used to choose `D*`? | `test_read_events` |
|---|---:|---|---:|
| `p1-fixed-d20-3x` only | 1.164768 | no | 1 |

Test SHA-256 `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf`. No `test_bpb` is reported for d8/d12/d16.

---

## 3. Prediction outcome

**Confirmatory.** Numerical minimum is at depth 20. The series does **not** show a clean fall-then-flatten across 8→12→16→20: val BPB rises from 8 to 16, then d20 is lowest by a sub-0.01 margin over d8. The train–val gap widens from 8 to 16 (0.342 → 0.738) and is 0.500 at d20.

Falsification (“larger depths keep improving held-out BPB at `D_3x` with no increase in the train–validation gap”) did **not** occur. We do **not** claim “deeper is always better.”

---

## 4. Q6 exclusions (negative checklist)

**Fact.** No confirmatory run was excluded.

- [x] No NaN/Inf `val_bpb`
- [x] No ClimbMix or non-WikiText-TL-39 shards in the training directory
- [x] Test file was not in the active training directory during Gate I
- [x] Validation/test text was not used to train the tokenizer
- [x] `--target-param-data-ratio` was never `-1`
- [x] Depth and `T=2048` were not changed after OOM
- [x] No depth was dropped because BPB looked bad
- [x] d4 smoke is not a confirmatory observation

---

## 5. Secondary (not used to pick `D*` or the tokenizer)

**Secondary.**

| Item | Result |
|---|---|
| Tagalog 32768 vs GPT-2 bytes/token on val | 4.531 vs 2.758 (Gate F fertility) |
| Native ratio=12 vs `D_3x` corpus passes | `R_d` at `D_3x` is 0.458/0.174/0.082/0.044; a ratio=12 family would see the small corpus many more times and is not this experiment |
| gzip -9 on val UTF-8 bytes | 2.739 bits/byte (compressor, not a causal LM). Trained LMs beat gzip on this in-domain dump |
| d8/d12 `D_1x` pilots | d8 `val_bpb_full=1.420188`; d12 `1.428635` (step 98). Both worse than the matching `D_3x` seed-0 vals. Not used to pick `D*` |
| Extra seeds 1 and 2 at d8 and d12 | Q7 complete on val only. d8 mean 1.190892 (sample SD 0.010318); d12 mean 1.187442 (sample SD 0.008792). Test not read. Does not reopen `D*` |
| Document-level val bootstrap (1000) | Different packing than `val_bpb_full` (per-doc non-overlap). All four 95% CIs overlap (~1.23–1.39). Not used to choose `D*` |

---

## 6. Limitations

**Limitation.**

- Original 2019 train/val/test files were not recovered. Split is reconstructed-article 70/15/15.
- One seed for the four-depth comparison. Sub-0.01 gaps are not a ranking.
- WikiText-TL-39 is 2019 Tagalog Wikipedia, not general Filipino web text.
- BOS-bestfit packing crops long documents (~35% token crop is the nanochat default).
- No chat, SFT, instruction following, CORE, or classification in this study.
- Packed `val_bpb_full` scores 5,868,797 target bytes (1,286,864 tokens); raw val UTF-8 is 6,771,275 bytes. Unigram uses the raw byte stream by registration.

---

## 6b. Optional document-level bootstrap (val only)

**Secondary.** Per-document non-overlapping `T=2048` blocks, 1000 resamples, seed 0. This is **not** `val_bpb_full` (BOS-bestfit packed). CIs are for the document-sum metric only.

| Depth | document-sum BPB | bootstrap mean | 95% CI |
|---:|---:|---:|---|
| 8 | 1.307171 | 1.305728 | 1.235–1.378 |
| 12 | 1.315718 | 1.314191 | 1.242–1.391 |
| 16 | 1.305280 | 1.303591 | 1.232–1.379 |
| 20 | 1.317213 | 1.315260 | 1.246–1.390 |

All four intervals overlap. This does not support a one-seed depth ranking and does not change `D*`.

---

## 7. Qualitative samples

**Secondary / not a metric.** Protocol §16.7: three fixed prompts, temperature 0.8, top-p 0.95, 100 tokens, five continuations, decoding seeds 0 and 1, on `D*` only. 30 strings written to `artifacts/p1/p1-20260816T025911Z-0067a57/gate-j/samples_d20.json`. Native-speaker 1–5 ratings: **no rater available; scores not invented.** Continuations are Tagalog-Wikipedia-flavored and often incoherent; they are not a metric and do not select `D*`.

---

## 8. What this study is not

CORE, chat/SFT, dengue, hate speech, NewsPH-NLI, SEA-HELM, OSCAR, TLUnified, ClimbMix, clean-data ablation, Moses detokenization as canonical text, d24, `D_10x`, or a native `--target-param-data-ratio=12` equal-exposure claim.
