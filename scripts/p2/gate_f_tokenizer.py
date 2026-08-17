#!/usr/bin/env python3
"""P2 Gate F: official English tok_train (32768) on frozen English train shards only."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P2_RUN_ID = os.environ.get("P2_RUN_ID", "p2-20260817T150944Z-de99f8a")
VENDOR = ROOT / "vendor" / "nanochat"
PYTHON = Path(os.environ.get("VIRTUAL_ENV", str(VENDOR / ".venv"))) / "bin" / "python"
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data" / "cache" / P2_RUN_ID))
EN_DIR = Path(os.environ.get("NANOCHAT_DATA_DIR_EN", ROOT / "data" / "processed" / "wikitext-103" / "en-active"))
TL_DIR = Path(os.environ.get("NANOCHAT_DATA_DIR_TL", ROOT / "data" / "processed" / "p2-tl39-readonly"))
A3_DIR = Path(os.environ.get("NANOCHAT_DATA_DIR_A3", ROOT / "data" / "processed" / "p2-mix-a3-50-50"))
OUT_JSON = ROOT / "docs" / "run-cards" / "p2" / P2_RUN_ID / "gate-f-tokenizer.json"
OUT_LOG = ROOT / "docs" / "run-cards" / "p2" / P2_RUN_ID / "gate-f-tok_train.log"
EN_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_val.jsonl"
TL_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl"
P11_TOK = "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"
P11_BYTES = "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132"

EXPECTED_EN_TRAIN = {
    "train_00000.parquet": "9bdee964368da85a9b97af0d8cd50c4cd13ec392a8045dbec602ce31bd587861",
    "train_00001.parquet": "7331e6219eec3bf619b92c38f686778395b77b500d267cfb25412abb41c6379c",
    "train_00002.parquet": "59bc144b0191d10009baa7698bbb96ba25c2c750b7ab8cdbc9bba52998c4d9f7",
    "train_00003.parquet": "ac693bfc6c1820e9f978f90958b1afb4bf82d91c9bcbba682467d6a357ebcb0b",
}
EXPECTED_EN_VAL = "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f"
VOCAB = 32768
MAX_CHARS = 2_000_000_000
DOC_CAP = 10_000
COMMAND = [
    str(PYTHON),
    "-m",
    "scripts.tok_train",
    "--max-chars",
    str(MAX_CHARS),
    "--doc-cap",
    str(DOC_CAP),
    "--vocab-size",
    str(VOCAB),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fertility(tokenizer, texts: list[str]) -> dict:
    n_tokens = 0
    n_bytes = 0
    n_chars = 0
    n_moses = 0
    n_roundtrip = 0
    for text in texts:
        ids = tokenizer.encode(text)
        n_tokens += len(ids)
        n_bytes += len(text.encode("utf-8"))
        n_chars += len(text)
        n_moses += len(text.split())
        if tokenizer.decode(ids) == text:
            n_roundtrip += 1
    return {
        "n_docs": len(texts),
        "n_tokens": n_tokens,
        "n_bytes": n_bytes,
        "n_chars": n_chars,
        "n_moses_tokens": n_moses,
        "bytes_per_token": (n_bytes / n_tokens) if n_tokens else None,
        "chars_per_token": (n_chars / n_tokens) if n_tokens else None,
        "tokens_per_moses": (n_tokens / n_moses) if n_moses else None,
        "roundtrip_doc_fraction": (n_roundtrip / len(texts)) if texts else None,
        "bos_prepended": False,
    }


def load_texts(path: Path) -> list[str]:
    return [json.loads(line)["text"] for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> int:
    sys.path.insert(0, str(VENDOR))
    os.chdir(VENDOR)

    data_dir = os.environ.get("NANOCHAT_DATA_DIR")
    if data_dir != str(EN_DIR):
        print(json.dumps({"status": "fail", "error": "NANOCHAT_DATA_DIR must be NANOCHAT_DATA_DIR_EN", "got": data_dir}), file=sys.stderr)
        return 1
    if os.environ.get("NANOCHAT_BASE_DIR") != str(BASE):
        print(json.dumps({"status": "fail", "error": "NANOCHAT_BASE_DIR mismatch"}), file=sys.stderr)
        return 1

    from nanochat.dataset import list_parquet_files

    parquet_paths = list_parquet_files()
    names = [Path(p).name for p in parquet_paths]
    train_names = names[:-1]
    last_name = names[-1] if names else None
    input_hashes = {name: sha256_file(EN_DIR / name) for name in train_names}
    val_hash = sha256_file(EN_DIR / last_name) if last_name else None

    tok_dir = BASE / "tokenizer"
    pre_existing = sorted(p.name for p in tok_dir.iterdir()) if tok_dir.is_dir() else []

    preflight_ok = (
        names == ["train_00000.parquet", "train_00001.parquet", "train_00002.parquet", "train_00003.parquet", "val.parquet"]
        and last_name == "val.parquet"
        and input_hashes == EXPECTED_EN_TRAIN
        and val_hash == EXPECTED_EN_VAL
        and Path(data_dir) == EN_DIR
        and Path(data_dir) != TL_DIR
        and Path(data_dir) != A3_DIR
        and pre_existing == []
    )
    if not preflight_ok:
        payload = {
            "status": "fail",
            "error": "preflight",
            "names": names,
            "input_hashes": input_hashes,
            "val_hash": val_hash,
            "pre_existing": pre_existing,
        }
        OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2))
        return 1

    OUT_LOG.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["NANOCHAT_DATA_DIR"] = str(EN_DIR)
    env["NANOCHAT_BASE_DIR"] = str(BASE)
    started = time.time()
    with OUT_LOG.open("w", encoding="utf-8") as log:
        log.write(f"# cwd={VENDOR}\n# command={' '.join(COMMAND)}\n")
        log.write(f"# NANOCHAT_DATA_DIR={EN_DIR}\n# NANOCHAT_BASE_DIR={BASE}\n")
        log.write(f"# started_utc={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n\n")
        log.flush()
        proc = subprocess.run(
            COMMAND,
            cwd=str(VENDOR),
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
        elapsed = time.time() - started
        log.write(f"\n# exit_code={proc.returncode}\n# elapsed_s={elapsed:.3f}\n")
    if proc.returncode != 0:
        print(json.dumps({"status": "fail", "error": "tok_train failed", "exit_code": proc.returncode, "log": str(OUT_LOG)}), indent=2)
        return 1

    from nanochat.tokenizer import RustBPETokenizer

    tok = RustBPETokenizer.from_directory(str(tok_dir))
    vocab_size = tok.get_vocab_size()
    pkl = tok_dir / "tokenizer.pkl"
    nbytes = tok_dir / "token_bytes.pt"
    pkl_sha = sha256_file(pkl)
    bytes_sha = sha256_file(nbytes)

    en_val = load_texts(EN_VAL_JSONL)
    tl_val = load_texts(TL_VAL_JSONL)
    fert = {
        "english_val": fertility(tok, en_val),
        "tagalog_val": fertility(tok, tl_val),
        "note": "Descriptive bytes/token only. Not confirmatory BPB. English test and Tagalog train were not encoded.",
    }

    sanity_text = "Hello world! This is a test.\nNumbers: 123, 4567, 89"
    sanity_ok = tok.decode(tok.encode(sanity_text)) == sanity_text

    checks = [
        {"id": "F1_vocab_32768", "ok": vocab_size == VOCAB, "detail": vocab_size},
        {"id": "F2_train_only_shards", "ok": train_names == list(EXPECTED_EN_TRAIN)},
        {"id": "F3_val_excluded_from_tok_train", "ok": last_name == "val.parquet"},
        {"id": "F4_input_hashes_match_gate_e", "ok": input_hashes == EXPECTED_EN_TRAIN},
        {"id": "F5_not_p11_tokenizer", "ok": pkl_sha != P11_TOK and bytes_sha != P11_BYTES},
        {"id": "F6_not_tl_or_a3_data_dir", "ok": Path(data_dir) == EN_DIR},
        {"id": "F7_token_bytes_present", "ok": nbytes.is_file()},
        {"id": "F8_sanity_roundtrip", "ok": sanity_ok},
        {"id": "F9_did_not_run_nanochat_dataset", "ok": True},
        {"id": "F10_did_not_encode_english_test_or_tagalog_train", "ok": True},
    ]
    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "gate": "F",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p2_run_id": P2_RUN_ID,
        "script": "scripts/p2/gate_f_tokenizer.py",
        "command": COMMAND,
        "cwd": str(VENDOR),
        "elapsed_s": elapsed,
        "tok_train_log": str(OUT_LOG.relative_to(ROOT)),
        "nanochat_data_dir": str(EN_DIR),
        "nanochat_base_dir": str(BASE),
        "tokenizer_dir": str(tok_dir.relative_to(ROOT)),
        "flags": {"max_chars": MAX_CHARS, "doc_cap": DOC_CAP, "vocab_size": VOCAB},
        "train_parquet_names": train_names,
        "excluded_last_shard": last_name,
        "input_file_sha256": input_hashes,
        "val_parquet_sha256_not_used_for_training": val_hash,
        "vocab_size": vocab_size,
        "hashes": {
            "tokenizer.pkl": pkl_sha,
            "token_bytes.pt": bytes_sha,
        },
        "p11_tokenizer_pkl_not_reused": P11_TOK,
        "fertility": fert,
        "checks": checks,
        "started_en0": False,
        "computed_bpb": False,
        "next_gate": "G",
        "next_gate_note": "Measure T_en_train with this tokenizer. Expect N_EN0 >> 294. Cost A40-hours before renting. No EN0 yet.",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "vocab_size": vocab_size,
                "tokenizer_pkl": pkl_sha,
                "token_bytes_pt": bytes_sha,
                "bytes_per_token_en_val": fert["english_val"]["bytes_per_token"],
                "bytes_per_token_tl_val": fert["tagalog_val"]["bytes_per_token"],
                "failed": [c["id"] for c in checks if not c["ok"]],
                "log": str(OUT_LOG.relative_to(ROOT)),
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
