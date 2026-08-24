#!/usr/bin/env python3
"""P5 parent launch wrapper: seed Torch immediately before GPT.init_weights()."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import random
import runpy
import sys
from pathlib import Path

import torch

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    PANEL_SEEDS,
    WRAPPER_RNG_SEED,
    seed_box,
    sha256_file,
    utc_now,
    write_json,
)

WRAPPER_SHA = sha256_file(Path(__file__))


def parse_wrapper(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    p = argparse.ArgumentParser()
    p.add_argument("--parent-init-seed", type=int, required=True)
    p.add_argument("--wrapper-depth", type=int, choices=(8, 20), required=True)
    p.add_argument("--record-initial-state", default=None)
    return p.parse_known_args(argv)


def main() -> None:
    wrapper, rest = parse_wrapper(sys.argv[1:])
    if rest[:1] == ["--"]:
        rest = rest[1:]
    seed = wrapper.parent_init_seed
    if seed not in PANEL_SEEDS:
        raise SystemExit(f"parent-init-seed must be in {PANEL_SEEDS}")

    random.seed(WRAPPER_RNG_SEED)
    if np is not None:
        np.random.seed(WRAPPER_RNG_SEED)
    os.environ["PYTHONHASHSEED"] = str(WRAPPER_RNG_SEED)

    sys.path.insert(0, str(VENDOR))
    from nanochat.gpt import GPT  # noqa: WPS433

    orig = GPT.init_weights
    recorded: dict = {}

    def seeded_init(self):
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
        orig(self)
        buf = io.BytesIO()
        torch.save(self.state_dict(), buf)
        recorded["initial_state_sha256"] = hashlib.sha256(buf.getvalue()).hexdigest()
        recorded["at_utc"] = utc_now()
        print(
            f"P5 parent_train: seed={seed} depth={wrapper.wrapper_depth} "
            f"initial_state_sha256={recorded['initial_state_sha256']} wrapper={WRAPPER_SHA}",
            flush=True,
        )

    GPT.init_weights = seeded_init
    os.chdir(VENDOR)
    sys.argv = ["scripts/base_train.py", *rest]
    runpy.run_path(str(VENDOR / "scripts" / "base_train.py"), run_name="__main__")

    dest = Path(wrapper.record_initial_state) if wrapper.record_initial_state else seed_box(seed) / f"initial_state_d{wrapper.depth}.json"
    write_json(
        dest,
        {
            "seed": seed,
            "depth": wrapper.wrapper_depth,
            "wrapper_sha256": WRAPPER_SHA,
            "wrapper_numpy_rng_seed": WRAPPER_RNG_SEED,
            "initial_state_sha256": recorded.get("initial_state_sha256"),
            "at_utc": recorded.get("at_utc"),
            "no_training_in_this_record": False,
        },
    )


if __name__ == "__main__":
    main()
