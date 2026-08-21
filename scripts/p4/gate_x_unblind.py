#!/usr/bin/env python3
"""P4 Gate X formal unblinding. Run ONLY after gate_x_preflight ready_for_unblinding=true."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    LOCK_PATH,
    LOCKBOX,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    SAFE,
    mark_ledger,
    sha256_file,
    utc_now,
    write_json,
)

REQUIRED = [
    "p4-validation-seal.json",
    "gate-v-test.json",
    "gate-p0-t-eligibility.json",
    "c1_en_val_bpb_full.json",
    "c1_tl_val_bpb_full.json",
    "c2_en_val_bpb_full.json",
    "c2_tl_val_bpb_full.json",
    "c3_en_val_bpb_full.json",
    "c3_tl_val_bpb_full.json",
    "c0_en_val_bpb_full.json",
]
OPTIONAL = ["c0_tl_val_bpb_full.json", "byte_unigram_tagalog_val.json"]

PREFLIGHT = RUN_CARD / "gate-x-preflight.json"
EVENT_PATH = RUN_CARD / "P4_UNBLINDING_EVENT.json"
HANDOFF_PATH = RUN_CARD / "HANDOFF-gate-x.md"


def require_preflight() -> dict:
    if not PREFLIGHT.is_file():
        raise SystemExit("missing gate-x-preflight.json")
    data = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if not data.get("ready_for_unblinding"):
        raise SystemExit("preflight ready_for_unblinding is false")
    fails = [c["check"] for c in data.get("checks", []) if c.get("status") != "PASS"]
    if fails:
        raise SystemExit(f"preflight FAIL: {fails}")
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lockbox", type=Path, default=LOCKBOX)
    ap.add_argument("--released", type=Path, default=BASE / "released")
    ap.add_argument("--also-run-card-released", action="store_true")
    args = ap.parse_args()
    pre = require_preflight()
    lockbox: Path = args.lockbox
    released: Path = args.released

    missing = [n for n in REQUIRED if not (lockbox / n).is_file()]
    if missing:
        print("release refuses incomplete inventory:", ", ".join(missing), file=sys.stderr)
        return 2

    seal_sha = sha256_file(lockbox / "p4-validation-seal.json")
    u_safe = SAFE / "gate-u-status.json"
    if u_safe.is_file():
        expected = json.loads(u_safe.read_text(encoding="utf-8")).get("seal_sha256")
        if expected and seal_sha != expected:
            print("seal sha256 mismatch vs safe_progress", file=sys.stderr)
            return 3

    if released.exists() and any(released.iterdir()):
        print(f"refusing non-empty released dir: {released}", file=sys.stderr)
        return 4

    released.mkdir(parents=True, exist_ok=True)
    artifact_sha: dict[str, str] = {}
    for name in REQUIRED + OPTIONAL:
        src = lockbox / name
        if not src.is_file():
            continue
        dst = released / name
        shutil.copy2(src, dst)
        try:
            dst.chmod(0o644)
        except OSError:
            pass
        artifact_sha[name] = sha256_file(dst)

    at = utc_now()
    manifest = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "p4_run_id": P4_RUN_ID,
        "gate": "X",
        "at_utc": at,
        "artifacts": artifact_sha,
        "raw_test_still_restricted": True,
        "c3_is_not_p3_b3": True,
        "note": "Simultaneous sealed release. No new computation.",
    }
    man_path = released / "released_manifest.json"
    write_json(man_path, manifest)
    man_sha = sha256_file(man_path)

    card_released = None
    if args.also_run_card_released:
        card_released = RUN_CARD / "released"
        if card_released.exists() and any(card_released.iterdir()):
            print(f"refusing non-empty run-card released dir: {card_released}", file=sys.stderr)
            return 4
        shutil.copytree(released, card_released)

    event = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "p4_run_id": P4_RUN_ID,
        "event": "P4_UNBLINDING",
        "gate": "X",
        "at_utc": at,
        "releaser": "gate_x_unblind.py",
        "release_condition": "U seal + V event complete (Policy A)",
        "checklist": {
            "preflight_ready": True,
            "preflight_path": str(PREFLIGHT.relative_to(ROOT)),
            "u_before_v": True,
            "c3_only_test": True,
            "raw_test_still_restricted": True,
        },
        "released_dir": str(released.relative_to(ROOT)),
        "run_card_released_dir": str(card_released.relative_to(ROOT)) if card_released else None,
        "artifact_sha256s": artifact_sha,
        "released_manifest_sha256": man_sha,
        "raw_test_still_restricted": True,
        "no_additional_validation_or_test_eval": True,
    }
    write_json(EVENT_PATH, event)

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["status"] = "gate_x_unblinded"
    lock["gate_statuses"]["X"] = "pass"
    lock["unblinding_status"] = "gate_x_unblinded"
    lock["no_p4_outcomes"] = False
    lock["p4_outcome_access_count"] = int(lock.get("p4_outcome_access_count") or 0) + 1
    lock["validation_scalar_access_count"] = int(lock.get("validation_scalar_access_count") or 0) + 1
    lock["test_access_count"] = 1
    lock["gate_x_at_utc"] = at
    lock["gate_x_event"] = str(EVENT_PATH.relative_to(ROOT))
    lock["gate_x_released"] = str(released.relative_to(ROOT))
    lock["note"] = (
        "ResearchBox #8869. Gate X unblinded. Scalars in data/cache/.../released/. "
        "Raw test text remains restricted. C3 is not P3 B3. Does not amend #307342."
    )
    write_json(LOCK_PATH, lock)
    mark_ledger("X", "pass", str(EVENT_PATH.relative_to(ROOT)), "W")

    receipt = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "X",
        "status": "pass",
        "at_utc": at,
        "p4_run_id": P4_RUN_ID,
        "released_manifest_sha256": man_sha,
        "raw_test_still_restricted": True,
        "next_gate": "W",
    }
    write_json(RUN_CARD / "gate-x-unblind.json", receipt)

    names = "\n".join(f"- `{released.relative_to(ROOT)}/{n}`" for n in artifact_sha)
    HANDOFF_PATH.write_text(
        f"""# Gate X handoff — P4 #307591

Status: **PASS** — formal unblinding complete.

- Preflight: `{PREFLIGHT.relative_to(ROOT)}`
- Event: `{EVENT_PATH.relative_to(ROOT)}` at `{at}`
- Released: `{released.relative_to(ROOT)}/`
- Manifest SHA-256: `{man_sha}`
- `raw_test_still_restricted=true`
- C3 is not P3 B3; P4 does not amend #307342

Released files:
{names}

Next: Gate W (paper from seals; Hub four weights or defer; new RB contents; stop GPU).
""",
        encoding="utf-8",
    )
    print("Gate X unblinding complete")
    print(f"event: {EVENT_PATH.relative_to(ROOT)}")
    print(f"released: {released.relative_to(ROOT)}")
    print(f"n_artifacts: {len(artifact_sha)}")
    print(f"manifest_sha256: {man_sha}")
    print("raw_test_still_restricted: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
