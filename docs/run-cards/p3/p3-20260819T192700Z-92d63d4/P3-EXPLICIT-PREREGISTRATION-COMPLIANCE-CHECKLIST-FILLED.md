# P3 Explicit Preregistration Compliance Checklist — FILLED AUDIT

**Source checklist:** `/Users/paulpajo/Downloads/P3 Explicit Preregistration Compliance Checklist.md`  
**Audit date:** 2026-08-20 (post–Gate X)  
**Run:** `p3-20260819T192700Z-92d63d4` · AsPredicted **#307342** · ResearchBox **#8834**  
**LOCK status:** `gate_x_unblinded` (`docs/papers/p3-reverse/LOCK.json`)

### Legend (this filled copy)

| Marker | Meaning |
|---|---|
| `[x]` | Verified against safe receipts / Gate X preflight / released seal |
| `[ ]` | Still open — paper, ResearchBox deposit packaging, Hub, or public release wording |
| `[!]` | Stop / incident — documented and dispositioned (not blocking confirmatory path) |

### Executive verdict

**Execution path (E-01–E-95 + X-01–X-22 where applicable): CLOSED and compliant.**  
**Public report closure (paper/RB packaging/Hub/GitHub `results/p3`): NOT yet closed** — those remain `[ ]`.

Gate X preflight (`gate-x-preflight.json`, 2026-08-20T08:54:36Z): **10/10 PASS**, `ready_for_unblinding=true`.  
Formal unblinding (`P3_UNBLINDING_EVENT.json`, 2026-08-20T08:56:47Z): **PASS**.  
Released: `data/cache/p3-20260819T192700Z-92d63d4/released/` (11 files).

**Registered directional outcomes (from seal; one seed; observed/not observed):**

| Contrast | Filed rule | Released value | Call |
|---|---|---|---|
| `C_tl` | ≥ 0.01 | **1.023484…** | **observed** |
| `G_en` | ≤ −0.01 | **−1.697955…** | **observed** |
| `C_tl(B3)` | report only | −0.275035… | reported; B3 **not mitigation** |
| `G_en(B3)` | report only | −1.683684… | reported; B3 **not mitigation** |

---

## §2 Filing identity (E-01–E-07)

| ID | Status | Evidence |
|---|---|---|
| E-01 | `[x]` | PDF `docs/run-cards/AsPredicted-307342.pdf`; SHA `6cfad038…50b1` matches LOCK |
| E-02 | `[x]` | Filed 2026-08-19 12:27 PT; anonymous; LOCK records title/pages |
| E-03 | `[x]` filing · `[ ]` release materials | LOCK `designed_after_p2_gate_u=true`; **paper/model card still need explicit post-P2 sentence** |
| E-04 | `[x]` Q2 · `[ ]` paper wording | Protocol/LOCK: not confirmation of P2; **paper not yet written** |
| E-05 | `[x]` | LOCK `does_not_amend_306780/306935` |
| E-06 | `[x]` | Gates A/F/I/Q: fresh P3 weights + P3 tok; pin `92d63d4…`; no P1.1/P2 parent |
| E-07 | `[x]` | Protocol SHA recomputed: `899ba83f0b36f2b4bf4c16b3c675e58788d7763cb439f8a8c3a3c061bda2b986` **match** |

---

## §3 RQ / constructs (E-08–E-21)

| ID | Status | Evidence |
|---|---|---|
| E-08 | `[x]` calc · `[ ]` paper prose | Seal answers the filed directional comparison |
| E-09 | `[x]` | Seal `C_tl` from B2−B1 TL cells |
| E-10 | `[x]` | `C_tl >= 0.01` → **observed** |
| E-11 | `[x]` | Seal `G_en` from B2−B1 EN cells |
| E-12 | `[x]` | `G_en <= −0.01` → **observed** |
| E-13 | `[x]` design · `[ ]` release language | Seal `not_mitigation=true`; Gate E 50/50 docs |
| E-14 | `[x]` | Seal `C_tl_B3`, `G_en_B3` present |
| E-15 | `[x]` safe · `[ ]` paper table | Gate E: doc 50/50; byte EN≈0.961 / TL≈0.039; `K=28472`; mix SHA `b6ae432b…` |
| E-16 | `[x]` | P0-T `03:40:16Z` ≺ Gate S `07:38:32Z` |
| E-17 | `[x]` | P0-T PASS both depths both floors (released eligibility) |
| E-18 | `[x]` | PASS path → B1/B2/B3 ran |
| E-19 | `[x]` | B0 parent only; `forbidden_parents.py`; R/S/T parent SHA = Gate I d20 |
| E-20 | `[x]` | Gate F tok SHA `04436b85…` used throughout |
| E-21 | `[x]` | `core_metric_every=-1`; no chat/SFT in primary path |

---

## §4 DVs / measurement (E-22–E-36)

| ID | Status | Evidence |
|---|---|---|
| E-22 | `[x]` | Gate D TL val SHA `4d51644b…` |
| E-23 | `[x]` | Gate D EN val SHA `874dec29…` |
| E-24 | `[x]` | Same P3 TL BPE on all arms |
| E-25 | `[x]` | `scripts/p3/evaluate_bpb.py` official nats/(ln2×bytes) |
| E-26 | `[x]` | Released cells: packing BOS-bestfit; `sequence_len=2048`; full val |
| E-27 | `[x]` | Train: `eval_every=-1`; no in-loop selection |
| E-28 | `[x]` | Six child cells in seal + released files |
| E-29 | `[x]` | Seal: `b0_en_descriptive`, `b0_en_excluded_from_contrasts` |
| E-30 | `[x]` | B0 TL from P0-T; no duplicate confirmatory B0 TL at U |
| E-31 | `[x]` | Gate V: one B2-only event, two components |
| E-32 | `[x]` | EN test SHA `2bccabc0…` (Gate D / V path) |
| E-33 | `[x]` | TL test SHA `3bd19345…` |
| E-34 | `[x]` | Gate C/E: tests absent from train/tok dirs |
| E-35 | `[x]` | Contrasts from U seal only; V secondary |
| E-36 | `[x]` · `[ ]` paper | P3 V values released; **paper must not reuse P1.1 1.164768 / P2 tests** |

---

## §5 Conditions / apparatus (E-37–E-54)

| ID | Status | Evidence |
|---|---|---|
| E-37 | `[x]` | No human subjects |
| E-38 | `[x]` | Gate A + live `vendor/nanochat` HEAD = pin |
| E-39 | `[x]` | `tok_train` → `base_train` / `continue_from_frozen` → `evaluate_bpb` |
| E-40 | `[x]` | Gate G + all train/eval: T=2048 |
| E-41 | `[x]` | `core_metric_every=-1` |
| E-42 | `[x]` | TL train SHA `2b0474c5…`; fresh TL0 tags |
| E-43 | `[x]` | Gate F fresh `tok_train`; vocab 32768 |
| E-44 | `[x]` | Gate I d8+d20; P0-T both depths |
| E-45 | `[x]` | Gate G: `T_tl_train=6401013`, `N_TL0=294` |
| E-46 | `[x]` | Gate Q PASS; B0 SHA `ae621be2…` |
| E-47 | `[x]` | Gate R: Tagalog stream only |
| E-48 | `[x]` + `[!]` incident | Official S PASS on `en-clean`; see Gate S note |
| E-49 | `[x]` | Gate E before TL0 val; seed 42; K=28472; SHA-sort+interleave |
| E-50 | `[x]` | R/S/T: step 294; `D_phase2=19267584` |
| E-51 | `[x]` | Gate G `fresh_muon_adamw=true`; continue_from_frozen |
| E-52 | `[x]` | `load_optimizer=False` in continue_from_frozen |
| E-53 | `[x]` | Gate G `lr_peak_rule=0.3 * TL0`; child LRs 0.09/0.0024/0.006/0.15 |
| E-54 | `[x]` | warmup=14 < N=294 |

**[!]** Gate S: early attempts failed (missing/corrupt EN data; zero official steps). Disposition (Gate X preflight #8): *partial attempt quarantined; official clean restart from B0* with `en-clean`, 294 steps, `train_exit_code=0`. Documented in `gate-x-preflight.json`.

---

## §6 Analysis plan (E-55–E-65)

| ID | Status | Evidence |
|---|---|---|
| E-55 | `[x]` | P0-T before S (timestamps) |
| E-56 | `[x]` | Operator stdout was `P0-T: PASS` only before X |
| E-57 | `[x]` | PASS → children ran |
| E-58 | `[x]` | Seal uses B1/B2 cells |
| E-59 | `[x]` | B0 EN excluded from contrasts |
| E-60 | `[x]` | `not_mitigation=true` |
| E-61 | `[x]` · `[ ]` paper | Point estimates only in seal; **paper must not add CI/p** |
| E-62 | `[x]` | Cutoffs applied as filed; no |Δ| ranking |
| E-63 | `[x]` | Frozen 294 / 0.01 / 50/50 retained |
| E-64 | `[ ]` | **Paper must state mechanical carry-forward** |
| E-65 | `[x]` · `[ ]` paper | No exploratory arms in confirmatory run; **paper must keep them exploratory** |

---

## §7 Cleaning / prohibitions (E-66–E-82)

| ID | Status | Evidence |
|---|---|---|
| E-66–E-70 | `[x]` | Gates B–E split/hygiene pass; filed hashes; no rebuild |
| E-71 | `[x]` | Accept scripts required `finite`; health=pass |
| E-72 | `[x]` | Gate C hygiene; no ClimbMix |
| E-73 | `[x]` | Train-only dirs; tests unmounted |
| E-74 | `[x]` | Single Gate F tok; no post-outcome retok |
| E-75 | `[x]` | Explicit `--num-iterations=294` (no ratio=-1) |
| E-76 | `[x]` | Pin `base_train` / evaluate_bpb only |
| E-77 | `[x]` · `[ ]` GitHub layout | Separate `scripts/p3`, run-cards/p3; **`results/p3/` not yet published** |
| E-78 | `[x]` | B0-only parents |
| E-79 | `[x]` | `flash_attention.py` diff vs pin = empty |
| E-80 | `[x]` | S incident recorded; no silent erase |
| E-81 | `[x]` | B1/B2/B3 all released together |
| E-82 | `[x]` | Smoke d4 not in confirmatory table |

---

## §8 Sample size / test-touch (E-83–E-90)

| ID | Status | Evidence |
|---|---|---|
| E-83–E-86 | `[x]` | Gate D/G/I hashes & budgets |
| E-87 | `[x]` | R/S/T: N=294, D=19,267,584, d20 |
| E-88 | `[x]` | U seal `test_access=0` |
| E-89 | `[x]` | V: 1 touch, 2 components → `test_access=1` |
| E-90 | `[x]` | test_access_log: only `p3-b2-en-d20` |

---

## §9 Lockbox / release (E-91–E-95)

| ID | Status | Evidence |
|---|---|---|
| E-91 | `[x]` | Filed Q8 contemporaneous |
| E-92 | `[x]` | U then V then X; scalars released only at X |
| E-93 | `[x]` | Lockbox + Gate 0 tests; `p3_outcome_access_count` 0→1 at X |
| E-94 | `[x]` | Tests outside train dirs; `raw_test_still_restricted=true` |
| E-95 | `[x]` | Protocol SHA + pin preserved in LOCK |

---

## §11 Pre-Gate-X audit (X-01–X-15) — ALL DONE

| ID | Status | Evidence |
|---|---|---|
| X-01 | `[x]` | PDF + protocol SHA match |
| X-02 | `[x]` | Pin match; FA unpatched |
| X-03 | `[x]` | Q–W all PASS |
| X-04 | `[x]` | Identical B0 parent on R/S/T |
| X-05 | `[x]` | Gate F tok identity |
| X-06 | `[x]` | d20, N=294, fresh opt |
| X-07 | `[x]` | S disposition PASS in preflight |
| X-08 | `[x]` | Filed split/holdout hashes |
| X-09 | `[x]` | U `07:57:24Z` < V `07:58:38Z` |
| X-10 | `[x]` | 0 at U → 1 after V |
| X-11 | `[x]` | B2 only |
| X-12 | `[x]` | Was 0 immediately before X |
| X-13 | `[x]` | Preflight safe-log scan clean |
| X-14 | `[x]` | Released + manifest SHA recorded |
| X-15 | `[x]` | No further confirmatory train/eval at X |

---

## §12 Post-unblinding (X-16–X-27)

| ID | Status | Evidence / remaining |
|---|---|---|
| X-16 | `[x]` | `P3_UNBLINDING_EVENT.json` |
| X-17 | `[x]` | Bundle opened once together under `released/` |
| X-18 | `[x]` | LOCK `p3_outcome_access_count=1` |
| X-19 | `[x]` | Six child cells + B0 EN descriptive released |
| X-20 | `[x]` | `C_tl`, `G_en` in seal with filed signs |
| X-21 | `[x]` | B3 contrasts + Gate E shares available |
| X-22 | `[x]` | `released/gate-v-test.json` B2-only secondary |
| X-23 | `[x]` · `[ ]` paper | Point estimates ready; **paper must keep one-seed boundary** |
| X-24 | `[x]` | Both primary predictions **observed** (no rescue needed) |
| X-25 | `[x]` | Event: `no_additional_validation_or_test_eval=true` |
| X-26 | `[ ]` | **Paper, ResearchBox deposit pack, Hub (optional), GitHub `results/p3` still open** |
| X-27 | `[ ]` | **Every public narrative must disclose post-P2 design timing** |

---

## Remaining open checklist (must still be done)

1. **Paper** from frozen seal — observed/not observed grammar; post-P2 disclosure; B3 not mitigation; no CI/p; secondary tests labeled.  
2. **ResearchBox #8834** deposit of non-sensitive artifacts (no raw test text).  
3. **GitHub** package `results/p3/` + docs (separate from P1.1/P2).  
4. **Hub (optional)** — B0+B1+B2+B3 together if releasing weights.  
5. **Stop A40 pod** after local hash verification of released + closeout.

---

## Count summary

| Bucket | Count |
|---|---|
| E-items fully closed by execution/X | ~88 of 95 (some dual-status with paper half still `[ ]`) |
| X-01–X-15 | **15/15 `[x]`** |
| X-16–X-25 | **10/10 `[x]`** (X-23 paper half open) |
| X-26–X-27 | **`[ ]` documentary release** |
| Stop incidents documented | Gate S `[!]` dispositioned |

**Bottom line:** The filed confirmatory execution checklist is checked off through Gate X. What remains is **documentary / public release work**, not more gates or computation.
