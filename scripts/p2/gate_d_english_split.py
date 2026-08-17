#!/usr/bin/env python3
"""P2 Gate D: official WikiText-103 raw article split. MUST NOT re-hash 70/15/15."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
P2_RUN_ID = os.environ.get("P2_RUN_ID", "p2-20260817T150944Z-de99f8a")
RAW_DIR = ROOT / "data" / "raw" / "wikitext-103-raw" / "wikitext-103-raw-v1"
INTERIM = ROOT / "data" / "interim" / "wikitext-103"
OUT_JSON = ROOT / "docs" / "run-cards" / "p2" / P2_RUN_ID / "gate-d-english-split.json"
TL_TEST = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
P2_CACHE = ROOT / "data" / "cache" / P2_RUN_ID

HEADER_RE = re.compile(r"^= [^=\n][^\n]*? =$")
EXPECTED_TL_TEST_SHA = "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf"
TABLE1_ARTICLES = {"train": 28475, "val": 60, "test": 60}
TABLE1_TRAIN_MOSES = 103_227_021
SPLIT_NAME = "wikitext103_official_raw_splits"

PARQUETS = {
    "train": [
        (
            "train-00000-of-00002.parquet",
            "74da360f23826045b3e6ac6375411fdb15f003030aa74f2596ed08b857cb9212",
        ),
        (
            "train-00001-of-00002.parquet",
            "ba090ac30dbf5461e8dcbdd1a1b8e6f3cf9c2c756d64f0c1220450acd514f720",
        ),
    ],
    "val": [
        (
            "validation-00000-of-00001.parquet",
            "204929b7ff9d6184953f867dedb860e40aa69c078fc1e54b3baaa8fb28511c4c",
        ),
    ],
    "test": [
        (
            "test-00000-of-00001.parquet",
            "5f1bea067869d04849c0f975a2b29c4ff47d867f484f5010ea5e861eab246d91",
        ),
    ],
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def lf_normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def row_text(raw) -> str:
    if raw is None:
        return ""
    text = lf_normalize(str(raw))
    if text.endswith("\n"):
        text = text[:-1]
    return text


def is_loose_header(text: str) -> bool:
    return HEADER_RE.fullmatch(text.strip()) is not None


def iter_split_rows(split: str):
    for name, _expected in PARQUETS[split]:
        pf = pq.ParquetFile(RAW_DIR / name)
        for batch in pf.iter_batches(columns=["text"], batch_size=8192):
            for raw in batch.column("text").to_pylist():
                yield row_text(raw)


def iter_marked_rows(split: str):
    prev = None
    cur = None
    for nxt in iter_split_rows(split):
        if cur is not None:
            is_article = is_loose_header(cur) and (prev is None or prev.strip() == "") and nxt.strip() == ""
            yield cur, is_article
        prev, cur = cur, nxt
    if cur is not None:
        # EOF is not a following blank. Article headers in this dump are blank-delimited.
        yield cur, False


def writable_replace(path: Path) -> None:
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWUSR)


def freeze(path: Path) -> None:
    path.chmod(0o444)


def reconstruct_split(split: str, out_path: Path) -> dict:
    writable_replace(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    hasher = hashlib.sha256()
    n_rows = 0
    n_loose = 0
    n_articles = 0
    n_preamble_nonempty = 0
    n_chars = 0
    n_bytes = 0
    n_moses = 0
    doc_ids: list[str] = []
    titles: list[str] = []
    first_title = None
    last_title = None
    current: list[str] = []
    started = False
    preamble: list[str] = []

    def flush(lines: list[str]) -> None:
        nonlocal n_articles, n_chars, n_bytes, n_moses, first_title, last_title
        text = "\n".join(lines)
        title = text.split("\n", 1)[0].strip()
        doc_id = sha256_bytes(text.encode("utf-8"))
        rec = {
            "doc_id": doc_id,
            "title": title,
            "kind": "article",
            "split": split,
            "article_index": n_articles,
            "text": text,
            "n_chars": len(text),
            "n_bytes": len(text.encode("utf-8")),
            "n_moses_tokens": len(text.split()),
        }
        line = json.dumps(rec, ensure_ascii=False) + "\n"
        encoded = line.encode("utf-8")
        out.write(encoded)
        hasher.update(encoded)
        doc_ids.append(doc_id)
        titles.append(title)
        n_articles += 1
        n_chars += rec["n_chars"]
        n_bytes += rec["n_bytes"]
        n_moses += rec["n_moses_tokens"]
        if first_title is None:
            first_title = title
        last_title = title

    with out_path.open("wb") as out:
        for text, is_article in iter_marked_rows(split):
            n_rows += 1
            if is_loose_header(text):
                n_loose += 1
            if is_article:
                if started:
                    flush(current)
                started = True
                current = [text]
            elif started:
                current.append(text)
            else:
                preamble.append(text)
        if started and current:
            flush(current)

    freeze(out_path)
    n_preamble_nonempty = sum(1 for line in preamble if line.strip())
    return {
        "path": str(out_path.relative_to(ROOT)),
        "sha256": hasher.hexdigest(),
        "n_parquet_rows": n_rows,
        "n_loose_single_eq_headers": n_loose,
        "n_false_headers_kept_in_body": n_loose - n_articles,
        "n_documents": n_articles,
        "n_chars": n_chars,
        "n_bytes": n_bytes,
        "n_moses_tokens_whitespace": n_moses,
        "first_title": first_title,
        "last_title": last_title,
        "n_preamble_nonempty_lines": n_preamble_nonempty,
        "doc_ids": doc_ids,
        "titles": titles,
        "mode": oct(out_path.stat().st_mode & 0o777),
    }


def main() -> int:
    tl_before = sha256_file(TL_TEST) if TL_TEST.is_file() else None
    parquet_ok = []
    for split, files in PARQUETS.items():
        for name, expected in files:
            path = RAW_DIR / name
            got = sha256_file(path)
            parquet_ok.append({"file": name, "ok": got == expected, "sha256": got, "expected": expected})
    if not all(item["ok"] for item in parquet_ok):
        payload = {"status": "fail", "error": "Gate B parquet hash mismatch", "parquets": parquet_ok}
        OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "fail", "error": payload["error"]}, indent=2))
        return 1

    INTERIM.mkdir(parents=True, exist_ok=True)
    paths = {
        "train": INTERIM / "english_train.jsonl",
        "val": INTERIM / "english_val.jsonl",
        "test": INTERIM / "english_test.jsonl",
    }
    splits = {name: reconstruct_split(name, path) for name, path in paths.items()}

    id_sets = {name: set(splits[name]["doc_ids"]) for name in splits}
    title_sets = {name: set(splits[name]["titles"]) for name in splits}
    overlap_ids = {
        "train_val": sorted(id_sets["train"] & id_sets["val"]),
        "train_test": sorted(id_sets["train"] & id_sets["test"]),
        "val_test": sorted(id_sets["val"] & id_sets["test"]),
    }
    overlap_titles = {
        "train_val": sorted(title_sets["train"] & title_sets["val"]),
        "train_test": sorted(title_sets["train"] & title_sets["test"]),
        "val_test": sorted(title_sets["val"] & title_sets["test"]),
    }
    overlap_n = {k: len(v) for k, v in overlap_ids.items()}
    title_overlap_n = {k: len(v) for k, v in overlap_titles.items()}

    counts = {name: splits[name]["n_documents"] for name in splits}
    literature = {
        name: {
            "table1_articles": TABLE1_ARTICLES[name],
            "reconstructed": counts[name],
            "delta": counts[name] - TABLE1_ARTICLES[name],
        }
        for name in splits
    }
    val_test_match = counts["val"] == 60 and counts["test"] == 60
    disjoint = all(v == 0 for v in overlap_n.values())
    tl_after = sha256_file(TL_TEST) if TL_TEST.is_file() else None
    tl_untouched = tl_before == EXPECTED_TL_TEST_SHA and tl_after == EXPECTED_TL_TEST_SHA
    test_not_in_p2_cache = not list(P2_CACHE.rglob("english_test.jsonl")) if P2_CACHE.is_dir() else True
    used_tagalog_hash_split = False

    checks = [
        {"id": "D1_parquet_hashes_match_gate_b", "ok": True},
        {"id": "D2_disjoint_doc_ids", "ok": disjoint, "detail": overlap_n},
        {"id": "D3_val_test_article_count_60", "ok": val_test_match, "detail": {"val": counts["val"], "test": counts["test"]}},
        {"id": "D4_canonical_split_identity", "ok": True, "detail": SPLIT_NAME},
        {"id": "D5_did_not_rehash_701515", "ok": not used_tagalog_hash_split},
        {"id": "D6_tagalog_test_untouched", "ok": tl_untouched, "detail": {"sha256": tl_after}},
        {"id": "D7_english_test_not_in_p2_cache", "ok": test_not_in_p2_cache},
        {"id": "D8_no_preamble_documents", "ok": all(splits[n]["n_preamble_nonempty_lines"] == 0 for n in splits)},
    ]
    ok = all(c["ok"] for c in checks)

    public_splits = {}
    for name, rec in splits.items():
        public_splits[name] = {k: v for k, v in rec.items() if k not in {"doc_ids", "titles"}}

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "gate": "D",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p2_run_id": P2_RUN_ID,
        "script": "scripts/p2/gate_d_english_split.py",
        "split_name": SPLIT_NAME,
        "assignment_rule": "merity_official_train_valid_test",
        "seed_used": None,
        "used_tagalog_reconstructed_article_70_15_15": False,
        "header_rule": "LF-normalize parquet cell; drop one trailing record newline; article iff stripped line matches ^= [^=]+ =$ and previous and next rows are blank",
        "canonical_normalization": "LF line endings only; no detokenize, NFC, language filter, or dedup",
        "parquets": parquet_ok,
        "splits": public_splits,
        "document_counts": counts,
        "literature_table1": literature,
        "literature_train_moses_whitespace": {
            "table1": TABLE1_TRAIN_MOSES,
            "raw_reconstructed": splits["train"]["n_moses_tokens_whitespace"],
            "note": "Word-level paper Table 1 is Moses tokens on wikitext-103-v1. Raw BPE T_en_train is Gate G.",
        },
        "file_sha256": {name: splits[name]["sha256"] for name in splits},
        "overlap_doc_id_n": overlap_n,
        "overlap_title_n": title_overlap_n,
        "overlap_title_examples": {k: v[:10] for k, v in overlap_titles.items()},
        "checks": checks,
        "started_en0": False,
        "next_gate": "E",
        "next_gate_note": "Pack English train/val parquets (val last lexicographically). Read-only copy of frozen P1.1 Tagalog train. Freeze A3 mix before EN0. No GPU.",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "path": str(OUT_JSON.relative_to(ROOT)),
                "counts": counts,
                "overlap_doc_id_n": overlap_n,
                "file_sha256": payload["file_sha256"],
                "failed": [c["id"] for c in checks if not c["ok"]],
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
