# P5 pre-filing addendum draft (embed SHA in the AsPredicted PDF)

**Status:** UNSIGNED. Not filed. Does **not** authorize Gate A, tokenizer copy, stream reuse, smoke, or GPU rental.  
**Sibling of:** `P5-GATES-EXHAUSTIVE-PLAN.md` (Downloads copy). If they conflict, **filed PDF ≫ this addendum ≫ the plan**.  
**Role after signature:** the **one** scientific addendum whose SHA-256 **MUST** be printed in the filed P5 AsPredicted PDF.

Embed in the PDF:

```text
P5 gate-plan SHA-256:  d51115aade9c0b1fb8698eaa33540db2d75b2b27765aaaad1bf14b13b0132092
This addendum SHA-256: 839fcaa3dd6e94bd9546df4880a5892851a54ea31743cb0359adc8faebbe9258
nanochat pin:          92d63d4e8bb4df75c3b71618f31ddde2378b2bcd
P4 mix-manifest SHA:   f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107
```

---

## Signed choices (copy into the PDF)

| ID | Choice | Value to file |
|---|---|---|
| F5-01 | Identity | `P5-P4-MULTI-SEED`; post-P4; does not amend #306780/#306935/#307342/**#307591** |
| F5-02 | Tokenizer | Carry-forward `tokenizer.pkl` `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` and `token_bytes.pt` `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132` |
| F5-03 | \(q_{\mathrm{TL}}\) | **0.50** source-content tokens (no BOS/pad/pack/crop). Not retuned from P4 magnitudes. |
| F5-04 | \(\delta\), \(\delta_{\mathrm{P0T}}\) | **0.01** BPB; equality counts; six decimals |
| F5-05 | C3 | **Reuse P4 packed stream by SHA.** Quotas 9,633,792 / 9,633,792. Doc-order/interleave seed **42**. Rebuild only if byte-identical. For each P5 C3 run, trainer-consumed packed **train** shard SHA-256 and `language_origin_mask_sha256` must match the P4 freeze below; matching source JSONLs or the mix-manifest alone is insufficient. |
| F5-06 | Panel | \(K=3\); parent-init seeds **1, 2, 3** in that order. P4 seed **0** is historical only. |
| F5-07 | Unblinding | **One panel Gate X** after every seed's V or ineligible-parent stop. No seed-level X. |
| F5-08 | Early-stop | **Forbidden.** No replacement seed. No “stop if the first two recur.” |
| F5-09 | Test | **One C3-only secondary test event per eligible predeclared seed** (zero to three total P5 test events; not one test for the whole panel). Each test is post-seal, secondary, descriptive, and excluded from seed classification and the panel count table. Holdouts EN `2bccabc0…` / TL `3bd19345…`. |
| F5-10 | Budget | d8 eligibility only; d20 = \(C0_s\); \(T=2048\); \(B=65536\); \(N=294\); \(D=19{,}267{,}584\) |
| F5-11 | Optimizer | Fresh Muon+AdamW; `load_optimizer=False`; `--resume-from-step=-1`; peak LR \(=0.3\times\) parent; warmup 14 |
| F5-12 | CUDA host | **NVIDIA A40 48 GB**, CUDA **12.8**, torch **2.9.1+cu128**, container `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404`. File this contract; another NVIDIA class only if named here with dated deviation before H. |
| F5-13 | C0 EN val | Once per seed at U_s; descriptive |
| F5-14 | Order | Within seed: R→S→T→U→V. Across seeds: 1→2→3. Continue through all filed seeds regardless of prior safe status. |
| F5-15 | Related | Overlapping #306780, #306935, #307342, **#307591** |
| F5-16 | Grammar | Per-seed four-way + panel count table. No CI/\(p\). Not a population estimate. |
| F5-17 | Hub | New ID. C0+C1+C2+C3 together **per seed** (or all eligible seeds together). Never C3 alone. Never the P4 Hub ID. |
| F5-18 | Terminal save | `--save-every=-1` → `model_000294.pt` |
| F5-19 | P0-T | CUDA-only status. **Seed-matched untrained floor:** for each \(s\), compare the d8/d20 parent against untrained same-depth models initialized with the **same** filed seed \(s\), plus the shared Tagalog train-fitted add-one byte-unigram floor. Same packing as P4 F4-21. |
| F5-20 | Splits | Byte-identical P4 JSONLs; hash mismatch = panel-level protocol stop |
| F5-21 | Deposit | New ResearchBox (not #8869); new AsCollected |
| F5-22 | Parent-init mechanism | P5-owned parent launch wrapper sets `torch.manual_seed(s)` and `torch.cuda.manual_seed(s)` immediately before `GPT.init_weights()` for parent d8 and d20; constructs the official GPT model only after that Torch CPU/CUDA RNG state is set, or reinitializes every trainable GPT parameter through the pinned `GPT.init_weights()` call after that state is set; records wrapper SHA and SHA-256 of the serialized initial model state before parent training. Python/NumPy wrapper/preprocessing RNG uses fixed seed **424242** (recorded). C3 interleave/doc-order seed **42** is separate and fixed. Model initialization is the only factor varied by \(s\). |
| F5-23 | P5 scripts | Use `scripts/p5/env.sh`, `scripts/p5/env.cuda.sh`, `scripts/p5/evaluate_bpb.py`, `scripts/p5/continue_from_frozen.py`, and P5 gate wrappers only. **Never** source `scripts/p4/*` or `scripts/p1/p2/p3/*` at runtime. Script SHAs frozen at Gate A. |
| F5-24 | Lockbox scalars | Before panel Gate X, permitted P0-T output is only `PASS`, `BLOCKED`, or `TECHNICAL_STOP`. Gate U/V scalar JSON, evaluator stdout/stderr, and test reports go directly to the P5 lockbox and are not displayed, copied into public run cards, or inspected. `test_access[s]` is a safe count, not a score disclosure. |
| F5-25 | Protocol-stop scope | **Panel-level protocol stop:** material integrity breach involving shared inputs, tokenizer, evaluator, packed C3 treatment, or test isolation — no remaining seed runs under the compromised registry. **Seed-level protocol stop:** breach demonstrably isolated to an unexecuted seed-specific staging/output path — no result assigned to that seed, no replacement seed, remaining seeds continue only if the shared registry is independently re-verified unchanged. |

---

## P4 C3 trainer-input freeze (F5-05)

| Artifact | SHA-256 |
|---|---|
| C3 train shard 0 | `249e2c5e9d06bf17fe14e03c02e622c9e68d90ba337e1e6e33c237fc723252f5` |
| C3 train shard 1 | `d24fe7f933abeb38b277b099385518718d2d57e330e5f9b5fd8b1a534e43444e` |
| C3 train shard 2 | `a56a729a0e3c7fd2d1e2e99236a4225bf9a86e55d6d97153063de9d6455fa523` |
| C3 train shard 3 | `4adbf8f9afcc9870f46f6298ac22f3691ec073d2f452f73aa65322e3ff6331de` |
| `language_origin_mask_sha256` | `140e174a427a7ddf2126553c53352ec049f72fbed475e2404cd4ef122b309c46` |
| Mix-manifest (reference) | `f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107` |

---

## F5 seed allocation table

| Process | Seed | Notes |
|---|---:|---|
| P4 historical parent (not a P5 cell) | 0 | Already released |
| P5 parent d8/d20 init | **s ∈ {1,2,3}** | Same \(s\) for both depths; set by F5-22 wrapper before `init_weights()` |
| Child init | n/a | Load \(C0_s\); fresh optimizer |
| Untrained P0-T floor | **same s as parent** | Seed-matched same-depth comparator (F5-19) |
| P5 wrapper/preprocessing RNG | **424242** | Fixed across all seeds; not the experimental factor |
| C3 document order / interleave | **42** | Shared treatment; do not re-draw per \(s\) |
| Gate H smoke | 0 | Once; nonconfirmatory |

---

## Inheritance registry (authority chain)

| Carried forward unchanged | Fresh by P5 design | Prohibited |
|---|---|---|
| Pin `92d63d4…`, six JSONL manifests, P3/P4 tokenizer pair, P4 C3 packed train shards + origin mask, budget \(N,B,T,D\), evaluator packing, thresholds, C3-only test policy, branch geometry | P5 seed panel, P5 parents/children, optimizer states, output paths, lockbox, gate cards, terminal checkpoints, test-access ledger, `scripts/p5/*` | P1.1/P2/P3/P4 weights as P5 parents; P4 seed 0 as a P5 cell; new tokenizer; new \(q_{\mathrm{TL}}\); byte balancing; altered C3 order; re-cleaned corpus; SFT/replay/EWC; post-outcome extra seed; P1–P4 env scripts at runtime |

**Linkage (one sentence each):** P1.1 = protected Tagalog corpus/split and BPB instrument. P2 = canonical WikiText-103-raw stream provenance and matched-branch lineage. P3 = fresh-Tagalog-parent, P0-T, common-parent, protected-evaluation architecture; B3 is not C3. P4 = token-share-locked C3 treatment, contrasts, and C3-only test policy being replicated. P5 = first predeclared multi-new-seed recurrence panel for that treatment.

---

## Failure / disposition taxonomy

| Event | P5 disposition |
|---|---|
| Shared-registry breach (splits, tokenizer, C3 trainer inputs/mask, evaluator, test isolation, forbidden lineage) | **Panel-level protocol stop**; preserve receipts; no P5 result label |
| Seed-isolated staging/output breach before that seed's official terminal checkpoint | **Seed-level protocol stop**; no result for that seed; re-verify shared registry unchanged; remaining seeds continue |
| Pre-outcome technical failure with no official terminal checkpoint and no accessed P5 scalar | **Quarantine**; clean restart from immutable \(C0_s\), fresh optimizer, new empty output dir; log incident |
| Finite terminal official checkpoint and sealed scalar | **Never exclude for outcome**; retain in panel classification even if both criteria fail |
| P0-T blocked | **Ineligible seed**; no children; no replacement; remaining seeds continue |

---

## Form sentence 1

P5 is designed after released P4 findings (AsPredicted #307591; Gate X 2026-08-21; both co-primary criteria observed in one initialization). It is a post-P4, prospectively preregistered multi-seed panel of the P4 token-share apparatus. It does not amend AsPredicted #306780, #306935, #307342, or #307591. It is not an independent confirmation of P4. It is not a population estimate, confidence interval, or inferential test.

---

## Question 8 linkage paragraph (ready to paste)

P5 is the separately preregistered multi-seed follow-up identified by P4's one-seed limitation. P1.1 supplies the protected Tagalog corpus/split and BPB measurement apparatus; P2 supplies the canonical WikiText-103-raw stream provenance and matched-branch lineage; P3 supplies the fresh-Tagalog-parent, P0-T, common-parent, and protected-evaluation architecture; P4 supplies the distinct token-share-locked C3 treatment, contrasts, and C3-only test policy. P5 changes only the predeclared parent-initialization seed and newly trained descendants. It does not load earlier weights, count P4 seed 0 as a P5 cell, or treat P4's released magnitudes as calibration targets. P5 is computationally independent of P4 in its parent weights, children, ledgers, and P5 outcomes; it is not outcome-independent of P4, because P4's released seed-0 results informed this pre-filed replication panel. P5 uses archived public text but prospectively trains new computational models and generates new P5 evaluation outcomes; there are no human participants.

---

## What this addendum does not do

It does not add a C4 arm, change \(q_{\mathrm{TL}}\), allow fertility or P4 magnitudes to pick \(\delta\), allow CPU P0-T to set status, allow seed-level unblinding, or treat P4 seed 0 as a P5 confirmatory cell.
