#!/usr/bin/env python3
"""Gate E: pack train/val articles into nanochat parquet shards. Test stays isolated."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
SPLIT = json.loads((ROOT / "manifests" / "split_manifest.json").read_text(encoding="utf-8"))
TRAIN_JSONL = ROOT / SPLIT["paths"]["train"]
VAL_JSONL = ROOT / SPLIT["paths"]["val"]
ACTIVE = ROOT / SPLIT["paths"]["active_training_dir"]
TEST_DIR = ROOT / "data" / "processed" / "wikitext-tl39" / "test"
VENDOR = ROOT / "vendor" / "nanochat"
PYTHON = VENDOR / ".venv" / "bin" / "python"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path, expected_sha: str) -> list[dict]:
    actual = sha256_file(path)
    if actual != expected_sha:
        raise SystemExit(f"hash mismatch {path}: {actual}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    rows.sort(key=lambda r: r["doc_id"])
    return rows


def chunk_document(rec: dict) -> list[dict]:
    text = rec["text"]
    if len(text) <= 50_000:
        return [rec]
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for line in text.splitlines(keepends=True):
        if len(line) > 10_000:
            if buf:
                chunks.append("".join(buf))
                buf, buf_len = [], 0
            for i in range(0, len(line), 10_000):
                chunks.append(line[i : i + 10_000])
            continue
        if buf and buf_len + len(line) > 10_000:
            chunks.append("".join(buf))
            buf, buf_len = [], 0
        buf.append(line)
        buf_len += len(line)
    if buf:
        chunks.append("".join(buf))
    out = []
    for k, chunk in enumerate(chunks):
        out.append(
            {
                "doc_id": f"{rec['doc_id']}#{k}",
                "parent_doc_id": rec["doc_id"],
                "text": chunk,
                "n_chars": len(chunk),
            }
        )
    return out


def write_shard(path: Path, texts: list[str]) -> dict:
    table = pa.Table.from_pydict({"text": texts})
    pq.write_table(
        table,
        path,
        row_group_size=1024,
        use_dictionary=False,
        compression="zstd",
        compression_level=3,
        write_statistics=False,
    )
    pf = pq.ParquetFile(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256_file(path),
        "n_rows": pf.metadata.num_rows,
        "n_row_groups": pf.metadata.num_row_groups,
        "schema": pf.schema_arrow.names,
        "compression": "zstd",
        "compression_level": 3,
        "row_group_size": 1024,
        "bytes": path.stat().st_size,
    }


def main() -> int:
    train_articles = load_jsonl(TRAIN_JSONL, SPLIT["file_sha256"]["train"])
    val_articles = load_jsonl(VAL_JSONL, SPLIT["file_sha256"]["val"])
    n_long = sum(1 for r in train_articles + val_articles if r["n_chars"] > 50_000)
    mid = len(train_articles) // 2
    groups_articles = {
        "shard_00000.parquet": train_articles[:mid],
        "shard_00001.parquet": train_articles[mid:],
        "shard_00002.parquet": val_articles,
    }
    groups = {name: [c for rec in recs for c in chunk_document(rec)] for name, recs in groups_articles.items()}

    ACTIVE.mkdir(parents=True, exist_ok=True)
    for stale in ACTIVE.glob("*.parquet"):
        stale.unlink()
    shard_meta = {}
    index = {}
    for name, recs in groups.items():
        texts = [r["text"] for r in recs]
        shard_meta[name] = write_shard(ACTIVE / name, texts)
        index[name] = {
            "role": "val" if name == "shard_00002.parquet" else "train",
            "chunk_ids": [r["doc_id"] for r in recs],
            "parent_doc_ids": [r.get("parent_doc_id", r["doc_id"]) for r in recs],
        }

    names = sorted(p.name for p in ACTIVE.iterdir() if p.suffix == ".parquet")
    e1 = names == ["shard_00000.parquet", "shard_00001.parquet", "shard_00002.parquet"]
    train_ids = {r["doc_id"] for r in train_articles}
    val_ids = {r["doc_id"] for r in val_articles}
    e2 = set(index["shard_00002.parquet"]["parent_doc_ids"]) == val_ids
    train_shard_parents = set(index["shard_00000.parquet"]["parent_doc_ids"]) | set(
        index["shard_00001.parquet"]["parent_doc_ids"]
    )
    e3 = train_shard_parents == train_ids and not (train_shard_parents & val_ids)

    pf0 = pq.ParquetFile(ACTIVE / "shard_00000.parquet")
    got0 = pf0.read().column("text").to_pylist()
    e4_train = got0[:10] == [r["text"] for r in groups["shard_00000.parquet"][:10]]
    pf2 = pq.ParquetFile(ACTIVE / "shard_00002.parquet")
    got2 = pf2.read().column("text").to_pylist()
    e4_val = got2[:10] == [r["text"] for r in groups["shard_00002.parquet"][:10]]

    test_hits = [p.name for p in ACTIVE.rglob("*") if "test" in p.name.lower()]
    test_dir_ok = TEST_DIR.is_dir() and not any(ACTIVE in p.parents or p.parent == ACTIVE for p in TEST_DIR.rglob("*") if False)
    isolated = (not test_hits) and TEST_DIR.is_dir() and not (ACTIVE / "test.jsonl").exists()

    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(ROOT / "data" / "cache" / "p1-20260816T025911Z-0067a57")
    env["NANOCHAT_DATA_DIR"] = str(ACTIVE)
    env["PYTHONPATH"] = str(VENDOR)
    probe = (
        "from nanochat.dataset import DATA_DIR, list_parquet_files; "
        "import os; "
        "paths = list_parquet_files(); "
        "print(DATA_DIR); "
        "print('\\n'.join(paths)); "
        "print('LAST', os.path.basename(paths[-1]) if paths else 'NONE')"
    )
    proc = subprocess.run(
        [str(PYTHON), "-c", probe],
        cwd=str(VENDOR),
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    lines = [ln for ln in proc.stdout.splitlines() if ln]
    last_is_val = lines[-1] == "LAST shard_00002.parquet"
    data_dir_ok = lines[0] == str(ACTIVE)

    climbmix = list((ROOT / "data" / "cache" / "p1-20260816T025911Z-0067a57").glob("base_data*"))

    payload = {
        "ok": all([e1, e2, e3, e4_train, e4_val, isolated, last_is_val, data_dir_ok, not climbmix]),
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "split_name": SPLIT["split_name"],
        "active_dir": str(ACTIVE.relative_to(ROOT)),
        "shards": shard_meta,
        "index_counts": {
            k: {
                "n_chunks": len(v["chunk_ids"]),
                "n_parent_articles": len(set(v["parent_doc_ids"])),
            }
            for k, v in index.items()
        },
        "n_articles_over_50000_chars": n_long,
        "checks": {
            "E1_names": e1,
            "E2_last_is_val_ids": e2,
            "E3_train_shards_train_only": e3,
            "E4_roundtrip_train": e4_train,
            "E4_roundtrip_val": e4_val,
            "E5_no_dataset_downloader_climbmix": climbmix == [],
            "test_absent_from_active": isolated,
            "fresh_process_DATA_DIR": data_dir_ok,
            "fresh_process_last_file_val": last_is_val,
        },
        "fresh_process_stdout": proc.stdout,
        "test_filenames_in_active": test_hits,
        "chunking_applied": n_long > 0,
        "padding_empty_strings": False,
        "test_not_packaged_into_active": True,
    }
    (ROOT / "manifests" / "shard_index.json").write_text(
        json.dumps(
            {
                k: {
                    "role": v["role"],
                    "n_chunks": len(v["chunk_ids"]),
                    "n_parent_articles": len(set(v["parent_doc_ids"])),
                    "parent_doc_ids_sha256": hashlib.sha256("\n".join(v["parent_doc_ids"]).encode()).hexdigest(),
                }
                for k, v in index.items()
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
