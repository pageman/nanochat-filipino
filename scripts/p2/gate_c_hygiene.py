#!/usr/bin/env python3
"""P2 Gate C hygiene. Read-only checks plus a failed write probe on frozen P1.1 active."""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P2_RUN_ID = os.environ.get("P2_RUN_ID", "p2-20260817T150944Z-de99f8a")
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data" / "cache" / P2_RUN_ID))
ACTIVE = ROOT / "data" / "processed" / "wikitext-tl39" / "active"
TEST = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
ENRAW = ROOT / "data" / "raw" / "wikitext-103-raw"
ENV_SH = ROOT / "scripts" / "p2" / "env.sh"
OUT = ROOT / "docs" / "run-cards" / "p2" / P2_RUN_ID / "gate-c-hygiene.json"
FORBIDDEN_NAMES = ("climbmix", "fineweb", "dclm", "oscar")
HF_TOKEN_RE = re.compile(r"hf_[A-Za-z0-9]{20,}")
RUNPOD_ASSIGN_RE = re.compile(r"RUNPOD_API_KEY\s*=\s*['\"]?[A-Za-z0-9_-]{20,}")
HF_HUB_ASSIGN_RE = re.compile(r"HUGGING_FACE_HUB_TOKEN\s*=\s*['\"]?\S{8,}")
PASSCODE_FIELD_RE = re.compile(r"(?i)(?:passcode|researchbox\s*code)\s*[:=]\s*([A-Za-z0-9]{6,})")
P1_HUB = "pageman/nanochat-filipino-p1-fixed-d20-3x"
P2_HUB = "pageman/nanochat-filipino-p2-en-then-tl"
P1_SUBMITTED = "docs/run-cards/aspredicted-p1-submitted.txt"
P2_SUBMITTED = "docs/run-cards/aspredicted-p2-submitted.txt"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        text=True,
        capture_output=True,
        check=check,
    )


def writable(path: Path) -> bool:
    return bool(path.stat().st_mode & 0o222)


def passcodes_from_gitignored_submitted() -> list[str]:
    found: list[str] = []
    for rel in (P1_SUBMITTED, P2_SUBMITTED):
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in PASSCODE_FIELD_RE.finditer(text):
            found.append(match.group(1))
    return found


def scan_secrets(path: Path, rel: str, passcodes: list[str]) -> list[dict]:
    hits = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return hits
    for code in passcodes:
        if code and code in text:
            hits.append({"file": rel, "needle": "researchbox_passcode"})
    if HF_TOKEN_RE.search(text):
        hits.append({"file": rel, "needle": "hf_token"})
    if RUNPOD_ASSIGN_RE.search(text):
        hits.append({"file": rel, "needle": "runpod_api_key_assignment"})
    if HF_HUB_ASSIGN_RE.search(text):
        hits.append({"file": rel, "needle": "hf_hub_token_assignment"})
    return hits


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    base_entries = sorted(p.relative_to(BASE).as_posix() for p in BASE.rglob("*") if p != BASE) if BASE.is_dir() else []
    record(
        "C1_p2_cache_only",
        BASE.is_dir() and set(base_entries) <= {".p2_run_id"},
        {"base": str(BASE), "entries": base_entries},
    )

    hits = []
    if BASE.is_dir():
        for p in BASE.rglob("*"):
            low = p.as_posix().lower()
            if any(tok in low for tok in FORBIDDEN_NAMES):
                hits.append(str(p))
    record("C2_no_climbmix_fineweb_dclm_oscar", hits == [], hits)

    active_ok = ACTIVE.is_dir()
    active_writable = []
    write_probe_blocked = False
    write_probe_error = None
    if active_ok:
        if writable(ACTIVE):
            active_writable.append(str(ACTIVE))
        for child in ACTIVE.iterdir():
            if writable(child):
                active_writable.append(str(child))
        probe = ACTIVE / ".p2_write_probe"
        try:
            probe.write_text("p2-must-not-write\n", encoding="utf-8")
            probe.unlink(missing_ok=True)
            write_probe_blocked = False
            write_probe_error = "write succeeded"
        except OSError as exc:
            write_probe_blocked = True
            write_probe_error = f"{type(exc).__name__}: {exc}"
    record(
        "C3_p11_active_readonly",
        active_ok and active_writable == [] and write_probe_blocked,
        {
            "active": str(ACTIVE),
            "mode": oct(ACTIVE.stat().st_mode & 0o777) if active_ok else None,
            "writable": active_writable,
            "write_probe_blocked": write_probe_blocked,
            "write_probe_error": write_probe_error,
        },
    )

    test_in_p2 = [str(p) for p in (BASE.rglob("test.jsonl") if BASE.is_dir() else [])]
    test_in_en = [str(p) for p in (ENRAW.rglob("test.jsonl") if ENRAW.is_dir() else [])]
    record(
        "C4_p11_test_not_in_p2_train",
        TEST.is_file() and not test_in_p2 and not test_in_en,
        {
            "p11_test": str(TEST),
            "test_mode": oct(TEST.stat().st_mode & 0o777) if TEST.is_file() else None,
            "in_p2_cache": test_in_p2,
            "in_english_raw": test_in_en,
            "test_writable": writable(TEST) if TEST.is_file() else None,
        },
    )

    passcodes = passcodes_from_gitignored_submitted()
    secret_hits = []
    tracked = git("ls-files").stdout.splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard").stdout.splitlines()
    for rel in tracked + untracked:
        path = ROOT / rel
        if path.resolve() == OUT.resolve():
            continue
        if path.is_file():
            secret_hits.extend(scan_secrets(path, rel, passcodes))
    record(
        "C5_no_secrets_in_files_that_will_be_committed",
        secret_hits == [],
        {
            "hits": secret_hits,
            "gitignored_passcodes_loaded": len(passcodes),
            "note": "Passcode values are not written to this JSON.",
        },
    )

    porcelain = git("status", "--porcelain").stdout
    staged = [ln[3:] for ln in porcelain.splitlines() if ln and ln[0] in "MADRCU"]
    p1_ignored = git("check-ignore", "-q", P1_SUBMITTED, check=False).returncode == 0
    p2_ignored = git("check-ignore", "-q", P2_SUBMITTED, check=False).returncode == 0
    record(
        "C6_p1_submitted_not_staged",
        P1_SUBMITTED not in staged
        and P2_SUBMITTED not in staged
        and p1_ignored
        and p2_ignored,
        {
            "staged": staged,
            "p1_submitted_ignored": p1_ignored,
            "p2_submitted_ignored": p2_ignored,
        },
    )

    lfs_proc = git("lfs", "ls-files", check=False)
    git_lfs_installed = lfs_proc.returncode == 0
    lfs_files = (lfs_proc.stdout or "").strip() if git_lfs_installed else ""
    gitattributes = ROOT / ".gitattributes"
    gitattributes_has_lfs = False
    if gitattributes.is_file():
        gitattributes_has_lfs = "filter=lfs" in gitattributes.read_text(encoding="utf-8", errors="replace")
    env_text = ENV_SH.read_text(encoding="utf-8") if ENV_SH.is_file() else ""
    env_forbids_p1_hub = P1_HUB in env_text and "MUST NOT write" in env_text
    record(
        "C7_p1_d20_not_lfs_push_target",
        (not git_lfs_installed)
        and not (ROOT / ".lfsconfig").exists()
        and not gitattributes_has_lfs
        and P1_HUB not in lfs_files
        and env_forbids_p1_hub,
        {
            "git_lfs_installed": git_lfs_installed,
            "lfs_files": lfs_files or "none",
            "lfsconfig_exists": (ROOT / ".lfsconfig").exists(),
            "gitattributes_has_lfs": gitattributes_has_lfs,
            "env_sh_forbids_p1_hub": env_forbids_p1_hub,
            "p2_hub": P2_HUB,
        },
    )

    ok = all(c["ok"] for c in checks)
    out = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "gate": "C",
        "status": "pass" if ok else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": "Mac/CPU",
        "p2_run_id": P2_RUN_ID,
        "script": "scripts/p2/gate_c_hygiene.py",
        "checks": checks,
        "started_en0": False,
        "next_gate": "D",
        "next_gate_note": "Official WikiText-103 raw train/valid/test article split. Do not re-hash 70/15/15. No GPU. Do not start EN0.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": out["status"],
                "path": str(OUT.relative_to(ROOT)),
                "failed": [c["id"] for c in checks if not c["ok"]],
            },
            indent=2,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
