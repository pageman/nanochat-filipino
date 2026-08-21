#!/usr/bin/env python3
"""P4 Gate W closeout: SHA256SUMS + archive manifest. No new P4 computation."""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import (
    ASPREDICTED_ID,
    BASE,
    LOCK_PATH,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    mark_ledger,
    sha256_file,
    write_json,
)

CARD_GLOBS = [
    "gate-0-filing-lock.json",
    "gate-a-source-pin.json",
    "gate-b-raw-assets.json",
    "gate-c-hygiene.json",
    "gate-d-split-freeze.json",
    "gate-e-c1-c2-pack.json",
    "gate-e-packed-streams-and-c3-freeze.json",
    "gate-f-tokenizer.json",
    "gate-g-budget-command-freeze.json",
    "gate-h-cuda-smoke.json",
    "gate-i-tl0.json",
    "gate-p0-t.json",
    "gate-q-c0-freeze.json",
    "gate-r-c1.json",
    "gate-s-c2.json",
    "gate-t-c3.json",
    "gate-u-seal.json",
    "gate-v-test.json",
    "gate-x-preflight.json",
    "gate-x-unblind.json",
    "P4_UNBLINDING_EVENT.json",
]

PAPER_OUTPUTS = ROOT / "docs" / "papers" / "p4-token-share-mix" / "paper_outputs"
RELEASED = BASE / "released"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def add(entries: list, role: str, path: Path) -> None:
    if not path.is_file():
        return
    entries.append(
        {
            "role": role,
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    )


def main() -> int:
    entries: list[dict] = []
    for name in CARD_GLOBS:
        add(entries, name.replace(".json", ""), RUN_CARD / name)
    add(entries, "lock", LOCK_PATH)
    add(entries, "gate_ledger", ROOT / "manifests" / "p4" / "p4_gate_ledger.json")
    add(entries, "mix_manifest", ROOT / "manifests" / "p4" / "p4_mix_manifest.json")
    add(entries, "budget_manifest", ROOT / "manifests" / "p4" / "p4_budget_manifest.json")
    add(entries, "aspredicted_pdf", ROOT / "docs" / "run-cards" / "p4" / "AsPredicted-307591.pdf")
    add(entries, "paper_tex", ROOT / "docs" / "papers" / "p4-token-share-mix" / "paper.tex")
    for ext in ("pdf", "md", "txt", "html", "docx", "tex"):
        add(entries, f"paper_{ext}", PAPER_OUTPUTS / f"paper.{ext}")
    if RELEASED.is_dir():
        for p in sorted(RELEASED.glob("*.json")):
            add(entries, f"released_{p.name}", p)
    add(entries, "tables", ROOT / "results" / "p4" / "tables.json")

    sums_path = RUN_CARD / "SHA256SUMS"
    lines = [f"{e['sha256']}  {e['path']}" for e in entries]
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "W",
        "status": "pass",
        "at_utc": utc_now(),
        "host": platform.node(),
        "p4_run_id": P4_RUN_ID,
        "artifacts": entries,
        "sha256sums": str(sums_path.relative_to(ROOT)),
        "excludes": ["raw_test_text", "secrets", "ssh_keys", "optimizer_states", "HOST_cards"],
        "no_new_computation": True,
        "hub": {
            "provisional_id": "pageman/nanochat-filipino-p4-token-share-mix",
            "status": "deferred",
            "reason": "C0+C1+C2+C3 must ship together with tokenizer and meta; Hub upload deferred 2026-08-21 pending operator HF staging. Never C3 alone. Never write onto P1/P2/P3 Hub IDs.",
        },
        "researchbox": {
            "id": RESEARCHBOX_ID,
            "status": "for_peer_review_passcode_protected",
            "make_public": False,
            "operator_step": "Deposit protocol, PDF, non-sensitive receipts, released seals, paper. No test.jsonl. No passcode in git.",
        },
        "c3_is_not_p3_b3": True,
        "does_not_amend_307342": True,
    }
    out = RUN_CARD / "p4_closeout_manifest.json"
    write_json(out, payload)

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["status"] = "gate_w_pass"
    lock["gate_statuses"]["W"] = "pass"
    lock["gate_w_at_utc"] = payload["at_utc"]
    lock["gate_w_closeout"] = str(out.relative_to(ROOT))
    lock["hub_status"] = "deferred"
    lock["note"] = (
        "P4 confirmatory process closed. Gate X unblinded; Gate W archived. "
        "Hub weights deferred. ResearchBox #8869 remains passcode-protected (not Make Public). "
        "C3 is not P3 B3. Does not amend #307342. Byte-balanced mix is P6-B; multi-seed is P5."
    )
    write_json(LOCK_PATH, lock)
    mark_ledger("W", "pass", str(out.relative_to(ROOT)), None)

    print(json.dumps({"status": "pass", "path": str(out.relative_to(ROOT)), "n_artifacts": len(entries)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
