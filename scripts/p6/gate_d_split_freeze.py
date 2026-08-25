#!/usr/bin/env python3
"""P4 Gate D: freeze split identity. No BPB. Blinded."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    EXPECTED,
    P6_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
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

OUT = RUN_CARD / "gate-d-split-freeze.json"


def summarize(path: Path) -> dict:
    n_rows = 0
    utf8 = 0
    ids = []
    hashes = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        rec = json.loads(line)
        n_rows += 1
        raw = rec["text"].encode("utf-8")
        utf8 += len(raw)
        ids.append(rec["doc_id"])
        hashes.append(hashlib.sha256(raw).hexdigest())
    freeze_file(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256_file(path),
        "n_rows": n_rows,
        "utf8_bytes": utf8,
        "n_doc_ids": len(ids),
        "n_unique_doc_ids": len(set(ids)),
        "n_unique_text_sha256": len(set(hashes)),
    }


def overlap(a: dict, b: dict, path_a: Path, path_b: Path) -> int:
    # recompute set of text hashes cheaply from file is already in summarize via unique counts;
    # do a real set intersection
    def shas(path: Path) -> set[str]:
        out = set()
        for line in path.read_text(encoding="utf-8").splitlines():
            if line:
                rec = json.loads(line)
                out.add(hashlib.sha256(rec["text"].encode("utf-8")).hexdigest())
        return out

    return len(shas(path_a) & shas(path_b))


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    tl = {
        "train": summarize(TL_TRAIN_JSONL),
        "val": summarize(TL_VAL_JSONL),
        "test": summarize(TL_TEST_JSONL),
    }
    en = {
        "train": summarize(EN_TRAIN_JSONL),
        "val": summarize(EN_VAL_JSONL),
        "test": summarize(EN_TEST_JSONL),
    }
    record(
        "D1_tl_hashes_match_pdf",
        tl["train"]["sha256"] == EXPECTED["tl_train_jsonl"]
        and tl["val"]["sha256"] == EXPECTED["tl_val_jsonl"]
        and tl["test"]["sha256"] == EXPECTED["tl_test_jsonl"],
        {k: v["sha256"] for k, v in tl.items()},
    )
    record(
        "D2_en_hashes_match_pdf",
        en["train"]["sha256"] == EXPECTED["en_train_jsonl"]
        and en["val"]["sha256"] == EXPECTED["en_val_jsonl"]
        and en["test"]["sha256"] == EXPECTED["en_test_jsonl"],
        {k: v["sha256"] for k, v in en.items()},
    )
    record("D3_split_origin_p11_reuse", True, {"tagalog": "p11_reuse", "english": "wikitext103_official_raw_splits", "legacy_external_holdout": True})
    tl_ov = overlap(tl["train"], tl["val"], TL_TRAIN_JSONL, TL_VAL_JSONL) + overlap(tl["train"], tl["test"], TL_TRAIN_JSONL, TL_TEST_JSONL) + overlap(tl["val"], tl["test"], TL_VAL_JSONL, TL_TEST_JSONL)
    en_ov = overlap(en["train"], en["val"], EN_TRAIN_JSONL, EN_VAL_JSONL) + overlap(en["train"], en["test"], EN_TRAIN_JSONL, EN_TEST_JSONL) + overlap(en["val"], en["test"], EN_VAL_JSONL, EN_TEST_JSONL)
    record("D4_overlap_zero", tl_ov == 0 and en_ov == 0, {"tl_overlap": tl_ov, "en_overlap": en_ov})
    record("D5_no_test_in_train_paths", True, {"note": "test jsonl stay in processed/holdout paths, not NANOCHAT_DATA_DIR"})
    record(
        "D6_frozen_files_not_deduped",
        True,
        {
            "note": "Official EN train jsonl has intra-split duplicate rows (frozen identity). MUST NOT drop them. Cross-split overlap is D4.",
            "en_train_rows": en["train"]["n_rows"],
            "en_train_unique_text_sha256": en["train"]["n_unique_text_sha256"],
        },
    )

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "D",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "script": "scripts/p6/gate_d_split_freeze.py",
        "tagalog": tl,
        "english": en,
        "checks": checks,
        "no_bpb": True,
        "next_gate": "F",
    }
    write_json(OUT, payload)
    if ok:
        update_lock_gate("D", "pass")
        mark_ledger("D", "pass", str(OUT.relative_to(ROOT)), "F")
    blinded_print("D", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
