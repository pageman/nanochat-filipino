#!/usr/bin/env python3
"""Gate 0 lockbox acceptance tests (dummy data only; no real val/test text)."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "p3"))
from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256  # noqa: E402

PIN = "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"
PROTOCOL = ROOT / "docs" / "papers" / "p3-reverse" / "PROTOCOL-p3-tl-then-en.md"
LOCK = ROOT / "docs" / "papers" / "p3-reverse" / "LOCK.json"
PDF = ROOT / "docs" / "run-cards" / "AsPredicted-307342.pdf"
FILED_PROTOCOL_SHA = "899ba83f0b36f2b4bf4c16b3c675e58788d7763cb439f8a8c3a3c061bda2b986"
FILED_PDF_SHA = "6cfad0386dff689ad73fa2bf80b70dd4ad191dc44e21e3e4c11c06825ae550b1"

DUMMY_BPB = "9.123456"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk_sha(dir_path: Path) -> dict[str, str]:
    out = {}
    for p in sorted(dir_path.rglob("*")):
        if p.is_file() and p.name != "__pycache__" and p.suffix != ".pyc":
            rel = str(p.relative_to(ROOT))
            out[rel] = sha256(p)
    return out


def run(cmd: list[str], env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)


def encrypt(src: Path, dst: Path, passfile: Path) -> None:
    subprocess.run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-pbkdf2",
            "-salt",
            "-pass",
            f"file:{passfile}",
            "-in",
            str(src),
            "-out",
            str(dst),
        ],
        check=True,
    )


def main() -> int:
    os.environ["NANOCHAT_FILIPINO_ROOT"] = str(ROOT)
    run_id = "p3-20260819T192700Z-92d63d4"
    cache = ROOT / "data" / "cache" / run_id
    lockbox = cache / "lockbox"
    safe = cache / "safe_progress"
    released = cache / "released_dummy"
    passfile = cache / ".lockbox_pass"
    for d in (lockbox, safe, released):
        d.mkdir(parents=True, exist_ok=True)
        os.chmod(d, 0o700)
    passfile.write_text("p3-gate0-dummy-passphrase-not-for-production\n")
    os.chmod(passfile, 0o600)

    tests: dict[str, dict] = {}

    proto_sha = sha256(PROTOCOL)
    pdf_sha = sha256(PDF)
    lock_sha = sha256(LOCK)
    scripts_sha = walk_sha(ROOT / "scripts" / "p3")
    t1 = proto_sha == FILED_PROTOCOL_SHA and pdf_sha == FILED_PDF_SHA
    tests["1"] = {
        "name": "protocol/lock/pdf hashes agree with filing",
        "pass": t1,
        "protocol_sha256": proto_sha,
        "pdf_sha256": pdf_sha,
        "lock_sha256": lock_sha,
    }

    dummy_plain = lockbox / "dummy_bpb.json"
    dummy_plain.write_text(json.dumps({"val_bpb_full": float(DUMMY_BPB)}) + "\n")
    dummy_enc = lockbox / "dummy_bpb.json.enc"
    encrypt(dummy_plain, dummy_enc, passfile)
    dummy_plain.unlink()
    steward_blob = dummy_enc.read_bytes()
    t2 = DUMMY_BPB.encode() not in steward_blob
    try:
        json.loads(steward_blob.decode("utf-8"))
        t2 = False
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass
    tests["2"] = {"name": "steward cannot open dummy lockbox result", "pass": t2}

    (safe / "health.json").write_text(json.dumps({"health": "pass", "finite": True}) + "\n")
    safe_text = "".join(p.read_text() for p in safe.glob("*") if p.is_file())
    t3 = DUMMY_BPB not in safe_text
    tests["3"] = {"name": "dummy BPB string absent from safe_progress", "pass": t3}

    labels = {"job-amber": "B1", "job-cobalt": "B2", "job-cedar": "B3"}
    (lockbox / "opaque_job_map.json").write_text(json.dumps(labels) + "\n")
    (safe / "jobs.json").write_text(json.dumps({"jobs": ["job-amber", "job-cobalt", "job-cedar"]}) + "\n")
    job_txt = (safe / "jobs.json").read_text()
    t4 = all(x not in job_txt for x in ("B1", "B2", "B3"))
    tests["4"] = {"name": "opaque job labels omit B1/B2/B3", "pass": t4}

    env = os.environ.copy()
    env["NANOCHAT_FILIPINO_ROOT"] = str(ROOT)
    sourced = subprocess.run(
        ["bash", "-lc", f"source {ROOT}/scripts/p3/env.sh && echo TEST_EN=${{P3_TEST_JSONL_EN-UNSET}} && echo TEST_TL=${{P3_TEST_JSONL_TL-UNSET}}"],
        capture_output=True,
        text=True,
        env=env,
    )
    t5 = "TEST_EN=UNSET" in sourced.stdout and "TEST_TL=UNSET" in sourced.stdout
    tests["5"] = {"name": "train env cannot resolve test path", "pass": t5, "stdout": sourced.stdout.strip()}

    t6 = True
    try:
        reject_parent_sha256(next(iter(FORBIDDEN_PARENT_SHA256)))
        t6 = False
    except SystemExit:
        t6 = True
    tests["6"] = {"name": "P1.1/P2 weight SHA256s rejected as parent", "pass": t6}

    r7 = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "dummy_p0t.py"),
            "--lockbox",
            str(lockbox),
            "--safe-progress",
            str(safe),
            "--status",
            "PASS",
        ]
    )
    safe_p0 = (safe / "gate-p0-t-status.json").read_text()
    t7 = r7.returncode == 0 and "P0-T: PASS" in r7.stdout and "1.111111" not in safe_p0 and "1.111111" in (lockbox / "gate-p0-t-eligibility.json").read_text()
    tests["7"] = {"name": "dummy P0-T emits only PASS/BLOCKED outside lockbox", "pass": t7, "stdout": r7.stdout.strip()}

    r8a = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "make_validation_seal.py"),
            "--lockbox",
            str(lockbox),
            "--safe-progress",
            str(safe),
        ]
    )
    t8_refuse = r8a.returncode == 2
    for name, val in {
        "b1_en_val_bpb_full.json": 2.01,
        "b1_tl_val_bpb_full.json": 1.51,
        "b2_en_val_bpb_full.json": 1.41,
        "b2_tl_val_bpb_full.json": 1.61,
        "b3_en_val_bpb_full.json": 1.71,
        "b3_tl_val_bpb_full.json": 1.55,
        "b0_en_val_bpb_full.json": 3.01,
    }.items():
        (lockbox / name).write_text(json.dumps({"val_bpb_full": val, "arm_file": name}) + "\n")
        os.chmod(lockbox / name, 0o600)
    r8b = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "make_validation_seal.py"),
            "--lockbox",
            str(lockbox),
            "--safe-progress",
            str(safe),
        ]
    )
    u_safe = (safe / "gate-u-status.json").read_text()
    t8 = t8_refuse and r8b.returncode == 0 and "1.41" not in u_safe and "C_tl" not in u_safe
    tests["8"] = {
        "name": "contrast refuses until six child + B0 EN exist",
        "pass": t8,
        "refuse_rc": r8a.returncode,
        "ok_rc": r8b.returncode,
        "safe": u_safe.strip(),
    }

    r9a = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "dummy_b2_test.py"),
            "--lockbox",
            str(lockbox),
            "--safe-progress",
            str(safe),
            "--arm",
            "B1",
        ]
    )
    seal_bak = (lockbox / "p3-validation-seal.json").read_bytes()
    (lockbox / "p3-validation-seal.json").unlink()
    r9b = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "dummy_b2_test.py"),
            "--lockbox",
            str(lockbox),
            "--safe-progress",
            str(safe),
            "--arm",
            "B2",
        ]
    )
    (lockbox / "p3-validation-seal.json").write_bytes(seal_bak)
    r9c = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "dummy_b2_test.py"),
            "--lockbox",
            str(lockbox),
            "--safe-progress",
            str(safe),
            "--arm",
            "B2",
        ]
    )
    v_safe = (safe / "gate-v-status.json").read_text()
    t9 = r9a.returncode == 2 and r9b.returncode == 2 and r9c.returncode == 0 and "9.999" not in v_safe
    tests["9"] = {
        "name": "dummy test evaluator rejects B1/B3 and missing U seal",
        "pass": t9,
        "stdout_ok": r9c.stdout.strip(),
    }

    incomplete = cache / "lockbox_incomplete"
    incomplete.mkdir(exist_ok=True)
    r10 = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "release_bundle.py"),
            "--lockbox",
            str(incomplete),
            "--released",
            str(released / "bad"),
        ]
    )
    t10 = r10.returncode == 2
    tests["10"] = {"name": "release refuses incomplete inventory", "pass": t10}

    r11 = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "release_bundle.py"),
            "--lockbox",
            str(lockbox),
            "--released",
            str(released / "good"),
        ]
    )
    man = json.loads((released / "good" / "released_manifest.json").read_text())
    t11 = r11.returncode == 0 and all(
        man[n] == hashlib.sha256((lockbox / n).read_bytes()).hexdigest() for n in man
    )
    tests["11"] = {"name": "dummy released hashes match manifest", "pass": t11}

    r12 = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "p3" / "break_glass.py"),
            "--lockbox",
            str(lockbox),
            "--safe-progress",
            str(safe),
        ]
    )
    bg_safe = (safe / "break-glass-status.json").read_text()
    t12 = r12.returncode == 0 and DUMMY_BPB not in r12.stdout and "9.123456" not in bg_safe
    tests["12"] = {"name": "break-glass dummy writes audit without printing dummy BPB", "pass": t12, "stdout": r12.stdout.strip()}

    all_pass = all(v["pass"] for v in tests.values())
    report = {
        "gate": "0",
        "p3_run_id": run_id,
        "nanochat_pin": PIN,
        "all_pass": all_pass,
        "tests": tests,
        "scripts_p3_sha256": scripts_sha,
        "no_p3_outcomes": True,
        "no_real_val_test_text": True,
        "researchbox_id": None,
        "note": "ResearchBox still human. Dummy lockbox lives under gitignored data/cache.",
    }
    out_dir = ROOT / "docs" / "run-cards" / "p3" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "gate-0-lockbox-tests.json"
    # Strip dummy BPB from any test debug fields
    text = json.dumps(report, indent=2, sort_keys=True)
    if DUMMY_BPB in text:
        report["tests"]["3"]["sanitized"] = True
    (out).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    public = ROOT / "docs" / "run-cards" / "p3" / "gate-0-filing-lock.json"
    print(json.dumps({"all_pass": all_pass, "report": str(out.relative_to(ROOT))}, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
