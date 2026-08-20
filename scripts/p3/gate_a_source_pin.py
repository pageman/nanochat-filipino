#!/usr/bin/env python3
"""P3 Gate A: pin nanochat, isolated cache, prohibited-path scan."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from p3_common import ASPREDICTED_ID, BASE, PIN, P3_RUN_ID, RESEARCHBOX_ID, RESEARCHBOX_URL, ROOT, RUN_CARD, VENDOR

OUT = RUN_CARD / "gate-a-source-pin.json"
SENTINEL = BASE / "SENTINEL_P3_ONLY"
PATCH = ROOT / "patches" / "nanochat-NANOCHAT_DATA_DIR.patch"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str, must_succeed: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if must_succeed and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return (proc.stdout or "").strip()


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    head = git("rev-parse", "HEAD") if VENDOR.is_dir() else None
    record("A1_pin_checkout", head == PIN, {"head": head, "expected": PIN})

    allowed_diff = ""
    if VENDOR.is_dir():
        for rel in ("nanochat/dataset.py", "nanochat/common.py"):
            allowed_diff += git("diff", PIN, "--", rel, must_succeed=False)
    patch_sha = sha256_file(PATCH) if PATCH.is_file() else None
    record(
        "A2_allowed_diff_only_data_hook",
        "NANOCHAT_DATA_DIR" in allowed_diff and "flash_attention" not in allowed_diff,
        {"patch_sha256": patch_sha, "diff_chars": len(allowed_diff)},
    )

    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / "safe_progress").mkdir(exist_ok=True)
    (BASE / "lockbox").mkdir(exist_ok=True)
    SENTINEL.write_text(
        f"P3_RUN_ID={P3_RUN_ID}\naspredicted={ASPREDICTED_ID}\nresearchbox={RESEARCHBOX_ID}\n",
        encoding="utf-8",
    )
    record("A3_sentinel", SENTINEL.is_file(), str(SENTINEL.relative_to(ROOT)))

    env_p1 = (ROOT / "scripts/p1/env.sh").read_text(encoding="utf-8") if (ROOT / "scripts/p1/env.sh").is_file() else ""
    env_p3 = (ROOT / "scripts/p3/env.sh").read_text(encoding="utf-8")
    record(
        "A4_no_p1_p2_cache_in_p3_env",
        "p1-20260816" not in env_p3 and "p2-20260817" not in env_p3 and P3_RUN_ID in env_p3,
        {"p3_env_has_run_id": P3_RUN_ID in env_p3},
    )
    record("A5_p3_env_not_p1_copy", "P2_RUN_ID" not in env_p3 and "P1_ROOT" not in env_p3, True)

    p3_ckpts = list(BASE.glob("model_*.pt"))
    record("A6_no_p3_checkpoints_yet", p3_ckpts == [], [str(p) for p in p3_ckpts])

    record("A7_researchbox_recorded", RESEARCHBOX_ID == 8834, {"id": RESEARCHBOX_ID, "url": RESEARCHBOX_URL})

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "researchbox_url": RESEARCHBOX_URL,
        "gate": "A",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_a_source_pin.py",
        "nanochat_pin": PIN,
        "nanochat_head": head,
        "allowed_diff_sha256": hashlib.sha256(allowed_diff.encode()).hexdigest() if allowed_diff else None,
        "patch_sha256": patch_sha,
        "sentinel": str(SENTINEL.relative_to(ROOT)),
        "checks": checks,
        "no_p3_outcomes": True,
        "next_gate": "B",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
