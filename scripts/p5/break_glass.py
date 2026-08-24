#!/usr/bin/env python3
"""Break-glass dummy: audit JSON, no BPB on stdout."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lockbox", required=True)
    p.add_argument("--safe-progress", required=True)
    p.add_argument("--reason", default="dummy_gate0")
    args = p.parse_args()
    utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rec = {
        "utc": utc,
        "reason": args.reason,
        "inspected_outcome_values": False,
        "dummy": True,
        "study": "P5",
    }
    path = Path(args.lockbox) / f"P4_BREAK_GLASS_{utc}.json"
    path.write_text(json.dumps(rec, indent=2) + "\n")
    Path(args.safe_progress).mkdir(parents=True, exist_ok=True)
    (Path(args.safe_progress) / "break-glass-status.json").write_text(
        json.dumps({"break_glass_audit_written": True, "inspected_outcome_values": False}) + "\n"
    )
    print("break-glass dummy: audit written; no BPB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
