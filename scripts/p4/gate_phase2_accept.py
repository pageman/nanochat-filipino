#!/usr/bin/env python3
"""Safe receipt for phase-2 train gates R/S/T (no BPB)."""

from __future__ import annotations

import argparse
import json
import math
import platform
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    B,
    BASE,
    LOCK_PATH,
    LOCKBOX,
    N_PHASE2,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    SAFE,
    mark_ledger,
    sha256_file,
    utc_now,
    write_json,
    blinded_print,
)

LOSS_RE = re.compile(r"step\s+(\d+)/\d+ .* \| loss:\s+([0-9.eE+-]+)")
STEP_RE = re.compile(r"step\s+(\d+)/(\d+)")


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
    ap.add_argument("--c0-sha", required=True)
    ap.add_argument("--mix-manifest-sha", default=None)
    args = ap.parse_args()

    gate_l = args.gate.lower()
    out = RUN_CARD / f"gate-{gate_l}-{args.arm}.json"
    lock_log = LOCKBOX / f"gate-{gate_l}-{args.arm}-full.log"
    safe = SAFE / f"gate-{gate_l}-{args.arm}-progress.txt"
    ckpt = BASE / "base_checkpoints" / args.model_tag / f"model_{N_PHASE2:06d}.pt"

    final_step_ok = False
    finite = False
    has_val_bpb = False
    if lock_log.is_file():
        text = lock_log.read_text(encoding="utf-8", errors="replace")
        losses = [(int(m.group(1)), float(m.group(2))) for m in LOSS_RE.finditer(text)]
        finite = all(math.isfinite(v) for _, v in losses) if losses else False
        steps = STEP_RE.findall(text)
        if steps:
            final_step_ok = max(int(s) for s, _ in steps) >= N_PHASE2 - 1
        has_val_bpb = "Validation bpb:" in text or "val_bpb_full" in text

    ckpt_sha = sha256_file(ckpt) if ckpt.is_file() else None
    reload = reload_ok(ckpt) if ckpt.is_file() else False
    health = (
        args.exit_code == 0
        and ckpt_sha is not None
        and reload
        and finite
        and final_step_ok
        and not has_val_bpb
    )

    if ckpt.is_file():
        try:
            ckpt.chmod(0o444)
        except OSError:
            pass
    try:
        if lock_log.is_file():
            lock_log.chmod(0o600)
    except OSError:
        pass

    safe.parent.mkdir(parents=True, exist_ok=True)
    safe.write_text(
        "\n".join(
            [
                f"health={'pass' if health else 'block'}",
                f"gate={args.gate}",
                f"arm={args.arm}",
                f"step={N_PHASE2}",
                f"tokens_seen={N_PHASE2 * B}",
                f"reload_ok={'true' if reload else 'false'}",
                "test_access=0",
                "no_bpb_field=true",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    next_map = {"R": "S", "S": "T", "T": "U"}
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": args.gate,
        "arm": args.arm,
        "status": "pass" if health else "fail",
        "health": "pass" if health else "block",
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": True,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "model_tag": args.model_tag,
        "parent_c0_sha256": args.c0_sha,
        "checkpoint_sha256": ckpt_sha,
        "checkpoint_bytes": ckpt.stat().st_size if ckpt.is_file() else None,
        "D_phase2": N_PHASE2 * B,
        "stream": args.stream,
        "nanochat_data_dir": args.data_dir,
        "step": N_PHASE2,
        "reload_ok": reload,
        "test_access": 0,
        "lockbox_log": str(lock_log.relative_to(ROOT)),
        "safe_progress": str(safe.relative_to(ROOT)),
        "train_exit_code": args.exit_code,
        "no_bpb_in_receipt": True,
        "next_gate": next_map[args.gate] if health else f"{args.gate}-blocked",
    }
    if args.gate == "T":
        payload["mix_manifest_sha256"] = args.mix_manifest_sha
        payload["not_mitigation_during_execution"] = True
        payload["c3_is_not_p3_b3"] = True

    write_json(out, payload)
    if health:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"][args.gate] = "pass"
        lock["status"] = f"gate_{gate_l}_pass"
        write_json(LOCK_PATH, lock)
        mark_ledger(args.gate, "pass", str(out.relative_to(ROOT)), next_map[args.gate])
    blinded_print(
        args.gate,
        payload["status"],
        {
            "arm": args.arm,
            "health": payload["health"],
            "step": N_PHASE2,
            "checkpoint_bytes": payload["checkpoint_bytes"],
            "reload_ok": reload,
        },
    )
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
