"""P5 constants. Not a rename of scripts/p4. Do not import scripts.p4 at runtime."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P5_RUN_ID = os.environ.get("P5_RUN_ID", "p5-20260823T160632Z-439d1de5")
P4_RUN_ID = "p4-20260821T060032Z-92d63d4"
PIN = "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
ASPREDICTED_ID = 307836
ASPREDICTED_URL = "https://aspredicted.org/k6ib64.pdf"
RESEARCHBOX_ID = 8904
RESEARCHBOX_URL = "https://researchbox.org/8904"
ASCOLLECTED_ID = 2503
ASCOLLECTED_URL = "https://ascollected.org/HC8_G2F"
FILED_PDF_SHA = "439d1de5ff9fd18e466f33192c5ac9c5c36b020ca72942ae218b9e69a8f5bbf3"
FILED_ADDENDUM_SHA = "839fcaa3dd6e94bd9546df4880a5892851a54ea31743cb0359adc8faebbe9258"
FILED_GATE_PLAN_SHA = "d51115aade9c0b1fb8698eaa33540db2d75b2b27765aaaad1bf14b13b0132092"
MIX_MANIFEST_SHA = "f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107"

VENDOR = ROOT / "vendor" / "nanochat"
PYTHON = Path(os.environ.get("VIRTUAL_ENV", str(VENDOR / ".venv"))) / "bin" / "python"
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data" / "cache" / P5_RUN_ID))
P4_BASE = ROOT / "data" / "cache" / P4_RUN_ID
RUN_CARD = ROOT / "docs" / "run-cards" / "p5" / P5_RUN_ID
LOCK_PATH = ROOT / "docs" / "papers" / "p5-multi-seed-p4" / "LOCK.json"
LEDGER_PATH = ROOT / "manifests" / "p5" / "p5_gate_ledger.json"
PDF = ROOT / "docs" / "run-cards" / "p5" / "AsPredicted-307836.pdf"
GATE_PLAN = ROOT / "docs" / "papers" / "p5-multi-seed-p4" / "P5-GATES-EXHAUSTIVE-PLAN.md"
ADDENDUM = ROOT / "docs" / "papers" / "p5-multi-seed-p4" / "P5-PREFILING-ADDENDUM-DRAFT.md"

TOKENIZER_PKL_SHA = "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"
TOKEN_BYTES_SHA = "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132"
P3_B3_MIX_ORDER_SHA = "b6ae432b625b6768f84db3f45c411378d1d5a5fdbd15cbfc0e5f6c511196b1a0"
P4_TOK_DIR = P4_BASE / "tokenizer"

TL_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl"
TL_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl"
TL_TEST_JSONL = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
EN_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_train.jsonl"
EN_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_val.jsonl"
EN_TEST_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_test.jsonl"

CACHE = BASE
LOCKBOX = CACHE / "lockbox"
SAFE = CACHE / "safe_progress"
PASSFILE = CACHE / ".lockbox_pass"
TOK_DIR = CACHE / "tokenizer"
C1_DIR = CACHE / "streams" / "c1_tl"
C2_DIR = CACHE / "streams" / "c2_en"
C3_DIR = CACHE / "streams" / "c3_mix"
HOLDOUT_DIR = CACHE / "holdouts"
SPLIT_COPY_DIR = CACHE / "splits"
PANEL_SEEDS = (1, 2, 3)
WRAPPER_RNG_SEED = 424242
C3_INTERLEAVE_SEED = 42

FORBIDDEN_P4_PARENT_SHA256 = {
    "34e069646be4158979809c023691188439047d6cbee08a141db432c78bcf02e2",
    "87b9f55146de72dd6ae53598b9aea8d99079ff0f9492b7f9ea4fdce550664c55",
    "0787aed0f13a0ab3ec144baf6802b144a18412780a2d00a64ca7adcb67a4a375",
    "eef9a4e11c4840ac036d42c3bf4d87a2139ea1fa5809e1c756df2770fe0609f3",
}

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
    "c2_shards": {
        "train_00000.parquet": "9bdee964368da85a9b97af0d8cd50c4cd13ec392a8045dbec602ce31bd587861",
        "train_00001.parquet": "7331e6219eec3bf619b92c38f686778395b77b500d267cfb25412abb41c6379c",
        "train_00002.parquet": "59bc144b0191d10009baa7698bbb96ba25c2c750b7ab8cdbc9bba52998c4d9f7",
        "train_00003.parquet": "ac693bfc6c1820e9f978f90958b1afb4bf82d91c9bcbba682467d6a357ebcb0b",
        "val.parquet": "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f",
    },
    "c3_train_shards": {
        "train_00000.parquet": "249e2c5e9d06bf17fe14e03c02e622c9e68d90ba337e1e6e33c237fc723252f5",
        "train_00001.parquet": "d24fe7f933abeb38b277b099385518718d2d57e330e5f9b5fd8b1a534e43444e",
        "train_00002.parquet": "a56a729a0e3c7fd2d1e2e99236a4225bf9a86e55d6d97153063de9d6455fa523",
        "train_00003.parquet": "4adbf8f9afcc9870f46f6298ac22f3691ec073d2f452f73aa65322e3ff6331de",
        "val.parquet": "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f",
    },
    "language_origin_mask_sha256": "140e174a427a7ddf2126553c53352ec049f72fbed475e2404cd4ef122b309c46",
}
EXPECTED["p11_shards"] = {
    "shard_00000.parquet": EXPECTED["c1_shards"]["train_00000.parquet"],
    "shard_00001.parquet": EXPECTED["c1_shards"]["train_00001.parquet"],
    "shard_00002.parquet": EXPECTED["c1_shards"]["val.parquet"],
}

VOCAB = 32768
B = 65536
T = 2048
N_TL0 = 294
N_PHASE2 = 294
D_PHASE2 = N_PHASE2 * B
Q_TL = 0.50
DELTA = 0.01
WARMUP = 14
FILED_EVALUATOR_SHA = "78e77d9761fa4473344abd4773129e56f04561e615bdbcfad144ab8730ded977"
CHILD_LR = {
    "embedding_lr": 0.09,
    "unembedding_lr": 0.0024,
    "matrix_lr": 0.006,
    "scalar_lr": 0.15,
    "weight_decay": 0.28,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def freeze_file(path: Path) -> None:
    path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def blinded_print(gate: str, status: str, extra: dict | None = None) -> None:
    row = {
        "gate": gate,
        "status": status,
        "blinded": True,
        "unblinded": False,
        "no_p5_outcomes": True,
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seed_lockbox_dirs() -> None:
    LOCKBOX.mkdir(parents=True, exist_ok=True)
    SAFE.mkdir(parents=True, exist_ok=True)
    for s in PANEL_SEEDS:
        (LOCKBOX / f"seed-{s}").mkdir(parents=True, exist_ok=True)
        (SAFE / f"seed-{s}").mkdir(parents=True, exist_ok=True)
        (RUN_CARD / f"seed-{s}").mkdir(parents=True, exist_ok=True)
    os.chmod(LOCKBOX, 0o700)
    os.chmod(SAFE, 0o755)


def seed_card(seed: int) -> Path:
    path = RUN_CARD / f"seed-{seed}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def seed_box(seed: int) -> Path:
    path = LOCKBOX / f"seed-{seed}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def seed_safe(seed: int) -> Path:
    path = SAFE / f"seed-{seed}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def tl0_tag(seed: int, depth: int) -> str:
    return f"p5-s{seed}-tl0-d{depth}"


def c0_tag(seed: int) -> str:
    return f"p5-s{seed}-c0-tl-d20"


def child_tag(seed: int, arm: str) -> str:
    mapping = {"c1": f"p5-s{seed}-c1-tl-d20", "c2": f"p5-s{seed}-c2-en-d20", "c3": f"p5-s{seed}-c3-mix-d20"}
    return mapping[arm]


def frozen_c0_dir(seed: int) -> Path:
    return BASE / f"p5-s{seed}" / "c0" / "frozen" / c0_tag(seed)


def require_auth(path: Path, gate: str, extra: dict | None = None) -> dict:
    if not path.is_file():
        raise SystemExit(f"missing authorization: {path}")
    row = json.loads(path.read_text(encoding="utf-8"))
    if row.get("gate") != gate or row.get("authorized") is not True:
        raise SystemExit(f"authorization is not Gate {gate}")
    if extra:
        for k, v in extra.items():
            if row.get(k) != v:
                raise SystemExit(f"authorization field {k} must be {v!r}")
    return row
