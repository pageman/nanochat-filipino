#!/usr/bin/env python3
"""Gate A tests for the NANOCHAT_DATA_DIR hook.

Unset env must keep the ClimbMix default. Set env must use the Project 1 directory.
Last-lexicographic parquet is treated as val (nanochat convention).
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

VENDOR = Path(__file__).resolve().parents[2] / "vendor" / "nanochat"
PYTHON = VENDOR / ".venv" / "bin" / "python"


def test_unset_keeps_climbmix_default(tmp_base: Path) -> None:
    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(tmp_base)
    env.pop("NANOCHAT_DATA_DIR", None)
    env["PYTHONPATH"] = str(VENDOR)
    proc = subprocess.run(
        [str(PYTHON), "-c", "from nanochat.dataset import DATA_DIR; import sys; sys.stdout.write(DATA_DIR)"],
        cwd=str(VENDOR),
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.stdout.endswith("base_data_climbmix"), proc.stdout
    assert str(tmp_base) in proc.stdout


def test_set_uses_project_dir(tmp_base: Path, project_dir: Path) -> None:
    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(tmp_base)
    env["NANOCHAT_DATA_DIR"] = str(project_dir)
    env["PYTHONPATH"] = str(VENDOR)
    proc = subprocess.run(
        [str(PYTHON), "-c", "from nanochat.dataset import DATA_DIR; import sys; sys.stdout.write(DATA_DIR)"],
        cwd=str(VENDOR),
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.stdout == str(project_dir), proc.stdout


def test_last_file_is_val(tmp_base: Path, project_dir: Path) -> None:
    for name in ("shard_00000.parquet", "shard_00001.parquet", "shard_00002.parquet"):
        (project_dir / name).write_bytes(b"")
    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(tmp_base)
    env.pop("NANOCHAT_DATA_DIR", None)
    env["PYTHONPATH"] = str(VENDOR)
    code = (
        "from nanochat.dataset import list_parquet_files; "
        f"paths = list_parquet_files(data_dir={str(project_dir)!r}); "
        "print('\\n'.join(paths))"
    )
    proc = subprocess.run(
        [str(PYTHON), "-c", code],
        cwd=str(VENDOR),
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    names = [Path(p).name for p in proc.stdout.strip().splitlines()]
    assert names == [
        "shard_00000.parquet",
        "shard_00001.parquet",
        "shard_00002.parquet",
    ]
    assert names[-1] == "shard_00002.parquet"


def main() -> int:
    if not PYTHON.is_file():
        print("missing vendor/nanochat/.venv", file=sys.stderr)
        return 1
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        base = tmp / "base"
        project = tmp / "p1_shards"
        base.mkdir()
        project.mkdir()
        test_unset_keeps_climbmix_default(base)
        test_set_uses_project_dir(base, project)
        test_last_file_is_val(base, project)
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
