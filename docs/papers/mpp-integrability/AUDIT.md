# Six-layer weakness census of v1

Parent draft: *Integrability Protection and the Accelerated Fragility of Quantum-Corrected Myers-Perry Spacetimes* (Pajo, 23 December 2025), archived as `paper_v1_source.pdf`.

Layer confidence while writing: explicit 99%; residual 95%; implicit 90%; inferred 85%; extrapolated 80%; hidden 75%. Hidden items are the most load-bearing and the easiest to miss.

This census enumerates weaknesses. The repaired statements live in `paper.md` / `paper.tex`. No item below is left as a “future work” dodge: each maps to a quarantine, a definition, a lemma, or a deletion.

Wrong answers, named so they can be rejected on sight:

1. Keep `ρ = 0.998`, `γ₂ = −0.163`, or `P(D) ∼ 10^6` as physical results.
2. Call quadratic-curvature EFT “quantum” or “semiclassical” because `ℏ` is not in the truncated action.
3. Treat Stein’s `qnm` package as a higher-dimensional Killing–Yano or Love-number solver.
4. Identify CMPP Type D, principal CKY, geodesic integrability, linear mode stability, and cosmic censorship.
5. Call classical `k₂` in `D ≥ 5` “quantum hair.”
6. Use `a → 1` ultraspinning language for `D = 5`.
7. Treat a Gate that requires `ρ ≥ 0.70` as independent confirmation of `ρ = 0.998`.
8. Cite JHEP 11 (2022) 161 as Cano et al. (it is Aalsma–Shiu).
9. Claim singularity resolution inside a truncated EFT.
10. Invent replacement numerics to fill the plots.

---

## E. Explicit (on the page)

E1. **Sample-size contradiction.** Abstract: `10^5` Sobol points. Block 1: `50,000` points. These cannot both be the study.

E2. **Unreproduced headline numbers.** `ρ = 0.998`, `γ₂ = −0.163`, `P(D)` suppression `10^6` have no table, no residual definition, no seed, no code, no data file.

E3. **Equation (1) is not an equation.** `log10(k₂) ∝ α_W log10(Weyl Deviation)` states neither intercept, slope, error model, domain, nor the definition of “Weyl Deviation.”

E4. **`α_W` never evaluated.** The only displayed formula contains a free symbol that is never fitted.

E5. **`β_a` never defined.** Figure 1C caption names a coefficient that does not appear in the text.

E6. **`γ₂` never defined.** “Negative curvature” is not a statistical model. Quadratic in what variable, on what scale, with what link function?

E7. **`P(D)` never defined.** A “protection factor” without a formula cannot be dimension-independent, nor equal to `10^6`.

E8. **Placeholder citations.** `[cite: 1]`, `[cite: 2]`, `[cite: 3]`, `[cite: 15]` remain in the PDF.

E9. **Mis-citation of JHEP 11 (2022) 161.** That article is Aalsma–Shiu on WGC/rotating extremality, not Cano et al. on algebraic degeneracy.

E10. **Mis-pagination of Stein JOSS.** The `qnm` paper is *J. Open Source Softw.* **4**, 1683 (2019), not 1692.

E11. **Incomplete Frassino (2025) reference.** Journal, volume, and page are missing; the bibliographic key cannot be resolved.

E12. **Unresolved Liu (2024) and Sánchez (2024) keys.** No arXiv ids, no titles. At least one collides with the well-known Hui et al. JCAP 04 (2021) 052 Love-number paper.

E13. **`qnm` used for the wrong observables.** Stein (2019) computes 4D Kerr QNM frequencies `(s,ℓ,m,n; a)`. It does not compute KY residuals, CMPP boost-weight norms, or `D ≥ 5` Love numbers.

E14. **Figures without data.** Figures 1–3 are captions over empty or schematic panels. No axis units, no error bars, no file hashes.

E15. **Duplicate `P(D)` figures.** Figure 1A and Figure 2 both claim to display `P(D)`.

E16. **`r` versus `ρ`.** Caption of Figure 1B uses `r = 0.998`; the text uses `ρ = 0.998`. Pearson and a Greek rho are not identified.

E17. **DOI claimed, DOI absent.** Block 6 promises “a unique DOI.” None is given.

E18. **`nuances.yml` claimed, file absent.** Pre-registration cannot be a missing config.

E19. **`Λ_{QG} ∈ [0, 0.1]` has no units** and no relation to a Planck mass, a Wilson coefficient, or a curvature scale.

E20. **“ArXiv Classification” is not a keyword field.**

E21. **Author footnote thanks GPT-5.2 / AI Studio / Kosmos as if they were co-authors**, while the author line is a single name. Provenance of the scientific claims is then un-auditable.

E22. **Kosmos trajectory URL is presented as “the data analysis.”** A third-party chat log is not a metric, not a residual, not a Love number.

E23. **Title/filename mismatch.** Filename: *Algebraic Degeneracy and Integrability in Quantum-Corrected Higher-Dimensional Rotating Black Holes*. Title: *Integrability Protection and the Accelerated Fragility of Quantum-Corrected Myers-Perry Spacetimes*.

E24. **Abstract “D = 5 − 9” versus ultraspinning language `a → 1`.** In `D = 5` there is a Kerr-like bound; ultraspinning is `D ≥ 6`.

E25. **“Weyl Type D deviations suppressed by `10^6`”** is a numerical claim with no Weyl component, no frame, no boost-weight, no norm.

E26. **Gate `ρ ≥ 0.70` is printed as a validation filter** for a paper whose headline is `ρ = 0.998`.

E27. **50,000 / 100,000 “synthetic numerical solutions”** are never identified as solutions of any PDE.

E28. **No Myers–Perry line element is written.**

E29. **No EFT action is written.** “`R²`, `R⁴`” is not an operator basis.

E30. **No Killing–Yano equation is written.**

---

## I. Implicit (used but not stated)

I1. That a Sobol sequence on `(M, a_i, D)` induces the *physical* measure on the moduli space of black holes.

I2. That “synthetic” labels are unbiased estimators of on-shell EFT observables.

I3. That bootstrap confidence intervals capture the dominant uncertainty (they do not, if the labels are the model).

I4. That `joblib` parallelization is a methodological contribution.

I5. That equal-spin configurations are a positive-measure set in the Sobol design (they are a lower-dimensional submanifold).

I6. That Cube Design stratification was applied *and* that the abstract’s `10^5` still describes the stratified set.

I7. That “single fidelity tier” means something other than “we did not converge anything.”

I8. That CMPP Type D is equivalent to existence of a principal conformal Killing–Yano tensor in `D ≥ 5`.

I9. That geodesic integrability is equivalent to linear mode stability.

I10. That linear mode stability is equivalent to cosmic censorship.

I11. That algebraic “fragility” is a decay toward naked singularities.

I12. That `k₂` is the gravitational quadrupole Love number rather than a scalar response.

I13. That the Love numbers are static, in a stated gauge, without logarithmic running.

I14. That a log–log correlation is a power law with a universal exponent.

I15. That “quantum hair” denotes a violation of the no-hair theorem rather than a classical tidal response.

I16. That “semiclassical” means one-loop `ℏ` rather than “we used EFT.”

I17. That Reall–Santos (2019) computed the corrected *metric* (they computed thermodynamics without the metric).

I18. That Cano’s Kerr EFT metric results transplant to MP in `D = 5–9` without work.

I19. That Charalambous–Ivanov (2023) support “Love symmetry as a consequence of equal-spin protection.” They study generic 5D MP, including unequal spins, and find generically *nonzero* `k₂`.

I20. That Kehagias–Riotto vanishing theorems apply in `D ≥ 5` (they are 4D statements).

I21. That a six-block pipeline with an immutable skeleton is a scientific control rather than a narrative.

I22. That committing `nuances.yml` “prior to execution” occurred, in a repository that does not contain the file.

I23. That `D` may be sampled as a continuous Sobol coordinate (it is an integer).

I24. That mass `M` and spins `a_i` may be sampled independently of horizon existence.

I25. That figures 1–3 exist as scientific objects rather than as caption shells.

---

## N. Inferred (forced by combining explicit statements)

N1. **The Gate selects the result.** If only configurations with `ρ ≥ 0.70` pass, a reported `ρ = 0.998` is a selected statistic, not a discovery.

N2. **Labels were planted or tautological.** Independent noise at the claimed `N` cannot produce `|ρ| = 0.998` (stress test T50). A near-perfect correlation in a “label engine” is the signature of a deterministic function of one variable, not of a measured hidden-symmetry breakdown.

N3. **UQ is circular.** Bootstrapping planted labels recovers the planting (T22).

N4. **The pipeline cannot have computed the observables it names**, because the named tool (`qnm`) cannot emit them (T14).

N5. **“Quantum-corrected” in the title is false advertising** given the body (`R²` operators, no loops, no `ℏ`).

N6. **Equal-spin “protection” as a `10^6` numerical factor contradicts “dimension-independent structural feature.”** A structural vanishing is exact, not `10^{-6}`. A numerical `10^{-6}` is a truncation or a float residual.

N7. **v1’s rigidification “stress test” is not a stress test of a stated hypothesis**, because the hypothesis is uncited and unformalized (T45).

N8. **D=5 generic-sector `a → 1` is an extrapolation off the sub-extremal domain** or a silent switch to dimensionless `a/a_{\mathrm{ext}}`.

N9. **The paper’s own Block 1 and abstract cannot be true together** (E1), so every downstream frequency, CI, and plot is unanchored.

N10. **“Cross-model validation” is empty** without a second model or a DOI.

N11. **Love numbers cannot be “activated by `R²`” in `D ≥ 5`**, because they are already generically nonzero in GR (Charalambous–Ivanov 2023; Kol–Smolkin; higher-D Schwarzschild-Tangherlini).

N12. **The “integrability gap” is being asked to do the work of isometry reduction.** Equal-spin odd-`D` MP is cohomogeneity-1; generic MP is not. That gap exists in *classical* GR with `α = 0`.

N13. **A protection factor that is robust from `D = 5` to `D = 9` cannot be a statement about ultraspinning**, which does not exist in `D = 5`.

N14. **MSC 83C75 (singularities) is not licensed by the calculations**, which never inspect a curvature singularity.

N15. **PACS 04.70.Dy (quantum aspects of black holes)** is not licensed by a classical EFT truncation.

---

## X. Extrapolated (v1 treats a local statement as global)

X1. From 5D scalar Love numbers to `D = 5–9` gravitational `k₂`.

X2. From Kerr 4D EFT (Cano–Ruipérez, Reall–Santos) to MP `D = 9`.

X3. From algebraic speciality lifting to naked singularities.

X4. From KY residual growth to “accelerated fragility” of the spacetime.

X5. From equal-spin odd-`D` isometry to “semiclassical protection” in all sectors.

X6. From a log–log plot (not shown) to a universal power law.

X7. From perturbative `R²` to a verdict on nonperturbative RG improvement.

X8. From Bonanno–Reuter-style RG folklore to “must incorporate RG-flow dynamics [11].”

X9. From 4D vanishing Love numbers to the claim that nonzero `k₂` is *the* quantum signature.

X10. From existence of a principal tensor in GR MP to persistence of a “deformed KY tensor” under EFT.

X11. From cohomogeneity-1 *quadrature* to persistence of the *hidden* KY tower.

X12. From one unspecified `D = 5` generic-sector fit to “higher-dimensional black holes appear more fragile.”

X13. From Wilson coefficients of unspecified sign and magnitude to a universal `γ₂ < 0`.

X14. From a Kosmos trajectory to an archival scientific record.

X15. From “future work must…” to a negative discovery about singularity resolution.

---

## R. Residual (left after charitable reading)

R1. Even if one ignores the numbers, **no operator basis is fixed** (Gauss–Bonnet vs Weyl-squared vs Ricci-squared vs Riemann-cubed vs `R^4`).

R2. Even if one ignores `qnm`, **no reduction-of-order or Reall–Santos protocol is specified**, so the EFT initial-value problem is ill-posed (Ostrogradsky).

R3. Even if equal-spin protection is re-read as isometry, **v1 still claims the deformed KY tensor remains nearly invariant**, which is a stronger, unproved PDE statement.

R4. Even if `k₂` is re-read as scalar, **v1 still claims it tracks KY breakdown**, which does not follow from a correlation, and which is false as a universal because of resonant magic zeroes.

R5. Even if the Gate is dropped, **Sobol on dimension as a real variable is still wrong**.

R6. Even if citations are repaired, **the empirical study did not occur**.

R7. Even if “quantum” is replaced by “EFT,” **EFT validity `|α R| ≪ 1` at the horizon is unchecked**, especially near extremality.

R8. Even if figures are ignored, **the logical outline still identifies four inequivalent properties**.

R9. Even if AI assistance is moved to acknowledgments, **the scientific provenance of every number remains Kosmos**.

R10. Even if `N` is chosen to be `10^5` *or* `5×10^4`, **no split between generic and equal-spin samples is given**.

R11. Even if `Λ_{QG}` is declared dimensionless, **the map to Wilson coefficients is missing**.

R12. Even if one accepts synthetic data as a surrogate, **the surrogate’s generative model is unspecified**, so the correlation is uninterpretable.

R13. Residual ambiguity between **closed conformal KY, genuine KY, Killing tensors, and Killing vectors**.

R14. Residual ambiguity between **inner-horizon Cauchy instability and outer-horizon ultraspinning GL**.

R15. Residual ambiguity between **static, dynamical, and running Love numbers**.

---

## H. Hidden (load-bearing, easy to miss)

H1. **The equal-spin locus has measure zero** in the generic spin torus for `n ≥ 2` (codimension `n−1`). A Sobol harvest of generic `a_i` will almost never hit it; Cube Design must *force* it. v1 never says how many equal-spin points exist.

H2. **Cohomogeneity-1 geodesic motion is integrable by quadrature from *explicit* isometries**, without a principal tensor. The “integrability gap” in GR is therefore not evidence of a quantum mechanism.

H3. **The converse “CMPP Type D ⇒ principal CKY” is not a theorem in `D ≥ 5`.** v1 uses the converse silently.

H4. **Super-extremal Kerr/MP is still Type D and still KY-integrable, and is a naked singularity.** So algebraic speciality does not protect cosmic censorship.

H5. **Ultraspinning MP is still Type D and still KY-integrable, and is linearly unstable for `D ≥ 6`.** So hidden symmetry does not protect dynamical stability.

H6. **`D = 5` cannot ultraspin.** Any `D = 5` “accelerated fragility as `a → 1`” is extremal-EFT breakdown, not Emparan–Myers ultraspinning.

H7. **Gauss–Bonnet is topological in `D = 4` and the leading *dynamical* quadratic term in `D ≥ 5`.** Talking about “`R²` corrections” without saying GB vs Weyl-squared is not an EFT.

H8. **Ricci-squared terms are field-redefinition redundant** on Einstein backgrounds at leading order. A pipeline that “turns on `R²`” may be turning on nothing.

H9. **Naive `Riem^2` has ghosts.** Without reduction of order, “fragility” may be an artifact of extra modes.

H10. **Love numbers in `D ≥ 5` generically run.** A single `k₂` is not an observable until the matching scale is chosen.

H11. **Resonant vanishing (“magic zeroes”)** produces `k₂ = 0` without KY restoration. Therefore `k₂` cannot be a faithful signature of KY breakdown.

H12. **Near-zone `SL(2,ℝ)` Love symmetry is a truncation of the wave equation**, not the principal 2-form. v1 cites Charalambous–Ivanov against their actual theorem.

H13. **A log of a signed residual is undefined.** Any implementation of eq. (1) must have thresholded or taken an absolute value; that choice is a degree of freedom that can create a fake power law.

H14. **The 4D vanishing of Kerr Love numbers is a 4D theorem.** Using it as the null against which `D ≥ 5` `R²` “activates” `k₂` is a category error: `D ≥ 5` GR already activates `k₂`.

H15. **Reall–Santos can give corrected thermodynamics without a corrected metric.** KY residuals and Weyl boost-weights *require the metric* (or an equivalent tensor). RS does not supply them.

H16. **Higher-derivative well-posedness and horizon regularity are independent of Sobol sampling.**

H17. **“Immutable six-block skeleton” plus plug-ins is an unregistered garden of forking paths.**

H18. **Naming the pipeline after the author (Myers–Perry–Pajo) does not create a method.**

H19. **A `10^6` factor is a typical plotting ratio, not a derived suppression from representation theory.** Exact symmetry protection is `0`, not `10^{-6}`.

H20. **The paper is five pages including three non-figures.** There is no room in v1 for the calculation it claims to have done; the calculation did not occur in the manuscript.

H21. **Pre-registration theater.** A YAML file that is neither hashed nor dated nor archived cannot underwrite `ρ = 0.998`.

H22. **The true hidden variable is the label engine.** Until that function is written, every correlation is a statement about a computer program that is not in the paper.

---

## Repair map

| Weakness class | Repair in the revised paper |
| --- | --- |
| E2, N2, N3, R6, H22 | Quarantine all v1 numbers. Do not replace them with new fictions. |
| E13, N4, I18 | Delete `qnm` as a method. Specify what a valid pipeline would need. |
| E9–E12 | Correct the bibliography. |
| I8–I11, H3–H5 | Proposition on logical independence, with Lamport proofs. |
| I16, N5, H7–H9 | Replace “quantum/semiclassical” by a written EFT action and field-redefinition lemmas. |
| N12, H1, H2 | Equal-spin protection as classical isometry / cohomogeneity, not `P(D)∼10^6`. |
| I12–I15, H10–H14, N11 | Love numbers as classical, generically nonzero, running; not quantum hair. |
| X3–X4, H4 | Algebraic type does not imply censorship. |
| R2, H9, H15 | Ostrogradsky / reduction of order / RS vs metric. |
| E26, N1 | Gate bias lemma. |
| T1–T50 | Executable stress tests of the *repaired* claims. |
