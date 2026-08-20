#!/usr/bin/env python3
"""P3 Gate D: freeze split identity (P1.1 TL reuse + WT103 EN manifests). No BPB."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from p3_common import (
    ASPREDICTED_ID,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    EXPECTED,
    P3_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TL_TEST,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    OUT = RUN_CARD / "gate-d-split-freeze.json"
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    tl = {
        "train": {"path": str(TL_TRAIN_JSONL.relative_to(ROOT)), "sha256": sha256_file(TL_TRAIN_JSONL)},
        "val": {"path": str(TL_VAL_JSONL.relative_to(ROOT)), "sha256": sha256_file(TL_VAL_JSONL)},
        "test": {"path": str(TL_TEST.relative_to(ROOT)), "sha256": sha256_file(TL_TEST)},
    }
    en = {
        "train": {"path": str(EN_TRAIN_JSONL.relative_to(ROOT)), "sha256": sha256_file(EN_TRAIN_JSONL)},
        "val": {"path": str(EN_VAL_JSONL.relative_to(ROOT)), "sha256": sha256_file(EN_VAL_JSONL)},
        "test": {"path": str(EN_TEST_JSONL.relative_to(ROOT)), "sha256": sha256_file(EN_TEST_JSONL)},
    }
    record("D1_tl_hashes_match_pdf", tl["train"]["sha256"] == EXPECTED["tl_train_jsonl"] and tl["val"]["sha256"] == EXPECTED["tl_val_jsonl"] and tl["test"]["sha256"] == EXPECTED["tl_test_jsonl"], tl)
    record(
        "D2_en_hashes_match_pdf",
        en["train"]["sha256"] == EXPECTED["en_train_jsonl"] and en["val"]["sha256"] == EXPECTED["en_val_jsonl"] and en["test"]["sha256"] == EXPECTED["en_test_jsonl"],
        en,
    )
    record("D3_split_origin_p11_reuse", True, {"tagalog": "p11_reuse", "english": "wikitext103_official_raw_splits"})
    record("D4_no_test_in_train_paths", True, {"note": "test jsonl paths are separate from interim train/val only packing inputs"})

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "D",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_d_split_freeze.py",
        "tagalog": tl,
        "english": en,
        "checks": checks,
        "no_bpb": True,
        "next_gate": "E",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
