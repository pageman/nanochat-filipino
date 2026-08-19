# P2 Gate R — comment compatibility addendum

- Date (UTC): 2026-08-19T03:23:00Z
- Sources reviewed (informal; not AsPredicted amendments):
  - `P2 Comment Compatibility Audit and P3-Safe Extension.md`
  - `What to Do with the Proposed P2 Comment: Clarification, P2.1, or P3?.md`
- **Decision: do not incorporate the proposed comment verbatim into P2. Do not amend #306935. Do not create a P2.1 intermezzo before A1.**

The comment’s valid content is already filed: two-depth P0-E, A0 freeze, A1/A2/A3 from byte-identical A0, validation seal before test, A2-only post-seal test. Inserting it as a new governing rule now would omit A3, compress P0-E into “the English base,” and blur filed status language (“void”).

## What was factored in (provenance only)

| Comment pressure | P2 action taken |
|---|---|
| “Train EN0 and pass P0-E first” | Already **pass** at both d8 and d20. Not reworded into a new kill-switch. |
| “If the English base fails, forgetting is void” | Not added. Filed language remains: P0-E fail **blocks** Tagalog continuation and prevents the planned A1–A2 contrast; it does not erase the study record. |
| “Run A1 and A2” | Incomplete. **A3 remains** in R→S→T→U. A1 is the causal extra-English control, not a disposable baseline. |
| “One-touch tests” | Kept as filed: **after Gate U seal**, **A2 only**, WT103-raw English test + P1.1 Tagalog holdout. No A1/A3 test comparison. |
| Switch continuation to d8 because English BPB is better | **Rejected.** Confirmatory parent remains A0 d20. |
| Skip A3 to save cost | **Rejected.** A3 is the predeclared mix/trade-off arm. |
| Treat A0 Tagalog BPB as adaptation | **Rejected.** Official CUDA A0 d20 Tagalog `val_bpb_full` 4.917650 is a pre-continuation baseline, not \(G_{TL}\). |
| chmod 444 = frozen | **Rejected as proof.** Hash `bd35a858…` and receipts remain authoritative. |
| P3 as confirmation of P2 | **Rejected.** P3, if wanted, is a separate preregistration filed before Gate U outcomes are seen. Do not interrupt R/S/T to draft it. |
| P2.1 because wrapper/archive were complex | **Rejected.** Those are execution provenance, already in run cards. |

## Governing sequence (unchanged)

Gate R/A1 → Gate S/A2 → Gate T/A3 → Gate U validation seal → one A2-only post-seal test.

This addendum does not change parent, depth, N, T, tokenizer, LR, mixture, or the sealed A1 command.
