#!/usr/bin/env python3
"""P3 Gate C: hygiene, leakage, lineage."""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from p3_common import (
    ASPREDICTED_ID,
    BASE,
    B3_DIR,
    EN_DIR,
    EN_TEST_JSONL,
    P3_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TL_DIR,
    TL_TEST,
)

FORBIDDEN_NAMES = ("climbmix", "fineweb", "dclm", "oscar")
P1_HUB = "pageman/nanochat-filipino-p1-fixed-d20-3x"
P2_HUB = "pageman/nanochat-filipino-p2-en-then-tl"
ENV_SH = ROOT / "scripts/p3/env.sh"
HF_TOKEN_RE = re.compile(r"hf_[A-Za-z0-9]{20,}")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(ROOT), *args], text=True, capture_output=True, check=check)


def main() -> int:
    OUT = RUN_CARD / "gate-c-hygiene.json"
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    sentinel_ok = (BASE / "SENTINEL_P3_ONLY").is_file()
    base_entries = sorted(p.relative_to(BASE).as_posix() for p in BASE.rglob("*") if p.is_file()) if BASE.is_dir() else []
    record("C1_p3_cache_sentinel", sentinel_ok, {"entries": base_entries[:20], "n_files": len(base_entries)})

    hits = []
    for d in (BASE, TL_DIR, EN_DIR, B3_DIR):
        if d.is_dir():
            for p in d.rglob("*"):
                if any(tok in p.as_posix().lower() for tok in FORBIDDEN_NAMES):
                    hits.append(str(p))
    record("C2_no_climbmix_fineweb_dclm_oscar", hits == [], hits)

    forbidden_ckpts = []
    for pat in ("**/model_000294.pt", "**/p1-fixed-d20-3x/**", "**/p2-en-then-tl/**"):
        forbidden_ckpts.extend(str(p) for p in ROOT.glob(pat) if "vendor" not in str(p))
    record(
        "C3_no_p11_p2_checkpoint_in_p3_train_paths",
        not any("data/cache/p3" in p for p in forbidden_ckpts),
        {"forbidden_sample": forbidden_ckpts[:5]},
    )

    test_in_train = []
    for d in (TL_DIR, EN_DIR, B3_DIR):
        if d.is_dir():
            test_in_train.extend(str(p) for p in d.rglob("*") if "test" in p.name.lower())
    record(
        "C4_test_absent_from_p3_train_roots",
        test_in_train == [] and TL_TEST.is_file() and EN_TEST_JSONL.is_file(),
        {"test_hits_in_train_dirs": test_in_train, "tl_test": str(TL_TEST), "en_test": str(EN_TEST_JSONL)},
    )

    secret_hits = []
    for rel in git("ls-files").stdout.splitlines():
        path = ROOT / rel
        if path.is_file() and rel.startswith("scripts/p3/"):
            text = path.read_text(encoding="utf-8", errors="replace")
            if HF_TOKEN_RE.search(text):
                secret_hits.append(rel)
    record("C5_no_secrets_in_p3_scripts", secret_hits == [], secret_hits)

    env_text = ENV_SH.read_text(encoding="utf-8")
    record(
        "C6_p3_env_forbids_p1_p2",
        "scripts/p1/env.sh" in env_text and "scripts/p2/env.sh" in env_text and "MUST NOT" in env_text,
        True,
    )
    record("C7_hubs_not_write_targets", P1_HUB not in env_text and P2_HUB not in env_text, True)

    safe = BASE / "safe_progress"
    lock = BASE / "lockbox"
    perm_ok = safe.is_dir() and lock.is_dir()
    record("C8_safe_progress_and_lockbox_exist", perm_ok, {"safe": str(safe), "lockbox": str(lock)})

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "C",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_c_hygiene.py",
        "checks": checks,
        "test_access_count": 0,
        "p3_outcome_access_count": 0,
        "next_gate": "D",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
