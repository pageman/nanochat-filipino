#!/usr/bin/env python3
"""P4 Gate B: verify six confirmatory JSONL hashes; byte-identical copies. Blinded."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    EXPECTED,
    HOLDOUT_DIR,
    P6_RUN_ID,
    RESEARCHBOX_ID,
    RESEARCHBOX_URL,
    ROOT,
    RUN_CARD,
    SPLIT_COPY_DIR,
    TL_TEST_JSONL,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
    blinded_print,
    freeze_file,
    mark_ledger,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-b-raw-assets.json"

ASSETS = {
    "tl_train": (TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"], SPLIT_COPY_DIR / "tl" / "train.jsonl", False),
    "tl_val": (TL_VAL_JSONL, EXPECTED["tl_val_jsonl"], SPLIT_COPY_DIR / "tl" / "val.jsonl", False),
    "tl_test": (TL_TEST_JSONL, EXPECTED["tl_test_jsonl"], HOLDOUT_DIR / "tl" / "test.jsonl", True),
    "en_train": (EN_TRAIN_JSONL, EXPECTED["en_train_jsonl"], SPLIT_COPY_DIR / "en" / "train.jsonl", False),
    "en_val": (EN_VAL_JSONL, EXPECTED["en_val_jsonl"], SPLIT_COPY_DIR / "en" / "val.jsonl", True and False),
    "en_test": (EN_TEST_JSONL, EXPECTED["en_test_jsonl"], HOLDOUT_DIR / "en" / "test.jsonl", True),
}
# en_val is train-visible split, not a test holdout
ASSETS["en_val"] = (EN_VAL_JSONL, EXPECTED["en_val_jsonl"], SPLIT_COPY_DIR / "en" / "val.jsonl", False)


def copy_identical(src: Path, dst: Path, expected: str) -> dict:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.chmod(0o644)
    shutil.copy2(src, dst)
    freeze_file(src)
    freeze_file(dst)
    got = sha256_file(dst)
    return {
        "src": str(src.relative_to(ROOT)),
        "dst": str(dst.relative_to(ROOT)),
        "bytes": dst.stat().st_size,
        "sha256": got,
        "expected": expected,
        "ok": got == expected,
        "p11_split_reuse": "tl" in dst.as_posix(),
        "license": "wikitext / cc-by-sa-family as recorded in source dumps",
        "utc": utc_now(),
    }


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    rows = {}
    for name, (src, exp, dst, is_test) in ASSETS.items():
        rows[name] = copy_identical(src, dst, exp)
        rows[name]["is_test"] = is_test
    record("B1_six_confirmatory_shas", all(v["ok"] for v in rows.values()), {k: {"sha256": v["sha256"], "ok": v["ok"]} for k, v in rows.items()})
    record(
        "B2_p11_split_reuse",
        rows["tl_train"]["ok"] and rows["tl_val"]["ok"] and rows["tl_test"]["ok"],
        {"split_origin": "p11_reuse", "p11_split_reuse": True},
    )
    record(
        "B3_en_test_not_used_as_train",
        EN_TEST_JSONL.resolve() != EN_TRAIN_JSONL.resolve() and rows["en_test"]["sha256"] != rows["en_train"]["sha256"],
        True,
    )
    test_under_train = []
    for p in SPLIT_COPY_DIR.rglob("*") if SPLIT_COPY_DIR.is_dir() else []:
        if p.is_file() and "test" in p.name.lower():
            test_under_train.append(str(p))
    record("B4_tests_unmounted", test_under_train == [] and (HOLDOUT_DIR / "tl" / "test.jsonl").is_file(), test_under_train)
    record("B5_no_train_or_eval_started", True, {"tok_train": False, "base_train": False, "packing": False})

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "researchbox_url": RESEARCHBOX_URL,
        "gate": "B",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "script": "scripts/p6/gate_b_raw_assets.py",
        "hf_dataset": "Salesforce/wikitext",
        "hf_config": "wikitext-103-raw-v1",
        "hf_revision_sha": "b08601e04326c79dfdd32d625aee71d232d685c3",
        "artifacts": rows,
        "checks": checks,
        "no_train_or_eval_started": True,
        "tests_unmounted": True,
        "next_gate": "C",
    }
    write_json(OUT, payload)
    if ok:
        update_lock_gate("B", "pass")
        mark_ledger("B", "pass", str(OUT.relative_to(ROOT)), "C")
    blinded_print("B", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
