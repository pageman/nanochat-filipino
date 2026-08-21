# P4 Explicit Preregistration Close-Out Checklist

## Purpose and authority

This is an **explicit-only** completion checklist for filed AsPredicted #307591, *P4: token-share mix after fresh TL parent (nanochat, TL-39/WikiText-103)*. It translates the explicit commitments in Questions 1–8 into auditable closure items. It does not add a new arm, metric, dataset, selection rule, or scientific claim.

> **Controlling authority:** filed PDF #307591 first; its SHA-bound master protocol, gate bible, and pre-filing addendum second; dated technical incident records third. No later document can amend the filed registration.

**Current status date: 2026-08-21 (post–Gate W).** Run ID `p4-20260821T060032Z-92d63d4`. LOCK `status=gate_w_pass`, `unblinding_status=gate_x_unblinded`. All confirmatory gates 0 / A–I / P0-T / Q–V / X / W are `pass`. This file remains an execution-control artifact: it cites receipts and hashes, not BPB scalars.

**Still open (operator, not science).** Leave these unchecked until the named action exists: **E-119** post-X ResearchBox deposit of paper + released seals (box #8869 exists; not Make Public); **E-121** GitHub/Hub publication of code and model cards; **E-122** public re-hash of Hub downloads (Hub is jointly deferred); **E-124** credential rotation; **E-125** stop/terminate GPU after that verification. Local SHA256SUMS and Hub deferral documentation are already recorded under E-118 and E-120.

## Status legend

| Mark | Meaning |
|---|---|
| `[x]` | Reported complete with safe evidence; retain named receipt/hash. For former `[!]` items: confirmed nonoccurrence (or, for E-59, filed-narrow reporting after both criteria). |
| `[~]` | In progress; no claim of completion. |
| `[ ]` | Required before that close-out surface can be called complete. |
| `[!]` | Stop condition or prohibition; confirm nonoccurrence rather than perform an action. |

## 1. Filing, scope, and non-amendment commitments

- [x] **E-01.** Archive filed AsPredicted #307591 PDF and record its URL, filing time, and SHA-256. Receipt: `docs/run-cards/p4/AsPredicted-307591.pdf`; SHA `463b29fcff8d7c8099790325fa19d6bcf9ee29f64424c373a380566a6fe9011c`; https://aspredicted.org/if84km.pdf; generated/preregistered 2026/08/20 22:29 PT.
- [x] **E-02.** Preserve the filing’s post-P3 disclosure: P4 was designed after released P3 findings and the P3 B3 document/byte-share ambiguity were known. LOCK `designed_after_p3_gate_x=true`, `p3_gate_x_date=2026-08-20`.
- [x] **E-03.** Preserve the statement that P4 does not amend #306780, #306935, or #307342. LOCK flags true; paper Methods/Availability.
- [x] **E-04.** Preserve the statement that P4 is not “P3 B3 fixed.” LOCK `c3_is_not_p3_b3=true`; paper.
- [x] **E-05.** Preserve the statement that P3 magnitudes are not P4 calibration targets. Protocol/addendum SHA-bound; paper.
- [x] **E-06.** Preserve the study scope: fresh Tagalog parent; C1/C2/C3 siblings; token-share mixture trade-off. Gates I/Q/R/S/T receipts.
- [x] **E-07.** Preserve the one-seed scope; do not add a second confirmatory seed. Seed 42 only; no extra seed trained.
- [x] **E-08.** Preserve the non-CORE, non-chat, non-SFT scope. Confirmatory trainer: eval/sample/core-metric off.
- [x] **E-09.** Preserve the rule that mitigation is not claimed by the registration itself. Filing/title omit mitigation.
- [x] **E-10.** Preserve all three SHA-bound protocol references in the filed PDF: master `22c28f2bc632f132d9c95bbbcc9d1facbddf0b6b821445487e451c472ea58d4b`; bible `b389b70e0b8e3af869e8dea314b1c7c6b91df313e49d1bf11d9d07961b4a5a42`; addendum `f056a6f75c73a4d8dc3401ba8d7219d406aa7e498e5b0799d3d0373f9f74c216`. Unedited.

## 2. Gate 0 and P4-run identity

- [x] **E-11.** File before any P4 parent, child, official `val_bpb_full`, or test BPB computation. PDF 2026-08-20; `P4_RUN_ID` minted 2026-08-21T06:00:32Z after PDF.
- [x] **E-12.** Maintain the lockbox such that P4 scalar outcomes are inaccessible before Gate X. Preflight: `p4_outcome_access_count=0`, `unblinding_status=blinded` at 2026-08-21T13:41:44Z.
- [x] **E-13.** Preserve the filed source pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`. Gate A / LOCK.
- [x] **E-14.** Preserve the filed protocol SHA values without post-filing edits. E-10 hashes unchanged.
- [x] **E-15.** Create and retain `P4_RUN_ID`/cache/ledger identity under a P4-only namespace. `p4-20260821T060032Z-92d63d4`; `manifests/p4/`; `scripts/p4/`.
- [x] **E-16.** Set initial outcome and test-access counters to zero before parent training. Gate 0; U receipt `test_access=0`.
- [x] **E-17.** Retain proof that lockbox dummy tests passed without opening a P4 scientific scalar. `docs/run-cards/p4/p4-20260821T060032Z-92d63d4/gate-0-lockbox-tests.json` `all_pass=true`; LOCK `lockbox_acceptance_tests=pass`.
- [x] **E-18.** Retain a Gate 0 record that the raw test files remain outside training directories. Gate C check `C-04_tests_absent_from_train_roots` ok; `no_real_val_test_text=true`.

## 3. Source, environment, and no-reuse requirements

- [x] **E-19.** Retain evidence that the nanochat pin matches the filed SHA. Gate A; LOCK `nanochat_pin`.
- [x] **E-20.** Retain evidence of P4-only environment/cache sentinel and no P1/P2/P3 environment sourcing. `scripts/p4/env.sh` / `env.cuda.sh`; Gate C sentinel.
- [x] **E-21.** Retain the official `evaluate_bpb.py` copy and formula-identity receipt. Official SHA `9afebdb405aaac0bb4287051d9b6f5d16f56d6dd9269a1e6c2c5df29becbced1` (Gate A; not the Gate 0 stub).
- [x] **E-22.** Retain proof that the P4 Hub endpoint is a scalar-free stub before results release. Pre-W stub; Hub still deferred at W.
- [x] **E-23.** Retain proof that no P1.1, P2, or P3 `.pt` file is loaded as a P4 parent. Gate C `C-03`; children `parent_c0_sha256` = I d20 `34e069646be4158979809c023691188439047d6cbee08a141db432c78bcf02e2`.
- [x] **E-24.** Retain proof that no P1.1/P2/P3 Hub is a P4 write target. No writes onto those IDs; P4 Hub deferred.
- [x] **E-25.** At final close-out, verify that no prohibited prior weight appeared in any parent/child lineage receipt. Q/R/S/T: C0 only; smoke quarantined `p4-smoke-tl-d4`; d8 not C0.
- [x] **E-26.** Never use P1.1/P2/P3 weights as parent, smoke-resume source, child parent, or emergency fallback. `not_occurred`.
- [x] **E-27.** Never use a child as a parent for another P4 child. `not_occurred`; R/S/T all from C0.

## 4. Confirmatory data, identity, and split requirements

- [x] **E-28.** Retain all six named confirmatory JSONL SHA-256 values. Gate B.
- [x] **E-29.** Retain proof that the P1.1 Tagalog training JSONL matches SHA `2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687`.
- [x] **E-30.** Retain proof that the Tagalog validation JSONL matches SHA `4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c`.
- [x] **E-31.** Retain proof that the English validation JSONL matches SHA `874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b`.
- [x] **E-32.** Retain proof that the English legacy test JSONL matches SHA `2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e`.
- [x] **E-33.** Retain proof that the Tagalog legacy test JSONL matches SHA `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf`.
- [x] **E-34.** Retain proof that the official English training identity is frozen, including filed hash prefix `09ae691c...` and complete manifest value. Gate B/D.
- [x] **E-35.** Retain `split_origin=p11_reuse` and the frozen document-level split identity. Gate D.
- [x] **E-36.** Retain overlap report showing train/validation/test overlap equals zero within language. Gate D; cross-split overlap 0.
- [x] **E-37.** Record the intra-split English duplicate observation as provenance only; preserve filed rows unchanged. Gate D: 28472 rows / 28232 unique; not dropped.
- [x] **E-38.** Treat any filed JSONL hash mismatch as `STOP`; do not reclean, deduplicate, substitute, or regenerate a split. `not_occurred` (no mismatch).
- [x] **E-39.** Do not place validation or test content in a training directory. `not_occurred` at Gate C; V used named test paths under logged access only.

## 5. Tokenizer and evaluation definition

- [x] **E-40.** Retain carry-forward P3 `tokenizer.pkl` SHA `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8`. Gate F.
- [x] **E-41.** Retain carry-forward P3 `token_bytes.pt` SHA `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132`. Gate F.
- [x] **E-42.** Retain tokenizer write-probe failure/read-only receipt. Gate F.
- [x] **E-43.** Retain official BPB definition: mean token NLL divided by `ln(2)` times mean UTF-8 bytes per token. Frozen `evaluate_bpb.py`.
- [x] **E-44.** Retain evaluator configuration: official `evaluate_bpb`, `T=2048`, BOS-best-fit, full validation, CUDA. U/V receipts; packing fields in test log.
- [x] **E-45.** Retain frozen train-fitted add-1 UTF-8 byte-unigram floor implementation for P0-T. P0-T CUDA path; released `byte_unigram_tagalog_val.json`.
- [x] **E-46.** Retain frozen untrained same-depth floor implementation for P0-T. P0-T CUDA path.
- [x] **E-47.** Do not substitute `meta.val_bpb` for `val_bpb_full`. `not_occurred`; official evaluator only.
- [x] **E-48.** Do not use C3 `val.parquet` as a dependent variable or gate signal. `not_occurred`.
- [x] **E-49.** Do not train a new tokenizer after any P4 BPB has been observed. `not_occurred`; F before E; tokenizer unchanged after BPB.

## 6. C3 treatment construction and packed-stream closure

- [x] **E-50.** Retain filed C3 treatment: `q_TL=0.50` Tagalog source-content tokens under the carry-forward P3 tokenizer. LOCK / mix manifest.
- [x] **E-51.** Retain C3 token quotas: 9,633,792 Tagalog and 9,633,792 English source-content tokens. Gate E; LOCK `c3_quota_*`.
- [x] **E-52.** Retain evidence that C3 was frozen after tokenizer freeze and before any P4 BPB. Operational F then E; first BPB at P0-T after I.
- [x] **E-53.** Retain C3 seed 42 and deterministic 2,048-token block schedule. Gate E / G.
- [x] **E-54.** Retain packed train-stream manifest, language-origin mask SHA, shard hashes, and consumed-order receipt. Mix SHA `f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107`.
- [x] **E-55.** Retain audit that first `N x B` consumed C3 tokens have exact quota and no wrap. Gate E packed-stream freeze.
- [x] **E-56.** Retain C1 extra-Tagalog and C2 WT103-raw packed-stream hashes. `gate-e-c1-c2-pack.json`.
- [x] **E-57.** Do not alter C3 to byte balancing, another quota, another block size, or another PRNG rule. `not_occurred`.
- [x] **E-58.** Do not wrap C3 before `N x B`. `not_occurred`.
- [x] **E-59.** Do not claim C3 is P3 B3 or call its result mitigation unless the filed joint criteria are met and reported narrowly. C3 ≠ B3 throughout. After X, paper uses the filed four-way grammar plus the filed narrow sentence only.

## 7. Parent training and Gate I closure

- [x] **E-60.** Retain Gate H quarantined d4 smoke receipt; smoke is not TL0/C0 and cannot be a parent. `gate-h-cuda-smoke.json`; quarantine `p4-smoke-tl-d4`.
- [x] **E-61.** Retain fresh d8 TL0 terminal receipt: exact step 294/294, health pass, reload pass, terminal artifact record. SHA `f9b2ffbbc72fc6168bff7f2a1a6aae79292da198d12121f71d5385741b2c6111`; 335,570,367 B.
- [x] **E-62.** Complete fresh d20 TL0 at exact step 294/294. `gate-i-tl0-d20.json`; SHA `34e069646be4158979809c023691188439047d6cbee08a141db432c78bcf02e2`; 2,663,446,486 B.
- [x] **E-63.** Record d20 terminal checkpoint path, byte count, SHA-256, reload/health result, and run card. Same receipt; reload_ok true; health pass.
- [x] **E-64.** Verify that d8 and d20 parent runs used fresh initialization and the frozen P4 seed table. Gate I authorization/preflight; seed 42; not resumed from smoke/P1–P3.
- [x] **E-65.** Verify official NVIDIA CUDA execution for d8/d20, not MPS or CPU. A40; receipts `gpu=true`.
- [x] **E-66.** Verify no `ratio=-1`, Hugging Face Trainer, or nonfiled parent command was used. `not_occurred`; `refuse_ratio.py` / nanochat trainer argv from Gate G freeze.
- [x] **E-67.** Verify terminal checkpoint only; no mid-run checkpoint selection. `save-every=-1`; step 294 only.
- [x] **E-68.** Mark Gate I `PASS` only after both d8 and d20 receipts are complete. `gate-i-tl0.json` status pass; LOCK I=pass.

## 8. P0-T eligibility gate

- [x] **E-69.** Run official CUDA-only full Tagalog `val_bpb_full` for d8 parent against both filed floors. `gate-p0-t.json`; depth 8 `pass_both_floors=true`.
- [x] **E-70.** Run official CUDA-only full Tagalog `val_bpb_full` for d20 parent against both filed floors. Depth 20 `pass_both_floors=true`.
- [x] **E-71.** Confirm each depth is at least 0.01 BPB below its untrained same-depth floor. CUDA P0-T PASS; scalars were lockboxed until X.
- [x] **E-72.** Confirm each depth is at least 0.01 BPB below the train-fitted add-1 byte-unigram floor. Same.
- [x] **E-73.** Record only `PASS`, `BLOCKED`, or `TECHNICAL_STOP` externally; preserve P0-T scalars in the lockbox. Safe receipt `p0_t_status=PASS`, `no_bpb_in_receipt=true`; lockbox SHA `07c153892a8afe09b5291b5d346a39edafe2240dedb78136edf52368b4c26a9f`.
- [x] **E-74.** If either depth/floor requirement fails, block all C1/C2/C3 training and document the stop. N/A: PASS; children not started before PASS.
- [x] **E-75.** If P0-T passes, record that d8 was eligibility-only and d20 alone is eligible to become C0. Gate Q freeze from I d20 only.
- [x] **E-76.** Do not use a CPU P0-T evaluation as authoritative status. `not_occurred`; official status CUDA A40.

## 9. C0 freeze and child continuations

- [x] **E-77.** Freeze exact d20 parent as C0 only after P0-T passes. `gate-q-c0-freeze.json`; SHA matches I d20; `additional_train_tokens=0`; `immutable=true`.
- [x] **E-78.** Record immutable C0 SHA, path, mode, and reload receipt. Path `data/cache/p4-20260821T060032Z-92d63d4/c0/frozen/p4-c0-tl-d20/`.
- [x] **E-79.** Run C1 extra-Tagalog from C0, fresh Muon+AdamW, `load_optimizer=False`, warmup 14, 294 steps. `gate-r-c1.json`; tag `p4-c1-tl-d20`; SHA `87b9f55146de72dd6ae53598b9aea8d99079ff0f9492b7f9ea4fdce550664c55`.
- [x] **E-80.** Run C2 pure English from the same C0, same fresh-optimizer rule, warmup 14, 294 steps. `gate-s-c2.json`; tag `p4-c2-en-d20`; SHA `0787aed0f13a0ab3ec144baf6802b144a18412780a2d00a64ca7adcb67a4a375`.
- [x] **E-81.** Run C3 frozen mixture from the same C0, same fresh-optimizer rule, warmup 14, 294 steps. `gate-t-c3.json`; tag `p4-c3-mix-d20`; SHA `eef9a4e11c4840ac036d42c3bf4d87a2139ea1fa5809e1c756df2770fe0609f3`.
- [x] **E-82.** Confirm serial order C1 then C2 then C3, without using outcomes to alter later branches. Timestamps R 12:30:44Z → S 12:58:10Z → T 13:25:39Z; blinded receipts.
- [x] **E-83.** Confirm each child has `D_phase2=19,267,584` model-budget rule and its terminal checkpoint only. All three receipts `D_phase2=19267584`, step 294.
- [x] **E-84.** Hash, reload, and archive each C1/C2/C3 terminal checkpoint. Receipts + local copies SHA-matched 2026-08-21 (2,663,446,486 B each).
- [x] **E-85.** If a child is partial, quarantine it and clean-restart from C0; do not resume the partial optimization trajectory. `not_occurred` for children. (Separate: Gate V first attempt TECHNICAL before any test score; rerun once from U seal.)
- [x] **E-86.** Do not drop an arm because a contrast appears unfavorable. `not_occurred`; C1/C2/C3 all completed.
- [x] **E-87.** Do not train English before C2, children before C0, or a child from another child. `not_occurred`.

## 10. Gate U full validation seal

- [x] **E-88.** Complete all six full child validation cells: C1/C2/C3 by Tagalog/English. Seal SHA `5c7287752ba1abb39245acab43b9917ea9e089c0309959ec24990015e1ad580f`.
- [x] **E-89.** Use only filed frozen validation JSONLs, filed P3 tokenizer, official evaluator, T=2048, BOS-best-fit, full validation, and CUDA. Gate U CUDA; evaluator SHA frozen.
- [x] **E-90.** Collect C0 English validation once at U and label it descriptive only. Seal `c0_en_descriptive=true`.
- [x] **E-91.** Exclude C0 English descriptive value from `R_TL` and `A_EN`. Seal `c0_en_excluded_from_contrasts=true`.
- [x] **E-92.** Before any test access, seal complete validation table and record `test_access=0`. U receipt `test_access=0` at 2026-08-21T13:28:05Z; V at 13:31:01Z.
- [x] **E-93.** Compute filed `R_TL = TL(C3) - TL(C2)` only from sealed full validation values. Seal + `scripts/p4/fill_p4_tables.py` recomputation agrees.
- [x] **E-94.** Compute filed `A_EN = EN(C3) - EN(C1)` only from sealed full validation values. Same.
- [x] **E-95.** Apply equality rule: `R_TL <= -0.01` and `A_EN <= -0.01`; equality at -0.01 counts. Applied at X from seal; `results/p4/tables.json` `both_criteria_met=true`.
- [x] **E-96.** Classify the predeclared conclusion as both / only-R / only-A / neither. `grammar=both`.
- [x] **E-97.** Preserve no-composite and no-best-arm rule. Paper/tables: no composite; no extra arm selection.
- [x] **E-98.** Do not print BPB values, contrasts, or conclusion category before Gate X. `not_occurred` in safe logs (X preflight check 10 PASS). Release was Gate X.

## 11. Gate V restricted secondary test event

- [x] **E-99.** Confirm Gate U seal exists and test access was zero at seal time. E-92.
- [x] **E-100.** Run exactly one C3-only test event after Gate U. `gate-v-test.json`; tag `p4-c3-mix-d20`; `authorized_touches=1`.
- [x] **E-101.** Read exactly the named English legacy test SHA and Tagalog legacy test SHA once under logged access control. `manifests/p4/p4_test_access_log.json`; two component paths.
- [x] **E-102.** Record one authorized test event containing two named component reads. `component_evaluations=2`.
- [x] **E-103.** Keep C1 and C2 untested forever under P4. X preflight: C1/C2 tags absent from test log.
- [x] **E-104.** Preserve test values as descriptive secondary evidence only. Paper: tests secondary; `does_not_alter_sealed_contrasts=true`.
- [x] **E-105.** Do not compute a test-set `R_TL` or `A_EN`. `not_occurred`.
- [x] **E-106.** Do not reuse P1.1 `1.164768` or P2/P3 Gate V numbers. `not_occurred`.

## 12. Gate X formal unblinding

- [x] **E-107.** Before opening outcome files, run a status-only Gate X preflight confirming P0-T/U/V requirements and outcome-access count zero. `gate-x-preflight.json` `ready_for_unblinding=true` at 2026-08-21T13:41:44Z.
- [x] **E-108.** Record the pre-unblinding timestamp, operator, files authorized for opening, and lockbox state. Same receipt; unblind script `releaser=gate_x_unblind.py`.
- [x] **E-109.** Open the sealed scalar bundle once and release the complete predeclared validation table, contrasts, conclusion category, and C3-only secondary test outputs together. `P4_UNBLINDING_EVENT.json` at 2026-08-21T13:42:01Z; released dir `data/cache/p4-20260821T060032Z-92d63d4/released/`; `raw_test_still_restricted=true`.
- [x] **E-110.** Mechanically recompute `R_TL` and `A_EN` from the released sealed table and record agreement. `scripts/p4/fill_p4_tables.py`; `paper_decimals_match_seal=true`.
- [x] **E-111.** Record outcome-access count transition and formal unblinding timestamp. LOCK: `p4_outcome_access_count=1`, `validation_scalar_access_count=1`, `unblinding_status=gate_x_unblinded`.
- [x] **E-112.** State one-seed result interpretation without CI, p values, or population claim. Paper + `P4-REPORTING-GRAMMAR.md`.
- [x] **E-113.** After X, do not run additional validation/test evaluations, change C3, add arms, retune `q_TL`, `D`, delta, or tests. `not_occurred`; `no_additional_validation_or_test_eval=true`.

## 13. Gate W, reporting, and artifact close-out

- [x] **E-114.** Write the P4 paper from sealed/unblinded outputs; retain post-P3 disclosure and no-amendment wording. `docs/papers/p4-token-share-mix/paper.tex` and `paper_outputs/paper.pdf` SHA `d0bf73d30bd43b3984441f3d567ce49c886194376575148354494b7f7892da71` (deposits line revised 2026-08-22: AsPredicted if84km.pdf, ResearchBox #8869, AsCollected #2471). Prior Gate-W PDF SHA `9fc06a6c559ce2269c1ae841de6e33b04bdfe36e506b8cbb40de6462380ceb90`.
- [x] **E-115.** Report C3 as a token-share mixture intervention, not byte-balanced and not P3 B3. Paper Methods/Discussion.
- [x] **E-116.** Describe conclusions according to both / only-R / only-A / neither; do not overstate mitigation. Grammar `both`; narrow sentence only.
- [x] **E-117.** State the one-seed limitation, no CI/p rule, and source-content-token exposure definition. Paper Limitations; LOCK `q_tl_clock`.
- [x] **E-118.** Archive filed PDF, master, gate bible, addendum, LOCK, all run cards, hashes, manifests, evaluator, and test access log. `p4_closeout_manifest.json` + `SHA256SUMS` under `docs/run-cards/p4/p4-20260821T060032Z-92d63d4/`.
- [ ] **E-119.** Create a ResearchBox/deposit package with no test text, secrets, passcodes, or prohibited raw artifacts. Box **#8869** exists (anonymous, passcode-protected, not Make Public). Post-X upload of paper + released seals is still an operator deposit; do not put passcode in git; do not upload `test.jsonl`.
- [x] **E-120.** Publish C0/C1/C2/C3 weights together or document an explicit joint deferral; never present C3 alone as “the final P4 model.” LOCK `hub_status=deferred` 2026-08-21; `docs/hub/p4-token-share-mix/README.md`. Local C0–C3 `.pt` now present; Hub upload still optional under this deferral.
- [ ] **E-121.** Publish code and model cards with parent lineage, tokenizer hashes, corpus/split hashes, `N`, B, terminal checkpoint rule, and post-P3 disclosure. Local paper/docs/hub stub exist; GitHub subtree and Hub card publication not done.
- [ ] **E-122.** Verify public download hashes for all released files. Local SHA256SUMS recorded (E-118). Public Hub re-hash is N/A until a joint C0–C3 Hub upload.
- [x] **E-123.** Update the program website/status page without adding unregistered claims. Local study record `docs/p4/README.md` updated to X/W closed + Hub deferred. Public git/site push still follows E-121.
- [ ] **E-124.** Rotate any Runpod, SSH, or Hub credentials that may have been exposed during execution. No rotation receipt yet.
- [ ] **E-125.** Stop/terminate GPU/volume only after all required local and external archives are verified. Local lockbox hashes matched the pod. Pod `cjaakd9i2w8x7t` (`p4-gate-h-smoke`) was still running at last check; volume should be kept until Hub staging is decided. Do not terminate the volume solely to “finish” P4.

## Explicit stop-condition ledger

| Condition | Record |
|---|---|
| NaN/Inf | `not_occurred` (child health pass, reload_ok) |
| ClimbMix | `not_occurred` (Gate C C-02) |
| Validation/test in train | `not_occurred` (Gate C C-04) |
| Inexact C3 quota | `not_occurred` (Gate E exact 9633792/9633792) |
| C3 wrap before `N x B` | `not_occurred` |
| New tokenizer after BPB | `not_occurred` |
| `ratio=-1` | `not_occurred` |
| Hugging Face Trainer | `not_occurred` |
| Write into a P1/P2/P3 Hub | `not_occurred` |
| Prohibited prior parent weights | `not_occurred` |
| Child-as-parent | `not_occurred` |
| MPS/CPU official GPU gate | `not_occurred` (A40 CUDA) |
| Missing terminal checkpoint | `not_occurred` (I d8/d20; R/S/T step 294) |
| Gate V missing JSONL | `technical_stop` then repaired: first V attempt FileNotFoundError on `english_test.jsonl` **before any score**; files restored; V rerun once from U seal with `test_access=0` at U |

## Final explicit closure declaration

**Confirmatory science is closed:** E-01 through E-118 and E-120/E-123 are `[x]`. P4 is **not** fully closed as an archival/public-surface process until E-119, E-121, E-122 (if Hub is later published), E-124, and E-125 are completed or explicitly waived with a dated operator note. A paper, Hub repository, or public checkpoint by itself is **not** P4 completion. Conversely, publication work after Gate X must not create new P4 evidence.

## Filed authority

*AsPredicted #307591, “P4: token-share mix after fresh TL parent (nanochat, TL-39/WikiText-103),” filed 2026-08-20; PDF: https://aspredicted.org/if84km.pdf.*
