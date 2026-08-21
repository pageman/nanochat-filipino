# P4 release plan (Gate W only)

**Purpose:** Public surfaces without new science.  
**Acceptance:** No confirmatory training; Hub all-or-nothing; secrets absent.

| Surface | Rule |
|---|---|
| GitHub | `scripts/p4/`, `docs/p4/`, `docs/papers/p4-token-share-mix/`, `docs/run-cards/p4/`, `results/p4/`, `docs/hub/p4-token-share-mix/` — no HOST cards |
| Hub | C0+C1+C2+C3 + tokenizer **together**, or **all deferred** with dated reason. Never C3 alone. Never write onto P1/P2/P3 Hub IDs |
| ResearchBox | **New** box; not #8834. Dear Reader: not P3; C3 ≠ B3 |
| AsCollected | New project/version for P4 public-data provenance |
| Paper | After X; reporting grammar; post-P3 sentence |
| Secrets | No API tokens, SSH keys, lockbox plaintext, RB passcodes |

Archive: `p4_closeout_manifest.json` + SHA256SUMS. Re-hash downloads before use.
