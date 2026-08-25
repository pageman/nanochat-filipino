#!/usr/bin/env python3
"""Write Gate H authorization JSON (d4 smoke only; no BPB; A40 CUDA)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import ASPREDICTED_ID, P6_RUN_ID, ROOT, RUN_CARD, utc_now, write_json  # noqa: E402

OUT = RUN_CARD / "gate-h-authorization.json"


def main() -> int:
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "p6_run_id": P6_RUN_ID,
        "gate": "H",
        "authorized": True,
        "authorizes_gate_i": False,
        "authorizes_parent": False,
        "authorizes_children": False,
        "scope": "d4 Tagalog-path CUDA smoke only; tag p6-smoke-tl-d4; seed 0; 30 steps; warmup 3; eval/sample/core-metric off",
        "must_not": [
            "p6-s1-*",
            "p6-s2-*",
            "p6-s3-*",
            "p6-tl0-*",
            "p6-c0-*",
            "p6-c1-*",
            "p6-c2-*",
            "p6-c3-*",
            "print BPB",
            "Mac MPS",
            "CPU confirmatory",
        ],
        "host_class": "NVIDIA CUDA A40",
        "authorized_at_utc": utc_now(),
        "authorized_by": "operator chat: Gate 0 closeout + H authorization",
        "note": "Does not authorize Gate I_1.",
    }
    write_json(OUT, payload)
    print(json.dumps({"status": "authorized", "path": str(OUT.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
