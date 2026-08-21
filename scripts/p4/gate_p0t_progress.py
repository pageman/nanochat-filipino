#!/usr/bin/env python3
"""Blinded P0-T progress. Last eval header only. No BPB, no gaps, no ranking."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import LOCKBOX, RUN_CARD, SAFE, utc_now  # noqa: E402

HEADER_RE = re.compile(r"^=== (.+) ===")


def last_header(log: Path) -> str | None:
    if not log.is_file():
        return None
    last = None
    with log.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            m = HEADER_RE.match(line.strip())
            if m:
                last = m.group(1)
    return last


def gpu_util() -> str | None:
    try:
        nmi = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            check=False,
        )
        if nmi.returncode == 0:
            return nmi.stdout.strip().splitlines()[0] if nmi.stdout.strip() else None
    except FileNotFoundError:
        return None
    return None


def main() -> int:
    receipt = RUN_CARD / "gate-p0-t.json"
    safe = SAFE / "gate-p0-t-status.json"
    status = None
    if receipt.is_file():
        status = json.loads(receipt.read_text(encoding="utf-8")).get("p0_t_status")
    elif safe.is_file():
        status = json.loads(safe.read_text(encoding="utf-8")).get("P0-T")
    log = LOCKBOX / "gate-p0-t-eval-full.log"
    print(
        json.dumps(
            {
                "gate": "P0-T",
                "blinded": True,
                "unblinded": False,
                "no_bpb_printed": True,
                "at_utc": utc_now(),
                "gpu_util_mem": gpu_util(),
                "last_eval_header": last_header(log),
                "log_exists": log.is_file(),
                "p0_t_status": status,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
