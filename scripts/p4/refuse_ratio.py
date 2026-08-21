#!/usr/bin/env python3
"""Refuse confirmatory P4 training with ratio=-1 (filed N=294, not implicit)."""

from __future__ import annotations

import sys


def main() -> int:
    args = sys.argv[1:]
    joined = " ".join(args)
    if "ratio=-1" in joined or "--ratio=-1" in joined:
        print("P4 refuses ratio=-1", file=sys.stderr)
        return 2
    for i, a in enumerate(args):
        if a in ("--ratio", "-ratio") and i + 1 < len(args) and args[i + 1] == "-1":
            print("P4 refuses ratio=-1", file=sys.stderr)
            return 2
    print("ratio guard: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
