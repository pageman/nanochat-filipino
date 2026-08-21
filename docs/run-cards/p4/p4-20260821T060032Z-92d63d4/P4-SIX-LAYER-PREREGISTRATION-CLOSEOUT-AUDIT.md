# P4 Six-Layer Preregistration Close-Out Audit

## 1. Status, purpose, and authority

This audit identifies what must be closed before P4 can be described as complete under six distinct layers of obligation:

1. **Explicit** — literally promised in filed AsPredicted #307591.
2. **Implicit** — necessary for the filed design to mean what it says.
3. **Inferred** — necessary to report the design and result without overstating it.
4. **Extrapolated** — necessary to make the work reproducible, inspectable, and responsibly released.
5. **Residual** — work still open at the last status update.
6. **Hidden** — failure modes that can silently invalidate interpretation despite apparently completed gates.

> **Authority order:** filed AsPredicted #307591 PDF -> SHA-bound master protocol -> SHA-bound gate bible -> SHA-bound pre-filing addendum -> dated technical incident/deviation record -> exploratory material. No downstream item can amend the filed PDF.

**Outcome-protection rule.** This audit remains an execution-control artifact: it cites receipts, hashes, timestamps, and grammar *labels*, not BPB scalars, floor gaps, cell values, or contrast magnitudes. Numeric cells live only in the Gate X released bundle and paper.

**Companion.** Use with `/Users/paulpajo/Downloads/P4 Explicit Preregistration Close-Out Checklist.md` (E-01–E-125). That file is the PDF-literal map; this audit is the interpretability / reproducibility / honesty boundary.

## 2. Current status dashboard

Dated **2026-08-21**, run ID `p4-20260821T060032Z-92d63d4`. LOCK `status=gate_w_pass`, `unblinding_status=gate_x_unblinded`.

| Status area | State | What still cannot be inferred |
|---|---|---|
| Filing and Gate 0 | Filed #307591; hashes archived; dummy lockbox pass | — |
| Gates A–G | `PASS` | — |
| Gate H | `PASS`; d4 smoke quarantined, not parent | — |
| Gate I d8 + d20 | Both terminal step 294, health/reload pass | — |
| P0-T | CUDA `PASS`; both depths both floors | — |
| C0 / C1 / C2 / C3 | Frozen C0; serial R→S→T from same C0 SHA | — |
| Gate U | Seal SHA `5c7287752ba1abb3…`; `test_access=0` | — |
| Gate V | One C3-only event; two components; C1/C2 untested | First V attempt TECHNICAL (missing JSONL) before any score; rerun once |
| Gate X | Preflight then one-time release 2026-08-21T13:42:01Z | — |
| Gate W | Paper + local archive + Hub **deferred** | Public Hub, post-X ResearchBox deposit, git push, credential rotation, GPU stop |
| Outcome access | `p4_outcome_access_count=1` after recorded X | No new val/test after X |

## 3. Layer I — explicit obligations

The companion **P4 Explicit Preregistration Close-Out Checklist** enumerates 125 clause-level obligations, `E-01` through `E-125`. Families E-01–E-118 are `[x]`; E-120 and E-123 are `[x]`; **E-119, E-121, E-122, E-124, E-125 remain `[ ]`**.

| Explicit family | Companion IDs | Required closure proof | Family status |
|---|---:|---|---|
| Filed authority and non-amendment | E-01–E-10 | Filed PDF, local SHA, protocol-hash comparison, and no unrecorded amendment. | `[x]` |
| Gate 0 and lockbox identity | E-11–E-18 | P4 run identity, dummy-lockbox receipt, initial access counters, and raw-test isolation. | `[x]` |
| Pin, environment, no-reuse | E-19–E-27 | Pin diff, P4-only cache/environment, forbidden-weight scan, Hub write-target scan. | `[x]` |
| Data/split identity | E-28–E-39 | Six JSONL hashes, split-origin receipt, overlap report, unmodified-row assertion. | `[x]` |
| Tokenizer/evaluator | E-40–E-49 | Both tokenizer hashes, read-only receipt, exact evaluator/floor configuration. | `[x]` |
| C3 treatment | E-50–E-59 | Quota, deterministic schedule, packed-stream/origin-mask manifest, no-wrap proof. | `[x]` |
| Parent/Gate I | E-60–E-68 | d8/d20 terminal receipts, CUDA evidence, fresh-init proof, no mid-run selection. | `[x]` |
| P0-T | E-69–E-76 | CUDA-only two-depth/two-floor sealed result with status-only external output before X. | `[x]` |
| C0 and children | E-77–E-87 | Immutable C0 lineage, C1/C2/C3 fresh-optimizer receipts, quarantines if needed. | `[x]` |
| Gate U | E-88–E-98 | Full six-cell validation seal, U-before-V timestamp proof, lockbox receipt. | `[x]` |
| Gate V | E-99–E-106 | Exactly one C3-only event, two named component reads, C1/C2 never tested. | `[x]` |
| Gate X | E-107–E-113 | Status-only preflight, one-time bundle release, contrast recomputation, access transition. | `[x]` |
| Gate W | E-114–E-125 | Paper and local archive `[x]`; joint deferral `[x]`; RB deposit / git-Hub publish / public re-hash / credential rotation / GPU stop still open. | **partial** |

### 3.1 Explicit closure conditions that cannot be treated as “administrative”

- [x] **XL-01.** C3 must retain exactly 9,633,792 Tagalog and 9,633,792 English **source-content** tokens in the first consumed `N x B` stream, using the filed tokenizer and deterministic schedule. Gate E; mix SHA `f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107`.
- [x] **XL-02.** C1, C2, and C3 must descend from exactly the same immutable d20 C0 checkpoint, not merely a checkpoint with the same tag. Parent SHA `34e069646be4158979809c023691188439047d6cbee08a141db432c78bcf02e2` on Q/R/S/T.
- [x] **XL-03.** Every child must begin with a fresh optimizer (`load_optimizer=False`) and use the filed 294-step budget, warmup 14, and terminal-checkpoint rule. Gate G freeze; R/S/T step 294.
- [x] **XL-04.** P0-T must pass at both d8 and d20 under CUDA-only official evaluation before any child token. `gate-p0-t.json` `PASS`; Q after P0-T.
- [x] **XL-05.** Gate U must be sealed while `test_access=0`; this timestamp order is not optional. U 2026-08-21T13:28:05Z; V 13:31:01Z.
- [x] **XL-06.** C1 and C2 must never be tested, even if the validation results are surprising. Test log tags `p4-c3-mix-d20` only.
- [x] **XL-07.** The P4 result must be released as the joint outcome of `R_TL` and `A_EN`, not a retrospective best-arm choice. Seal + `fill_p4_tables.py` grammar from both filed inequalities; no extra arm.

## 4. Layer II — implicit obligations

### 4.1 Causal-comparison integrity

- [x] **IM-01.** The same C0 must be byte-identical for all child loads; lineage cannot be inferred from matching filenames. Identical `parent_c0_sha256` on R/S/T.
- [x] **IM-02.** C1 and C2 must differ from C3 in the intended stream composition, not in hidden batch size, context length, optimizer state, device type, precision policy, or checkpoint choice. Shared G freeze argv; streams `c1_tl` / `c2_en` / `c3_mix`; A40.
- [x] **IM-03.** The fresh-parent claim requires no load, resume, or optimizer-state transfer from P1.1/P2/P3 or the H smoke run. Smoke quarantined; I from scratch; children `load_optimizer=False` from C0.
- [x] **IM-04.** The C3 intervention is the **source-content language-share rule**, not document count, byte share, or an undocumented packer artifact. LOCK `q_tl_clock=source_content_tokens_no_bos_no_pad_no_pack_no_crop`.
- [x] **IM-05.** The C3 origin mask must be linked to the exact packed sequence consumed by the trainer; a pre-pack document-list audit alone is insufficient. Gate E packed-stream freeze + consumed-order receipt.
- [x] **IM-06.** The source-content quota must be established before model-visible budget completion, with any boundary/BOS policy explicitly reconciled to the filed addendum. E before T; `D_phase2=19267584` model-visible; source-content quotas exact.
- [x] **IM-07.** P0-T parent eligibility is a capability screen, not a comparison result and not a reason to select depth. d8 eligibility-only; d20 only C0; no d8-vs-d20 ranking in I receipt.
- [x] **IM-08.** d8 is eligibility-only; the d20 parent is the only legal C0. A d8 fallback after d20 difficulty is prohibited. `not_occurred`.
- [x] **IM-09.** In-loop loss, samples, partial validation, and metadata do not substitute for official full-validation outcomes. Trainer eval off; official `evaluate_bpb` at U/V/P0-T.
- [x] **IM-10.** A test event has two named component reads but counts as one authorized event; counters and wording must remain consistent. `authorized_touches=1`, `component_evaluations=2`.

### 4.2 Measurement integrity

- [x] **IM-11.** `val_bpb_full` uses the same tokenizer for every P4 arm and both languages, as filed. Carry-forward pair; both artifact SHAs.
- [x] **IM-12.** The official evaluator must consume full frozen validation inputs and must not silently fall back to an incomplete evaluation window. Full-split cells; evaluator SHA `9afebdb405aaac0bb4287051d9b6f5d16f56d6dd9269a1e6c2c5df29becbced1`.
- [x] **IM-13.** The byte-unigram floor is fitted on the filed training corpus only and is not refit after parent/child work begins. Frozen at P0-T; released `byte_unigram_tagalog_val.json` identity unchanged.
- [x] **IM-14.** Untrained floors use the filed seed/configuration, not a conveniently weaker random initialization. P0-T CUDA path; same-depth untrained floors in eligibility JSON.
- [x] **IM-15.** Evaluation hardware and numerical configuration must match the filed CUDA-only authority for P0-T/U/V. NVIDIA A40 receipts `gpu=true`.
- [x] **IM-16.** The same BPB formula must govern parent floor checks, child validation, and C3-only test reporting. Single frozen `evaluate_bpb.py`.

### 4.3 Blinding and access integrity

- [x] **IM-17.** Safe logs must never accidentally print lines containing BPB, loss-derived decision values, contrast values, or test scores. X preflight check 10 PASS.
- [x] **IM-18.** Lockbox files must not be readable through a dashboard, tail command, error trace, notebook output, Hub card, or generated paper preview. Pre-X Hub stub scalar-free; paper built after X; no Hub weights with eval JSON uploaded.
- [x] **IM-19.** The Gate X operator must not have previewed scalar filenames/content through a file browser before the recorded unblinding event. Preflight hashed lockbox files without printing scalars; `gate_x_unblind.py` was the recorded open.
- [x] **IM-20.** All script paths that could read tests must be disabled or physically absent until Gate V. V ran only after U seal; Policy A.
- [x] **IM-21.** A technical incident is not a license to inspect outcomes; its card must describe only safe status and remediation. V JSONL miss failed at `require_hash` before any test score; rerun from U with test_access still 0 at U.

## 5. Layer III — inferred reporting obligations

- [x] **IN-01.** Describe P4 as a **post-P3, outcome-informed** study; never present it as outcome-independent replication. Paper Introduction/Availability.
- [x] **IN-02.** Describe C3 as a token-share-locked mixture intervention; never call it byte balanced unless an exploratory byte-balanced study was separately run and clearly labelled exploratory. Paper; byte-balanced deferred to P6-B.
- [x] **IN-03.** Do not write “P3 B3 was corrected” or “P3 B3 was fixed.” Paper uses required negations only.
- [x] **IN-04.** If both joint thresholds are met, use narrow wording: the specified mixture satisfied the filed one-seed trade-off criteria in this apparatus. Applicable branch: companion E-96 `grammar=both`; paper uses filed both-sentence plus the filed narrow mitigation sentence (not a generic CF claim).
- [x] **IN-05.** If only `R_TL` meets its rule, report a Tagalog-retention advantage without claiming preserved English acquisition. **N/A** (not the realized branch).
- [x] **IN-06.** If only `A_EN` meets its rule, report English acquisition advantage without claiming reduced retention cost. **N/A**.
- [x] **IN-07.** If neither meets its rule, report neither joint criterion was satisfied; do not rescue the result through C0 descriptive English, tests, B3 history, or a different cutoff. **N/A**.
- [x] **IN-08.** State that the study has one seed and no confidence intervals or p values by design. Paper Limitations.
- [x] **IN-09.** Do not claim a population effect, universal forgetting law, human-language competence, or a general mitigation solution. Paper Discussion; narrow sentence only.
- [x] **IN-10.** Explain the active controls: C1 is source-language retention control; C2 is pure-English comparator; C3 is the pre-frozen mixture. Paper Methods.
- [x] **IN-11.** State that Gate V is descriptive secondary evidence and does not create a test-set trade-off contrast. Paper Results; `does_not_alter_sealed_contrasts`.
- [x] **IN-12.** State that future P5/P6-style fresh seeds and seed panels are required to address initialization stability. Paper Limitations; W.8: P5 multi-seed, P6-B byte-balanced.

## 6. Layer IV — extrapolated reproducibility and stewardship obligations

### 6.1 Artifact preservation

- [x] **EX-01.** Preserve the filed PDF and all three SHA-bound documents exactly as used at filing. Unedited Q8 hashes.
- [x] **EX-02.** Preserve a machine-readable final lock, run-card index, gate ledger, test-access log, and outcome-access log. `LOCK.json`; `manifests/p4/`; `P4_UNBLINDING_EVENT.json`.
- [x] **EX-03.** Preserve exact parent/child command records, environment fingerprint, image/torch/CUDA identifiers, and GPU receipt. Gate G freeze; H/I/P0-T/Q–V CUDA receipts; A40.
- [x] **EX-04.** Preserve tokenizer artifacts, packed C1/C2/C3 manifests, origin mask, source JSONL hash table, and evaluator copy. Gates B/E/F; `scripts/p4/evaluate_bpb.py`.
- [x] **EX-05.** Preserve terminal checkpoint hashes, byte sizes, lineage, and read-only status at archive time. Local C0–C3 `model_000294.pt` SHA-matched; mode 444 on children.
- [x] **EX-06.** Preserve failed/partial child outputs only as quarantined technical artifacts; mark them nonconfirmatory and excluded. Smoke quarantined. No partial child trajectory. V miss is a test-host incident, not a child ckpt.

### 6.2 Release integrity

- [x] **EX-07.** Release C0/C1/C2/C3 jointly, or publish a dated joint deferral that explains why no subset is being privileged. LOCK `hub_status=deferred` 2026-08-21; hub README.
- [ ] **EX-08.** Give every released weight a model card with lineage, tokenizer SHA, corpus/split hashes, filed registration, terminal step, scope, and known limitations. Stub exists; Hub cards not published because weights are deferred.
- [x] **EX-09.** Do not upload raw test JSONL, protected validation data if restricted, secrets, SSH material, access credentials, or ResearchBox passcodes. `not_occurred`; passcode null in LOCK.
- [ ] **EX-10.** Re-download released weights and verify public SHA-256 values before claiming a successful release. N/A until joint Hub upload; local SHA256SUMS under EX-16.
- [ ] **EX-11.** Deposit code, protocol, manifests, safe receipts, and paper sources in ResearchBox or equivalent; keep raw/model artifacts in their appropriate repository class. Box **#8869** exists (not Make Public). Post-X paper + released-seal deposit still operator.
- [x] **EX-12.** Update the website only after claims match the final sealed/unblinded paper language. Local `docs/p4/README.md` matches X/W + deferral. Public git/site push still EX-08/E-121.

### 6.3 Infrastructure close-out

- [x] **EX-13.** Copy required logs/checkpoints/manifests to independent storage before volume termination. Laptop cache holds lockbox/released JSON and C0–C3 `.pt`. Volume **not** terminated.
- [ ] **EX-14.** Stop GPU billing when no filed compute remains; retain only a separately costed volume if artifacts are not yet archived. Pod `cjaakd9i2w8x7t` was still **RUNNING** at last check ($0.44/hr). No filed compute remains; stop is operator.
- [ ] **EX-15.** Rotate Runpod, SSH, Hugging Face, and other credentials if exposure is plausible. No rotation receipt.
- [x] **EX-16.** Record the final location, size, hash, and verification time of every archive artifact. `p4_closeout_manifest.json` + `SHA256SUMS`; released lockbox hashes matched pod.

## 7. Layer V — residual ledger

| Residual ID | Required closure | Current state |
|---|---|---|
| R-01 | Finish d20 fresh TL0 at fixed terminal step with receipt/hash/reload proof | `[x]` SHA `34e06964…` |
| R-02 | Mark Gate I pass only after both d8 and d20 satisfy terminal technical checks | `[x]` |
| R-03 | Run P0-T two-depth/two-floor CUDA-only eligibility | `[x]` PASS |
| R-04 | Freeze C0 from eligible d20 parent | `[x]` Q |
| R-05 | Run C1/C2/C3 child branches from C0 | `[x]` R then S then T |
| R-06 | Seal six-cell Gate U validation and compute registered contrasts in lockbox | `[x]` |
| R-07 | One C3-only Gate V test event after U | `[x]` |
| R-08 | Gate X status-only preflight and one-time unblinding | `[x]` |
| R-09 | Paper, archive, Hub, ResearchBox, website, credential, and volume close-out | **Partial:** paper + local archive `[x]`; Hub deferred `[x]`; RB post-X deposit, git/Hub publish, credential rotation, GPU stop `[ ]` |

### 7.1 Residual closure order

Filed order **I -> P0-T -> Q/C0 -> R -> S -> T -> U -> V -> X -> W** was followed. Remaining R-09 items are stewardship, not new science. Do not add C4 or rerun val/test.

## 8. Layer VI — hidden-risk register

| Hidden ID | Risk | Disposition |
|---|---|---|
| HN-01 | Smoke used as TL0/C0 | **closed_controlled** — smoke quarantined; C0 = I d20 SHA |
| HN-02 | d8 treated as C0 fallback | **closed_controlled** — Q from d20 only |
| HN-03 | C3 quota drifts in consumed stream | **closed_controlled** — Gate E first `N x B` exact quota, no wrap |
| HN-04 | Source-content vs model-visible clock mix-up | **closed_controlled** — LOCK clock string; `D_phase2` separate |
| HN-05 | Partial C2/C3 resumed from own optimizer | **closed_controlled** — `not_occurred`; children terminal 294 from C0 |
| HN-06 | Hidden seed/order/precision drift across children | **closed_controlled** — shared G argv; serial R→S→T; A40 |
| HN-07 | English val/test via C3 parquet | **closed_controlled** — parquet non-DV; tests only at V from named JSONL |
| HN-08 | Duplicate EN train rows dropped after filing | **closed_controlled** — Gate D provenance; rows kept |
| HN-09 | Hash mismatch recleaned | **closed_controlled** — `not_occurred` |
| HN-10 | Console/log BPB leak before X | **closed_controlled** — X preflight safe-log PASS |
| HN-11 | U seal after test path read | **closed_controlled** — U `test_access=0`; V after U |
| HN-12 | Test counter vs component reads | **closed_controlled** — 1 event, 2 components |
| HN-13 | Tests used to explain validation | **closed_controlled** — paper: tests secondary; no test contrast |
| HN-14 | C0 EN promoted to primary | **closed_controlled** — descriptive; excluded from formulas |
| HN-15 | “Almost success” ranking | **closed_controlled** — filed four-way grammar only |
| HN-16 | Generic mitigation frame | **closed_controlled** — filed narrow sentence only |
| HN-17 | Null result spawns new mix/seed | **closed_controlled** — no C4; P5/P6-B new filings |
| HN-18 | P3 B3 as P4 calibration | **closed_controlled** — post-P3 disclosure; no retune |
| HN-19 | Tag collision with P1/P2/P3 | **closed_controlled** — `p4-*` namespace |
| HN-20 | C3-alone Hub “best model” | **closed_controlled** via **joint deferral** (not yet uploaded) |
| HN-21 | SHA-bound docs vs runtime scripts | **closed_controlled** — Q8 files unedited; evaluator SHA frozen at A |
| HN-22 | GPU killed before independent archive | **closed_controlled** for copies (laptop has JSON + `.pt`); **open** for billing stop |
| HN-23 | Credential exposure unrotated | **open** — E-124 / EX-15 |
| HN-24 | Paper draft scalars before X | **closed_controlled** — paper filled from released seals after X |
| HN-25 | Post-X “verification” rerun | **closed_controlled** — `no_additional_validation_or_test_eval=true` |
| HN-26 | P4 resolves all CF | **closed_controlled** — one mixture, one architecture, one corpus pair, one seed |

## 9. Six-layer final-decision rule

| Classification | Necessary condition |
|---|---|
| **Open / in execution** | Any core residual from R-01 through R-08 remains. |
| **Protocol stop** | Filed P0-T or another explicit hard-stop rule blocks children; all evidence and stop documentation are complete. |
| **Computationally closed, pending release** | Gate X complete, scalar bundle released once, but W/archive/public release remains open. |
| **Fully closed** | Explicit requirements are resolved; implicit/inferred controls have closure evidence; extrapolated stewardship is complete or explicitly deferred; residuals are zero; hidden-risk ledger is dispositioned. |

> **Current classification: computationally closed, pending release.** Science and local archive are done. Hub joint deferral is documented (EX-07). Not **fully closed** until ResearchBox post-X deposit (EX-11 / E-119), optional joint Hub upload or continued deferral with public re-hash if uploaded (EX-08/10), credential rotation (EX-15), and GPU stop with volume retained as needed (EX-14).

## 10. Gate X safe preflight — executed

Executed 2026-08-21T13:41:44Z (`gate-x-preflight.json`, `ready_for_unblinding=true`) before unblinding 13:42:01Z. All ten status-only assertions passed: I/P0-T/Q–V pass; U before V; test_access 0 at U and one C3-only V event; C1/C2 tests absent; outcome-access 0 before release; six cells sealed; C0–C3 lineage; C3 quota/no-wrap; V JSONL incident documented as technical-before-score; releaser/files/counters in `P4_UNBLINDING_EVENT.json`.

## 11. Companion documents

- `/Users/paulpajo/Downloads/P4 Explicit Preregistration Close-Out Checklist.md` (E-01–E-125)
- Run-card copy: `docs/run-cards/p4/p4-20260821T060032Z-92d63d4/P4-EXPLICIT-PREREGISTRATION-CLOSEOUT-CHECKLIST.md`
- Filed AsPredicted #307591 PDF: https://aspredicted.org/if84km.pdf
- SHA-bound P4 master protocol, gate bible, and pre-filing addendum (do not edit)

Together: **a P4 result is not closed merely because training ends; confirmatory science is now closed, and remaining work is stewardship (deposit, optional joint Hub, credentials, GPU stop) that must not create new P4 evidence.**
