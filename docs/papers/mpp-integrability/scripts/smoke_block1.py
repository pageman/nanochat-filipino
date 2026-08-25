#!/usr/bin/env python3
"""Block 1 harvest smoke test for the reconstructed MPP CSVs.

Does not run Gate-4 science tables or invent physics. Confirms the frozen
query can load both files from /workspace under the canonical names.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

WORKSPACE = Path("/workspace")
FILE_BASE = "MP_Quantum_Corrections_Sweep_D5-D9_baseline.csv"
FILE_RIGID = "MP_Quantum_Corrections_Sweep_D5-D9_rigid.csv"
FALLBACK_BASE = "Quantum Corrections Sweep D5-D9 Baseline.csv"
FALLBACK_RIGID = "Quantum Corrections Sweep D5-D9 Rigid.csv"
REQUIRED = [
    "Dimension",
    "Spin_Configuration",
    "Spin_Parameter_a",
    "EFT_Coupling_Lambda",
    "Weyl_Boost_Weight_2",
    "KY_Residual_Norm",
    "Love_Number_k2",
    "Model_Variant",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve() -> tuple[Path, Path, str]:
    p_base = WORKSPACE / FILE_BASE
    p_rigid = WORKSPACE / FILE_RIGID
    if p_base.is_file() and p_rigid.is_file():
        return p_base, p_rigid, "canonical"
    p_base = WORKSPACE / FALLBACK_BASE
    p_rigid = WORKSPACE / FALLBACK_RIGID
    if p_base.is_file() and p_rigid.is_file():
        return p_base, p_rigid, "fallback"
    raise SystemExit("Block 1 FAIL — files not found.")


def main() -> None:
    path_base, path_rigid, how = resolve()
    print("Block 1 result: PASS — files found via", how)
    print("FILE_BASE ", path_base.resolve())
    print("FILE_RIGID", path_rigid.resolve())
    print("HASH_BASE ", sha256_file(path_base))
    print("HASH_RIGID", sha256_file(path_rigid))
    df_base = pd.read_csv(path_base)
    df_rigid = pd.read_csv(path_rigid)
    print("shape_base ", df_base.shape)
    print("shape_rigid", df_rigid.shape)
    for name, df in ("baseline", df_base), ("rigid", df_rigid):
        missing = [c for c in REQUIRED if c not in df.columns]
        if missing:
            raise SystemExit(f"Block 1 FAIL — {name} missing {missing}")
        for col in ["Weyl_Boost_Weight_2", "KY_Residual_Norm", "Love_Number_k2"]:
            n_neg = int((df[col] < 0).sum())
            if n_neg:
                raise SystemExit(f"Block 1 FAIL — {name} has {n_neg} negative {col}")
    print("required columns present; labels non-negative")
    print("variants", sorted(set(df_base["Model_Variant"]) | set(df_rigid["Model_Variant"])))


if __name__ == "__main__":
    main()
