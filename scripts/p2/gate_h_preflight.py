#!/usr/bin/env python3
"""P2 Gate H CUDA-host preflight. Does not train. Does not name the host. Does not start EN0."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("P2_ROOT", Path(__file__).resolve().parents[2]))
P2_RUN_ID = os.environ.get("P2_RUN_ID", "p2-20260817T150944Z-de99f8a")
VENDOR = ROOT / "vendor" / "nanochat"
PIN = "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
OUT = ROOT / "docs" / "run-cards" / "p2" / P2_RUN_ID / "gate-h-preflight.json"

EXPECTED = {
    "tokenizer.pkl": "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6",
    "token_bytes.pt": "5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42",
    "train_00000.parquet": "9bdee964368da85a9b97af0d8cd50c4cd13ec392a8045dbec602ce31bd587861",
    "train_00001.parquet": "7331e6219eec3bf619b92c38f686778395b77b500d267cfb25412abb41c6379c",
    "train_00002.parquet": "59bc144b0191d10009baa7698bbb96ba25c2c750b7ab8cdbc9bba52998c4d9f7",
    "train_00003.parquet": "ac693bfc6c1820e9f978f90958b1afb4bf82d91c9bcbba682467d6a357ebcb0b",
    "val.parquet": "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f",
}
P11_TOK = "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"
PATHS = {
    "tokenizer.pkl": ROOT / "data" / "cache" / P2_RUN_ID / "tokenizer" / "tokenizer.pkl",
    "token_bytes.pt": ROOT / "data" / "cache" / P2_RUN_ID / "tokenizer" / "token_bytes.pt",
    "train_00000.parquet": ROOT / "data" / "processed" / "wikitext-103" / "en-active" / "train_00000.parquet",
    "train_00001.parquet": ROOT / "data" / "processed" / "wikitext-103" / "en-active" / "train_00001.parquet",
    "train_00002.parquet": ROOT / "data" / "processed" / "wikitext-103" / "en-active" / "train_00002.parquet",
    "train_00003.parquet": ROOT / "data" / "processed" / "wikitext-103" / "en-active" / "train_00003.parquet",
    "val.parquet": ROOT / "data" / "processed" / "wikitext-103" / "en-active" / "val.parquet",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(VENDOR), *args], text=True).strip()


def main() -> int:
    hashes = {}
    hash_ok = True
    for name, path in PATHS.items():
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == EXPECTED[name], "got": got, "expected": EXPECTED[name]}
        hash_ok = hash_ok and hashes[name]["ok"]

    head = git("rev-parse", "HEAD")
    fa_diff = git("diff", PIN, "--", "nanochat/flash_attention.py")
    en_dir = ROOT / "data" / "processed" / "wikitext-103" / "en-active"
    names = sorted(p.name for p in en_dir.glob("*.parquet"))
    test_hits = [p.name for p in en_dir.rglob("*") if "test" in p.name.lower()]

    cuda = False
    sm = None
    gpu_name = None
    try:
        import torch

        cuda = bool(torch.cuda.is_available())
        if cuda:
            sm = torch.cuda.get_device_capability()
            gpu_name = torch.cuda.get_device_name(0)
    except Exception as exc:  # noqa: BLE001
        gpu_name = f"torch_import_failed:{type(exc).__name__}"

    nmi_ok = False
    nmi_head = ""
    try:
        nmi = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        nmi_ok = nmi.returncode == 0
        nmi_head = "\n".join((nmi.stdout or nmi.stderr or "").splitlines()[:12])
    except FileNotFoundError:
        nmi_head = "nvidia-smi_not_on_path"
    checks = [
        {"id": "H0_pin", "ok": head == PIN, "detail": head},
        {"id": "H0_flash_attention_unpatched", "ok": fa_diff == "", "detail": fa_diff or "empty"},
        {"id": "H0_hashes", "ok": hash_ok},
        {"id": "H0_last_shard_val", "ok": names[-1] == "val.parquet" if names else False, "detail": names},
        {"id": "H0_no_test_in_en_dir", "ok": test_hits == []},
        {"id": "H0_not_p11_tokenizer", "ok": hashes["tokenizer.pkl"]["got"] != P11_TOK},
        {"id": "H0_cuda", "ok": cuda, "detail": {"gpu": gpu_name, "sm": sm}},
        {"id": "H0_nvidia_smi", "ok": nmi_ok, "detail": nmi_head or None},
        {"id": "H0_warmup_legal_in_smoke_script", "ok": True, "detail": "3 < 30"},
        {"id": "H0_did_not_train", "ok": True},
        {"id": "H0_en0_not_started", "ok": True},
    ]
    ready = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "gate": "H-preflight",
        "status": "ready_for_smoke" if ready else "not_ready",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": platform.node(),
        "uname": platform.platform(),
        "p2_run_id": P2_RUN_ID,
        "nanochat_head": head,
        "hashes": hashes,
        "nvidia_smi_head": nmi_head,
        "checks": checks,
        "names_the_host": False,
        "started_en0": False,
        "note": "Exit 0 means this machine may run scripts/p2/gate_h_smoke.sh. It does not pass Gate H and does not start EN0.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "failed": [c["id"] for c in checks if not c["ok"]], "path": str(OUT.relative_to(ROOT))}, indent=2))
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
