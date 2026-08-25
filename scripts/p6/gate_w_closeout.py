#!/usr/bin/env python3
"""P6-M Gate W closeout: SHA256SUMS + archive manifest. No new BPB."""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    LOCK_PATH,
    P6_RUN_ID,
    PANEL_SEEDS,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TOPOLOGY_ARMS,
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
    "gate-x-authorization.json",
    "gate-x-preflight.json",
    "gate-x-unblind.json",
    "P6_UNBLINDING_EVENT.json",
]

SEED_GLOBS = [
    "gate-i-tl0.json",
    "gate-i-tl0-d8.json",
    "gate-i-tl0-d20.json",
    "gate-p0-t.json",
    "gate-q-c0-freeze.json",
    "gate-r-c1.json",
    "gate-s-c2.json",
    "gate-t-m-fine.json",
    "gate-t-m-coarse.json",
    "gate-t-m-blocked.json",
    "gate-t-m-rand.json",
    "gate-u-seal.json",
    "gate-v-test.json",
]

PAPER_DIR = ROOT / "docs" / "papers" / "p6-m-schedule-topology"
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
        add(entries, f"seed{seed}_validation_seal", seed_box(seed) / f"p6-s{seed}-validation-seal.json")
        add(entries, f"seed{seed}_released_contrasts", RELEASED / f"p6-s{seed}-released-contrasts.json")
    add(entries, "lock", LOCK_PATH)
    add(entries, "gate_ledger", ROOT / "manifests" / "p6" / "p6_gate_ledger.json")
    add(entries, "mix_identity", ROOT / "manifests" / "p6" / "p6_mix_identity.json")
    add(entries, "budget_manifest", ROOT / "manifests" / "p6" / "p6_budget_manifest.json")
    add(entries, "topology_manifest", ROOT / "manifests" / "p6" / "p6_topology_schedule_manifest.json")
    add(entries, "aspredicted_pdf", ROOT / "docs" / "run-cards" / "p6" / "AsPredicted-307969.pdf")
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
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "W",
        "status": "pass",
        "at_utc": utc_now(),
        "host": platform.node(),
        "p6_run_id": P6_RUN_ID,
        "artifacts": entries,
        "sha256sums": str(sums_path.relative_to(ROOT)),
        "excludes": ["raw_test_text", "secrets", "ssh_keys", "optimizer_states", "HOST_cards"],
        "no_new_computation": True,
        "hub": {
            "provisional_id": "pageman/nanochat-filipino-p6-m-schedule-topology",
            "status": "deferred",
            "reason": "W5 requires independent remote re-hash after upload; deferred to operator HF staging. Never write onto P4/P5 Hub IDs.",
        },
        "researchbox": {
            "id": RESEARCHBOX_ID,
            "status": "pending_new_box",
            "make_public": False,
        },
        "github_public_subtree": {"status": "deferred", "reason": "W3 push requires the public-subtree scan plus explicit push."},
        "paper": {"status": "built_from_released_json", "source": "scripts/p6/fill_paper_from_released.py"},
        "does_not_confirm_p4": True,
        "does_not_confirm_p5": True,
        "topology_arms": list(TOPOLOGY_ARMS),
    }
    out = RUN_CARD / "p6_closeout_manifest.json"
    write_json(out, payload)

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    lock["status"] = "gate_w_pass"
    lock["gate_statuses"]["W"] = "pass"
    lock["gate_w_at_utc"] = payload["at_utc"]
    lock["gate_w_closeout"] = str(out.relative_to(ROOT))
    lock["hub_status"] = "deferred"
    lock["note"] = (
        "P6-M closed at Gate W archive/paper. Hub/ResearchBox/public git deferred. "
        "Primary result is topology contrasts vs M-fine, not P5 recurrence counts."
    )
    write_json(LOCK_PATH, lock)
    mark_ledger("W", "pass", str(out.relative_to(ROOT)), None)
    print(json.dumps({"status": "pass", "path": str(out.relative_to(ROOT)), "n_artifacts": len(entries)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
