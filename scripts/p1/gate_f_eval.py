#!/usr/bin/env python3
"""Gate F tokenizer evaluation. Fertility is not confirmatory BPB."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

from nanochat.tokenizer import RustBPETokenizer  # noqa: E402

SPLIT = json.loads((ROOT / "manifests" / "split_manifest.json").read_text(encoding="utf-8"))
TOKENIZER_DIR = ROOT / "data" / "cache" / "p1-20260816T025911Z-0067a57" / "tokenizer"
SANITY = [
    "Ang mabilis na kayumangging fox ay tumalon sa tamad na aso.",
    "Filipinas",
    "Pilipinas",
    "ng",
    "mga",
    "sa",
    "ang",
    "Ang ñ at ng ay nasa wikang Filipino.",
    "artipisyal na itlog @-@ ng bayag",
    "artipisyal na itlog-ng bayag",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_texts(path: Path) -> list[str]:
    return [json.loads(line)["text"] for line in path.read_text(encoding="utf-8").splitlines() if line]


def fertility(tokenizer, texts: list[str], other=None) -> dict:
    n_tokens = 0
    n_bytes = 0
    n_chars = 0
    n_moses = 0
    n_single_byte = 0
    n_roundtrip_ok = 0
    for text in texts:
        ids = tokenizer.encode(text)  # no BOS
        n_tokens += len(ids)
        n_bytes += len(text.encode("utf-8"))
        n_chars += len(text)
        n_moses += len(text.split())
        n_single_byte += sum(1 for i in ids if len(tokenizer.decode_single_token_bytes(i)) == 1)
        if tokenizer.decode(ids) == text:
            n_roundtrip_ok += 1
    out = {
        "n_docs": len(texts),
        "n_tokens": n_tokens,
        "n_bytes": n_bytes,
        "n_chars": n_chars,
        "n_moses_tokens": n_moses,
        "bytes_per_token": (n_bytes / n_tokens) if n_tokens else None,
        "chars_per_token": (n_chars / n_tokens) if n_tokens else None,
        "tokens_per_moses": (n_tokens / n_moses) if n_moses else None,
        "single_byte_token_fraction": (n_single_byte / n_tokens) if n_tokens else None,
        "roundtrip_doc_fraction": (n_roundtrip_ok / len(texts)) if texts else None,
    }
    if other is not None:
        o_tokens = sum(len(other.encode(t)) for t in texts)
        out["gpt2_n_tokens"] = o_tokens
        out["gpt2_bytes_per_token"] = (n_bytes / o_tokens) if o_tokens else None
    return out


def main() -> int:
    tok = RustBPETokenizer.from_directory(str(TOKENIZER_DIR))
    gpt2 = RustBPETokenizer.from_pretrained("gpt2")
    train = load_texts(ROOT / SPLIT["paths"]["train"])
    val = load_texts(ROOT / SPLIT["paths"]["val"])
    test = load_texts(ROOT / SPLIT["paths"]["test"])

    sanity = []
    for s in SANITY:
        ids = tok.encode(s)
        decoded = tok.decode(ids)
        sanity.append(
            {
                "text": s,
                "ids": ids,
                "n_tokens": len(ids),
                "roundtrip": decoded == s,
                "decoded": decoded,
            }
        )

    payload = {
        "ok": tok.get_vocab_size() == 32768
        and (TOKENIZER_DIR / "token_bytes.pt").is_file()
        and all(x["roundtrip"] for x in sanity),
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vocab_size": tok.get_vocab_size(),
        "bos_not_prepended_in_fertility": True,
        "train_only": True,
        "test_read_kind": "tokenizer_fertility_not_confirmatory_bpb",
        "hashes": {
            "tokenizer.pkl": sha256_file(TOKENIZER_DIR / "tokenizer.pkl"),
            "token_bytes.pt": sha256_file(TOKENIZER_DIR / "token_bytes.pt"),
        },
        "fertility": {
            "train": fertility(tok, train, gpt2),
            "val": fertility(tok, val, gpt2),
            "test": fertility(tok, test, gpt2),
        },
        "sanity": sanity,
        "gpt2_comparison_is_descriptive_only": True,
    }
    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
