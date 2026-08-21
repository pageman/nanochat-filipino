# P4 pre-filing addendum draft (embed SHA in the AsPredicted PDF)

**Status:** UNSIGNED. Not filed. Does **not** authorize Gate A, C3 construction, tokenizer copy, smoke, or GPU rental.  
**Role after signature:** This is the **one** scientific addendum whose SHA-256 **MUST** be printed in the filed P4 AsPredicted PDF. After filing, only non-scientific operational clarifications (paths, host IDs, lockbox mechanics) may be dated. A later “pre-Gate-A addendum” **MUST NOT** change any quantity in this file.  
**Does not change:** the P4 question, C0/C1/C2/C3 sibling structure, token-share clock, co-primary contrasts, U-before-V, C3-only Policy A, Hub-together, or “C3 is not P3 B3.”

Embed in the PDF:

```text
Protocol master SHA-256: <hash PROTOCOL-p4-token-share-mix.md>
Gate bible SHA-256:      <hash PROTOCOL-p4-GATES-EXHAUSTIVE.md>
This addendum SHA-256:   <hash this file after last pre-file edit>
nanochat pin:            92d63d4e8bb4df75c3b71618f31ddde2378b2bcd
```

---

## Signed choices (copy into the PDF; recommended column becomes FILED when you file)

| ID | Choice | Value to file |
|---|---|---|
| F4-01 | Identity | P4-C3-TOKEN-SHARE; post-P3; does not amend #306780/#306935/#307342 |
| F4-02 | Tokenizer | **Carry-forward** both artifacts: `tokenizer.pkl` `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8`; `token_bytes.pt` `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132`. If either hash cannot be verified, **do not** use carry-forward. |
| F4-03 | \(q_{\mathrm{TL}}\) | **0.50 Tagalog source-content tokens** under the carried-forward P3 tokenizer: encode each eligible **train** document with **no BOS, no padding, no pack, no crop**, then concatenate. Trainer packing / BOS-at-pack **MUST NOT** redefine this quota. Packed-train language-origin audit must still match \(T_{\mathrm{TL}}^{\star}=T_{\mathrm{EN}}^{\star}=9{,}633{,}792\). Signed at Gate 0, **before Gate F**. Not chosen from fertility, loss, BPB, samples, or P3 magnitudes. **Not** byte balance. |
| F4-04 | \(\delta\), \(\delta_{\mathrm{P0T}}\) | **0.01** BPB; \(\delta_{\mathrm{P0T}}=\delta\); equality at \(-\delta\) **counts**; six decimals |
| F4-05 / F4-19 | PRNG + seeds | See seed table below. Library: **Python 3 `random.Random`**. Exact CPython version string **MUST** be recorded in `p4_mix_manifest.json` at Gate E before mix construction (do not invent a version in this draft). |
| F4-06 | Interleave | Deterministic **fine-grained blocks**, \(K_{\mathrm{blk}}=2048\); not whole-document; not randomly mixed. Final residual block may be shorter; record length. Prefix \(\varepsilon_{\mathrm{path}}=K_{\mathrm{blk}}/D_{\mathrm{phase2}}\). |
| F4-07 | Rounding | Round-half-to-even on TL target; English residual so sum \(=D_{\mathrm{phase2}}\) |
| F4-08 | Quota failure | **Exact integer match** on the **final packed C3 train stream consumed by the trainer**, excluding any val shard. 0 token slack when \(D q\) is integer (\(9{,}633{,}792\) / \(9{,}633{,}792\) at \(q=0.50\), \(D=19{,}267{,}584\)). Pre-step rebuild only on predeclared integrity failure with **no** outcomes; new manifest identity. After C3 training starts: stop. |
| F4-09 | Last shard | C3 **train** shards = mix construction. `val.parquet` = byte-identical C2 English val pack. **`val.parquet` is a trainer-interface artifact only.** It is **not** confirmatory; it **cannot** set a gate; in-loop metrics from it stay in lockbox; official outcomes are frozen EN/TL split JSONL evaluations at U. |
| F4-10 | Test | **Policy A**: one C3-only event after U. Holdouts: EN test `2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e`; TL test `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf`. C1/C2 never tested. Tests descriptive; **no** test-set \(R_{\mathrm{TL}}\)/\(A_{\mathrm{EN}}\). |
| F4-11 | Budget/depth | d8 **eligibility only**; **d20 = only C0**; \(T=2048\); \(B=65536\); \(N_{\mathrm{TL0}}=N=294\); \(D_{\mathrm{phase2}}=19{,}267{,}584\). No d8 fallback after outcomes. Gate G **MUST** confirm \(N_{\mathrm{TL0}}=294\) under carry-forward tokenizer. |
| F4-12 | Optimizer | Fresh Muon+AdamW; `load_optimizer=False`; `--resume-from-step=-1`; peak LR \(=0.3\times\) parent; warmup 14 |
| F4-13 | CUDA class | Authoritative confirmatory: **NVIDIA CUDA**, recommended **A40 48 GB**. File a class, not a live pod. Other NVIDIA class: **only if named in this PDF**; else dated deviation **before Gate H**; no bit-identical claim. **No** numeric “close enough.” MPS/CPU/TPU = protocol stop for H, I, P0-T, R–T, U, V. |
| F4-14 | Deposit | New ResearchBox (not #8834); new AsCollected project/version |
| F4-15 | C0 English val | **Yes — collect once at U**, descriptive only; excluded from \(R_{\mathrm{TL}}\) and \(A_{\mathrm{EN}}\) |
| F4-15b | Child order | **Serial** R → S → T |
| F4-16–18 | Roles / overlapping / grammar | As master protocol |
| F4-20 | Terminal save | Pin `92d63d4`: `--save-every=-1` writes exactly one `model_{N:06d}.pt` at the last step (verified on this pin by P3). P4 wrappers **MUST** refuse a missing terminal file. No contingent alternative. |
| F4-21 | P0-T evaluator | CUDA-only for **status**. CPU eval, if any, is diagnostic and **MUST NOT** set PASS/BLOCKED. Untrained seed **0** (`torch.manual_seed` + `cuda.manual_seed`). `--device-batch-size=8`. Packing `bos_bestfit_buffer1000_one_pass_no_wrap`; stride `non_overlapping_T_official_bos_bestfit`; \(T=2048\). Byte-unigram: add-1 on Tagalog **train UTF-8**, score Tagalog **val UTF-8**. Equality: floor pass iff \((\mathrm{floor}-\mathrm{trained})\ge\delta_{\mathrm{P0T}}\). Evaluator script SHA frozen at Gate A. |
| F4-22 | Split identity | Official P4 confirmatory JSONLs are **byte-identical copies** of the six named frozen files. Hash mismatch = **stop**. **No** cleaning/re-emission of official P4 inputs. |

---

## F4-19 random-seed allocation table

| Process | Seed | PRNG | Consumed by |
|---|---:|---|---|
| Parent d8 init | 0 (nanochat `compute_init` / torch 42 family on this pin) | pin default | Gate I d8 |
| Parent d20 init | **same as d8** (not a second draw; depth is not selected by seed) | pin default | Gate I d20 |
| Child C1/C2/C3 init | Fresh weights from C0; **no** new model-init seed; optimizer freshly constructed | n/a | Gates R–T |
| Untrained P0-T floor (d8 and d20) | **0** | `torch.manual_seed` + `torch.cuda.manual_seed` | Gate P0-T |
| C3 English document order | **42** | Python `random.Random` | Gate E |
| C3 Tagalog document order | **42** | same instance class, independent `Random(42)` per language list | Gate E |
| C3 block interleave | **42** | `random.Random(42)` if the schedule needs a tie-break; otherwise fully deterministic alternation EN/TL of \(K_{\mathrm{blk}}\) | Gate E |
| Gate H smoke | **0** if the trainer seeds; smoke is nonconfirmatory | pin default | Gate H |
| Fresh `tok_train` | **not used** under carry-forward. If that fork is later selected, this addendum is invalid until a tok seed is filed. | — | — |
| Packed-stream consumption | **no extra shuffle**; lexicographic shard order; **one pass**; **no wrap/revisit** before \(N\times B\) tokens | n/a | Gates R–T trainer |

SHA-sorted-then-seed-shuffled document lists: sort by SHA-256 of raw document text, then `Random(42).shuffle`.

---

## Packed C3 train-stream audit (Gate E pass)

On the **exact final packed C3 train shards** (exclude `val.parquet`):

1. Decode each packed token’s **language origin** from the construction ledger (EN vs TL block).  
2. Sum origin tokens; require `achieved_tl == 9633792` and `achieved_en == 9633792` at filed \(q=0.50\), \(D=19267584\).  
3. Prove the trainer will consume the first \(N\times B\) tokens in shard order **without wrap**.  
4. Store `language_origin_mask_sha256` (or block-schedule digest) beside `full_stream_sha256`.  
5. Record revisits, truncation offsets, unique-document proportions, and whether a document boundary crosses a training block — **descriptive**, not outcomes.

---

## What this addendum does not do

It does not add a C4 arm, change co-primary contrasts, allow fertility to pick \(q_{\mathrm{TL}}\), allow CPU P0-T to set status, or treat C3 `val.parquet` as a DV.
