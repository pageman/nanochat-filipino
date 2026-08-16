# How to sign off and start Gate A

**This is not a new protocol.** AsPredicted #306780 remains the lock.  
**This is not permission to train d8/d12/d16/d20.** After sign-off you may start **Gate A only**.

Ordered path after sign-off:

> **A → B → C → D → E → F → G → H → stop for decision.**

Do not begin pilots, confirmatory depths, or any test evaluation until A–H are all `pass` and `python3 scripts/p1/preflight.py --require-pre-i` succeeds.

---

## What “sign-off” means

You sign off by making three dated facts true in the repo, then recording a commit/tag. There is no AsPredicted button and no extra form.

| # | Fact | Status now |
|---|---|---|
| 1 | Official registration PDF is in the repo and its SHA-256 is in the ledger | **Done** — `docs/run-cards/AsPredicted-306780.pdf` = `a34f119df557d2e763aa154e02b76b0ebcbcba1f3fb32c3219d85ae6395cc5ca` |
| 2 | Execution note, ledger, empty test-access log, budget stub, and template are the working copies | **Done** — note hash `71c2b992ef1771fc7f31cad6d2f259d23d5c3b99367e7b9cbdcf7ae749552c8e` |
| 3 | You name the execution host (GPU/CPU/storage) in `manifests/execution_host.json` | **You must decide** |
| 4 | One clean commit/tag of that baseline | **Say the word** — I will not commit until you ask |
| 5 | `P_scaling` capture method | **During Gate A**, after pinning `92d63d4`. Not a pre-A blocker. |

Item 5 was listed as an “immediate blocker” in the review. Operationally it is a **Gate A acceptance check**, not a reason to delay pinning nanochat. You cannot read `base_train.py` at that commit until Gate A clones it.

---

## Your two remaining actions

### Action 1 — name the host

Edit [../../manifests/execution_host.json](../../manifests/execution_host.json) or tell me which of these is true:

- **This Mac** is only for A–F (download, audit, split, shards, tokenizer). H/I will run on a named GPU box later.
- **A specific GPU machine** (hostname, GPU model, VRAM, disk) is the execution host from Gate A onward.
- **Cloud** (which account/SKU) is the execution host.

Gate A must record the *actual* machine. An unplanned later move is a ledger event, not a silent switch.

### Action 2 — ask for the baseline commit/tag

When the host field is filled, say: **commit and tag the pre-Gate-A baseline**.

Suggested tag: `p1.1-pre-gate-a`

That commit should contain:

- `docs/EXECUTION-CLARIFICATIONS-p1.1.md`
- `docs/run-cards/AsPredicted-306780.pdf`
- `docs/run-cards/SIGNOFF-gate-a.md`
- `manifests/gate_ledger.json`
- `manifests/gate_ledger.template.json`
- `manifests/budget_manifest.json`
- `manifests/test_access_log.json`
- `manifests/execution_host.json`
- `scripts/p1/preflight.py`

It must **not** contain parquet, checkpoints, or confirmatory BPB.

---

## After the tag: start Gate A

Gate A work, in order:

1. Clone nanochat and pin `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`.
2. Isolate `NANOCHAT_BASE_DIR`. Do **not** run `python -m nanochat.dataset`.
3. Add the one-line `NANOCHAT_DATA_DIR` hook; default behavior unchanged if the variable is unset.
4. Read pinned `base_train.py`, write the exact `P_scaling` capture method into the ledger.
5. Write the hardware/environment record for the host you named.
6. Set Gate A to `pass` only when those artifacts are hashed.

Then stop and start Gate B. Do not jump to H or I.

---

## Later (not required to start A)

| When | Action |
|---|---|
| Before H / I | Expand `preflight.py` to check source hash, split disjointness, active shards, tokenizer provenance, positive ratio, exact `D_actual`, and test exclusion. |
| At Gate D | Separate test directory, read-only if practical, evaluator writes `manifests/test_access_log.json`. |

---

## Check status

```bash
python3 scripts/p1/signoff_gate_a.py
```
