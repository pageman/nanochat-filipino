#!/usr/bin/env python3
"""Refuse python -m nanochat.dataset (P4 uses frozen JSONL copies, not the stock downloader)."""

from __future__ import annotations

import sys


def main() -> int:
    print("P4 refuses python -m nanochat.dataset", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
