#!/usr/bin/env python3
"""Safe receipt for phase-2 train gates R/S/T (no BPB)."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
from datetime import datetime, timezone
from pathlib import Path

from p3_common import ASPREDICTED_ID, BASE, B, P3_RUN_ID, RESEARCHBOX_ID, ROOT, RUN_CARD
from phase2_common import B0_SHA256, N_PHASE2

LOSS_RE = re.compile(r"step\s+(\d+)/\d+ .* \| loss:\s+([0-9.eE+-]+)")
STEP_RE = re.compile(r"step\s+(\d+)/(\d+)")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def reload_ok(path: Path) -> bool:
    try:
        import torch

        obj = torch.load(path, map_location="cpu", weights_only=False)
        if isinstance(obj, dict) and "model" in obj:
            return True
        if hasattr(obj, "keys"):
            return any(k.startswith("transformer.") for k in obj.keys())
        return False
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", choices=("R", "S", "T"), required=True)
    ap.add_argument("--arm", required=True)
    ap.add_argument("--model-tag", required=True)
    ap.add_argument("--stream", required=True)
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--exit-code", type=int, default=0)
    ap.add_argument("--b0-sha", default=B0_SHA256)
    args = ap.parse_args()

    gate_l = args.gate.lower()
    out = RUN_CARD / f"gate-{gate_l}-{args.arm}.json"
    lock_log = BASE / "lockbox" / f"gate-{gate_l}-{args.arm}-full.log"
    safe = BASE / "safe_progress" / f"gate-{gate_l}-{args.arm}-progress.txt"
    ckpt = BASE / "base_checkpoints" / args.model_tag / f"model_{N_PHASE2:06d}.pt"

    final_step_ok = False
    finite = False
    if lock_log.is_file():
        text = lock_log.read_text(encoding="utf-8", errors="replace")
        import math

        losses = [(int(m.group(1)), float(m.group(2))) for m in LOSS_RE.finditer(text)]
        finite = all(math.isfinite(v) for _, v in losses) if losses else False
        steps = STEP_RE.findall(text)
        if steps:
            final_step_ok = max(int(s) for s, _ in steps) >= N_PHASE2 - 1

    ckpt_sha = sha256_file(ckpt) if ckpt.is_file() else None
    health = (
        args.exit_code == 0
        and ckpt_sha is not None
        and reload_ok(ckpt)
        and finite
        and final_step_ok
    )

    safe_lines = [
        f"health={'pass' if health else 'block'}",
        f"gate={args.gate}",
        f"arm={args.arm}",
        f"step={N_PHASE2}",
        f"tokens_seen={N_PHASE2 * B}",
        f"reload_ok={'true' if (ckpt.is_file() and reload_ok(ckpt)) else 'false'}",
        "test_access=0",
        "no_bpb_field=true",
    ]
    safe.parent.mkdir(parents=True, exist_ok=True)
    safe.write_text("\n".join(safe_lines) + "\n", encoding="utf-8")

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": args.gate,
        "arm": args.arm,
        "status": "pass" if health else "fail",
        "health": "pass" if health else "block",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": platform.node(),
        "p3_run_id": P3_RUN_ID,
        "model_tag": args.model_tag,
        "parent_b0_sha256": args.b0_sha,
        "checkpoint_sha256": ckpt_sha,
        "checkpoint_bytes": ckpt.stat().st_size if ckpt.is_file() else None,
        "D_phase2": N_PHASE2 * B,
        "stream": args.stream,
        "nanochat_data_dir": args.data_dir,
        "step": N_PHASE2,
        "reload_ok": reload_ok(ckpt) if ckpt.is_file() else False,
        "test_access": 0,
        "lockbox_log": str(lock_log.relative_to(ROOT)),
        "safe_progress": str(safe.relative_to(ROOT)),
        "train_exit_code": args.exit_code,
        "no_bpb_in_receipt": True,
    }
    if args.gate == "R":
        payload["next_gate"] = "S" if health else "R-blocked"
    elif args.gate == "S":
        payload["next_gate"] = "T" if health else "S-blocked"
    else:
        payload["next_gate"] = "U" if health else "T-blocked"

    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "health": payload["health"], "path": str(out.relative_to(ROOT))}, indent=2))
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
