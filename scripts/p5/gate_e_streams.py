#!/usr/bin/env python3
"""P5 Gate E: verify/copy P4 C1/C2/C3 packed streams and language-origin mask by SHA."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C2_DIR,
    C3_DIR,
    EXPECTED,
    LOCKBOX,
    MIX_MANIFEST_SHA,
    P4_BASE,
    P5_RUN_ID,
    ROOT,
    RUN_CARD,
    blinded_print,
    freeze_file,
    mark_ledger,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-e-packed-streams.json"
MANIFEST_OUT = ROOT / "manifests" / "p5" / "p5_mix_identity.json"
P4_MANIFEST = ROOT / "manifests" / "p4" / "p4_mix_manifest.json"
MASK_SRC = P4_BASE / "lockbox" / "c3_language_origin_mask.bin"
MASK_DST = LOCKBOX / "c3_language_origin_mask.bin"


def copy_tree(src_dir: Path, dst_dir: Path, expected: dict[str, str]) -> list[dict]:
    rows = []
    dst_dir.mkdir(parents=True, exist_ok=True)
    for name, exp in expected.items():
        src = src_dir / name
        dst = dst_dir / name
        if not src.is_file():
            raise SystemExit(f"missing P4 artifact {src}")
        if dst.exists():
            dst.chmod(0o644)
        shutil.copy2(src, dst)
        got = sha256_file(dst)
        freeze_file(dst)
        rows.append({"file": name, "expected": exp, "sha256": got, "ok": got == exp})
    return rows


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    c1 = copy_tree(P4_BASE / "streams" / "c1_tl", C1_DIR, EXPECTED["c1_shards"])
    c2 = copy_tree(P4_BASE / "streams" / "c2_en", C2_DIR, EXPECTED["c2_shards"])
    c3 = copy_tree(P4_BASE / "streams" / "c3_mix", C3_DIR, EXPECTED["c3_train_shards"])
    record("E1_c1_hashes", all(r["ok"] for r in c1), c1)
    record("E2_c2_hashes", all(r["ok"] for r in c2), c2)
    record("E3_c3_train_shard_hashes", all(r["ok"] for r in c3 if r["file"].startswith("train_")), c3)

    LOCKBOX.mkdir(parents=True, exist_ok=True)
    if MASK_DST.exists():
        MASK_DST.chmod(0o644)
    shutil.copy2(MASK_SRC, MASK_DST)
    mask_sha = sha256_file(MASK_DST)
    freeze_file(MASK_DST)
    record(
        "E4_language_origin_mask",
        mask_sha == EXPECTED["language_origin_mask_sha256"],
        {"got": mask_sha, "expected": EXPECTED["language_origin_mask_sha256"]},
    )

    p4_manifest_sha = sha256_file(P4_MANIFEST) if P4_MANIFEST.is_file() else None
    record("E5_p4_mix_manifest_reference", p4_manifest_sha == MIX_MANIFEST_SHA, {"sha256": p4_manifest_sha})

    identity = {
        "p5_run_id": P5_RUN_ID,
        "source_p4_run_id": P4_BASE.name,
        "reuse_policy": "byte_identical_copy_from_p4_cache",
        "mix_manifest_sha256": MIX_MANIFEST_SHA,
        "language_origin_mask_sha256": EXPECTED["language_origin_mask_sha256"],
        "c3_train_shards": EXPECTED["c3_train_shards"],
        "c3_is_not_p3_b3": True,
        "created_utc": utc_now(),
    }
    write_json(MANIFEST_OUT, identity)
    freeze_file(MANIFEST_OUT)

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED",
        "aspredicted_id": ASPREDICTED_ID,
        "gate": "E",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p5_run_id": P5_RUN_ID,
        "script": "scripts/p5/gate_e_streams.py",
        "checks": checks,
        "mix_identity": str(MANIFEST_OUT.relative_to(ROOT)),
        "no_p5_outcomes": True,
        "next_gate": "G",
    }
    write_json(OUT, payload)
    if ok:
        update_lock_gate("E", "pass", {"mix_manifest_sha256": MIX_MANIFEST_SHA})
        mark_ledger("E", "pass", str(OUT.relative_to(ROOT)), "G")
    blinded_print("E", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
