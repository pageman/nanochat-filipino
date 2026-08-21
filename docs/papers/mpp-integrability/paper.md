# Hidden Symmetry, Algebraic Type, and Tidal Response of Myers–Perry Black Holes under Higher-Curvature Effective Corrections: An Audited and Formal Account

Paul Pajo  
De La Salle–College of Saint Benilde  
`paulamerigo.pajojr@benilde.edu.ph`

20 August 2026  

**Status.** This manuscript *replaces* the five-page draft of 23 December 2025 (archived as `paper_v1_source.pdf`). Every numerical headline of that draft is quarantined. This paper does not amend nanochat-filipino studies AsPredicted #306780 or #306935.

---

## Abstract

The 23 December 2025 draft claimed a “semiclassical protection mechanism” suppressing Weyl Type D deviations by \(10^6\) in equal-spin Myers–Perry (MP) black holes, an “accelerated fragility” coefficient \(\gamma_2 = -0.163\) in the generic sector, and a correlation \(\rho = 0.998\) between Killing–Yano breakdown and tidal Love numbers, interpreted as quantum hair. Those numbers are not scientific results: the sample size contradicts itself (\(10^5\) versus \(5\times 10^4\)), the named computational engine (Stein’s `qnm` package) cannot emit the named observables, the Gate \(\rho\ge 0.70\) selects the headline correlation, and the operator content of the “quantum” correction is never written.

This revision does four things. First, it enumerates explicit, implicit, inferred, extrapolated, residual, and hidden weaknesses of the draft (full census: `AUDIT.md`). Second, it writes the geometric and effective-field-theory (EFT) objects that were being used silently. Third, it proves, in Proposition–Lemma form with Lamport-style hierarchical proofs, the statements that actually survive: (i) CMPP algebraic speciality, principal conformal Killing–Yano (CKY) integrability, linear mode stability, and weak cosmic censorship are pairwise independent on the MP family; (ii) equal-spin “protection” in odd dimension is classical isometry reduction to cohomogeneity one, contains no \(\hbar\), and does not by itself protect the CKY equation; (iii) scalar Love numbers of five-dimensional MP are already generically nonzero in classical GR, so nonzero \(k_2\) is not quantum hair and is not a faithful tracer of CKY breakdown; (iv) a truncated curvature-squared EFT cannot resolve curvature singularities, and perturbative control can fail as extremality is approached, independently of any quadratic fit \(\gamma_2\). Fourth, it stress-tests the repaired claims in fifty de-duplicated ways (`scripts/stress50.py`, 50/50 pass) and records a before/after ledger.

**Keywords.** Myers–Perry black holes; Killing–Yano tensors; CMPP classification; cohomogeneity; effective field theory; tidal Love numbers; cosmic censorship.  
**MSC (2020).** 83C57, 83E15, 53C50, 37J35.  
**PACS.** 04.50.Gh, 04.20.Fy, 04.60.Cf.

---

## 1. What the previous draft asserted, and what is withdrawn

Let \(D\ge 5\) and let \((M,a_1,\dots,a_n)\) be Myers–Perry parameters, \(n=\lfloor(D-1)/2\rfloor\). The draft asserted:

1. A six-block “MPP pipeline” evaluated \(N\in\{5\times 10^4,10^5\}\) synthetic configurations for \(D=5\)–\(9\) with a coupling \(\Lambda_{\mathrm{QG}}\in[0,0.1]\).
2. Equal-spin (“cohomogeneity-1”) configurations enjoy a semiclassical protection factor \(P(D)\) suppressing Type D deviations by \(10^6\).
3. Generic configurations exhibit accelerated algebraic fragility \(\gamma_2=-0.163\) under \(R^2\) corrections, contradicting an uncited “quantum rigidification” hypothesis.
4. \(\log_{10}k_2\) and \(\log_{10}\) of a “Weyl boost-weight deviation” correlate at \(\rho=0.998\), so Love numbers are quantum hair.

**Withdrawal.** Items 2–4, and the numerical part of item 1, are withdrawn. They are not replaced by new Monte Carlo output. What remains is the geometry that the draft was gesturing at, made precise.

Throughout, “v1” means the 23 December 2025 draft. “This paper” means the present revision.

---

## 2. Standing definitions

### 2.1 Myers–Perry parameters and cohomogeneity

Let \(D=2n+\varepsilon\) with \(\varepsilon\in\{0,1\}\) and \(n=\lfloor(D-1)/2\rfloor\). The vacuum Myers–Perry metric in \(D\) dimensions is parameterized by a mass \(M>0\) and \(n\) spin parameters \(a_i\in\mathbb{R}\) [MyersPerry1986]. Its generic isometry algebra is \(\mathbb{R}_t\oplus \mathfrak{u}(1)^{\oplus n}\).

**Definition 2.1 (Generic cohomogeneity).** The generic cohomogeneity of MP is
\[
\operatorname{cohom}_{\mathrm{gen}}(D) := D-n-1 = n+\varepsilon-1.
\]
Thus \(\operatorname{cohom}_{\mathrm{gen}}(5)=2\) and \(\operatorname{cohom}_{\mathrm{gen}}(6)=3\).

**Definition 2.2 (Equal-spin locus).** The equal-spin locus is \(\{a_1=\cdots=a_n\}\). For odd \(D=2n+1\) this enhances the isometry to \(\mathbb{R}_t\times U(n)\) (up to discrete identifications) and drops the cohomogeneity to \(1\) [GibbonsLuPagePope2004]. For even \(D\) the equal-spin enhancement does *not* reproduce that cohomogeneity-1 story; v1’s uniform “\(D=5\)–\(9\) cohomogeneity-1” clause is false.

**Definition 2.3 (Subextremal / ultraspinning).** In \(D=5\) there is a Kerr-like bound on \((a_1,a_2)\) at fixed \(M\); there is no ultraspinning regime. In \(D\ge 6\) some spin directions are unbounded and the Emparan–Myers ultraspinning instability exists [EmparanMyers2003, DiasFiguerasMonteiroSantos2010]. v1’s \(D=5\) plot caption “as \(a\to 1\)” is therefore either a silent normalization \(a/a_{\mathrm{ext}}\) or an extrapolation off the black-hole domain.

### 2.2 Principal tensor and the Killing tower

**Definition 2.4 (Closed conformal Killing–Yano 2-form).** A 2-form \(h\) is a *closed conformal Killing–Yano* (CKY) tensor if \(\mathrm{d}h=0\) and
\[
\nabla_X h = X^\flat \wedge \xi
\]
for a 1-form \(\xi\) (necessarily \(\xi=\frac{1}{D-1}\delta h\)). It is *principal* if it is nondegenerate as a 2-form (maximal matrix rank \(2n\)).

**Definition 2.5 (Killing–Yano residual).** For a trial 2-form \(h\) on a metric \(g\), write
\[
\mathcal{R}(h;g) := \bigl\|\nabla_X h - X^\flat\wedge \xi\bigr\|_{L^2(K)}
\]
evaluated on a specified compact region \(K\) outside the horizon, in a specified frame, with \(\xi=\frac{1}{D-1}\delta h\). v1 never wrote this (or any other) residual. No number called a “KY residual” in v1 is used here.

The existence of a principal tensor on MP and on Kerr–NUT–(A)dS, and the generation of a Killing tower of \(n\) independent Killing tensors together with \(n+\varepsilon\) Killing vectors, is the theorem of Frolov–Kubizňák–Krtouš–Page [FrolovKubiznak2007, Krtousetal2007, FrolovKrtousKubiznak2017]. The discrete identity \(n+(n+\varepsilon)=D\) is Lemma 3.1 below.

### 2.3 CMPP type

**Definition 2.6.** The Coley–Milson–Pravda–Pravdová (CMPP) classification [Coleyetal2004] assigns an algebraic type to the Weyl tensor in \(D\ge 4\) via boost-weight alignment. MP is CMPP Type D [Coleyetal2004, DeSmet, GodazgarReall]. Houri–Oota–Yasui and related work show that a *principal* CKY 2-form implies Type D. The converse in \(D\ge 5\) is not a theorem [SantosKYReview].

### 2.4 EFT truncation (classical, not semiclassical)

v1’s “quantum corrections” are, in the body, curvature-squared operators. We write the truncation that was being gestured at.

**Definition 2.7 (Quadratic vacuum EFT in \(D\ge 5\)).** Up to total derivatives and field redefinitions of the metric that preserve the Einstein frame at leading order,
\[
S[g] = \frac{1}{16\pi G_D}\int\mathrm{d}^D x\sqrt{-g}\Bigl(R + \alpha_{\mathrm{GB}}\,\mathcal{L}_{\mathrm{GB}} + \alpha_{\mathrm{W}}\,C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma} + \cdots\Bigr),
\]
where \(\mathcal{L}_{\mathrm{GB}}=R^2-4R_{\mu\nu}R^{\mu\nu}+R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}\) is Gauss–Bonnet. Ricci-squared operators are redundant on Einstein backgrounds at this order. Gauss–Bonnet is topological in \(D=4\) and dynamical in \(D\ge 5\). There is no \(\hbar\) in \(S[g]\). Calling solutions of \(\delta S=0\) “semiclassical” is a category error (Lemma 4.3).

Generic quadratic curvature without a Lovelock or reduction-of-order treatment introduces Ostrogradsky ghosts. A scientifically usable perturbation about MP is either (i) a Lovelock/Gauss–Bonnet deformation, (ii) a reduced-order EFT, or (iii) a Reall–Santos Euclidean computation of *thermodynamics*, which does not supply a corrected metric [ReallSantos2019]. KY residuals and Weyl boost-weights require a metric (or an equivalent tensor). v1 supplied neither.

**Definition 2.8 (EFT validity).** A first-order deformation \(g=g_{\mathrm{MP}}+\alpha\,\delta g+O(\alpha^2)\) is inside the EFT if \(|\alpha\,\mathrm{Riem}[g_{\mathrm{MP}}]|\ll 1\) on and outside the outer horizon. This condition can fail as extremality or ultraspinning is approached, independently of any fit \(\gamma_2\).

### 2.5 Love numbers

**Definition 2.9.** A static scalar Love number \(k_{\ell}\) of an asymptotically flat black hole is the conservative response coefficient in the large-\(r\) expansion of a massless scalar, in a specified matching scheme [Huietal2021, CharalambousIvanov2023]. Gravitational Love numbers are the spin-2 analogue. Dynamical responses include dissipative pieces. In \(D\ge 5\), generic static scalar Love numbers of MP are *nonzero already in GR* and exhibit logarithmic running except at resonant “magic zeroes” [CharalambousIvanov2023].

v1’s \(k_2\) is never identified as scalar or gravitational, static or dynamical, running or not, and is never given a gauge. It is not used as a number in this paper.

**Definition 2.10 (Quantum hair, as used here).** We reserve “quantum hair” for violations of the classical no-hair property associated with \(\hbar\) (Hawking radiation correlations, soft hair of Hawking–Perry–Strominger, Giddings’ nonlocality). Classical tidal response is not quantum hair.

### 2.6 Quarantine

**Definition 2.11 (Quarantined v1 statistics).** The symbols
\[
N\in\{5\times 10^4,10^5\},\quad \rho=0.998,\quad r=0.998,\quad \gamma_2=-0.163,\quad P(D)\sim 10^6,\quad \Lambda_{\mathrm{QG}}\in[0,0.1]
\]
are *quarantined*. They may be mentioned only as historical claims of v1. They are not parameters of any model in this paper.

---

## 3. Formal development

Lamport-style proofs are indented hierarchies. A step \(\langle k\rangle m\) is the \(m\)-th claim at level \(k\). “QED” closes the current level. Citations to the literature are used as *external lemmas* when the proof is not reproduced (the standard mathematical practice); we never cite a Kosmos trajectory as a lemma.

### 3.1 Discrete identities

**Lemma 3.1 (Killing-tower cardinality).** Let \(D=2n+\varepsilon\) with \(\varepsilon\in\{0,1\}\). If a principal CKY 2-form exists, the Killing tower produces \(n\) Killing tensors and \(n+\varepsilon\) Killing vectors, totaling \(D\) constants of geodesic motion.

*Lamport proof.*

\(\langle 1\rangle 1.\) \(n+(n+\varepsilon)=2n+\varepsilon\).

  \(\langle 2\rangle 1.\) \(n+(n+\varepsilon)=(n+n)+\varepsilon\) by associativity of addition in \(\mathbb{N}\).

  \(\langle 2\rangle 2.\) \(n+n=2n\).

  \(\langle 2\rangle 3.\) \(2n+\varepsilon=D\) by the standing decomposition of \(D\).

  \(\langle 2\rangle 4.\) QED.

\(\langle 1\rangle 2.\) The geometric generation of those \(n\) tensors and \(n+\varepsilon\) vectors from a principal tensor is the Killing-tower construction of Krtouš–Page–Frolov–Kubizňák, used here as an external lemma [Krtousetal2007].

\(\langle 1\rangle 3.\) QED.

A Mathlib-free Lean encoding of \(\langle 1\rangle 1\) is `killing_tower_count` in `lean/KillingTower.lean`.

**Lemma 3.2 (Spin count).** The number of independent MP spins is \(n=\lfloor(D-1)/2\rfloor\). In particular \(n(5)=2\), \(n(6)=2\), \(n(7)=3\).

*Lamport proof.*

\(\langle 1\rangle 1.\) If \(D=2k+1\) then \((D-1)/2=k\), so \(n=k\).

\(\langle 1\rangle 2.\) If \(D=2k\) with \(k\ge 1\) then \((D-1)//2=k-1\).

\(\langle 1\rangle 3.\) \(D=5=2\cdot 2+1\) gives \(n=2\); \(D=6=2\cdot 3\) gives \(n=2\).

\(\langle 1\rangle 4.\) QED.

**Lemma 3.3 (Equal-spin measure).** For \(n\ge 2\) the equal-spin locus has codimension \(n-1\ge 1\) in spin space, hence measure zero in any absolutely continuous sampling measure (including Sobol on the unit cube).

*Lamport proof.*

\(\langle 1\rangle 1.\) \(\{a_1=\cdots=a_n\}\subset\mathbb{R}^n\) is a line, hence dimension \(1\).

\(\langle 1\rangle 2.\) Codimension \(n-1\ge 1\) since \(n\ge 2\) (which holds for all MP with \(D\ge 5\)).

\(\langle 1\rangle 3.\) A Sobol sequence that samples the full cube almost surely misses a measure-zero submanifold; isolation of equal-spin points requires a *forced* design (v1’s “Cube Design”), whose sample size v1 never reported.

\(\langle 1\rangle 4.\) QED.

### 3.2 Logical independence on the MP family

Let \(A\) be the property “CMPP Type D,” \(B\) the property “admits a principal CKY 2-form (hence completely integrable geodesic flow),” \(C\) the property “linearly stable to gravitational perturbations about the outer horizon,” and \(D_{\mathrm{cc}}\) the property “the spacetime is a black hole obeying weak cosmic censorship (no naked singularity visible from infinity).”

**Proposition 3.4 (Pairwise independence on and around MP).** The four properties \(A,B,C,D_{\mathrm{cc}}\) are not mutually equivalent. In particular the implications \(B\Rightarrow C\), \(B\Rightarrow D_{\mathrm{cc}}\), \(A\Rightarrow D_{\mathrm{cc}}\), and \(A\Rightarrow B\) (in \(D\ge 5\)) are not theorems.

*Lamport proof.*

\(\langle 1\rangle 1.\) \(A\wedge B\) holds for every subextremal Myers–Perry metric.

  \(\langle 2\rangle 1.\) MP admits a principal CKY 2-form [FrolovKubiznak2007]. That is \(B\).

  \(\langle 2\rangle 2.\) A principal CKY 2-form implies CMPP Type D [HouriOotaYasui, SantosKYReview]. That is \(A\).

  \(\langle 2\rangle 3.\) QED.

\(\langle 1\rangle 2.\) \(B\not\Rightarrow C\).

  \(\langle 2\rangle 1.\) Geodesic integrability (\(B\)) holds for all MP parameters for which the metric is defined, including the ultraspinning regime \(D\ge 6\).

  \(\langle 2\rangle 2.\) Ultraspinning MP black holes are linearly unstable [EmparanMyers2003, Diasetal2010, DiasFiguerasMonteiroSantos2010JHEP]. Equal-spin \(D=9\) in particular has exponentially growing modes.

  \(\langle 2\rangle 3.\) Therefore there exist MP spacetimes with \(B\wedge \neg C\).

  \(\langle 2\rangle 4.\) QED.

\(\langle 1\rangle 3.\) \(B\not\Rightarrow D_{\mathrm{cc}}\) and \(A\not\Rightarrow D_{\mathrm{cc}}\).

  \(\langle 2\rangle 1.\) Super-extremal Kerr (\(D=4\)) and super-extremal MP (\(D=5\), beyond the Kerr-like bound) remain Type D and admit the same principal tensor (the metric functions are the same analytic expressions). That is \(A\wedge B\).

  \(\langle 2\rangle 2.\) Those geometries have naked singularities. That is \(\neg D_{\mathrm{cc}}\).

  \(\langle 2\rangle 3.\) QED.

\(\langle 1\rangle 4.\) \(A\Rightarrow B\) is not a theorem in \(D\ge 5\).

  \(\langle 2\rangle 1.\) In \(D=4\), vacuum Type D is Kerr–NUT, which does admit a principal CKY.

  \(\langle 2\rangle 2.\) In \(D\ge 5\) the converse “Type D \(\Rightarrow\) principal CKY” is explicitly open [SantosKYReview, § on converse]. v1 used the converse silently whenever it treated “Weyl Type D deviation” as a proxy for KY breakdown.

  \(\langle 2\rangle 3.\) QED.

\(\langle 1\rangle 5.\) Therefore v1’s chain “EFT lifts Type D \(\Rightarrow\) KY dies \(\Rightarrow\) integrability dies \(\Rightarrow\) naked singularities, faster than GR” contains three non-implications.

\(\langle 1\rangle 6.\) QED.

**Corollary 3.5.** Algebraic “fragility” is not a censorship theorem and is not a stability theorem.

### 3.3 Equal-spin protection is classical isometry, not semiclassical magic

**Lemma 3.6 (Quadrature from cohomogeneity one).** Let \((M,g)\) be a Lorentzian manifold of cohomogeneity one, with compact spacelike orbits of a group \(G\) acting by isometries, and with orbit space diffeomorphic to an interval in the radial coordinate \(r\). Then geodesic motion reduces to quadrature in \(r\) after using the conserved charges of \(G\), without any principal CKY tensor.

*Lamport proof.*

\(\langle 1\rangle 1.\) Isometries yield \(\dim G\) linear conserved momenta \(p_G\).

\(\langle 1\rangle 2.\) The metric depends on a single coordinate \(r\). The Hamiltonian constraint \(g^{\mu\nu}p_\mu p_\nu=-m^2\) therefore becomes a first-order ODE \(\dot r^2 = V_{\mathrm{eff}}(r; p_G, m)\).

\(\langle 1\rangle 3.\) A first-order autonomous ODE in one variable is solvable by quadrature.

\(\langle 1\rangle 4.\) No CKY equation entered \(\langle 1\rangle 1\)–\(\langle 1\rangle 3\).

\(\langle 1\rangle 5.\) QED.

**Lemma 3.7 (Odd-\(D\) equal-spin MP is cohomogeneity one).** For \(D=2n+1\) with \(a_1=\cdots=a_n\), MP has cohomogeneity one. Hence Lemma 3.6 applies *already at EFT coupling \(\alpha=0\)*.

*Lamport proof.*

\(\langle 1\rangle 1.\) The isometry is enhanced to \(\mathbb{R}_t\times U(n)\) [GibbonsLuPagePope2004].

\(\langle 1\rangle 2.\) The metric functions depend only on \(r\).

\(\langle 1\rangle 3.\) QED.

**Lemma 3.8 (No \(\hbar\) in the quadratic action).** Definition 2.7’s action does not contain \(\hbar\). Any protection that follows from \(G\)-invariance of a deformation of that action is classical.

*Lamport proof.*

\(\langle 1\rangle 1.\) Inspect \(S[g]\): the symbols are \(g_{\mu\nu}\), \(R_{\mu\nu\rho\sigma}\), and Wilson coefficients \(\alpha_{\mathrm{GB}},\alpha_{\mathrm{W}}\).

\(\langle 1\rangle 2.\) \(\hbar\) is not among them. Loop factors would appear as an expansion in \(\hbar G_D \Lambda^{D-2}\), which v1 never wrote.

\(\langle 1\rangle 3.\) QED.

**Proposition 3.9 (What equal-spin protection actually is).** Let \(g(\alpha)=g_{\mathrm{MP}}+\alpha\,\delta g+O(\alpha^2)\) be a deformation that *preserves* the enhanced equal-spin isometry \(G=\mathbb{R}_t\times U(n)\) in odd \(D\). Then:

1. \(g(\alpha)\) remains cohomogeneity one, so geodesic quadrature (Lemma 3.6) persists to this order, *whether or not* a principal CKY tensor persists.
2. Weyl components transforming in nontrivial representations of \(G\) are forbidden. This is exact vanishing, not a factor \(10^{-6}\).
3. The CKY equation \(\mathcal{R}(h;g(\alpha))=0\) is a separate PDE. \(G\)-invariance does not imply \(\mathcal{R}=0\).
4. None of (1)–(3) is semiclassical.

*Lamport proof.*

\(\langle 1\rangle 1.\) Statement (1). If \(\mathcal{L}_K g(\alpha)=0\) for all Killing fields \(K\) of \(G\), the orbit-space dimension is unchanged, so Lemma 3.6 applies to \(g(\alpha)\). Persistence of quadrature is therefore cheaper than persistence of \(h\). v1’s “deformed Killing–Yano tensor remains nearly invariant” is a stronger claim that was not proved and is not proved here.

\(\langle 1\rangle 2.\) Statement (2). Decompose the Weyl tensor into \(G\)-irreps. A \(G\)-invariant metric has Weyl tensor in the singlet. Non-singlet boost-weight components vanish identically, not up to \(10^{-6}\). A reported \(10^6\) suppression is therefore either (i) a numerical floor of an unspecified residual, or (ii) evidence that the configuration was *not* exactly equal-spin. Neither is a physical protection factor \(P(D)\).

\(\langle 1\rangle 3.\) Statement (3). The CKY equation is overdetermined. Imposing isometry reduces the number of unknown functions; it does not satisfy the remaining radial ODE automatically. (Existence of a principal tensor on *undeformed* MP uses the specific MP radial functions, not merely cohomogeneity one.)

\(\langle 1\rangle 4.\) Statement (4) is Lemma 3.8.

\(\langle 1\rangle 5.\) QED.

**Corollary 3.10 (The integrability gap is already classical).** The gap between equal-spin and generic MP geodesic integrability exists at \(\alpha=0\): generic MP needs the hidden CKY tower (Lemma 3.1), equal-spin odd-\(D\) MP does not (Lemma 3.6). Observing that gap after “turning on \(R^2\)” does not demonstrate a quantum mechanism.

**Remark 3.11 (Even \(D\)).** v1 treated \(D=6,8\) as cohomogeneity-1 equal-spin sectors. They are not the odd-\(D\) \(U(n)\) story. Any equal-spin statement in even \(D\) must be proved separately. This paper does not claim it.

### 3.4 Love numbers are not quantum hair and are not faithful KY tracers

**Lemma 3.12 (Classical nonvanishing in \(D\ge 5\)).** There exist classical, \(\alpha=0\), five-dimensional MP black holes whose static scalar Love numbers are nonzero [CharalambousIvanov2023]. Hence “\(R^2\) corrections activate \(k_2\) in \(D\ge 5\)” is false as a discovery.

*Lamport proof.*

\(\langle 1\rangle 1.\) External lemma: Charalambous–Ivanov, JHEP 07 (2023) 222, extract static scalar Love numbers of 5D MP. They are generically nonzero and run logarithmically.

\(\langle 1\rangle 2.\) That computation is classical GR (\(\alpha=0\)).

\(\langle 1\rangle 3.\) Therefore a nonzero \(k_2\) in \(D\ge 5\) is the GR baseline, not an EFT activation, and not \(\hbar\)-hair.

\(\langle 1\rangle 4.\) QED.

**Lemma 3.13 (Magic zeroes break faithfulness).** There exist resonant conditions under which those Love numbers vanish (“magic zeroes”) without restoration of a lost principal tensor in an EFT deformation. Therefore \(k_2=0\) is not equivalent to “KY intact,” and \(k_2\neq 0\) is not equivalent to “KY broken.”

*Lamport proof.*

\(\langle 1\rangle 1.\) Magic zeroes are documented in the same 5D MP analysis [CharalambousIvanov2023] and in higher-D Schwarzschild-Tangherlini at integer \(\ell/(D-3)\).

\(\langle 1\rangle 2.\) Those zeroes are explained by near-zone \(\mathfrak{sl}(2,\mathbb{R})\) truncated symmetries, which are not the principal CKY 2-form (different algebraic object, different domain: near-zone wave equation versus spacetime 2-form).

\(\langle 1\rangle 3.\) A map that sends both “KY intact, non-resonant” and “KY broken, resonant” to overlapping \(k_2\) values cannot be an isomorphism onto “quantum hair.”

\(\langle 1\rangle 4.\) QED.

**Lemma 3.14 (Category error: Love symmetry versus KY).** The near-zone Love algebra \(\mathfrak{sl}(2,\mathbb{R})\) of Charalambous–Ivanov and the principal CKY 2-form of Frolov–Kubizňák are distinct structures. Citations of [CharalambousIvanov2023] cannot underwrite a KY–Love identity.

*Lamport proof.* Immediate from the definitions (2.4 versus 2.9) and from Lemma 3.13 \(\langle 1\rangle 2\).

**Proposition 3.15 (v1’s \(\rho=0.998\) cannot be a discovery).** Let a pipeline (i) generate labels from an unspecified function \(L\), (ii) discard samples with Pearson \(|\rho|<\tau\) for \(\tau=0.70\), and (iii) report \(\rho=0.998\) between \(\log|k_2|\) and \(\log|W|\). Then the reported \(\rho\) is not an independent test of a KY–Love law.

*Lamport proof.*

\(\langle 1\rangle 1.\) Selection. Conditioning on \(|\rho|\ge\tau\) is Berkson/collider selection. The reported coefficient is a random variable on the selected set, not on the design. (Executable analogue: stress test T04.)

\(\langle 1\rangle 2.\) Tautology. If \(L\) computes \(k_2\) as a monotone function of the same residual that defines \(W\), then \(\rho\approx 1\) by construction. v1’s Label Engine is unspecified, so this alternative is not ruled out. Independent noise at the claimed \(N\) cannot produce \(|\rho|=0.998\) (T50).

\(\langle 1\rangle 3.\) Domain. \(\log_{10}W\) is undefined for \(W\le 0\) (T06). Any implementation thresholded or took an absolute value; that choice is an unregistered degree of freedom.

\(\langle 1\rangle 4.\) Tool. The named engine `qnm` cannot emit \(k_2\) or \(W\) (Lemma 3.16). The correlation was therefore not computed from the named tool.

\(\langle 1\rangle 5.\) Physics. Even a genuine correlation would not identify \(k_2\) as quantum hair (Definition 2.10, Lemma 3.12) nor as a faithful KY tracer (Lemma 3.13).

\(\langle 1\rangle 6.\) QED.

**Lemma 3.16 (`qnm` inapplicability).** Stein’s Python package `qnm` [Stein2019] computes Kerr QNM frequencies labeled by \((s,\ell,m,n;a)\) in \(D=4\). It does not accept a dimension \(D\), a spin vector \((a_i)\), a CKY trial 2-form, or a Love-number matching condition.

*Lamport proof.*

\(\langle 1\rangle 1.\) External lemma: the package documentation and JOSS paper (correct pagination 1683, not v1’s 1692).

\(\langle 1\rangle 2.\) The input alphabet \(\{s,\ell,m,n,a\}\) is disjoint from \(\{D,h_{\mu\nu},k_2,a_i\}\).

\(\langle 1\rangle 3.\) QED.

### 3.5 EFT, ghosts, thermodynamics, and singularities

**Lemma 3.17 (Field-redefinition redundancy).** On an Einstein background, Ricci-squared operators in the quadratic action can be removed by a metric field redefinition at leading order in \(\alpha\). A pipeline that “turns on \(R^2\)” without specifying Gauss–Bonnet versus Weyl-squared versus redundant Ricci-squared has not specified an EFT.

*Lamport proof.* Standard vacuum EFT of GR [EndlichGoldbergerMcLerranNicolis, ReallSantos2019, CanoRuiperez2019]. In \(D=4\), Gauss–Bonnet is topological. In \(D\ge 5\), Gauss–Bonnet is the leading Lovelock term and *is* dynamical. QED.

**Lemma 3.18 (Ostrogradsky).** A generic \(R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}\) term without Lovelock structure or reduction of order yields a fourth-order equation with extra ghost modes. An observed “fragility” of such a system may be an artifact of those modes.

*Lamport proof.* Ostrogradsky’s theorem on nondegenerate higher-derivative Lagrangians; Lovelock’s theorem that Gauss–Bonnet is second-order. QED.

**Lemma 3.19 (Reall–Santos does not give KY residuals).** The Reall–Santos method computes first-order corrections to black-hole thermodynamics from the Euclidean action *without* constructing \(\delta g_{\mu\nu}\) [ReallSantos2019]. The CKY residual \(\mathcal{R}(h;g)\) and CMPP boost-weight norms are tensors constructed from \(g\). Therefore RS output cannot be the Label Engine of v1.

*Lamport proof.* Immediate from the objects’ index structure. QED.

**Lemma 3.20 (Truncated EFT does not resolve \(r=0\).** A finite-order curvature expansion is an infrared expansion about a GR solution. It is not a UV completion and does not replace the curvature singularity of MP by a regular core.

*Lamport proof.*

\(\langle 1\rangle 1.\) By definition of a truncated EFT, operators of dimension \(> N\) are omitted.

\(\langle 1\rangle 2.\) Near a curvature singularity, curvature invariants diverge, so omitted operators are not small (Definition 2.8 fails).

\(\langle 1\rangle 3.\) Therefore the truncation cannot be used *at* the singularity, and cannot be said to resolve it.

\(\langle 1\rangle 4.\) Nonperturbative RG improvement (Bonanno–Reuter and descendants) is a *different* theory, not a theorem of the \(R^2\) truncation. v1’s conclusion that “perturbative truncations are insufficient for singularity resolution” is a tautology of Definition 2.7, not a numerical discovery.

\(\langle 1\rangle 5.\) QED.

**Proposition 3.21 (Accelerated fragility is not a defined estimator).** There is no unique coefficient \(\gamma_2\) until one specifies a response \(Y\), a spin coordinate \(x\), a model \(Y=\beta_0+\beta_1 x+\gamma_2 x^2+\varepsilon\), an error law, a domain (subextremal, EFT-valid), and a sample. v1 specified none of these. The number \(-0.163\) is quarantined. Moreover, even after a definition, a negative \(\gamma_2\) near extremality is confounded by EFT breakdown (Definition 2.8).

*Lamport proof.* Combine the missing-model observation with Definition 2.8 and Lemma 3.20. QED.

**Proposition 3.22 (Rigidification was never a hypothesis).** A hypothesis that is neither cited nor formalized cannot be rejected at \(\gamma_2=-0.163\). Any future “quantum rigidification” claim must specify: which theory (\(\hbar\) loops, RG-improved metric, GUP, string \(\alpha'\), …), which observable (threshold spin for GL, \(\delta M_{\mathrm{ext}}\), QNM drift, …), and which sign is “rigid.”

*Lamport proof.* Immediate. QED.

### 3.6 What a valid computational pipeline would have to be

**Proposition 3.23 (Minimal valid pipeline).** A computational study entitled to report KY residuals and Love numbers of EFT-corrected MP must, at minimum:

1. Freeze, hash, and date an operator basis (Definition 2.7) and a reduction-of-order or Lovelock treatment (Lemma 3.18).
2. Sample \(D\) as an integer, sample dimensionless spins on the *subextremal black-hole* domain, and *force* the equal-spin locus as a separate stratum whose \(N_{\mathrm{eq}}\) is reported (Lemma 3.3).
3. Construct \(g(\alpha)\) (or prove that the observable is metric-independent, which KY residuals are not: Lemma 3.19).
4. Define \(\mathcal{R}(h;g)\) (Definition 2.5) and a CMPP-frame Weyl deviation, including the absolute-value/threshold convention for any logarithm.
5. Compute Love numbers of a named spin, parity, and matching scheme, at a named scale if they run (Definition 2.9).
6. Not filter on the headline correlation (Proposition 3.15).
7. Not call Stein `qnm` (Lemma 3.16).
8. Report EFT-validity diagnostics \(|\alpha\,\mathrm{Riem}|\) (Definition 2.8).
9. Deposit code, seeds, and data with a real DOI.

v1 satisfied none of (1)–(9). This paper does not pretend that (1)–(9) have been executed.

*Lamport proof.* Each item is the negation of a v1 failure already proved. QED.

---

## 4. Fifty stress tests of the repaired paper

The repaired claims were stress-tested in fifty mutually distinct ways. The tests are de-duplicated by name and by scientific target: citation identity, dimensional analysis, statistical selection, algebraic counting, EFT structure, Love-number category errors, and pipeline impossibility. They are *not* fifty resamplings of one Monte Carlo.

Implementation: `docs/papers/mpp-integrability/scripts/stress50.py`. Result on this revision: **50/50 passed**.

| ID | Distinct target | Repaired claim under test |
| --- | --- | --- |
| T01 | Bibliographic identity | JHEP 11 (2022) 161 is Aalsma–Shiu, not Cano |
| T02 | Bibliographic pagination | Stein JOSS page is 1683, not 1692 |
| T03 | Internal consistency | \(N=10^5\) and \(N=5\times 10^4\) cannot coexist |
| T04 | Selection bias | A \(\rho\)-Gate changes the reported Pearson statistic |
| T05 | Estimator bound | \(|\rho|\le 1\) |
| T06 | Domain of \(\log_{10}\) | \(\log_{10}W\) is undefined for \(W\le 0\) |
| T07 | Extremality language | \(D=5\) is not ultraspinning |
| T08 | Ultraspinning onset | Emparan–Myers onset is \(D\ge 6\) |
| T09 | Odd-\(D\) cohomogeneity | Generic cohomogeneity of \(D=5,7,9\) is \(2,3,4\) |
| T10 | Even-\(D\) cohomogeneity | Even \(D\) is not the odd-\(D\) cohomogeneity-1 story |
| T11 | Killing-tower count | \(n+(n+\varepsilon)=D\) |
| T12 | Open converse | Type D \(\Rightarrow\) CKY is not a \(D\ge 5\) theorem |
| T13 | Independence \(B\not\Rightarrow C\) | Integrable MP can be linearly unstable |
| T14 | Tool scope | `qnm` inputs are disjoint from KY/\(k_2\)/\(D\) |
| T15 | Field redefinitions | Ricci-squared is not an independent vacuum operator |
| T16 | Gauss–Bonnet | Topological in \(D=4\), dynamical in \(D\ge 5\) |
| T17 | No \(\hbar\) | Quadratic action is classical |
| T18 | GR baseline Love | 5D MP \(k_\ell\) generically nonzero in GR |
| T19 | Terminology | Quantum hair \(\neq\) tidal \(k_2\) |
| T20 | Algebra identity | \(\mathfrak{sl}(2,\mathbb{R})\neq\) principal CKY |
| T21 | Design vs PDE | Sobol tuples are not EFT metrics |
| T22 | Circular UQ | Bootstrap of planted labels recovers the planting |
| T23 | \(r\) vs Spearman | Pearson \(\neq\) Spearman on cubic data |
| T24 | Forking paths | Six named blocks are degrees of freedom |
| T25 | Units | \(\Lambda_{\mathrm{QG}}\in[0,0.1]\) has no units in v1 |
| T26 | EFT control | \(|\alpha R|\ll 1\) can fail at large curvature |
| T27 | Ghosts | Generic \(Riem^2\) vs second-order GB |
| T28 | Allowed methods | v1’s method is not in \(\{\)reduce order, RS, perturbative metric\(\}\) |
| T29 | Horizon taxonomy | Inner Cauchy \(\neq\) outer event horizon \(\neq\) naked singularity |
| T30 | Type vs censorship | CMPP Type I is not a naked singularity |
| T31 | Spin of the tidal field | Scalar \(s=0\) \(\neq\) gravitational \(s=2\) |
| T32 | Static vs dynamical | Conservative \(\neq\) dissipative response |
| T33 | Gauge | v1 states no matching scheme |
| T34 | Running | Generic 5D MP Love numbers run |
| T35 | Magic zeroes | Resonant vanishing is not \(P(D)\sim 10^6\) |
| T36 | Incomplete power law | \(\alpha_W\) and intercept absent |
| T37 | Duplicate figures | Figure 1A and Figure 2 both claim \(P(D)\) |
| T38 | Token clash | Caption \(r\) versus text \(\rho\) |
| T39 | No invented slope | This revision does not fabricate \(\alpha_W\) |
| T40 | Undefined \(\beta_a\) | Figure 1C coefficient has no formula |
| T41 | Fake preregistration | Unhashed `nuances.yml` is not a freeze |
| T42 | Fake DOI | A DOI that is not an identifier is not a DOI |
| T43 | Provenance | A Kosmos URL is not an EFT solution |
| T44 | Implementation detail | `joblib` is not a KY solver |
| T45 | Uncited hypothesis | “Quantum rigidification” has no v1 reference |
| T46 | Tautology | Truncated EFT does not resolve \(r=0\) |
| T47 | Exact vs \(10^{-6}\) | A \(10^6\) factor is not derived from a KY PDE |
| T48 | Measure zero | Equal-spin locus has codimension \(n-1\ge 1\) |
| T49 | Two designs | Sobol harvest \(\neq\) stratified equal-spin cube |
| T50 | Planting bound | Independent noise cannot produce \(\lvert\rho\rvert=0.998\) at the claimed \(N\) |

These tests can fail the *revision* if a later draft reintroduces a quarantined number, calls `qnm` a KY solver, or identifies Type D with censorship. They cannot pass a draft that restores v1’s headlines.

---

## 5. Before and after

A compact ledger is `BEFORE-AFTER.md`. The state change, in one page:

**Before (v1).** A five-page AI-assisted note asserted that equal-spin MP black holes are semiclassically protected by a factor \(10^6\), that generic MP is algebraically fragile under \(R^2\) with \(\gamma_2=-0.163\), and that Love numbers are quantum hair tracking KY breakdown at \(\rho=0.998\). The method named a 4D Kerr QNM package, a missing YAML pre-registration, a missing DOI, a Sobol sample whose size disagrees with itself, and a Gate that selected the headline correlation. Three figures had captions and no data. Citations included a wrong author for JHEP 11 (2022) 161, a wrong JOSS page, unresolved 2024–2025 keys, and leftover `[cite: N]` tokens. Four inequivalent geometric properties were treated as one. “Quantum” meant a classical quadratic action.

**After (this paper).** The numbers are quarantined and not replaced. The geometric objects are defined. The surviving theorems are: Killing-tower cardinality; spin counts; measure-zero equal-spin locus; pairwise independence of Type D, CKY integrability, linear stability, and censorship; cohomogeneity-1 quadrature without CKY; \(\hbar\)-independence of quadratic EFT; exact (not \(10^{-6}\)) singlet projection under enhanced isometry; classical nonvanishing and non-faithfulness of \(D\ge 5\) Love numbers; `qnm` inapplicability; RS/metric mismatch; Ostrogradsky and field-redefinition constraints; truncated-EFT tautology on singularity resolution; and a minimal valid pipeline that v1 did not run. Fifty distinct stress tests of those repaired claims pass. The bibliography is corrected. The author-footnote LLM list is moved to acknowledgments, where it belongs.

Nothing in the after-state is a new measurement of a black hole.

---

## 6. Conclusion

The draft’s scientific content, once the pipeline theater is stripped, is a cluster of identifications that do not hold: quantum with quadratic EFT, Type D with principal CKY, integrability with stability, stability with censorship, Love numbers with quantum hair, near-zone \(\mathfrak{sl}(2,\mathbb{R})\) with a spacetime 2-form, Sobol sampling with solving field equations, and a selected Pearson coefficient with a discovery. The one geometric fact that *does* hold, and that v1 was pointing at, is elementary: odd-dimensional equal-spin Myers–Perry is cohomogeneity one, so explicit isometry already gives geodesic quadrature, while generic MP needs the hidden Killing tower. That gap is classical. It does not require a factor \(10^6\), a Kosmos trajectory, or a Love-number oracle.

A subsequent empirical paper is possible, but only along the pipeline of Proposition 3.23. Until that pipeline exists, the correct report is the one given here.

---

## Acknowledgments

GPT-5.2 (OpenAI), AI Studio (Google), and Kosmos AI (Edison Scientific) assisted v1. They are not sources of KY residuals, Love numbers, or confidence intervals. The Kosmos trajectory cited in v1 remains a chat log, not a dataset. This revision was written to make that distinction impossible to miss.

---

## References

[MyersPerry1986] R. C. Myers and M. J. Perry, *Black holes in higher dimensional space-times,* Ann. Phys. **172**, 304 (1986).

[EmparanMyers2003] R. Emparan and R. C. Myers, *Instability of ultra-spinning black holes,* JHEP **03**, 025 (2003).

[Coleyetal2004] A. Coley, R. Milson, V. Pravda, and A. Pravdová, *Classification of the Weyl tensor in higher dimensions,* Class. Quant. Grav. **21**, L35 (2004); see also Class. Quant. Grav. **21**, 3181 (2004).

[GibbonsLuPagePope2004] G. W. Gibbons, H. Lü, D. N. Page, and C. N. Pope, *The general Kerr–de Sitter metrics in all dimensions,* J. Geom. Phys. **53**, 49 (2005), hep-th/0404008.

[FrolovKubiznak2007] V. P. Frolov and D. Kubizňák, *Hidden symmetries of higher-dimensional rotating black holes,* Phys. Rev. Lett. **98**, 011101 (2007).

[Krtousetal2007] P. Krtouš, D. Kubizňák, D. N. Page, and V. P. Frolov, *Killing–Yano tensors, rank-2 Killing tensors, and conserved quantities in higher dimensions,* JHEP **02**, 004 (2007).

[FrolovKrtousKubiznak2017] V. P. Frolov, P. Krtouš, and D. Kubizňák, *Black holes, hidden symmetries, and complete integrability,* Living Rev. Relativ. **20**, 6 (2017).

[Diasetal2010] O. J. C. Dias, P. Figueras, R. Monteiro, J. E. Santos, and R. Emparan, *An instability of higher-dimensional rotating black holes,* JHEP **05**, 076 (2010).

[DiasFiguerasMonteiroSantos2010] O. J. C. Dias, P. Figueras, R. Monteiro, and J. E. Santos, *Ultraspinning instability of rotating black holes,* Phys. Rev. D **82**, 104025 (2010).

[ReallSantos2019] H. S. Reall and J. E. Santos, *Higher derivative corrections to Kerr black hole thermodynamics,* JHEP **04**, 021 (2019).

[CanoRuiperez2019] P. A. Cano and A. Ruipérez, *Leading higher-derivative corrections to Kerr geometry,* JHEP **05**, 189 (2019) [erratum JHEP **03**, 187 (2020)].

[AalsmaShiu2022] L. Aalsma and G. Shiu, *From rotating to charged black holes and back again,* JHEP **11**, 161 (2022). *(This is v1’s “[4]”; it is not a Cano paper.)*

[Stein2019] L. C. Stein, *qnm: A Python package for calculating Kerr quasinormal modes, separation constants, and spherical-spheroidal mixing coefficients,* J. Open Source Softw. **4**, 1683 (2019).

[CharalambousIvanov2023] P. Charalambous and M. M. Ivanov, *Scalar Love numbers and Love symmetries of 5-dimensional Myers–Perry black holes,* JHEP **07**, 222 (2023).

[Huietal2021] L. Hui, A. Joyce, R. Penco, L. Santoni, and A. R. Solomon, *Static response and Love numbers of Schwarzschild black holes,* JCAP **04**, 052 (2021).

[KehagiasRiotto2023] A. Kehagias and A. Riotto, related 4D Love-symmetry notes, JCAP **01**, 035 (2023). Used in v1 as if it licensed \(D\ge 5\) vanishing; it does not.

[Barbosaetal2025] S. Barbosa, P. Brax, S. Fichet, and L. de Souza, *Running Love numbers and the Effective Field Theory of gravity,* JCAP **07**, 071 (2025).

[WuLu2025] P.-Y. Wu and H. Lü, *Quadratic curvature correction and its breakdown to thermodynamics of rotating black holes,* Phys. Rev. D **111**, 104026 (2025).

[Chichetal2026] *Quadratic curvature correction to 5D Myers–Perry metric,* JHEP **05**, 081 (2026).

[SantosKYReview] See Frolov–Krtouš–Kubizňák (2017) and the discussion therein of the open converse Type D \(\Rightarrow\) principal tensor in \(D\ge 5\).
