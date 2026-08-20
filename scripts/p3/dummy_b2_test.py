#!/usr/bin/env python3
"""B2-only dummy test gate. Rejects B1/B3 and missing U seal. Does not print test BPB."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--lockbox", required=True)
    p.add_argument("--safe-progress", required=True)
    p.add_argument("--arm", required=True)
    args = p.parse_args()
    lockbox = Path(args.lockbox)
    if args.arm != "B2":
        print("test evaluator rejects non-B2 arm", file=sys.stderr)
        return 2
    if not (lockbox / "p3-validation-seal.json").exists():
        print("test evaluator rejects missing U seal", file=sys.stderr)
        return 2
    seal = json.loads((lockbox / "p3-validation-seal.json").read_text())
    if seal.get("test_access", 1) != 0:
        print("test evaluator rejects nonzero pre-test access", file=sys.stderr)
        return 2
    event = {
        "arm": "B2",
        "authorized_touches": 1,
        "component_evaluations": 2,
        "test_bpb_en": 9.999001,
        "test_bpb_tl": 9.999002,
    }
    (lockbox / "gate-v-test.json").write_text(json.dumps(event, indent=2) + "\n")
    Path(args.safe_progress).mkdir(parents=True, exist_ok=True)
    (Path(args.safe_progress) / "gate-v-status.json").write_text(
        json.dumps({"one_authorized_B2_only_test_event_completed": True, "test_access_count": 1}) + "\n"
    )
    print("one authorized B2-only test event completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
