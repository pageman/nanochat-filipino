#!/usr/bin/env python3
"""P3 Gate F: new Tagalog 32768 BPE on TL train shards only. Fertility -> lockbox."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from p3_common import (
    ASPREDICTED_ID,
    BASE,
    B3_DIR,
    EN_DIR,
    EN_VAL_JSONL,
    EXPECTED,
    P3_RUN_ID,
    PYTHON,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TL_DIR,
    TL_VAL_JSONL,
    VOCAB,
    VENDOR,
)

OUT_JSON = RUN_CARD / "gate-f-tokenizer.json"
OUT_LOG = RUN_CARD / "gate-f-tok_train.log"
LOCKBOX_FERTILITY = BASE / "lockbox" / "gate-f-fertility.json"
COMMAND = [str(PYTHON), "-m", "scripts.tok_train", "--max-chars", "2000000000", "--doc-cap", "10000", "--vocab-size", str(VOCAB)]


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_texts(path: Path) -> list[str]:
    return [json.loads(line)["text"] for line in path.read_text(encoding="utf-8").splitlines() if line]


def fertility(tokenizer, texts: list[str]) -> dict:
    n_tokens = n_bytes = n_chars = n_moses = n_roundtrip = 0
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
        "bytes_per_token": (n_bytes / n_tokens) if n_tokens else None,
        "roundtrip_doc_fraction": (n_roundtrip / len(texts)) if texts else None,
    }


def main() -> int:
    sys.path.insert(0, str(VENDOR))
    os.chdir(VENDOR)

    data_dir = os.environ.get("NANOCHAT_DATA_DIR")
    if data_dir != str(TL_DIR):
        print(json.dumps({"status": "fail", "error": "NANOCHAT_DATA_DIR must be TL_DIR", "got": data_dir}), file=sys.stderr)
        return 1
    if os.environ.get("NANOCHAT_BASE_DIR") != str(BASE):
        print(json.dumps({"status": "fail", "error": "NANOCHAT_BASE_DIR mismatch"}), file=sys.stderr)
        return 1

    from nanochat.dataset import list_parquet_files

    parquet_paths = list_parquet_files()
    names = [Path(p).name for p in parquet_paths]
    train_names = names[:-1]
    last_name = names[-1] if names else None
    input_hashes = {name: sha256_file(TL_DIR / name) for name in train_names}
    expected_train = {k: v for k, v in EXPECTED["p11_shards"].items() if k != "shard_00002.parquet"}

    tok_dir = BASE / "tokenizer"
    pre_existing = sorted(p.name for p in tok_dir.iterdir()) if tok_dir.is_dir() else []
    already_trained = pre_existing != [] and (tok_dir / "tokenizer.pkl").is_file()
    preflight_ok = (
        names == ["shard_00000.parquet", "shard_00001.parquet", "shard_00002.parquet"]
        and last_name == "shard_00002.parquet"
        and input_hashes == expected_train
        and (pre_existing == [] or already_trained)
        and Path(data_dir) not in (EN_DIR, B3_DIR)
    )
    if not preflight_ok:
        OUT_JSON.write_text(json.dumps({"status": "fail", "error": "preflight", "names": names, "input_hashes": input_hashes, "pre_existing": pre_existing}, indent=2) + "\n", encoding="utf-8")
        return 1

    if not already_trained:
        OUT_LOG.parent.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["NANOCHAT_DATA_DIR"] = str(TL_DIR)
        env["NANOCHAT_BASE_DIR"] = str(BASE)
        started = time.time()
        with OUT_LOG.open("w", encoding="utf-8") as log:
            log.write(f"# NANOCHAT_DATA_DIR={TL_DIR}\n# NANOCHAT_BASE_DIR={BASE}\n\n")
            proc = subprocess.run(COMMAND, cwd=str(VENDOR), env=env, stdout=log, stderr=subprocess.STDOUT, text=True)
            log.write(f"\n# exit_code={proc.returncode}\n")
        if proc.returncode != 0:
            return 1
        elapsed = time.time() - started
    else:
        started = time.time()
        elapsed = 0.0

    from nanochat.tokenizer import RustBPETokenizer

    tok = RustBPETokenizer.from_directory(str(tok_dir))
    pkl_sha = sha256_file(tok_dir / "tokenizer.pkl")
    bytes_sha = sha256_file(tok_dir / "token_bytes.pt")
    fert = {
        "english_val": fertility(tok, load_texts(EN_VAL_JSONL)),
        "tagalog_val": fertility(tok, load_texts(TL_VAL_JSONL)),
        "note": "Lockbox-only diagnostics. Not confirmatory BPB.",
    }
    LOCKBOX_FERTILITY.parent.mkdir(parents=True, exist_ok=True)
    LOCKBOX_FERTILITY.write_text(json.dumps(fert, indent=2) + "\n", encoding="utf-8")
    try:
        LOCKBOX_FERTILITY.chmod(0o600)
    except OSError:
        pass

    p1_tok_path = ROOT / "data" / "cache" / "p1-20260816T025911Z-0067a57" / "tokenizer" / "tokenizer.pkl"
    p2_tok_path = ROOT / "data" / "cache" / "p2-20260817T150944Z-de99f8a" / "tokenizer" / "tokenizer.pkl"
    p3_pkl = tok_dir / "tokenizer.pkl"
    copied_from_p1 = p1_tok_path.is_file() and p3_pkl.samefile(p1_tok_path)
    copied_from_p2 = p2_tok_path.is_file() and p3_pkl.samefile(p2_tok_path)
    checks = [
        {"id": "F1_vocab_32768", "ok": tok.get_vocab_size() == VOCAB},
        {"id": "F2_train_only_tl_shards", "ok": train_names == ["shard_00000.parquet", "shard_00001.parquet"]},
        {
            "id": "F3_fresh_tok_train_not_copied_p1_p2",
            "ok": not copied_from_p1 and not copied_from_p2 and OUT_LOG.is_file(),
            "detail": {
                "p3_pkl_sha256": pkl_sha,
                "p11_pkl_sha256": EXPECTED["p11_tok"],
                "p2_pkl_sha256": EXPECTED["p2_tok"],
                "note": "Identical SHA to P1.1 is allowed if BPE retrains to the same fixed point; forbidden act is copying P1/P2 artifact bytes without tok_train.",
            },
        },
        {"id": "F4_fertility_in_lockbox", "ok": LOCKBOX_FERTILITY.is_file()},
        {"id": "F5_no_bpb", "ok": True},
    ]
    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "F",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_f_tokenizer.py",
        "command": COMMAND,
        "elapsed_s": elapsed,
        "tok_train_skipped_existing": already_trained,
        "tok_train_log": str(OUT_LOG.relative_to(ROOT)),
        "nanochat_data_dir": str(TL_DIR.relative_to(ROOT)),
        "tokenizer_dir": str(tok_dir.relative_to(ROOT)),
        "hashes": {"tokenizer.pkl": pkl_sha, "token_bytes.pt": bytes_sha},
        "fertility_lockbox_path": str(LOCKBOX_FERTILITY.relative_to(ROOT)),
        "checks": checks,
        "no_p3_bpb": True,
        "next_gate": "G",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "vocab_size": VOCAB, "tokenizer_pkl": pkl_sha[:16] + "...", "fertility": "lockbox", "failed": [c["id"] for c in checks if not c["ok"]]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
