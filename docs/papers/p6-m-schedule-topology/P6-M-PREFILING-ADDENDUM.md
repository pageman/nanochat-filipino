# P6-M prefiling addendum: schedule topology and recovery authority

Status: **PREFILING — NO P6-M OUTCOMES COLLECTED OR VIEWED**

This addendum is controlling only if its SHA-256 is named in the filed P6-M
AsPredicted PDF. It does not amend P1.1, P2, P3, P4, or P5.

## 1. Prior evidence and prospective boundary

P1.1, P2 (#306935), P3 (#307342), P4 (#307591), and P5 (#307836) are
pre-existing studies. Their released designs and outcomes motivated P6-M, so
P6-M is prospectively preregistered but **not outcome-independent**.

Before this filing, no P6-M seed-4 parent or child was trained; no P6-M
validation or restricted-test scalar was collected or viewed; no P6-M topology
comparison was computed; and no P6-specific model-selection outcome existed.
The reused English and Tagalog corpora, frozen splits, tokenizer artifacts, and
prior-study results are not P6-M outcome observations.

P6-M is a schedule-topology BPB experiment. It is not a downstream Filipino
task study, not a test of all Philippine languages, not an extension or
validation of Cheng's catastrophic-forgetting experiments, and not a
population estimate.

## 2. Authority order after filing

The authority order is:

1. the filed P6-M AsPredicted PDF;
2. this addendum at the SHA-256 named in that PDF;
3. the unmodified P6-M gate plan at SHA-256
   `d8a63608608c59d2c4d9882e5346625462056c331094942a8a01d496697a1c79`;
4. the P6 `LOCK.json` minted only after filing;
5. the P6 manifests and deterministic gate receipts.

If these sources conflict, the earlier source in the list controls. A missing
or mismatched controlling artifact is a protocol stop; it is not reconstructed
from memory.

## 3. Fixed design

- Parent initialization seed: **4**.
- Common parent: one fresh Tagalog d20 parent, frozen as `C0` only after the
  filed P0-T eligibility gate passes.
- Children: `C1`, `C2`, `M-fine`, `M-coarse`, `M-blocked`, and `M-rand`, all
  direct siblings from the same immutable C0.
- Child optimizer: freshly constructed for every child;
  `load_optimizer=False`; no parent optimizer state.
- Context length: `T=2048`.
- Batch size: `B=65536`.
- Child updates: `N=294`.
- Phase-two model-visible budget:
  `D_phase2=19,267,584 = 294 × 65,536`.
- Mixed-arm target quotas:
  `9,633,792` Tagalog source-content tokens and `9,633,792` English
  source-content tokens.
- Quota language: **source-content token quotas** under the carried-forward
  tokenizer, not document count, UTF-8 byte share, packed BOS/padding count, or
  a post-hoc observed proportion.
- Quota rounding: round-half-to-even for the Tagalog target; English is the
  exact residual. Here both targets are exact integers.
- Within-language stream identity: every mixed arm consumes the same
  preconstructed P4-lineage English token stream and the same preconstructed
  P4-lineage Tagalog token stream. Only the cross-language block schedule
  differs.
- Within-language construction: sort eligible train documents by SHA-256 of
  raw UTF-8 text, then independently apply Python `random.Random(42).shuffle`
  to each language list. Follow each shuffled list cyclically until its exact
  source-content quota is filled, truncating only the final document at a token
  boundary. This carries forward P4's `cyclic_per_language` quota construction
  unchanged; P6-M does not vary it. The no-wrap rule below applies to trainer
  consumption of the final mixed stream.
- Trainer consumption: consume the precomputed schedule exactly once in stored
  block-index order. No runtime reshuffle, per-epoch regeneration, worker
  randomization, or wrap is permitted.

Tokenizer identities:

- `tokenizer.pkl`:
  `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8`
- `token_bytes.pt`:
  `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132`

Frozen train split identities:

- English:
  `09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a`
- Tagalog:
  `2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687`

## 4. Pinned topology schedules

The prefiling generator is
`scripts/p6/prefile_topology_schedules.py`. It reads no corpus, checkpoint,
validation, test, or outcome artifact.

Controlling topology manifest:

- Path: `manifests/p6/p6_topology_schedule_manifest.json`
- SHA-256:
  `d1e7d5af7247a572e319ee003b5f4e3da5d1fb1592e5ed9ff6b22eeec15ea606`
- Combined schedule-file digest:
  `165d7084be485299b305935a6b76e80c53a03bd75ba5f90a74f5ca0714e8278d`

Each schedule is a UTF-8 TSV with one ordered row per block:
`block_index`, `language`, `source_offset_tokens`, and `length_tokens`.
The schedule-file SHA pins the serialized sequence. The language-origin-mask
SHA additionally pins one byte per scheduled source-content token (`EN=0`,
`TL=1`).

### 4.1 M-fine

- Algorithm: strict EN/TL alternation, starting with English.
- Block unit and nominal length: `2,048` source-content tokens.
- Counts: `4,704` English blocks and `4,704` Tagalog blocks; `9,408` total.
- Final-partial rule: take `min(2,048, remaining language quota)`. The filed
  quotas divide exactly, so no partial block occurs.
- Schedule file:
  `manifests/p6/topology-schedules/m-fine.tsv`
- Schedule SHA-256:
  `2503f5abead67264c1e180507b4f8fbc5454283f2dcafd150cb73f66b1076789`
- Language-origin-mask SHA-256:
  `140e174a427a7ddf2126553c53352ec049f72fbed475e2404cd4ef122b309c46`

The origin-mask SHA equals P4's filed C3 origin-mask SHA, making M-fine the
positive-control topology. This does not authorize loading P4 weights.

### 4.2 M-coarse

- Algorithm: strict EN/TL alternation, starting with English.
- Block unit and nominal length: `1,204,224` source-content tokens, exactly
  one eighth of each language quota.
- Counts: `8` English blocks and `8` Tagalog blocks; `16` total.
- Final-partial rule: take `min(1,204,224, remaining language quota)`. The
  filed quotas divide exactly, so no partial block occurs.
- Schedule file:
  `manifests/p6/topology-schedules/m-coarse.tsv`
- Schedule SHA-256:
  `3f5073e6afbc02bf3ec98c7da737e3f06d8a78fc9ec8f82adc10282ea02955dc`
- Language-origin-mask SHA-256:
  `2f739be813ef6c9e23eb3bc5a70e3bf508cbab4441c84f8b69e5421409a01453`

### 4.3 M-blocked

- Algorithm: consume the complete Tagalog quota, then the complete English
  quota.
- Block unit: one complete language quota.
- Boundary: tokens `[0, 9,633,792)` are Tagalog; tokens
  `[9,633,792, 19,267,584)` are English.
- Counts: `1` Tagalog block and `1` English block; `2` total.
- Final-partial rule: not applicable because each block equals its exact quota.
- Schedule file:
  `manifests/p6/topology-schedules/m-blocked.tsv`
- Schedule SHA-256:
  `eedcea17699ac911c76373c3a05494cbd79555785cb70820a82bbb37821942dd`
- Language-origin-mask SHA-256:
  `e6c0ff201dfa2b7546bea113c9f20933758b966e1cc1506c8bd7cc8eb637367d`

The TL-first direction is part of this treatment. P6-M does not estimate a
direction-free blocking effect.

### 4.4 M-rand

- Randomization unit: `2,048` source-content token language blocks.
- Multiset: `4,704` English labels and `4,704` Tagalog labels.
- PRNG: Python standard-library `random.Random` (MT19937).
- Seed: integer `42`.
- Precomputation: construct the complete 9,408-label multiset and call
  `random.Random(42).shuffle(...)` exactly once under Python `3.9.6`.
- Exact-quota method: the multiset contains the full exact count for each
  language before shuffling; there is no post-shuffle quota repair or tie.
- Runtime rule: load the stored TSV. Never call the PRNG during training,
  resume, dataloader construction, epoch transition, or worker startup.
- Final-partial rule: take `min(2,048, remaining language quota)` before
  shuffling. The filed quotas divide exactly, so no partial block occurs.
- Schedule file:
  `manifests/p6/topology-schedules/m-rand.tsv`
- Schedule SHA-256:
  `bf7e3c329d780ba0941d664deaa37a8bfb34c3b2641e0d6e0797b32b62f1d4c1`
- Language-origin-mask SHA-256:
  `923ecfe50353811a52f3492beea503c431118c03aafd1ffeee8435a2c03e3c7c`

M-rand is therefore one precomputed pinned schedule, not a distribution of
runtime schedules.

## 5. Measurement, sealing, and access order

The primary outcomes are the preregistered full-split validation BPB contrasts
in the filed form. All six named child conditions × two languages are evaluated
with the same pinned evaluator and remain lockboxed until one formal
unblinding.

The required order is:

1. complete and seal all filed validation cells;
2. perform exactly one authorized `M-fine`-only secondary restricted-test
   event;
3. perform one formal unblinding after all filed prerequisites pass.

`C1`, `C2`, `M-coarse`, `M-blocked`, and `M-rand` are never evaluated on the
restricted tests. No cross-topology test contrast, test-derived ranking, or
test-based model-selection decision will be computed.

In-loop monitoring is diagnostic only and cannot define an observation,
eligibility decision, model selection, topology choice, or result.

## 6. Technical recovery taxonomy

Recovery never authorizes outcome-dependent replacement, an additional seed,
an additional arm, a changed topology, or a changed budget.

Allowed technical incidents before protected outcome access include process
wrapper death, SSH/control-plane loss, pod-host capacity unavailability, and
storage-transfer interruption.

Rules:

1. No mid-arm resume from a partial checkpoint is permitted under this
   addendum.
2. A partial or unverifiable output is quarantined. If the incident was
   documented before outcome access, the same gate may restart from its
   immutable filed input:
   - a parent restarts from the filed seed-4 initialization procedure;
   - a child restarts from the immutable C0 with a fresh child optimizer and
     the full 294-update budget.
3. If a valid terminal checkpoint was already written before a wrapper or host
   failure, it must be hash-, metadata-, and reload-verified and accepted
   without retraining.
4. Host relocation is allowed only from a hash-verified portability capsule
   containing the pinned source, environment specification, immutable inputs,
   schedule, exact argv, gate ledger, and checkpoint inventory. Secrets are
   referenced, not copied into the capsule.
5. NaN/Inf, an outcome-bearing failure, a mismatched schedule/input, an
   unauthorized access, or an unrecoverable filed stop condition is reported
   under the failure taxonomy. It is not repaired by replacement or selective
   rerun.
6. Every incident receipt records UTC time, gate/arm, technical cause, input
   hashes, terminal-checkpoint status, protected-outcome access status, and
   disposition.

## 7. Exclusions and adjacent studies

P6-M does not vary document revisit policy (P7-M), parent-to-child optimizer
state (P8-M), replay/protection (P9-R/P10-R), tokenizer/corpus/language transfer
(P11-X/P12-X), source-content quotas, training budget, evaluator, or parent
lineage. It does not load P1.1–P5 checkpoints.

All finite terminal outcomes are retained. No seed or arm is replaced because
of the direction or magnitude of a result.
