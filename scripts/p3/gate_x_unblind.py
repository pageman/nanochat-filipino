#!/usr/bin/env python3
"""P3 Gate X formal unblinding. Run ONLY after gate_x_preflight ready_for_unblinding=true.

Releases the sealed lockbox inventory once into released/. Does not compute new metrics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from p3_common import ASPREDICTED_ID, BASE, P3_RUN_ID, RESEARCHBOX_ID, ROOT, RUN_CARD

REQUIRED = [
    "p3-validation-seal.json",
    "gate-v-test.json",
    "gate-p0-t-eligibility.json",
    "b1_en_val_bpb_full.json",
    "b1_tl_val_bpb_full.json",
    "b2_en_val_bpb_full.json",
    "b2_tl_val_bpb_full.json",
    "b3_en_val_bpb_full.json",
    "b3_tl_val_bpb_full.json",
    "b0_en_val_bpb_full.json",
]

PREFLIGHT = RUN_CARD / "gate-x-preflight.json"
LOCK_PATH = ROOT / "docs" / "papers" / "p3-reverse" / "LOCK.json"
EVENT_PATH = RUN_CARD / "P3_UNBLINDING_EVENT.json"
HANDOFF_PATH = RUN_CARD / "HANDOFF-gate-x.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_preflight() -> dict:
    if not PREFLIGHT.is_file():
        raise SystemExit("missing gate-x-preflight.json — run gate_x_preflight.py first")
    data = json.loads(PREFLIGHT.read_text(encoding="utf-8"))
    if not data.get("ready_for_unblinding"):
        raise SystemExit("preflight ready_for_unblinding is false — refusing unblind")
    fails = [c["check"] for c in data.get("checks", []) if c.get("status") != "PASS"]
    if fails:
        raise SystemExit(f"preflight has FAIL checks: {fails}")
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lockbox", type=Path, default=BASE / "lockbox")
    ap.add_argument(
        "--released",
        type=Path,
        default=BASE / "released",
        help="Destination for simultaneous sealed release",
    )
    ap.add_argument(
        "--also-run-card-released",
        action="store_true",
        help="Also copy released tree under docs/run-cards/.../released/",
    )
    args = ap.parse_args()

    pre = require_preflight()
    lockbox: Path = args.lockbox
    released: Path = args.released

    missing = [n for n in REQUIRED if not (lockbox / n).is_file()]
    if missing:
        print("release refuses incomplete inventory:", ", ".join(missing), file=sys.stderr)
        return 2

    # Refuse Gate-0 placeholders: seal must match preflight-observed seal_sha256 when present.
    seal_sha = sha256_file(lockbox / "p3-validation-seal.json")
    u_safe = BASE / "safe_progress" / "gate-u-status.json"
    if u_safe.is_file():
        expected = json.loads(u_safe.read_text(encoding="utf-8")).get("seal_sha256")
        if expected and seal_sha != expected:
            print(
                "lockbox p3-validation-seal.json sha256 mismatch vs safe_progress "
                "(placeholders?). Pull authoritative lockbox before unblind.",
                file=sys.stderr,
            )
            return 3

    if released.exists() and any(released.iterdir()):
        print(f"refusing non-empty released dir: {released}", file=sys.stderr)
        return 4

    released.mkdir(parents=True, exist_ok=True)
    artifact_sha: dict[str, str] = {}
    for name in REQUIRED:
        src = lockbox / name
        dst = released / name
        shutil.copy2(src, dst)
        try:
            dst.chmod(0o600)
        except OSError:
            pass
        artifact_sha[name] = sha256_file(dst)

    manifest = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "p3_run_id": P3_RUN_ID,
        "gate": "X",
        "at_utc": utc_now(),
        "artifacts": artifact_sha,
        "raw_test_still_restricted": True,
        "note": "Simultaneous sealed release. No new computation.",
    }
    (released / "released_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    card_released = None
    if args.also_run_card_released:
        card_released = RUN_CARD / "released"
        if card_released.exists() and any(card_released.iterdir()):
            print(f"refusing non-empty run-card released dir: {card_released}", file=sys.stderr)
            return 4
        shutil.copytree(released, card_released)

    at = utc_now()
    checklist = {
        "preflight_ready": True,
        "preflight_path": str(PREFLIGHT.relative_to(ROOT)),
        "preflight_at_utc": pre.get("at_utc"),
        "qrstuvw_pass": True,
        "u_before_v": True,
        "b2_only_test": True,
        "seal_and_inventory_complete": True,
        "raw_test_still_restricted": True,
    }
    event = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "p3_run_id": P3_RUN_ID,
        "event": "P3_UNBLINDING",
        "gate": "X",
        "at_utc": at,
        "releaser": "gate_x_unblind.py",
        "release_condition": "Gate X after Q–W PASS + gate_x_preflight ready_for_unblinding",
        "checklist": checklist,
        "released_dir": str(released.relative_to(ROOT)),
        "run_card_released_dir": str(card_released.relative_to(ROOT)) if card_released else None,
        "artifact_sha256s": artifact_sha,
        "released_manifest_sha256": sha256_file(released / "released_manifest.json"),
        "raw_test_still_restricted": True,
        "no_additional_validation_or_test_eval": True,
    }
    EVENT_PATH.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")

    if LOCK_PATH.is_file():
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["status"] = "gate_x_unblinded"
        lock["gate_x_status"] = "pass"
        lock["gate_x_at_utc"] = at
        lock["gate_x_event"] = str(EVENT_PATH.relative_to(ROOT))
        lock["gate_x_released"] = str(released.relative_to(ROOT))
        lock["no_p3_outcomes"] = False
        lock["note"] = (
            "ResearchBox #8834. Gates A–W pass; Gate X unblinded. "
            "Scalars released under data/cache/.../released/. Raw test text remains restricted."
        )
        LOCK_PATH.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

    handoff = f"""# Gate X handoff — P3 #307342

Status: **PASS** — formal unblinding complete.

- Preflight: `{PREFLIGHT.relative_to(ROOT)}` (`ready_for_unblinding=true`)
- Event: `{EVENT_PATH.relative_to(ROOT)}` at `{at}`
- Released bundle: `{released.relative_to(ROOT)}/`
- Manifest: `{released.relative_to(ROOT)}/released_manifest.json`
- LOCK status: `gate_x_unblinded`
- `raw_test_still_restricted=true` (no raw test text released)
- No additional validation or test eval was run at Gate X

Released files (open these for scalars):
{chr(10).join(f"- `{released.relative_to(ROOT)}/{n}`" for n in REQUIRED)}

Next: paper/table fill from **pre-frozen** scripts only; report observed / not observed / blocked; one-seed; post-P2.
"""
    HANDOFF_PATH.write_text(handoff, encoding="utf-8")

    # Safe operator summary — hashes and paths only, no BPB scalars
    print("Gate X unblinding complete")
    print(f"event: {EVENT_PATH.relative_to(ROOT)}")
    print(f"released: {released.relative_to(ROOT)}")
    print(f"n_artifacts: {len(artifact_sha)}")
    print(f"manifest_sha256: {event['released_manifest_sha256']}")
    print(f"raw_test_still_restricted: true")
    print(f"handoff: {HANDOFF_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
