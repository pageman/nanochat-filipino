# Review of the Revised P5 Multi-Seed Registration

## Verdict

This revised version is **substantially stronger** and resolves nearly all of the high-priority issues identified in the prior audit. It now states a concrete parent-initialization mechanism, uses seed-matched P0-T untrained floors, formalizes scalar quarantine through panel Gate X, adopts P5-owned scripts and an exact CUDA host contract, defines a no-outcome-exclusion rule, and gives an unusually clear P1.1–P4 inheritance statement.

> **Recommended decision:** The scientific design is filing-ready in principle. Before approval, make the four precision edits in the “Remaining required clarifications” section. They are operational clarifications of the filed plan, not new treatments, new hypotheses, or amendments to P1.1–P4.

The draft remains appropriately two pages. It should not be compressed to one page if that would require deleting the seed, lockbox, restart, or inherited-artifact commitments that make the panel interpretable.

## What the revision fixed well

| Prior concern | Revised text | Assessment |
|---|---|---|
| Parent seed was merely named, not operationalized | The P5 wrapper applies `torch.manual_seed(s)` and `torch.cuda.manual_seed(s)` immediately before `GPT.init_weights()` and records its SHA and initial-weight identity. | **Resolved in substance.** The wrapper’s timing and output identity should make parent initialization auditable. |
| Untrained P0-T comparator used fixed seed 0 | P0-T now uses untrained same-depth models with the same seed \(s\) as the parent. | **Resolved.** This is the cleaner comparator for a seed panel. |
| Scalar leakage was possible despite “no seed-level unblinding” | P0-T/U/V scalar files, evaluator stdout/stderr, and test reports are lockboxed and not inspected; test access is count-only. | **Resolved.** This is the key procedural control that gives “one panel Gate X” real operational meaning. |
| Technical failure versus unfavorable result was blurred | The form now separates protocol stop, pre-outcome technical quarantine/restart, and the prohibition on excluding finite official outcomes. | **Resolved in structure.** One ambiguity about the scope of a protocol stop remains below. |
| P4 environment-file reuse and host identity were unclear | The form specifies P5-only environment scripts and the A40/CUDA/Torch/container contract. | **Resolved.** This narrows host-side implementation variance without importing P4 execution state. |
| Panel execution order was incomplete | The form fixes `1 → 2 → 3`, requires all filed seeds to proceed, and permits one panel Gate X only after each seed reaches V or a P0-T stop. | **Resolved.** This prevents seed-by-seed adaptation or early stopping. |
| Linkage to the P1.1–P4 series was implicit | Q8 now distinguishes inherited infrastructure from fresh P5 weights and expressly says P5 is computationally independent but not outcome-independent of P4. | **Resolved.** This is accurate, candid, and unusually good preregistration language. |

## Why P5 is now cleanly linked to the earlier studies

The new Q8 is the right intellectual map. It treats the program as a stack of bounded instruments and treatments rather than as one endlessly amended experiment.

| Study | P5 connection | Boundary P5 preserves |
|---|---|---|
| **P1.1** | P5 inherits the frozen WikiText-TL-39 corpus, reconstructed split, protected Tagalog validation/test identity, BPB definition, and final-checkpoint/equal-budget discipline. | P5 does not load P1.1 weights or report P1.1 test BPB as a P5 observation. |
| **P2** | P5 inherits the canonical WikiText-103-raw source and matched-control/equal-budget lineage that later studies carry forward. | P5 is not a forward English-to-Tagalog replication and does not load P2 weights or use P2’s English tokenizer. |
| **P3** | P5 inherits the fresh Tagalog parent, P0-T, frozen common parent, extra-Tagalog versus English branches, protected validation-before-test sequence, and the carry-forward Tagalog tokenizer. | P5’s C3 is explicitly not P3’s document-balanced B3, and P3’s weights/results are not P5 data. |
| **P4** | P5 directly replicates P4’s distinct C3 treatment: exact \(q_{\mathrm{TL}}=0.50\) source-content-token-share construction, fixed packed stream, C1/C2/C3 branch geometry, primary contrasts, and C3-only secondary test policy. | P4 seed 0 is historical disclosure only; P5 does not reuse P4 weights, tune to P4 magnitudes, or claim outcome independence. |

The resulting construct is best described as a **predeclared three-new-seed recurrence panel for the P4 treatment**. It is stronger than another one-seed result, but it still does not estimate a model-population effect, justify a confidence interval, establish a universal mixture law, establish an optimal token share, identify a mechanism, or demonstrate mitigation efficacy.

## Remaining required clarifications

### 1. Make the wrapper’s model-construction boundary explicit

The new sentence is highly valuable, but it should establish that `GPT.init_weights()` is the point at which all trainable parameter initialization occurs in the pinned code path. Otherwise a future reader cannot tell whether constructors initialized parameters before the wrapper set the seed.

Add one short sentence to Q2 or the SHA-bound addendum:

> “The P5 wrapper constructs the official GPT model only after setting the filed Torch CPU/CUDA RNG state, or reinitializes every trainable GPT parameter through the pinned `GPT.init_weights()` call after that state is set; a SHA-256 of the serialized initial model state is recorded before parent training.”

Also specify whether all non-initialization stochastic states are fixed identically across seeds or intentionally inherit the model-initialization RNG stream. The cleanest replication interpretation is: **the intended experimental factor is model initialization; C3 order, dataset order, evaluator behavior, and all other controllable random sources are fixed.** If Python or NumPy RNG affects any P5-owned preprocessing/wrapper step, seed those streams with a named fixed value and record it.

### 2. Clarify whether a “protocol stop” ends one seed or the whole panel

Q6 says “Protocol stop (affected seed/study; no P5 result label),” which is too broad. For example, an inexact C3 quota in seed 2 could mean: terminate only seed 2 and continue with seed 3, terminate the entire panel because a replicated treatment was not delivered, or repair a pre-outcome construction defect and restart it. Those are scientifically distinct.

The preferred strict policy is:

> “A material integrity breach involving shared inputs, tokenizer, evaluator, packed C3 treatment, or test isolation is a **panel-level protocol stop**: no remaining seed is run under the compromised registry. A breach demonstrably isolated to an unexecuted seed-specific staging/output path is a **seed-level protocol stop**: no result is assigned to that seed, no replacement seed is added, and remaining seeds continue only if the shared registry is independently re-verified unchanged.”

If the authors prefer the most conservative policy, define every listed protocol breach as a panel-level stop. Either choice is defensible once filed; ambiguity is not.

### 3. Make the C3 identity check cover the actual trainer inputs, not only the manifest

The form correctly locks the P4 mix-manifest hash and says “do not reshuffle.” To preserve the exact P4 treatment, it should also name the hashes of the P4 packed train shards and the language-origin mask consumed by the trainer, or state that those values are listed in the SHA-bound addendum.

Add:

> “For each P5 C3 execution, the trainer-consumed packed train shard SHA-256 values and `language_origin_mask_sha256` must match the P4 freeze. Matching source JSONLs or a manifest alone is insufficient; a mismatch is handled under the filed protocol-stop rule.”

This is not an extra outcome control. It is the mechanical proof that the claimed token-share treatment was actually delivered.

### 4. Name the multi-seed test policy as a panel-specific exception to singular one-touch language

The draft correctly states “up to three C3-only test events, one per eligible seed.” Preserve that sentence, but add one clarifying line because prior studies used a single one-test-touch rule:

> “P5’s protected-secondary policy is **one C3-only test event per eligible predeclared seed**, hence zero to three total P5 test events; it is not one total test event for the whole three-seed panel. Each test remains post-seal, secondary, descriptive, and excluded from seed classification and the panel count table.”

This does not weaken the primary analysis because all seed classifications come from lockboxed validation cells. It simply describes the already-filed secondary-evidence design honestly.

## Two small optional wording improvements

The phrase “Does C3 retain more Tagalog than C2 and still acquire more English than C1?” is intuitive, but it is slightly less exact than the contrast definitions. Consider changing it to:

> “Does C3 yield lower held-out Tagalog BPB than C2 and lower held-out English BPB than C1?”

This keeps the question identical to the estimands and eliminates any potential ambiguity about what “retain more” or “acquire more” means.

The heading “Observational / archival data study” may be the closest available platform category. If no better option exists, retain it, but add a short Q8 sentence: “P5 uses archived public text but prospectively trains new computational models and generates new P5 evaluation outcomes; there are no human participants.”

## Submission recommendation

After the four required clarifications are written into the SHA-bound addendum and its hash is updated in the form, I would regard the registration as ready to submit. The previous substantial concerns are resolved. The remaining edits make the implementation audit-proof; they do not alter the proposed P5 question, contrasts, number of seeds, treatments, data, or outcome interpretation.

The study now makes a disciplined claim that earlier papers could not make: it prospectively asks whether the P4 token-share result recurs across a fixed, visible panel of new parent initializations, without allowing the first or second outcome to determine whether the third trajectory exists.

## References

[1]: https://aspredicted.org/6r6v4v.pdf "AsPredicted #306780 — P1.1"

[2]: https://aspredicted.org/xa56bs.pdf "AsPredicted #306935 — P2"

[3]: https://aspredicted.org/wd2pc8.pdf "AsPredicted #307342 — P3"

[4]: https://aspredicted.org/if84km.pdf "AsPredicted #307591 — P4"

[5]: https://huggingface.co/pageman/nanochat-filipino-p4-token-share-mix "P4 model card"

[6]: https://github.com/pageman/nanochat-filipino/tree/main/docs/p4 "P4 study record"

[7]: https://github.com/pageman/nanochat-filipino/tree/main/results/p4 "P4 released results"
