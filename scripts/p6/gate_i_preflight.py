#!/usr/bin/env python3
"""P6 Gate I_s TL0 preflight. Does not train."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256  # noqa: E402
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C3_DIR,
    EXPECTED,
    N_TL0,
    P6_RUN_ID,
    PANEL_SEEDS,
    PIN,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TOK_DIR,
    TOKEN_BYTES_SHA,
    TOKENIZER_PKL_SHA,
    VENDOR,
    WARMUP,
    require_auth,
    seed_card,
    sha256_file,
    tl0_tag,
    utc_now,
    write_json,
)


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return proc.stdout.strip()


def main() -> int:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if seed not in PANEL_SEEDS:
        raise SystemExit(f"usage: gate_i_preflight.py one of {PANEL_SEEDS}")
    checks = []

    def record(cid: str, ok: bool, detail=None) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    record("I0_not_darwin", platform.system() != "Darwin", platform.system())
    auth = require_auth(seed_card(seed) / "gate-i-authorization.json", "I", {"seed": seed, "authorizes_children": False})
    record("I0_authorization", True, auth.get("scope"))

    gate_h = json.loads((RUN_CARD / "gate-h-cuda-smoke.json").read_text()) if (RUN_CARD / "gate-h-cuda-smoke.json").is_file() else {}
    record("I0_gate_h_pass", gate_h.get("status") == "pass" and gate_h.get("health") == "pass")

    seed_idx = PANEL_SEEDS.index(seed)
    if seed_idx > 0:
        prev = PANEL_SEEDS[seed_idx - 1]
        v_rec = seed_card(prev) / "gate-v-test.json"
        inelig = seed_card(prev) / "ineligible_parent.json"
        lawful = (v_rec.is_file() and json.loads(v_rec.read_text()).get("status") == "pass") or inelig.is_file()
        record("I0_prior_seed_terminal", lawful, f"seed-{prev}")
    else:
        record("I0_prior_seed_terminal", True, "first/only panel seed")

    hashes = {}
    tok_ok = True
    for name, path, exp in (
        ("tokenizer.pkl", TOK_DIR / "tokenizer.pkl", TOKENIZER_PKL_SHA),
        ("token_bytes.pt", TOK_DIR / "token_bytes.pt", TOKEN_BYTES_SHA),
    ):
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == exp}
        tok_ok = tok_ok and hashes[name]["ok"]
    shard_ok = True
    for name, exp in EXPECTED["c1_shards"].items():
        path = C1_DIR / name
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == exp}
        shard_ok = shard_ok and hashes[name]["ok"]
    record("I0_hashes", tok_ok and shard_ok, {k: v["ok"] for k, v in hashes.items()})
    head = git("rev-parse", "HEAD") if (VENDOR / ".git").is_dir() else None
    record("I0_pin", head == PIN, head)
    names = sorted(p.name for p in C1_DIR.glob("*.parquet")) if C1_DIR.is_dir() else []
    record("I0_last_shard_val", bool(names) and names[-1] == "val.parquet", names)
    record("I0_no_test_in_c1", [p.name for p in C1_DIR.rglob("*") if "test" in p.name.lower()] == [])
    record("I0_data_dir_not_c3", os.environ.get("NANOCHAT_DATA_DIR") in (None, "", str(C1_DIR)))

    empty_ok = True
    empty_detail = {}
    for depth in (8, 20):
        tag = tl0_tag(seed, depth)
        pts = list((BASE / "base_checkpoints" / tag).glob("model_*.pt")) if (BASE / "base_checkpoints" / tag).is_dir() else []
        empty_detail[tag] = [p.name for p in pts]
        if pts:
            empty_ok = False
    record("I0_tl0_dirs_empty", empty_ok, empty_detail)
    reject_ok = True
    try:
        reject_parent_sha256(next(iter(FORBIDDEN_PARENT_SHA256)))
        reject_ok = False
    except SystemExit:
        reject_ok = True
    record("I0_forbidden_reject_live", reject_ok)
    record("I0_n_tl0_locked", N_TL0 == 294, N_TL0)
    record("I0_warmup_legal", WARMUP < N_TL0)
    cuda = False
    gpu_name = None
    try:
        import torch

        cuda = bool(torch.cuda.is_available())
        gpu_name = torch.cuda.get_device_name(0) if cuda else None
    except Exception as exc:  # noqa: BLE001
        gpu_name = type(exc).__name__
    record("I0_cuda", cuda, gpu_name)
    record("I0_gpu_class_a40", "A40" in (gpu_name or ""), gpu_name)
    ready = all(c["ok"] for c in checks)
    out = seed_card(seed) / "gate-i-preflight.json"
    write_json(
        out,
        {
            "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
            "aspredicted_id": ASPREDICTED_ID,
            "researchbox_id": RESEARCHBOX_ID,
            "gate": "I-preflight",
            "seed": seed,
            "status": "ready_for_tl0" if ready else "not_ready",
            "at_utc": utc_now(),
            "host": platform.node(),
            "p6_run_id": P6_RUN_ID,
            "checks": checks,
            "blinded": True,
            "note": f"Exit 0 authorizes Gate I_{seed} TL0 only.",
        },
    )
    print(json.dumps({"status": "ready_for_tl0" if ready else "not_ready", "seed": seed, "failed": [c["id"] for c in checks if not c["ok"]], "blinded": True}, indent=2))
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
