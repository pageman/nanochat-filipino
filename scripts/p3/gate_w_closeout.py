#!/usr/bin/env python3
"""P3 Gate W: closeout manifest (no new computation)."""

from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

from p3_common import ASPREDICTED_ID, P3_RUN_ID, RESEARCHBOX_ID, ROOT, RUN_CARD

OUT = RUN_CARD / "p3_closeout_manifest.json"
CARD_GLOBS = [
    "gate-q-b0-freeze.json",
    "gate-r-b1.json",
    "gate-s-b2.json",
    "gate-t-b3.json",
    "gate-u-seal.json",
    "gate-v-test.json",
    "gate-p0-t.json",
    "gate-i-tl0.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    entries = []
    for name in CARD_GLOBS:
        p = RUN_CARD / name
        if p.is_file():
            entries.append({
                "role": name.replace(".json", ""),
                "path": str(p.relative_to(ROOT)),
                "bytes": p.stat().st_size,
                "sha256": sha256_file(p),
            })
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "W",
        "status": "pass",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": platform.node(),
        "p3_run_id": P3_RUN_ID,
        "artifacts": entries,
        "excludes": ["raw_test_text", "secrets", "ssh_keys", "optimizer_states"],
        "no_new_computation": True,
        "note": "Gate X unblinding is separate. Scalars remain lockboxed until Gate X.",
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "path": str(OUT.relative_to(ROOT)), "n_artifacts": len(entries)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
