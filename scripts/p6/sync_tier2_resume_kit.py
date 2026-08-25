#!/usr/bin/env python3
"""Sync or initialize the P6-M Tier-2 portable resume kit (host-independent).

Minimum viable resume kit after a gate pass:
  - latest checkpoint .pt (when present)
  - tokenizer.pkl + token_bytes.pt (when present)
  - LOCK.json + gate ledger copy
  - env / script identity hashes

Does not print BPB scalars. Does not require a live GPU pod.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    LEDGER_PATH,
    LOCK_PATH,
    NETWORK_VOLUME_DC,
    NETWORK_VOLUME_GB,
    NETWORK_VOLUME_ID,
    P6_RUN_ID,
    PARENT_SEED,
    ROOT,
    TIER2,
    TOK_DIR,
    sha256_file,
    utc_now,
    write_json,
)


def copy_if_exists(src: Path, dst: Path) -> dict | None:
    if not src.is_file():
        return None
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"path": str(dst.relative_to(TIER2)), "sha256": sha256_file(dst), "bytes": dst.stat().st_size}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--init-only", action="store_true", help="Create empty kit scaffold + manifest")
    p.add_argument("--checkpoint", type=Path, default=None, help="Optional latest .pt to include")
    p.add_argument("--gate", default="0", help="Gate label recorded in the kit receipt")
    args = p.parse_args()

    TIER2.mkdir(parents=True, exist_ok=True)
    (TIER2 / "checkpoints").mkdir(parents=True, exist_ok=True)
    (TIER2 / "tokenizer").mkdir(parents=True, exist_ok=True)
    (TIER2 / "authority").mkdir(parents=True, exist_ok=True)
    (TIER2 / "scripts_identity").mkdir(parents=True, exist_ok=True)

    files: dict[str, dict] = {}
    lock_copy = copy_if_exists(LOCK_PATH, TIER2 / "authority" / "LOCK.json")
    if lock_copy:
        files["LOCK.json"] = lock_copy
    if LEDGER_PATH.is_file():
        led = copy_if_exists(LEDGER_PATH, TIER2 / "authority" / "p6_gate_ledger.json")
        if led:
            files["p6_gate_ledger.json"] = led

    if not args.init_only:
        for name in ("tokenizer.pkl", "token_bytes.pt"):
            src = TOK_DIR / name
            entry = copy_if_exists(src, TIER2 / "tokenizer" / name)
            if entry:
                files[name] = entry
        if args.checkpoint is not None:
            entry = copy_if_exists(args.checkpoint, TIER2 / "checkpoints" / args.checkpoint.name)
            if entry:
                files[args.checkpoint.name] = entry

    # Script identity hashes for cold-start verification (no payloads)
    for rel in (
        "scripts/p6/env.sh",
        "scripts/p6/p6_common.py",
        "scripts/p6/sync_tier2_resume_kit.py",
    ):
        src = ROOT / rel
        if src.is_file():
            files[rel] = {"path": rel, "sha256": sha256_file(src), "bytes": src.stat().st_size}

    manifest = {
        "kit": "p6-m-tier2-resume-kit",
        "p6_run_id": P6_RUN_ID,
        "parent_seed": PARENT_SEED,
        "gate": args.gate,
        "at_utc": utc_now(),
        "init_only": bool(args.init_only),
        "network_volume": {
            "id": NETWORK_VOLUME_ID,
            "dc": NETWORK_VOLUME_DC,
            "gb": NETWORK_VOLUME_GB,
            "role": "archival_or_colocated_future; live A40 recovery uses this local kit when DCs differ",
        },
        "invariant": "Never let a gate-critical checkpoint exist in only one host-pinned place",
        "files": files,
        "note": "Minimum viable resume kit. Full optimizer state remains Tier-1 until explicitly archived.",
    }
    write_json(TIER2 / "RESUME_KIT_MANIFEST.json", manifest)
    print(
        json.dumps(
            {
                "status": "ok",
                "tier2": str(TIER2),
                "init_only": bool(args.init_only),
                "file_count": len(files),
                "at_utc": manifest["at_utc"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
