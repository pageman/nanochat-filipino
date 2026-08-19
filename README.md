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
