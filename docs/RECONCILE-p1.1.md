# P1.1 reconciliation — implementation plan folded into the protocol

**Date:** 2026-08-16  
**Trigger:** Factor in `/Users/paulpajo/Downloads/project1_wikitext_tl39_nanochat_implementation_plan.md` before any AsPredicted filing.  
**Archived copy:** [SOURCE-implementation-plan-2026-08-16.md](SOURCE-implementation-plan-2026-08-16.md)  
**Status:** P1.1 supersedes P1.0 wherever they conflict. Do not file AsPredicted on P1.0 answers.

P1.0 was a local pre-analysis draft. The downloaded plan is a tighter nanochat-interface blueprint (pinned commit, loader packing, horizon math, two experiment families, canonical-vs-clean data). This note records every confirmatory change so the AsPredicted text matches the plan we will actually run.

---

## Decisions adopted from the implementation plan

| Topic | P1.0 (old) | P1.1 (now) | Why |
|---|---|---|---|
| nanochat pin | "record whatever HEAD is" | **`92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`** (2026-08-16) | Reproducible interface; loader/horizon notes are commit-specific |
| Data-path | Symlink into `base_data_climbmix` (no patch) | **Preferred: one-line `NANOCHAT_DATA_DIR` hook**; symlink only as a zero-patch smoke | Auditable publication config; default ClimbMix path unchanged |
| Canonical text | Moses detokenize (`@-@` → `-`) | **Preserve source text**; line-ending normalize only | Answers "nanochat on the public mirror," not a new corpus |
| Detokenize / NFC / dedup | Detok was default | **Clean ablation only**; never overwrite canonical | Separate questions |
| Split recovery | Jump to hash split | **First try to recover 2019 train/val/test files**; else label `reconstructed_70_15_15` | Honest about the single-parquet mirror |
| Split seed / rule | Hash `u` with seed 20260816 | **Lexicographic `sha256(utf8 text)` order, 70/15/15**; seed 42 only if a shuffle is used | Matches `configs/project1.yaml` |
| Split unit | Always reconstruct `= Title =` articles | **Attempt article reconstruction; if it fails the audit, use parquet-row identity and label it row-level** | 1.52M rows vs ~121k paper documents |
| Depths | d4/d6/d8/d12; d24 forbidden | **Smoke d4; pilot d8/d12; production d8, d12, d16, d20; d24 optional** | Plan's miniseries; still not a GPT-2 speedrun claim |
| Horizon | One epoch as primary | **Two families: native ratio (compatibility) and fixed-data `D_1x`/`D_3x`/`D_10x`. Primary science = fixed-data `D_3x`** | Default ratio will reuse this small corpus |
| `--target-param-data-ratio=-1` | Not discussed | **MUST NOT.** Keep a positive ratio; set `--num-iterations` and `--total-batch-size` | Current `base_train.py` still uses the ratio in scaling math |
| Sequence length | 1024 default | **2048 confirmatory**; reduce only `device-batch-size` on small VRAM | Native nanochat T; report cropping |
| Tokens | Mixed Moses / BPE | **Three named counts: paper-Moses, whitespace approx, nanochat BPE.** Never one column called "tokens" | Incomparable units |
| Loader | Ignored packing | **Report source tokens and model-visible tokens** (BOS best-fit pack, ~35% crop at T=2048) | Methods requirement |
| Eval | `val_bpb` | Same, plus **independent test script**, `base_eval --eval=bpb,sample`, optional bootstrap CIs | Plan Phase 12 |
| Tokenizer H | Leakage (train-only vs all-split) | **Primary H2 = Tagalog 32k BPE vs English GPT-2 tokenizer compression.** Leakage stays secondary | Plan H2 |
| Pipeline H | Implicit | **H1 = pipeline works with only the data-dir hook** | Plan H1 |
| Seeds | seed 0; 3 seeds if ranking | **d8/d12 pilots 3 seeds if feasible; d16/d20 1–2; no bitwise determinism** | nanochat seed 42, determinism off |
| Layout | `data/raw|interim|processed` | **Add `configs/`, `data/canonical/`, `data/clean_ablation/`, `runtime/`, manifests** | Plan §5 |
| Human audit | Optional rater on samples | **SHOULD: Tagalog-proficient stratified sample of corpus + fixed prompt rubric** | Plan §3.5, §18.5 |

---

## Conflicts resolved (do not mix)

1. **Do not detokenize the confirmatory corpus.** P1.0 §9.4 default is revoked. Detokenize, if run, is an exploratory ablation with a new run id.  
2. **Do not file AsPredicted claiming one-epoch d4/d6 as the only confirmatory matrix.** The confirmatory depth grid is d8/d12/d16/d20 under a predeclared fixed budget.  
3. **Do not treat symlink-into-ClimbMix as the publication path.** It is a smoke fallback.  
4. **Do not set `--target-param-data-ratio=-1`.  
5. **Do not compare native-horizon depths as equal data exposure.**

---

## What stayed from P1.0

- Isolated `NANOCHAT_BASE_DIR`; never `python -m nanochat.dataset`.  
- S3 zip is 404; use `linkanjarad/Wikitext-TL39`.  
- Last parquet = val; test outside the active dir.  
- Train-only tokenizer, vocab 32768.  
- CORE disabled as a primary claim.  
- Test BPB once after val selection.  
- No dengue/hate-speech/SFT in this study.  
- AsPredicted is still unfiled; Q1 remains **Yes (archival corpus), outcomes not yet computed**.

---

## AsPredicted impact

File **P1.1** answers only ([run-cards/aspredicted-answers-p1.txt](run-cards/aspredicted-answers-p1.txt)). Delete or ignore any mental model of the P1.0 eight boxes. Hash **this reconciliation + `configs/project1.yaml` + the protocol** together before submit.
