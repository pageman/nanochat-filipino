#!/usr/bin/env python3
"""P4 Gate F: carry-forward tokenizer. Copy + verify both filed SHAs. Blinded."""

from __future__ import annotations

import os
import shutil
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    P4_TOK_DIR,
    P6_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TOK_DIR,
    TOKEN_BYTES_SHA,
    TOKENIZER_PKL_SHA,
    blinded_print,
    freeze_file,
    mark_ledger,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-f-tokenizer.json"


def copy_readonly(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.chmod(0o644)
    shutil.copy2(src, dst)
    freeze_file(dst)
    return sha256_file(dst)


def write_probe(path: Path) -> bool:
    try:
        with path.open("ab") as f:
            f.write(b"")
        return False
    except OSError:
        return True


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    pkl_src = P4_TOK_DIR / "tokenizer.pkl"
    bytes_src = P4_TOK_DIR / "token_bytes.pt"
    record("F0_carry_forward_sources_exist", pkl_src.is_file() and bytes_src.is_file(), {"src": str(P4_TOK_DIR.relative_to(ROOT))})

    pkl_sha = copy_readonly(pkl_src, TOK_DIR / "tokenizer.pkl")
    bytes_sha = copy_readonly(bytes_src, TOK_DIR / "token_bytes.pt")
    record("F1_tokenizer_pkl_sha", pkl_sha == TOKENIZER_PKL_SHA, {"got": pkl_sha, "expected": TOKENIZER_PKL_SHA})
    record("F2_token_bytes_sha", bytes_sha == TOKEN_BYTES_SHA, {"got": bytes_sha, "expected": TOKEN_BYTES_SHA})
    record("F3_write_probe_pkl", write_probe(TOK_DIR / "tokenizer.pkl"), True)
    record("F4_write_probe_bytes", write_probe(TOK_DIR / "token_bytes.pt"), True)
    record("F5_not_p2_english_tokenizer", pkl_sha != "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6", True)
    record("F6_no_p5_bpb", True, {"fertility": "deferred_optional_lockbox_after_E"})

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "F",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "script": "scripts/p6/gate_f_tokenizer.py",
        "policy": "carry_forward",
        "tokenizer_dir": str(TOK_DIR.relative_to(ROOT)),
        "hashes": {"tokenizer.pkl": pkl_sha, "token_bytes.pt": bytes_sha},
        "input_manifest": {
            "src_tokenizer_dir": str(P4_TOK_DIR.relative_to(ROOT)),
            "reuse_weights": False,
            "reuse_tokenizer_artifacts": True,
        },
        "checks": checks,
        "no_p5_bpb": True,
        "next_gate": "E",
    }
    write_json(OUT, payload)
    if ok:
        update_lock_gate("F", "pass")
        mark_ledger("F", "pass", str(OUT.relative_to(ROOT)), "E")
    blinded_print("F", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]], "policy": "carry_forward"})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
