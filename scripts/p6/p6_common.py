"""P6-M constants. Not a rename of scripts/p4 or scripts/p5. Do not import prior-study env at runtime."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P6_RUN_ID = os.environ.get("P6_RUN_ID", "p6-20260824T155226Z-769f807a")
P4_RUN_ID = "p4-20260821T060032Z-92d63d4"
P5_RUN_ID = "p5-20260823T160632Z-439d1de5"
PIN = "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
ASPREDICTED_ID = 307969
ASPREDICTED_URL = "https://aspredicted.org/bk6m9d.pdf"
RESEARCHBOX_ID = None
RESEARCHBOX_URL = None
ASCOLLECTED_ID = None
ASCOLLECTED_URL = None

FILED_PDF_SHA = "769f807a00264a996b02c38b83ee2cf6c23c4981e36fb477dfc1959fa918a1e7"
FILED_ADDENDUM_SHA = "df49664809ada69d23dcd2c799e75b30f0fdb9afd7aee12b071ac24ef2f81082"
FILED_GATE_PLAN_SHA = "d8a63608608c59d2c4d9882e5346625462056c331094942a8a01d496697a1c79"
TOPOLOGY_MANIFEST_SHA = "d1e7d5af7247a572e319ee003b5f4e3da5d1fb1592e5ed9ff6b22eeec15ea606"
MIX_MANIFEST_SHA = "f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107"

VENDOR = ROOT / "vendor" / "nanochat"
PYTHON = Path(os.environ.get("VIRTUAL_ENV", str(VENDOR / ".venv"))) / "bin" / "python"
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data" / "cache" / P6_RUN_ID))
P4_BASE = ROOT / "data" / "cache" / P4_RUN_ID
RUN_CARD = ROOT / "docs" / "run-cards" / "p6" / P6_RUN_ID
LOCK_PATH = ROOT / "docs" / "papers" / "p6-m-schedule-topology" / "LOCK.json"
LEDGER_PATH = ROOT / "manifests" / "p6" / "p6_gate_ledger.json"
PDF = ROOT / "docs" / "run-cards" / "p6" / "AsPredicted-307969.pdf"
# Immutable filed copy (Cursor working plan may mutate YAML todo statuses).
GATE_PLAN = ROOT / "docs" / "papers" / "p6-m-schedule-topology" / "P6-M-GATE-PLAN-FILED.md"
GATE_PLAN_WORKING = Path("/Users/paulpajo/.cursor/plans/p6-m_gate_plan_29fa4469.plan.md")
ADDENDUM = ROOT / "docs" / "papers" / "p6-m-schedule-topology" / "P6-M-PREFILING-ADDENDUM.md"
TOPOLOGY_MANIFEST = ROOT / "manifests" / "p6" / "p6_topology_schedule_manifest.json"

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
TIER2 = CACHE / "tier2-resume-kit"
C1_DIR = CACHE / "streams" / "c1_tl"
C2_DIR = CACHE / "streams" / "c2_en"
C3_DIR = CACHE / "streams" / "c3_mix"  # historical name; P6 mixed arms use topology dirs
HOLDOUT_DIR = CACHE / "holdouts"
SPLIT_COPY_DIR = CACHE / "splits"

# P6-M: one fixed parent-init seed
PARENT_SEED = 4
PANEL_SEEDS = (4,)  # compatibility alias for scripts expecting a sequence
TOPOLOGY_ARMS = ("m-fine", "m-coarse", "m-blocked", "m-rand")
CHILD_ARMS = ("c1", "c2") + TOPOLOGY_ARMS
POLICY_A_TEST_ARM = "m-fine"
WRAPPER_RNG_SEED = 424242
DOC_ORDER_SEED = 42

# Infrastructure (lockout-resistant)
NETWORK_VOLUME_ID = "3xuadadrph"
NETWORK_VOLUME_DC = "CA-MTL-3"
NETWORK_VOLUME_GB = 200
GPU_CLASS = "NVIDIA A40"
GPU_VRAM_GB = 48  # A40 VRAM is fixed; 200 GB is network volume storage
CONTAINER_IMAGE = "runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404"

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
    # Symlink layout used by Gate P0-T (train0/train1/val only)
    "p11_shards": {
        "shard_00000.parquet": "be3cecd0e7138666a8c87e8023a6d13411b6c02553cd307b9f9239b3d1c6d2de",
        "shard_00001.parquet": "08fbfba33b57e8c7e1a376edc43ac99e40eb5a7f74e5a8d774c696cb175a89a6",
        "shard_00002.parquet": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
    },
    "c2_shards": {
        "train_00000.parquet": "9bdee964368da85a9b97af0d8cd50c4cd13ec392a8045dbec602ce31bd587861",
        "train_00001.parquet": "7331e6219eec3bf619b92c38f686778395b77b500d267cfb25412abb41c6379c",
        "train_00002.parquet": "59bc144b0191d10009baa7698bbb96ba25c2c750b7ab8cdbc9bba52998c4d9f7",
        "train_00003.parquet": "ac693bfc6c1820e9f978f90958b1afb4bf82d91c9bcbba682467d6a357ebcb0b",
        "val.parquet": "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f",
    },
    "language_origin_mask_sha256_m_fine": "140e174a427a7ddf2126553c53352ec049f72fbed475e2404cd4ef122b309c46",
    # P4 C3 == P6 M-fine packed stream (same origin mask / fine schedule)
    "m_fine_shards": {
        "train_00000.parquet": "249e2c5e9d06bf17fe14e03c02e622c9e68d90ba337e1e6e33c237fc723252f5",
        "train_00001.parquet": "d24fe7f933abeb38b277b099385518718d2d57e330e5f9b5fd8b1a534e43444e",
        "train_00002.parquet": "a56a729a0e3c7fd2d1e2e99236a4225bf9a86e55d6d97153063de9d6455fa523",
        "train_00003.parquet": "4adbf8f9afcc9870f46f6298ac22f3691ec073d2f452f73aa65322e3ff6331de",
        "val.parquet": "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f",
    },
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
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def blinded_print(gate: str, status: str, extra: dict | None = None) -> None:
    payload = {"gate": gate, "status": status, "at_utc": utc_now()}
    if extra:
        payload.update(extra)
    print(json.dumps(payload, sort_keys=True), flush=True)


def seed_lockbox_dirs() -> None:
    LOCKBOX.mkdir(parents=True, exist_ok=True)
    SAFE.mkdir(parents=True, exist_ok=True)
    TIER2.mkdir(parents=True, exist_ok=True)
    (LOCKBOX / f"seed-{PARENT_SEED}").mkdir(parents=True, exist_ok=True)
    (SAFE / f"seed-{PARENT_SEED}").mkdir(parents=True, exist_ok=True)
    try:
        LOCKBOX.chmod(0o700)
        SAFE.chmod(0o755)
        TIER2.chmod(0o755)
        if PASSFILE.is_file():
            PASSFILE.chmod(0o600)
    except OSError:
        pass


def seed_card(seed: int) -> Path:
    d = RUN_CARD / f"seed-{seed}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def seed_box(seed: int) -> Path:
    path = LOCKBOX / f"seed-{seed}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def seed_safe(seed: int) -> Path:
    path = SAFE / f"seed-{seed}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def tl0_tag(seed: int, depth: int) -> str:
    return f"p6-s{seed}-tl0-d{depth}"


def c0_tag(seed: int) -> str:
    return f"p6-s{seed}-c0-tl-d20"


def child_tag(seed: int, arm: str) -> str:
    if arm == "c1":
        return f"p6-s{seed}-c1-tl-d20"
    if arm == "c2":
        return f"p6-s{seed}-c2-en-d20"
    if arm in TOPOLOGY_ARMS:
        return f"p6-s{seed}-{arm}-d20"
    raise KeyError(f"unknown P6 child arm: {arm}")


def frozen_c0_dir(seed: int) -> Path:
    return BASE / f"p6-s{seed}" / "c0" / "frozen" / c0_tag(seed)


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


def update_lock_gate(gate: str, status: str, extra: dict | None = None) -> None:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8")) if LOCK_PATH.is_file() else {}
    gates = lock.setdefault("gate_statuses", {})
    gates[str(gate)] = status
    if extra:
        lock.update(extra)
    lock["updated_utc"] = utc_now()
    write_json(LOCK_PATH, lock)


def mark_ledger(gate: str, status: str, receipt: str, next_gate: str | None = None) -> None:
    ledger = {"study": "P6-M", "p6_run_id": P6_RUN_ID, "entries": []}
    if LEDGER_PATH.is_file():
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ledger.setdefault("entries", []).append(
        {
            "gate": gate,
            "status": status,
            "receipt": receipt,
            "next": next_gate,
            "at_utc": utc_now(),
        }
    )
    write_json(LEDGER_PATH, ledger)


def freeze_file(path: Path) -> None:
    path.chmod(path.stat().st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
