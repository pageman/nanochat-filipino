#!/usr/bin/env python3
"""P3 Gate Q: freeze TL0 d20 as immutable B0."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
from datetime import datetime, timezone
from pathlib import Path

from p3_common import ASPREDICTED_ID, BASE, PIN, P3_RUN_ID, RESEARCHBOX_ID, ROOT, RUN_CARD
from phase2_common import B0_SHA256, B0_STEP, B0_TAG, TOKENIZER_SHA

OUT = RUN_CARD / "gate-q-b0-freeze.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-copy", action="store_true")
    args = ap.parse_args()

    gate_i = json.loads((RUN_CARD / "gate-i-tl0-d20.json").read_text(encoding="utf-8"))
    gate_p0t = json.loads((RUN_CARD / "gate-p0-t.json").read_text(encoding="utf-8"))
    if gate_i.get("status") != "pass" or gate_p0t.get("p0_t_status") != "PASS":
        raise SystemExit("Gate I d20 or P0-T not pass")

    src_dir = BASE / "base_checkpoints" / B0_TAG
    dst_dir = BASE / "b0" / "frozen" / B0_TAG
    dst_dir.mkdir(parents=True, exist_ok=True)
    copied = {}
    for name in (f"meta_{B0_STEP:06d}.json", f"model_{B0_STEP:06d}.pt"):
        src = src_dir / name
        dst = dst_dir / name
        if not src.is_file():
            raise SystemExit(f"missing {src}")
        if not args.skip_copy:
            if dst.exists() and sha256_file(dst) != sha256_file(src):
                raise SystemExit(f"frozen dst hash mismatch: {dst}")
            if not dst.exists():
                shutil.copy2(src, dst)
        actual = sha256_file(dst)
        if name.endswith(".pt") and actual != B0_SHA256:
            raise SystemExit(f"B0 SHA mismatch: {actual} != {B0_SHA256}")
        copied[name] = {"path": str(dst.relative_to(ROOT)), "sha256": actual, "bytes": dst.stat().st_size}

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "Q",
        "arm": "B0",
        "status": "pass",
        "immutable": True,
        "additional_train_tokens": 0,
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": platform.node(),
        "p3_run_id": P3_RUN_ID,
        "model_tag": B0_TAG,
        "depth": 20,
        "checkpoint_step": B0_STEP,
        "checkpoint_sha256": B0_SHA256,
        "frozen_dir": str(dst_dir.relative_to(ROOT)),
        "copied": copied,
        "tokenizer_sha256": TOKENIZER_SHA,
        "nanochat_pin": PIN,
        "p0_t_status": "PASS",
        "child_parent_whitelist": [B0_TAG],
        "forbidden_parents": ["p3-tl0-d8", "P1.1", "P2"],
        "fresh_optimizer_required": True,
        "test_access": 0,
        "next_gate": "R",
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "path": str(OUT.relative_to(ROOT)), "b0_sha256": B0_SHA256}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
