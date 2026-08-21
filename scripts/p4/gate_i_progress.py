#!/usr/bin/env python3
"""Blinded Gate I progress. Step counts only. No loss, no BPB, no d8/d20 ranking."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import BASE, LOCKBOX, N_TL0, RUN_CARD, SAFE, utc_now  # noqa: E402

STEP_RE = re.compile(r"step\s+(\d+)/(\d+)")


def last_step(log: Path) -> int | None:
    if not log.is_file():
        return None
    last = None
    with log.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            m = STEP_RE.search(line)
            if m:
                last = int(m.group(1))
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
    rows = []
    for depth in (8, 20):
        receipt = RUN_CARD / f"gate-i-tl0-d{depth}.json"
        status = None
        if receipt.is_file():
            status = json.loads(receipt.read_text(encoding="utf-8")).get("status")
        log = LOCKBOX / f"gate-i-tl0-d{depth}-full.log"
        step = last_step(log)
        rows.append(
            {
                "depth": depth,
                "tag": f"p4-tl0-d{depth}",
                "last_step": step,
                "n_tl0": N_TL0,
                "receipt_status": status,
                "log_exists": log.is_file(),
            }
        )
    print(
        json.dumps(
            {
                "gate": "I",
                "blinded": True,
                "unblinded": False,
                "no_bpb_printed": True,
                "no_loss_printed": True,
                "no_ranking": True,
                "at_utc": utc_now(),
                "gpu_util_mem": gpu_util(),
                "arms": rows,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
