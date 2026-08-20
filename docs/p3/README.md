# P3 study record

**P3 only.** Reverse-direction continual pretraining: newly trained Tagalog parent from fresh weights, then matched English continuation. Does **not** amend AsPredicted #306780 or #306935. Does **not** reuse P1.1 or P2 weights.

**Filed:** AsPredicted [#307342](https://aspredicted.org/wd2pc8.pdf) (2 pages; generated 2026-08-19 12:27 PT). Local copy: [`docs/run-cards/AsPredicted-307342.pdf`](../run-cards/AsPredicted-307342.pdf). SHA256 `6cfad0386dff689ad73fa2bf80b70dd4ad191dc44e21e3e4c11c06825ae550b1`.

**Lock:** [`docs/papers/p3-reverse/LOCK.json`](../papers/p3-reverse/LOCK.json)  
**Protocol (SHA in PDF):** [`PROTOCOL-p3-tl-then-en.md`](../papers/p3-reverse/PROTOCOL-p3-tl-then-en.md) `899ba83f0b36f2b4bf4c16b3c675e58788d7763cb439f8a8c3a3c061bda2b986`  
**Env:** [`scripts/p3/env.sh`](../../scripts/p3/env.sh) — never `scripts/p1/env.sh` or `scripts/p2/env.sh`.

**Status:** Gates **A–X complete**. Gate X unblinded / released. Sealed results: [`results/p3/`](../../results/p3/). Paper v1.2: [`docs/papers/p3-reverse/`](../papers/p3-reverse/) · [ResearchGate](https://www.researchgate.net/publication/412889563_Tagalog_Retention_and_English_Acquisition_under_Equal-Budget_nanochat_Continual_Pretraining_v12_-_A_Preregistered_Post-P2_Reverse-Direction_Study_on_WikiText-TL-39_and_WikiText-103). Hub: [`pageman/nanochat-filipino-p3-tl-then-en`](https://huggingface.co/pageman/nanochat-filipino-p3-tl-then-en). ResearchBox [#8834](https://researchbox.org/8834); AsCollected [F36_C2C](https://ascollected.org/F36_C2C).

**Primary (one seed):** \(C_{tl}=1.023484\) **observed**; \(G_{en}=-1.697955\) **observed**. B3 is trade-off, not mitigation.

P3 is a **post-P2** prospective study. Do not cite P1.1 `1.164768` or P2 Gate V as P3.
