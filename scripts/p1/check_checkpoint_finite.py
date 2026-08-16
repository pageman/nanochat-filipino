#!/usr/bin/env python3
"""Fresh-process checkpoint reload: report only whether a dummy forward is finite.

Does not read val or test. Does not print a BPB number.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

import torch  # noqa: E402
from nanochat.checkpoint_manager import load_model  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-tag", required=True)
    parser.add_argument("--step", type=int, required=True)
    parser.add_argument("--device-type", default="mps")
    parser.add_argument("--seq-len", type=int, default=2048)
    args = parser.parse_args()

    os.environ.setdefault("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / "p1-20260816T025911Z-0067a57"))
    device = torch.device(args.device_type)
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=args.model_tag, step=args.step)
    seq_len = min(args.seq_len, meta["model_config"]["sequence_len"])
    vocab = tokenizer.get_vocab_size()
    idx = torch.randint(0, vocab, (1, seq_len), device=device)
    targets = torch.randint(0, vocab, (1, seq_len), device=device)
    with torch.no_grad():
        loss = model(idx, targets)
    value = float(loss.detach().cpu())
    finite = math.isfinite(value)
    json.dump(
        {
            "ok": finite,
            "finite": finite,
            "model_tag": args.model_tag,
            "step": args.step,
            "device_type": args.device_type,
            "seq_len": seq_len,
            "numeric_value_redacted": True,
            "split_read": "none_dummy_tokens_only",
        },
        sys.stdout,
        indent=2,
    )
    sys.stdout.write("\n")
    return 0 if finite else 1


if __name__ == "__main__":
    raise SystemExit(main())
