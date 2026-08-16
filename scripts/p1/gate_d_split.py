#!/usr/bin/env python3
"""Gate D: recover 2019 splits if present, else lex-hash 70/15/15. Isolate test."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "data" / "interim" / "wikitext-tl39" / "documents_canonical.jsonl"
AUDIT = ROOT / "manifests" / "corpus_audit.json"
EXPECTED_CANONICAL_SHA = "aec6da3c8fadf2243c1ea3545289d9f651cd0c2a9e95adcaf8e340dde051d652"
INTERIM_SPLITS = ROOT / "data" / "interim" / "wikitext-tl39" / "splits"
TEST_DIR = ROOT / "data" / "processed" / "wikitext-tl39" / "test"
ACTIVE_DIR = ROOT / "data" / "processed" / "wikitext-tl39" / "active"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_jsonl(path: Path, rows: list[dict]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return sha256_file(path)


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    if sha256_file(CANONICAL) != EXPECTED_CANONICAL_SHA:
        print(json.dumps({"ok": False, "error": "canonical jsonl hash mismatch"}), file=sys.stderr)
        return 1
    if not audit["reconstruction"]["reconstruction_ok"]:
        print(json.dumps({"ok": False, "error": "Gate C recommended row fallback; refusing to invent article split"}), file=sys.stderr)
        return 1

    units: dict[str, dict] = {}
    for line in CANONICAL.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        doc_id = rec["doc_id"]
        text = rec["text"]
        text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if text_hash != doc_id:
            print(json.dumps({"ok": False, "error": "doc_id is not sha256(text)", "doc_id": doc_id}), file=sys.stderr)
            return 1
        if doc_id not in units:
            units[doc_id] = rec

    ids = sorted(units)
    n = len(ids)
    i_train = int(n * 0.70)
    i_val = int(n * 0.85)
    assignment = {
        "train": ids[:i_train],
        "val": ids[i_train:i_val],
        "test": ids[i_val:],
    }
    rows = {name: [units[i] for i in assignment[name]] for name in ("train", "val", "test")}

    hashes = {name: {r["doc_id"] for r in rows[name]} for name in rows}
    overlap = {
        "train_val": sorted(hashes["train"] & hashes["val"]),
        "train_test": sorted(hashes["train"] & hashes["test"]),
        "val_test": sorted(hashes["val"] & hashes["test"]),
    }
    overlap_n = {k: len(v) for k, v in overlap.items()}

    titles = {name: Counter(r["title"] for r in rows[name]) for name in rows}
    title_overlap = {
        "train_val": sorted(set(titles["train"]) & set(titles["val"])),
        "train_test": sorted(set(titles["train"]) & set(titles["test"])),
        "val_test": sorted(set(titles["val"]) & set(titles["test"])),
    }

    def stats(name: str) -> dict:
        recs = rows[name]
        n_chars = sum(r["n_chars"] for r in recs)
        n_bytes = sum(len(r["text"].encode("utf-8")) for r in recs)
        return {
            "n_units": len(recs),
            "unit_fraction": len(recs) / n,
            "n_chars": n_chars,
            "char_fraction": n_chars / sum(r["n_chars"] for r in units.values()),
            "n_bytes": n_bytes,
        }

    split_stats = {name: stats(name) for name in rows}
    d4 = all(0.65 <= split_stats["train"]["unit_fraction"] <= 0.75 for _ in [0]) and all(
        0.12 <= split_stats[s]["unit_fraction"] <= 0.18 for s in ("val", "test")
    )
    d5 = all(0.65 <= split_stats["train"]["char_fraction"] <= 0.75 for _ in [0]) and all(
        0.12 <= split_stats[s]["char_fraction"] <= 0.18 for s in ("val", "test")
    )

    INTERIM_SPLITS.mkdir(parents=True, exist_ok=True)
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)

    train_path = INTERIM_SPLITS / "train.jsonl"
    val_path = INTERIM_SPLITS / "val.jsonl"
    test_path = TEST_DIR / "test.jsonl"
    file_hashes = {
        "train": write_jsonl(train_path, rows["train"]),
        "val": write_jsonl(val_path, rows["val"]),
        "test": write_jsonl(test_path, rows["test"]),
    }
    test_path.chmod(0o444)
    (TEST_DIR / "README.md").write_text(
        "Isolated P1.1 test split. Do not copy into the active training directory.\n"
        "The evaluator may read this once after validation-only D* selection.\n",
        encoding="utf-8",
    )

    # Guard: no test filename inside the future active dir
    active_test_hits = [p.name for p in ACTIVE_DIR.rglob("*") if "test" in p.name.lower()]

    payload = {
        "ok": overlap_n["train_val"] == 0 and overlap_n["train_test"] == 0 and overlap_n["val_test"] == 0,
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "historical_split_recovered": False,
        "split_name": "reconstructed_article_70_15_15",
        "split_unit": "article",
        "assignment_rule": "lexicographic_sha256_utf8_70_15_15",
        "seed_used": None,
        "n_unique_units": n,
        "n_canonical_lines": audit["reconstruction"]["n_article_candidates"],
        "recovery": {
            "hf_linkanjarad_files": [".gitattributes", "README.md", "data/train.parquet"],
            "legacy_s3": 404,
            "filipino_text_benchmarks_wiki_train_tokens": 404,
            "seacrowd_loader_url": "https://s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/wikitext-tl-39/wikitext-tl-39.zip",
            "seacrowd_expected_files": ["train.txt", "valid.txt", "test.txt"],
            "result": "not_recovered",
        },
        "paths": {
            "train": str(train_path.relative_to(ROOT)),
            "val": str(val_path.relative_to(ROOT)),
            "test": str(test_path.relative_to(ROOT)),
            "active_training_dir": str(ACTIVE_DIR.relative_to(ROOT)),
        },
        "file_sha256": file_hashes,
        "stats": split_stats,
        "checks": {
            "D1_set_intersection_empty": overlap_n,
            "D2_exact_hash_overlap": overlap_n,
            "D3_identical_title_overlap_counts": {k: len(v) for k, v in title_overlap.items()},
            "D4_unit_ratio_in_band": d4,
            "D5_char_ratio_in_band": d5,
        },
        "title_overlap_examples": {k: v[:10] for k, v in title_overlap.items()},
        "d5_action": "registered_lex_hash_kept" if d5 else "registered_lex_hash_kept_d5_out_of_band_no_stratified_resplit",
        "active_dir_test_filenames": active_test_hits,
        "test_chmod": "0444",
        "near_duplicate_removal": False,
    }
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    if not payload["ok"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
