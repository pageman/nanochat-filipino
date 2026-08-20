#!/usr/bin/env python3
"""Parse lockboxed Gate H smoke log; emit safe receipt without BPB."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from p3_common import ASPREDICTED_ID, BASE, P3_RUN_ID, RESEARCHBOX_ID, ROOT, RUN_CARD

LOSS_RE = re.compile(r"step\s+(\d+)/\d+ .* \| loss:\s+([0-9.]+)")
OUT = RUN_CARD / "gate-h-cuda-smoke.json"
LOCK_LOG = BASE / "lockbox" / "gate-h-smoke-full.log"
SAFE = BASE / "safe_progress" / "gate-h-smoke-progress.txt"
CKPT = BASE / "base_checkpoints" / "p3-smoke-tl-d4" / "model_000030.pt"


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
            keys = list(obj.keys())
            return any(k.startswith("transformer.") for k in keys)
        return False
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exit-code", type=int, default=0)
    args = ap.parse_args()

    detail = {"train_loss_step0": None, "train_loss_last": None, "lockbox_only": True}
    finite = False
    below_init = False
    if LOCK_LOG.is_file():
        text = LOCK_LOG.read_text(encoding="utf-8", errors="replace")
        losses = [(int(m.group(1)), float(m.group(2))) for m in LOSS_RE.finditer(text)]
        if losses:
            step0 = next((v for s, v in losses if s == 0), losses[0][1])
            last = losses[-1][1]
            detail["train_loss_step0"] = step0
            detail["train_loss_last"] = last
            finite = all(math.isfinite(v) for _, v in losses)
            below_init = finite and last < step0
        detail["has_validation_bpb_in_log"] = "Validation bpb" in text
        detail["has_samples_in_log"] = "<|bos|>" in text

    ckpt_sha = sha256_file(CKPT) if CKPT.is_file() else None
    reload = reload_ok(CKPT) if CKPT.is_file() else False
    health = args.exit_code == 0 and finite and below_init and reload and ckpt_sha is not None

    safe_lines = [
        f"health={'pass' if health else 'block'}",
        f"finite={'true' if finite else 'false'}",
        f"below_init={'true' if below_init else 'false'}",
        f"reload_ok={'true' if reload else 'false'}",
        f"exit_code={args.exit_code}",
        "no_confirmatory_training=true",
    ]
    SAFE.parent.mkdir(parents=True, exist_ok=True)
    SAFE.write_text("\n".join(safe_lines) + "\n", encoding="utf-8")

    lock_detail_path = BASE / "lockbox" / "gate-h-smoke-metrics.json"
    lock_detail_path.write_text(json.dumps(detail, indent=2) + "\n", encoding="utf-8")
    try:
        lock_detail_path.chmod(0o600)
    except OSError:
        pass

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "H",
        "status": "pass" if health else "fail",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": platform.node(),
        "p3_run_id": P3_RUN_ID,
        "script": "scripts/p3/gate_h_smoke.sh",
        "model_tag": "p3-smoke-tl-d4",
        "depth": 4,
        "num_iterations": 30,
        "warmup_steps": 3,
        "eval_every": -1,
        "sample_every": -1,
        "nanochat_data_dir": "data/processed/p3-tl39-active",
        "finite": finite,
        "below_init": below_init,
        "reload_ok": reload,
        "checkpoint_sha256": ckpt_sha,
        "health": "pass" if health else "block",
        "no_confirmatory_training": True,
        "tl0_not_started": True,
        "lockbox_log": str(LOCK_LOG.relative_to(ROOT)),
        "lockbox_metrics": str(lock_detail_path.relative_to(ROOT)),
        "safe_progress": str(SAFE.relative_to(ROOT)),
        "train_exit_code": args.exit_code,
        "next_gate": "I" if health else "H-blocked",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "health": payload["health"], "path": str(OUT.relative_to(ROOT))}, indent=2))
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
