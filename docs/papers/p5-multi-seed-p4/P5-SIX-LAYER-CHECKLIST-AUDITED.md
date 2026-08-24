# P5 Six-Layer Preregistration Requirements Checklist

## Purpose and governing rule

This document is the **six-layer companion** to the explicit-only checklist for AsPredicted #307836, *P5: multi-seed panel of the P4 token-share mix after fresh TL parents*. It separates six kinds of requirements so that an operationally sensible safeguard is never misrepresented as a filed commitment, and a filed commitment is never diluted into optional advice.

> **Authority rule:** The filed P5 PDF is the governing preregistration. The hash-pinned P5 gate plan and addendum named in Q8 are controlling implementation documents only after their SHA-256 values match the filed values. Earlier P1.1–P4 materials provide historical context and carry-forward artifacts, but they do not amend P5. [1]

| Layer | Meaning in this document | Can it be called “preregistered”? | Required handling |
|---|---|---|---|
| **I. Explicit** | Directly stated in the filed P5 PDF. | Yes | Must be followed exactly or classified under the filed failure taxonomy. |
| **II. Implicit** | Necessary operational consequence of an explicit commitment or a hash-pinned implementation reference. | Not by itself | Document it as an implementation safeguard; do not call it a novel filed hypothesis. |
| **III. Inferred** | Required to make the filed causal/design claim internally coherent. | No | Preserve it unless the filed authority says otherwise; label the reasoning. |
| **IV. Extrapolated** | Sensible follow-on practice imported from P1.1–P4, community norms, or future-study plans. | No | Keep separate from P5 confirmatory execution and label it optional or future work. |
| **V. Residual** | A still-open item, ambiguity, or absent deliverable that the filing does not resolve. | No | Track it explicitly; never silently fill the gap with an outcome-driven choice. |
| **VI. Hidden** | A plausible failure mode that could compromise an otherwise compliant-looking run. | No | Audit proactively; escalate if it intersects an explicit stop condition. |

## How to use this checklist

1. Complete **Layer I** against the companion explicit checklist, `p5_explicit_preregistration_requirements_checklist.md`.
2. Record Layers II–VI in a dated audit ledger with one of `pass`, `open`, `blocked`, `not-applicable`, or `escalate`.
3. Never use a Layer II–VI item to change a Layer I parameter, add an arm/seed, reopen a sealed scalar, or reinterpret the P5 estimand.
4. If a practical decision is not fixed in Layer I, check the hash-pinned gate plan/addendum. If still unresolved, stop and record the ambiguity rather than deciding after looking at P5 outcomes.
5. For every incident, record: UTC time, seed/arm if applicable, affected asset SHA/path, whether any scalar/test was accessed, authority consulted, and final classification.

## Audit status snapshot (2026-08-24 UTC)

Run **`p5-20260823T160632Z-439d1de5`** · AsPredicted **#307836** · Gates **0→W pass** · Gate X **2026-08-24T02:05:35Z**

| Mark | Meaning | Count |
|---|---|---:|
| `[x]` pass | Receipt-backed | 76 |
| `[~]` partial | Evidenced; sub-receipt or publication step open | 5 |
| `[ ]` open | Still outstanding (ops/publication/residual) | 17 |
| `[—]` n/a | Conditional not triggered / future-work only | 7 |

**Layer I companion (explicit PDF items):** 159 `[x]` · 20 `[ ]` · 13 `[—]` in `P5 Explicit Preregistration Requirements Checklist.md`.

**Panel result:** `both=3/3` eligible; `ineligible_parent=0`; count table only (`P5_UNBLINDING_EVENT.json`).

**Evidence root:** `docs/run-cards/p5/p5-20260823T160632Z-439d1de5/` · lockboxes · `p5_closeout_manifest.json`.

**Authority boundary:** Layers II–VI marks strengthen audit only; they do not amend #307836.

---


# Layer I — Explicit Filed Requirements

The following complete filed-PDF requirement families are incorporated by reference to the companion explicit checklist. That checklist provides individual IDs, source questions, and receipt types; it is the authoritative Layer-I item register.

| Layer-I family | Status | Companion checklist sections | Required result | Evidence |
|---|---|---|
| Study identity and interpretation boundaries | A-01–A-12 | Post-P4, outcome-informed multi-seed P4 recurrence panel; no amendment, independent-confirmation, population, or mitigation claim. |
| Pin, files, corpus, tokenizer, and C3 identity | B-01–B-23 | Pinned source, frozen carry-forward tokenizer, exact C3 quotas/interleave/shards/mask, and protected raw-test boundaries. |
| Host, environment, and lineage | C-01–C-17 | P5-only environment, pinned A40/CUDA/Torch/container class, no prior weights or forbidden trainer/data/device conditions. |
| Nonconfirmatory shared smoke | D-01–D-03 | One seed-0 d4 smoke only; never a P5 parent, cell, or outcome. |
| Parent seed initialization | E-01–E-14 | Exactly seeds 1→2→3; actual model-initialization control/hashes; no early stop, replacement, or fourth seed. |
| Parent and P0-T | F-01–F-13 | Fresh d8/d20 Tagalog parents; P0-T before child tokens; C0 only after P0-T pass; no replacement after ineligibility. |
| Children | G-01–G-13 | C1/C2/C3 from common C0_s; exact 294-step equal child budget; fresh optimizer; R→S→T order. |
| BPB and primary analysis | H-01–H-19 | Full CUDA validation; fixed bilingual contrasts and ≤ −0.01 criteria; no composite or meta metric. |
| Seal and C3-only secondary test | I-01–I-16 | Validation before test; one C3-only event per eligible seed; test secondary/descriptive and excluded from class count. |
| Panel classification and unblinding | J-01–J-12 | Count table only; no seed-level unblinding; exactly one panel Gate X. |
| Outcome exclusion and failure taxonomy | K-01–K-30 | Never exclude finite terminal outcomes for their values; apply panel/seed/technical classifications as filed. |
| Disclosure and close-out | L-01–L-12; M-01–M-08 | Accurate post-P4 disclosure, program linkage, provenance, and completion evidence. |

## Layer-I execution cross-checks

| ID | Status | Explicit cross-check | Evidence | Receipt pointer |
|---|---|---|
| I-EXP-01 | [x] | The local PDF SHA must equal `439d1de5ff9fd18e466f33192c5ac9c5c36b020ca72942ae218b9e69a8f5bbf3`. | SHA-256 receipt. | gate-0/LOCK pdf sha |
| I-EXP-02 | [x] | The gate-plan SHA must equal `d51115aade9c0b1fb8698eaa33540db2d75b2b27765aaaad1bf14b13b0132092`. | SHA-256 receipt. | gate-0/LOCK gate_plan sha |
| I-EXP-03 | [x] | The addendum SHA must equal `839fcaa3dd6e94bd9546df4880a5892851a54ea31743cb0359adc8faebbe9258`. | SHA-256 receipt. | gate-0 filed addendum sha |
| I-EXP-04 | [x] | The parent panel is seed 1, then seed 2, then seed 3—not “any three successful seeds.” | Ordered run ledger. | p5_gate_ledger ordered 1→2→3 |
| I-EXP-05 | [—] | A P0-T-blocked seed is reported as ineligible, not silently omitted or treated as a bad result. | Eligibility ledger. | 0 BLOCKED seeds |
| I-EXP-06 | [x] | A P0-T-passed seed receives C1, C2, and C3 from exactly its frozen C0_s, not sequential children. | Parent-SHA table. | parent_c0_sha256 table |
| I-EXP-07 | [x] | No P5 P0-T/U/V scalar or evaluator stdout/stderr is examined before the single Gate X. | Access-control ledger. | gate-x-preflight outcome_access_zero |
| I-EXP-08 | [x] | C1 and C2 are never evaluated on the P5 test sets. | Test-access ledger. | C3-only tests |
| I-EXP-09 | [x] | A technical restart is permitted only under the filed conditions; it is not a generic permission to retry an unfavorable or ambiguous arm. | Incident classification record. | S₂ accept-only; no unfavorable retry |
| I-EXP-10 | [x] | A restart of cloud hardware is not automatically a restart of Gate H, a parent, or a seed. | Gate-state ledger. | pod restart ≠ Gate H restart |

---

# Layer II — Implicit Operational Requirements

These requirements are not necessarily literal PDF sentences. They follow directly from being able to demonstrate an explicit filed commitment.

| ID | Status | Implicit requirement | Why it follows | Minimum receipt | Evidence |
|---|---|---|---|
| II-01 | [x] | Make the filed PDF, matching gate plan, and matching addendum read-only working references before training. | A hash cannot prove compliance if the checked object is later edited. | SHA log plus permissions/copy receipt. | pdf readonly; SHA bindings |
| II-02 | [x] | Maintain a P5-only run ledger keyed by seed, arm, and gate. | Ordered seeds, one panel release, and failure taxonomy need an auditable state record. | Ledger with UTC transition history. | p5_gate_ledger.json |
| II-03 | [x] | Record every parent/C0/child checkpoint SHA and parent relationship. | “Never load previous weights” and “common C0_s” are otherwise not independently auditable. | Parent–child lineage table. | lineage SHA receipts |
| II-04 | [x] | Verify the actual initial serialized state, not only a wrapper filename. | The filed design claims seed-controlled initialization and records the initial-state hash. | Per-seed state SHA. | seed-knob-proof + initial_state JSON |
| II-05 | [x] | Use a clean process/environment at every official launch. | P5-only environment sourcing and prohibited prior environments cannot be established from a final model alone. | Captured sanitized environment and command receipt. | preflight + authorization per gate |
| II-06 | [~] | Check GPU identity, CUDA, Torch, and container before every new official GPU gate after a host restart. | The filed host contract applies to official gates, not merely the first pod. | Per-host preflight receipt. | I-preflight per seed; torch/container not every card |
| II-07 | [x] | Keep raw test data physically or logically unavailable to parent/child packers and tokenizer processes. | The filing says test files stay outside train/tokenizer/staged child paths; a path-only assertion needs enforcement. | Mount/path scan and denied-read test. | test isolation gates B/D/C |
| II-08 | [x] | Distinguish diagnostic training metadata from official `val_bpb_full`. | The filing excludes `meta.val_bpb` from the DV. | Separate diagnostic and official-result namespaces. | lockbox val_bpb_full namespace |
| II-09 | [x] | Ensure each child starts from `C0_s` with a fresh optimizer, not from a partial child or optimizer resume. | Filed common-parent and `load_optimizer=False` requirements would otherwise be defeated. | Load source and optimizer-state audit. | load_optimizer=false |
| II-10 | [x] | Confirm that 294 means **new child updates**, not an absolute global step inherited from the parent. | Equal phase-2 budget needs a common origin. | Terminal metadata and command receipt. | init_step=294 child budget |
| II-11 | [x] | Check C3 quotas and order from trainer-consumed bytes/shards, not from a planning manifest alone. | The filing explicitly says the manifest/source JSONLs alone are insufficient. | Runtime input/hash audit. | gate-e shard hashes |
| II-12 | [x] | Separate safe progress indicators from lockboxed scalars in logs and dashboards. | “PASS/BLOCKED/TECHNICAL_STOP” and `test_access` counts are safe; BPB and evaluator output are not. | Redacted safe-progress log. | safe vs lockbox separation |
| II-13 | [x] | Capture a pre-test validation-seal timestamp and test-access count per eligible seed. | The test is permitted only after that seed’s seal with `test_access[s]=0`. | Seal manifest and test ledger. | U before V each seed |
| II-14 | [x] | Keep one authoritative test-access counter per seed. | Zero-to-three events and C3-only policy cannot be audited from scattered logs. | Append-only ledger. | LOCK test_access_count |
| II-15 | [x] | Prevent a model-selection decision after seeing C3-only tests. | Tests are descriptive/secondary and excluded from seed classification. | Fixed terminal-selection policy before V. | terminal-only selection |
| II-16 | [~] | Preserve terminal checkpoint artifacts before releasing or deleting cloud storage. | Missing terminal checkpoint is an explicit stop condition. | Local/remote checksum manifest. | lockboxes local; full ckpts on pod volume |
| II-17 | [x] | Distinguish a cloud host restart from an experimental restart in all cards and public updates. | The same word “restart” otherwise creates a false claim that Gate H/I/parent was re-run. | Run-card language audit. | wait-start-resume.log |
| II-18 | [x] | Freeze the contrast/classification code before Gate X. | A count-only primary analysis can still be altered post-outcome if its implementation is not frozen. | Script SHA / lock record. | gate_x_unblind in closeout |
| II-19 | [x] | Verify that every eligible seed produces all six child validation cells before classification. | `both/only-R/only-A/neither` needs C1/C2/C3 on TL and EN. | U completeness matrix. | six_child_cells seals |
| II-20 | [x] | Require a no-scalar-access statement when classifying an interruption as technical. | Technical repair is pre-outcome; lockbox integrity is part of that fact. | Incident declaration and access audit. | S₂ accept without scalar access |

---

# Layer III — Inferred Scientific and Causal Requirements

These items are necessary to preserve the meaning of the P5 estimand, even where the PDF uses a more operational formulation.

| ID | Status | Inferred requirement | Rationale | Do not misstate as | Evidence |
|---|---|---|---|
| III-01 | [x] | Keep the P4 C3 treatment definition fixed while changing only P5 parent initialization and descendants. | P5’s scientific role is recurrence across new seeds, not a new ratio/tokenizer/data-treatment study. | A direct P4 clone in every implementation detail. | P4 C3 fixed; seeds vary only |
| III-02 | [x] | Treat C1 and C2 as separate reference branches, not as competing “winners.” | R_TL and A_EN have distinct counterfactual comparators. | One composite mixed-versus-pure result. | separate R_TL/A_EN |
| III-03 | [x] | Interpret P5 as seed-level recurrence evidence, not a statistical sample from a defined superpopulation. | The filed primary analysis is a count table without inference. | A population rate or significance test. | count table only |
| III-04 | [x] | Preserve common-parent sibling comparability within each seed. | Otherwise C3–C2 or C3–C1 differences confound treatment with parent history. | A comparison of independently evolved descendants. | common C0 siblings |
| III-05 | [x] | Hold the total phase-2 budget fixed across C1/C2/C3. | Otherwise exposure quantity, rather than source-content composition, changes with arm. | An optimal-token-budget claim. | equal D_phase2 |
| III-06 | [x] | Treat source-content token share as the P5 exposure definition. | P4/P5 explicitly distinguish token share from document count and byte share. | Equal document count or equal bytes. | token-share quotas |
| III-07 | [x] | Keep parent eligibility independent of downstream arm outcomes. | P0-T precedes any child and must not become a result-screening device. | Outcome-based parent selection. | P0-T precedes children |
| III-08 | [x] | Treat C0 English validation and C3-only tests as descriptive auxiliaries. | The contrast/classification logic excludes them. | Additional co-primary endpoints. | C0/test descriptive |
| III-09 | [x] | Preserve directional meaning: P5 is a fresh Tagalog parent with English/Tagalog continuations. | Direction is part of the P3/P4/P5 construct and cannot be reversed under the same label. | A bidirectional general claim. | TL parent EN/TL continuations |
| III-10 | [x] | Interpret a seed’s `both` classification only as meeting two preregistered BPB inequalities in this apparatus. | The outcome does not establish general mitigation, task retention, causal mechanism, or optimality. | “C3 fixes forgetting.” | no mitigation claim in event |
| III-11 | [—] | Interpret a P0-T ineligible seed as a defined eligibility outcome, not a failed panel estimate or a removable outlier. | The filing prespecifies its handling. | A reason to replace or discard a seed silently. | no ineligible seeds |
| III-12 | [x] | Keep test isolation stronger than ordinary validation isolation. | The panel primary result is validation-defined and the test is one-touch secondary evidence. | A reusable tuning endpoint. | one-touch C3 tests |
| III-13 | [x] | Treat evidence of failure to reproduce P4’s pattern as informative rather than a protocol defect. | No early stop, no replacement, and no unfavorable-result exclusion preserve this interpretation. | A reason to “repair” the science. | seed 3 run after 1/2 both |
| III-14 | [x] | Attribute any C3 pattern to the entire filed treatment bundle: source-content share, fixed stream, schedule, tokenizer, parent, and budget. | P5 does not isolate mechanism; it tests recurrence of P4’s bundled treatment. | Proof that token share alone caused the result. | bundled treatment attribution |
| III-15 | [x] | Reserve causal-mechanism claims for later separate ablations such as P6-M. | P5 changes seeds, not schedule topology, revisit, or optimizer state. | A mechanism test. | no mechanism arms |
| III-16 | [~] | Preserve P5’s explicit post-P4 disclosure in all summaries. | The sequence was outcome-informed by released P4 seed 0. | Outcome-independent replication. | gate-0 post-P4; paper L-01/L-02 open |

---

# Layer IV — Extrapolated / Non-Filed Good-Practice Requirements

These are prudent practices drawn from the P1.1–P4 program, reproducible-computation norms, or later-study planning. They should be adopted if useful, but they are **not P5 confirmatory conditions unless the matching P5 plan/addendum says so**.

| ID | Status | Extrapolated item | Origin / motivation | Safe use | Evidence |
|---|---|---|---|
| IV-01 | [ ] | Prepare a ResearchBox deposit package with hashes, scripts, manifests, and paper source. | P1.1–P4 close-out practice. | Documentary release after results; no new evidence. | ResearchBox pending |
| IV-02 | [ ] | Release all P5 eligible parent/child weights together under clear model-card boundaries. | P3/P4 release ethics and sibling comparability. | Treat as release policy, not a selection rule. | Hub deferred |
| IV-03 | [ ] | Build P5 paper sources and a reproducibility README before Gate X. | Program documentation practice. | Keep results values out until release. | no paper.tex yet |
| IV-04 | [x] | Maintain separate internal and public-safe run cards. | Prior lockbox/safe-progress practice. | Public card exposes only allowed statuses/hashes/counts. | blinded run-cards |
| IV-05 | [x] | Preserve host stdout/stderr, preflight, transfer, and environment logs. | Recovery and reproducibility practice. | Do not expose lockboxed scalars before Gate X. | lockbox logs + preflight JSON |
| IV-06 | [ ] | Archive checkpoints locally before terminating a cloud volume. | Earlier GPU/volume loss prevention. | Does not authorize duplicate evaluation. | full checkpoint archive optional |
| IV-07 | [ ] | Rotate exposed cloud, SSH, or Hub credentials. | Security hygiene. | Private operational action, not study evidence. | no credential rotation receipt |
| IV-08 | [—] | Conduct a separately preregistered downstream-task retention study after P5. | BPB/task distinction and Cheng-adjacent Filipino NLP resources. | Do not backfill task claims into P5. | future task study |
| IV-09 | [—] | Conduct P6-M schedule-topology, P7-M revisit, or P8-M optimizer-state ablations only as new studies. | Post-P5 mechanism roadmap. | Do not add them as P5 exploratory arms. | P6+ roadmap |
| IV-10 | [—] | Consider P9-R/P10-R mitigations only after mechanism work and separate filing. | Stability–plasticity intervention roadmap. | Do not call P5 C3 a mitigation. | P9/P10 roadmap |
| IV-11 | [—] | Consider P11-X/P12-X tokenizer/corpus/language transfer only under new corpus and split protocols. | External-validity roadmap. | Do not generalize P5 beyond English–Tagalog. | P11/P12 roadmap |
| IV-12 | [x] | Use reproducible checksums, immutable object storage, and signed manifests. | General reproducible-computing practice. | Supplement, not replace, filed asset requirements. | closeout manifest + SHA256SUMS |
| IV-13 | [ ] | Have an advisor or coauthor review the final paper’s claims. | Authorship and scientific-quality practice. | Do not imply an unrecorded coauthor or endorsement. | no coauthor review receipt |
| IV-14 | [ ] | Produce a post-hoc compute/cost audit. | Transparency practice. | Do not use cost to alter completed execution. | no compute audit doc |
| IV-15 | [ ] | Preserve a public explanation that P5 uses small nanochat models and BPB, not deployed LLM performance. | Scope discipline. | Use in discussion/limitations. | limitations section pending |

---

# Layer V — Residual Requirements and Open Decisions

These are known gaps that cannot be solved by simply choosing an answer after outcomes. Each requires an authority check, a pre-outcome decision, or an explicit post-study disclosure.

| ID | Status | Residual item | Why it remains open | Required next step | Disposition |
|---|---|---|---|
| V-01 | [x] | Full authoritative English-train SHA | The filed PDF renders it in abbreviated form. | Obtain only from matching gate plan/addendum or immutable P5 asset manifest. | gate-b full EN train SHA |
| V-02 | [x] | Exact implementation text of the gate plan/addendum | Their hashes are filed, but the documents are not present in this workspace. | Verify and archive matching originals before relying on detailed recovery language. | plan/addendum in repo; SHA match |
| V-03 | [x] | Status of seed-2 C2 after interruption | The filing gives general failure rules; the actual checkpoint/provenance state must be inspected without outcome access. | Use the acceptance screen; classify under matching P5 plan/addendum. | seed-2 gate-s-c2 accept |
| V-04 | [x] | Current P5 execution status | The filing does not state later operational progress. | Maintain a safe status ledger; never infer completion from a pod or file name. | gate_w_pass |
| V-05 | [x] | Whether a faulty extant `model_000294.pt` counts as “no official terminal checkpoint” or an explicit panel-stop event | Q6 contains both a technical-restart clause and a missing-terminal-checkpoint panel-stop condition. | Resolve only with the hash-matching gate plan/addendum before retraining. | S₂ terminal ckpt accepted |
| V-06 | [ ] | Exact P5 archive/release destination and release timing | Not stated in #307836. | Decide as documentary policy without changing science or outcome access. | release timing deferred |
| V-07 | [ ] | Exact paper title, author order, and advisor/coauthor role | Not stated in #307836. | Obtain human authorship agreement; do not infer it from prior consultation. | authorship open |
| V-08 | [ ] | Downstream task relevance | P5 measures BPB only. | Label as limitation; file a later task study if desired. | limitation to state in paper |
| V-09 | [ ] | Generalization to larger models, other corpora, other language pairs, or user-facing models | Not tested by the P5 apparatus. | State boundary; use later X-family studies. | limitation to state in paper |
| V-10 | [ ] | Mechanism of any observed recurrence/nonrecurrence | P5 varies initialization seed, not mechanism factors. | Reserve for a filed mechanism ablation. | mechanism for later studies |
| V-11 | [ ] | Whether C3 is a mitigation or an optimum | P5 does not test a mitigation set or ratio surface. | Do not claim either; file a remediation/ratio study separately. | forbidden claims — paper audit |
| V-12 | [—] | Meaning of a P0-T-ineligible parent for wider catastrophic-forgetting theory | The filing defines operational handling but not a population-theoretic interpretation. | Report it descriptively as predeclared eligibility status. | no ineligible parent occurred |
| V-13 | [x] | What to do if host availability prevents a timely continuation | Compute availability is not a scientific parameter. | Keep the panel state; resume only at the lawful unfinished gate when infrastructure returns. | wait-start-resume lawful continuation |
| V-14 | [ ] | Whether the P5 GitHub public tree contains scripts/docs | Current public tree may lag private or unpushed P5 materials. | Do not treat a public 404 as authorization to recreate or alter the pinned plan. | public GitHub may lag |

---

# Layer VI — Hidden Risks and Failure-Mode Checks

These checks are not extra hypotheses. They are failure-mode probes designed to protect the explicit P5 structure.

| ID | Status | Hidden risk | Why it matters | Preventive or diagnostic check | Evidence |
|---|---|---|---|
| VI-01 | [x] | **Host restart mistaken for Gate H restart** | Could create an unauthorized second smoke or misleading ledger state. | Separate hardware lifecycle from gate lifecycle; retain H=`pass`. | H pass retained |
| VI-02 | [x] | **Partial child checkpoint silently reused** | Violates C0_s/fresh-optimizer/common-parent logic. | Check load source, optimizer state, output directory, and command history. | C0-only child loads |
| VI-03 | [x] | **Checkpoint file exists but is not an official terminal result** | A file name alone does not establish 294-step completion or provenance. | Reload/metadata/hash screen without BPB evaluation. | S₂ reload/meta screen |
| VI-04 | [x] | **P5 scalar leakage through logs, dashboards, filenames, or shell scrollback** | Violates the one-panel-unblinding lockbox. | Write outputs to restricted paths; audit commands and views. | lockbox until X |
| VI-05 | [x] | **In-loop evaluation accidentally reaches full validation** | Could expose an outcome before the U seal. | Audit evaluator calls and data paths; distinguish diagnostics from official evaluator. | eval_every=-1 |
| VI-06 | [x] | **Test file mounted under a generic data root** | A packer or dataset glob may ingest it without an obvious manual read. | Allowlist train/val input paths; deny test mounts to training/tokenizer jobs. | test path isolation |
| VI-07 | [x] | **Wrong cached tokenizer or token-bytes file** | The model may run successfully with a wrong vocabulary and invalidate comparability. | Verify both hashes and resolved real paths on host. | tokenizer hash preflight |
| VI-08 | [x] | **C3 manifest matches but packed runtime shards do not** | The filing specifically treats manifest-only matching as insufficient. | Hash actual consumed shards and origin mask for every C3 run. | runtime C3 shard hashes |
| VI-09 | [x] | **Seed fixed after model construction** | A seed call then becomes cosmetically present but does not determine initialized weights. | Compare wrapper ordering and initial-state SHA. | seed-knob-proof |
| VI-10 | [~] | **Different GPU stack after a new pod** | Numerical/environment drift can be hidden by a superficially working run. | Repeat host-contract preflight before each official new GPU gate. | I-preflight after restart |
| VI-11 | [x] | **Fresh optimizer claim is false because resume state is loaded indirectly** | It converts child continuation into a different optimization intervention. | Scan command/config/logs for resume and optimizer-state loads. | no optimizer resume |
| VI-12 | [x] | **P0-T computed on CPU or with a wrong seed** | Misclassifies eligibility and can change the panel path. | Record device, evaluator hash, initial-state seed, and safe status only. | P0-T CUDA seed-matched |
| VI-13 | [x] | **Seed 3 begun before seed 2 is resolved** | Violates ordering/no-skip conditions and complicates repair classification. | Gate scheduler refuses seed 3 until seed 2 has a lawful terminal status. | seed 3 after seed 2 V |
| VI-14 | [x] | **An unfavorable finite result is mislabeled “technical”** | Creates outcome-dependent exclusion. | Incident record must predate any scalar access and identify a technical cause. | S₂ not outcome-labeled technical |
| VI-15 | [x] | **NaN/Inf is seen but treated as an ordinary retry** | The filed taxonomy lists NaN/Inf as panel-level stop. | Health monitor escalates immediately; preserve logs and stop. | health pass all arms |
| VI-16 | [x] | **Missing terminal checkpoint conflated with cloud transfer delay** | Could trigger an incorrect panel stop or unauthorized retry. | Determine whether source terminal artifact exists, hashes, and can be verified before classifying. | S₂ terminal verified |
| VI-17 | [ ] | **P4 seed 0 appears in a table beside P5 cells and is counted implicitly** | Blurs historical disclosure with confirmatory panel data. | Distinct table section and explicit `historical only` label. | paper table must separate P4 seed 0 |
| VI-18 | [x] | **C3 byte share is described as the treatment definition** | P5 defines source-content token share, not byte share. | Use filed terminology in all reports and cards. | token-share terminology |
| VI-19 | [x] | **A result count is turned into a mean/p-value/CI during drafting** | Violates the filed count-only analysis. | Freeze a results-table template before Gate X. | count-only Gate X |
| VI-20 | [x] | **C1/C2 tests are run “for completeness”** | Directly violates C3-only protected-secondary policy. | Test runner hard-codes allowed model tag to C3_s. | C3-only test runner |
| VI-21 | [x] | **A second C3 test is run after a transfer or environment glitch** | Exceeds one event per eligible seed. | Test ledger increments before launch and rejects a prior count of one. | one test per seed |
| VI-22 | [x] | **P4 weights are used as an accidental convenience parent** | Breaks P5’s fresh-parent computational independence. | Parent wrapper refuses prior-study checkpoint paths and hashes. | forbidden_parents |
| VI-23 | [x] | **P1/P2/P3/P4 environment variables bleed into a P5 shell** | Could redirect cache, data, Hub target, or launch policy. | Start clean shell; print allowlisted P5 variables before launch. | P5 env isolation |
| VI-24 | [x] | **One panel Gate X occurs before all seed statuses are terminal** | Transforms the design into adaptive sequential analysis. | Gate-X script checks all three terminal/ineligible states. | gate-x-preflight terminals |
| VI-25 | [x] | **Public release or support message reveals a scalar before Gate X** | Breaks lockbox even without opening a local result file. | Review text/log attachments; share status/hash/count only. | blinded public updates |
| VI-26 | [x] | **A missing plan/addendum is replaced from memory** | Small implementation differences can change the filed recovery or seed policy. | Retrieve only the document matching the filed SHA; otherwise block the decision. | SHA-bound plan/addendum |
| VI-27 | [x] | **The same artifact is rehashed after a writeable-path operation** | A passed prior hash does not prove current identity. | Rehash after transfer/mount/copy and before the dependent gate. | post-rsync hash verify |
| VI-28 | [ ] | **Interpreter/library update changes deterministic wrapper behavior** | Seed/initialization and serialized state may change. | Include Python/Torch/container versions in initial-state receipt. | torch/container not on every init receipt |
| VI-29 | [x] | **A staged C3 file is regenerated under the same filename** | Filename continuity can disguise stream/order change. | Content hashes and provenance manifest, not names, govern identity. | content hashes govern identity |
| VI-30 | [~] | **A study-deviation is communicated verbally but not recorded** | Later readers cannot distinguish lawful repair from unlogged redesign. | Dated run card that names authority, event, scalar-access status, and disposition. | wait-start-resume.log; S₂ incident card thin |

---

## Six-layer acceptance matrix

Use this compact table at every major gate or incident.

| Question | Layer | `pass` requires | `blocked` / `escalate` condition |
|---|---|---|---|
| Is the action explicitly authorized? | I | Filed PDF item and, where needed, matching plan/addendum. | Not named or contradicts a filed item. |
| Can the action be demonstrated operationally? | II | Hash/path/command/ledger receipt. | Assertion only, missing provenance, or mutable asset. |
| Does it preserve the P5 estimand? | III | Common parent, fixed treatment, fixed budget, no outcome-based choice. | Changes what a seed-level contrast means. |
| Is it merely useful future work? | IV | Clearly labelled non-P5/documentary/future. | Being smuggled into confirmatory execution. |
| Is there an unresolved gap? | V | Authority source identifies the needed next check. | Filled from memory or post-outcome preference. |
| Could a silent failure fake compliance? | VI | Targeted audit was performed and recorded. | Hidden-risk signal or ambiguous incident. |

## Completion statement template

> “P5 compliance was assessed using a six-layer audit. All applicable Layer-I filed requirements were evidenced against AsPredicted #307836; Layer-II operational receipts preserved those requirements; Layer-III interpretations were kept within the seed-level BPB apparatus; Layer-IV items were treated as nonconfirmatory follow-ons; Layer-V residuals were disclosed; and Layer-VI hidden-risk checks were documented. This statement does not expand P5 beyond its filed claims.”

## References

[1]: https://aspredicted.org/k6ib64.pdf "AsPredicted #307836 — P5: multi-seed panel of the P4 token-share mix after fresh TL parents"
