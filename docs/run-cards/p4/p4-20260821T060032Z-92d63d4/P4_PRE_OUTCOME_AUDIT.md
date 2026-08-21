# P4 pre-outcome audit (Gate 0)

**Study:** P4-C3-TOKEN-SHARE  
**AsPredicted:** [#307591](https://aspredicted.org/if84km.pdf)  
**PDF SHA-256:** `463b29fcff8d7c8099790325fa19d6bcf9ee29f64424c373a380566a6fe9011c`  
**Run ID:** `p4-20260821T060032Z-92d63d4`  
**Checked against:** filed PDF Q2–Q8 + SHA-bound addendum `f056a6f75c73a4d8dc3401ba8d7219d406aa7e498e5b0799d3d0373f9f74c216`  
**Does not amend:** #306780, #306935, #307342  

This file is an operational Gate 0 receipt. It does **not** change any filed quantity. The three Q8-hashed protocol files were not edited for this audit.

## F4 checklist

| ID | Filed value | In PDF / addendum | Status |
|---|---|---|---|
| F4-01 | P4-C3-TOKEN-SHARE; post-P3; does not amend #306780/#306935/#307342 | PDF Q2, Q8 | checked |
| F4-02 | Carry-forward `tokenizer.pkl` `04436b85…` and `token_bytes.pt` `a5dbc1c8…7f7ad…` | PDF Q4 | checked |
| F4-03 | \(q_{\mathrm{TL}}=0.50\) Tagalog source-content tokens (no BOS/pad/pack/crop) | PDF Q2, Q4 | checked |
| F4-04 | \(\delta=\delta_{\mathrm{P0T}}=0.01\); equality counts | PDF Q2 | checked |
| F4-05 / F4-19 | Python `random.Random`; C3 list/interleave seed 42; untrained P0-T seed 0; parent init seed 0 | PDF Q4 seed 42; addendum table | checked |
| F4-06 | 2048-token blocks | PDF Q4 | checked |
| F4-07 | Round-half-to-even TL; EN residual | addendum (SHA-bound) | checked |
| F4-08 | Quotas 9633792/9633792; \(D_{\mathrm{phase2}}=19267584\) | PDF Q4, Q7 | checked |
| F4-09 | C3 `val.parquet` not a DV | PDF Q3 | checked |
| F4-10 | Policy A: C3-only after U; named holdouts | PDF Q3 | checked |
| F4-11 | d8 eligibility only; d20 = only C0; \(N=294\); \(T=2048\); \(B=65536\) | PDF Q2, Q4 | checked |
| F4-12 | Fresh Muon+AdamW; `load_optimizer=False`; peak LR = 0.3 x parent; warmup 14 | PDF Q4 | checked |
| F4-13 | NVIDIA CUDA (A40 class); not a live pod | PDF Q4 | checked |
| F4-14 | New ResearchBox #8869; AsCollected #2455 v1 | LOCK; not #8834 | checked |
| F4-15 | C0 English val once at U, descriptive, excluded from contrasts | PDF Q3, Q5 | checked |
| F4-15b | Serial R then S then T | PDF Q4 | checked |
| F4-16 | Roles: operator (gates); lockbox custodian (distinct if possible); unblinding officer at Gate X | master §; this audit | checked (one-person fallback below) |
| F4-17 | Overlapping #306780, #306935, #307342 | PDF bundle footer | checked |
| F4-18 | Reporting grammar: no “mitigation”; C3 is not P3 B3; no test-set \(R_{\mathrm{TL}}\)/\(A_{\mathrm{EN}}\) | PDF Q2, Q5, Q8 | checked |
| F4-20 | Terminal checkpoint only | PDF Q4 | checked |
| F4-21 | P0-T CUDA-only status; evaluator/packing/seeds in SHA-bound addendum | PDF Q5, Q8 | checked |
| F4-22 | Byte-identical copies of six named JSONLs; hash mismatch = stop | PDF Q3, Q6 | checked |

## One-person lockbox fallback

Preferred: a second person holds the lockbox passphrase and is the only Gate X opener.

Until that person exists, P4 uses the **weak fallback** named in the gate bible:

1. Dummy/real outcome JSON lives only under `data/cache/p4-20260821T060032Z-92d63d4/lockbox/` (mode `0700`; gitignored).  
2. Passphrase file `data/cache/p4-20260821T060032Z-92d63d4/.lockbox_pass` is mode `0600`, gitignored, and is **not** the ResearchBox passcode.  
3. Gate 0 encrypts dummy results with OpenSSL AES-256-CBC + PBKDF2 so a steward who can list the directory cannot read plaintext BPB.  
4. Time-lock: do not decrypt lockbox files until Gate X preflight is status-only complete. Break-glass writes an audit JSON **without** printing BPB (`scripts/p4/break_glass.py`).  
5. Safe progress (`0755`, different from lockbox) may contain PASS/BLOCKED/TECHNICAL BLOCK, hashes, and counts only.

## Blinding reminder

No P4 `val_bpb_full` or test BPB has been computed. Dummy scalars in Gate 0 tests are synthetic (`1.111111` family) and stay in the gitignored lockbox. Do not paste them into chat, paper, or ResearchBox.

## Result

Dummy lockbox tests **1–18 pass** (`docs/run-cards/p4/p4-20260821T060032Z-92d63d4/gate-0-lockbox-tests.json`). `scripts/p4/` tree SHA-256 `499b1771661ed16a86630ea89679a2cadc3c32b46f78e36886b71658e770888f`. Gate 0 is **pass**. Next is Gate A. No P4 outcomes exist.
