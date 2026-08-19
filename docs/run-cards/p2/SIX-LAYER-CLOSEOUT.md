# P2 six-layer close-out — filled ledger (2026-08-19)

Companion to the operator document *P2 Six-Layer Preregistration Completion Checklist*.  
**No new P2 training, validation, or test access.** Hidden-risk scans used filenames, hashes, and existing JSON/TeX only.

**Verdict B.** Computational P2 is closed. Remaining work is dissemination (ResearchBox upload, Hub complete-set, live website, volume termination after backup, secret rotation, advisor review)—not evidence generation.

Hard stops H1–H8 honored this session.

## Layer I — explicit (E-01–E-32)

E-01–E-22, E-24–E-27: complete (Gates A–V receipts).  
E-23, E-30, E-31: current `paper.tex` / Hub card source pass language checks (A3 “not mitigation”; no CI/\(p\); no CORE/SFT primary claim).  
E-28, E-29, E-32: **now documented** in `paper.tex` Table exposure + A3 shares + §Q8; JSON `registered-reporting-q3-q8.json`.

## Layer II — implicit

I-01–I-07, I-09, I-11–I-12, I-14–I-15: complete (parent SHA on R/S/T; wrapper `load_optimizer=False`; mix frozen Gate E; evaluator `inloop_val_is_not_val_bpb_full`; CUDA A0 TL 4.917650 vs CPU diagnostic 4.921200).  
I-08: BPB formula now in methods.  
I-10: A3 token shares published (0.933/0.067), not called token-balanced.  
I-13: local checkpoint hashes match Q/R/S/T (`p2_closeout_manifest.json`). Hub `.pt` not uploaded, so Hub filename reconciliation is N/A until R-08.

## Layer III — inferred

N-01–N-06 supported in current paper. N-07–N-12 blocked by explicit wording. Abstract contains “not observed,” “observed,” and “one-seed.”

## Layer IV — extrapolated (not P2 obligations)

X-01–X-07 remain labeled future work. `p3-post-unblinding.md` forbids outcome-independent P3.

## Layer V — residuals

| ID | Status |
|---|---|
| R-01 | Done: `p2_closeout_manifest.json` |
| R-02 | Done: A0–A3 hash match |
| R-03 | Done: U 07:17:53Z before V 07:47:24Z; test_read_count=0 at seal |
| R-04 | Done: exposure + A3 shares in paper/JSON |
| R-05 | Done: Q8 status lines |
| R-06 | Partial: pin `92d63d4e…`; wrapper SHA in Gate R integrity; git working tree still dirty |
| R-07 | Local pack ready; **upload pending** |
| R-08 | **Deferred** complete A0–A3 set |
| R-09 | Card source complete; Hub live README may lag until push |
| R-10 | Current PDF SHA `8689946f38c83c07758ed64ea0d16ca7ba8d4b71737852e33db966589fc0ec5a`; obsolete Stage-1 PDF quarantined |
| R-11 | Cheng not coauthor (paper/ethics); advisor review not dated |
| R-12 | `PUBLIC-STATUS.md` ready; live site not updated |
| R-13 | Volume **retained** (user: do not turn off pods) |
| R-14 | No missing checkpoint; no recovery run |
| R-15 | Rotation not executed this session |
| R-16 | Local frozen archive `transfer/p2-closeout-archive-20260819`; external deposit pending R-07 |

## Layer VI — hidden-risk scans

| ID | Result |
|---|---|
| HN-01 | `git ls-files`: no `test.jsonl` / `english_test.jsonl`. Local packs previously exclusion-scanned empty. |
| HN-02 | `1.164768` in P2 paper only as **nonreuse** / P1.1 citation, not as P2 A2 outcome. P2 test is 1.160154. |
| HN-03 | Ledger: `authorized_touches=1`, two component reads. Paper: “one authorized secondary test touch.” |
| HN-04 | Gate C/D/G isolation receipts; no new mount inspection of live pod (pod EXITED, not started). |
| HN-05 | Mix order SHA `b6ae432b…` in LOCK, Gate E, A3 cards. |
| HN-06 | Local rehash matched Q/R/S/T. |
| HN-07 | Card source lists same four SHAs as gates. Hub `.pt` absent. |
| HN-08 | R/S/T: `resume_from_step=-1`, wrapper `load_optimizer=False`. EN0 d20 resume-from-2400 is parent provenance only, not a child resume. |
| HN-09 | Paper A0 TL **4.917650**. CPU 4.921200 only in `*.cpu-diagnostic.json` and Gate Q note. |
| HN-10 | N/A until Hub upload. |
| HN-11 | Recalc: \(1.385684-1.459675=-0.073991\); \(1.171616-5.054664=-3.883048\). |
| HN-12 | TeX/JSON match. Stale `paper.html` (missing shares) **regenerated** from current TeX this pass. |
| HN-13 | Current paper: “not registered as mitigation.” Planning file `LITERATURE-CF-CONSTRUCTS.md` still contains pre-study “Replay (A3) mitigated BWT”—**not a results table**; do not cite as P2 finding. |
| HN-14 | Tests in separate Gate V subsection, not Table 2. |
| HN-15 | Abstract and limitations retain one-seed scope. |
| HN-16 | Current PDF compiled 2026-08-19 from current TeX; Stage-1 PDF quarantined. |
| HN-17 | Discussion uses required narrow reading; forbids general English improvement. |
| HN-18 | Authorship: Paul Pajo; Cheng not coauthor. Title consistent with #306935. |
| HN-19 | Hub YAML `license: other`; compatibility review not a legal opinion. |
| HN-20 | Passcodes gitignored (`aspredicted-p2-submitted.txt`). No token values in tracked files. Rotation residual. |
| HN-21 | Live site not checked (no URL edited). |
| HN-22 | Paper + `p3-post-unblinding.md`: P3 is post-P2. |

## §10 Final evidence ledger

| # | Item | Evidence | Yes/No |
|---:|---|---|---|
| 1 | Gates A–W preserved | `docs/run-cards/p2/p2-20260817T150944Z-de99f8a/gate-*.json` including `gate-w-deposit.json` | **Yes** |
| 2 | A0–A3 SHA reconciliation | `p2_closeout_manifest.json` | **Yes** |
| 3 | Gate U table matches paper | seal vs `paper.tex` Table 2 | **Yes** |
| 4 | U before V; test count 0 at seal | U `2026-08-19T07:17:53Z` `test_read_count=0`; V `07:47:24Z` | **Yes** |
| 5 | Gate V one touch / two components / A2 only | `test_access_log.json` | **Yes** |
| 6 | Hygiene receipts | Gates C/D/G + Q3–Q8 drop audit 0 | **Yes** |
| 7 | A3 shares + exposure table published | `paper.tex` + `registered-reporting-q3-q8.json` | **Yes** |
| 8 | Descriptive-item status | paper §Q8 | **Yes** |
| 9 | \(C_{EN}\)/\(G_{TL}\) formulas and narrow wording | results + discussion | **Yes** |
| 10 | One-seed; no formal inference | limitations | **Yes** |
| 11 | A3 not mitigation in current paper | TeX scan | **Yes** (watch old literature notes) |
| 12 | Tests secondary; legacy holdout | Gate V subsection | **Yes** |
| 13 | Current PDF from current source | SHA `8689946f…ec5a` | **Yes** |
| 14 | ResearchBox live | local pack only | **No** (upload pending) |
| 15 | Hub release/defer + hashes | deferral recorded; weights not uploaded | **Yes** as deferral |
| 16 | Website matches paper | `PUBLIC-STATUS.md` only | **No** (live URL pending) |
| 17 | Local archive + external backup | local frozen archive yes; ResearchBox/Hub backup no | **Partial** |
| 18 | Secrets excluded; rotation | excluded from packs; rotation not done | **Partial** |
| 19 | P1.1/P3/P4 separated | paper + `p3-post-unblinding.md` | **Yes** |
| 20 | Volume terminated or reason retained | EXITED pods, 80 GB retained per user instruction | **Yes** (retained, named reason) |

## Verdict text (template B)

The preregistered computation, validation seal, and one authorized A2-only test event are complete and must not be repeated. The overall close-out remains open only for documentary/residual rows **R-07, R-08/R-09 Hub push, R-11, R-12, R-13 (after backup), R-15, ledger 14/16/17/18**—archival, reporting, release, or security evidence, not new P2 training, validation, or test access.
