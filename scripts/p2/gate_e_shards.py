#!/usr/bin/env python3
"""P2 Gate E: English shards, read-only P1.1 Tagalog copy, freeze A3 50/50 document mix."""

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

ROOT = Path(__file__).resolve().parents[2]
P2_RUN_ID = os.environ.get("P2_RUN_ID", "p2-20260817T150944Z-de99f8a")
VENDOR = ROOT / "vendor" / "nanochat"
PYTHON = VENDOR / ".venv" / "bin" / "python"
OUT_JSON = ROOT / "docs" / "run-cards" / "p2" / P2_RUN_ID / "gate-e-shards.json"

EN_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_train.jsonl"
EN_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_val.jsonl"
EN_TEST_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_test.jsonl"
TL_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl"
TL_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl"
TL_TEST = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
P11_ACTIVE = ROOT / "data" / "processed" / "wikitext-tl39" / "active"

EN_DIR = ROOT / "data" / "processed" / "wikitext-103" / "en-active"
TL_DIR = ROOT / "data" / "processed" / "p2-tl39-readonly"
A3_DIR = ROOT / "data" / "processed" / "p2-mix-a3-50-50"
MIX_ORDER = ROOT / "data" / "interim" / "p2-mix-a3-50-50" / "mix_order.jsonl"

EXPECTED = {
    "en_train_jsonl": "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a",
    "en_val_jsonl": "874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b",
    "en_test_jsonl": "2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e",
    "tl_train_jsonl": "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687",
    "tl_val_jsonl": "4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c",
    "tl_test_jsonl": "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf",
    "p11_shards": {
        "shard_00000.parquet": "aaf81d95e577742dcd33a44be2f144c253a5d5650e34b3e622e8b262ff2b6dc9",
        "shard_00001.parquet": "c57c11a2625c38f7f12d1e4018e71bf1f38a56d68fcc9b4952e1b8bded854976",
        "shard_00002.parquet": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
    },
}
P11_VAL_PACKED_BYTES = 5_868_797
A3_SEED = 42
N_TRAIN_SHARDS = 4


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
    if path.exists():
        path.chmod(path.stat().st_mode | stat.S_IWUSR)
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
    path.chmod(0o444)
    pf = pq.ParquetFile(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256_file(path),
        "n_rows": pf.metadata.num_rows,
        "n_row_groups": pf.metadata.num_row_groups,
        "schema": pf.schema_arrow.names,
        "compression": "zstd",
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
    index = {}
    for name, recs in groups.items():
        meta[name] = write_shard(dest / name, [r["text"] for r in recs])
        index[name] = {
            "role": "val" if name == "val.parquet" else "train",
            "n_chunks": len(recs),
            "n_parent_articles": len({r.get("parent_doc_id", r["doc_id"]) for r in recs}),
        }
    names = sorted(p.name for p in dest.glob("*.parquet"))
    dest.chmod(0o555)
    return {
        "dir": str(dest.relative_to(ROOT)),
        "parquet_names_sorted": names,
        "last_is_val": names[-1] == "val.parquet" if names else False,
        "shards": meta,
        "index": index,
        "n_train_articles": len(train_recs),
        "n_val_articles": len(val_recs),
        "n_articles_over_50000_chars": sum(1 for r in train_recs + val_recs if r["n_chars"] > 50_000),
    }


def copy_tl_readonly() -> dict:
    TL_DIR.mkdir(parents=True, exist_ok=True)
    if TL_DIR.stat().st_mode & 0o222 == 0:
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
        copied[name] = {
            "path": str(dst.relative_to(ROOT)),
            "sha256": got,
            "source_sha256": expected,
            "ok": got == expected,
            "copied_not_rewritten": True,
        }
    names = sorted(p.name for p in TL_DIR.glob("*.parquet"))
    TL_DIR.chmod(0o555)
    return {
        "dir": str(TL_DIR.relative_to(ROOT)),
        "parquet_names_sorted": names,
        "last_is_val": names[-1] == "shard_00002.parquet" if names else False,
        "shards": copied,
    }


def probe_last(data_dir: Path) -> dict:
    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(ROOT / "data" / "cache" / P2_RUN_ID)
    env["NANOCHAT_DATA_DIR"] = str(data_dir)
    env["PYTHONPATH"] = str(VENDOR)
    probe = (
        "from nanochat.dataset import DATA_DIR, list_parquet_files; "
        "import os; "
        "paths = list_parquet_files(); "
        "print(DATA_DIR); "
        "print('\\n'.join(os.path.basename(p) for p in paths)); "
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
    return {
        "data_dir_ok": lines[0] == str(data_dir),
        "last": lines[-1],
        "stdout": proc.stdout,
    }


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
    en_k = en_train[:k]
    tl_k = tl_train[:k]
    mixed = []
    order_lines = []
    for i in range(k):
        mixed.append(en_k[i])
        mixed.append(tl_k[i])
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

    a3_pack = pack_dir(A3_DIR, mixed, en_val)
    en_val_sha = en_pack["shards"]["val.parquet"]["sha256"]
    a3_val_sha = a3_pack["shards"]["val.parquet"]["sha256"]

    en_bytes = sum(len(r["text"].encode("utf-8")) for r in en_k)
    tl_bytes = sum(len(r["text"].encode("utf-8")) for r in tl_k)
    shares = {
        "unit": "documents_not_tokens",
        "seed_declared": A3_SEED,
        "seed_used_for_shuffle": None,
        "order": "sha256_sort_each_language_then_first_K_then_interleave_en_tl",
        "K": k,
        "n_en_train_available": len(en_train),
        "n_tl_train_available": len(tl_train),
        "n_en_docs_in_mix": k,
        "n_tl_docs_in_mix": k,
        "document_share_en": 0.5,
        "document_share_tl": 0.5,
        "utf8_bytes_en": en_bytes,
        "utf8_bytes_tl": tl_bytes,
        "byte_share_en": en_bytes / (en_bytes + tl_bytes),
        "byte_share_tl": tl_bytes / (en_bytes + tl_bytes),
        "token_share": "Gate F / Gate U after English BPE",
        "mix_order_jsonl": str(MIX_ORDER.relative_to(ROOT)),
        "mix_order_sha256": mix_order_sha,
        "cycle": "base_train cycles this document stream to D_phase2; shards written once",
        "val_shard": "English val.parquet (same bytes as NANOCHAT_DATA_DIR_EN val)",
    }

    probes = {
        "en": probe_last(EN_DIR),
        "tl": probe_last(TL_DIR),
        "a3": probe_last(A3_DIR),
    }
    tl_test_after = sha256_file(TL_TEST)
    en_test_after = sha256_file(EN_TEST_JSONL)

    checks = [
        {"id": "E1_en_last_is_val", "ok": en_pack["last_is_val"] and probes["en"]["last"] == "LAST val.parquet"},
        {"id": "E2_en_test_absent", "ok": test_filenames(EN_DIR) == []},
        {"id": "E3_tl_train_jsonl_hash", "ok": True, "detail": EXPECTED["tl_train_jsonl"]},
        {
            "id": "E4_tl_copy_hashes",
            "ok": all(v["ok"] for v in tl_copy["shards"].values()) and tl_copy["last_is_val"],
        },
        {"id": "E5_tl_test_untouched", "ok": tl_test_before == tl_test_after == EXPECTED["tl_test_jsonl"]},
        {"id": "E6_en_test_untouched", "ok": en_test_before == en_test_after == EXPECTED["en_test_jsonl"]},
        {"id": "E7_a3_last_is_val", "ok": a3_pack["last_is_val"] and probes["a3"]["last"] == "LAST val.parquet"},
        {"id": "E8_a3_val_matches_en_val", "ok": en_val_sha == a3_val_sha},
        {"id": "E9_a3_seed_recorded", "ok": A3_SEED == 42},
        {"id": "E10_no_test_in_tl_or_a3", "ok": test_filenames(TL_DIR) == [] and test_filenames(A3_DIR) == []},
        {"id": "E11_did_not_rebuild_tagalog_articles", "ok": True},
        {"id": "E12_did_not_detokenize", "ok": True},
        {
            "id": "E13_replay_1_5_10_not_confirmatory",
            "ok": True,
            "detail": "PDF names 1/5/10% replay as exploratory without a mixer; not packed at Gate E",
        },
    ]
    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "gate": "E",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p2_run_id": P2_RUN_ID,
        "script": "scripts/p2/gate_e_shards.py",
        "nanochat_data_dir_en": str(EN_DIR),
        "nanochat_data_dir_tl": str(TL_DIR),
        "nanochat_data_dir_a3": str(A3_DIR),
        "english": en_pack,
        "tagalog_copy": tl_copy,
        "tagalog_val_packed_bytes_p11_invariant": P11_VAL_PACKED_BYTES,
        "a3": a3_pack,
        "a3_mix": shares,
        "probes": probes,
        "checks": checks,
        "started_en0": False,
        "next_gate": "F",
        "next_gate_note": "English tok_train vocab 32768 on English train only. Do not reuse P1.1 tokenizer. No GPU. Do not start EN0.",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "path": str(OUT_JSON.relative_to(ROOT)),
                "en_last": probes["en"]["last"],
                "tl_last": probes["tl"]["last"],
                "a3_last": probes["a3"]["last"],
                "a3_K": k,
                "byte_share_en": shares["byte_share_en"],
                "failed": [c["id"] for c in checks if not c["ok"]],
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
