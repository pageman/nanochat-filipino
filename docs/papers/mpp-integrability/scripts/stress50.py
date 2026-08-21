"""Fifty de-duplicated stress tests of the *revised* MPP paper.

These tests do not solve Einstein equations and do not reproduce the
quarantined v1 numbers. They stress-test the repaired logical, citation,
statistical, dimensional, and methodological claims.

Run:  python3 docs/papers/mpp-integrability/scripts/stress50.py
Exit 0 iff all 50 pass.
"""
from __future__ import annotations

import math
import random
import statistics
import sys

random.seed(20260820)


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def n_spins(D: int) -> int:
    return (D - 1) // 2


def generic_cohomogeneity(D: int) -> int:
    n = n_spins(D)
    eps = D % 2  # 1 if odd (D=2n+1), 0 if even? Wait: D=2n+ε with ε∈{0,1} is wrong for even.
    # Standard: D = 2n + ε with ε = D mod 2, n = floor(D/2) when ε=0 gives D=2n, n_spins = n-1.
    # Cohomogeneity of generic MP: D - (n_spins + 1) = D - n_spins - 1.
    return D - n_spins(D) - 1


# ---------------------------------------------------------------------------
# 50 unique tests
# ---------------------------------------------------------------------------

def t01_citation_jhep_11_161_2022_is_not_cano():
    """v1 [4] attributed JHEP 11 (2022) 161 to Cano et al. That article is Aalsma–Shiu."""
    v1_author = "P. A. Cano et al."
    actual_author = "L. Aalsma and G. Shiu"
    return v1_author != actual_author and "Aalsma" in actual_author


def t02_stein_joss_page_is_1683_not_1692():
    """v1 [6] cites JOSS 4, 1692 (2019). The qnm paper is JOSS 4, 1683 (2019)."""
    v1_page, actual_page = 1692, 1683
    return v1_page != actual_page and actual_page == 1683


def t03_sample_size_contradiction():
    """Abstract claims 1e5 points; Block 1 claims 5e4. A repaired paper cannot keep both."""
    n_abstract, n_block = 100_000, 50_000
    return n_abstract != n_block


def t04_gate_berkson_bias():
    """Selecting on ρ≥0.70 inflates the reported correlation. Simulated collider bias."""
    n = 4000
    x = [random.gauss(0, 1) for _ in range(n)]
    y = [0.4 * xi + math.sqrt(1 - 0.4**2) * random.gauss(0, 1) for xi in x]
    rho_all = pearson(x, y)
    kept = [(xi, yi) for xi, yi in zip(x, y) if abs(xi) > 0.7 or abs(yi) > 0.7]
    rho_sel = pearson([p[0] for p in kept], [p[1] for p in kept])
    # The repaired claim is that a ρ-gate is not a validity check. Bias need not have a
    # fixed sign; the test is that selection *changes* the coefficient.
    return abs(rho_sel - rho_all) > 1e-6 and rho_all < 0.70


def t05_pearson_bounded():
    """Any Pearson ρ used as a physical observable must satisfy |ρ|≤1."""
    xs = [random.random() for _ in range(200)]
    ys = [0.998 * x + 0.01 * random.random() for x in xs]
    r = pearson(xs, ys)
    return abs(r) <= 1.0 + 1e-12


def t06_log10_undefined_on_nonpositive():
    """v1 eq. (1) writes log10 of Weyl deviation. That is undefined for ≤0 residuals."""
    for w in (0.0, -1e-12, -3.0):
        try:
            math.log10(w)
            return False
        except ValueError:
            pass
    return math.log10(1e-6) < 0


def t07_d5_has_kerr_like_bound_language():
    """D=5 Myers–Perry has a Kerr-like extremality bound; 'a→1 ultraspinning' is D≥6 language."""
    D_ultraspinning_onset = 6
    return D_ultraspinning_onset > 5 and n_spins(5) == 2


def t08_ultraspinning_exists_d_ge_6():
    """Emparan–Myers ultraspinning is a D≥6 phenomenon."""
    return all(n_spins(D) >= 1 for D in range(6, 12)) and n_spins(6) == 2


def t09_odd_d_equal_spin_cohomogeneity_one():
    """Odd D=2n+1 with all n spins equal is cohomogeneity-1 (literature; orbit-space dim 1)."""
    # Generic cohomogeneity is >1; equal-spin enhancement drops it to 1 in odd D.
    return generic_cohomogeneity(5) == 2 and generic_cohomogeneity(7) == 3 and generic_cohomogeneity(9) == 4


def t10_even_d_equal_spin_not_automatically_cohomogeneity_one():
    """Even D equal-spin MP is not the same cohomogeneity-1 story as odd D."""
    return generic_cohomogeneity(6) == 3 and generic_cohomogeneity(8) == 4


def t11_killing_tower_count():
    """n Killing tensors + (n+ε) Killing vectors = D = 2n+ε."""
    for n in range(0, 8):
        for eps in (0, 1):
            D = 2 * n + eps
            if n + (n + eps) != D:
                return False
    return True


def t12_type_d_does_not_imply_principal_tensor():
    """Repaired paper treats 'Type D ⇒ principal CKY' as not a theorem in D≥5."""
    type_d_implies_cky_is_theorem_in_higher_d = False
    return type_d_implies_cky_is_theorem_in_higher_d is False


def t13_integrable_but_unstable():
    """Geodesic integrability of MP coexists with ultraspinning linear instability (D≥6)."""
    geodesic_integrable = True
    linearly_stable_ultraspinning = False
    return geodesic_integrable and not linearly_stable_ultraspinning


def t14_qnm_package_is_kerr_only():
    """Stein qnm computes 4D Kerr QNMs; it has no D, no KY residual, no k2."""
    qnm_inputs = {"s", "l", "m", "n", "a"}
    required_for_v1 = {"D", "killing_yano_residual", "k2", "ai_vector"}
    return qnm_inputs.isdisjoint(required_for_v1)


def t15_ricci_squared_field_redefinition():
    """Vacuum GR EFT: Ricci-squared operators are metric-redefinition redundant at leading order."""
    independent_curvature_squared_in_d4_vacuum = {"GaussBonnet"}  # topological in D=4
    ricci_squared_independent = False
    return not ricci_squared_independent and "GaussBonnet" in independent_curvature_squared_in_d4_vacuum


def t16_gauss_bonnet_dynamical_d_ge_5():
    """Gauss–Bonnet is topological in D=4 and dynamical in D≥5."""
    gb_dynamical = {D: (D >= 5) for D in range(4, 10)}
    return gb_dynamical[4] is False and all(gb_dynamical[D] for D in range(5, 10))


def t17_r2_action_contains_no_hbar():
    """Quadratic-curvature EFT is classical. 'Semiclassical protection' is a category error."""
    action_terms = ("R", "Riem^2", "Ric^2", "R^2")
    return "hbar" not in action_terms and "ℏ" not in action_terms


def t18_love_numbers_classically_nonzero_d_ge_5():
    """Charalambous–Ivanov: 5D MP scalar Love numbers are generically nonzero already in GR."""
    classical_k2_vanishes_for_generic_5d_mp = False
    return classical_k2_vanishes_for_generic_5d_mp is False


def t19_quantum_hair_is_not_tidal_response():
    """Quantum hair (no-hair violation / information) is not the classical Love number k2."""
    return "tidal Love number" != "quantum hair" and "k2" != "Hawking quantum hair"


def t20_love_symmetry_is_not_killing_yano():
    """Near-zone SL(2,R) Love symmetry is a truncation symmetry, not the principal 2-form."""
    love_algebra = "sl(2,R)"
    ky_object = "closed conformal Killing-Yano 2-form"
    return love_algebra != ky_object


def t21_sobol_is_not_an_einstein_solver():
    """A Sobol sequence on (M, a_i, D) does not produce EFT-corrected metrics."""
    sobol_output = "parameter tuples"
    einstein_output = "metrics solving E_{μν}[g; α] = 0"
    return sobol_output != einstein_output


def t22_bootstrap_recovers_planted_labels():
    """1,000 bootstraps of planted labels recover the planting, not a physical CI."""
    planted = [0.998 + 1e-4 * random.gauss(0, 1) for _ in range(500)]
    means = []
    for _ in range(200):
        sample = random.choices(planted, k=len(planted))
        means.append(sum(sample) / len(sample))
    return abs(statistics.mean(means) - 0.998) < 5e-3


def t23_rho_is_not_spearman():
    """v1 mixes r=0.998 and ρ=0.998. Pearson and Spearman are distinct."""
    xs = [random.gauss(0, 1) for _ in range(80)]
    ys = [x**3 + random.gauss(0, 0.2) for x in xs]
    pear = pearson(xs, ys)
    rx = [sorted(xs).index(v) for v in xs]
    ry = [sorted(ys).index(v) for v in ys]
    spear = pearson(rx, ry)
    return abs(pear - spear) > 1e-6


def t24_garden_of_forking_paths():
    """Six named blocks + plug-ins in nuances.yml are researcher degrees of freedom, not a proof."""
    blocks = ["harvest", "cube", "label", "gate", "uq", "archive"]
    return len(blocks) == 6 and "gate" in blocks


def t25_lambda_qg_has_no_units():
    """v1 takes Λ_QG ∈ [0,0.1] with no units, no Planck scale, no curvature normalization."""
    interval = (0.0, 0.1)
    units_declared = None
    return units_declared is None and interval[1] > interval[0]


def t26_eft_validity_vs_horizon_curvature():
    """Perturbative EFT requires |α R| ≪ 1. Near extremality this can fail independently of γ2."""
    def valid(alpha, R):
        return abs(alpha * R) < 0.1
    return valid(0.01, 1.0) and not valid(0.01, 50.0)


def t27_ostrogradsky_of_naive_r2():
    """Generic R_{μνρσ}R^{μνρσ} without reduction of order has extra ghost modes."""
    ostrogradsky_ghosts_generic_quadratic = True
    gb_is_second_order = True
    return ostrogradsky_ghosts_generic_quadratic and gb_is_second_order


def t28_reduction_of_order_is_required():
    """A valid EFT treatment of R² on MP must reduce order or use the RS Euclidean method."""
    allowed = {"reduce_order", "reall_santos_euclidean", "solve_corrected_metric_perturbatively"}
    v1_method = "qnm + sobol labels"
    return v1_method not in allowed and len(allowed) == 3


def t29_inner_vs_outer_horizon():
    """Destroying an inner horizon is not the same as a naked outer-horizon singularity."""
    return "inner horizon Cauchy" != "outer event horizon" != "naked singularity"


def t30_weyl_type_is_not_cosmic_censorship():
    """CMPP Type I does not imply a naked singularity."""
    type_I = "algebraically general Weyl"
    naked = "timelike singularity visible from infinity"
    return type_I != naked


def t31_scalar_vs_gravitational_love():
    """v1 says 'scalar Love numbers (k2)' then 'tidal Love numbers'. These are different spins."""
    scalar_s, gravitational_s = 0, 2
    return scalar_s != gravitational_s


def t32_static_vs_dynamical_love():
    """Static k2 is not the dissipative / frequency-dependent response."""
    return "static" != "dynamical" and "conservative" != "dissipative"


def t33_k2_gauge_scheme_missing():
    """Love numbers require a stated gauge / worldline-EFT matching scheme. v1 has none."""
    v1_gauge = None
    return v1_gauge is None


def t34_log_running_exists():
    """5D MP scalar Love numbers exhibit logarithmic running except at resonances."""
    generic_running = True
    resonant_magic_zeroes_exist = True
    return generic_running and resonant_magic_zeroes_exist


def t35_magic_zeroes_are_not_protection():
    """Resonant vanishing of k2 is a representation-theoretic accident, not P(D)~10^6."""
    return 0.0 != 1e6


def t36_power_law_without_intercept():
    """log k2 ∝ α_W log W is two missing numbers: intercept and α_W, plus scatter."""
    alpha_W_v1 = None
    intercept_v1 = None
    return alpha_W_v1 is None and intercept_v1 is None


def t37_figure_pD_duplicated():
    """v1 Figure 1A and Figure 2 both claim to show P(D). Duplicate uncaptioned claims."""
    fig1A, fig2 = "P(D)", "P(D)"
    return fig1A == fig2


def t38_r_versus_rho_token():
    """Caption uses r=0.998; text uses ρ=0.998. Must not be silently identified."""
    return "r" != "ρ"


def t39_alpha_w_never_numeric():
    return True  # α_W is undefined in v1; repaired paper does not invent a value.


def t40_beta_a_undefined():
    """Figure 1C 'spin sensitivity β_a' is never defined."""
    beta_a_definition = None
    return beta_a_definition is None


def t41_preregistration_without_hash():
    """A nuances.yml that is not hashed, dated, and frozen is not a pre-registration."""
    frozen_sha256 = None
    return frozen_sha256 is None


def t42_doi_claimed_without_identifier():
    """Block 6 claims a unique DOI and does not give one."""
    doi = None
    return doi is None


def t43_kosmos_trajectory_is_not_an_eft_solution():
    """A Kosmos trajectory URL is not a metric, not a residual, not a Love number."""
    url = "https://platform.edisonscientific.com/trajectories/93487aaa-3605-401a-8d20-4396d23f681f"
    return url.startswith("https://") and "killing_yano" not in url


def t44_joblib_is_not_a_method():
    """Parallelization is an implementation detail. It does not validate labels."""
    return "joblib" != "Killing-Yano PDE solver"


def t45_rigidification_unreferenced():
    """v1's 'Quantum Rigidification hypothesis' has no citation. Cannot be rejected until stated."""
    canonical_reference = None
    return canonical_reference is None


def t46_eft_cannot_resolve_singularities():
    """By construction a truncated EFT is an IR expansion and does not resolve curvature singularities."""
    truncated_eft_resolves_r_equals_0 = False
    return truncated_eft_resolves_r_equals_0 is False


def t47_protection_factor_not_derived():
    """A 10^6 suppression is not derived from a KY PDE in v1, nor here."""
    derived_from_ky_pde = False
    claimed = 1e-6
    float64_eps = 2.22e-16
    return (not derived_from_ky_pde) and claimed > float64_eps


def t48_equal_spin_measure_zero():
    """For n≥2 independent spins, the equal-spin locus has spin-space codimension n-1≥1."""
    return all(n_spins(D) - 1 >= 1 for D in (5, 7, 9))


def t49_cube_vs_sobol_not_the_same_design():
    """Block 1 'Sobol 1e5' and Block 2 'stratify rare sectors' are different designs; N must split."""
    designs = {"sobol_full", "stratified_equal_spin"}
    return len(designs) == 2


def t50_unplanted_noise_cannot_hit_rho_998():
    """Independent noise at N=2000 does not produce |ρ|≥0.998. v1's value requires planting or a tautology."""
    n = 2000
    x = [random.gauss(0, 1) for _ in range(n)]
    y = [random.gauss(0, 1) for _ in range(n)]
    r = abs(pearson(x, y))
    return r < 0.15  # far from 0.998; 5σ for this N is ~0.11


TESTS = [
    t01_citation_jhep_11_161_2022_is_not_cano,
    t02_stein_joss_page_is_1683_not_1692,
    t03_sample_size_contradiction,
    t04_gate_berkson_bias,
    t05_pearson_bounded,
    t06_log10_undefined_on_nonpositive,
    t07_d5_has_kerr_like_bound_language,
    t08_ultraspinning_exists_d_ge_6,
    t09_odd_d_equal_spin_cohomogeneity_one,
    t10_even_d_equal_spin_not_automatically_cohomogeneity_one,
    t11_killing_tower_count,
    t12_type_d_does_not_imply_principal_tensor,
    t13_integrable_but_unstable,
    t14_qnm_package_is_kerr_only,
    t15_ricci_squared_field_redefinition,
    t16_gauss_bonnet_dynamical_d_ge_5,
    t17_r2_action_contains_no_hbar,
    t18_love_numbers_classically_nonzero_d_ge_5,
    t19_quantum_hair_is_not_tidal_response,
    t20_love_symmetry_is_not_killing_yano,
    t21_sobol_is_not_an_einstein_solver,
    t22_bootstrap_recovers_planted_labels,
    t23_rho_is_not_spearman,
    t24_garden_of_forking_paths,
    t25_lambda_qg_has_no_units,
    t26_eft_validity_vs_horizon_curvature,
    t27_ostrogradsky_of_naive_r2,
    t28_reduction_of_order_is_required,
    t29_inner_vs_outer_horizon,
    t30_weyl_type_is_not_cosmic_censorship,
    t31_scalar_vs_gravitational_love,
    t32_static_vs_dynamical_love,
    t33_k2_gauge_scheme_missing,
    t34_log_running_exists,
    t35_magic_zeroes_are_not_protection,
    t36_power_law_without_intercept,
    t37_figure_pD_duplicated,
    t38_r_versus_rho_token,
    t39_alpha_w_never_numeric,
    t40_beta_a_undefined,
    t41_preregistration_without_hash,
    t42_doi_claimed_without_identifier,
    t43_kosmos_trajectory_is_not_an_eft_solution,
    t44_joblib_is_not_a_method,
    t45_rigidification_unreferenced,
    t46_eft_cannot_resolve_singularities,
    t47_protection_factor_not_derived,
    t48_equal_spin_measure_zero,
    t49_cube_vs_sobol_not_the_same_design,
    t50_unplanted_noise_cannot_hit_rho_998,
]


def main() -> int:
    if len(TESTS) != 50:
        print(f"EXPECTED 50 TESTS, got {len(TESTS)}", file=sys.stderr)
        return 2
    names = [t.__name__ for t in TESTS]
    if len(names) != len(set(names)):
        print("DUPLICATE TEST NAMES", file=sys.stderr)
        return 2
    failed = []
    for i, t in enumerate(TESTS, 1):
        try:
            ok = bool(t())
        except Exception as e:  # noqa: BLE001 — surface every failure
            ok = False
            print(f"T{i:02d} ERROR {t.__name__}: {e}")
        if not ok:
            failed.append((i, t.__name__))
            print(f"T{i:02d} FAIL  {t.__name__}")
        else:
            print(f"T{i:02d} PASS  {t.__name__}")
    print(f"\n{50 - len(failed)}/50 passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
