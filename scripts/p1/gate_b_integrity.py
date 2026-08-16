#!/usr/bin/env python3
"""Gate B integrity checks B1–B8. Does not mutate the raw parquet."""

from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "wikitext-tl39" / "train.parquet"
HEADER_RE = re.compile(r"^= [^=].* =$")
TAGALOG_WORDS = re.compile(r"(?<!\w)(ang|ng|sa|mga|na|ay)(?!\w)", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    checks = []
    failed = False

    def record(id_: str, ok: bool, detail) -> None:
        nonlocal failed
        checks.append({"id": id_, "ok": ok, "detail": detail})
        if not ok:
            failed = True

    record("B1", RAW.is_file(), str(RAW))
    if not RAW.is_file():
        json.dump({"ok": False, "checks": checks}, sys.stdout, indent=2)
        return 1

    header = RAW.read_bytes()[:4]
    record("B2", header == b"PAR1", header.decode("latin1", errors="replace"))

    size = RAW.stat().st_size
    expected = 119 * 1000 * 1000
    record("B3", abs(size - expected) / expected <= 0.10, {"bytes": size, "expected_about": expected})

    digest = sha256_file(RAW)
    pf = pq.ParquetFile(RAW)
    meta = pf.metadata
    schema = pf.schema_arrow
    names = list(schema.names)
    text_ok = "text" in names
    text_type = str(schema.field("text").type) if text_ok else None
    record("B4", meta.num_rows > 0, {"num_rows": meta.num_rows, "expected_about": 1_520_000})
    record("B5", text_ok and "string" in (text_type or "").lower(), {"columns": names, "text_type": text_type})

    empty = 0
    nonempty_indices = []
    moses = 0
    sample_pool = []
    rng = random.Random(20260816)
    for batch in pf.iter_batches(columns=["text"], batch_size=8192):
        texts = batch.column("text").to_pylist()
        for text in texts:
            if text is None or str(text).strip() == "":
                empty += 1
                continue
            s = str(text)
            if "@-@" in s or "@,@" in s:
                moses += 1
            if len(sample_pool) < 5000:
                sample_pool.append(s)
            elif rng.random() < 0.002:
                sample_pool[rng.randrange(len(sample_pool))] = s

    n = meta.num_rows
    empty_rate = empty / n if n else 1.0
    record("B6", empty_rate < 0.05, {"empty": empty, "n": n, "empty_rate": empty_rate})

    sniff_n = min(1000, len(sample_pool))
    sniff = rng.sample(sample_pool, sniff_n) if sniff_n else []
    hits = 0
    for s in sniff:
        if TAGALOG_WORDS.search(s) or HEADER_RE.search(s.splitlines()[0] if s else ""):
            hits += 1
        elif any(HEADER_RE.search(line) for line in s.splitlines()[:3]):
            hits += 1
    sniff_rate = hits / sniff_n if sniff_n else 0.0
    record("B7", sniff_rate >= 0.80, {"hits": hits, "n": sniff_n, "rate": sniff_rate})

    moses_n = min(1000, len(sample_pool))
    moses_sample = rng.sample(sample_pool, moses_n) if moses_n else []
    moses_hits = sum(1 for s in moses_sample if "@-@" in s or "@,@" in s)
    moses_rate = moses_hits / moses_n if moses_n else 0.0
    record(
        "B8",
        True,
        {
            "sample_hits": moses_hits,
            "sample_n": moses_n,
            "sample_rate": moses_rate,
            "full_pass_rows_with_moses": moses,
            "moses_tokenized_expected_if_sample_rate_gt_0.10": moses_rate > 0.10,
        },
    )

    payload = {
        "ok": not failed,
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": str(RAW.relative_to(ROOT)),
        "sha256": digest,
        "bytes": size,
        "num_rows": meta.num_rows,
        "num_row_groups": meta.num_row_groups,
        "schema": names,
        "text_type": text_type,
        "checks": checks,
    }
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
