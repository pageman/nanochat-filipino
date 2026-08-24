#!/usr/bin/env python3
"""Write per-seed authorizations for I and, after P0-T PASS, Q–V."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import ASPREDICTED_ID, P5_RUN_ID, PANEL_SEEDS, ROOT, seed_card, utc_now, write_json  # noqa: E402


def write_auth(seed: int, gate: str, extra: dict | None = None) -> Path:
    out = seed_card(seed) / {
        "I": "gate-i-authorization.json",
        "P0-T": "gate-p0t-authorization.json",
        "Q": "gate-q-authorization.json",
        "R": "gate-r-authorization.json",
        "S": "gate-s-authorization.json",
        "T": "gate-t-authorization.json",
        "U": "gate-u-authorization.json",
        "V": "gate-v-authorization.json",
    }[gate]
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED",
        "aspredicted_id": ASPREDICTED_ID,
        "p5_run_id": P5_RUN_ID,
        "gate": gate,
        "seed": seed,
        "authorized": True,
        "authorizes_other_seeds": False,
        "host_class": "NVIDIA CUDA A40",
        "authorized_at_utc": utc_now(),
        "authorized_by": "scripts/p5/authorize_seed_gates.py",
    }
    if extra:
        payload.update(extra)
    write_json(out, payload)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--phase", choices=("i", "p0t", "children"), required=True)
    args = ap.parse_args()
    if args.seed not in PANEL_SEEDS:
        raise SystemExit("seed must be 1, 2, or 3")
    written = []
    if args.phase == "i":
        written.append(write_auth(args.seed, "I", {"authorizes_children": False}))
    elif args.phase == "p0t":
        written.append(write_auth(args.seed, "P0-T", {"authorizes_children": False}))
    else:
        i = json.loads((seed_card(args.seed) / "gate-i-tl0.json").read_text())
        p = json.loads((seed_card(args.seed) / "gate-p0-t.json").read_text())
        if i.get("status") != "pass" or p.get("p0_t_status") != "PASS":
            raise SystemExit("children auth requires I pass and P0-T PASS")
        for g in ("Q", "R", "S", "T", "U", "V"):
            written.append(write_auth(args.seed, g))
    print(json.dumps({"seed": args.seed, "phase": args.phase, "paths": [str(p.relative_to(ROOT)) for p in written]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
