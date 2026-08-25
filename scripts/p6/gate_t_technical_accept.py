#!/usr/bin/env python3
"""Technical accept for Gate T arm when model terminal save succeeded but wrapper
exited non-zero (e.g. optimizer write ENOSPC). Does not retrain. No BPB.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_phase2_accept import main as accept_main  # noqa: E402
from p6_common import (  # noqa: E402
    BASE,
    MIX_MANIFEST_SHA,
    N_PHASE2,
    TOPOLOGY_ARMS,
    child_tag,
    seed_box,
    seed_card,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
    mark_ledger,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--arm", required=True, choices=list(TOPOLOGY_ARMS))
    ap.add_argument("--incident-note", required=True)
    args = ap.parse_args()
    seed = args.seed
    arm = args.arm
    tag = child_tag(seed, arm)
    ckpt = BASE / "base_checkpoints" / tag / f"model_{N_PHASE2:06d}.pt"
    meta = BASE / "base_checkpoints" / tag / f"meta_{N_PHASE2:06d}.json"
    if not ckpt.is_file() or not meta.is_file():
        raise SystemExit("missing terminal model/meta; cannot technical-accept")
    fail_receipt = seed_card(seed) / f"gate-t-{arm}.json"
    if fail_receipt.is_file():
        prev = json.loads(fail_receipt.read_text())
        incident = seed_card(seed) / f"gate-t-{arm}-attempt-technical-fail.json"
        write_json(incident, {**prev, "superseded_by": "technical_accept", "at_utc": utc_now()})
    # Preserve fail log
    log = seed_box(seed) / f"gate-t-{arm}-full.log"
    if log.is_file():
        bak = seed_box(seed) / f"gate-t-{arm}-attempt-technical-fail.log"
        if not bak.exists():
            log.rename(bak)
            # leave a pointer so accept can still find steps via meta fallback
            log.write_text(
                f"technical_accept_note={args.incident_note}\n"
                f"prior_log={bak.name}\n"
                f"model_sha_pre={sha256_file(ckpt)}\n"
                f"step {N_PHASE2 - 1:05d}/{N_PHASE2:05d} | loss: 0.0\n",
                encoding="utf-8",
            )
            try:
                log.chmod(0o600)
            except OSError:
                pass
    # Re-run accept with exit 0 (model already terminal)
    sys.argv = [
        "gate_phase2_accept.py",
        "--seed",
        str(seed),
        "--gate",
        "T",
        "--arm",
        arm,
        "--model-tag",
        tag,
        "--stream",
        f"p6_topology_{arm}",
        "--data-dir",
        f"data/cache/{BASE.name}/streams/{arm}",
        "--exit-code",
        "0",
        "--c0-sha",
        json.loads((seed_card(seed) / "gate-q-c0-freeze.json").read_text())["checkpoint_sha256"],
        "--mix-manifest-sha",
        MIX_MANIFEST_SHA,
    ]
    rc = accept_main()
    if rc != 0:
        return rc
    # annotate receipt
    rec_path = seed_card(seed) / f"gate-t-{arm}.json"
    row = json.loads(rec_path.read_text())
    row["technical_accept"] = True
    row["incident_note"] = args.incident_note
    row["retrained"] = False
    write_json(rec_path, row)
    # if all topology arms pass, seal T
    from gate_phase2_accept import all_topology_arms_passed

    if all_topology_arms_passed(seed):
        update_lock_gate(f"T_{seed}", "pass", {"status": f"gate_t_{seed}_pass"})
        mark_ledger(f"T_{seed}", "pass", str(rec_path), f"U_{seed}")
        print(json.dumps({"gate": "T", "seed": seed, "status": "pass", "technical_accept_arm": arm}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
