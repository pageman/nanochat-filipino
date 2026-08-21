# P4 gate ledger (human)

**Purpose:** Explain `manifests/p4_gate_ledger.json`.  
**Acceptance:** One row per gate; status ∈ {not_started, prepared, pass, blocked, technical_stop, protocol_stop, awaiting_authorization}.

| Field | Type |
|---|---|
| `gate` | string (0,A–I,P0-T,Q–W,X) |
| `status` | enum above |
| `at_utc` | ISO-8601 or null |
| `artifact` | path |
| `sha256_prefix` | 8+ chars or full |
| `safe_note` | no scalars |
| `next` | gate id |

**MUST NOT** store BPB in the ledger. Scalars live in lockbox until X, then `released/`.

Update authority: named gate script or operator with dual control at X.

**Operational order vs letters:** ledger keys stay `0,A–I,P0-T,Q–W,X` including both `E` and `F`. Because C3 is token-share-locked, **F MUST reach `pass` before E is marked `pass`.** See `PROTOCOL-p4-GATES-EXHAUSTIVE.md` §0.10.
