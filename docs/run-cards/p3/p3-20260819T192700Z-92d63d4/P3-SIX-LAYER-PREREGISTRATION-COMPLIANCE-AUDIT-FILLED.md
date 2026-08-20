# P3 Six-Layer Preregistration Compliance Audit — FILLED

**Source:** `/Users/paulpajo/Downloads/P3 Six-Layer Preregistration Compliance Audit.md`  
**Audit fill date:** 2026-08-20 (post–Gate X)  
**Run:** `p3-20260819T192700Z-92d63d4` · AsPredicted **#307342** · ResearchBox **#8834**  
**LOCK:** `gate_x_unblinded` · `p3_outcome_access_count=1` · `test_access_count=1`

### Verdict

| Scope | Position |
|---|---|
| Layers I–II (execution + interpretability) | **CLOSED** — Gate X preflight 10/10 PASS; unblinding 2026-08-20T08:56:47Z |
| Layer III (reporting grammar) | **Seal-ready `[x]`**; paper/site/Hub prose still `[ ]` |
| Layer IV (stewardship beyond filing) | Mostly `[ ]` — ResearchBox/Hub/`results/p3`/advisor |
| Layer V residuals | Pre-X residuals **R-01–R-10 closed**; documentary R-11–R-20 partly open |
| Layer VI hidden risks | **Audited/cleared or dispositioned** at Gate X (H-01–H-11, H-13–H-16, H-21–H-22, H-24–H-26); paper/release risks remain until public docs |

**Primary contrasts (released seal):** `C_tl≈1.023` **observed**; `G_en≈−1.698` **observed**; B3 `not_mitigation=true`.

---

## 1. Executive compliance position (updated)

### 1.1 Narrow conclusion (post-X)

Q–W PASS was confirmed by status-only Gate X preflight (`gate-x-preflight.json`, 08:54:36Z). Formal unblinding (`P3_UNBLINDING_EVENT.json`, 08:56:47Z) released the full precommitted package under `released/` (cache + run-card mirror). **Confirmatory computation is closed.** Full public-report closure still requires paper, ResearchBox deposit, optional Hub, and `results/p3` packaging.

### 1.2 Layered finding summary (filled)

| Layer | Current position |
|---|---|
| **I. Explicit** | Filed path executed; EX-01–EX-32 computational halves `[x]`; release-channel wording still `[ ]` |
| **II. Implicit** | IM-01–IM-18 `[x]` via preflight + gate cards; IM-19–IM-20 `[x]` seal / `[ ]` paper freeze ongoing |
| **III. Inferred** | Grammar locked in seal; IN-01–IN-15 paper application `[ ]` |
| **IV. Extrapolated** | EP-07 partial (HOST card); EP-01–06,08–12 mostly open |
| **V. Residual** | R-01–R-10 `[x]`; R-11–R-20 documentary/ops open or deferred |
| **VI. Hidden** | Gate S dispositioned `[!]→cleared`; other pre-X risks audited; paper/archive risks open |

### 1.3 Authority + stale protocol

Authority hierarchy unchanged (PDF ≫ ops ≫ LOCK/cards ≫ deviations ≫ paper).  
**R-17 / H-13:** Dated supersession note added to `/Users/paulpajo/Downloads/P3 Comprehensive Staged Execution Protocol.md` (2026-08-20); historical header preserved.

---

# Layer I — Explicit (filled)

## §3 Domain index

| Explicit domain | Status |
|---|---|
| Filing and scope | `[x]` filing · `[ ]` every release channel |
| Question and signs | `[x]` Gate X mechanical contrasts |
| B3 role | `[x]` seal `not_mitigation` · `[ ]` paper wording |
| P0-T | `[x]` PASS both depths; before S |
| Freshness | `[x]` B0 parent + tok SHA matrix |
| Primary DVs | `[x]` evaluator/packing/hashes |
| Six cells + B0 EN descriptive | `[x]` released; B0 EN excluded |
| Legacy tests | `[x]` B2-only; secondary |
| Training conditions | `[x]` Q–T + budgets |
| Analysis constraints | `[x]` seal · `[ ]` paper |
| Exclusions | `[x]` hygiene/FA/parents |
| Access control | `[x]` U=0→V=1; outcome 0→1 at X |

## §4 EX-01–EX-32

| ID | Status | Evidence |
|---|---|---|
| EX-01 | `[x]` filing · `[ ]` release | Q1/Q8 in PDF |
| EX-02 | `[x]` | Pre-outcome LOCK + filed Q8 |
| EX-03 | `[ ]` | Paper/site/Hub/RB |
| EX-04 | `[x]` | Q/R/S parent = B0 `ae621be2…` |
| EX-05 | `[x]` | Seal `C_tl` |
| EX-06 | `[x]` | Seal `G_en` |
| EX-07 | `[x]` | Both observed vs 0.01 |
| EX-08 | `[x]` seal · `[ ]` paper | `not_mitigation=true` |
| EX-09 | `[x]` Gate E · `[ ]` paper table | doc 50/50; byte EN≈0.961 |
| EX-10 | `[x]` | P0-T ≺ S |
| EX-11–EX-15 | `[x]` | Gate D/F/U/released cells |
| EX-16 | `[x]` | Contrasts from U only |
| EX-17–EX-19 | `[x]` | d20; streams; `load_optimizer=False` |
| EX-20 | `[x]` seal · `[ ]` paper | One seed / no CI |
| EX-21–EX-25 | `[x]` | Frozen configs / hygiene |
| EX-26 | `[x]` | All arms released together |
| EX-27–EX-28 | `[x]` | N=294; B2-only V |
| EX-29–EX-32 | `[x]` | U+V then X; protocol SHA match |

---

# Layer II — Implicit (filled)

| ID | Status | Evidence |
|---|---|---|
| IM-01 | `[x]` | R/S/T `parent_b0_sha256` identical to Q/I d20 |
| IM-02 | `[x]` | Each child from B0 only |
| IM-03 | `[x]` | `selection_rule=final_checkpoint`; step 294 |
| IM-04 | `[x]` | 294×65536 = 19,267,584 |
| IM-05 | `[x]` | All d20 |
| IM-06 | `[x]` | Tok `04436b85…` |
| IM-07 | `[x]` | `evaluate_bpb.py`; packing BOS-bestfit T=2048 |
| IM-08 | `[x]` | Gates C/D/E mount hygiene |
| IM-09 | `[x]` | P0-T PASS before children |
| IM-10 | `[x]` | `b3_frozen_before_tl0_val=true` |
| IM-11 | `[x]` | Doc 50/50; byte shares unequal (reported) |
| IM-12 | `[x]` | Fresh optimizer on R/S/T |
| IM-13 | `[x]` | HOST A40 + pin; FA unpatched |
| IM-14 | `[x]` `[!]` cleared | Gate S: partial quarantined; clean restart |
| IM-15 | `[x]` | Preflight safe-log: 0 forbidden hits |
| IM-16 | `[x]` | V whitelist B2 only |
| IM-17 | `[x]` | 1 touch / 2 component events |
| IM-18 | `[x]` | LOCK outcome count 0→1 at X |
| IM-19 | `[x]` ready · `[ ]` paper | No P1.1/P2 numbers in seal path |
| IM-20 | `[x]` event · monitor | `no_additional_validation_or_test_eval=true` |

---

# Layer III — Inferred (filled)

| ID | Status | Note |
|---|---|---|
| IN-01–IN-07 | `[x]` seal grammar · `[ ]` paper | Observed/not observed; B3 descriptive; V secondary |
| IN-08 | `[ ]` | Public post-P2 sentence still required |
| IN-09–IN-14 | `[ ]` | Paper/site obligations |
| IN-15 | `[x]` disposition · `[ ]` paper | Gate S recovery documented in preflight |

---

# Layer IV — Extrapolated (filled)

| ID | Status |
|---|---|
| EP-01 | `[~]` scripts/p3 + run-cards present · `[ ]` public `results/p3` |
| EP-02 | `[ ]` Hub all-arms or dated deferral |
| EP-03 | `[ ]` ResearchBox #8834 deposit |
| EP-04 | `[ ]` advisor hash review |
| EP-05 | `[ ]` frozen table script execution hash |
| EP-06 | `[x]` partial | `released_manifest.json` · `[ ]` public ledger |
| EP-07 | `[x]` partial | `HOST-bef5h2lzy6f3mp.md` (A40, cu128, torch 2.9.1) |
| EP-08–EP-12 | `[ ]` | Licenses, site, P5, rotation |

---

# Layer V — Residual (filled)

| ID | Status | Action left |
|---|---|---|
| R-01 | `[x]` | Preflight done |
| R-02 | `[x]` | Was 0 before X |
| R-03 | `[x]` | Disposition in check 8 |
| R-04 | `[x]` | U 07:57:24Z < V 07:58:38Z |
| R-05 | `[x]` | B2 only |
| R-06 | `[x]` | Parent/tok/budget matrix |
| R-07 | `[x]` | Filed hashes |
| R-08 | `[x]` | Safe-log clean |
| R-09 | `[x]` | `P3_UNBLINDING_EVENT.json` |
| R-10 | `[x]` | Full simultaneous `released/` |
| R-11 | `[ ]` | Locked paper/table from frozen script |
| R-12 | `[ ]` | Apply IN-* in paper/card/site |
| R-13 | `[ ]` | ResearchBox upload |
| R-14 | `[ ]` | Public code/`results/p3` |
| R-15 | `[ ]` | Hub all-arms or deferral |
| R-16 | `[ ]` | Website post-X wording |
| R-17 | `[x]` | Supersession note on comprehensive protocol |
| R-18 | `[ ]` | Advisor/authorship check |
| R-19 | `[ ]` | Stop pod after 2nd-copy hash verify |
| R-20 | `[ ]` | Credential rotation as needed |

---

# Layer VI — Hidden risk register (filled)

| ID | Status | Disposition |
|---|---|---|
| H-01 | `[x]` cleared | Official S = clean B0 restart; no partial ckpt |
| H-02 | `[x]` cleared | Preflight safe-log + access=0 before X |
| H-03 | `[x]` cleared | No rank/adjective leak in scanned patterns |
| H-04 | `[x]` cleared | 2 components, B2 only |
| H-05 | `[x]` cleared | Hygiene/mount audits |
| H-06 | `[x]` cleared | Tok hash stable |
| H-07 | `[x]` cleared | Pin + evaluate_bpb |
| H-08 | `[x]` cleared | Common B0 parent |
| H-09 | `[x]` cleared | B0 SHA stable across children |
| H-10 | `[x]` cleared | Step 294, fresh opt |
| H-11 | `[x]` cleared | Byte ≠ doc share disclosed in Gate E |
| H-12 | `[x]` filing · `[ ]` paper | Mechanical carry-forward wording |
| H-13 | `[x]` | Supersession note added |
| H-14 | `[x]` partial | HOST env captured |
| H-15–H-17 | `[ ]` | Paper/table language audits |
| H-18 | `[ ]` | Hub policy |
| H-19–H-20 | `[ ]` | Archive denylist + external deposit |
| H-21 | `[x]` | W before X; scalars only at X |
| H-22 | `[x]` disclosed | One-person lab + automated hashes |
| H-23 | `[ ]` | Keep P4/P5 separate in future filings |
| H-24 | `[x]` | Event freezes further confirmatory eval |
| H-25 | `[~]` | Local+run-card mirrors exist; confirm before pod stop |
| H-26 | `[x]` scoped | Audit covers repo/run-cards/LOCK; chat screenshots out of band |

---

## §10 Gate X safety contract (filled)

| X-ID | Status |
|---|---|
| X-01–X-15 | **All `[x]`** via `gate-x-preflight.json` + companion explicit checklist fill |
| Release steps 1–5 | **`[x]`** — event written; bundle opened once; seal contrasts; access=1; no new eval |
| Hold conditions | None triggered |

## §11 Post-X declaration

**Eligible to sign for confirmatory execution.** Sign for full public closure only after R-11–R-16 (and chosen deferrals for R-15/R-18–R-20) are complete.

## §12 Dashboard (filled)

| Question | Answer |
|---|---|
| Filed before P3 outcomes? | **Yes** |
| Transparently post-P2? | **Yes** (must still say so publicly) |
| Q–W order? | **Yes** (hash/timestamp audited) |
| U before V? | **Yes** |
| Outcomes protected until X? | **Yes** |
| Values displayable? | **Yes** (released/) |
| More confirmatory compute? | **No** |
| Fully publicly closed? | **Not yet** — paper/RB/Hub/`results/p3` |

---

## Remaining open (do these next)

1. Paper + frozen table script (IN-*, EX-03, R-11–R-12)  
2. ResearchBox #8834 deposit (R-13, EP-03)  
3. `results/p3/` + docs packaging (R-14, EP-01)  
4. Hub all-arms or dated deferral (R-15, H-18)  
5. Website wording (R-16)  
6. Verify second archive copy → stop A40 pod (R-19, H-25)  
7. Rotate credentials if needed (R-20, EP-12)
