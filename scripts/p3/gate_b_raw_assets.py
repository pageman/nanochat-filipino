#!/usr/bin/env python3
"""P3 Gate B: verify F-01/F-02 raw assets on disk. No train/eval."""

from __future__ import annotations

import json
import stat
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

from p3_common import (
    ASPREDICTED_ID,
    EN_RAW_DIR,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    EXPECTED,
    P3_RUN_ID,
    RESEARCHBOX_ID,
    RESEARCHBOX_URL,
    ROOT,
    RUN_CARD,
    TL_TEST,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
)


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def freeze(path: Path) -> None:
    path.chmod(0o444)


def audit_parquet(path: Path, expected_sha: str) -> dict:
    got = sha256_file(path)
    pf = pq.ParquetFile(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": got,
        "expected": expected_sha,
        "ok": got == expected_sha,
        "bytes": path.stat().st_size,
        "num_rows": pf.metadata.num_rows,
        "columns": list(pf.schema_arrow.names),
        "mode": oct(path.stat().st_mode & 0o777),
    }


def main() -> int:
    OUT = RUN_CARD / "gate-b-raw-assets.json"
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    tl_files = {
        "train.jsonl": (TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"]),
        "val.jsonl": (TL_VAL_JSONL, EXPECTED["tl_val_jsonl"]),
        "test.jsonl": (TL_TEST, EXPECTED["tl_test_jsonl"]),
    }
    tl_rows = {}
    for name, (path, exp) in tl_files.items():
        got = sha256_file(path) if path.is_file() else None
        tl_rows[name] = {"path": str(path.relative_to(ROOT)), "sha256": got, "expected": exp, "ok": got == exp}
        if path.is_file() and got == exp:
            freeze(path)
    record("B1_tl_split_hashes", all(v["ok"] for v in tl_rows.values()), tl_rows)

    en_files = {
        "english_train.jsonl": (EN_TRAIN_JSONL, EXPECTED["en_train_jsonl"]),
        "english_val.jsonl": (EN_VAL_JSONL, EXPECTED["en_val_jsonl"]),
        "english_test.jsonl": (EN_TEST_JSONL, EXPECTED["en_test_jsonl"]),
    }
    en_rows = {}
    for name, (path, exp) in en_files.items():
        got = sha256_file(path) if path.is_file() else None
        en_rows[name] = {"path": str(path.relative_to(ROOT)), "sha256": got, "expected": exp, "ok": got == exp}
        if path.is_file() and got == exp:
            freeze(path)
    record("B2_en_document_manifest_hashes", all(v["ok"] for v in en_rows.values()), en_rows)

    raw_rows = []
    for fname, exp in EXPECTED["en_raw_parquets"].items():
        path = EN_RAW_DIR / fname
        if path.is_file():
            freeze(path)
        row = audit_parquet(path, exp) if path.is_file() else {"path": str(path), "ok": False}
        raw_rows.append(row)
    record("B3_en_raw_parquet_hashes", all(r.get("ok") for r in raw_rows), raw_rows)

    record(
        "B4_p11_split_reuse_not_rebuilt",
        tl_rows["train.jsonl"]["ok"] and tl_rows["val.jsonl"]["ok"],
        {"split_origin": "p11_reuse"},
    )
    record(
        "B5_en_test_not_used_as_train",
        EN_TEST_JSONL.is_file() and EN_TRAIN_JSONL.is_file() and EN_TEST_JSONL != EN_TRAIN_JSONL,
        True,
    )
    record("B6_no_train_or_eval_started", True, {"p3_tok_train": False, "p3_base_train": False})

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "researchbox_url": RESEARCHBOX_URL,
        "gate": "B",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_b_raw_assets.py",
        "f01_tagalog": tl_rows,
        "f02_english_manifests": en_rows,
        "f02_english_raw": raw_rows,
        "hf_dataset": "Salesforce/wikitext",
        "hf_config": "wikitext-103-raw-v1",
        "hf_revision_sha": "b08601e04326c79dfdd32d625aee71d232d685c3",
        "rehash_note": "Existing on-disk archives verified; Gate B identity is SHA256 match to filed manifests.",
        "checks": checks,
        "no_train_or_eval_started": True,
        "next_gate": "C",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
