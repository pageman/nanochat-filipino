"""Shared P3 constants. No outcomes."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P3_RUN_ID = os.environ.get("P3_RUN_ID", "p3-20260819T192700Z-92d63d4")
PIN = "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
ASPREDICTED_ID = 307342
RESEARCHBOX_ID = 8834
RESEARCHBOX_URL = "https://researchbox.org/8834"

VENDOR = ROOT / "vendor" / "nanochat"
PYTHON = Path(os.environ.get("VIRTUAL_ENV", str(VENDOR / ".venv"))) / "bin" / "python"
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data" / "cache" / P3_RUN_ID))
RUN_CARD = ROOT / "docs" / "run-cards" / "p3" / P3_RUN_ID

TL_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl"
TL_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl"
TL_TEST = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
EN_TRAIN_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_train.jsonl"
EN_VAL_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_val.jsonl"
EN_TEST_JSONL = ROOT / "data" / "interim" / "wikitext-103" / "english_test.jsonl"
EN_RAW_DIR = ROOT / "data" / "raw" / "wikitext-103-raw" / "wikitext-103-raw-v1"
P11_ACTIVE = ROOT / "data" / "processed" / "wikitext-tl39" / "active"
P2_EN_ACTIVE = ROOT / "data" / "processed" / "wikitext-103" / "en-active"

TL_DIR = ROOT / "data" / "processed" / "p3-tl39-active"
EN_DIR = ROOT / "data" / "processed" / "p3-en-active"
B3_DIR = ROOT / "data" / "processed" / "p3-mix-b3-50-50"
MIX_ORDER = ROOT / "data" / "interim" / "p3-mix-b3-50-50" / "mix_order.jsonl"

EXPECTED = {
    "tl_train_jsonl": "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687",
    "tl_val_jsonl": "4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c",
    "tl_test_jsonl": "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf",
    "en_train_jsonl": "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a",
    "en_val_jsonl": "874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b",
    "en_test_jsonl": "2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e",
    "p11_shards": {
        "shard_00000.parquet": "aaf81d95e577742dcd33a44be2f144c253a5d5650e34b3e622e8b262ff2b6dc9",
        "shard_00001.parquet": "c57c11a2625c38f7f12d1e4018e71bf1f38a56d68fcc9b4952e1b8bded854976",
        "shard_00002.parquet": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
    },
    "en_train_shards": {
        "train_00000.parquet": "9bdee964368da85a9b97af0d8cd50c4cd13ec392a8045dbec602ce31bd587861",
        "train_00001.parquet": "7331e6219eec3bf619b92c38f686778395b77b500d267cfb25412abb41c6379c",
        "train_00002.parquet": "59bc144b0191d10009baa7698bbb96ba25c2c750b7ab8cdbc9bba52998c4d9f7",
        "train_00003.parquet": "ac693bfc6c1820e9f978f90958b1afb4bf82d91c9bcbba682467d6a357ebcb0b",
        "val.parquet": "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f",
    },
    "en_raw_parquets": {
        "test-00000-of-00001.parquet": "5f1bea067869d04849c0f975a2b29c4ff47d867f484f5010ea5e861eab246d91",
        "train-00000-of-00002.parquet": "74da360f23826045b3e6ac6375411fdb15f003030aa74f2596ed08b857cb9212",
        "train-00001-of-00002.parquet": "ba090ac30dbf5461e8dcbdd1a1b8e6f3cf9c2c756d64f0c1220450acd514f720",
        "validation-00000-of-00001.parquet": "204929b7ff9d6184953f867dedb860e40aa69c078fc1e54b3baaa8fb28511c4c",
    },
    "p11_tok": "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8",
    "p2_tok": "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6",
}

B3_SEED = 42
N_EN_TRAIN_SHARDS = 4
VOCAB = 32768
B = 65536
T = 2048
N_PHASE2 = 294
D_PHASE2 = N_PHASE2 * B
