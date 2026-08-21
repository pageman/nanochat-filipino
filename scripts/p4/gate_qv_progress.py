#!/usr/bin/env python3
"""Blinded Q→V progress. Steps/status/hashes only. No BPB, no contrasts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import LOCKBOX, RUN_CARD, SAFE, utc_now  # noqa: E402

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
        if nmi.returncode == 0 and nmi.stdout.strip():
            return nmi.stdout.strip().splitlines()[0]
    except FileNotFoundError:
        return None
    return None


def receipt_status(name: str) -> str | None:
    p = RUN_CARD / name
    if not p.is_file():
        return None
    row = json.loads(p.read_text(encoding="utf-8"))
    return row.get("p0_t_status") or row.get("status")


def main() -> int:
    arms = {
        "R": ("gate-r-c1-full.log", "gate-r-c1.json"),
        "S": ("gate-s-c2-full.log", "gate-s-c2.json"),
        "T": ("gate-t-c3-full.log", "gate-t-c3.json"),
    }
    train = {}
    for gate, (log_name, rec_name) in arms.items():
        train[gate] = {
            "last_step": last_step(LOCKBOX / log_name),
            "receipt": receipt_status(rec_name),
        }
    print(
        json.dumps(
            {
                "span": "Q-V",
                "blinded": True,
                "no_bpb_printed": True,
                "at_utc": utc_now(),
                "gpu_util_mem": gpu_util(),
                "Q": receipt_status("gate-q-c0-freeze.json"),
                "R": train["R"],
                "S": train["S"],
                "T": train["T"],
                "U": receipt_status("gate-u-seal.json"),
                "V": receipt_status("gate-v-test.json"),
                "safe_u": (SAFE / "gate-u-status.json").is_file(),
                "safe_v": (SAFE / "gate-v-status.json").is_file(),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
