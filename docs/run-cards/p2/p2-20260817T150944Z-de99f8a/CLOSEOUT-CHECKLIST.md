# P2 Comprehensive Close-out Checklist and Operator Hand-off

> **Study:** P2 — English retention after Tagalog continuation with nanochat and WikiText-103 / WikiText-TL-39
>
> **Governing preregistration:** [AsPredicted #306935](https://aspredicted.org/xa56bs.pdf)
>
> **P2 run ID:** `p2-20260817T150944Z-de99f8a`
>
> **Pinned nanochat commit:** `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`
>
> **Protocol SHA-256:** `da7ac07b86d097770c10e76c79f0534d6c609ceea71baabcf587a4fcd01bc0e8`

## 0. Close-out purpose and boundary

P2’s **confirmatory computation is complete**. Gates A through W have been recorded, the full validation table was sealed before test access, and Gate V performed the one permitted A2-only secondary test event. The remaining work is evidence preservation, deposit, publication, public reporting, and clearly bounded future planning. It is **not** permission to run new P2 training, re-evaluate a branch, add another test read, select a new best arm, or reframe the sealed outcomes.

This document uses three distinct labels throughout:

| Label | Meaning | May it change the P2 result? |
|---|---|---|
| **Confirmed / sealed** | A recorded outcome or integrity fact in the existing P2 ledger | No |
| **Close-out operation** | A copying, hashing, compiling, uploading, writing, or disclosure task | No |
| **Future study** | P1.1 close-out, P3, P4, exploratory work, or new replication | No; it needs its own governing record |

The central rule is simple: **P2 can now be disseminated more clearly, but it cannot be recomputed into a different study.**

## 1. Authoritative completion record

### 1.1 Gate status

| Stage | Status | Close-out significance |
|---|---|---|
| Gates A–G | Pass | P2 source pin, English corpus, hygiene, official split, frozen inputs/mix, English tokenizer, and budgets were set before outcomes |
| Gate H | Pass | CUDA smoke established the intended NVIDIA execution path |
| Gate I | Pass | EN0 d8 and d20 English parents completed |
| P0-E | Pass | Both d8 and d20 EN0 parents exceeded the filed untrained and byte-unigram English eligibility floors before Tagalog child training |
| Gate Q | Pass | A0 is the immutable final EN0 d20 parent; official CUDA A0 Tagalog baseline is provenance only |
| Gate R / A1 | Pass | Extra-English active control completed from A0 |
| Gate S / A2 | Pass | Tagalog-only intervention completed from the same A0 |
| Gate T / A3 | Pass | Pre-frozen 50/50-document English–Tagalog mix arm completed from the same A0 |
| Gate U | Pass | All three branches received full English and Tagalog validation; validation table and contrasts sealed while test count remained zero |
| Gate V | Pass | One authorized A2-only secondary test event completed; A1/A3 were not tested |
| Gate W | Recorded | Paper/deposit close-out material prepared without another P2 evaluation or test touch |

### 1.2 The sealed P2 facts to reproduce verbatim

These numbers should be copied from `gate-u-seal.json` and `gate-v-test.json`, not manually retyped from memory. Any publication table should be checked against the source JSON before release.

| Arm / outcome | English BPB | Tagalog BPB | Interpretation role |
|---|---:|---:|---|
| A0 validation baseline | 1.389990 | 4.917650 | Parent provenance; A0→A2 Tagalog difference is descriptive only |
| A1 validation | 1.459675 | 5.054664 | Matched extra-English active control |
| A2 validation | 1.385684 | 1.171616 | Frozen-Tagalog continuation intervention |
| A3 validation | 1.279433 | 1.528858 | Predeclared 50/50-document trade-off arm |
| A2 English secondary test | 1.392015 | — | Official WT103-raw test; A2 only |
| A2 Tagalog secondary test | — | 1.160154 | P1.1 legacy `test.jsonl` under P2 English BPE; A2 only |

The primary contrasts must be displayed with their exact definitions:

\[
C_{EN}=\operatorname{English\ val\_bpb\_full}(A2)-\operatorname{English\ val\_bpb\_full}(A1)=-0.073991.
\]

\[
G_{TL}=\operatorname{Tagalog\ val\_bpb\_full}(A2)-\operatorname{Tagalog\ val\_bpb\_full}(A1)=-3.883048.
\]

| Filed interpretation rule | Sealed outcome | Required wording |
|---|---:|---|
| \(C_{EN}\geq0.01\): practical English-retention-cost pattern | −0.073991 | **Not observed.** The contrast has the opposite sign from the filed prediction; do not redescribe this as support for forgetting. |
| \(G_{TL}\leq-0.01\): practical Tagalog-adaptation-gain pattern | −3.883048 | **Observed in this one-seed fixed apparatus.** |
| A3 English contrast, \(EN(A3)-EN(A1)\) | −0.180242 | Report descriptively as part of the predeclared trade-off map. |
| A3 Tagalog contrast, \(TL(A3)-TL(A1)\) | −3.525806 | Report descriptively as part of the predeclared trade-off map. |

> **Forbidden rewrite:** “P2 found that Tagalog continuation causes English improvement.”
>
> **Required narrow reading:** “In this preregistered, one-seed, fixed-parent, fixed-budget apparatus, the predicted English-retention-cost pattern was not observed; the A2-versus-A1 validation contrast instead favored A2 on English BPB, while the preregistered Tagalog-gain pattern was observed.”

### 1.3 Test-access final state

The final P2 test log must show the following, without ambiguity:

| Field | Required final state |
|---|---|
| Authorized test touches | `1` |
| Authorized event | Gate V only |
| Component reads | Exactly two: one official WT103-raw English test and one P1.1 legacy Tagalog holdout |
| Tested checkpoint | A2 d20 final checkpoint only |
| A1 test evaluation | Never run |
| A3 test evaluation | Never run |
| Reuse of P1.1 `test_bpb=1.164768` | Never used as a P2 observation |
| Future P2 test reads | Prohibited; the P2 test boundary is closed |

## 2. Close-out hard stops

Before any upload, paper revision, or repository update, all operators should acknowledge these hard stops.

| Do not do this | Why it is prohibited | Correct response instead |
|---|---|---|
| Restart a GPU to rerun P2 validation “for confidence” | It would create another outcome path after sealing | Use existing hashes, logs, and sealed outputs; record any missing artifact as an archival issue |
| Read either P2 test data file again | Gate V consumed the one permitted test touch | Use the sealed Gate V JSONs and test-access log |
| Test A1 or A3 | #306935 restricts test evaluation to A2 only | State that A1/A3 remain validation-only arms |
| Replace a sealed output JSON | It breaks auditability | Preserve the original; a later diagnostic, if ever legitimate, must have a separate filename and nonconfirmatory status |
| Upload `test.jsonl` to a public repository or ResearchBox pack | It may compromise the legacy holdout and violates the deposit plan | Deposit hashes, manifest entries, evaluator configuration, and scalar output—not the raw protected file |
| Add an unregistered P2 seed, replay fraction, SFT run, or tokenizer swap to the P2 paper’s confirmatory table | It changes the study and invites post-outcome selection | Give it a future-study/exploratory label and a separate protocol |
| Backdate or call a new P3 outcome-independent | Gate U/V values are now known | Label P3 a post-P2 follow-up unless an independently frozen earlier P3 plan exists |

## 3. Evidence preservation: first operational priority

The target is a **local, hash-verified, read-only P2 archive** that is sufficient to audit every reported claim without containing credentials, passcodes, or raw protected test text.

### 3.1 Create the definitive archive manifest

Create one top-level `p2_closeout_manifest.json` or CSV. Each row must include, at minimum:

| Field | Required content |
|---|---|
| Logical artifact name | Human-readable role, e.g., `Gate U validation seal` |
| Relative archive path | Path inside the close-out archive |
| Source path | Original local path or remote source description |
| SHA-256 | Actual hash of archived file |
| Byte size | Actual size |
| Copy/verification UTC time | ISO-8601 UTC timestamp |
| Sensitivity classification | `public`, `controlled`, or `excluded` |
| Verification status | `hash matched`, `not applicable`, or a documented exception |
| Notes | Parent/branch relation or reason for exclusion where useful |

### 3.2 Minimum public/controlled artifact inventory

| Artifact family | Minimum contents | Classification |
|---|---|---|
| Governing documents | AsPredicted #306935 PDF, protocol SHA, dated operational clarification/addendum files | Public |
| Source provenance | Pinned commit, git status/diff record, environment files, dependency lockfiles/container metadata | Public |
| Data provenance | Corpus/config revisions, split and input manifests, file hashes, A3 mix manifest, token counts, but not necessarily raw corpora | Public or controlled depending on licensing |
| Tokenizer | `tokenizer.pkl`/`token_bytes.pt` hashes and release copies if licensing permits | Public |
| Parent and branch receipts | A0/A1/A2/A3 SHA records, lineage table, run cards, launch commands, terminal-step evidence | Public |
| Training and evaluation evidence | H/I/P0/Q/R/S/T/U/V/W cards, logs, evaluator source, full validation JSONs, Gate V output JSONs, `gate-u-seal.json`, test-access log | Public except any file containing protected raw text |
| Weights | A0/A1/A2/A3 final `.pt` files, hash file, model card, release manifest | Controlled until Hub release; then public if licensing/consent check passes |
| Paper materials | `paper.tex`, bibliography, tables/figures, Pandoc outputs, PDF build log, rendered PDF when compiled | Public |
| Credentials and secrets | ResearchBox passcodes, Runpod tokens, SSH keys, cookies, private host details | **Excluded** |
| Raw protected test inputs | WT103 test package and P1.1 `test.jsonl` | **Excluded** from public deposit; record only the prescribed identity/hash where appropriate |

### 3.3 Hash and immutability checks

Perform, record, and independently spot-check the following before deleting the retained volume:

1. Verify the local copies of A0, A1, A2, and A3 final checkpoints against their recorded SHA-256 receipts.
2. Verify `gate-u-seal.json`, `gate-v-test.json`, `test_access_log.json`, `LOCK.json`, and each relevant run card are present and hashes are recorded.
3. Verify that the paper’s values match the sealed JSON values exactly, including signs and decimal precision for \(C_{EN}\), \(G_{TL}\), A3 contrasts, and both secondary test BPBs.
4. Verify that archive paths contain no raw `test.jsonl`, no P1.1 `test_bpb` reuse file, no `.env`, no SSH private key, no access token, and no ResearchBox passcode.
5. Make the final archive directory read-only after successful manifest verification.
6. Retain two independent copies: a local immutable archive and the eventual external deposit/repository release.

If an expected file is missing, do **not** recompute any result. Recover the pre-existing artifact from a verified backup or remote volume if possible, log the recovery, hash it, and state precisely what could not be reconstructed if recovery fails.

## 4. ResearchBox 8763 deposit procedure

The local package already prepared at `transfer/p2-researchbox-8763-20260819/` is a documentation deposit. It deliberately contains no raw protected test file, passcode, or model weight.

### 4.1 Operator procedure

1. Log in to [ResearchBox 8763](https://researchbox.org/8763) personally. Do not send passwords or passcodes through chat, Git, an archive, or an issue tracker.
2. Before uploading, enumerate the local package and confirm it matches the close-out manifest. Verify absence of excluded secrets and raw protected test data.
3. Upload the package as a **new P2 close-out deposit**; do not overwrite a P1.1 deposit or silently replace an earlier P2 draft.
4. Complete required deposit metadata with the study title, authorship, P2 run ID, AsPredicted #306935 link, source repository URL, model repository URL, protocol SHA, and a concise data-access statement.
5. State explicitly that the deposit contains run documentation and reproducibility metadata, not raw protected legacy holdout text or model weights.
6. After upload, capture the permanent identifier/URL, package version, uploader, UTC timestamp, and any platform checksum or file inventory.
7. Add those facts to the P2 close-out manifest and the paper’s data/code availability statement.
8. Open/download a non-sensitive deposited file through the ResearchBox interface and verify it matches the local SHA-256. This is a delivery check, not a new scientific evaluation.

### 4.2 Suggested deposit description

> This deposit documents P2, a preregistered one-seed continual-pretraining study of English retention after frozen Tagalog continuation in nanochat. It contains the governing preregistration, execution protocol, environment and source provenance, gate receipts, sealed validation and authorized test outcome records, and paper source. It excludes raw protected legacy holdout text, credentials, and model weight files. P2’s primary validation conclusion is that the registered English-retention-cost pattern was not observed in this fixed apparatus, while the registered Tagalog-gain pattern was observed. A3 is reported as a predeclared document-mix trade-off arm, not mitigation.

## 5. Hugging Face model release procedure

The new repository is [pageman/nanochat-filipino-p2-en-then-tl](https://huggingface.co/pageman/nanochat-filipino-p2-en-then-tl). It is separate from P1.1 and must remain visibly separate.

### 5.1 Decide the release scope before upload

The ideal P2 model release contains the final checkpoints required to reconstruct the branch architecture:

| Candidate artifact | Recommended release status | Why |
|---|---|---|
| A0 d20 frozen English parent | Release with SHA and immutable-parent description | Enables lineage verification |
| A1 final extra-English child | Release with SHA and branch card | Enables matched-control inspection |
| A2 final Tagalog-continuation child | Release with SHA and branch card | Central intervention artifact; only tested branch |
| A3 final document-mix child | Release with SHA and branch card | Predeclared trade-off arm; prevents selective availability |
| Optimizer states / intermediate checkpoints | Do not release by default | Not needed for inference; release only if independently justified and clearly labeled |
| P1.1 weights under P2 repo | Never upload | Violates study separation and invites lineage confusion |
| Raw test material | Never upload | Protects the P2/P1.1 test boundary |

Before uploading `.pt` files, confirm their recorded SHA-256 hashes, byte sizes, and model-card names. Use the platform’s large-file mechanism if necessary. Do not upload a file merely because its name is convenient; the hash is the identity.

### 5.2 Required model-card sections

The Hub README should contain at least these sections:

1. **Identity and scope:** P2 only; not P1.1; not trained from `p1-fixed-d20-3x`; not an instruction-tuned/chat/SFT model.
2. **Research purpose:** controlled, preregistered continual-pretraining evidence—not a broad leaderboard or production deployment claim.
3. **Branch map:** A0 → A1/A2/A3, all d20, same parent, same phase-2 budget, fresh optimizer, English BPE.
4. **Data provenance:** WT103-raw and documented frozen P1.1 Tagalog train input; no raw protected holdout release.
5. **Evaluation table:** sealed full validation outcomes and A2-only secondary test outcomes; label test results secondary and disclose the P1.1 legacy-holdout status.
6. **Interpretation boundary:** English-cost prediction not observed; Tagalog-gain pattern observed; one seed; no significance test, confidence interval, population-effect, or universal-language claim.
7. **Checksums:** model filename, SHA-256, byte size, and role for every released `.pt` file.
8. **License and use restrictions:** confirm the selected license is compatible with code, model, and data provenance; include research-only caveats if desired, but do not invent legal terms.
9. **Reproduction:** link to code and ResearchBox deposit; state exact commit and environment requirements.

### 5.3 Post-upload verification

After the user uploads model files:

1. Download or stream each uploaded checkpoint and compare its SHA-256 to the local release manifest.
2. Verify the displayed filenames make A0/A1/A2/A3 distinct.
3. Verify no P1.1 tag, `p1-fixed-d20-3x` path, test file, token, passcode, or secret entered the repository history.
4. Freeze the release manifest and add the Hub revision URL/commit to the ResearchBox deposit and paper.

## 6. Paper completion and PDF production

### 6.1 Source of truth

`docs/papers/p2-cf-english/paper.tex` is the current source. The old 16 August PDF is obsolete and must not be released as the P2 results paper. Pandoc output is a convenience export, not proof that the paper is final.

### 6.2 Required paper checks before compiling

| Check | Acceptance criterion |
|---|---|
| Title and abstract | Describe a preregistered, leakage-controlled, one-seed continual-pretraining study; avoid claiming universal catastrophic forgetting or a benchmark win |
| Methods | Match #306935 on parent, child arms, frozen input roles, English BPE, budget, validation seal, and A2-only test rule |
| Results | All numbers match sealed JSONs; A3 labeled trade-off arm; secondary tests segregated from primary contrasts |
| Interpretation | English-cost pattern “not observed,” Tagalog-gain pattern “observed in this apparatus”; no causal overstatement beyond the design scope |
| Tables | Include A0 provenance separately from A1/A2/A3 primary comparison; label A0 Tagalog baseline descriptive |
| Test description | Explain P1.1 `test.jsonl` is a legacy external holdout and that the prior P1.1 test BPB was not reused |
| Limitations | One seed; specific corpora/tokenizer/architecture/budget; no significance testing; no SFT/CORE; no direct external benchmark claim |
| Availability statement | Link code, Hub, ResearchBox; distinguish metadata availability from protected raw holdout text |
| Author check | Dr. Charibeth Cheng’s framing and authorship review are complete before public circulation as a co-authored paper |

### 6.3 Compile procedure

1. Work from a clean copy of the current paper source and bibliography. Record git commit/hash or a source-archive SHA.
2. Use a versioned LaTeX environment with the required packages. Record compiler name/version and the exact command in `paper_build_receipt.txt`.
3. Compile twice if the bibliography/cross-reference system requires it; use the same source files for every pass.
4. Inspect the PDF visually for clipped tables, wrong decimals, broken references, empty bibliography fields, overfull boxes that hide meaning, and accidental inclusion of stale 16 August text.
5. Extract text from the resulting PDF and compare the primary values, test values, and words **“not observed”**, **“observed”**, **“one seed”**, and **“secondary”** against the source/checklist.
6. Hash the final PDF, TeX source archive, and build receipt. Place all three in the archive/deposit.
7. If compilation cannot be performed locally, do not substitute the old PDF. Leave PDF status as `pending compiler environment`, publish source/Pandoc formats only if clearly labeled, and compile later in a clean documented environment.

## 7. Public reporting and communication kit

### 7.1 Technical summary

> P2 is a preregistered one-seed continual-pretraining experiment that compared frozen Tagalog continuation (A2) against a matched extra-English continuation control (A1), both initialized from the same immutable English d20 parent under equal phase-2 model-visible-token budgets. On sealed validation, the registered English-retention-cost prediction was not observed: \(C_{EN}=EN(A2)-EN(A1)=-0.073991\). The registered Tagalog-adaptation-gain pattern was observed: \(G_{TL}=TL(A2)-TL(A1)=-3.883048\). A3, a pre-frozen 50/50-document mix, is reported as a trade-off arm rather than mitigation. A2 alone received the one registered secondary English and legacy-Tagalog test evaluation.

### 7.2 Layperson summary

> The study trained a small English-language model and then compared three equally sized follow-up lessons: more English, Tagalog, or a fixed English–Tagalog mix. In this specific controlled setup, learning Tagalog greatly improved the model’s ability to predict held-out Tagalog text. It did **not** produce the predicted loss on held-out English text when compared with giving the model more English practice. This is one carefully controlled model experiment, not proof that all language models or all languages behave this way.

### 7.3 Claims to avoid

Do not say that the experiment proves there is no catastrophic forgetting; proves Tagalog enhances English; establishes language-general transfer; beats a benchmark; validates an LLM for deployment; or measures instruction-following. Do not present the one-seed result as a formal significance test or population estimate.

## 8. Website and project-index update

Update the interactive guide only after the paper table and archive manifest are verified. The website should display a **status summary**, not raw unsealed working material.

| Website field | Recommended content |
|---|---|
| Study status | “P2 empirical execution complete: Gates A–W recorded” |
| Primary result | English-cost pattern not observed; Tagalog-gain pattern observed, with clear one-seed scope |
| Test boundary | “One A2-only secondary test event completed; A1/A3 were not tested” |
| Links | AsPredicted, code, Hub, ResearchBox once uploaded, and paper once compiled/released |
| Data safety | No raw protected holdout files or credentials exposed |
| Follow-on wording | P3 is post-P2 unless earlier independent freezing is documented; P4 is a future multi-seed/robustness design |

Do not quietly modify prior P1.1 status or blend P1.1 and P2 result tables. P1.1 remains a separate fixed-budget depth study with its own outstanding close-out work.

## 9. Infrastructure and cost closure

The A40 pod is stopped. That eliminates GPU runtime billing, but the retained 80-GB volume may still incur storage cost.

| Condition | Correct infrastructure action |
|---|---|
| All required P2 artifacts are local, hash-verified, and externally deposited/backed up | Terminate the retained volume to stop storage charges |
| A required artifact has not been retrieved or hash-verified | Retain volume temporarily, recover only the pre-existing artifact, update manifest, then terminate |
| P1.1 needs official CUDA full-validation later | Start a new explicitly P1.1-scoped GPU job from P1.1 artifacts; do not reopen P2 or reuse its ledger |
| P3/P4 work begins later | Provision a new separately recorded environment after a new preregistration; do not treat the retained P2 volume as a blank continuation space |

Record the final pod status, volume ID, termination time, and archive-verification receipt. Rotate any old infrastructure credentials that may have been exposed during earlier operations.

## 10. P3, P4, and P1.1 separation

### P3

P3 is not an amendment or rescue of P2. Because P2 is unblinded, a newly filed P3 must state that it is a **post-P2 follow-up**. It may test the reverse Tagalog-parent → English-continuation question on new P3 outcomes, but it cannot claim that its direction, thresholds, or design were chosen without P2 knowledge.

### P4

P4 is the appropriate place for a fresh-seed replication core and, if separately preregistered, a bounded Sobol-style robustness slab. It must report every predeclared seed/design point and must not select a favorable configuration to reinterpret P2.

### P1.1

P1.1 remains separately open for its own final full `val_bpb_full` close-out, baselines, locked depth-selection record, and its own one-test-touch rules. A P1.1 CUDA evaluation is not a P2 Gate W action and must retain its own ledger, paths, paper language, and source environment.

## 11. Final sign-off table

Use this table as the last operator hand-off. Do not mark a row complete merely because a command ran; attach a path, hash, URL, or signed statement.

| # | Close-out item | Evidence required | Owner | Status |
|---:|---|---|---|---|
| 1 | Local P2 archive complete | `docs/run-cards/p2/p2-20260817T150944Z-de99f8a/p2_closeout_manifest.json`; frozen tree `transfer/p2-closeout-archive-20260819` (444/555) | Operator | ☑ 2026-08-19T08:20Z |
| 2 | A0/A1/A2/A3 checkpoint identities verified | Local `data/cache/p2-20260817T150944Z-de99f8a/` A0 `bd35a858…e1d`, A1 `e2881049…85d`, A2 `2b01acf8…026`, A3 `d6c62bb7…368` (all hash matched; 2 663 446 486 bytes each) | Operator | ☑ |
| 3 | Gate U/V/W records preserved | U seal `eb902b71…5751`; V `802a812d…0072`; ledger `fa95b9b0…a2d8` (`authorized_touches=1`); LOCK `1397ce00…8fb9`; Gate W card updated | Operator | ☑ |
| 4 | No raw protected test files/secrets in archive | Exclusion scan empty on archive and ResearchBox pack; prescribed test SHAs recorded without copying raw files | Operator | ☑ |
| 5 | ResearchBox 8763 upload complete | Local pack refreshed at `transfer/p2-researchbox-8763-20260819` (no `test.jsonl`/passcode/`.pt`). Human login upload + post-upload hash spot-check still required | User/operator | ☐ local pack ready; **upload pending** |
| 6 | Hub weights published or deliberately deferred | Complete-set SHAs + expanded card in `docs/run-cards/p2/HF-MODEL-CARD-p2.md`. Hub currently README + `WEIGHTS_SHA256.txt` only. **Deferred** until A0+A1+A2+A3 `.pt` can be uploaded together. P1.1 Hub untouched | User/operator | ☑ deferred (weights not uploaded) |
| 7 | Paper source reconciled with seals | `paper.tex` contains all sealed six-decimal values and required phrases; A3 labeled trade-off; tests secondary. Cheng is not a coauthor | Operator | ☑ numbers; authors still own circulation |
| 8 | Current PDF compiled | tectonic 0.17.0; `paper.pdf` SHA-256 `1b6fce09f75cf052cffb363e9eaa0ae45297523da4542323c035b4e6c3362c16`; receipt `paper_outputs/paper_build_receipt.txt`; pypdf text check passed (Unicode minus on \(C_{EN}\)/\(G_{TL}\)) | Operator | ☑ |
| 9 | Website status updated | Copy-ready page `docs/run-cards/p2/PUBLIC-STATUS.md`. Live site not edited in this close-out | Operator | ☐ source ready; **live URL pending** |
| 10 | P2 results release statement approved | Technical + lay summaries are in PUBLIC-STATUS and the checklist §7; author sign-off not recorded | Authors | ☐ |
| 11 | Volume disposition recorded | Pods `8ik4ix7j8iju9u` and `xk8orhscuk2jsu` remain EXITED, **not terminated**. 80 GB volume retained until ResearchBox upload and Hub complete-set backup exist. Per user: do not turn off pods yet | User/operator | ☑ retained (reason recorded) |
| 12 | Future-study register updated | `p3-post-unblinding.md` now includes P4 and P1.1 separation | Authors | ☑ |

## 12. Definition of done

P2 close-out is complete when all of the following are true:

1. The sealed scientific record can be audited from local and external copies without recomputation.
2. The ResearchBox deposit is uploaded and verified, with no raw protected holdout text or secret material.
3. The Hub release is either hash-verified and accurately documented, or its intentional deferral is stated openly.
4. The current paper source and compiled PDF agree with the sealed result artifacts and do not use the obsolete 16 August PDF.
5. Public communication uses the narrow registered interpretation and accurately labels A3 and A2-only tests.
6. The P2 GPU/volume is terminated once archive retention is safe.
7. P1.1, P3, P4, and any exploratory work are visibly separated from P2’s closed confirmatory record.

At that point, P2 becomes a completed, citable methodological and empirical study—not a live experiment awaiting a more favorable rerun.

## References

[1] [AsPredicted #306935: P2 — English retention after Tagalog continuation](https://aspredicted.org/xa56bs.pdf).

[2] [P2 model repository: `pageman/nanochat-filipino-p2-en-then-tl`](https://huggingface.co/pageman/nanochat-filipino-p2-en-then-tl).

[3] [P1.1 model repository: `pageman/nanochat-filipino-p1-fixed-d20-3x`](https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x).
