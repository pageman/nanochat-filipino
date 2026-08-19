# P2 explicit preregistration reporting audit (AsPredicted #306935)

Source audit: operator hand-off of 2026-08-19. This file records documentary inclusion after reconstructing A3 token shares and the A1/A2/A3 exposure table from frozen train files (no test read, no new `val_bpb_full`).

**Verdict (Version B, then documentary close on rows 8–9–18):** All primary confirmatory commitments were executed and sealed. Computational P2 remains closed. Reporting residuals that were blocking “every explicit obligation documented” are now in `paper.tex`, `registered-reporting-q3-q8.json`, and the model-card source. External ResearchBox upload and Hub weight-set publication remain operator steps (rows 16–17 public copies).

## §11 sign-off

| # | Required check | Evidence | Status |
|---:|---|---|---|
| 1 | AsPredicted #306935 cited | Paper bibitem + Hub card | yes |
| 2 | P0-E d8/d20 and both floors | Table 1; paper states P0-E passed | yes |
| 3 | A0 separated from primary contrasts | Table 2; A0 Tagalog descriptive | yes |
| 4 | A1/A2/A3 val table matches seal | `gate-u-seal.json` vs `paper.tex` | yes |
| 5 | \(C_{EN}\) formula/sign/cutoff/not observed | Results | yes |
| 6 | \(G_{TL}\) formula/sign/cutoff/observed in one-seed apparatus | Results | yes |
| 7 | A3 \(C_{EN}(A3)\)/\(G_{TL}(A3)\) | EN−0.180242, TL−3.525806 | yes |
| 8 | A3 document/byte/BPE-token shares | docs 50/50; bytes 0.961314/0.038686; tokens 0.933232/0.066768 | yes |
| 9 | Unique docs/bytes/tokens/revisit per arm | Table `\ref{tab:exposure}` / `registered-reporting-q3-q8.json` | yes |
| 10 | English BPE / BPB formula / evaluator / full val | Methods; tokenizer SHAs; `evaluate_bpb.py` | yes |
| 11 | One-seed point estimates; no test/CI | Limitations | yes |
| 12 | A2-only secondary tests segregated | Gate V subsection | yes |
| 13 | Legacy holdout + nonreuse of 1.164768 | Gate V subsection | yes |
| 14 | Test log 1 touch / 2 reads / A2 only | `test_access_log.json` | yes |
| 15 | Q6 exclusion/hygiene | Gate C/D/G/R/S/T; drop audit 0/0; hash overlap 0 | yes (compiled, not a new run) |
| 16 | Frozen hashes + environment in deposit | LOCK + run cards + local ResearchBox pack; **human upload pending** | yes locally; public deposit pending |
| 17 | No P1.1 weights/test raw/secrets in P2 public release | Local packs clean; Hub `.pt` not yet uploaded | yes locally; Hub complete-set still deferred |
| 18 | Q8 descriptive statuses explicit | Paper §Q8; JSON | yes (two items transparently not run/not collected) |
| 19 | Exploratories excluded from confirmatory table | Limitations | yes |
| 20 | P3 post-P2; P1.1/P3/P4 separate | Discussion + `p3-post-unblinding.md` | yes |

## Exact published A3 shares

From Gate E bytes (unchanged) plus English-BPE token reconstruction on the frozen mix Tagalog subset (train only):

- Documents: EN 28472 / TL 28472 (0.5 / 0.5)
- UTF-8 bytes: EN 539903397 / TL 21726972 (0.961314 / 0.038686)
- BPE tokens (no BOS): EN 118286771 / TL 8462807 (0.933232 / 0.066768)

## Q8 residual dispositions

| Item | Disposition |
|---|---|
| A2 English trajectory | Not collected. A2 in-loop val is Tagalog diagnostic. |
| PTPP \(R_d\) | Defined as step/294; EN0/phase-2 \(D/P_{\mathrm{scaling}}\) from Gate G; no English-BPB plot. |
| Fertility | Gate F: EN val 4.603, TL val 2.574 bytes/token. |
| P1.1-on-English OOD | Not run; not BWT; not a P2 rescue. |

**Hard exclusions honored:** no further confirmation run, no validation re-evaluation, no test read.
