"""Shared parquet packing for P4 C1/C2/C3. Document text only. No BPB."""

from __future__ import annotations

import os
import stat
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from p4_common import N_TRAIN_SHARDS, ROOT, sha256_file


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
        out.append({"doc_id": f"{rec['doc_id']}#{k}", "parent_doc_id": rec["doc_id"], "text": chunk, "n_chars": len(chunk)})
    return out


def write_shard(path: Path, texts: list[str]) -> dict:
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWUSR)
    table = pa.Table.from_pydict({"text": texts})
    pq.write_table(table, path, row_group_size=1024, use_dictionary=False, compression="zstd", compression_level=3, write_statistics=False)
    path.chmod(0o444)
    pf = pq.ParquetFile(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256_file(path),
        "n_rows": pf.metadata.num_rows,
        "bytes": path.stat().st_size,
        "utf8_bytes": sum(len(t.encode("utf-8")) for t in texts),
    }


def split_named(prefix: str, n: int, recs: list[dict]) -> dict[str, list[dict]]:
    if n <= 1:
        return {f"{prefix}_00000.parquet": recs}
    size = (len(recs) + n - 1) // n
    out = {}
    for i in range(n):
        chunk = recs[i * size : (i + 1) * size]
        if chunk:
            out[f"{prefix}_{i:05d}.parquet"] = chunk
    return out


def pack_dir(dest: Path, train_recs: list[dict], val_recs: list[dict]) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    dest.chmod(dest.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
    for stale in dest.glob("*.parquet"):
        stale.chmod(stale.stat().st_mode | stat.S_IWUSR)
        stale.unlink()
    train_chunks = [c for rec in train_recs for c in chunk_document(rec)]
    val_chunks = [c for rec in val_recs for c in chunk_document(rec)]
    groups = split_named("train", N_TRAIN_SHARDS, train_chunks)
    groups["val.parquet"] = val_chunks
    meta = {}
    for name, recs in groups.items():
        meta[name] = write_shard(dest / name, [r["text"] for r in recs])
    names = sorted(p.name for p in dest.glob("*.parquet"))
    dest.chmod(0o555)
    return {"dir": str(dest.relative_to(ROOT)), "parquet_names_sorted": names, "last_is_val": names[-1] == "val.parquet", "shards": meta}
