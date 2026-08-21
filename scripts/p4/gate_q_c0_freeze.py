#!/usr/bin/env python3
"""P4 Gate Q: freeze TL0 d20 as immutable C0. No extra train tokens."""

from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forbidden_parents import reject_parent_sha256  # noqa: E402
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    LOCK_PATH,
    N_TL0,
    P4_RUN_ID,
    PIN,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TOKENIZER_PKL_SHA,
    blinded_print,
    mark_ledger,
    sha256_file,
    utc_now,
    write_json,
)
from phase2_common import C0_SOURCE_TAG, C0_TAG, C1_TAG, C2_TAG, C3_TAG, PROTOCOL_ALIAS_C1  # noqa: E402

OUT = RUN_CARD / "gate-q-c0-freeze.json"
AUTH = RUN_CARD / "gate-q-authorization.json"


def main() -> int:
    auth = json.loads(AUTH.read_text(encoding="utf-8")) if AUTH.is_file() else {}
    if auth.get("gate") != "Q" or auth.get("authorized") is not True:
        raise SystemExit("missing Gate Q authorization")

    gate_i = json.loads((RUN_CARD / "gate-i-tl0-d20.json").read_text(encoding="utf-8"))
    gate_p0t = json.loads((RUN_CARD / "gate-p0-t.json").read_text(encoding="utf-8"))
    if gate_i.get("status") != "pass" or gate_p0t.get("p0_t_status") != "PASS":
        raise SystemExit("Gate I d20 or P0-T not PASS")

    expected = gate_i["checkpoint_sha256"]
    reject_parent_sha256(expected)

    src_dir = BASE / "base_checkpoints" / C0_SOURCE_TAG
    dst_dir = BASE / "c0" / "frozen" / C0_TAG
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
        copied[name] = {
            "path": str(dst.relative_to(ROOT)),
            "sha256": actual,
            "bytes": dst.stat().st_size,
        }

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "Q",
        "arm": "C0",
        "status": "pass",
        "immutable": True,
        "additional_train_tokens": 0,
        "at_utc": utc_now(),
        "host": platform.node(),
        "gpu": False,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "model_tag": C0_TAG,
        "source_tag": C0_SOURCE_TAG,
        "depth": 20,
        "checkpoint_step": N_TL0,
        "checkpoint_sha256": expected,
        "frozen_dir": str(dst_dir.relative_to(ROOT)),
        "copied": copied,
        "tokenizer_sha256": TOKENIZER_PKL_SHA,
        "nanochat_pin": PIN,
        "p0_t_status": "PASS",
        "child_parent_whitelist": [C0_TAG],
        "allowed_child_tags": [C1_TAG, C2_TAG, C3_TAG],
        "protocol_alias_c1": PROTOCOL_ALIAS_C1,
        "forbidden_parents": ["p4-tl0-d8", "P1.1", "P2", "P3", "C1", "C2", "C3"],
        "fresh_optimizer_required": True,
        "load_optimizer": False,
        "test_access": 0,
        "next_gate": "R",
    }
    write_json(OUT, payload)
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["gate_statuses"]["Q"] = "pass"
    lock["status"] = "gate_q_pass"
    lock["parent_status"] = "c0_frozen"
    write_json(LOCK_PATH, lock)
    mark_ledger("Q", "pass", str(OUT.relative_to(ROOT)), "R")
    blinded_print("Q", "pass", {"checkpoint_sha256": expected, "immutable": True, "additional_train_tokens": 0})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
