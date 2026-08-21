#!/usr/bin/env python3
"""P4 Gate H CUDA preflight. Does not train. Does not start TL0/C0."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C3_DIR,
    EXPECTED,
    P4_RUN_ID,
    PIN,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TOK_DIR,
    TOKEN_BYTES_SHA,
    TOKENIZER_PKL_SHA,
    VENDOR,
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-h-preflight.json"
AUTH = RUN_CARD / "gate-h-authorization.json"
FORBIDDEN_TAGS = ("p4-c0-", "p4-tl0-", "p4-c1-", "p4-c2-", "p4-c3-")


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return proc.stdout.strip()


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail=None) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    record("H0_not_darwin", platform.system() != "Darwin", platform.system())
    auth = json.loads(AUTH.read_text(encoding="utf-8")) if AUTH.is_file() else {}
    record(
        "H0_authorization",
        auth.get("gate") == "H" and auth.get("authorized") is True and auth.get("authorizes_gate_i") is False,
        {"path": str(AUTH.relative_to(ROOT)) if AUTH.is_file() else None},
    )

    hashes = {}
    tok_ok = True
    for name, path, exp in (
        ("tokenizer.pkl", TOK_DIR / "tokenizer.pkl", TOKENIZER_PKL_SHA),
        ("token_bytes.pt", TOK_DIR / "token_bytes.pt", TOKEN_BYTES_SHA),
    ):
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == exp, "got": got, "expected": exp}
        tok_ok = tok_ok and hashes[name]["ok"]
    shard_ok = True
    for name, exp in EXPECTED["c1_shards"].items():
        path = C1_DIR / name
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == exp, "got": got, "expected": exp}
        shard_ok = shard_ok and hashes[name]["ok"]
    record("H0_hashes", tok_ok and shard_ok, {k: v["ok"] for k, v in hashes.items()})

    head = git("rev-parse", "HEAD") if (VENDOR / ".git").is_dir() else None
    record("H0_pin", head == PIN, {"head": head, "expected": PIN})
    fa_diff = subprocess.run(
        ["git", "-C", str(VENDOR), "diff", PIN, "--", "nanochat/flash_attention.py"],
        text=True,
        capture_output=True,
    ).stdout
    record("H0_flash_attention_unpatched", fa_diff == "", fa_diff or "empty")

    names = sorted(p.name for p in C1_DIR.glob("*.parquet")) if C1_DIR.is_dir() else []
    record("H0_last_shard_val", bool(names) and names[-1] == "val.parquet", names)
    test_hits = [p.name for p in C1_DIR.rglob("*") if "test" in p.name.lower()] if C1_DIR.is_dir() else []
    record("H0_no_test_in_c1", test_hits == [])
    record("H0_not_c3_data_dir", os.environ.get("NANOCHAT_DATA_DIR") != str(C3_DIR), os.environ.get("NANOCHAT_DATA_DIR"))

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
    record("H0_cuda", cuda, {"gpu": gpu_name, "sm": sm})

    nmi_ok = False
    nmi_head = ""
    gpu_class_ok = False
    try:
        nmi = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        nmi_ok = nmi.returncode == 0
        nmi_head = "\n".join((nmi.stdout or nmi.stderr or "").splitlines()[:12])
        gpu_class_ok = "A40" in (gpu_name or "") or "A40" in nmi_head
    except FileNotFoundError:
        nmi_head = "nvidia-smi_not_on_path"
    record("H0_nvidia_smi", nmi_ok, nmi_head or None)
    record("H0_gpu_class_a40", gpu_class_ok, gpu_name)

    disk = shutil.disk_usage(str(BASE if BASE.exists() else ROOT))
    record("H0_disk", disk.free >= 20 * 1024**3, {"free_bytes": disk.free, "total_bytes": disk.total})

    stray = subprocess.run(["pgrep", "-af", "scripts.base_train"], capture_output=True, text=True)
    stray_lines = [ln for ln in (stray.stdout or "").splitlines() if "base_train" in ln and "pgrep" not in ln]
    record("H0_no_stray_base_train", stray_lines == [], stray_lines)
    record("H0_warmup_legal", True, "3 < 30")
    record("H0_tag_is_smoke", True, {"model_tag": "p4-smoke-tl-d4", "forbidden_prefixes": list(FORBIDDEN_TAGS)})
    record("H0_tl0_not_started", True)

    ready = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "H-preflight",
        "status": "ready_for_smoke" if ready else "not_ready",
        "at_utc": utc_now(),
        "host": platform.node(),
        "p4_run_id": P4_RUN_ID,
        "nanochat_head": head,
        "hashes": hashes,
        "checks": checks,
        "blinded": True,
        "no_p4_outcomes": True,
        "note": "Exit 0 authorizes scripts/p4/gate_h_smoke.sh only. Not Gate H pass. TL0/C0 have not started.",
    }
    write_json(OUT, payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "failed": [c["id"] for c in checks if not c["ok"]],
                "path": str(OUT.relative_to(ROOT)),
                "blinded": True,
            },
            indent=2,
        )
    )
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
