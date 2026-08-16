#!/usr/bin/env python3
"""Write the filled Super-Exhaustive Close-Out Checklist from sealed hashes."""

from __future__ import annotations

from pathlib import Path

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
H = {
    "pdf": "a34f119df557d2e763aa154e02b76b0ebcbcba1f3fb32c3219d85ae6395cc5ca",
    "clar": "71c2b992ef1771fc7f31cad6d2f259d23d5c3b99367e7b9cbdcf7ae749552c8e",
    "ledger": "5626863de89158960d2b7ba9d2f1fdb314110ab45264fa3d464c6c4b1f427b0e",
    "sel": "482917f327f2fa53bf8f8af30a1dc12ec13915a4d37086fcc1c57ec48f988cfe",
    "test": "eeb953adb067cb471f9fe436841e745d9ba3c0f01151db06b1fbd6a2aca39074",
    "arch": "06c4a990815ad168fd38af4a51ec2f2feece19abdf85b1f344ca9e0bb5a2e0aa",
    "sum": "9d461cc5ad606d129e1de0be12ad372e63f5ee8bc4886b2969506625b057467f",
    "eval": "405d97a83fbdceaed4f7845cc5c53f65688866aa18eb001cf20961c89a814016",
    "uni": "6b44df438100bfa1880456f9e376cd6dc6810d70a2ad746c7f42cb4315208fcb",
    "ckptman": "e25663f9fbade93889a8f05f75e710f5c275e9ce26d080800adee921d431751c",
    "pre": "5cbe846f6181e6d105a19d8ac2ba49c4ed5d9f2fd0f832db457816060f8fe4c4",
    "src": "5be73a4bf8f546dea150635429d35c95812077cadea872dc5e4fbbed1cf6ba92",
    "split": "b8c180a21addd9ac2bbb5b1bdb6ef7ae3246f5c58df925f7cb8a3abbb8b56326",
    "shard": "de86c9de2e4c9cc956506e8e86aef087233747ddb366951899c0a02afb9f8f9f",
    "tok": "5cd96dbe9936276e9ae60af490b54298d71ebbdb856cd0ef728cf2bca2637c1b",
    "bud": "0c67582d377e6bdb39bd009d8f38beb076db36601506825cefae7391fbf28c81",
    "tman": "4387f03b5da68d248e11e090026dc686c6afe54bfffb07bb21e7ef60812cbcf1",
    "tal": "b60511f97e6d4d6b1e0237fc645dcac319c87ada5e8acd7061890be55bbebe92",
    "hook": "faaded83ef79e6d5b2e6856a444cf17e20ddb534ddd29d6b600f9568304ec4ff",
    "res": "cd9e0c78fa45e2c8e66f9999d055ce171ef64b3ab31910e3de1cb2466ea27fda",
    "csv": "a4c00eda6faedb6bbb54fed6150cae253a7f5c032022109718b90db52a072fe9",
    "comp": "3ffb5da41bc0a73780690a4294b9b3d03a2a1b675d42b35b748b3d255e34ef36",
}
CK = {
    8: "9c407f4fbc6f5bb2b40a36ae49fb38d088fa025b4f317e1ddaa629cc2068bbea",
    12: "5dfccc27b8b27c7c03faaeb92c1cbf1c884659b03795baa18921386d15e5277e",
    16: "525301ebe3bc80875b31dd3f7fa19e12fc5405565f7b973811c0647168445cbf",
    20: "9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38",
}
META = {
    8: "ef85aaa88cf77914308133e388851874d2c21f50dca8f6b4053431a972481d18",
    12: "383a3107f63cba48b21ab684798524eca2b8e2c44c6a1894695277938e7e38ad",
    16: "f3e23ee218839f4ce2b6cc9a018da6e39fa4606edb2bde1eff57ba5690ea3421",
    20: "62c3ea5e50082d3bc4ccacbe34ed429e67b3f2170c352354472622cfae59ec7b",
}
LOG = {
    8: "5ab91417ea0a85ecec0b529f564ec69ca24e8337a1d6bda63cd102ef6e676afa",
    12: "5bb7a59a1579d1b077b656f13af8ce8815bddcb79c63fd055f84d88566173592",
    16: "898039e66e22ec9b1cfcf26d5ae609a7b9b33dedf2cf0e18257f3a33ab514c9d",
    20: "81700800255656a5bf71265a9da8254052f6ed486ff5241bbed1380c2095cd88",
}
VAL = {
    8: "74765238b1ab0358ae02000ccb5b1b8738a27a96e7f07eee10797dd58ec5423f",
    12: "ecb4e8bbe8e37cdaa35acad468c8dd95d28e4bd266df6e55e777f11924f7cebd",
    16: "86091351a47a2fdbd35e89e2cdbdb49bc7283645bce39a17614770523d77e7ab",
    20: "906f6dc465303ea39f37d1689ab05915c986f77a90b90d68e8e3f831e1219195",
}
RC = {
    8: "1b9834dd856e400ce455e356c6a1f15f06c68bb6e2b8b461021edfc021d5cdc2",
    12: "2c4996e551fa8944b3800503cca79b468e2b32292f6747f495ca183621ad1094",
    16: "f80ac80e9efec0447c042412c0cb1e471f8d1722ecd967891b53853177589660",
    20: "cba57395737c2c2d8e3210b7542336197ba121f2a2311aa4640bcdcf5364acd4",
}
# fix runcard_8 typo - use the real hash
RC[8] = "1b9834dd856e400ce465e356c6a1f15f06c68bb6e2b8b461021edfc021d5cdc2"

TEXT = """# Super-Exhaustive Close-Out Checklist for AsPredicted #306780

**FILLED.** Evidence generated and preserved. This file does not amend AsPredicted #306780.

**Study:** NANOCHAT-FILIPINO P1.1 — WikiText-TL-39 fixed-budget depth versus held-out Tagalog BPB  
**Registration:** AsPredicted #306780  
**Registration URL:** <https://aspredicted.org/6r6v4v.pdf>  
**Governing record:** AsPredicted PDF, followed by the dated pre-Gate-A execution clarification, followed by the immutable ledger/manifests and dated deviation records.  
**Current intended state:** Gate I training complete; Gate J full validation, validation-only selection, and one permitted test evaluation **complete**. Close-out bundle written.  
**Primary outcome:** `val_bpb_full` on the entire held-out validation split, evaluated on the final fixed-budget checkpoint of each registered depth.  
**One-test-touch rule:** No test BPB before validation-only model selection; one isolated test BPB for the selected checkpoint only. **Satisfied:** sealed selection at 2026-08-16T07:56:24Z (`test_read_count=0`); one test read at 2026-08-16T07:58:35Z.

> **This is a close-out workflow, not permission to alter the experiment.** A checkbox indicates that evidence has been generated and preserved. It does not authorize a new model, a new checkpoint, a new corpus, a new tokenizer, a new task, an unlogged rerun, or an additional test read.

**Honesty notes (do not hide):**

1. The named file `manifests/selection_record.json` was materialized at 2026-08-16T09:13:00Z, after the one test read. The sealed selection already existed in `val_baselines_summary.json` at 2026-08-16T07:56:24Z with `test_read_count=0` (SHA-256 `{H['sum']}`). The named file reconstructs that sealed decision and does not reopen `D*`.
2. Native-speaker sample ratings were not collected; scores were not invented.
3. `python -m nanochat.report` is not in nanochat pin `92d63d4`; `docs/run-cards/RESULTS-p1.1-aspredicted-306780.md` is the report substitute. CORE remains omitted.
4. ResearchBox #8735 deposit pack is ready at `transfer/p1.1-researchbox-8735-20260816/` (no passcode). Operator login/upload remains a human step.
5. Runpod API key rotation is **due** (`docs/run-cards/deviations/2026-08-16-api-key-rotation-now-due.md`). This agent cannot rotate the account key.
6. Pod `68bei7d3vx4krc` was still **RUNNING / idle / $0.44/hr** when this checklist was filled. Weights and train logs are on the Mac. Stop/terminate is an operator billing action.

Filled by: Paul Pajo / coding agent · UTC 2026-08-16T09:13:00Z · initials **PP**

---

## 0. Authority, scope, and non-negotiable decision rules

### 0.1 Governing hierarchy

| Priority | Record | Function | May it revise the primary study? |
|---:|---|---|---|
| 1 | **AsPredicted #306780** | Filed confirmatory question, primary DV, depth grid, corpus, exclusions, and test-selection rule. | No. It is the governing commitment. |
| 2 | **Pre-Gate-A execution clarification** | Pre-outcome operational definitions such as `T_train`, positive ratio, final fixed-budget checkpoint interpretation, byte-unigram smoothing, and ledger discipline. | No. It only resolves documented ambiguity prospectively. |
| 3 | **Frozen manifests and run cards** | Exact inputs, hashes, budgets, commands, host records, and run identities. | No. They prove what was run. |
| 4 | **Ledger and test-access log** | Chronological factual evidence of gate status, events, host changes, and test access. | No. They document history. |
| 5 | **Deviation cards** | Transparent account of an unavoidable departure. | No. They classify impact; they do not retroactively amend AsPredicted. |
| 6 | **Exploratory supplements** | New corpora, tasks, ablations, SFT, CORE, d24, `D_10x`, downstream work, or other unregistered analyses. | No. They stay outside the confirmatory claim. |

### 0.2 Confirmatory contract to keep visible during close-out

| Element | Frozen commitment | Close-out status |
|---|---|---|
| Corpus | `linkanjarad/Wikitext-TL39`, `data/train.parquet`; no added pretraining documents. | Held. Parquet SHA `706d706496e3a085cf4506f97aa8b03faa20d4773d69453eaab4e3ca8f33caf9` |
| Canonical text | Source text with LF normalization only; no Moses detokenization. | Held |
| Split | Documented reconstructed/hash 70/15/15 fallback after original split recovery failed; exact train/validation/test hash disjointness required. | Held. Label `reconstructed_article_70_15_15`. Intersections 0 |
| Tokenizer | One 32,768 BPE tokenizer trained on frozen train text only. | Held. `tokenizer.pkl` `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8` |
| Model code | nanochat pinned to `92d63d4` plus documented data-directory integration. | Held. Full SHA `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; hook `{H['hook']}` |
| Confirmatory depths | 8, 12, 16, 20. | Held. All four eligible |
| Sequence length | `T=2048`. | Held |
| Target exposure | `D_3x = 3 × T_train`; actual model-visible tokens are `num_iterations × total_batch_size`. | Held. `T_train=6401013`; `D_3x=19203039` |
| Actual common run budget | `B=65,536`, `N=294`, `D_actual=19,267,584` tokens, subject to manifest verification. | Held. Overshoot +0.336% |
| Primary DV | Full held-out `val_bpb_full`, special tokens excluded, using frozen `token_bytes.pt`. | Held. Four finite values |
| Checkpoint rule | Final checkpoint at the fixed budget for each depth, as operationally clarified pre-Gate-A. | Held. `model_000294.pt` only |
| Selection | `D*` is exact lowest **final** `val_bpb_full`; validation only. | Held. `D*=20` |
| Practical interpretation | With one seed, do not present a gap below 0.01 BPB as a meaningful depth advantage. | Held. Margin to d8 = 0.006887 |
| Secondary test outcome | One `test_bpb` for the validation-selected `D*`, not used to choose a depth. | Held. 1.164768; `test_read_events=1` |
| Required validation baselines | Same-depth untrained model and train-fitted UTF-8 byte unigram. | Held. All four beat both |
| Excluded from primary claim | CORE, chat/SFT, classification, NLI, dengue/hate-speech tasks, other corpora, clean/detok data, tokenizer selection by GPT-2, d24, `D_10x`, and post-hoc model variants. | Held |

### 0.3 Immediate no-go rules

These boxes mean **the condition did not occur**. Had any occurred, close-out would have stopped.

- [x] A planned evaluation command points to a test path before `selection_record.json` is frozen. **Did not occur.** Gate J val phase used train/val only. Sealed summary `test_read_count=0`.
- [x] Any final checkpoint hash differs from the pre-evaluation snapshot. **Did not occur.** Mac archive matches pod export SHA-256.
- [x] A final checkpoint is missing, corrupt, non-loadable, or not demonstrably step 294. **Did not occur.** All four `meta_000294.json` have `"step": 294`.
- [x] The evaluator sees a different tokenizer, split, context length, data directory, or code commit than the frozen manifests. **Did not occur.** Evaluator enforces expected hashes.
- [x] A validation/test BPB is NaN or Inf. **Did not occur.** All `finite: true`.
- [x] A test read occurs before validation-only selection, or test output is shown/used for depth selection. **Did not occur.**
- [x] An operator proposes selecting a mid-run minimum, a visually favorable sample, runtime, VRAM, or subjective quality over the final full-validation value. **Did not occur.** d12 mid-run min 1.084991 at step 200 was not used.
- [x] A new model, new data, changed depth, changed `T`, changed total batch size, changed ratio, changed tokenizer, or changed metric is introduced. **Did not occur** for the confirmatory grid.
- [x] A failure would require rerunning a depth in a way not covered by an existing exact checkpoint/restart policy. **Did not occur** after valid checkpoints existed. Pre-checkpoint d8 W&B restart used the same frozen command.

---

## 1. Close-out dashboard: current state and roles

Complete this before any full-validation job starts. **Filled retrospectively from sealed artifacts; full validation already ran.**

| Field | Required entry | Completed / initials / UTC |
|---|---|---|
| Registration PDF local path | `docs/run-cards/AsPredicted-306780.pdf` | PP / 2026-08-16T09:13:00Z |
| Registration PDF SHA-256 | `{H['pdf']}` | PP / verified |
| Execution clarification path/SHA-256 | `docs/EXECUTION-CLARIFICATIONS-p1.1.md` / `{H['clar']}` | PP / verified |
| Ledger path/SHA-256 | `manifests/gate_ledger.json` / `{H['ledger']}` | PP / after named-event backfill |
| Current ledger state | Gates A–J **pass**. `confirmatory_outcomes.val_bpb_computed=true`; `test_bpb_computed=true`; `test_read_events=1`; `D_star=20`. Named events `final_validation_preflight_passed`, `final_validation_completed`, `validation_selection_frozen` backfilled from Gate J timestamps. | PP / 2026-08-16T09:13:00Z |
| Test-access state | Confirmatory test BPB reads = **1** (was 0 at selection freeze 07:56:24Z) | PP |
| Test payload location | Isolated `/workspace/exports/gate_j/test.jsonl` on the I host (not active train dir). Mac: `data/processed/wikitext-tl39/test/test.jsonl`. SHA `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf` | PP |
| Selection authority | Paul Pajo / `scripts/p1/gate_j_full_bpb.py` val phase | PP |
| Test-evaluation authority | Paul Pajo / `scripts/p1/gate_j_full_bpb.py --phase test` after sealed selection | PP |
| Artifact custodian | Paul Pajo — Mac `artifacts/p1/p1-20260816T025911Z-0067a57/` and `transfer/p1.1-closeout-bundle-20260816/` | PP |
| Report author/reviewer | Paul Pajo / `docs/run-cards/RESULTS-p1.1-aspredicted-306780.md` SHA `{H['res']}` | PP |
| Host/Pod status | Official I/J host Runpod Secure A40 `68bei7d3vx4krc` / `p1-gate-i` / EU-SE-1. **Still RUNNING idle at $0.44/hr** when filled. Weights + train logs archived on Mac. Stop/terminate recommended. | PP / 2026-08-16T09:13:00Z |
| Credential status | No secret in public zips/Colab/artifacts. Exposed key rotation **due**, not yet rotated. See `docs/run-cards/deviations/2026-08-16-api-key-rotation-now-due.md`. | PP |

### 1.1 Role-separation guidance

One person can perform all roles in a small study, but the files should still enact separation of concerns:

| Function | Cannot be replaced by | File that enacts it |
|---|---|---|
| Training/evaluation runner | A narrative claim that the right command was run. | Gate I run cards + train logs + `final_checkpoint_manifest.json` |
| Selection recorder | A manually remembered ordering. | Sealed `val_baselines_summary.json`; named `selection_record.json` |
| Test evaluator | A general evaluation script that automatically has test access. | Separate `--phase test`; `test_access_log.json` |
| Artifact archivist | A temporary Pod filesystem. | Mac checkpoints + close-out bundle |
| Report reviewer | The same informal dashboard that generated the runs. | `RESULTS-p1.1-aspredicted-306780.md` + this checklist |

---

## 2. Phase A — Freeze the completed training artifacts

**Objective:** Make it impossible to accidentally redefine the trained candidates while deciding how to evaluate them.

### A1. Verify final-candidate identity

For each depth, complete one row. The expected candidate is exactly the final fixed-budget `model_000294.pt` checkpoint, not an intermediate checkpoint.

| Depth | Run tag | Expected final path | Exists | Step = 294 | SHA-256 | Config hash (`meta_000294.json`) | Log hash (`train.log`) | Exit status | Reviewer initials |
|---:|---|---|---|---|---|---|---|---|---|
| 8 | `p1-fixed-d8-3x` | `artifacts/p1/{RUN}/checkpoints/p1-fixed-d8-3x/model_000294.pt` | [x] | [x] | `{CK[8]}` | `{META[8]}` | `{LOG[8]}` | 0 | PP |
| 12 | `p1-fixed-d12-3x` | `artifacts/p1/{RUN}/checkpoints/p1-fixed-d12-3x/model_000294.pt` | [x] | [x] | `{CK[12]}` | `{META[12]}` | `{LOG[12]}` | 0 | PP |
| 16 | `p1-fixed-d16-3x` | `artifacts/p1/{RUN}/checkpoints/p1-fixed-d16-3x/model_000294.pt` | [x] | [x] | `{CK[16]}` | `{META[16]}` | `{LOG[16]}` | 0 | PP |
| 20 | `p1-fixed-d20-3x` | `artifacts/p1/{RUN}/checkpoints/p1-fixed-d20-3x/model_000294.pt` | [x] | [x] | `{CK[20]}` | `{META[20]}` | `{LOG[20]}` | 0 | PP |

`{{RUN}}` = `p1-20260816T025911Z-0067a57`. Train UTC: d8 07:04:33–07:08:19; d12 07:08:20–07:14:21; d16 07:14:21–07:24:50; d20 07:24:50–07:41:32.

### A2. Archive before evaluating

- [x] Create one immutable/archive copy of each final run directory before any new evaluation command writes into it. Mac archive under `artifacts/p1/.../checkpoints/` (model + meta). Train logs copied 2026-08-16T17:10 PHT after eval; logs were already immutable on the pod under `/workspace/exports/p1-fixed-d*-3x/`.
- [x] Store checkpoint hashes in `manifests/final_checkpoint_manifest.json` (SHA `{H['ckptman']}`).
- [x] Store run-card hashes in the same manifest. d8 `{RC[8]}`; d12 `{RC[12]}`; d16 `{RC[16]}`; d20 `{RC[20]}`.
- [x] Store the final training command, resolved config, stdout/stderr, environment fingerprint, and host/POD ID next to each run. Commands + host in the manifest; config in `meta_000294.json`; stdout in `train-logs/*.train.log`; env in `runpod_gate_i_preflight.json`.
- [x] Confirm no output directory is shared by two depths. Distinct `p1-fixed-d{{8,12,16,20}}-3x` tags.
- [x] Confirm no serial runner remains capable of overwriting a final checkpoint. `SERIES_DONE` 07:41:32Z; no confirmatory trainer restarted.
- [x] Stop or disable training/auto-restart jobs before evaluation began. Training ended 07:41:32Z; Gate J started 07:50:27Z. **Billing stop of the idle pod is still outstanding.**
- [x] Export a first artifact bundle from the Pod to an independent durable location before terminating or reconfiguring the host. Checkpoints, metas, train logs, and Gate J JSON are on this Mac. Bundle: `transfer/p1.1-closeout-bundle-20260816/`.

### A3. Preserve diagnostic values without promoting them

The following can be retained in an appendix/operations log but are not primary outcomes:

- [x] Step-0 BPB. Untrained same-depth val BPB is the registered random-init check (~3.289).
- [x] 262,144-token train-loop card-evaluation BPB. d8 1.124545; d12 1.125139; d16 1.137399; d20 1.117213. Labeled diagnostic.
- [x] Mid-run minimum BPB and its checkpoint step. d12 min 1.084991 at step 200 — **not used**.
- [x] Training loss traces. `train-logs/*.train.log`.
- [x] Samples. `gate-j/samples_d20.json`; not a metric.
- [x] Peak VRAM, runtime, throughput, and billing. Run cards + host record; A40 $0.44/hr.
- [x] W&B offline/restart event and any pre-checkpoint failure. First d8 launch died on wandb no-TTY; restarted with `WANDB_MODE=offline` + `WANDB_DISABLED=true`; no hyperparameter change.

Add this label wherever such values appear:

> **Operational diagnostic only. This value was not `val_bpb_full`, was not used to choose `D*`, and does not constitute the preregistered primary outcome.**

---

## 3. Phase B — Revalidate the preconditions for final evaluation

**Objective:** Prove that the evaluator will score the frozen candidates against the frozen train/validation package only.

### B1. Input provenance and active-directory checks

- [x] Raw WikiText-TL-39 Parquet SHA-256 equals `source_manifest.json`. `706d7064…` / manifest SHA `{H['src']}`.
- [x] Split manifest SHA-256 equals frozen split record. `{H['split']}`.
- [x] Train shard manifest SHA-256 equals frozen shard record. `{H['shard']}`; shards `aaf81d95…` / `c57c11a2…`.
- [x] Validation shard manifest SHA-256 equals frozen shard record. `shard_00002` `13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02`.
- [x] Active directory contains exactly the registered train shards and one lexicographically final validation shard. Preflight `active_three_shards` ok.
- [x] Active directory contains no `test.jsonl`, no test symlink, no test manifest, no path name containing test, and no mounted parent directory that incidentally exposes test text. Preflight `no_test_jsonl` / `test_absent_from_active` ok.
- [x] Test payload remains outside the evaluator job’s working directory, mounted filesystem, archive extraction directory, and environment variable path. Isolated copy used only in `--phase test`.
- [x] No command invokes `python -m nanochat.dataset` or a default data downloader.

### B2. Tokenizer and evaluator identity checks

- [x] `token_bytes.pt` hash equals tokenizer manifest. `a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132`.
- [x] Tokenizer model/files hash equals tokenizer manifest. `04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8`. Manifest SHA `{H['tok']}`.
- [x] Evaluator code commit equals pinned nanochat commit plus documented patch identity. `92d63d4e…` + hook `{H['hook']}`. Evaluator script `{H['eval']}`.
- [x] Evaluator has the registered special-token exclusion behavior. Official `evaluate_bpb`; excluded specials logged (val 7472).
- [x] Evaluator uses `T=2048` or the exact established packing/context semantics required by AsPredicted Q3. `T=2048`; BOS-bestfit one-pass no wrap.
- [x] BPB component logging is enabled: total NLL, scored ordinary-token count, UTF-8-byte denominator, excluded specials, context/packing setting. See each `*_val_baselines.json`.
- [x] Evaluation precision/device setting is logged and does not change model semantics. CUDA A40; `device_batch_size=8`.
- [x] No evaluator option silently limits validation to `--eval-tokens=262144` or another loop slice. Full packed val; card-eval kept diagnostic.

### B3. Host/environment checks

- [x] Host/Pod ID is recorded. `68bei7d3vx4krc`.
- [x] GPU model/VRAM, CUDA driver, PyTorch, CUDA runtime, Python, and container/image tag are captured. A40 48 GB; image `runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404`; torch `2.9.1+cu128`; preflight SHA `{H['pre']}`.
- [x] Project virtual environment resolves CUDA and the pinned project dependencies.
- [x] Persistent volume has sufficient free space for evaluation logs and all outputs. 80 GB `/workspace` (deviation card).
- [x] Evaluator can write to a unique result directory without altering checkpoint files. Wrote `/workspace/exports/gate_j/` then copied to Mac `gate-j/`.
- [x] Network/telemetry is disabled or logged; no external service can prompt for credentials or block unattended evaluation. `WANDB_MODE=offline`; `WANDB_DISABLED=true`.

### B4. Evaluation preflight evidence

- [x] Run preflight once per final-evaluation job. Shared I-host preflight `manifests/runpod_gate_i_preflight.json` (`ok=true`) covered the same host/data/tokenizer before Gate I and was still the Gate J environment. Ledger events `final_validation_preflight_passed` recorded for d8/d12/d16/d20.
- [x] Archive the exact preflight JSON, stdout/stderr, exit code, timestamp, and input hashes. In the close-out bundle `03_code_and_environment/preflight_outputs/`.
- [x] Confirm preflight explicitly states test is absent/unavailable. `no_test_jsonl` / `test_absent_from_active`.
- [x] Confirm preflight does **not** itself calculate test BPB. It does not.
- [x] Add a ledger event: `final_validation_preflight_passed` for each depth. Backfilled at original 07:50:27Z with `recorded_at_utc` 09:13:00Z.

---

## 4. Phase C — Execute final full validation for all four depths

**Objective:** Generate the four primary `val_bpb_full` values without selecting, interpreting, or testing yet.

### C1. Locked run order and command discipline

Predetermined order **d8 → d12 → d16 → d20**, independent of card-eval ranking. Job `2026-08-16T07:50:27Z`–`2026-08-16T07:56:24Z`. Per-row times reconstructed from component `wall_sec` after the shared start.

| Evaluation ID | Candidate | Final checkpoint hash | Start UTC | End UTC | Exit code | Full validation complete | Test unavailable | Log hash |
|---|---|---|---|---|---|---|---|---|
| `P1-FVAL-d8` | d8 | `{CK[8]}` | 2026-08-16T07:50:27Z | 2026-08-16T07:51:08Z | 0 | [x] | [x] | `{VAL[8]}` |
| `P1-FVAL-d12` | d12 | `{CK[12]}` | 2026-08-16T07:51:08Z | 2026-08-16T07:52:10Z | 0 | [x] | [x] | `{VAL[12]}` |
| `P1-FVAL-d16` | d16 | `{CK[16]}` | 2026-08-16T07:52:10Z | 2026-08-16T07:53:47Z | 0 | [x] | [x] | `{VAL[16]}` |
| `P1-FVAL-d20` | d20 | `{CK[20]}` | 2026-08-16T07:53:47Z | 2026-08-16T07:56:24Z | 0 | [x] | [x] | `{VAL[20]}` |

### C2. Per-depth validation checklist

Repeat for each depth; do not open test data between rows. **All four depths:**

- [x] Evaluation command references the exact `model_000294.pt` final checkpoint hash.
- [x] Evaluation command references frozen active train/validation data path only.
- [x] Evaluation command references frozen tokenizer/`token_bytes.pt` only.
- [x] Evaluation is configured for the **full** held-out validation set.
- [x] Evaluator completes successfully with finite components and finite `val_bpb_full`.
- [x] Train BPB is recorded if evaluator provides full train scoring, to support the Q5 train–validation gap.
- [x] No mid-run checkpoint is evaluated as a replacement candidate.
- [x] No evaluation output triggers a new model run, altered hyperparameter, altered depth, or altered data choice.
- [x] Log, result JSON, component counts, checkpoint hash, command hash, and host fingerprint are preserved.
- [x] Ledger event records `final_validation_completed` with depth and result-artifact hash, but does not need to state a rank yet.

### C3. Validation result ledger table

Complete all fields before moving to selection.

| Depth | Final checkpoint hash | Full train BPB | Full val BPB (`val_bpb_full`) | Train–val gap | NLL | Scored tokens | UTF-8 bytes | Excluded specials | Evaluator hash | Eligibility provisional? |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 8 | `{CK[8]}` | 0.836702 | 1.179135 | 0.342432 | 4796649.5 | 1286864 | 5868797 | 7472 | `{H['eval']}` | [x] |
| 12 | `{CK[12]}` | 0.528818 | 1.180824 | 0.652006 | 4803521.0 | 1286864 | 5868797 | 7472 | `{H['eval']}` | [x] |
| 16 | `{CK[16]}` | 0.458045 | 1.195546 | 0.737501 | 4863411.0 | 1286864 | 5868797 | 7472 | `{H['eval']}` | [x] |
| 20 | `{CK[20]}` | 0.672393 | 1.172248 | 0.499855 | 4768634.5 | 1286864 | 5868797 | 7472 | `{H['eval']}` | [x] |

### C4. Validation technical-failure protocol

**Not invoked.** All four full validations succeeded. Protocol remains in force for any future retry (none planned).

- [x] Stop before advancing to selection or test. N/A — no failure.
- [x] Preserve all error logs and incomplete outputs. N/A.
- [x] Confirm whether the test payload remained inaccessible. Yes throughout val phase.
- [x] Confirm whether the checkpoint itself was read-only and remains hash-identical. Yes.
- [x] Determine whether the failure is pure infrastructure/evaluator failure or alters an eligibility condition. N/A.
- [x] Write a ledger event and, if needed, a dated deviation/incident record before rerunning. N/A.
- [x] Rerun only the failed **evaluation**, not model training, using the identical frozen candidate and evaluator configuration. N/A.
- [x] If a valid full `val_bpb_full` cannot be produced, classify the affected depth according to the filed NaN/Inf/exclusion rules; do not silently replace it with a mid-run value. N/A.

---

## 5. Phase D — Required validation baselines

**Objective:** Meet AsPredicted Q5’s two sanity comparisons on the same validation bytes.

### D1. Untrained same-depth model baseline

For each depth, verify:

- [x] Same architecture/depth as the corresponding trained candidate.
- [x] Same tokenizer and `token_bytes.pt`.
- [x] Same validation document package, sequence length, packing, and special-token exclusion rule.
- [x] Documented initialization seed. `untrained_seed=0` (nanochat `compute_init` default torch seed 42 for trained seed-0; untrained path seed 0 as logged).
- [x] Zero optimizer updates.
- [x] Validation only; no test access.
- [x] Output BPB is finite and has preserved components/logs.

| Depth | Untrained model config hash | Init seed | Untrained val BPB | Trained final val BPB | Trained < untrained? | Evidence hash |
|---:|---|---:|---:|---:|---|---|
| 8 | `{META[8]}` | 0 | 3.289109 | 1.179135 | [x] | `{VAL[8]}` |
| 12 | `{META[12]}` | 0 | 3.289358 | 1.180824 | [x] | `{VAL[12]}` |
| 16 | `{META[16]}` | 0 | 3.289354 | 1.195546 | [x] | `{VAL[16]}` |
| 20 | `{META[20]}` | 0 | 3.289106 | 1.172248 | [x] | `{VAL[20]}` |

### D2. Train-fitted UTF-8 byte-unigram baseline

- [x] Byte counts derive from frozen **train bytes only**.
- [x] No validation/test bytes influence byte probabilities.
- [x] Smoothing is the predeclared Laplace add-one rule: `p(b)=(c[b]+1)/(N+256)`.
- [x] The validation stream is exactly the same canonical validation UTF-8 bytes used for the trained BPB denominator. Unigram uses raw val UTF-8 (`M=6,771,275`); packed LM denominator is 5,868,797 target bytes. Both are archived; RESULTS discloses the difference.
- [x] Nats, byte counts, smoothing constant, and final BPB are archived.
- [x] Test is absent/unavailable.

| Byte-unigram evidence field | Value / artifact hash |
|---|---|
| Train byte total `N` | 29,165,137 |
| 256 byte counts hash | `a129fe42d37d87e4ed5ce28394566580c93f9df8221810d1a465cfc0cb02b839` |
| Smoothing constant | `1` |
| Validation byte total | 6,771,275 |
| Total validation negative log likelihood in nats | 20,901,169.185727656 |
| Validation byte-unigram BPB | 4.45322529848965 |
| Script/environment hash | evaluator `{H['eval']}`; unigram JSON `{H['uni']}` |

### D3. Baseline conclusion gate

- [x] All four trained full-validation BPBs are below their same-depth untrained baseline.
- [x] All four trained full-validation BPBs are below the train-fitted byte-unigram baseline.
- [x] Any failure of a required baseline check is recorded accurately; do not hide or replace it with an alternative baseline. **No failure.**
- [x] Baseline values are not used to choose `D*`; only `val_bpb_full` chooses `D*`.

---

## 6. Phase E — Freeze validation-only selection

**Objective:** Create a tamper-evident record that selects `D*` before any test payload becomes available.

### E1. Preconditions

- [x] Four finite final full-validation values exist.
- [x] All final checkpoint hashes are frozen.
- [x] Full validation logs/components are archived.
- [x] Required baseline checks are complete and archived.
- [x] Eligibility matrix is complete or any ineligible run is explicitly classified. All four eligible.
- [x] Test payload remains unavailable to the selection job/operator. True at 07:56:24Z.
- [x] No test BPB has been calculated, displayed, or used. True at 07:56:24Z (`test_read_count=0`).

### E2. Selection algorithm

Implemented exactly:

1. Read the four final `val_bpb_full` values from the sealed validation artifacts.
2. Sort ascending because lower BPB is better. Order: 20 (1.172248), 8 (1.179135), 12 (1.180824), 16 (1.195546).
3. Select the exact numerical minimum as `D*` → **20**.
4. Compute all pairwise gaps and flag any gap `<0.01 BPB`. d20−d8 = 0.006887; d20−d12 = 0.008576.
5. If `D*` is within `<0.01 BPB` of another eligible depth, retain the exact minimum solely to identify the one test candidate, but state that the apparent order is practically indistinguishable at one-seed resolution. **Done.**
6. Do not consult test BPB, training loss, mid-run minimum, sample output, runtime, VRAM, cost, or subjective preference.
7. Do not reopen the model grid or schedule a new run before the one-test procedure.

### E3. Immutable `selection_record.json`

Written at `manifests/selection_record.json`. File SHA-256 `{H['sel']}`. Inner `record_sha256` hashes the body without that field. See honesty note 1.

### E4. Selection sign-off

| Sign-off assertion | Yes / No | Evidence / initials / UTC |
|---|---|---|
| Selection used final full validation only. | Yes | `{H['sum']}` / PP / 2026-08-16T07:56:24Z |
| Selection did not use mid-run minima. | Yes | d12 step-200 min unused |
| Selection did not use short card-loop BPB. | Yes | Card-eval labeled diagnostic |
| Selection did not use test data or test BPB. | Yes | `test_read_count=0` at freeze |
| Selection did not use sample quality, cost, runtime, or VRAM. | Yes | Samples written later, secondary |
| Final checkpoint fixed-budget rule was applied consistently to all depths. | Yes | All `model_000294.pt` |
| `selection_record.json` is hashed and archived. | Yes | `{H['sel']}` |
| Ledger records `validation_selection_frozen`. | Yes | Event at 07:56:24Z; recorded 09:13:00Z |

---

## 7. Phase F — One and only one isolated test evaluation

**Objective:** Obtain the registered secondary `test_bpb` without allowing test information to alter model selection.

### F1. Test-release authorization

Do not mount/copy/decrypt/open the test payload until every box below is checked. **These were true at 07:56:24Z** (sealed summary). Named `selection_record.json` reconstructs that freeze.

- [x] `selection_record.json` exists, is hashed, and identifies one selected final checkpoint. Sealed summary then named file `{H['sel']}`; `D*=20`; ckpt `{CK[20]}`.
- [x] All validation values, baseline checks, and eligibility results are archived.
- [x] Selection record proves `test_bpb_before_selection=false`.
- [x] Confirmatory test-access count is zero. True before 07:58:35Z.
- [x] The test evaluator job is separate from all training and validation jobs. `--phase test`.
- [x] The evaluator has read-only access to the selected checkpoint and frozen tokenizer.
- [x] The test job sees no alternative checkpoints or depth-ranking controls.
- [x] Test manifest hash is known and recorded. `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf`.
- [x] The evaluator command is reviewed against the same BPB/packing/`T=2048` semantics as validation.

### F2. Test-access log entry before opening test text

| Field | Required value |
|---|---|
| Event type | `confirmatory_test_evaluation` |
| UTC time | 2026-08-16T07:58:35Z |
| Operator/job ID | Paul Pajo / `gate_j_full_bpb.py --phase test` on `68bei7d3vx4krc` |
| Selected depth | `D*=20` from sealed selection |
| Selected checkpoint SHA-256 | `{CK[20]}` |
| Selection record SHA-256 | `{H['sel']}` (named file); sealed summary `{H['sum']}` |
| Test manifest SHA-256 | `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf` |
| Test access count before event | `0` |
| Intended access count after event | `1` |
| Evaluator command hash | `{H['eval']}` |
| Host/environment fingerprint hash | `{H['pre']}` |
| Reason | Registered secondary `test_bpb` only; not model selection. |

Also in `manifests/test_access_log.json` SHA `{H['tal']}`.

### F3. Test evaluation execution checks

- [x] Test evaluator uses the selected final checkpoint only.
- [x] Test evaluator uses frozen `token_bytes.pt` and tokenizer only.
- [x] Test evaluator uses same BPB formula, special-token exclusion, context/packing behavior, and canonical text policy as validation.
- [x] Test evaluator produces finite BPB components and finite `test_bpb`. `test_bpb=1.164768`; nats 4,383,024.5; bytes 5,428,863; tokens 1,198,803; excluded 13,613.
- [x] No other depth is scored on test.
- [x] No further model training, checkpoint selection, tokenization, or hyperparameter choice occurs after test evaluation. Extra seeds / D_1x / samples / bootstrap are val-only secondary.
- [x] Test result is written once to a unique immutable result path. `p1-fixed-d20-3x_test_bpb.json` SHA `{H['test']}`.
- [x] Result log/output/checkpoint/tokenizer/test-manifest/selection-record hashes are archived together.
- [x] Test directory is unmounted/restricted immediately afterward. Isolated path; not in active train dir. Pod copy deletion was Auto-review blocked; Mac test jsonl remains write-protected and out of public zips.
- [x] Ledger records confirmatory test-access count = `1` and `test_bpb_computed=true`.

### F4. Test technical failure rule

**Not invoked.** The one test job succeeded. No retry is permitted for the primary claim.

- [x] Preserve logs, command, selection record, and exact failure point. N/A.
- [x] Determine whether test bytes were opened or only the job initialization failed. N/A — full success.
- [x] Add a truthful test-access event; do not erase a partial read. One event recorded.
- [x] Do not silently rerun. No rerun.
- [x] Before any retry, create a dated incident record… N/A.
- [x] If a valid test BPB was already produced, no repeat test evaluation is permitted for the primary claim. **Acknowledged. No second confirmatory test read.**

---

## 8. Phase G — Final eligibility and deviation audit

**Objective:** Determine which runs, if any, are eligible for the confirmatory table; describe every departure rather than conceal it.

### G1. Registered exclusion matrix

| Condition from AsPredicted Q6 | d8 | d12 | d16 | d20 | Evidence path/hash | Close-out status |
|---|---|---|---|---|---|---|
| Finite final BPB | [x] | [x] | [x] | [x] | `{H['sum']}` | pass |
| WikiText-TL-39 only in train directory | [x] | [x] | [x] | [x] | preflight `{H['pre']}` | pass |
| No test file/path in train directory | [x] | [x] | [x] | [x] | preflight + test log | pass |
| Val/test absent from tokenizer training | [x] | [x] | [x] | [x] | tokenizer manifest `{H['tok']}` | pass |
| Positive ratio; not `-1` | [x] | [x] | [x] | [x] | 0.457834 / 0.174413 / 0.081756 / 0.044129 | pass |
| No silent depth change after OOM | [x] | [x] | [x] | [x] | run cards; Mac d20 MPS OOM did not shrink T | pass |
| No silent `T` change after OOM | [x] | [x] | [x] | [x] | `T=2048` all confirmatory | pass |
| Final checkpoint at fixed budget | [x] | [x] | [x] | [x] | step 294 / `D_actual=19267584` | pass |
| `D_actual` matches manifest | [x] | [x] | [x] | [x] | budget `{H['bud']}` | pass |
| Final checkpoint/hash intact | [x] | [x] | [x] | [x] | `{H['ckptman']}` | pass |

### G2. Required deviation/incident inventory

| Event | Category | Does it alter primary claim? | Disclosure required? | Artifact |
|---|---|---|---|---|
| Original 2019 split unavailable; reconstructed article split used | Predeclared/clarified fallback | No; deterministic audit passed | Yes | `split_manifest.json` `{H['split']}` |
| Final fixed-budget checkpoint interpretation | Pre-start operational clarification | No | Yes | clarifications `{H['clar']}` |
| Mac MPS smoke/dry-runs | Infrastructure-only, nonconfirmatory | No | Yes | Mac MPS deviation cards |
| Gate H Pod/host | Official environment certificate | No | Yes | `gpu_host_for_H` `p7e5zk3njnglgy` |
| W&B prompt caused pre-checkpoint d8 failure; restart occurred with W&B offline | Operational incident before valid checkpoint | No; same frozen command | Yes | d8 train.log + Gate I card |
| New Gate I Pod/host | Permitted infrastructure adaptation | No | Yes | `68bei7d3vx4krc` host card |
| d20 microbatch memory fit | Permitted hardware adaptation; `B` and `D_actual` fixed; `device-batch-size=8` | No | Yes | Gate I preflight |
| 80 GB `/workspace` volume | Infrastructure | No | Yes | `2026-08-16-gate-i-pod-volume-80gb.md` |
| API key pasted in chat; rotation deferred then marked due | Credential hygiene | No | Yes | rotation deviation cards |
| Named `selection_record.json` written after test | Documentation timing | No; sealed summary predates test | Yes | this checklist honesty note 1 |
| Extra seeds, D_1x, gzip, samples, bootstrap | Secondary / exploratory | No; not used for `D*` | Yes | RESULTS §5 |
| Native-speaker ratings unavailable | Missing optional qualitative scores | No | Yes | RESULTS §7; scores not invented |
| Pod still running after archive | Billing / ops | No | Yes | dashboard |

### G3. Final eligibility verdict per depth

- [x] d8: **eligible** — finite `val_bpb_full`, baselines pass, frozen command, hash intact.
- [x] d12: **eligible** — same.
- [x] d16: **eligible** — same.
- [x] d20: **eligible** — same.
- [x] If any depth is excluded, do not replace it, omit it, or reinterpret the grid silently. N/A.
- [x] If all four are eligible, state this explicitly. **All four confirmatory depths are eligible.**

---

## 9. Phase H — Analysis, interpretation, and limits

**Objective:** State exactly what the completed study supports and what it does not.

### H1. Required confirmatory result table

| Depth | `P_total` | `P_scaling` | Ratio | `D_actual` | Full train BPB | Full `val_bpb_full` | Train–val gap | Untrained check | Byte-unigram check | Eligible? | Final rank / practical tie note |
|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| 8 | 125,829,354 | 41,943,232 | 0.457834 | 19,267,584 | 0.836702 | 1.179135 | 0.342432 | pass (3.289109) | pass (4.453225) | eligible | 2nd; gap to D* 0.006887; practically indistinguishable |
| 12 | 286,261,730 | 110,100,912 | 0.174413 | 19,267,584 | 0.528818 | 1.180824 | 0.652006 | pass (3.289358) | pass (4.453225) | eligible | 3rd; gap to D* 0.008576; practically indistinguishable |
| 16 | 536,871,738 | 234,881,792 | 0.081756 | 19,267,584 | 0.458045 | 1.195546 | 0.737501 | pass (3.289354) | pass (4.453225) | eligible | 4th; highest val BPB |
| 20 | 896,533,746 | 435,160,240 | 0.044129 | 19,267,584 | 0.672393 | **1.172248** | 0.499855 | pass (3.289106) | pass (4.453225) | eligible | **D*** exact min; not a one-seed ranking vs d8 |

CSV SHA `{H['csv']}`. Components SHA `{H['comp']}`.

### H2. Required selected-model table

| Field | Value |
|---|---|
| Validation-selected depth `D*` | 20 |
| Selected final checkpoint SHA-256 | `{CK[20]}` |
| `D*` full `val_bpb_full` | 1.172247965803217 |
| Nearest competitor gap | 0.006886777915559916 vs d8 |
| Gap `<0.01`? | Yes |
| Practical interpretation at one seed | d20 and d8 are practically indistinguishable; do not claim a depth ranking |
| Selected `test_bpb` | 1.164768333672231 |
| Test evaluation date/host | 2026-08-16T07:59:01Z / Runpod A40 `68bei7d3vx4krc` |
| Test access count | `1` |

### H3. Permitted primary claims

> Under the frozen WikiText-TL-39-derived corpus, reconstructed split, train-only 32k tokenizer, nanochat implementation, `T=2048`, fixed `D_actual`, and one-seed design, final held-out validation BPB showed a practically indistinguishable pattern across the registered depth grid (numerical minimum at depth 20; margin to depth 8 is 0.006887 BPB). The validation-selected final checkpoint was depth 20, and its one-time held-out test BPB was 1.164768.

### H4. Prohibited or unsupported claims

- [x] Do not say “deeper is always better.” **Not said.**
- [x] Do not say “this is the best Tagalog LLM.” **Not said.**
- [x] Do not claim chat, instruction following, translation, NLI, classification, reasoning, safety, or downstream utility. **Not claimed.**
- [x] Do not claim the finding generalizes to all Tagalog/Filipino text, all corpora, all tokenizers, all training budgets, or all model families. **Not claimed.**
- [x] Do not claim causal superiority of depth if a practical tie remains below 0.01 BPB at one seed. **Not claimed.**
- [x] Do not present short card-loop values or mid-run minima as the registered primary outcome. **Not presented as primary.**
- [x] Do not use the one selected test BPB to rank untested depths. **Not used.**

### H5. Required limitations paragraph

Include all applicable limitations:

- [x] One seed produces point estimates, not a stable population distribution.
- [x] The corpus is public and limited to the frozen WikiText-TL-39-derived material.
- [x] Original historical splits were unavailable; a documented reconstructed split was used.
- [x] Near-duplicate structure and corpus-source provenance may limit broader generalization.
- [x] BPB is a base-language-model likelihood measure, not a user-task or assistant measure.
- [x] The study excludes SFT/chat, CORE, downstream classification, NLI, other corpora, d24, and `D_10x` from the confirmatory result.
- [x] GPU/resource differences are reported as operational context, not evidence of model quality.

See RESULTS §6.

---

## 10. Phase I — Reporting Q1–Q8 against the filed registration

### I1. Q1: Prior data

- [x] Restate accurately that the public corpus existed before registration.
- [x] State that no confirmatory trained final-model `val_bpb_full` or selected `test_bpb` had been computed at filing.
- [x] Cite registration timestamp, gate ledger, and pre-start clarification timestamp.
- [x] Do not imply no data whatsoever existed; explain the distinction between existing corpus data and unobserved confirmatory outcomes.

### I2. Q2: Main question

- [x] Restate the depth-8-to-20 equal-exposure BPB question verbatim or faithfully.
- [x] State whether final validation supports decline, flattening, reversal, or widening train–validation gap. Numerical min at 20; val rose 8→16 then d20 lowest by sub-0.01 vs d8; gap widened 8→16. Falsification (“deeper always improves with no gap increase”) did not occur.
- [x] Do not transform it into a question about chat, downstream tasks, English, catastrophic forgetting, or general AI capability.

### I3. Q3: Dependent variables

- [x] Report primary `val_bpb_full` for each final candidate.
- [x] Report secondary selected `test_bpb` once.
- [x] State BPB formula/byte denominator/special-token treatment/packing/context behavior.
- [x] State that full validation—not loop-slice evaluation—was used.
- [x] Disclose the final-checkpoint fixed-budget interpretation and its pre-start date.

### I4. Q4: Conditions

- [x] Show four depths only: 8, 12, 16, 20.
- [x] Show common corpus package, train-only tokenizer, split, `T=2048`, and fixed token exposure.
- [x] Show actual `D_actual` calculation per depth. 294 × 65,536 = 19,267,584 for all four.
- [x] State no native-ratio-12 run served as an equal-exposure primary comparison.

### I5. Q5: Analyses

- [x] Compare full final validation BPB across the four depths.
- [x] Report train–validation gap.
- [x] Report same-depth untrained and byte-unigram checks.
- [x] Define `D*` from validation only.
- [x] Report selected test BPB and state it did not choose `D*`.
- [x] Apply one-seed `<0.01 BPB` practical-interpretation rule.
- [x] State no CORE in confirmatory comparison.

### I6. Q6: Outliers/exclusions

- [x] Report unit drop count/percentage and whether it stayed below 5%. Registered drops 0 / 1,524,071 (0%).
- [x] Report split exact-hash disjointness. Intersections 0.
- [x] Report all run eligibility checks and any exclusion. None excluded.
- [x] State whether NaN/Inf occurred. No.
- [x] State whether train directory/test/tokenizer/ratio/depth/T exclusions were triggered. No.
- [x] Do not hide a poor-BPB depth merely because it looks unfavorable. d16 (highest val) is reported.

### I7. Q7: Sample/token determination

- [x] Report actual row/document/split counts and split method. 120,971 articles; 53,718 unique texts; 37,602 / 8,058 / 8,058 units.
- [x] Report `T_train`, `D_3x`, total batch, iterations, `D_actual`, token-count definition, and context length.
- [x] Report whether original 2019 splits were found; if not, name reconstructed fallback. Not found; `reconstructed_article_70_15_15`.
- [x] Report extra seeds/pilots only as specified secondary/exploratory analyses, with timing relative to test access. Extra seeds after test; val only; test not reread.

### I8. Q8: Secondary/exploratory work

- [x] List all executed exploratory/secondary analyses separately. Extra seeds d8/d12; D_1x pilots; gzip -9 val 2.739 bpb; D* samples; document-level bootstrap.
- [x] List prespecified secondary items not executed. Native-speaker 1–5 ratings (no rater). `python -m nanochat.report` (not in pin). SEA-HELM / CF / SFT not confirmatory.
- [x] List any unplanned analyses separately, with date and rationale. W&B-offline restart (ops). Named selection-record backfill (docs).
- [x] State explicitly that no exploratory outcome changed `D*` selection or primary interpretation.

---

## 11. Phase J — Reproducibility archive and release package

**Objective:** Ensure a skeptical reviewer can reconstruct what was done without trusting an oral account.

### J1. Required archive tree

Written at `transfer/p1.1-closeout-bundle-20260816/` (this study’s `project1_closeout_bundle/`). Weights omitted (hash pointers). Test text omitted.

```text
transfer/p1.1-closeout-bundle-20260816/
  00_registration/ … 08_integrity/MANIFEST.sha256
```

### J2. Archive integrity checks

- [x] Generate a recursive SHA-256 manifest after all output paths are final. `08_integrity/MANIFEST.sha256` SHA `{H['arch']}`.
- [x] Verify the manifest from a fresh environment or second storage location. Verified by `scripts/p1/build_aspredicted_closeout.py` immediately after write (local second pass).
- [x] Archive raw logs alongside polished tables/figures. Train logs + val JSON + RESULTS.
- [x] Keep protected test text out of any public archive unless license and access policy explicitly permit redistribution. **Omitted.**
- [x] Preserve test manifest/hash, evaluator command, aggregate components, and test-access log even if test text stays private.
- [x] Export the full bundle off the ephemeral Pod before stopping it. Mac archive complete. **Pod stop still outstanding.**
- [x] Record archive URI/location, access policy, retention commitment, and cryptographic manifest hash. `08_integrity/archive_metadata.json`.

Also: ResearchBox pack `transfer/p1.1-researchbox-8735-20260816/` (no passcode). Operator must upload.

---

## 12. Phase K — Final public communication and peer-review readiness

### K1. Pre-publication quality check

- [x] A reviewer who has not seen the live terminal can identify the primary outcome without reading diagnostic metrics. RESULTS §2 table.
- [x] A reviewer can reconstruct the selection path from validation artifacts only. `val_baselines_summary.json` + `selection_record.json`.
- [x] A reviewer can confirm the test was accessed once after selection. `test_access_log.json`; summary ended 07:56:24Z; test 07:58:35Z.
- [x] Every figure/table distinguishes confirmatory, secondary, diagnostic, and exploratory evidence. RESULTS statement classes.
- [x] Every model label carries depth, checkpoint rule, tokenizer, data/split label, token budget, and seed context.
- [x] Every limitation is stated before implications or future work.
- [x] No dashboard screenshot is the sole evidence for a result; raw machine-readable artifacts exist.

### K2. Suggested result announcement wording

> The preregistered fixed-budget depth study has completed its four final full-validation evaluations. The primary result compares final held-out Tagalog BPB for d8, d12, d16, and d20 under the frozen WikiText-TL-39-derived corpus, reconstructed split, train-only tokenizer, `T=2048`, and common actual token exposure. The validation-selected final checkpoint was evaluated once on the protected test split. Results are reported with one-seed practical-equivalence caution, full provenance, baseline checks, and a deviation/limitations record.

### K3. Statements to avoid in public updates

- [x] “We proved dX is the best model.” **Avoided.**
- [x] “The test confirms our choice” if the test was not used for selection. **Avoided.**
- [x] “The model understands Tagalog” without a task-specific evaluation framework. **Avoided.**
- [x] “This beats all existing Filipino models.” **Avoided.**
- [x] “The intermediate curve shows dY really won.” **Avoided.**
- [x] “The GPU was faster, therefore the model is better.” **Avoided.**

---

## 13. Final close-out declaration template

Complete this only after the full validation, selection, one test evaluation, eligibility audit, and archive verification are finished.

> **AsPredicted #306780 close-out declaration**
>
> I confirm that the preregistered confirmatory comparison used the filed four-depth grid (d8, d12, d16, d20), the frozen WikiText-TL-39-derived corpus package, the documented reconstructed split, the train-only 32,768 BPE tokenizer, `T=2048`, and the fixed token-budget configuration recorded in the budget manifest. The four primary values were full held-out final `val_bpb_full` evaluations of the final fixed-budget checkpoints. The selected depth `D*` was the exact minimum of those validation values, according to the dated pre-Gate-A final-checkpoint operational clarification. The protected test split was not used for model selection and was evaluated **once** only for the validation-selected final checkpoint. The required untrained same-depth and train-fitted byte-unigram validation baselines were **completed**. All exclusions, incidents, deviations, nonconfirmatory diagnostics, and limitations are listed in the accompanying ledger, deviation inventory, and archive. No post-outcome change was presented as part of the original preregistration.
>
> **Signed by:** Paul Pajo  
> **UTC timestamp:** 2026-08-16T09:13:00Z  
> **Selection-record SHA-256:** `{H['sel']}`  
> **Test-result artifact SHA-256:** `{H['test']}`  
> **Archive manifest SHA-256:** `{H['arch']}`

---

## 14. Ultimate “do not proceed” checklist

Historical gate at **2026-08-16T07:56:24Z**, immediately before the one permitted test read. All were true then. Test has since been read **once**. Do not access test data again.

- [x] The four final full validation evaluations are complete.
- [x] The values used are `val_bpb_full`, not card-loop values or mid-run minima.
- [x] The exact final fixed-budget candidate rule has been applied.
- [x] Required validation baselines are complete.
- [x] All run eligibility checks are complete.
- [x] `selection_record.json` is written and hashed. (Sealed summary at freeze; named file reconstructed later.)
- [x] Test-access count is exactly zero. **Was true at freeze. Now 1. Do not increment.**
- [x] The test job is isolated and sees one candidate only.
- [x] The selected checkpoint is hash-locked.
- [x] The test command/evaluator/test-manifest hash are recorded.
- [x] A test technical-failure policy has been read and acknowledged.

If **any** box is unchecked: **do not access test data.**

## Reference

[1]: https://aspredicted.org/6r6v4v.pdf "AsPredicted #306780: NANOCHAT-FILIPINO P1.1 — WikiText-TL-39 fixed-budget depth vs held-out BPB"
"""

def _fill(text: str) -> str:
    repl = {
        "{H['pdf']}": H["pdf"],
        "{H['clar']}": H["clar"],
        "{H['ledger']}": H["ledger"],
        "{H['sel']}": H["sel"],
        "{H['test']}": H["test"],
        "{H['arch']}": H["arch"],
        "{H['sum']}": H["sum"],
        "{H['eval']}": H["eval"],
        "{H['uni']}": H["uni"],
        "{H['ckptman']}": H["ckptman"],
        "{H['pre']}": H["pre"],
        "{H['src']}": H["src"],
        "{H['split']}": H["split"],
        "{H['shard']}": H["shard"],
        "{H['tok']}": H["tok"],
        "{H['bud']}": H["bud"],
        "{H['tman']}": H["tman"],
        "{H['tal']}": H["tal"],
        "{H['hook']}": H["hook"],
        "{H['res']}": H["res"],
        "{H['csv']}": H["csv"],
        "{H['comp']}": H["comp"],
        "{CK[8]}": CK[8],
        "{CK[12]}": CK[12],
        "{CK[16]}": CK[16],
        "{CK[20]}": CK[20],
        "{META[8]}": META[8],
        "{META[12]}": META[12],
        "{META[16]}": META[16],
        "{META[20]}": META[20],
        "{LOG[8]}": LOG[8],
        "{LOG[12]}": LOG[12],
        "{LOG[16]}": LOG[16],
        "{LOG[20]}": LOG[20],
        "{VAL[8]}": VAL[8],
        "{VAL[12]}": VAL[12],
        "{VAL[16]}": VAL[16],
        "{VAL[20]}": VAL[20],
        "{RC[8]}": RC[8],
        "{RC[12]}": RC[12],
        "{RC[16]}": RC[16],
        "{RC[20]}": RC[20],
        "{RUN}": "p1-20260816T025911Z-0067a57",
        "{{8,12,16,20}}": "{8,12,16,20}",
        "{{RUN}}": "p1-20260816T025911Z-0067a57",
    }
    for k, v in repl.items():
        text = text.replace(k, v)
    return text


TEXT = _fill(TEXT)

DESTS = [
    Path("/Users/paulpajo/Downloads/Super-Exhaustive Close-Out Checklist for AsPredicted #306780.md"),
    ROOT / "docs" / "run-cards" / "CLOSEOUT-aspredicted-306780.md",
    ROOT / "transfer" / "p1.1-closeout-bundle-20260816" / "07_results" / "reporting_checklist.md",
]


def main() -> None:
    for dest in DESTS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(TEXT, encoding="utf-8")
        print(dest, len(TEXT))


if __name__ == "__main__":
    main()
