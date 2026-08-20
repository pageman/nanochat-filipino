#!/usr/bin/env python3
"""P3 Gate I TL0 preflight. Does not train. Authorizes gate_i_tl0.sh only."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256
from p3_common import ASPREDICTED_ID, BASE, EXPECTED, PIN, P3_RUN_ID, ROOT, RUN_CARD, TL_DIR, VENDOR

OUT = RUN_CARD / "gate-i-preflight.json"
GATE_H = RUN_CARD / "gate-h-cuda-smoke.json"
GATE_G = RUN_CARD / "gate-g-budget-command-freeze.json"
N_TL0 = 294
WARMUP = 14
TL0_TAGS = ("p3-tl0-d8", "p3-tl0-d20")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return proc.stdout.strip()


def scan_forbidden_ckpts() -> list[dict]:
    hits: list[dict] = []
    ckpt_root = BASE / "base_checkpoints"
    if not ckpt_root.is_dir():
        return hits
    for tag in TL0_TAGS:
        tag_dir = ckpt_root / tag
        if not tag_dir.is_dir():
            continue
        for pt in tag_dir.glob("*.pt"):
            digest = sha256_file(pt)
            if digest in FORBIDDEN_PARENT_SHA256:
                hits.append({"path": str(pt.relative_to(ROOT)), "sha256": digest, "forbidden": True})
    return hits


def main() -> int:
    paths = {
        "tokenizer.pkl": BASE / "tokenizer" / "tokenizer.pkl",
        "token_bytes.pt": BASE / "tokenizer" / "token_bytes.pt",
        "shard_00000.parquet": TL_DIR / "shard_00000.parquet",
        "shard_00001.parquet": TL_DIR / "shard_00001.parquet",
        "shard_00002.parquet": TL_DIR / "shard_00002.parquet",
    }
    expected = {
        "tokenizer.pkl": "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8",
        "token_bytes.pt": "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132",
        **EXPECTED["p11_shards"],
    }
    hashes = {}
    hash_ok = True
    for name, path in paths.items():
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == expected[name], "got": got, "expected": expected[name]}
        hash_ok = hash_ok and hashes[name]["ok"]

    head = git("rev-parse", "HEAD")
    fa_diff = subprocess.run(
        ["git", "-C", str(VENDOR), "diff", PIN, "--", "nanochat/flash_attention.py"],
        text=True,
        capture_output=True,
    ).stdout
    names = sorted(p.name for p in TL_DIR.glob("*.parquet"))
    test_hits = [p.name for p in TL_DIR.rglob("*") if "test" in p.name.lower()]
    forbidden_hits = scan_forbidden_ckpts()

    gate_h_ok = False
    gate_h_detail = "missing"
    if GATE_H.is_file():
        gate_h = json.loads(GATE_H.read_text(encoding="utf-8"))
        gate_h_ok = gate_h.get("status") == "pass" and gate_h.get("health") == "pass"
        gate_h_detail = gate_h.get("status", "unknown")

    n_tl0 = N_TL0
    warmup = WARMUP
    if GATE_G.is_file():
        gate_g = json.loads(GATE_G.read_text(encoding="utf-8"))
        n_tl0 = int(gate_g.get("N_TL0", N_TL0))
        warmup = int(gate_g.get("commands", {}).get("tl0", {}).get("warmup_steps", WARMUP))

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

    reject_ok = True
    try:
        reject_parent_sha256(next(iter(FORBIDDEN_PARENT_SHA256)))
        reject_ok = False
    except SystemExit:
        reject_ok = True

    checks = [
        {"id": "I0_gate_h_pass", "ok": gate_h_ok, "detail": gate_h_detail},
        {"id": "I0_pin", "ok": head == PIN, "detail": head},
        {"id": "I0_flash_attention_unpatched", "ok": fa_diff == "", "detail": fa_diff or "empty"},
        {"id": "I0_hashes", "ok": hash_ok},
        {"id": "I0_last_shard_val", "ok": names[-1] == "shard_00002.parquet" if names else False, "detail": names},
        {"id": "I0_no_test_in_tl_dir", "ok": test_hits == []},
        {"id": "I0_no_forbidden_parent_ckpts", "ok": forbidden_hits == [], "detail": forbidden_hits or None},
        {"id": "I0_forbidden_reject_live", "ok": reject_ok},
        {"id": "I0_cuda", "ok": cuda, "detail": {"gpu": gpu_name, "sm": sm}},
        {"id": "I0_nvidia_smi", "ok": nmi_ok, "detail": nmi_head or None},
        {"id": "I0_warmup_legal", "ok": warmup < n_tl0, "detail": f"warmup={warmup} N_TL0={n_tl0}"},
        {"id": "I0_n_tl0_locked", "ok": n_tl0 == N_TL0, "detail": n_tl0},
    ]
    ready = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "gate": "I-preflight",
        "status": "ready_for_tl0" if ready else "not_ready",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": platform.node(),
        "p3_run_id": P3_RUN_ID,
        "nanochat_head": head,
        "N_TL0": n_tl0,
        "warmup_steps": warmup,
        "hashes": hashes,
        "checks": checks,
        "nanochat_data_dir": "data/processed/p3-tl39-active",
        "note": "Exit 0 authorizes scripts/p3/gate_i_tl0.sh only. Metrics stay in lockbox.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "failed": [c["id"] for c in checks if not c["ok"]],
                "path": str(OUT.relative_to(ROOT)),
            },
            indent=2,
        )
    )
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
