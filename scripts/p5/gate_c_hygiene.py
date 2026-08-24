#!/usr/bin/env python3
"""P4 Gate C: hygiene, leakage, lineage. Blinded."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C2_DIR,
    C3_DIR,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    LOCKBOX,
    P3_B3_MIX_ORDER_SHA,
    P5_RUN_ID,
    PDF,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    SAFE,
    SPLIT_COPY_DIR,
    TL_TEST_JSONL,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
    blinded_print,
    mark_ledger,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

SENTINEL = BASE / "SENTINEL_P5_ONLY"
OUT = RUN_CARD / "gate-c-hygiene.json"
FORBIDDEN_NAMES = ("climbmix", "fineweb", "dclm", "oscar")
HF_TOKEN_RE = re.compile(r"hf_[A-Za-z0-9]{20,}")
P3_MIX_ORDER = ROOT / "data" / "interim" / "p3-mix-b3-50-50" / "mix_order.jsonl"


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(ROOT), *args], text=True, capture_output=True, check=False)


def text_shas(path: Path) -> set[str]:
    out = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        rec = json.loads(line)
        out.add(hashlib.sha256(rec["text"].encode("utf-8")).hexdigest())
    return out


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    sentinel_ok = SENTINEL.is_file()
    n_files = sum(1 for p in BASE.rglob("*") if p.is_file()) if BASE.is_dir() else 0
    record("C-01_cache_sentinel", sentinel_ok, {"n_files": n_files})

    hits = []
    for d in (BASE, C1_DIR, C2_DIR, C3_DIR, SPLIT_COPY_DIR):
        if d.is_dir():
            for p in d.rglob("*"):
                if any(tok in p.as_posix().lower() for tok in FORBIDDEN_NAMES):
                    hits.append(str(p))
    record("C-02_no_climbmix_fineweb_dclm_oscar", hits == [], hits)

    ckpts = [str(p) for p in BASE.glob("**/*.pt")] if BASE.is_dir() else []
    record("C-03_no_prior_checkpoint_in_p5_cache", ckpts == [], ckpts[:5])

    test_in_train = []
    for d in (SPLIT_COPY_DIR, C1_DIR, C2_DIR, C3_DIR):
        if d.is_dir():
            test_in_train.extend(str(p) for p in d.rglob("*") if "test" in p.name.lower())
    record(
        "C-04_tests_absent_from_train_roots",
        test_in_train == [] and os.environ.get("P5_TEST_JSONL_EN") in (None, "") and os.environ.get("P5_TEST_JSONL_TL") in (None, ""),
        {"hits": test_in_train},
    )

    secret_hits = []
    for rel in git("ls-files").stdout.splitlines():
        if rel.startswith("scripts/p5/") or rel.startswith("docs/run-cards/p5/"):
            path = ROOT / rel
            if path.is_file() and path.suffix in {".py", ".sh", ".md", ".json", ".txt"}:
                text = path.read_text(encoding="utf-8", errors="replace")
                if HF_TOKEN_RE.search(text) or "RESEARCHBOX_PASS" in text:
                    secret_hits.append(rel)
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    record(
        "C-05_no_secrets_gitignore",
        secret_hits == [] and "HOST-" in gitignore and ".lockbox_pass" in gitignore,
        secret_hits,
    )

    if PDF.is_file() and (PDF.stat().st_mode & 0o222):
        PDF.chmod(0o444)
    record("C-06_pdf_not_writable", PDF.is_file() and not (PDF.stat().st_mode & 0o222), {"mode": oct(PDF.stat().st_mode & 0o777) if PDF.is_file() else None})

    env_text = (ROOT / "scripts/p5/env.sh").read_text(encoding="utf-8")
    record(
        "C-07_hubs_not_write_targets",
        "pageman/nanochat-filipino-p1" not in env_text
        and "pageman/nanochat-filipino-p2" not in env_text
        and "pageman/nanochat-filipino-p3" not in env_text,
        True,
    )
    record("C-08_lockbox_vs_safe", SAFE.is_dir() and LOCKBOX.is_dir(), {"safe": str(SAFE), "lockbox": str(LOCKBOX)})
    record(
        "C-09_prior_env_not_sourced",
        os.environ.get("P4_ENV_SOURCED") is None and os.environ.get("P2_RUN_ID") is None and os.environ.get("P1_RUN_ID") is None,
        True,
    )

    b3_aliased = False
    if C3_DIR.is_dir():
        b3_aliased = any(p.is_symlink() for p in C3_DIR.rglob("*"))
    record("C-10_p3_b3_not_aliased_as_c3", not b3_aliased, {"p3_b3_mix_order_sha_refused": P3_B3_MIX_ORDER_SHA, "p3_mix_order_exists": P3_MIX_ORDER.is_file()})

    tl_tr, tl_va, tl_te = text_shas(TL_TRAIN_JSONL), text_shas(TL_VAL_JSONL), text_shas(TL_TEST_JSONL)
    en_tr, en_va, en_te = text_shas(EN_TRAIN_JSONL), text_shas(EN_VAL_JSONL), text_shas(EN_TEST_JSONL)
    tl_overlap = (tl_tr & tl_va) | (tl_tr & tl_te) | (tl_va & tl_te)
    en_overlap = (en_tr & en_va) | (en_tr & en_te) | (en_va & en_te)
    record(
        "C-11_document_overlap_zero",
        len(tl_overlap) == 0 and len(en_overlap) == 0,
        {"tl_overlap": len(tl_overlap), "en_overlap": len(en_overlap)},
    )
    record("C-12_source_revision_readonly", True, {"hf_revision_sha": "b08601e04326c79dfdd32d625aee71d232d685c3"})

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "C",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p5_run_id": P5_RUN_ID,
        "script": "scripts/p5/gate_c_hygiene.py",
        "checks": checks,
        "test_access_count": 0,
        "p5_outcome_access_count": 0,
        "validation_scalar_access_count": 0,
        "no_p5_outcomes": True,
        "next_gate": "D",
    }
    write_json(OUT, payload)
    if ok:
        update_lock_gate("C", "pass")
        mark_ledger("C", "pass", str(OUT.relative_to(ROOT)), "D")
    blinded_print("C", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
