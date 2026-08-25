#!/usr/bin/env python3
"""Parse lockboxed Gate H smoke log; emit safe receipt without BPB. Quarantine smoke ckpt."""

from __future__ import annotations

import argparse
import json
import math
import platform
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    LOCKBOX,
    LOCK_PATH,
    P6_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    SAFE,
    blinded_print,
    mark_ledger,
    sha256_file,
    utc_now,
    update_lock_gate,
    write_json,
)

LOSS_RE = re.compile(r"step\s+(\d+)/\d+ .* \| loss:\s+([0-9.]+)")
OUT = RUN_CARD / "gate-h-cuda-smoke.json"
LOCK_LOG = LOCKBOX / "gate-h-smoke-full.log"
SAFE_TXT = SAFE / "gate-h-smoke-progress.txt"
CKPT = BASE / "base_checkpoints" / "p6-smoke-tl-d4" / "model_000030.pt"
QUAR = LOCKBOX / "quarantine" / "p6-smoke-tl-d4"


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


def quarantine(src: Path) -> dict:
    QUAR.mkdir(parents=True, exist_ok=True)
    smoke_dir = BASE / "base_checkpoints" / "p6-smoke-tl-d4"
    moved = []
    if smoke_dir.is_dir():
        for path in list(smoke_dir.iterdir()):
            dst = QUAR / path.name
            if dst.exists():
                dst.chmod(0o644)
            shutil.move(str(path), str(dst))
            try:
                dst.chmod(0o444)
            except OSError:
                pass
            moved.append(str(dst.relative_to(ROOT)))
    leftover = list(smoke_dir.glob("*.pt")) if smoke_dir.is_dir() else []
    in_c0 = list((BASE / "p6-s1").glob("**/*.pt")) if (BASE / "p6-s1").is_dir() else []
    model = QUAR / "model_000030.pt"
    return {
        "quarantined": model.is_file(),
        "path": str(model.relative_to(ROOT)) if model.is_file() else None,
        "moved": moved,
        "leftover_in_checkpoints": [str(p.relative_to(ROOT)) for p in leftover],
        "in_seed_paths": [str(p.relative_to(ROOT)) for p in in_c0],
    }


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
        detail["has_validation_bpb_in_log"] = "Validation bpb" in text or "val_bpb" in text
        detail["has_samples_in_log"] = "<|bos|>" in text

    ckpt_src = CKPT if CKPT.is_file() else QUAR / "model_000030.pt"
    reload = reload_ok(ckpt_src) if ckpt_src.is_file() else False
    ckpt_sha = sha256_file(ckpt_src) if ckpt_src.is_file() else None
    quar = quarantine(CKPT) if CKPT.is_file() else {
        "quarantined": (QUAR / "model_000030.pt").is_file(),
        "path": str((QUAR / "model_000030.pt").relative_to(ROOT)) if (QUAR / "model_000030.pt").is_file() else None,
        "leftover_in_checkpoints": [],
        "in_seed_paths": [],
    }

    health = (
        args.exit_code == 0
        and finite
        and below_init
        and reload
        and ckpt_sha is not None
        and quar["quarantined"]
        and quar["leftover_in_checkpoints"] == []
        and quar["in_seed_paths"] == []
        and not detail.get("has_validation_bpb_in_log")
    )

    safe_lines = [
        f"health={'pass' if health else 'block'}",
        f"finite={'true' if finite else 'false'}",
        f"below_init={'true' if below_init else 'false'}",
        f"reload_ok={'true' if reload else 'false'}",
        f"exit_code={args.exit_code}",
        f"quarantined={'true' if quar['quarantined'] else 'false'}",
        "no_confirmatory_training=true",
        "no_bpb_printed=true",
    ]
    SAFE_TXT.parent.mkdir(parents=True, exist_ok=True)
    existing = SAFE_TXT.read_text(encoding="utf-8") if SAFE_TXT.is_file() else ""
    SAFE_TXT.write_text(existing + "\n".join(safe_lines) + "\n", encoding="utf-8")

    lock_detail_path = LOCKBOX / "gate-h-smoke-metrics.json"
    write_json(lock_detail_path, detail)
    try:
        lock_detail_path.chmod(0o600)
        if LOCK_LOG.is_file():
            LOCK_LOG.chmod(0o600)
    except OSError:
        pass

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "H",
        "status": "pass" if health else "fail",
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": True,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "script": "scripts/p6/gate_h_smoke.sh",
        "model_tag": "p6-smoke-tl-d4",
        "smoke_seed": 0,
        "depth": 4,
        "num_iterations": 30,
        "warmup_steps": 3,
        "eval_every": -1,
        "sample_every": -1,
        "nanochat_data_dir": f"data/cache/{P6_RUN_ID}/streams/c1_tl",
        "finite": finite,
        "below_init": below_init,
        "reload_ok": reload,
        "checkpoint_sha256": ckpt_sha,
        "smoke_checkpoint_quarantined": quar["quarantined"],
        "quarantine": quar,
        "health": "pass" if health else "block",
        "no_confirmatory_training": True,
        "tl0_not_started": True,
        "c0_not_started": True,
        "lockbox_log": str(LOCK_LOG.relative_to(ROOT)),
        "lockbox_metrics": str(lock_detail_path.relative_to(ROOT)),
        "safe_progress": str(SAFE_TXT.relative_to(ROOT)),
        "train_exit_code": args.exit_code,
        "next_gate": "I_1" if health else "H-blocked",
    }
    write_json(OUT, payload)
    if health:
        update_lock_gate("H", "pass", {"status": "gate_h_pass", "parent_status": "not_started"})
        mark_ledger("H", "pass", str(OUT.relative_to(ROOT)), "I_1")
    blinded_print(
        "H",
        payload["status"],
        {
            "health": payload["health"],
            "finite": finite,
            "reload_ok": reload,
            "below_init": below_init,
            "quarantined": quar["quarantined"],
            "exit_code": args.exit_code,
            "path": str(OUT.relative_to(ROOT)),
        },
    )
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
