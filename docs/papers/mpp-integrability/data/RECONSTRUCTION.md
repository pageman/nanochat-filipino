# Reconstructed MPP dual-generator CSVs

**Status: `RECONSTRUCTED_NOT_ORIGINAL`.**

These files are a **new synthetic reconstruction** of the two CSVs that a
Kosmos-AI notebook once emitted. The original Edison/Kosmos bytes were never
in this repository. Hashes in `RECONSTRUCTION.json` are for **this** generator
(seed `20260820`). They will not match the 23 December 2025 run.

Do **not** treat recovered \(\rho\), \(\gamma_2\), or \(P(D)\) as Myers–Perry
measurements. The columns `Weyl_Boost_Weight_2`, `KY_Residual_Norm`, and
`Love_Number_k2` are synthetic labels. Gate-4 of the frozen query does **not**
filter on Pearson \(\rho\ge 0.70\).

## Files

Canonical names (Block 1 of `KOSMOS-QUERY-MPP-DUAL-GENERATOR-AUDIT.txt`):

- `MP_Quantum_Corrections_Sweep_D5-D9_baseline.csv`
- `MP_Quantum_Corrections_Sweep_D5-D9_rigid.csv`

The generator also writes permitted fallback names (same bytes) into `/workspace/`
so Block 1 of the frozen query can harvest either pair:

- `Quantum Corrections Sweep D5-D9 Baseline.csv`
- `Quantum Corrections Sweep D5-D9 Rigid.csv`

Do not treat those `/workspace/` copies as a second dataset. Generator:
`../scripts/reconstruct_csvs.py`.

Copy-paste audit query for these files (clean-room first draft):
`../KOSMOS-QUERY-RECONSTRUCTED-CLEANROOM-V1.txt`.

## What was matched

Published Cube counts (exact):

| \(D\) | Equal-spin | Generic |
|------:|----------:|--------:|
| 5 | 1992 | 7932 |
| 6 | 2047 | 8026 |
| 7 | 1915 | 7870 |
| 8 | 2055 | 8046 |
| 9 | 2013 | 8104 |

Also: \(N=50{,}000\) per variant; Single-Spin \(=19{,}940\); Generic-Multi-Spin \(=20{,}038\);
paired covariates across the two files; \(a\sim\mathrm{Unif}(4\cdot10^{-5},1.5)\);
\(\lambda\sim\mathrm{Unif}(10^{-6},0.3)\).

Label engines (not GR):

- Equal-spin KY \(\sim c\lambda^2\) (spin-independent). Recovered \(\beta_\lambda\approx 2.00\), \(\beta_a\approx 0\).
- Baseline \(D=5\) generic Weyl \(\sim c\,\lambda a^2\). Recovered \(\beta_a\approx 2.01\), \(\beta_\lambda\approx 1.00\).
- Rigid \(D=5\) generic Weyl is generated from the published quadratic
  \(\gamma_2=-0.1625\). The vertex is **out of range** (\(a_\star\sim 10^{12}\)).
  Protocol logs use \(\varepsilon=10^{-16}\), which pulls OLS \(\gamma_2\) toward
  about \(-0.14\); that is a logging-floor effect, not a turnover.
- Rigid differs from baseline **only** on \(D=5\) generic labels
  (Weyl and the KY/Love labels derived from it).
- Median generic/equal-spin Weyl **label** ratio is \(\sim 4\times 10^6\) on
  baseline and \(\sim 1\times 10^6\) on rigid \(D=5\), matching the previous
  Kosmos contrast. This is a generator contrast, not Type D protection.

This reconstruction’s SHA-256 values are in `RECONSTRUCTION.json`
(`HASH_BASE`, `HASH_RIGID`). They are **not** the 2025 Edison hashes.

## How to regenerate

```bash
python3 docs/papers/mpp-integrability/scripts/reconstruct_csvs.py
```

That writes both `/workspace/` copies (for a Block 1 harvest) and the copies
in this directory.
