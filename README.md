# nanochat-filipino

Clean-room experiments that train Tagalog / Filipino language models with [Karpathy’s nanochat](https://github.com/karpathy/nanochat), aligned with Dr. Charibeth Cheng’s public resources.

## Start here

**Project 1 protocol (P1.1):** [docs/PROTOCOL-project1-wikitext-tl39.md](docs/PROTOCOL-project1-wikitext-tl39.md)  
**Charter:** [configs/project1.yaml](configs/project1.yaml)  
**What changed vs P1.0:** [docs/RECONCILE-p1.1.md](docs/RECONCILE-p1.1.md)  
**Implementation plan folded in:** [docs/SOURCE-implementation-plan-2026-08-16.md](docs/SOURCE-implementation-plan-2026-08-16.md)  
**Paper:** https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39  
**AsPredicted #306780:** https://aspredicted.org/6r6v4v.pdf (anonymous)  
**ResearchBox #8735:** https://researchbox.org/8735  
**Results:** [docs/run-cards/RESULTS-p1.1-aspredicted-306780.md](docs/run-cards/RESULTS-p1.1-aspredicted-306780.md)  
**Machine-readable results:** [results/](results/)  
**Model card:** [docs/run-cards/MODEL-CARD-p1-fixed-d20-3x.md](docs/run-cards/MODEL-CARD-p1-fixed-d20-3x.md)  
**Weights (not in this repo):** https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x  
**Hub review (2026-08-16):** [docs/run-cards/published_d20_checkpoint_assessment.md](docs/run-cards/published_d20_checkpoint_assessment.md) · [response](docs/run-cards/RESPONSE-published-d20-checkpoint-assessment.md)  
**DeepWiki:** https://deepwiki.com/pageman/nanochat-filipino  
**Execution clarifications:** [docs/EXECUTION-CLARIFICATIONS-p1.1.md](docs/EXECUTION-CLARIFICATIONS-p1.1.md)  
**Gate ledger:** [manifests/gate_ledger.json](manifests/gate_ledger.json)  
**Data/code notices:** [DATA_AND_CODE_NOTICES.md](DATA_AND_CODE_NOTICES.md)

## Status

Gates A–J are complete. `D* = 20` by exact minimum `val_bpb_full = 1.172248`. Margin to depth 8 is 0.006887 BPB and is not a ranking. One `test_bpb = 1.164768`. This repo is the close-out archive: code, manifests, evaluator, and result bundles. Checkpoints stay on Hugging Face. Held-out `test.jsonl` and ResearchBox credentials are not published here.

Hub checkpoint metadata `val_bpb` used `--eval-tokens=262144` and is **not** the primary DV. Do not rank depths from those loop scores. The registered table is [results/full_validation.json](results/full_validation.json).

Do not claim that deeper is always better. Split label in every caption: `reconstructed_article_70_15_15`. SFT and English catastrophic-forgetting studies are new registrations, not this release.

## Start here (P2)

Does **not** amend AsPredicted #306780, ResearchBox 8735, or Hub `pageman/nanochat-filipino-p1-fixed-d20-3x`. Never use `scripts/p1/env.sh` for P2.

**Project 2 protocol (P2):** [docs/papers/p2-cf-english/PROTOCOL-p2-en-then-tl.md](docs/papers/p2-cf-english/PROTOCOL-p2-en-then-tl.md)  
**Study record:** [docs/p2/](docs/p2/)  
**Lock:** [docs/papers/p2-cf-english/LOCK.json](docs/papers/p2-cf-english/LOCK.json)  
**Paper (source / PDF):** [docs/papers/p2-cf-english/paper.tex](docs/papers/p2-cf-english/paper.tex) · [paper.pdf](docs/papers/p2-cf-english/paper_outputs/paper.pdf)  
**AsPredicted #306935:** https://aspredicted.org/xa56bs.pdf (anonymous)  
**ResearchBox #8763:** https://researchbox.org/8763  
**Results:** [docs/run-cards/p2/PUBLIC-STATUS.md](docs/run-cards/p2/PUBLIC-STATUS.md)  
**Machine-readable results:** [results/p2/](results/p2/)  
**Model card:** [docs/run-cards/p2/HF-MODEL-CARD-p2.md](docs/run-cards/p2/HF-MODEL-CARD-p2.md)  
**Weights (not in this repo):** https://huggingface.co/pageman/nanochat-filipino-p2-en-then-tl  
**Hub documentation pack:** [docs/hub/p2-en-then-tl/](docs/hub/p2-en-then-tl/)  
**DeepWiki:** https://deepwiki.com/pageman/nanochat-filipino  
**Environment:** [scripts/p2/env.sh](scripts/p2/env.sh) · [scripts/p2/env.cuda.sh](scripts/p2/env.cuda.sh)  
**Sealed validation table:** [results/p2/gate-u-seal.json](results/p2/gate-u-seal.json)  
**Data/code notices:** [DATA_AND_CODE_NOTICES.md](DATA_AND_CODE_NOTICES.md)

## Status (P2)

Gates A–W are recorded. Confirmatory depth is d20. Sealed `C_EN = EN(A2)−EN(A1) = −0.073991` (filed ≥0.01: **not observed**). Sealed `G_TL = TL(A2)−TL(A1) = −3.883048` (filed ≤−0.01: **observed** in this one-seed apparatus). One authorized A2-only secondary test (`test_bpb` English 1.392015; Tagalog holdout under English BPE 1.160154). Do not reuse P1.1 `test_bpb = 1.164768`. A1 and A3 were not tested. This repo is the P2 audit trail: code, manifests, evaluator, and result bundles under `docs/p2/` and `results/p2/`. Checkpoints stay on Hugging Face. Held-out `test.jsonl` and ResearchBox credentials are not published here.

Trainer in-loop `val_bpb` is **not** the primary DV. Do not rank arms from loop scores or from `meta_*.json` `val_bpb`. The registered table is [results/p2/sealed_val_table.csv](results/p2/sealed_val_table.csv) · [results/p2/gate-u-seal.json](results/p2/gate-u-seal.json).

Do not claim that Tagalog generally improves English. One seed; no significance test. A3 is a 50/50-document trade-off arm, not mitigation. Weights live on Hugging Face (`pageman/nanochat-filipino-p2-en-then-tl`), not in this git tree.

## Start here (P3)

Does **not** amend AsPredicted #306780 / #306935, ResearchBox 8735 / 8763, or Hub `p1-fixed-d20-3x` / `p2-en-then-tl`. Never use `scripts/p1/env.sh` or `scripts/p2/env.sh` for P3. Fresh Tagalog parent (TL0/B0), then matched English continuation.

**Project 3 protocol (P3):** [docs/papers/p3-reverse/PROTOCOL-p3-tl-then-en.md](docs/papers/p3-reverse/PROTOCOL-p3-tl-then-en.md)  
**Study record:** [docs/p3/](docs/p3/) · https://github.com/pageman/nanochat-filipino/tree/main/docs/p3  
**Lock:** [docs/papers/p3-reverse/LOCK.json](docs/papers/p3-reverse/LOCK.json)  
**Paper (source / PDF):** [docs/papers/p3-reverse/paper.tex](docs/papers/p3-reverse/paper.tex) · [paper.pdf](docs/papers/p3-reverse/paper_outputs/paper.pdf)  
**Paper (ResearchGate v1.2):** https://www.researchgate.net/publication/412889563_Tagalog_Retention_and_English_Acquisition_under_Equal-Budget_nanochat_Continual_Pretraining_v12_-_A_Preregistered_Post-P2_Reverse-Direction_Study_on_WikiText-TL-39_and_WikiText-103  
**AsPredicted #307342:** https://aspredicted.org/wd2pc8.pdf (anonymous)  
**ResearchBox #8834:** https://researchbox.org/8834  
**AsCollected:** https://ascollected.org/F36_C2C  
**Results:** [results/p3/](results/p3/)  
**Hub documentation pack:** [docs/hub/p3-tl-then-en/](docs/hub/p3-tl-then-en/)  
**Weights (not in this repo):** https://huggingface.co/pageman/nanochat-filipino-p3-tl-then-en  
**Environment:** [scripts/p3/env.sh](scripts/p3/env.sh) · [scripts/p3/env.cuda.sh](scripts/p3/env.cuda.sh)  
**Data/code notices:** [DATA_AND_CODE_NOTICES.md](DATA_AND_CODE_NOTICES.md)

## Status (P3)

Gates A–X are complete (Gate X released). Confirmatory depth is d20. Sealed \(C_{tl}=TL(B2)-TL(B1)=1.023484\) (filed ≥0.01: **observed**). Sealed \(G_{en}=EN(B2)-EN(B1)=-1.697955\) (filed ≤−0.01: **observed** in this one-seed apparatus). One authorized B2-only secondary test (English test BPB 1.357842; Tagalog legacy holdout under P3 BPE 2.493197). Do **not** reuse P1.1 `test_bpb = 1.164768` or P2 Gate V as P3. B1 and B3 were not tested. B3 is a 50/50-document trade-off arm (realized EN UTF-8 byte share ≈0.961), not mitigation. This repo is the P3 audit trail under `docs/p3/`, `docs/papers/p3-reverse/`, `docs/run-cards/p3/`, `scripts/p3/`, and `results/p3/`. Checkpoints stay on Hugging Face. Held-out `test.jsonl` and ResearchBox credentials are not published here.

Trainer in-loop `val_bpb` is **not** the primary DV. The registered table is under [results/p3/released/](results/p3/released/) · [results/p3/evaluation/p3-validation-seal.json](results/p3/evaluation/p3-validation-seal.json).

P3 is a **post-P2** prospective reverse-direction study. Weights live on Hugging Face (`pageman/nanochat-filipino-p3-tl-then-en`), not in this git tree.

## Start here (P4)

Does **not** amend AsPredicted #306780 / #306935 / #307342, ResearchBox 8735 / 8763 / 8834, or Hub `p1-fixed-d20-3x` / `p2-en-then-tl` / `p3-tl-then-en`. Never use `scripts/p1/env.sh`, `scripts/p2/env.sh`, or `scripts/p3/env.sh` for P4. Fresh Tagalog parent (TL0/C0), then matched C1/C2/C3. **C3 is not P3 B3.**

**Project 4 protocol (P4):** [docs/papers/p4-token-share-mix/PROTOCOL-p4-token-share-mix.md](docs/papers/p4-token-share-mix/PROTOCOL-p4-token-share-mix.md)  
**Study record:** [docs/p4/](docs/p4/) · https://github.com/pageman/nanochat-filipino/tree/main/docs/p4  
**Lock:** [docs/papers/p4-token-share-mix/LOCK.json](docs/papers/p4-token-share-mix/LOCK.json)  
**Paper (source / PDF):** [docs/papers/p4-token-share-mix/paper.tex](docs/papers/p4-token-share-mix/paper.tex) · [paper.pdf](docs/papers/p4-token-share-mix/paper_outputs/paper.pdf)  
**AsPredicted #307591:** https://aspredicted.org/if84km.pdf (anonymous)  
**ResearchBox #8869:** https://researchbox.org/8869  
**AsCollected:** #2471 (`NANOCHAT-FILIPINO-P4`)  
**Results:** [results/p4/](results/p4/)  
**Hub documentation pack:** [docs/hub/p4-token-share-mix/](docs/hub/p4-token-share-mix/)  
**Weights (not in this repo):** https://huggingface.co/pageman/nanochat-filipino-p4-token-share-mix  
**Environment:** [scripts/p4/env.sh](scripts/p4/env.sh) · [scripts/p4/env.cuda.sh](scripts/p4/env.cuda.sh)  
**Data/code notices:** [DATA_AND_CODE_NOTICES.md](DATA_AND_CODE_NOTICES.md)

## Status (P4)

Gates 0 / A–I / P0-T / Q–W are complete (Gate X released). Confirmatory depth is d20. Sealed \(R_{\mathrm{TL}}=\mathrm{TL}(C3)-\mathrm{TL}(C2)=-1.316637\) (filed \(\le -0.01\): **observed**). Sealed \(A_{\mathrm{EN}}=\mathrm{EN}(C3)-\mathrm{EN}(C1)=-1.375277\) (filed \(\le -0.01\): **observed** in this one-seed apparatus). One authorized C3-only secondary test (English test BPB 1.513698; Tagalog 1.202140). Do **not** reuse P1.1 `test_bpb = 1.164768` or P2/P3 Gate V as P4. C1 and C2 were not tested. C3 is a token-share trade-off arm (descriptive EN UTF-8 byte share ≈0.434), not byte-balanced and not P3 B3. This repo is the P4 audit trail under `docs/p4/`, `docs/papers/p4-token-share-mix/`, `docs/run-cards/p4/`, `scripts/p4/`, and `results/p4/`. Checkpoints stay on Hugging Face. Held-out `test.jsonl` and ResearchBox credentials are not published here.

Trainer in-loop `val_bpb` is **not** the primary DV. The registered table is under [results/p4/released/](results/p4/released/) · [results/p4/tables.json](results/p4/tables.json).

P4 is a **post-P3** prospective token-share mixture study. Weights live on Hugging Face (`pageman/nanochat-filipino-p4-token-share-mix`), not in this git tree.

## Start here (P5)

Does **not** amend AsPredicted #306780 / #306935 / #307342 / #307591, ResearchBox 8735 / 8763 / 8834 / 8869, or Hub `p1-fixed-d20-3x` / `p2-en-then-tl` / `p3-tl-then-en` / `p4-token-share-mix`. Never use `scripts/p1/env.sh`, `scripts/p2/env.sh`, `scripts/p3/env.sh`, or `scripts/p4/env.sh` for P5. Closed panel of unused parent-init seeds `{1,2,3}`: fresh Tagalog parent (TL0/C0) per seed, then matched C1/C2/C3. **C3 is not P3 B3.** P4 seed 0 is historical, not a P5 confirmatory cell.

**Study record:** [docs/p5/](docs/p5/) · https://github.com/pageman/nanochat-filipino/tree/main/docs/p5  
**Lock:** [docs/papers/p5-multi-seed-p4/LOCK.json](docs/papers/p5-multi-seed-p4/LOCK.json)  
**Paper (source / PDF):** [docs/papers/p5-multi-seed-p4/paper.tex](docs/papers/p5-multi-seed-p4/paper.tex) · [paper.pdf](docs/papers/p5-multi-seed-p4/paper_outputs/paper.pdf)  
**Paper (ResearchGate):** https://www.researchgate.net/publication/413546596_How_Often_a_Frozen_Mix_Recurs_across_Unused_Initializations_A_Closed_Three-Seed_Count_Not_a_Population_Estimate  
**Hub model card (paper + P5 subtree links):** https://huggingface.co/pageman/nanochat-filipino-p5-p4-multi-seed/commit/798829e250ece06615195432d91efd6f657dab3a  
**AsPredicted #307836:** https://aspredicted.org/k6ib64.pdf (anonymous)  
**ResearchBox #8904:** https://researchbox.org/8904  
**AsCollected #2503 v1:** https://ascollected.org/HC8_G2F (`NANOCHAT-FILIPINO P5`)  
**Results:** [results/p5/](results/p5/)  
**Hub documentation pack:** [docs/hub/p5-p4-multi-seed/](docs/hub/p5-p4-multi-seed/)  
**Weights (not in this repo):** https://huggingface.co/pageman/nanochat-filipino-p5-p4-multi-seed/  
**Environment:** [scripts/p5/env.sh](scripts/p5/env.sh) · [scripts/p5/env.cuda.sh](scripts/p5/env.cuda.sh)  
**Data/code notices:** [DATA_AND_CODE_NOTICES.md](DATA_AND_CODE_NOTICES.md)

## Status (P5)

Gates 0 / A–H / I₁–V₃ / X / W are complete (panel unblinded). Confirmatory depth is d20. Primary result is the **count table** only (`K=3`): eligible 3; both 3; only-R 0; only-A 0; neither 0; ineligible 0 (\(k_{\mathrm{both}}=3\) of \(K_{\mathrm{elig}}=3\)). No mean, CI, \(p\)-value, or “P5 confirms P4.” C3-only secondary tests are descriptive and excluded from classification. This repo is the P5 audit trail under `docs/p5/`, `docs/papers/p5-multi-seed-p4/`, `docs/run-cards/p5/`, `scripts/p5/`, `results/p5/`, `docs/hub/p5-p4-multi-seed/`, and `manifests/p5/`. Checkpoints stay on Hugging Face. Held-out `test.jsonl` and ResearchBox credentials are not published here.

Trainer in-loop `val_bpb` is **not** the primary DV. The registered count table is under [results/p5/](results/p5/).

P5 is a **post-P4** confirmatory closed three-seed panel. Weights live on Hugging Face (`pageman/nanochat-filipino-p5-p4-multi-seed`), not in this git tree.

## Start here (P6-M)

Does **not** amend AsPredicted #306780 / #306935 / #307342 / #307591 / #307836, prior ResearchBoxes, or Hub `p1`–`p5` IDs. Never use `scripts/p1`–`p5` env for P6. One unused parent-init seed **4**: frozen Tagalog C0, then C1/C2 plus four filed schedule-topology children (M-fine / M-coarse / M-blocked / M-rand) under a fixed phase-2 token budget.

**Study record:** [docs/p6/](docs/p6/) · https://github.com/pageman/nanochat-filipino/tree/main/docs/p6  
**Lock:** [docs/papers/p6-m-schedule-topology/LOCK.json](docs/papers/p6-m-schedule-topology/LOCK.json)  
**Paper (source / PDF):** [docs/papers/p6-m-schedule-topology/paper.tex](docs/papers/p6-m-schedule-topology/paper.tex) · [paper.pdf](docs/papers/p6-m-schedule-topology/paper_outputs/paper.pdf)  
**AsPredicted #307969:** https://aspredicted.org/bk6m9d.pdf (anonymous)  
**ResearchBox #8918:** https://researchbox.org/8918  
**AsCollected #2541:** `NANOCHAT-FILIPINO P6-M` (create share URL when ready)  
**Results:** [results/p6/](results/p6/)  
**Hub documentation pack:** [docs/hub/p6-m-schedule-topology/](docs/hub/p6-m-schedule-topology/)  
**Weights (not in this repo):** https://huggingface.co/pageman/nanochat-filipino-p6-m-schedule-topology  
**Weights commit:** [`5d3872b0`](https://huggingface.co/pageman/nanochat-filipino-p6-m-schedule-topology/commit/5d3872b000fe3aa7ed2d25e2e73927330002cb9b)  
**Environment:** [scripts/p6/env.sh](scripts/p6/env.sh) · [scripts/p6/env.cuda.sh](scripts/p6/env.cuda.sh)  
**Data/code notices:** [DATA_AND_CODE_NOTICES.md](DATA_AND_CODE_NOTICES.md)

## Status (P6-M)

Gates **0 / A–X / W** complete for run `p6-20260824T155226Z-769f807a` (seed **4** only). Primary result: topology contrasts ΔTL/ΔEN vs M-fine (`δ=0.01`). Policy A: M-fine test is secondary only. This repo is the P6-M audit trail under `docs/p6/`, `docs/papers/p6-m-schedule-topology/`, `docs/run-cards/p6/`, `scripts/p6/`, `results/p6/`, `docs/hub/p6-m-schedule-topology/`, and `manifests/p6/`. Checkpoints stay on Hugging Face. Held-out `test.jsonl` and ResearchBox credentials are not published here.

**Hub weight lineage:** C0/C1/C2/tokenizer are original study artifacts. The four topology children on Hub are a **2026-08-25 technical recreate** (new SHA-256; not bitwise identical to the original Gate T terminals, which were lost from the sticky pod volume). Science claims remain Gate X / filed receipts.

Trainer in-loop `val_bpb` is **not** the primary DV. Machine-readable contrasts: [results/p6/p6-s4-released-contrasts.json](results/p6/p6-s4-released-contrasts.json).

P6-M is a **post-P5** one-seed schedule-topology study. Weights live on Hugging Face (`pageman/nanochat-filipino-p6-m-schedule-topology`), not in this git tree.
