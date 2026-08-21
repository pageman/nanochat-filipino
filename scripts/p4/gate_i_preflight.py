#!/usr/bin/env python3
"""P4 Gate I TL0 preflight. Does not train. Authorizes gate_i_tl0.sh only."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256  # noqa: E402
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C3_DIR,
    EXPECTED,
    N_TL0,
    P4_RUN_ID,
    PIN,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TOK_DIR,
    TOKEN_BYTES_SHA,
    TOKENIZER_PKL_SHA,
    VENDOR,
    WARMUP,
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-i-preflight.json"
AUTH = RUN_CARD / "gate-i-authorization.json"
GATE_H = RUN_CARD / "gate-h-cuda-smoke.json"
GATE_G = RUN_CARD / "gate-g-budget-command-freeze.json"
TL0_TAGS = ("p4-tl0-d8", "p4-tl0-d20")


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
    checks = []

    def record(cid: str, ok: bool, detail=None) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    record("I0_not_darwin", platform.system() != "Darwin", platform.system())
    auth = json.loads(AUTH.read_text(encoding="utf-8")) if AUTH.is_file() else {}
    record(
        "I0_authorization",
        auth.get("gate") == "I" and auth.get("authorized") is True and auth.get("authorizes_children") is False,
        str(AUTH.relative_to(ROOT)) if AUTH.is_file() else None,
    )

    gate_h_ok = False
    if GATE_H.is_file():
        gate_h = json.loads(GATE_H.read_text(encoding="utf-8"))
        gate_h_ok = gate_h.get("status") == "pass" and gate_h.get("health") == "pass"
    record("I0_gate_h_pass", gate_h_ok, GATE_H.name if GATE_H.is_file() else "missing")

    hashes = {}
    tok_ok = True
    for name, path, exp in (
        ("tokenizer.pkl", TOK_DIR / "tokenizer.pkl", TOKENIZER_PKL_SHA),
        ("token_bytes.pt", TOK_DIR / "token_bytes.pt", TOKEN_BYTES_SHA),
    ):
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == exp, "got": got}
        tok_ok = tok_ok and hashes[name]["ok"]
    shard_ok = True
    for name, exp in EXPECTED["c1_shards"].items():
        path = C1_DIR / name
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == exp, "got": got}
        shard_ok = shard_ok and hashes[name]["ok"]
    record("I0_hashes", tok_ok and shard_ok, {k: v["ok"] for k, v in hashes.items()})

    head = git("rev-parse", "HEAD") if (VENDOR / ".git").is_dir() else None
    record("I0_pin", head == PIN, head)
    fa_diff = subprocess.run(
        ["git", "-C", str(VENDOR), "diff", PIN, "--", "nanochat/flash_attention.py"],
        text=True,
        capture_output=True,
    ).stdout
    record("I0_flash_attention_unpatched", fa_diff == "", fa_diff or "empty")

    names = sorted(p.name for p in C1_DIR.glob("*.parquet")) if C1_DIR.is_dir() else []
    record("I0_last_shard_val", bool(names) and names[-1] == "val.parquet", names)
    test_hits = [p.name for p in C1_DIR.rglob("*") if "test" in p.name.lower()] if C1_DIR.is_dir() else []
    record("I0_no_test_in_c1", test_hits == [])
    record(
        "I0_data_dir_not_c3",
        os.environ.get("NANOCHAT_DATA_DIR") in (None, "", str(C1_DIR)),
        os.environ.get("NANOCHAT_DATA_DIR"),
    )

    empty_ok = True
    empty_detail = {}
    for tag in TL0_TAGS:
        tag_dir = BASE / "base_checkpoints" / tag
        pts = list(tag_dir.glob("model_*.pt")) if tag_dir.is_dir() else []
        empty_detail[tag] = [p.name for p in pts]
        if pts:
            empty_ok = False
    record("I0_tl0_dirs_empty", empty_ok, empty_detail)
    record("I0_no_forbidden_parent_ckpts", scan_forbidden_ckpts() == [], None)

    reject_ok = True
    try:
        reject_parent_sha256(next(iter(FORBIDDEN_PARENT_SHA256)))
        reject_ok = False
    except SystemExit:
        reject_ok = True
    record("I0_forbidden_reject_live", reject_ok)

    n_tl0, warmup = N_TL0, WARMUP
    if GATE_G.is_file():
        gate_g = json.loads(GATE_G.read_text(encoding="utf-8"))
        n_tl0 = int(gate_g.get("N_TL0", N_TL0))
        warmup = int(gate_g.get("commands", {}).get("parent", {}).get("warmup_steps", WARMUP))
    record("I0_n_tl0_locked", n_tl0 == N_TL0, n_tl0)
    record("I0_warmup_legal", warmup < n_tl0, f"warmup={warmup} N_TL0={n_tl0}")

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
    record("I0_cuda", cuda, {"gpu": gpu_name, "sm": sm})
    record("I0_gpu_class_a40", "A40" in (gpu_name or ""), gpu_name)

    nmi_ok = False
    nmi_head = ""
    try:
        nmi = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        nmi_ok = nmi.returncode == 0
        nmi_head = "\n".join((nmi.stdout or nmi.stderr or "").splitlines()[:12])
    except FileNotFoundError:
        nmi_head = "nvidia-smi_not_on_path"
    record("I0_nvidia_smi", nmi_ok, nmi_head or None)

    ready = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "I-preflight",
        "status": "ready_for_tl0" if ready else "not_ready",
        "at_utc": utc_now(),
        "host": platform.node(),
        "p4_run_id": P4_RUN_ID,
        "nanochat_head": head,
        "N_TL0": n_tl0,
        "warmup_steps": warmup,
        "hashes": hashes,
        "checks": checks,
        "nanochat_data_dir": "data/cache/p4-20260821T060032Z-92d63d4/streams/c1_tl",
        "blinded": True,
        "no_p4_outcomes": True,
        "note": "Exit 0 authorizes scripts/p4/gate_i_tl0.sh only. Metrics stay in lockbox. Not C0 freeze.",
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
