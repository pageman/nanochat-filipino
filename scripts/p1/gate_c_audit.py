#!/usr/bin/env python3
"""Gate C audit. Reads the immutable parquet. Does not create the 70/15/15 split."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "wikitext-tl39" / "train.parquet"
SOURCE = ROOT / "manifests" / "source_manifest.json"
INTERIM = ROOT / "data" / "interim" / "wikitext-tl39"
HEADER_RE = re.compile(r"^= [^=\n][^\n]*? =$")
EXPECTED_SOURCE_SHA = "706d706496e3a085cf4506f97aa8b03faa20d4773d69453eaab4e3ca8f33caf9"
OVERLENGTH = 200_000
TABLE1_TRAIN_MOSES = 39_267_089


def lf_normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def percentile(sorted_vals: list[int], p: float) -> int:
    if not sorted_vals:
        return 0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    idx = min(len(sorted_vals) - 1, max(0, math.ceil(p * len(sorted_vals)) - 1))
    return sorted_vals[idx]


def is_header(text: str) -> bool:
    if "\n" in text.rstrip("\n"):
        return False
    return HEADER_RE.fullmatch(text.rstrip("\n")) is not None


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    file_sha = sha256_file(RAW)
    if file_sha != source["sha256"] or file_sha != EXPECTED_SOURCE_SHA:
        print(json.dumps({"ok": False, "error": "raw parquet hash mismatch", "actual": file_sha}), file=sys.stderr)
        return 1
    if RAW.stat().st_mode & 0o222:
        print(json.dumps({"ok": False, "error": "raw parquet is writable"}), file=sys.stderr)
        return 1

    INTERIM.mkdir(parents=True, exist_ok=True)
    canonical_path = INTERIM / "documents_canonical.jsonl"

    n_rows = 0
    n_null = 0
    n_empty = 0
    n_overlength = 0
    n_kept = 0
    n_short_lt_40 = 0
    n_header_rows = 0
    n_latin = 0
    n_digit = 0
    n_moses = 0
    unicode_major = Counter()
    token_counts = Counter()
    exact_hash_counts: Counter[str] = Counter()
    lengths: list[int] = []
    first_nonempty: list[str] = []
    last_nonempty: deque[str] = deque(maxlen=100)
    overlength_log: list[dict] = []

    articles: list[list[str]] = []
    current: list[str] = []
    preamble: list[str] = []
    seen_header = False
    rejected_fragments = 0

    pf = pq.ParquetFile(RAW)
    for batch in pf.iter_batches(columns=["text"], batch_size=8192):
        for raw in batch.column("text").to_pylist():
            n_rows += 1
            if raw is None:
                n_null += 1
                rejected_fragments += 1
                continue
            canon = lf_normalize(str(raw))
            if canon.strip() == "":
                n_empty += 1
                rejected_fragments += 1
                continue
            n_chars = len(canon)
            if n_chars > OVERLENGTH:
                n_overlength += 1
                rejected_fragments += 1
                overlength_log.append({"row_index": n_rows - 1, "n_chars": n_chars, "preview": canon[:120]})
                continue

            n_kept += 1
            if n_chars < 40:
                n_short_lt_40 += 1
            lengths.append(n_chars)
            if is_header(canon):
                n_header_rows += 1
            if any("A" <= ch <= "Z" or "a" <= ch <= "z" for ch in canon):
                n_latin += 1
            if any(ch.isdigit() for ch in canon):
                n_digit += 1
            if "@-@" in canon or "@,@" in canon:
                n_moses += 1
            for ch in canon:
                unicode_major[unicodedata.category(ch)[0]] += 1
            token_counts.update(canon.split())
            digest = sha256_bytes(canon.encode("utf-8"))
            exact_hash_counts[digest] += 1
            if len(first_nonempty) < 100:
                first_nonempty.append(canon)
            last_nonempty.append(canon)

            if is_header(canon):
                if not seen_header:
                    seen_header = True
                else:
                    articles.append(current)
                current = [canon]
            elif not seen_header:
                preamble.append(canon)
            else:
                current.append(canon)

    if current:
        articles.append(current)

    candidates = []
    empty_candidates = 0
    if preamble:
        pre_text = "\n".join(preamble)
        if pre_text.strip() == "":
            empty_candidates += 1
        else:
            candidates.append({"kind": "preamble", "text": pre_text})
    for art in articles:
        text = "\n".join(art)
        if text.strip() == "":
            empty_candidates += 1
        else:
            candidates.append({"kind": "article", "text": text})

    assigned_rows = sum(len(preamble) if True else 0 for _ in [0]) + sum(len(a) for a in articles)
    coverage_ok = assigned_rows == n_kept
    article_like = [c for c in candidates if c["kind"] == "article"]
    invariants = {
        "candidate_count_ge_1000": len(article_like) >= 1000,
        "coverage_every_kept_row_assigned": coverage_ok,
        "no_empty_candidate": empty_candidates == 0,
        "hash_ids_stable_sha256": True,
        "audit_statistics_present": True,
    }
    reconstruction_ok = all(invariants.values())
    split_unit = "article" if reconstruction_ok else "parquet_row"

    with canonical_path.open("w", encoding="utf-8") as out:
        if split_unit == "article":
            for cand in candidates:
                text = cand["text"]
                doc_id = sha256_bytes(text.encode("utf-8"))
                title = text.split("\n", 1)[0] if cand["kind"] == "article" else "preamble"
                rec = {
                    "doc_id": doc_id,
                    "title": title,
                    "kind": cand["kind"],
                    "text": text,
                    "n_chars": len(text),
                    "n_moses_tokens": len(text.split()),
                }
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        else:
            # Fallback canonical package is row-level; do not mix ids.
            pf2 = pq.ParquetFile(RAW)
            for batch in pf2.iter_batches(columns=["text"], batch_size=8192):
                for raw in batch.column("text").to_pylist():
                    if raw is None:
                        continue
                    canon = lf_normalize(str(raw))
                    if canon.strip() == "" or len(canon) > OVERLENGTH:
                        continue
                    rec = {
                        "doc_id": sha256_bytes(canon.encode("utf-8")),
                        "title": canon.split("\n", 1)[0][:200],
                        "kind": "row",
                        "text": canon,
                        "n_chars": len(canon),
                        "n_moses_tokens": len(canon.split()),
                    }
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    if split_unit == "article":
        t_moses = sum(len(c["text"].split()) for c in candidates)
        n_units = len(candidates)
    else:
        t_moses = sum(token_counts.values())
        n_units = n_kept

    lengths_sorted = sorted(lengths)
    duplicate_extra = sum(c - 1 for c in exact_hash_counts.values() if c > 1)
    duplicate_groups = sum(1 for c in exact_hash_counts.values() if c > 1)
    canary = sha256_bytes("".join(first_nonempty + list(last_nonempty)).encode("utf-8"))
    registered_drops = n_null + n_empty + n_overlength
    drop_rate = registered_drops / n_rows if n_rows else 1.0
    stop = drop_rate > 0.05
    moses_ratio = t_moses / TABLE1_TRAIN_MOSES if TABLE1_TRAIN_MOSES else None
    moses_status = "ok"
    if moses_ratio is not None:
        if moses_ratio < 0.1 or moses_ratio > 10:
            moses_status = "fail_factor_of_ten"
        elif moses_ratio < 0.5 or moses_ratio > 2:
            moses_status = "warning_factor_of_two"

    payload = {
        "ok": not stop and moses_status != "fail_factor_of_ten",
        "status": "stop" if stop else "pass",
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_sha256_verified": file_sha,
        "raw_writable": False,
        "canonical_normalization": "LF line endings only; no detokenize, NFC, language filter, or dedup",
        "registered_drop_rule": "null/empty after LF-normalize, or length > 200000 characters",
        "n_rows": n_rows,
        "n_null": n_null,
        "n_empty_after_lf": n_empty,
        "n_overlength": n_overlength,
        "n_kept": n_kept,
        "registered_drops": registered_drops,
        "registered_drop_rate": drop_rate,
        "n_short_lt_40_kept": n_short_lt_40,
        "note_short_rows": "Rows shorter than 40 characters are kept. They are not registered drops.",
        "length_chars": {
            "min": lengths_sorted[0] if lengths_sorted else 0,
            "median": percentile(lengths_sorted, 0.50),
            "mean": (sum(lengths_sorted) / len(lengths_sorted)) if lengths_sorted else 0,
            "p95": percentile(lengths_sorted, 0.95),
            "max": lengths_sorted[-1] if lengths_sorted else 0,
        },
        "unicode_major_categories": dict(unicode_major),
        "header_row_fraction": n_header_rows / n_kept if n_kept else 0,
        "n_header_rows": n_header_rows,
        "latin_letter_row_fraction": n_latin / n_kept if n_kept else 0,
        "digit_row_fraction": n_digit / n_kept if n_kept else 0,
        "moses_marker_row_fraction": n_moses / n_kept if n_kept else 0,
        "top50_whitespace_tokens": token_counts.most_common(50),
        "canary_sha256_first_last_100_nonempty": canary,
        "exact_duplicate_groups": duplicate_groups,
        "exact_duplicate_extra_copies": duplicate_extra,
        "near_duplicate_removal": False,
        "reconstruction": {
            "heading_regex": r"(?m)^= [^=\n][^\n]*? =$",
            "n_article_candidates": len(article_like),
            "n_preamble_rows": len(preamble),
            "n_units_written": n_units,
            "empty_candidates": empty_candidates,
            "rejected_fragments": rejected_fragments,
            "assigned_kept_rows": assigned_rows,
            "invariants": invariants,
            "reconstruction_ok": reconstruction_ok,
            "canonical_split_unit_recommendation": split_unit,
            "split_not_created": True,
        },
        "moses_census": {
            "T_moses_total": t_moses,
            "table1_train_moses": TABLE1_TRAIN_MOSES,
            "ratio_to_table1_train": moses_ratio,
            "status": moses_status,
        },
        "overlength_log": overlength_log,
        "canonical_jsonl": str(canonical_path.relative_to(ROOT)),
        "canonical_jsonl_sha256": sha256_file(canonical_path),
    }
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 2 if stop else 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
