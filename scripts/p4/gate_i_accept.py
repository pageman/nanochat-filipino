#!/usr/bin/env python3
"""Parse lockboxed Gate I TL0 train log; emit safe receipt without BPB."""

from __future__ import annotations

import argparse
import json
import math
import platform
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256  # noqa: E402
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    B,
    BASE,
    LOCKBOX,
    LOCK_PATH,
    N_TL0,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    SAFE,
    WARMUP,
    blinded_print,
    mark_ledger,
    sha256_file,
    utc_now,
    write_json,
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
            keys = list(obj.keys())
            return any(k.startswith("transformer.") for k in keys)
        return False
    except Exception:
        return False


def load_budget() -> tuple[int, int]:
    gate_g = RUN_CARD / "gate-g-budget-command-freeze.json"
    if gate_g.is_file():
        payload = json.loads(gate_g.read_text(encoding="utf-8"))
        parent = payload.get("commands", {}).get("parent", {})
        return int(payload.get("N_TL0", N_TL0)), int(parent.get("warmup_steps", WARMUP))
    return N_TL0, WARMUP


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, choices=(8, 20), required=True)
    ap.add_argument("--exit-code", type=int, default=0)
    args = ap.parse_args()

    n_tl0, warmup = load_budget()
    tag = f"p4-tl0-d{args.depth}"
    out = RUN_CARD / f"gate-i-tl0-d{args.depth}.json"
    lock_log = LOCKBOX / f"gate-i-tl0-d{args.depth}-full.log"
    safe = SAFE / f"gate-i-tl0-d{args.depth}-progress.txt"
    ckpt = BASE / "base_checkpoints" / tag / f"model_{n_tl0:06d}.pt"

    detail = {
        "finite": False,
        "final_step_seen": None,
        "num_iterations_expected": n_tl0,
        "has_validation_bpb_in_log": False,
        "has_samples_in_log": False,
        "lockbox_only": True,
    }
    finite = False
    final_step_ok = False

    if lock_log.is_file():
        text = lock_log.read_text(encoding="utf-8", errors="replace")
        losses = [(int(m.group(1)), float(m.group(2))) for m in LOSS_RE.finditer(text)]
        if losses:
            finite = all(math.isfinite(v) for _, v in losses)
        steps = STEP_RE.findall(text)
        if steps:
            last_step = max(int(s) for s, _ in steps)
            detail["final_step_seen"] = last_step
            final_step_ok = last_step >= n_tl0 - 1
        detail["has_validation_bpb_in_log"] = "Validation bpb:" in text or "val_bpb_full" in text
        detail["has_samples_in_log"] = "<|bos|>" in text
        detail["finite"] = finite

    ckpt_bytes = ckpt.stat().st_size if ckpt.is_file() else None
    ckpt_sha = sha256_file(ckpt) if ckpt.is_file() else None
    reload = reload_ok(ckpt) if ckpt.is_file() else False
    forbidden = bool(ckpt_sha and ckpt_sha in FORBIDDEN_PARENT_SHA256)
    if ckpt_sha:
        try:
            reject_parent_sha256(ckpt_sha)
        except SystemExit:
            forbidden = True

    health = (
        args.exit_code == 0
        and finite
        and final_step_ok
        and reload
        and ckpt_sha is not None
        and ckpt_bytes is not None
        and not forbidden
        and not detail["has_validation_bpb_in_log"]
        and not detail["has_samples_in_log"]
    )

    existing = safe.read_text(encoding="utf-8") if safe.is_file() else ""
    safe_lines = [
        f"health={'pass' if health else 'block'}",
        f"finite={'true' if finite else 'false'}",
        f"final_step_ok={'true' if final_step_ok else 'false'}",
        f"reload_ok={'true' if reload else 'false'}",
        f"exit_code={args.exit_code}",
        f"depth={args.depth}",
        f"step={n_tl0}",
        f"tokens_seen={n_tl0 * B}",
        "test_access=0",
        "english_train_tokens=0",
        "no_bpb_field=true",
    ]
    safe.parent.mkdir(parents=True, exist_ok=True)
    safe.write_text(existing + "\n".join(safe_lines) + "\n", encoding="utf-8")

    lock_detail_path = LOCKBOX / f"gate-i-tl0-d{args.depth}-metrics.json"
    write_json(lock_detail_path, detail)
    try:
        lock_detail_path.chmod(0o600)
        if lock_log.is_file():
            lock_log.chmod(0o600)
    except OSError:
        pass

    if ckpt.is_file():
        try:
            ckpt.chmod(0o444)
        except OSError:
            pass

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "I",
        "arm": f"TL0-d{args.depth}",
        "status": "pass" if health else "fail",
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": True,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "script": "scripts/p4/gate_i_tl0.sh",
        "model_tag": tag,
        "depth": args.depth,
        "num_iterations": n_tl0,
        "warmup_steps": warmup,
        "T": 2048,
        "B": B,
        "tokens_seen": n_tl0 * B,
        "eval_every": -1,
        "core_metric_every": -1,
        "sample_every": -1,
        "save_every": -1,
        "selection_rule": "final_checkpoint",
        "nanochat_data_dir": "data/cache/p4-20260821T060032Z-92d63d4/streams/c1_tl",
        "finite": finite,
        "final_step_ok": final_step_ok,
        "reload_ok": reload,
        "forbidden_parent": forbidden,
        "checkpoint": str(ckpt.relative_to(ROOT)) if ckpt.is_file() else None,
        "checkpoint_sha256": ckpt_sha,
        "checkpoint_bytes": ckpt_bytes,
        "step": n_tl0,
        "test_access": 0,
        "english_train_tokens": 0,
        "health": "pass" if health else "block",
        "lockbox_log": str(lock_log.relative_to(ROOT)),
        "lockbox_metrics": str(lock_detail_path.relative_to(ROOT)),
        "safe_progress": str(safe.relative_to(ROOT)),
        "train_exit_code": args.exit_code,
        "c0_not_frozen": True,
        "next_gate": "P0-T" if health else "I-blocked",
    }
    write_json(out, payload)

    summary_path = RUN_CARD / "gate-i-tl0.json"
    depths = {}
    for d in (8, 20):
        p = RUN_CARD / f"gate-i-tl0-d{d}.json"
        if p.is_file():
            row = json.loads(p.read_text(encoding="utf-8"))
            depths[f"d{d}"] = {
                "status": row.get("status"),
                "health": row.get("health"),
                "checkpoint_sha256": row.get("checkpoint_sha256"),
                "checkpoint_bytes": row.get("checkpoint_bytes"),
                "step": row.get("step"),
                "tokens_seen": row.get("tokens_seen"),
                "reload_ok": row.get("reload_ok"),
                "test_access": 0,
                "receipt": str(p.relative_to(ROOT)),
            }
    all_pass = all(depths.get(k, {}).get("status") == "pass" for k in ("d8", "d20")) and len(depths) == 2
    if all_pass:
        summary_status = "pass"
    elif any(v.get("status") == "pass" for v in depths.values()):
        summary_status = "partial"
    elif depths:
        summary_status = "fail"
    else:
        summary_status = "fail"
    summary = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "I",
        "status": summary_status,
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": True,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "depths": depths,
        "test_access": 0,
        "english_train_tokens": 0,
        "c0_not_frozen": True,
        "next_gate": "P0-T" if all_pass else "I-blocked",
        "note": "Do not rank d8 vs d20. C0 freeze is Gate Q after P0-T PASS.",
    }
    write_json(summary_path, summary)
    if all_pass:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["I"] = "pass"
        lock["status"] = "gate_i_pass"
        lock["parent_status"] = "tl0_complete_c0_not_frozen"
        write_json(LOCK_PATH, lock)
        mark_ledger("I", "pass", str(summary_path.relative_to(ROOT)), "P0-T")

    blinded_print(
        "I",
        payload["status"],
        {
            "depth": args.depth,
            "health": payload["health"],
            "finite": finite,
            "final_step_ok": final_step_ok,
            "reload_ok": reload,
            "step": n_tl0,
            "checkpoint_bytes": ckpt_bytes,
            "path": str(out.relative_to(ROOT)),
            "gate_i_overall": summary_status,
        },
    )
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
