#!/usr/bin/env python3
"""Parse lockboxed Gate I_s TL0 train log; emit safe receipt without BPB."""

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
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    B,
    BASE,
    LOCK_PATH,
    N_TL0,
    P6_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    WARMUP,
    blinded_print,
    mark_ledger,
    seed_box,
    seed_card,
    seed_safe,
    sha256_file,
    tl0_tag,
    update_lock_gate,
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
            return any(k.startswith("transformer.") for k in obj.keys())
        return False
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--depth", type=int, choices=(8, 20), required=True)
    ap.add_argument("--exit-code", type=int, default=0)
    args = ap.parse_args()
    seed, depth = args.seed, args.depth
    tag = tl0_tag(seed, depth)
    out = seed_card(seed) / f"gate-i-tl0-d{depth}.json"
    lock_log = seed_box(seed) / f"gate-i-tl0-d{depth}-full.log"
    safe = seed_safe(seed) / f"gate-i-tl0-d{depth}-progress.txt"
    ckpt = BASE / "base_checkpoints" / tag / f"model_{N_TL0:06d}.pt"

    detail = {"finite": False, "final_step_seen": None, "has_validation_bpb_in_log": False, "has_samples_in_log": False}
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
            final_step_ok = last_step >= N_TL0 - 1
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
        and not forbidden
        and not detail["has_validation_bpb_in_log"]
        and not detail["has_samples_in_log"]
    )
    safe.parent.mkdir(parents=True, exist_ok=True)
    safe.write_text(
        "\n".join(
            [
                f"health={'pass' if health else 'block'}",
                f"seed={seed}",
                f"depth={depth}",
                f"finite={'true' if finite else 'false'}",
                f"final_step_ok={'true' if final_step_ok else 'false'}",
                f"reload_ok={'true' if reload else 'false'}",
                f"step={N_TL0}",
                f"tokens_seen={N_TL0 * B}",
                "test_access=0",
                "no_bpb_field=true",
            ]
        )
        + "\n"
    )
    write_json(seed_box(seed) / f"gate-i-tl0-d{depth}-metrics.json", detail)
    if ckpt.is_file():
        try:
            ckpt.chmod(0o444)
        except OSError:
            pass
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "I",
        "seed": seed,
        "arm": f"TL0-d{depth}",
        "status": "pass" if health else "fail",
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": True,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "model_tag": tag,
        "parent_init_seed": seed,
        "depth": depth,
        "num_iterations": N_TL0,
        "warmup_steps": WARMUP,
        "tokens_seen": N_TL0 * B,
        "finite": finite,
        "final_step_ok": final_step_ok,
        "reload_ok": reload,
        "forbidden_parent": forbidden,
        "checkpoint": str(ckpt.relative_to(ROOT)) if ckpt.is_file() else None,
        "checkpoint_sha256": ckpt_sha,
        "checkpoint_bytes": ckpt_bytes,
        "health": "pass" if health else "block",
        "c0_not_frozen": True,
        "no_bpb_in_receipt": True,
        "next_gate": f"P0-T_{seed}" if health else f"I_{seed}-blocked",
    }
    write_json(out, payload)

    depths = {}
    for d in (8, 20):
        p = seed_card(seed) / f"gate-i-tl0-d{d}.json"
        if p.is_file():
            row = json.loads(p.read_text())
            depths[f"d{d}"] = {
                "status": row.get("status"),
                "health": row.get("health"),
                "checkpoint_sha256": row.get("checkpoint_sha256"),
                "checkpoint_bytes": row.get("checkpoint_bytes"),
                "reload_ok": row.get("reload_ok"),
            }
    all_pass = all(depths.get(k, {}).get("status") == "pass" for k in ("d8", "d20")) and len(depths) == 2
    summary = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "gate": "I",
        "seed": seed,
        "status": "pass" if all_pass else ("partial" if any(v.get("status") == "pass" for v in depths.values()) else "fail"),
        "at_utc": utc_now(),
        "depths": depths,
        "blinded": True,
        "c0_not_frozen": True,
        "next_gate": f"P0-T_{seed}" if all_pass else f"I_{seed}-blocked",
    }
    write_json(seed_card(seed) / "gate-i-tl0.json", summary)
    if all_pass:
        update_lock_gate(f"I_{seed}", "pass", {"status": f"gate_i_{seed}_pass", "parent_status": f"s{seed}_tl0_complete_c0_not_frozen"})
        mark_ledger(f"I_{seed}", "pass", str((seed_card(seed) / "gate-i-tl0.json").relative_to(ROOT)), f"P0-T_{seed}")
    blinded_print("I", payload["status"], {"seed": seed, "depth": depth, "health": payload["health"], "reload_ok": reload, "gate_i_overall": summary["status"]})
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
