#!/usr/bin/env python3
"""Reconstruct the two synthetic MPP CSVs from Kosmos-published margins.

These are NOT the original Edison/Kosmos bytes. The original files were never
checked into this repo. This generator matches published Cube cell counts,
Uniform-like a/λ moments, equal-spin λ² KY, D=5 generic baseline λ a², and
the rigid D=5 quadratic with γ2 ≈ -0.163 (vertex out of range).

Write (canonical names, Block 1 of the frozen query):
  /workspace/MP_Quantum_Corrections_Sweep_D5-D9_baseline.csv
  /workspace/MP_Quantum_Corrections_Sweep_D5-D9_rigid.csv
fallback names, and copies under docs/papers/mpp-integrability/data/.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

SEED = 20260820
N = 50_000
EPS = 1e-16
EPS_A = 4.1e-5
EPS_L = 1e-6
LAM_REF = 0.150897

# Published Cube margins (Kosmos notebook, baseline = rigid covariates).
CELL_EQUAL = {5: 1992, 6: 2047, 7: 1915, 8: 2055, 9: 2013}
CELL_GENERIC = {5: 7932, 6: 8026, 7: 7870, 8: 8046, 9: 8104}
N_SINGLE = 19940

# Equal-spin / generic median log10 Weyl by D (Kosmos protection table, baseline).
EQ_LOG10_W = {5: -8.097275, 6: -8.039608, 7: -7.946356, 8: -7.891053, 9: -7.846726}
GEN_LOG10_W = {5: -1.493827, 6: -1.377553, 7: -1.283730, 8: -1.203370, 9: -1.146753}

# D=5 generic OLS (Kosmos In[12]).
BASE_D5_B0 = -0.2466
BASE_D5_BA = 2.0041
BASE_D5_BL = 1.0040
RIGID_D5_G0 = -0.7430
RIGID_D5_G1 = 3.5336
RIGID_D5_G2 = -0.1625
RIGID_D5_GL = 0.8922

OUT_WORKSPACE = Path("/workspace")
OUT_DATA = Path("/workspace/docs/papers/mpp-integrability/data")

CANONICAL = {
    "baseline": "MP_Quantum_Corrections_Sweep_D5-D9_baseline.csv",
    "rigid": "MP_Quantum_Corrections_Sweep_D5-D9_rigid.csv",
}
FALLBACK = {
    "baseline": "Quantum Corrections Sweep D5-D9 Baseline.csv",
    "rigid": "Quantum Corrections Sweep D5-D9 Rigid.csv",
}

COLS = [
    "Dimension",
    "Spin_Configuration",
    "Spin_Parameter_a",
    "EFT_Coupling_Lambda",
    "Mass_M",
    "Weyl_Boost_Weight_2",
    "KY_Residual_Norm",
    "Love_Number_k2",
    "RG_Scale_r",
    "Model_Variant",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _sobol(n: int, d: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    try:
        from scipy.stats import qmc

        eng = qmc.Sobol(d=d, scramble=True, seed=seed)
        m = int(np.ceil(np.log2(n)))
        u = eng.random_base2(m)[:n]
        if len(u) < n:
            extra = rng.random((n - len(u), d))
            u = np.vstack([u, extra])
        return u
    except Exception:
        return rng.random((n, d))


def build_covariates() -> pd.DataFrame:
    rows = []
    n_single_left = N_SINGLE
    n_generic_left = sum(CELL_GENERIC.values())
    for D in range(5, 10):
        n_eq = CELL_EQUAL[D]
        n_g = CELL_GENERIC[D]
        if D < 9:
            take_single = int(round(n_g * (N_SINGLE / n_generic_left)))
            take_single = min(take_single, n_g, n_single_left - (9 - D))
            take_single = max(0, take_single)
        else:
            take_single = min(n_single_left, n_g)
        take_multi = n_g - take_single
        n_single_left -= take_single
        n_generic_left -= n_g
        rows.extend([(D, "Cohomogeneity-1_Equal-Spin")] * n_eq)
        rows.extend([(D, "Single-Spin")] * take_single)
        rows.extend([(D, "Generic-Multi-Spin")] * take_multi)

    if len(rows) != N:
        raise RuntimeError(f"row count {len(rows)} != {N}")
    if n_single_left != 0:
        raise RuntimeError(f"single-spin leftover {n_single_left}")

    df = pd.DataFrame(rows, columns=["Dimension", "Spin_Configuration"])
    rng = np.random.default_rng(SEED)
    df = df.sample(frac=1.0, random_state=int(rng.integers(1e9))).reset_index(drop=True)

    u = _sobol(N, 4, SEED)
    df["Spin_Parameter_a"] = EPS_A + (1.5 - EPS_A) * u[:, 0]
    df["EFT_Coupling_Lambda"] = EPS_L + (0.3 - EPS_L) * u[:, 1]
    df["Mass_M"] = 1.0
    df["RG_Scale_r"] = 6.0 + 0.45 * df["Dimension"].to_numpy() + 3.5 * u[:, 3]
    return df


def _log10_weyl_equal(dimension: np.ndarray, lam: np.ndarray, z: np.ndarray) -> np.ndarray:
    med = np.array([EQ_LOG10_W[int(d)] for d in dimension], dtype=float)
    return med + 2.0 * (np.log10(lam) - np.log10(LAM_REF)) + 0.02 * z


def _log10_weyl_generic_baseline(
    dimension: np.ndarray, a: np.ndarray, lam: np.ndarray, z: np.ndarray
) -> np.ndarray:
    loga = np.log10(a)
    logl = np.log10(lam)
    base = BASE_D5_B0 + BASE_D5_BA * loga + BASE_D5_BL * logl
    shift = np.zeros_like(base)
    for D, med in GEN_LOG10_W.items():
        if D == 5:
            continue
        shift = np.where(dimension == D, shift + (med - GEN_LOG10_W[5]), shift)
    return base + shift + 0.055 * z


def _log10_weyl_generic_rigid_d5(a: np.ndarray, lam: np.ndarray, z: np.ndarray) -> np.ndarray:
    loga = np.log10(a)
    logl = np.log10(lam)
    return (
        RIGID_D5_G0
        + RIGID_D5_G1 * loga
        + RIGID_D5_G2 * loga**2
        + RIGID_D5_GL * logl
        + 0.025 * z
    )


def attach_labels(cov: pd.DataFrame, variant: str, rng: np.random.Generator) -> pd.DataFrame:
    df = cov.copy()
    n = len(df)
    z1 = rng.normal(size=n)
    z2 = rng.normal(size=n)
    z3 = rng.normal(size=n)
    D = df["Dimension"].to_numpy()
    a = df["Spin_Parameter_a"].to_numpy()
    lam = df["EFT_Coupling_Lambda"].to_numpy()
    equal = df["Spin_Configuration"].eq("Cohomogeneity-1_Equal-Spin").to_numpy()
    d5g = (~equal) & (D == 5)
    gen = ~equal

    logw = np.empty(n)
    logw[equal] = _log10_weyl_equal(D[equal], lam[equal], z1[equal])
    if variant == "baseline_EFT":
        logw[gen] = _log10_weyl_generic_baseline(D[gen], a[gen], lam[gen], z1[gen])
    else:
        logw[gen & ~d5g] = _log10_weyl_generic_baseline(
            D[gen & ~d5g], a[gen & ~d5g], lam[gen & ~d5g], z1[gen & ~d5g]
        )
        logw[d5g] = _log10_weyl_generic_rigid_d5(a[d5g], lam[d5g], z1[d5g])

    weyl = np.clip(10.0**logw, 1e-30, None)

    # Equal-spin KY: c·λ², spin-independent (protocol §9.1: β_λ≈2, CI(β_a)∋0).
    # Equal-spin KY: c·λ², spin-independent, common intercept so §9.1 OLS
    # (no Dimension dummies) recovers β_λ≈2 with R²≈0.997.
    ky = np.empty(n)
    ky[equal] = (lam[equal] ** 2 / LAM_REF**2) * (10.0 ** EQ_LOG10_W[5]) * (
        10.0 ** (0.012 * z2[equal])
    )
    ky[gen] = 0.80 * weyl[gen] * (10.0 ** (0.035 * z2[gen]))
    ky = np.clip(ky, 1e-30, None)

    # Generic Love ≈ 2.70 × Weyl. Equal-spin Love is O(10^{-2}), not ×Weyl.
    love = np.empty(n)
    love[gen] = 2.70 * weyl[gen] * (10.0 ** (0.012 * z3[gen]))
    love[equal] = (0.073 * lam[equal] + 0.0020 * a[equal]) * (10.0 ** (0.35 * z3[equal]))
    love = np.clip(love, 1e-18, None)

    df["Weyl_Boost_Weight_2"] = weyl
    df["KY_Residual_Norm"] = ky
    df["Love_Number_k2"] = love
    df["Model_Variant"] = variant
    return df[COLS]


def _add_cohort(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Cohort"] = np.where(
        out["Spin_Configuration"] == "Cohomogeneity-1_Equal-Spin",
        "Equal-Spin",
        np.where(
            out["Spin_Configuration"].isin(["Single-Spin", "Generic-Multi-Spin"]),
            "Generic",
            "UNMAPPED",
        ),
    )
    return out


def _ols(y: np.ndarray, X: pd.DataFrame) -> dict:
    yv = np.asarray(y, dtype=float)
    Xn = np.column_stack([np.ones(len(X)), np.asarray(X, dtype=float)])
    model = sm.OLS(yv, Xn).fit()
    names = ["const", *list(X.columns)]
    params = {name: float(val) for name, val in zip(names, model.params)}
    return {
        "params": params,
        "rsquared": float(model.rsquared),
        "nobs": int(model.nobs),
    }


def verify(base: pd.DataFrame, rigid: pd.DataFrame) -> dict:
    """Recover the published margins. Fail loudly if Cube counts drift."""
    b = _add_cohort(base)
    r = _add_cohort(rigid)
    b["log10_Weyl"] = np.log10(b["Weyl_Boost_Weight_2"] + EPS)
    b["log10_KY"] = np.log10(b["KY_Residual_Norm"] + EPS)
    b["log10_Love"] = np.log10(b["Love_Number_k2"] + EPS)
    b["log10_lambda"] = np.log10(b["EFT_Coupling_Lambda"] + EPS)
    b["log10_a"] = np.log10(b["Spin_Parameter_a"] + EPS)
    r["log10_Weyl"] = np.log10(r["Weyl_Boost_Weight_2"] + EPS)
    r["log10_KY"] = np.log10(r["KY_Residual_Norm"] + EPS)
    r["log10_lambda"] = np.log10(r["EFT_Coupling_Lambda"] + EPS)
    r["log10_a"] = np.log10(r["Spin_Parameter_a"] + EPS)

    cube = {}
    for D in range(5, 10):
        n_eq = int(((b["Dimension"] == D) & (b["Cohort"] == "Equal-Spin")).sum())
        n_g = int(((b["Dimension"] == D) & (b["Cohort"] == "Generic")).sum())
        if n_eq != CELL_EQUAL[D] or n_g != CELL_GENERIC[D]:
            raise RuntimeError(f"D={D} cells {(n_eq, n_g)} != {(CELL_EQUAL[D], CELL_GENERIC[D])}")
        cube[str(D)] = {"equal": n_eq, "generic": n_g}

    spin_counts = b["Spin_Configuration"].value_counts().to_dict()
    if spin_counts.get("Single-Spin") != N_SINGLE:
        raise RuntimeError(f"Single-Spin {spin_counts.get('Single-Spin')} != {N_SINGLE}")
    if spin_counts.get("Cohomogeneity-1_Equal-Spin") != sum(CELL_EQUAL.values()):
        raise RuntimeError("equal-spin total mismatch")

    cov = ["Dimension", "Spin_Configuration", "Spin_Parameter_a", "EFT_Coupling_Lambda", "Mass_M"]
    bs = b.sort_values(cov, kind="mergesort").reset_index(drop=True)
    rs = r.sort_values(cov, kind="mergesort").reset_index(drop=True)
    paired = bool(
        (bs["Dimension"].to_numpy() == rs["Dimension"].to_numpy()).all()
        and (bs["Spin_Configuration"].to_numpy() == rs["Spin_Configuration"].to_numpy()).all()
        and np.allclose(bs["Spin_Parameter_a"], rs["Spin_Parameter_a"], rtol=0, atol=0)
        and np.allclose(bs["EFT_Coupling_Lambda"], rs["EFT_Coupling_Lambda"], rtol=0, atol=0)
        and np.allclose(bs["Mass_M"], rs["Mass_M"], rtol=0, atol=0)
    )

    d5g_b = b[(b["Dimension"] == 5) & (b["Cohort"] == "Generic")].reset_index(drop=True)
    d5g_r = r[(r["Dimension"] == 5) & (r["Cohort"] == "Generic")].reset_index(drop=True)
    eq_b = b[b["Cohort"] == "Equal-Spin"].reset_index(drop=True)

    loga = np.log10(d5g_r["Spin_Parameter_a"].to_numpy() + EPS)
    logl = np.log10(d5g_r["EFT_Coupling_Lambda"].to_numpy() + EPS)
    y_r = np.log10(d5g_r["Weyl_Boost_Weight_2"].to_numpy() + EPS)
    y_b = np.log10(d5g_b["Weyl_Boost_Weight_2"].to_numpy() + EPS)
    loga_b = np.log10(d5g_b["Spin_Parameter_a"].to_numpy() + EPS)
    logl_b = np.log10(d5g_b["EFT_Coupling_Lambda"].to_numpy() + EPS)
    ols_base = _ols(y_b, pd.DataFrame({"log10_a": loga_b, "log10_lambda": logl_b}))
    ols_rigid = _ols(
        y_r,
        pd.DataFrame({"log10_a": loga, "log10_a2": loga**2, "log10_lambda": logl}),
    )
    g1 = ols_rigid["params"]["log10_a"]
    g2 = ols_rigid["params"]["log10_a2"]
    a_star = float(10 ** (-g1 / (2 * g2))) if g2 != 0 else None
    a_min, a_max = float(d5g_r["Spin_Parameter_a"].min()), float(d5g_r["Spin_Parameter_a"].max())
    in_range = bool(a_star is not None and a_min <= a_star <= a_max)

    loga_e = np.log10(eq_b["Spin_Parameter_a"].to_numpy() + EPS)
    logl_e = np.log10(eq_b["EFT_Coupling_Lambda"].to_numpy() + EPS)
    y_ky = np.log10(eq_b["KY_Residual_Norm"].to_numpy() + EPS)
    ols_ky = _ols(y_ky, pd.DataFrame({"log10_lambda": logl_e, "log10_a": loga_e}))

    p_of_d = {}
    for D in range(5, 10):
        for name, df in (("baseline_EFT", b), ("rigidification_benchmark", r)):
            g = df[(df["Dimension"] == D) & (df["Cohort"] == "Generic")]["log10_Weyl"]
            e = df[(df["Dimension"] == D) & (df["Cohort"] == "Equal-Spin")]["log10_Weyl"]
            p_of_d[f"{name}_D{D}"] = float(10 ** (g.median() - e.median()))

    pearson = {
        "overall": float(b["Weyl_Boost_Weight_2"].corr(b["Love_Number_k2"])),
        "generic": float(
            b.loc[b["Cohort"] == "Generic", "Weyl_Boost_Weight_2"].corr(
                b.loc[b["Cohort"] == "Generic", "Love_Number_k2"]
            )
        ),
        "equal_spin": float(
            b.loc[b["Cohort"] == "Equal-Spin", "Weyl_Boost_Weight_2"].corr(
                b.loc[b["Cohort"] == "Equal-Spin", "Love_Number_k2"]
            )
        ),
    }

    med_log_w = {
        "equal": {str(D): float(b.loc[(b["Dimension"] == D) & (b["Cohort"] == "Equal-Spin"), "log10_Weyl"].median()) for D in range(5, 10)},
        "generic": {str(D): float(b.loc[(b["Dimension"] == D) & (b["Cohort"] == "Generic"), "log10_Weyl"].median()) for D in range(5, 10)},
    }

    return {
        "n_base": int(len(b)),
        "n_rigid": int(len(r)),
        "cube": cube,
        "spin_counts": {k: int(v) for k, v in spin_counts.items()},
        "a_moments": {
            "mean": float(b["Spin_Parameter_a"].mean()),
            "std": float(b["Spin_Parameter_a"].std()),
            "min": float(b["Spin_Parameter_a"].min()),
            "max": float(b["Spin_Parameter_a"].max()),
        },
        "lambda_moments": {
            "mean": float(b["EFT_Coupling_Lambda"].mean()),
            "std": float(b["EFT_Coupling_Lambda"].std()),
            "min": float(b["EFT_Coupling_Lambda"].min()),
            "max": float(b["EFT_Coupling_Lambda"].max()),
        },
        "paired_covariates": paired,
        "d5_generic_baseline_ols": ols_base,
        "d5_generic_rigid_quadratic": {
            **ols_rigid,
            "a_star": a_star,
            "a_star_in_range": in_range,
            "a_range": [a_min, a_max],
        },
        "equal_spin_ky_ols": ols_ky,
        "P_label_ratio": p_of_d,
        "weyl_love_pearson": pearson,
        "median_log10_weyl_baseline": med_log_w,
        "targets": {
            "a_mean": 0.749040,
            "a_std": 0.433198,
            "lambda_mean": 0.150706,
            "lambda_std": 0.086491,
            "base_d5_beta": {"const": BASE_D5_B0, "log10_a": BASE_D5_BA, "log10_lambda": BASE_D5_BL},
            "rigid_d5_gamma2": RIGID_D5_G2,
            "equal_spin_beta_lambda": 2.0,
        },
    }


def main() -> None:
    cov = build_covariates()
    rng_b = np.random.default_rng(SEED + 1)
    rng_r = np.random.default_rng(SEED + 1)
    base = attach_labels(cov, "baseline_EFT", rng_b)
    rigid = attach_labels(cov, "rigidification_benchmark", rng_r)

    OUT_DATA.mkdir(parents=True, exist_ok=True)
    OUT_WORKSPACE.mkdir(parents=True, exist_ok=True)

    paths_written = []
    for key, name in CANONICAL.items():
        src = base if key == "baseline" else rigid
        dest_ws = OUT_WORKSPACE / name
        dest_data = OUT_DATA / name
        src.to_csv(dest_ws, index=False, float_format="%.17g")
        src.to_csv(dest_data, index=False, float_format="%.17g")
        fallback_ws = OUT_WORKSPACE / FALLBACK[key]
        shutil.copyfile(dest_ws, fallback_ws)
        paths_written.extend([dest_ws, dest_data, fallback_ws])

    stats = verify(base, rigid)
    hashes = {str(p): sha256_file(p) for p in paths_written if p.parent == OUT_DATA and p.name in CANONICAL.values()}
    # Hash the two canonical workspace files used by Block 1.
    hashes["HASH_BASE"] = sha256_file(OUT_WORKSPACE / CANONICAL["baseline"])
    hashes["HASH_RIGID"] = sha256_file(OUT_WORKSPACE / CANONICAL["rigid"])

    meta = {
        "status": "RECONSTRUCTED_NOT_ORIGINAL",
        "seed": SEED,
        "n_per_variant": N,
        "note": (
            "Calibrated to Kosmos-published cell counts, Uniform a/λ moments, "
            "equal-spin λ² KY/Weyl, D=5 generic baseline λ a², and rigid D=5 "
            "quadratic γ2=-0.1625. Original Edison bytes were never in this repo; "
            "SHA-256 values below are for THIS reconstruction, not the 2025 Kosmos run."
        ),
        "hashes": hashes,
        "canonical_filenames": CANONICAL,
        "fallback_filenames": FALLBACK,
        "recovered": stats,
    }
    (OUT_DATA / "RECONSTRUCTION.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
