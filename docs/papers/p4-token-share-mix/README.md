# P4 protocol package (filed; Gate 0 pass)

**P4 only.** Post-P3 token-share-locked EN/TL mixture after a **fresh** Tagalog parent. Does **not** amend #306780, #306935, or #307342. **C3 is not P3 B3.**

**Status:** Filed AsPredicted **#307591** ([if84km.pdf](https://aspredicted.org/if84km.pdf)). ResearchBox **#8869**. AsCollected **#2471** (`NANOCHAT-FILIPINO-P4`; Gate-0 prior #2455 v1). Run ID `p4-20260821T060032Z-92d63d4`. Confirmatory gates through **W** are closed. Hub: [`pageman/nanochat-filipino-p4-token-share-mix`](https://huggingface.co/pageman/nanochat-filipino-p4-token-share-mix) (C0+C1+C2+C3 together). Dummy lockbox tests 1–18 passed at Gate 0. Do not Make Public. Do not edit the SHA-bound master / gate bible / addendum (Q8 hashes). See `LOCK.json`.

| Document | Role |
|---|---|
| [PROTOCOL-p4-token-share-mix.md](PROTOCOL-p4-token-share-mix.md) | Master protocol (19 sections) |
| [PROTOCOL-p4-GATES-EXHAUSTIVE.md](PROTOCOL-p4-GATES-EXHAUSTIVE.md) | Super-granular gate bible (0, A–I, P0-T, Q–W, X). Operational order: **F before E**. |
| [P4-PREFILING-ADDENDUM-DRAFT.md](P4-PREFILING-ADDENDUM-DRAFT.md) | One SHA-embeddable scientific addendum (unsigned until PDF) |
| [aspredicted-answers-p4.txt](aspredicted-answers-p4.txt) | **File this:** 2-page AsPredicted paste pack |
| [aspredicted-answers-p4-onepage.txt](aspredicted-answers-p4-onepage.txt) | 1-page cut if preview still exceeds 2 pages |
| [P4-EXECUTION-CLARIFICATIONS.md](P4-EXECUTION-CLARIFICATIONS.md) | Non-amending definitions |
| [P4-MIX-CONSTRUCTION-SPEC.md](P4-MIX-CONSTRUCTION-SPEC.md) | C3 algorithm |
| [P4-BLINDING-AND-LOCKBOX.md](P4-BLINDING-AND-LOCKBOX.md) | Access / Gate X preflight |
| [P4-GATE-LEDGER.md](P4-GATE-LEDGER.md) | Ledger explanation |
| [P4-TEST-ACCESS-POLICY.md](P4-TEST-ACCESS-POLICY.md) | C3-only one-touch |
| [P4-DEVIATION-TEMPLATE.md](P4-DEVIATION-TEMPLATE.md) | Incident card |
| [P4-REPORTING-GRAMMAR.md](P4-REPORTING-GRAMMAR.md) | Post-X sentences |
| [P4-PAPER-OUTLINE.md](P4-PAPER-OUTLINE.md) | Paper skeleton |
| [P4-RELEASE-PLAN.md](P4-RELEASE-PLAN.md) | Hub/GitHub/RB |
| [LOCK.json](LOCK.json) | Filed identity; Gate 0 pass |
| [P4_PRE_OUTCOME_AUDIT.md](P4_PRE_OUTCOME_AUDIT.md) | F4-01–F4-22 checked against the filed PDF |
| [schemas/](schemas/) | Manifest templates |

**Unsigned before filing:** see `P4-PREFILING-ADDENDUM-DRAFT.md`. Scientific F4 items go in the PDF or that **one** hashed addendum — not a later pre-Gate-A note.

Recommended (not frozen): carry-forward **both** `tokenizer.pkl` `04436b85…` **and** `token_bytes.pt` `a5dbc1c8…`; \(q_{\mathrm{TL}}=0.50\) signed **before F**; \(\delta=0.01\); test Policy A; \(N=294\); NVIDIA A40 class; collect C0 EN once at U; P0-T CUDA-only; Python `random.Random` seed 42 for C3 lists.

Env (after filing): `scripts/p4/env.sh` — never `scripts/p1/env.sh`, `scripts/p2/env.sh`, or `scripts/p3/env.sh`.
