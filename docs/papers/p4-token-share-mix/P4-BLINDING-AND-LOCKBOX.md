# P4 blinding and lockbox

**Purpose:** Outcome isolation until Gate X.  
**Acceptance:** Lockbox acceptance tests at Gate 0; counters lawful; no scalar in safe logs.

## Counters (initial 0)

| Counter | Lawful +1 |
|---|---|
| `test_access_count` | Gate V event (Policy A) |
| `p4_outcome_access_count` | Gate X release |
| `validation_scalar_access_count` | Gate X (or lockbox decrypt for X officer only) |
| `lockbox_open_events` | Every authorized open |

Storage: `data/cache/<P4_RUN_ID>/lockbox/` mode 600, gitignored. Append-only `access.jsonl`: utc, actor, files, purpose, counters_after.

## Safe pre-X

Gate status; hashes; existence; counts; liveness; finite; smoke descent/reload; terminal ckpt existence; counter **values that are counts not BPB**; P0-T PASS/BLOCKED/TECHNICAL BLOCK.

## Forbidden pre-X

BPB; contrasts; signs; rankings; “best”; quality samples; screenshots of metrics; scalars in filenames; interpreted outcomes in chat/issues/paper drafts.

**`meta_*.json` `val_bpb`:** strip from operator-visible copies or keep entirely in lockbox.

## Gate X preflight

Status/provenance only. **Do not open scalars** during preflight. Required states: all prereq gates pass; C0–C3 hashes match; mix target/hash match; U before V; test 0 at U and 1 after V if A; C3-only tests; outcome access 0; no log leakage; incidents quarantined.

Then one combined release with timestamp, operator, file list, counter transitions.
