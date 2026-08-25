#!/usr/bin/env python3
"""P6 Gate Q_s: freeze TL0 d20 as immutable C0_s. No extra train tokens."""

from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forbidden_parents import reject_parent_sha256  # noqa: E402
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    CHILD_ARMS,
    N_TL0,
    P6_RUN_ID,
    PIN,
    RESEARCHBOX_ID,
    ROOT,
    TOKENIZER_PKL_SHA,
    blinded_print,
    c0_tag,
    child_tag,
    frozen_c0_dir,
    mark_ledger,
    require_auth,
    seed_card,
    sha256_file,
    tl0_tag,
    update_lock_gate,
    utc_now,
    write_json,
)


def main() -> int:
    seed = int(sys.argv[1])
    require_auth(seed_card(seed) / "gate-q-authorization.json", "Q", {"seed": seed})
    gate_i = json.loads((seed_card(seed) / "gate-i-tl0-d20.json").read_text())
    gate_p0t = json.loads((seed_card(seed) / "gate-p0-t.json").read_text())
    if gate_i.get("status") != "pass" or gate_p0t.get("p0_t_status") != "PASS":
        raise SystemExit("Gate I d20 or P0-T not PASS")
    expected = gate_i["checkpoint_sha256"]
    reject_parent_sha256(expected)
    for arm in CHILD_ARMS:
        tag = child_tag(seed, arm)
        ckpt_dir = BASE / "base_checkpoints" / tag
        pts = list(ckpt_dir.glob("model_*.pt")) if ckpt_dir.is_dir() else []
        if pts:
            raise SystemExit(f"REFUSE: child outputs already present for {tag}: {[p.name for p in pts]}")
    src_dir = BASE / "base_checkpoints" / tl0_tag(seed, 20)
    dst_dir = frozen_c0_dir(seed)
    dst_dir.mkdir(parents=True, exist_ok=True)
    copied = {}
    for name in (f"meta_{N_TL0:06d}.json", f"model_{N_TL0:06d}.pt"):
        src = src_dir / name
        if not src.is_file():
            if name.startswith("meta_"):
                continue
            raise SystemExit(f"missing {src}")
        dst = dst_dir / name
        if dst.exists():
            if sha256_file(dst) != sha256_file(src):
                raise SystemExit(f"frozen dst hash mismatch: {dst}")
        else:
            shutil.copy2(src, dst)
        actual = sha256_file(dst)
        if name.endswith(".pt"):
            if actual != expected:
                raise SystemExit(f"C0 SHA mismatch: {actual} != {expected}")
            try:
                dst.chmod(0o444)
            except OSError:
                pass
        copied[name] = {"path": str(dst.relative_to(ROOT)), "sha256": actual, "bytes": dst.stat().st_size}
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "Q",
        "seed": seed,
        "arm": "C0",
        "status": "pass",
        "immutable": True,
        "additional_train_tokens": 0,
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": False,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "model_tag": c0_tag(seed),
        "source_tag": tl0_tag(seed, 20),
        "checkpoint_sha256": expected,
        "frozen_dir": str(dst_dir.relative_to(ROOT)),
        "copied": copied,
        "tokenizer_sha256": TOKENIZER_PKL_SHA,
        "nanochat_pin": PIN,
        "p0_t_status": "PASS",
        "child_parent_whitelist": [c0_tag(seed)],
        "allowed_child_tags": [child_tag(seed, a) for a in CHILD_ARMS],
        "fresh_optimizer_required": True,
        "load_optimizer": False,
        "test_access": 0,
        "next_gate": f"R_{seed}",
    }
    write_json(seed_card(seed) / "gate-q-c0-freeze.json", payload)
    update_lock_gate(
        f"Q_{seed}",
        "pass",
        {
            "status": f"gate_q_{seed}_pass",
            "c0_tag": c0_tag(seed),
            "c0_checkpoint_sha256": expected,
            "c0_frozen": True,
            "c0_frozen_dir": str(dst_dir.relative_to(ROOT)),
        },
    )
    mark_ledger(f"Q_{seed}", "pass", str((seed_card(seed) / "gate-q-c0-freeze.json").relative_to(ROOT)), f"R_{seed}")
    blinded_print("Q", "pass", {"seed": seed, "checkpoint_sha256": expected, "immutable": True, "additional_train_tokens": 0})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
