#!/usr/bin/env python3
"""P4 Gate E part 1: pack C1 (TL) and C2 (EN) from frozen jsonl. Blinded."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pack_parquet import pack_dir  # noqa: E402
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    C1_DIR,
    C2_DIR,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    EXPECTED,
    P4_RUN_ID,
    PYTHON,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TL_TEST_JSONL,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
    VENDOR,
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-e-c1-c2-pack.json"


def load_jsonl(path: Path, expected: str) -> list[dict]:
    actual = sha256_file(path)
    if actual != expected:
        raise SystemExit(f"hash mismatch {path}: {actual}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    rows.sort(key=lambda r: r["doc_id"])
    return rows


def probe_last(data_dir: Path) -> dict:
    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(ROOT / "data" / "cache" / P4_RUN_ID)
    env["NANOCHAT_DATA_DIR"] = str(data_dir)
    env["PYTHONPATH"] = str(VENDOR)
    probe = (
        "from nanochat.dataset import DATA_DIR, list_parquet_files; import os; "
        "paths = list_parquet_files(); print(DATA_DIR); "
        "print('LAST', os.path.basename(paths[-1]) if paths else 'NONE')"
    )
    proc = subprocess.run([str(PYTHON), "-c", probe], cwd=str(VENDOR), env=env, check=True, capture_output=True, text=True)
    lines = [ln for ln in proc.stdout.splitlines() if ln]
    return {"data_dir_ok": lines[0] == str(data_dir), "last": lines[-1]}


def test_filenames(path: Path) -> list[str]:
    return [p.name for p in path.rglob("*") if "test" in p.name.lower()]


def main() -> int:
    tl_test_before = sha256_file(TL_TEST_JSONL)
    en_test_before = sha256_file(EN_TEST_JSONL)
    en_train = load_jsonl(EN_TRAIN_JSONL, EXPECTED["en_train_jsonl"])
    en_val = load_jsonl(EN_VAL_JSONL, EXPECTED["en_val_jsonl"])
    tl_train = load_jsonl(TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"])
    tl_val = load_jsonl(TL_VAL_JSONL, EXPECTED["tl_val_jsonl"])
    c2 = pack_dir(C2_DIR, en_train, en_val)
    c1 = pack_dir(C1_DIR, tl_train, tl_val)
    probes = {"c1": probe_last(C1_DIR), "c2": probe_last(C2_DIR)}
    checks = [
        {"id": "E_C1_last_is_val", "ok": c1["last_is_val"] and probes["c1"]["last"] == "LAST val.parquet"},
        {"id": "E_C2_last_is_val", "ok": c2["last_is_val"] and probes["c2"]["last"] == "LAST val.parquet"},
        {"id": "E_tests_absent", "ok": test_filenames(C1_DIR) == [] and test_filenames(C2_DIR) == []},
        {
            "id": "E_tests_untouched",
            "ok": sha256_file(TL_TEST_JSONL) == tl_test_before == EXPECTED["tl_test_jsonl"]
            and sha256_file(EN_TEST_JSONL) == en_test_before == EXPECTED["en_test_jsonl"],
        },
        {"id": "E_c3_not_yet", "ok": True, "detail": "C3 constructed by gate_e_c3_mix.py after F"},
    ]
    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "E-pack",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "script": "scripts/p4/gate_e_shards.py",
        "c1_tl": c1,
        "c2_en": c2,
        "probes": probes,
        "checks": checks,
        "no_p4_outcomes": True,
        "next": "gate_e_c3_mix.py",
    }
    write_json(OUT, payload)
    print(json.dumps({"status": payload["status"], "path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]], "blinded": True}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
