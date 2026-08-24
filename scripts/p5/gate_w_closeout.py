#!/usr/bin/env python3
"""P5 Gate W closeout: SHA256SUMS + archive manifest. No new P5 computation."""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    LOCK_PATH,
    P5_RUN_ID,
    PANEL_SEEDS,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    mark_ledger,
    seed_box,
    seed_card,
    sha256_file,
    write_json,
)

SHARED_GLOBS = [
    "gate-0-filing-lock.json",
    "gate-0-lockbox-tests.json",
    "gate-a-source-pin.json",
    "gate-b-raw-assets.json",
    "gate-c-hygiene.json",
    "gate-d-split-freeze.json",
    "gate-e-packed-streams.json",
    "gate-f-tokenizer.json",
    "gate-g-budget-command-freeze.json",
    "gate-h-authorization.json",
    "gate-h-cuda-smoke.json",
    "gate-h-preflight.json",
    "gate-x-preflight.json",
    "gate-x-unblind.json",
    "P5_UNBLINDING_EVENT.json",
]

SEED_GLOBS = [
    "gate-i-tl0.json",
    "gate-i-tl0-d8.json",
    "gate-i-tl0-d20.json",
    "gate-p0-t.json",
    "gate-q-c0-freeze.json",
    "gate-r-c1.json",
    "gate-s-c2.json",
    "gate-t-c3.json",
    "gate-u-seal.json",
    "gate-v-test.json",
]

PAPER_DIR = ROOT / "docs" / "papers" / "p5-multi-seed-p4"
PAPER_OUTPUTS = PAPER_DIR / "paper_outputs"
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
    for name in SHARED_GLOBS:
        add(entries, name.replace(".json", ""), RUN_CARD / name)
    for seed in PANEL_SEEDS:
        for name in SEED_GLOBS:
            add(entries, f"seed{seed}_{name.replace('.json', '')}", seed_card(seed) / name)
        add(entries, f"seed{seed}_validation_seal", seed_box(seed) / f"p5-s{seed}-validation-seal.json")
    add(entries, "lock", LOCK_PATH)
    add(entries, "gate_ledger", ROOT / "manifests" / "p5" / "p5_gate_ledger.json")
    add(entries, "mix_identity", ROOT / "manifests" / "p5" / "p5_mix_identity.json")
    add(entries, "budget_manifest", ROOT / "manifests" / "p5" / "p5_budget_manifest.json")
    add(entries, "aspredicted_pdf", ROOT / "docs" / "run-cards" / "p5" / "AsPredicted-307836.pdf")
    add(entries, "paper_tex", PAPER_DIR / "paper.tex")
    for ext in ("pdf", "md", "txt", "html", "docx", "tex"):
        add(entries, f"paper_{ext}", PAPER_OUTPUTS / f"paper.{ext}")
    if RELEASED.is_dir():
        for path in sorted(RELEASED.glob("*.json")):
            add(entries, f"released_{path.name}", path)

    sums_path = RUN_CARD / "SHA256SUMS"
    lines = [f"{e['sha256']}  {e['path']}" for e in entries]
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    add(entries, "sha256sums", sums_path)

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "W",
        "status": "pass",
        "at_utc": utc_now(),
        "host": platform.node(),
        "p5_run_id": P5_RUN_ID,
        "artifacts": entries,
        "sha256sums": str(sums_path.relative_to(ROOT)),
        "excludes": ["raw_test_text", "secrets", "ssh_keys", "optimizer_states", "HOST_cards"],
        "no_new_computation": True,
        "hub": {
            "provisional_id": "pageman/nanochat-filipino-p5-p4-multi-seed",
            "status": "deferred",
            "reason": "Per eligible seed, C0+C1+C2+C3 must ship together with tokenizer and meta; Hub upload deferred pending operator HF staging. Never C3 alone. Never write onto P4 Hub ID.",
        },
        "researchbox": {
            "id": RESEARCHBOX_ID,
            "status": "pending_new_box",
            "make_public": False,
            "operator_step": "Deposit protocol, PDF, non-sensitive receipts, released seals, paper. No test.jsonl. No passcode in git.",
        },
        "paper": {
            "status": "deferred",
            "reason": "paper.tex not yet filled from released seals; build after Gate W archive.",
        },
        "c3_is_not_p3_b3": True,
        "does_not_confirm_p4": True,
        "p4_seed0_not_a_p5_cell": True,
    }
    out = RUN_CARD / "p5_closeout_manifest.json"
    write_json(out, payload)

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["status"] = "gate_w_pass"
    lock["gate_statuses"]["W"] = "pass"
    lock["gate_w_at_utc"] = payload["at_utc"]
    lock["gate_w_closeout"] = str(out.relative_to(ROOT))
    lock["hub_status"] = "deferred"
    lock["note"] = (
        "P5 confirmatory panel closed. Gate X unblinded; Gate W archived. "
        "Hub weights deferred. ResearchBox new box pending. "
        "C3 is not P3 B3. Does not confirm P4 as law. P4 seed 0 is historical, not a P5 cell."
    )
    write_json(LOCK_PATH, lock)
    mark_ledger("W", "pass", str(out.relative_to(ROOT)), None)

    print(json.dumps({"status": "pass", "path": str(out.relative_to(ROOT)), "n_artifacts": len(entries)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
