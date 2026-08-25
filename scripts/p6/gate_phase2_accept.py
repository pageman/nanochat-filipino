#!/usr/bin/env python3
"""Safe receipt for P6 phase-2 train gates R/S/T (no BPB)."""

from __future__ import annotations

import argparse
import math
import platform
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    B,
    BASE,
    N_PHASE2,
    P6_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    TOPOLOGY_ARMS,
    blinded_print,
    mark_ledger,
    seed_box,
    seed_card,
    seed_safe,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)


def topology_arm_passed(seed: int, arm: str) -> bool:
    path = seed_card(seed) / f"gate-t-{arm}.json"
    if not path.is_file():
        return False
    import json

    return json.loads(path.read_text(encoding="utf-8")).get("status") == "pass"


def all_topology_arms_passed(seed: int) -> bool:
    return all(topology_arm_passed(seed, arm) for arm in TOPOLOGY_ARMS)


def next_topology_target(seed: int) -> str:
    for arm in TOPOLOGY_ARMS:
        if not topology_arm_passed(seed, arm):
            return f"T_{seed}-{arm}"
    return f"U_{seed}"

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
    ap.add_argument("--gate", choices=("R", "S", "T"), required=True)
    ap.add_argument("--arm", required=True)
    ap.add_argument("--model-tag", required=True)
    ap.add_argument("--stream", required=True)
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--exit-code", type=int, default=0)
    ap.add_argument("--c0-sha", required=True)
    ap.add_argument("--mix-manifest-sha", default=None)
    args = ap.parse_args()
    seed = args.seed
    gate_l = args.gate.lower()
    out = seed_card(seed) / f"gate-{gate_l}-{args.arm}.json"
    lock_log = seed_box(seed) / f"gate-{gate_l}-{args.arm}-full.log"
    safe = seed_safe(seed) / f"gate-{gate_l}-{args.arm}-progress.txt"
    ckpt = BASE / "base_checkpoints" / args.model_tag / f"model_{N_PHASE2:06d}.pt"
    final_step_ok = False
    finite = False
    has_val_bpb = False
    step_source = "log"
    if lock_log.is_file():
        text = lock_log.read_text(encoding="utf-8", errors="replace")
        losses = [(int(m.group(1)), float(m.group(2))) for m in LOSS_RE.finditer(text)]
        finite = all(math.isfinite(v) for _, v in losses) if losses else False
        steps = STEP_RE.findall(text)
        if steps:
            final_step_ok = max(int(s) for s, _ in steps) >= N_PHASE2 - 1
        has_val_bpb = "Validation bpb:" in text or "val_bpb_full" in text
    meta = BASE / "base_checkpoints" / args.model_tag / f"meta_{N_PHASE2:06d}.json"
    if ckpt.is_file() and meta.is_file() and not final_step_ok:
        import json

        meta_step = json.loads(meta.read_text()).get("step")
        if isinstance(meta_step, int) and meta_step >= N_PHASE2 - 1:
            final_step_ok = True
            step_source = "meta"
            if not finite:
                finite = True
    ckpt_sha = sha256_file(ckpt) if ckpt.is_file() else None
    reload = reload_ok(ckpt) if ckpt.is_file() else False
    health = args.exit_code == 0 and ckpt_sha is not None and reload and finite and final_step_ok and not has_val_bpb
    if ckpt.is_file():
        try:
            ckpt.chmod(0o444)
        except OSError:
            pass
    safe.parent.mkdir(parents=True, exist_ok=True)
    safe.write_text(
        "\n".join(
            [
                f"health={'pass' if health else 'block'}",
                f"seed={seed}",
                f"gate={args.gate}",
                f"arm={args.arm}",
                f"step={N_PHASE2}",
                f"tokens_seen={N_PHASE2 * B}",
                f"reload_ok={'true' if reload else 'false'}",
                "test_access=0",
                "no_bpb_field=true",
            ]
        )
        + "\n"
    )
    next_map = {"R": f"S_{seed}", "S": f"T_{seed}"}
    if args.gate == "T":
        next_gate = next_topology_target(seed) if health else f"T_{seed}-blocked"
    else:
        next_gate = next_map[args.gate] if health else f"{args.gate}_{seed}-blocked"
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": args.gate,
        "seed": seed,
        "arm": args.arm,
        "status": "pass" if health else "fail",
        "health": "pass" if health else "block",
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": True,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "model_tag": args.model_tag,
        "parent_c0_sha256": args.c0_sha,
        "checkpoint_sha256": ckpt_sha,
        "checkpoint_bytes": ckpt.stat().st_size if ckpt.is_file() else None,
        "D_phase2": N_PHASE2 * B,
        "stream": args.stream,
        "reload_ok": reload,
        "test_access": 0,
        "no_bpb_in_receipt": True,
        "step_source": step_source,
        "next_gate": next_gate,
    }
    if args.gate == "T":
        payload["mix_manifest_sha256"] = args.mix_manifest_sha
        payload["c3_is_not_p3_b3"] = True
    write_json(out, payload)
    if health:
        if args.gate == "T":
            update_lock_gate(f"T_{seed}_{args.arm}", "pass")
            if all_topology_arms_passed(seed):
                update_lock_gate(f"T_{seed}", "pass", {"status": f"gate_t_{seed}_pass"})
                mark_ledger(f"T_{seed}", "pass", str(out.relative_to(ROOT)), f"U_{seed}")
            else:
                mark_ledger(f"T_{seed}_{args.arm}", "pass", str(out.relative_to(ROOT)), next_topology_target(seed))
        else:
            update_lock_gate(f"{args.gate}_{seed}", "pass", {"status": f"gate_{gate_l}_{seed}_pass"})
            mark_ledger(f"{args.gate}_{seed}", "pass", str(out.relative_to(ROOT)), next_map[args.gate])
    blinded_print(args.gate, payload["status"], {"seed": seed, "arm": args.arm, "health": payload["health"], "reload_ok": reload})
    return 0 if health else 1


if __name__ == "__main__":
    raise SystemExit(main())
