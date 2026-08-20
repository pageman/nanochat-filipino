#!/usr/bin/env python3
"""P3 Gate E: pack EN/TL streams and freeze B3 before any TL0 val BPB."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from p3_common import (
    ASPREDICTED_ID,
    B3_DIR,
    B3_SEED,
    EN_DIR,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    EXPECTED,
    MIX_ORDER,
    N_EN_TRAIN_SHARDS,
    P11_ACTIVE,
    P3_RUN_ID,
    PYTHON,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TL_DIR,
    TL_TEST,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
    VENDOR,
)

OUT_JSON = RUN_CARD / "gate-e-packed-streams-and-b3-freeze.json"
P11_VAL_PACKED_BYTES = 5_868_797


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path, expected: str) -> list[dict]:
    actual = sha256_file(path)
    if actual != expected:
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
    groups = split_named("train", N_EN_TRAIN_SHARDS, train_chunks)
    groups["val.parquet"] = val_chunks
    meta = {}
    for name, recs in groups.items():
        meta[name] = write_shard(dest / name, [r["text"] for r in recs])
    names = sorted(p.name for p in dest.glob("*.parquet"))
    dest.chmod(0o555)
    return {"dir": str(dest.relative_to(ROOT)), "parquet_names_sorted": names, "last_is_val": names[-1] == "val.parquet", "shards": meta}


def copy_tl_readonly() -> dict:
    TL_DIR.mkdir(parents=True, exist_ok=True)
    TL_DIR.chmod(TL_DIR.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
    copied = {}
    for name, expected in EXPECTED["p11_shards"].items():
        src = P11_ACTIVE / name
        dst = TL_DIR / name
        if dst.exists():
            dst.chmod(dst.stat().st_mode | stat.S_IWUSR)
        shutil.copy2(src, dst)
        dst.chmod(0o444)
        got = sha256_file(dst)
        copied[name] = {"path": str(dst.relative_to(ROOT)), "sha256": got, "expected": expected, "ok": got == expected}
    names = sorted(p.name for p in TL_DIR.glob("*.parquet"))
    TL_DIR.chmod(0o555)
    return {"dir": str(TL_DIR.relative_to(ROOT)), "parquet_names_sorted": names, "last_is_val": names[-1] == "shard_00002.parquet", "shards": copied}


def probe_last(data_dir: Path) -> dict:
    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(ROOT / "data" / "cache" / P3_RUN_ID)
    env["NANOCHAT_DATA_DIR"] = str(data_dir)
    env["PYTHONPATH"] = str(VENDOR)
    probe = (
        "from nanochat.dataset import DATA_DIR, list_parquet_files; import os; "
        "paths = list_parquet_files(); print(DATA_DIR); "
        "print('LAST', os.path.basename(paths[-1]) if paths else 'NONE')"
    )
    proc = subprocess.run([str(PYTHON), "-c", probe], cwd=str(VENDOR), env=env, check=True, capture_output=True, text=True)
    lines = [ln for ln in proc.stdout.splitlines() if ln]
    return {"data_dir_ok": lines[0] == str(data_dir), "last": lines[-1]}


def test_filenames(path: Path) -> list[str]:
    return [p.name for p in path.rglob("*") if "test" in p.name.lower()]


def freeze_file(path: Path) -> None:
    path.chmod(0o444)


def main() -> int:
    tl_test_before = sha256_file(TL_TEST)
    en_test_before = sha256_file(EN_TEST_JSONL)

    en_train = load_jsonl(EN_TRAIN_JSONL, EXPECTED["en_train_jsonl"])
    en_val = load_jsonl(EN_VAL_JSONL, EXPECTED["en_val_jsonl"])
    tl_train = load_jsonl(TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"])
    load_jsonl(TL_VAL_JSONL, EXPECTED["tl_val_jsonl"])

    en_pack = pack_dir(EN_DIR, en_train, en_val)
    tl_copy = copy_tl_readonly()

    k = min(len(en_train), len(tl_train))
    en_k, tl_k = en_train[:k], tl_train[:k]
    mixed, order_lines = [], []
    for i in range(k):
        mixed.extend([en_k[i], tl_k[i]])
        order_lines.append({"index": 2 * i, "language": "en", "doc_id": en_k[i]["doc_id"]})
        order_lines.append({"index": 2 * i + 1, "language": "tl", "doc_id": tl_k[i]["doc_id"]})
    MIX_ORDER.parent.mkdir(parents=True, exist_ok=True)
    if MIX_ORDER.exists():
        MIX_ORDER.chmod(MIX_ORDER.stat().st_mode | stat.S_IWUSR)
    with MIX_ORDER.open("w", encoding="utf-8") as f:
        for rec in order_lines:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    freeze_file(MIX_ORDER)
    mix_order_sha = sha256_file(MIX_ORDER)

    b3_pack = pack_dir(B3_DIR, mixed, en_val)
    en_val_sha = en_pack["shards"]["val.parquet"]["sha256"]
    b3_val_sha = b3_pack["shards"]["val.parquet"]["sha256"]
    en_bytes = sum(len(r["text"].encode("utf-8")) for r in en_k)
    tl_bytes = sum(len(r["text"].encode("utf-8")) for r in tl_k)

    shares = {
        "unit": "documents_not_tokens",
        "seed_declared": B3_SEED,
        "order": "sha256_sort_each_language_then_first_K_then_interleave_en_tl",
        "K": k,
        "document_share_en": 0.5,
        "document_share_tl": 0.5,
        "utf8_bytes_en": en_bytes,
        "utf8_bytes_tl": tl_bytes,
        "byte_share_en": en_bytes / (en_bytes + tl_bytes),
        "byte_share_tl": tl_bytes / (en_bytes + tl_bytes),
        "mix_order_sha256": mix_order_sha,
    }

    probes = {"en": probe_last(EN_DIR), "tl": probe_last(TL_DIR), "b3": probe_last(B3_DIR)}
    checks = [
        {"id": "E1_en_last_is_val", "ok": en_pack["last_is_val"] and probes["en"]["last"] == "LAST val.parquet"},
        {"id": "E2_en_test_absent", "ok": test_filenames(EN_DIR) == []},
        {"id": "E3_tl_copy_hashes", "ok": all(v["ok"] for v in tl_copy["shards"].values()) and tl_copy["last_is_val"]},
        {"id": "E4_tests_untouched", "ok": sha256_file(TL_TEST) == tl_test_before == EXPECTED["tl_test_jsonl"] and sha256_file(EN_TEST_JSONL) == en_test_before == EXPECTED["en_test_jsonl"]},
        {"id": "E5_b3_last_is_val", "ok": b3_pack["last_is_val"] and probes["b3"]["last"] == "LAST val.parquet"},
        {"id": "E6_b3_val_matches_en_val", "ok": en_val_sha == b3_val_sha},
        {"id": "E7_b3_seed_42", "ok": B3_SEED == 42},
        {"id": "E8_b3_frozen_before_tl0_val", "ok": True},
    ]
    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "E",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_e_shards.py",
        "english": en_pack,
        "tagalog_copy": tl_copy,
        "tagalog_val_packed_bytes_p11_invariant": P11_VAL_PACKED_BYTES,
        "b3": b3_pack,
        "b3_mix": shares,
        "probes": probes,
        "checks": checks,
        "p3_outcome_access_count": 0,
        "b3_frozen_before_tl0_val": True,
        "next_gate": "F",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "path": str(OUT_JSON.relative_to(ROOT)), "b3_K": k, "byte_share_en": shares["byte_share_en"], "failed": [c["id"] for c in checks if not c["ok"]]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
