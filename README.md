# nanochat-filipino

Clean-room experiments that train Tagalog / Filipino language models with [Karpathy’s nanochat](https://github.com/karpathy/nanochat), aligned with Dr. Charibeth Cheng’s public resources.

## Start here

**Project 1 protocol (P1.1):** [docs/PROTOCOL-project1-wikitext-tl39.md](docs/PROTOCOL-project1-wikitext-tl39.md)  
**Charter:** [configs/project1.yaml](configs/project1.yaml)  
**What changed vs P1.0:** [docs/RECONCILE-p1.1.md](docs/RECONCILE-p1.1.md)  
**Implementation plan folded in:** [docs/SOURCE-implementation-plan-2026-08-16.md](docs/SOURCE-implementation-plan-2026-08-16.md)  
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
