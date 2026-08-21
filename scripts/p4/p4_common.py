"""P4 constants. Not a rename of scripts/p3. Do not import scripts.p3."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P4_RUN_ID = os.environ.get("P4_RUN_ID", "p4-20260821T060032Z-92d63d4")
PIN = "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
ASPREDICTED_ID = 307591
RESEARCHBOX_ID = 8869
RESEARCHBOX_URL = "https://researchbox.org/8869"
ASCOLLECTED_URL = "https://ascollected.org/DJ6_FL3"

VENDOR = ROOT / "vendor" / "nanochat"
PYTHON = Path(os.environ.get("VIRTUAL_ENV", str(VENDOR / ".venv"))) / "bin" / "python"
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data" / "cache" / P4_RUN_ID))
RUN_CARD = ROOT / "docs" / "run-cards" / "p4" / P4_RUN_ID
LOCK_PATH = ROOT / "docs" / "papers" / "p4-token-share-mix" / "LOCK.json"
LEDGER_PATH = ROOT / "manifests" / "p4" / "p4_gate_ledger.json"
PDF = ROOT / "docs" / "run-cards" / "p4" / "AsPredicted-307591.pdf"

MASTER = ROOT / "docs" / "papers" / "p4-token-share-mix" / "PROTOCOL-p4-token-share-mix.md"
BIBLE = ROOT / "docs" / "papers" / "p4-token-share-mix" / "PROTOCOL-p4-GATES-EXHAUSTIVE.md"
ADDENDUM = ROOT / "docs" / "papers" / "p4-token-share-mix" / "P4-PREFILING-ADDENDUM-DRAFT.md"

FILED_MASTER_SHA = "22c28f2bc632f132d9c95bbbcc9d1facbddf0b6b821445487e451c472ea58d4b"
FILED_BIBLE_SHA = "b389b70e0b8e3af869e8dea314b1c7c6b91df313e49d1bf11d9d07961b4a5a42"
FILED_ADDENDUM_SHA = "f056a6f75c73a4d8dc3401ba8d7219d406aa7e498e5b0799d3d0373f9f74c216"
FILED_PDF_SHA = "463b29fcff8d7c8099790325fa19d6bcf9ee29f64424c373a380566a6fe9011c"

TOKENIZER_PKL_SHA = "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"
TOKEN_BYTES_SHA = "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132"
P3_B3_MIX_ORDER_SHA = "b6ae432b625b6768f84db3f45c411378d1d5a5fdbd15cbfc0e5f6c511196b1a0"
P3_TOK_DIR = ROOT / "data" / "cache" / "p3-20260819T192700Z-92d63d4" / "tokenizer"

TL_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl"
TL_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl"
TL_TEST_JSONL = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
EN_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_train.jsonl"
EN_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_val.jsonl"
EN_TEST_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_test.jsonl"

CACHE = ROOT / "data" / "cache" / P4_RUN_ID
LOCKBOX = CACHE / "lockbox"
SAFE = CACHE / "safe_progress"
PASSFILE = CACHE / ".lockbox_pass"
TOK_DIR = CACHE / "tokenizer"
C1_DIR = CACHE / "streams" / "c1_tl"
C2_DIR = CACHE / "streams" / "c2_en"
C3_DIR = CACHE / "streams" / "c3_mix"
HOLDOUT_DIR = CACHE / "holdouts"
SPLIT_COPY_DIR = CACHE / "splits"

EXPECTED = {
    "tl_train_jsonl": "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687",
    "tl_val_jsonl": "4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c",
    "tl_test_jsonl": "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf",
    "en_train_jsonl": "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a",
    "en_val_jsonl": "874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b",
    "en_test_jsonl": "2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e",
    "c1_shards": {
        "train_00000.parquet": "be3cecd0e7138666a8c87e8023a6d13411b6c02553cd307b9f9239b3d1c6d2de",
        "train_00001.parquet": "08fbfba33b57e8c7e1a376edc43ac99e40eb5a7f74e5a8d774c696cb175a89a6",
        "train_00002.parquet": "8ce8aca7042b37feeee038f22a1a77c2d66de749567dab7a31b32471fc5fe271",
        "train_00003.parquet": "44dbade713110a5071a1c5fc7a8a0c6cfb5c98314e66e880dabbbed2a34fc234",
        "val.parquet": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
    },
}

# Gate A copied scripts/p4/evaluate_bpb.py from P3 without renaming last-is-val.
# P4 C1 last-is-val is val.parquet. These aliases let the frozen evaluator SHA
# (9afebdb4…) hash-check without changing the BPB formula.
EXPECTED["p11_shards"] = {
    "shard_00000.parquet": EXPECTED["c1_shards"]["train_00000.parquet"],
    "shard_00001.parquet": EXPECTED["c1_shards"]["train_00001.parquet"],
    "shard_00002.parquet": EXPECTED["c1_shards"]["val.parquet"],
}

FILED_EVALUATOR_SHA = "9afebdb405aaac0bb4287051d9b6f5d16f56d6dd9269a1e6c2c5df29becbced1"

VOCAB = 32768
B = 65536
T = 2048
N_TL0 = 294
N_PHASE2 = 294
D_PHASE2 = N_PHASE2 * B
Q_TL = 0.50
K_BLK = 2048
SEED = 42
N_TRAIN_SHARDS = 4
WARMUP = 14
DELTA = 0.01


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def freeze_file(path: Path) -> None:
    path.chmod(0o444)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def blinded_print(gate: str, status: str, extra: dict | None = None) -> None:
    row = {
        "gate": gate,
        "status": status,
        "blinded": True,
        "unblinded": False,
        "no_p4_outcomes": True,
        "no_bpb_printed": True,
    }
    if extra:
        row.update(extra)
    print(json.dumps(row, indent=2), flush=True)


def mark_ledger(gate: str, status: str, artifact: str, next_gate: str | None) -> None:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ledger["gates"][gate] = {
        "status": status,
        "at_utc": utc_now(),
        "artifact": artifact,
        "sha256_prefix": sha256_file(ROOT / artifact)[:8] if (ROOT / artifact).is_file() else None,
        "safe_note": "blinded; hashes/status only",
        "next": next_gate,
    }
    write_json(LEDGER_PATH, ledger)


def update_lock_gate(gate: str, status: str, extra: dict | None = None) -> None:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["gate_statuses"][gate] = status
    lock["status"] = f"gate_{gate.lower()}_pass" if status == "pass" else lock.get("status")
    if extra:
        for k, v in extra.items():
            lock[k] = v
    write_json(LOCK_PATH, lock)
