#!/usr/bin/env python3
"""Run official scripts.base_train after replacing nanochat's hardcoded seed 42.

Does not modify vendor code. Extra seeds use new --model-tag values.
"""

from __future__ import annotations

import os
import runpy
import sys


def main() -> int:
    if "--p1-seed" not in sys.argv:
        raise SystemExit("usage: run_seeded_base_train.py --p1-seed INT -- <base_train args>")
    i = sys.argv.index("--p1-seed")
    seed = int(sys.argv[i + 1])
    rest = sys.argv[i + 2 :]
    if rest[:1] == ["--"]:
        rest = rest[1:]
    os.environ["P1_TORCH_SEED"] = str(seed)
    os.environ.setdefault("PYTHONHASHSEED", str(seed))

    import torch
    import nanochat.common as common

    orig = common.compute_init

    def compute_init(device_type="cuda"):
        out = orig(device_type)
        torch.manual_seed(seed)
        if device_type == "cuda":
            torch.cuda.manual_seed(seed)
        return out

    common.compute_init = compute_init
    sys.argv = ["scripts.base_train", *rest]
    runpy.run_module("scripts.base_train", run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
