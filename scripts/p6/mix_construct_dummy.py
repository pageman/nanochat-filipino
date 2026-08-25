#!/usr/bin/env python3
"""Dummy C3 mix constructor for Gate 0 tests.

Does not read real train/val/test JSONL. Refuses val/test inputs, unset
tokenizer hash, and reconstruction from the P3 B3 mix-order SHA.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

P3_B3_MIX_ORDER_SHA = "b6ae432b625b6768f84db3f45c411378d1d5a5fdbd15cbfc0e5f6c511196b1a0"


def _looks_like_holdout(path: str) -> bool:
    name = Path(path).name.lower()
    return any(tok in name for tok in ("val", "valid", "test", "holdout"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tokenizer-sha", default="")
    p.add_argument("--token-bytes-sha", default="")
    p.add_argument("--train-tl", default="")
    p.add_argument("--train-en", default="")
    p.add_argument("--also", action="append", default=[])
    p.add_argument("--from-p3-b3-mix-order-sha", default="")
    p.add_argument("--out", default="")
    args = p.parse_args()

    if args.from_p3_b3_mix_order_sha.lower() == P3_B3_MIX_ORDER_SHA:
        print("mix refuses C3 reconstruction from P3 B3 mix-order SHA", file=sys.stderr)
        return 2
    if not args.tokenizer_sha:
        print("mix refuses to start if tokenizer hash unset", file=sys.stderr)
        return 2
    extras = list(args.also)
    for candidate in extras + [args.train_tl, args.train_en]:
        if candidate and _looks_like_holdout(candidate):
            print("mix-construction dummy refuses val/test documents", file=sys.stderr)
            return 2

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(
                {
                    "dummy": True,
                    "q_tl": 0.50,
                    "clock": "source_content_tokens",
                    "tokenizer_sha": args.tokenizer_sha,
                    "c3_is_not_p3_b3": True,
                    "from_p3_b3_mix_order": False,
                },
                indent=2,
            )
            + "\n"
        )
    print("dummy mix construction accepted (train-only; new identity)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
