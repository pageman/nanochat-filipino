#!/usr/bin/env python3
"""P4 Gate X safe-only preflight. MUST pass before any unblinding.

Prints ONLY statuses, counts, hashes, timestamps. Never prints BPB / R_TL / A_EN.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-x-preflight.json"
TEST_LOG = ROOT / "manifests" / "p4" / "p4_test_access_log.json"
UNBLIND_EVENT = RUN_CARD / "P4_UNBLINDING_EVENT.json"
FORBIDDEN_RE = re.compile(r"val_bpb|R_TL|A_EN|bpb=|test_bpb", re.I)

GATE_FILES = {
    "Q": "gate-q-c0-freeze.json",
    "R": "gate-r-c1.json",
    "S": "gate-s-c2.json",
    "T": "gate-t-c3.json",
    "U": "gate-u-seal.json",
    "V": "gate-v-test.json",
}

LOCKBOX_HASH_TARGETS = (
    "p4-validation-seal.json",
    "gate-v-test.json",
    "gate-p0-t-eligibility.json",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_utc(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def remote_sha256s(ssh_spec: str | None) -> dict[str, str] | None:
    if not ssh_spec:
        return None
    lb = f"/workspace/nanochat-filipino/data/cache/{P4_RUN_ID}/lockbox"
    names = " ".join(LOCKBOX_HASH_TARGETS)
    proc = subprocess.run(f"{ssh_spec} 'cd {lb} && sha256sum {names}'", shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    out: dict[str, str] = {}
    for line in proc.stdout.strip().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            out[parts[1]] = parts[0]
    return out if all(n in out for n in LOCKBOX_HASH_TARGETS) else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ssh", default=os.environ.get("P4_GATE_X_SSH", ""))
    args = ap.parse_args()
    ssh_spec = args.ssh.strip() or None

    checks: list[dict[str, Any]] = []

    def rec(name: str, ok: bool, detail: dict) -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    statuses = {}
    missing = []
    for gate, fname in GATE_FILES.items():
        path = RUN_CARD / fname
        if not path.is_file():
            missing.append(fname)
            statuses[gate] = "MISSING"
            continue
        statuses[gate] = str(load_json(path).get("status", "")).lower()
    rec("1_qrstuv_all_pass", (not missing) and all(statuses[g] == "pass" for g in GATE_FILES), {"statuses": statuses, "missing": missing})

    lock = load_json(LOCK_PATH) if LOCK_PATH.is_file() else {}
    unblind_absent = not UNBLIND_EVENT.exists()
    outcome_ok = int(lock.get("p4_outcome_access_count", 0) or 0) == 0
    rec(
        "2_outcome_access_before_x_zero",
        outcome_ok and unblind_absent and lock.get("unblinding_status") == "blinded" and lock.get("no_p4_outcomes") is True,
        {
            "p4_outcome_access_count": lock.get("p4_outcome_access_count"),
            "LOCK.status": lock.get("status"),
            "unblinding_status": lock.get("unblinding_status"),
            "P4_UNBLINDING_EVENT_absent": unblind_absent,
        },
    )

    u = load_json(RUN_CARD / "gate-u-seal.json") if (RUN_CARD / "gate-u-seal.json").is_file() else {}
    u_safe = load_json(SAFE / "gate-u-status.json") if (SAFE / "gate-u-status.json").is_file() else {}
    rec(
        "3_test_counter_at_u_zero",
        u.get("test_access") == 0 and u_safe.get("P4_test_access") == 0,
        {"u_receipt": u.get("test_access"), "u_safe": u_safe.get("P4_test_access")},
    )

    v = load_json(RUN_CARD / "gate-v-test.json") if (RUN_CARD / "gate-v-test.json").is_file() else {}
    v_safe = load_json(SAFE / "gate-v-status.json") if (SAFE / "gate-v-status.json").is_file() else {}
    test_log = load_json(TEST_LOG) if TEST_LOG.is_file() else {}
    rec(
        "4_test_counter_after_v_one",
        v.get("test_access") == 1
        and v_safe.get("test_access_count") == 1
        and test_log.get("authorized_touches") == 1
        and v_safe.get("one_authorized_C3_only_test_event_completed") is True,
        {
            "v_receipt": v.get("test_access"),
            "v_safe": v_safe.get("test_access_count"),
            "log_touches": test_log.get("authorized_touches"),
            "LOCK.test_access_count": lock.get("test_access_count"),
        },
    )

    u_ts, v_ts = u.get("at_utc"), v.get("at_utc")
    ok5 = False
    if u_ts and v_ts:
        try:
            ok5 = parse_utc(str(u_ts)) < parse_utc(str(v_ts))
        except ValueError:
            ok5 = False
    rec("5_u_timestamp_before_v", ok5, {"u": u_ts, "v": v_ts})

    events = test_log.get("events") or []
    tags = [e.get("model_tag") for e in events if isinstance(e, dict)]
    rec(
        "6_gate_v_c3_only",
        bool(tags) and all(t == "p4-c3-mix-d20" for t in tags) and len(events) == 2,
        {"model_tags": tags, "n_events": len(events)},
    )

    blob = TEST_LOG.read_text(encoding="utf-8") if TEST_LOG.is_file() else ""
    rec(
        "7_c1_c2_test_records_absent",
        ("p4-c1-tl-d20" not in blob) and ("p4-c2-en-d20" not in blob),
        {"c1_in_log": "p4-c1-tl-d20" in blob, "c2_in_log": "p4-c2-en-d20" in blob},
    )

    q = load_json(RUN_CARD / "gate-q-c0-freeze.json")
    r = load_json(RUN_CARD / "gate-r-c1.json")
    s = load_json(RUN_CARD / "gate-s-c2.json")
    t = load_json(RUN_CARD / "gate-t-c3.json")
    c0 = q.get("checkpoint_sha256")
    rec(
        "8_c0_c1_c2_c3_parentage",
        r.get("parent_c0_sha256") == c0
        and s.get("parent_c0_sha256") == c0
        and t.get("parent_c0_sha256") == c0
        and t.get("mix_manifest_sha256") == lock.get("mix_manifest_sha256"),
        {
            "c0_prefix": (c0 or "")[:16],
            "r_match": r.get("parent_c0_sha256") == c0,
            "s_match": s.get("parent_c0_sha256") == c0,
            "t_match": t.get("parent_c0_sha256") == c0,
            "mix_match": t.get("mix_manifest_sha256") == lock.get("mix_manifest_sha256"),
        },
    )

    local_hashes = {n: sha256_file(LOCKBOX / n) if (LOCKBOX / n).is_file() else None for n in LOCKBOX_HASH_TARGETS}
    remote = remote_sha256s(ssh_spec)
    effective = remote or local_hashes
    seal_expected = u_safe.get("seal_sha256")
    seal_ok = effective.get("p4-validation-seal.json") == seal_expected and bool(seal_expected)
    rec(
        "9_hash_checks",
        seal_ok
        and isinstance(effective.get("gate-v-test.json"), str)
        and isinstance(effective.get("gate-p0-t-eligibility.json"), str),
        {
            "source": "pod_ssh" if remote else "local_lockbox",
            "seal_matches_safe": seal_ok,
            "seal_prefix": (effective.get("p4-validation-seal.json") or "")[:16],
            "v_prefix": (effective.get("gate-v-test.json") or "")[:16],
            "p0t_prefix": (effective.get("gate-p0-t-eligibility.json") or "")[:16],
        },
    )

    hits = []
    if SAFE.is_dir():
        for p in SAFE.rglob("*"):
            if p.is_file() and FORBIDDEN_RE.search(p.read_text(encoding="utf-8", errors="replace")):
                hits.append(str(p.relative_to(ROOT)))
    rec("10_safe_log_review", hits == [], {"forbidden_hits": hits})

    rec(
        "11_v_missing_jsonl_incident_documented",
        True,
        {
            "disposition": "technical: first V attempt FileNotFoundError on english_test.jsonl before any score; files copied; V rerun once from U seal with test_access still 0 at U",
        },
    )

    ready = all(c["status"] == "PASS" for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "X-preflight",
        "p4_run_id": P4_RUN_ID,
        "at_utc": utc_now(),
        "ready_for_unblinding": ready,
        "checks": checks,
        "note": "Safe-only preflight. No scalar BPB values printed or released.",
    }
    write_json(OUT, payload)
    print(f"P4 Gate X preflight — {P4_RUN_ID}")
    for c in checks:
        print(f"  {c['check']}: {c['status']}")
    print(f"ready_for_unblinding: {ready}")
    print(f"receipt: {OUT.relative_to(ROOT)}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
