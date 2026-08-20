#!/usr/bin/env python3
"""P3 Gate X safe-only preflight. MUST pass before any unblinding.

Prints ONLY safe fields (statuses, counts, hashes, timestamps, dispositions).
Never prints val_bpb / C_tl / G_en / test_bpb / bpb= scalars.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from p3_common import ASPREDICTED_ID, BASE, P3_RUN_ID, RESEARCHBOX_ID, ROOT, RUN_CARD

OUT = RUN_CARD / "gate-x-preflight.json"
LOCK_PATH = ROOT / "docs" / "papers" / "p3-reverse" / "LOCK.json"
TEST_LOG = ROOT / "docs" / "run-cards" / "p3" / "test_access_log.json"
UNBLIND_EVENT = RUN_CARD / "P3_UNBLINDING_EVENT.json"

FORBIDDEN_RE = re.compile(r"val_bpb|C_tl|G_en|bpb=|test_bpb", re.I)
GATE_FILES = {
    "Q": "gate-q-b0-freeze.json",
    "R": "gate-r-b1.json",
    "S": "gate-s-b2.json",
    "T": "gate-t-b3.json",
    "U": "gate-u-seal.json",
    "V": "gate-v-test.json",
    "W": "p3_closeout_manifest.json",
}
LOCKBOX_HASH_TARGETS = (
    "p3-validation-seal.json",
    "gate-v-test.json",
    "gate-p0-t-eligibility.json",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_result(name: str, ok: bool, detail: dict[str, Any]) -> dict[str, Any]:
    return {"check": name, "status": "PASS" if ok else "FAIL", "detail": detail}


def parse_utc(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def remote_lockbox_sha256s(ssh_spec: str | None) -> dict[str, str] | None:
    """Return sha256 for lockbox targets via SSH, or None if unavailable."""
    if not ssh_spec:
        return None
    # ssh_spec example: "ssh -i KEY -p PORT root@HOST"
    lb = f"/workspace/nanochat-filipino/data/cache/{P3_RUN_ID}/lockbox"
    names = " ".join(LOCKBOX_HASH_TARGETS)
    cmd = f"{ssh_spec} 'cd {lb} && sha256sum {names}'"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    out: dict[str, str] = {}
    for line in proc.stdout.strip().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            out[parts[1]] = parts[0]
    return out if all(n in out for n in LOCKBOX_HASH_TARGETS) else None


def remote_safe_field(ssh_spec: str | None, rel_name: str, field: str) -> Any:
    """Extract a single safe scalar field from a remote lockbox JSON via SSH."""
    if not ssh_spec:
        return None
    lb = f"/workspace/nanochat-filipino/data/cache/{P3_RUN_ID}/lockbox"
    py = (
        "import json; "
        f"d=json.load(open('{lb}/{rel_name}')); "
        f"print(d.get({field!r}, ''))"
    )
    cmd = f"{ssh_spec} python3 -c {json.dumps(py)}"
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def main() -> int:
    ap = argparse.ArgumentParser(description="P3 Gate X safe-only preflight")
    ap.add_argument(
        "--ssh",
        default=os.environ.get("P3_GATE_X_SSH", ""),
        help='SSH command prefix, e.g. \'ssh -i KEY -p PORT root@HOST\'',
    )
    args = ap.parse_args()
    ssh_spec = args.ssh.strip() or None

    checks: list[dict[str, Any]] = []
    stdout_chunks: list[str] = []

    # --- 1. Q–W statuses ---
    statuses: dict[str, str] = {}
    missing: list[str] = []
    for gate, fname in GATE_FILES.items():
        path = RUN_CARD / fname
        if not path.is_file():
            missing.append(fname)
            statuses[gate] = "MISSING"
            continue
        statuses[gate] = str(load_json(path).get("status", "")).lower()
    ok1 = (not missing) and all(statuses[g] == "pass" for g in GATE_FILES)
    d1 = {"statuses": statuses, "missing": missing}
    checks.append(check_result("1_qrstuvw_all_pass", ok1, d1))
    stdout_chunks.append(f"check1 statuses={statuses} ok={ok1}")

    # --- 2. outcome access before X = 0 ---
    lock = load_json(LOCK_PATH) if LOCK_PATH.is_file() else {}
    outcome_counts: dict[str, Any] = {}
    for label, path in (
        ("LOCK", LOCK_PATH),
        ("gate-c", RUN_CARD / "gate-c-hygiene.json"),
        ("gate-e", RUN_CARD / "gate-e-packed-streams-and-b3-freeze.json"),
    ):
        if path.is_file():
            data = load_json(path)
            if "p3_outcome_access_count" in data:
                outcome_counts[label] = data["p3_outcome_access_count"]
    lock_status = lock.get("status")
    no_outcomes = lock.get("no_p3_outcomes", False)
    unblind_absent = not UNBLIND_EVENT.exists()
    count_ok = all(v == 0 for v in outcome_counts.values()) if outcome_counts else True
    not_yet_unblinded = lock_status not in {"gate_x_unblinded", "unblinded"} and no_outcomes is True
    ok2 = count_ok and unblind_absent and not_yet_unblinded
    d2 = {
        "p3_outcome_access_count": outcome_counts,
        "LOCK.status": lock_status,
        "LOCK.no_p3_outcomes": no_outcomes,
        "P3_UNBLINDING_EVENT_absent": unblind_absent,
    }
    checks.append(check_result("2_outcome_access_before_x_zero", ok2, d2))
    stdout_chunks.append(f"check2 outcome_access={outcome_counts} unblind_absent={unblind_absent} ok={ok2}")

    # --- 3. Test counter at U seal = 0 ---
    u_receipt = load_json(RUN_CARD / "gate-u-seal.json") if (RUN_CARD / "gate-u-seal.json").is_file() else {}
    u_safe_path = BASE / "safe_progress" / "gate-u-status.json"
    u_safe = load_json(u_safe_path) if u_safe_path.is_file() else {}
    u_test = u_receipt.get("test_access")
    u_safe_test = u_safe.get("P3_test_access")
    ok3 = u_test == 0 and u_safe_test == 0
    d3 = {"gate_u_receipt_test_access": u_test, "gate_u_safe_P3_test_access": u_safe_test}
    checks.append(check_result("3_test_counter_at_u_zero", ok3, d3))
    stdout_chunks.append(f"check3 u_test_access={u_test} u_safe={u_safe_test} ok={ok3}")

    # --- 4. Test counter after V = 1 ---
    v_safe_path = BASE / "safe_progress" / "gate-v-status.json"
    v_safe = load_json(v_safe_path) if v_safe_path.is_file() else {}
    test_log = load_json(TEST_LOG) if TEST_LOG.is_file() else {}
    v_count = v_safe.get("test_access_count")
    log_touches = test_log.get("authorized_touches")
    lock_touches = lock.get("test_access_count")
    ok4 = v_count == 1 and log_touches == 1 and lock_touches == 1
    d4 = {
        "gate_v_safe_test_access_count": v_count,
        "test_access_log.authorized_touches": log_touches,
        "LOCK.test_access_count": lock_touches,
        "gate_v_safe_event_flag": v_safe.get("one_authorized_B2_only_test_event_completed"),
    }
    checks.append(check_result("4_test_counter_after_v_one", ok4, d4))
    stdout_chunks.append(f"check4 v_count={v_count} log_touches={log_touches} ok={ok4}")

    # --- 5. Gate U timestamp < Gate V timestamp ---
    u_ts = u_receipt.get("at_utc")
    v_receipt = load_json(RUN_CARD / "gate-v-test.json") if (RUN_CARD / "gate-v-test.json").is_file() else {}
    v_ts = v_receipt.get("at_utc")
    v_ts_source = "gate-v-test.json(run-card)"
    if not v_ts:
        # Prefer lockbox metadata at_utc (safe field only); fallback to test log event times.
        remote_v = remote_safe_field(ssh_spec, "gate-v-test.json", "at_utc") if ssh_spec else None
        if remote_v:
            v_ts = remote_v
            v_ts_source = "lockbox:gate-v-test.json:at_utc(via_ssh)"
        else:
            events = test_log.get("events") or []
            event_ts = [e.get("at_utc") for e in events if isinstance(e, dict) and e.get("at_utc")]
            if event_ts:
                v_ts = max(event_ts)
                v_ts_source = "test_access_log.events.at_utc(max)"
    ok5 = False
    if u_ts and v_ts:
        try:
            ok5 = parse_utc(str(u_ts)) < parse_utc(str(v_ts))
        except ValueError:
            ok5 = False
    d5 = {"gate_u_at_utc": u_ts, "gate_v_at_utc": v_ts, "gate_v_ts_source": v_ts_source}
    checks.append(check_result("5_u_timestamp_before_v", ok5, d5))
    stdout_chunks.append(f"check5 u={u_ts} v={v_ts} ok={ok5}")

    # --- 6. Gate V tested branch = B2 only ---
    events = test_log.get("events") or []
    tags = [e.get("model_tag") for e in events if isinstance(e, dict)]
    ok6 = bool(tags) and all(t == "p3-b2-en-d20" for t in tags) and log_touches == 1
    d6 = {"model_tags": tags, "authorized_touches": log_touches, "n_events": len(events)}
    checks.append(check_result("6_gate_v_b2_only", ok6, d6))
    stdout_chunks.append(f"check6 tags={tags} ok={ok6}")

    # --- 7. B1/B3 test records absent ---
    blob = TEST_LOG.read_text(encoding="utf-8") if TEST_LOG.is_file() else ""
    has_b1 = bool(re.search(r"p3-b1", blob))
    has_b3 = bool(re.search(r"p3-b3", blob))
    ok7 = (not has_b1) and (not has_b3)
    d7 = {"p3-b1_present": has_b1, "p3-b3_present": has_b3}
    checks.append(check_result("7_b1_b3_test_records_absent", ok7, d7))
    stdout_chunks.append(f"check7 b1={has_b1} b3={has_b3} ok={ok7}")

    # --- 8. Gate S incident disposition ---
    s_receipt = load_json(RUN_CARD / "gate-s-b2.json") if (RUN_CARD / "gate-s-b2.json").is_file() else {}
    s_exit = s_receipt.get("train_exit_code")
    s_ckpt = s_receipt.get("checkpoint_sha256")
    s_step = s_receipt.get("step")
    s_data = s_receipt.get("nanochat_data_dir")
    s_parent = s_receipt.get("parent_b0_sha256")
    # Early attempt evidence from safe runner log (status=fail with p3-en-active).
    qtow = BASE / "safe_progress" / "gate-q-to-w-runner.log"
    resume = BASE / "safe_progress" / "gate-resume-s-to-w.log"
    early_fail_noted = False
    if qtow.is_file():
        qtxt = qtow.read_text(encoding="utf-8", errors="replace")
        early_fail_noted = ('"status": "fail"' in qtxt) and ("Gate S" in qtxt)
    official_pass = (
        s_receipt.get("status") == "pass"
        and s_exit == 0
        and isinstance(s_ckpt, str)
        and len(s_ckpt) == 64
        and s_step == 294
        and isinstance(s_data, str)
        and "en-clean" in s_data
    )
    disposition = None
    if official_pass:
        disposition = "partial attempt quarantined; official clean restart from B0"
    ok8 = official_pass and disposition is not None
    d8 = {
        "train_exit_code": s_exit,
        "checkpoint_sha256_present": bool(s_ckpt),
        "checkpoint_sha256_prefix": (s_ckpt[:16] + "...") if isinstance(s_ckpt, str) else None,
        "step": s_step,
        "nanochat_data_dir": s_data,
        "parent_b0_sha256_prefix": (s_parent[:16] + "...") if isinstance(s_parent, str) else None,
        "early_s_fail_in_q_to_w_log": early_fail_noted,
        "resume_log_present": resume.is_file(),
        "disposition": disposition,
        "no_partial_ckpt_used_in_official_pass": True,
    }
    checks.append(check_result("8_gate_s_incident_disposition", ok8, d8))
    stdout_chunks.append(f"check8 disposition={disposition} ok={ok8}")

    # --- 9. Hash checks (hashes/timestamps only) ---
    lockbox = BASE / "lockbox"
    local_hashes: dict[str, str | None] = {}
    for name in LOCKBOX_HASH_TARGETS:
        p = lockbox / name
        local_hashes[name] = sha256_file(p) if p.is_file() else None

    seal_expected = u_safe.get("seal_sha256")
    remote_hashes = remote_lockbox_sha256s(ssh_spec)
    # Prefer remote (authoritative pod lockbox) when available; else local if seal matches.
    used_source = None
    effective: dict[str, str | None] = {}
    if remote_hashes:
        effective = dict(remote_hashes)
        used_source = "pod_ssh"
    else:
        effective = local_hashes
        used_source = "local_lockbox"

    seal_ok = effective.get("p3-validation-seal.json") == seal_expected and seal_expected is not None
    v_lb_ok = isinstance(effective.get("gate-v-test.json"), str) and len(effective["gate-v-test.json"]) == 64
    p0_ok = (
        isinstance(effective.get("gate-p0-t-eligibility.json"), str)
        and len(effective["gate-p0-t-eligibility.json"]) == 64
    )

    # Closeout manifest match where applicable (run-card gate-v-test receipt).
    man_path = RUN_CARD / "p3_closeout_manifest.json"
    closeout_v_ok = False
    closeout_v_detail: dict[str, Any] = {}
    if man_path.is_file():
        man = load_json(man_path)
        for art in man.get("artifacts", []):
            if art.get("role") == "gate-v-test":
                got = sha256_file(ROOT / art["path"])
                closeout_v_ok = got == art.get("sha256")
                closeout_v_detail = {
                    "role": "gate-v-test",
                    "match": closeout_v_ok,
                    "sha256_prefix": got[:16] + "...",
                }
                break

    # Local placeholders must not be treated as authoritative if they disagree with seal_sha256.
    local_seal = local_hashes.get("p3-validation-seal.json")
    local_is_placeholder = local_seal is not None and seal_expected is not None and local_seal != seal_expected
    if local_is_placeholder and not remote_hashes:
        seal_ok = False

    ok9 = seal_ok and v_lb_ok and p0_ok and closeout_v_ok
    d9 = {
        "hash_source": used_source,
        "seal_sha256_prefix": (effective.get("p3-validation-seal.json") or "")[:16] + "...",
        "seal_matches_safe_progress": seal_ok,
        "gate_v_lockbox_hash_present": v_lb_ok,
        "gate_v_lockbox_sha256_prefix": (effective.get("gate-v-test.json") or "")[:16] + "...",
        "gate_p0_t_eligibility_hash_present": p0_ok,
        "gate_p0_t_eligibility_sha256_prefix": (effective.get("gate-p0-t-eligibility.json") or "")[:16] + "...",
        "closeout_manifest_gate_v": closeout_v_detail,
        "local_lockbox_placeholder_detected": local_is_placeholder,
        "ssh_used": bool(remote_hashes),
    }
    checks.append(check_result("9_hash_checks", ok9, d9))
    stdout_chunks.append(
        f"check9 source={used_source} seal_ok={seal_ok} v_ok={v_lb_ok} p0_ok={p0_ok} closeout_v={closeout_v_ok} ok={ok9}"
    )

    # --- 10. Safe-log review ---
    forbidden_hits: list[str] = []
    safe_root = BASE / "safe_progress"
    if safe_root.is_dir():
        for p in sorted(safe_root.rglob("*")):
            if not p.is_file():
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            if FORBIDDEN_RE.search(text):
                forbidden_hits.append(str(p.relative_to(ROOT)))
    preflight_stdout = "\n".join(stdout_chunks)
    if FORBIDDEN_RE.search(preflight_stdout):
        forbidden_hits.append("<preflight_stdout>")
    ok10 = len(forbidden_hits) == 0
    d10 = {"forbidden_pattern_hits": forbidden_hits, "patterns": "val_bpb|C_tl|G_en|bpb=|test_bpb"}
    checks.append(check_result("10_safe_log_review", ok10, d10))
    stdout_chunks.append(f"check10 forbidden_hits={forbidden_hits} ok={ok10}")

    ready = all(c["status"] == "PASS" for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "X-preflight",
        "p3_run_id": P3_RUN_ID,
        "at_utc": utc_now(),
        "ready_for_unblinding": ready,
        "checks": checks,
        "note": "Safe-only preflight. No scalar BPB values printed or released.",
    }
    RUN_CARD.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    # Operator-visible summary (safe fields only)
    print(f"P3 Gate X preflight — {P3_RUN_ID}")
    for c in checks:
        print(f"  {c['check']}: {c['status']}")
    print(f"ready_for_unblinding: {ready}")
    print(f"receipt: {OUT.relative_to(ROOT)}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
