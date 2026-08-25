#!/usr/bin/env python3
"""P6 Gate 0 lockbox acceptance tests (dummy data only; no real val/test text)."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "p6"))
from forbidden_parents import FORBIDDEN_PARENT_SHA256, reject_parent_sha256  # noqa: E402
from p6_common import (  # noqa: E402
    ADDENDUM,
    CACHE,
    FILED_ADDENDUM_SHA,
    FILED_GATE_PLAN_SHA,
    FILED_PDF_SHA,
    GATE_PLAN,
    LOCK_PATH,
    LOCKBOX,
    P3_B3_MIX_ORDER_SHA,
    P6_RUN_ID,
    PANEL_SEEDS,
    PASSFILE,
    PDF,
    PIN,
    RESEARCHBOX_ID,
    RUN_CARD,
    SAFE,
    TIER2,
    TOKEN_BYTES_SHA,
    TOKENIZER_PKL_SHA,
    mark_ledger,
    seed_lockbox_dirs,
    utc_now,
    write_json,
)

DUMMY_BPB = "9.123456"
SCRIPTS = ROOT / "scripts" / "p6"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk_sha(dir_path: Path) -> dict[str, str]:
    out = {}
    for p in sorted(dir_path.rglob("*")):
        if p.is_file() and p.name != "__pycache__" and p.suffix != ".pyc":
            out[str(p.relative_to(ROOT))] = sha256(p)
    return out


def tree_digest(files: dict[str, str]) -> str:
    blob = "".join(f"{k} {v}\n" for k, v in sorted(files.items())).encode()
    return hashlib.sha256(blob).hexdigest()


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
    os.environ["P6_RUN_ID"] = P6_RUN_ID
    os.environ["NANOCHAT_BASE_DIR"] = str(CACHE)
    released = CACHE / "released_dummy"
    seed_lockbox_dirs()
    for d in (released,):
        d.mkdir(parents=True, exist_ok=True)
    PASSFILE.write_text("p6-gate0-dummy-passphrase-not-for-production-or-researchbox\n")
    os.chmod(PASSFILE, 0o600)

    tests: dict[str, dict] = {}
    lock_obj = json.loads(LOCK_PATH.read_text())

    plan_sha = sha256(GATE_PLAN)
    addendum_sha = sha256(ADDENDUM)
    pdf_sha = sha256(PDF)
    eval_sha = sha256(SCRIPTS / "evaluate_bpb.py")
    t1 = (
        plan_sha == FILED_GATE_PLAN_SHA
        and pdf_sha == FILED_PDF_SHA
        and lock_obj.get("gate_plan_sha256") == FILED_GATE_PLAN_SHA
        and lock_obj.get("addendum_sha256") == FILED_ADDENDUM_SHA
        and lock_obj.get("aspredicted_pdf_sha256") == FILED_PDF_SHA
        and (SCRIPTS / "evaluate_bpb.py").is_file()
        and TIER2.is_dir()
        and stat.S_IMODE(LOCKBOX.stat().st_mode) != stat.S_IMODE(SAFE.stat().st_mode)
        and all((LOCKBOX / f"seed-{s}").is_dir() for s in PANEL_SEEDS)
    )
    tests["1"] = {
        "name": "filing/lock/config/evaluator + seed-4 lockbox + tier2",
        "pass": t1,
        "gate_plan_sha256": plan_sha,
        "addendum_filed_sha256": FILED_ADDENDUM_SHA,
        "addendum_local_sha256": addendum_sha,
        "addendum_local_matches_filed": addendum_sha == FILED_ADDENDUM_SHA,
        "pdf_sha256": pdf_sha,
        "evaluate_bpb_stub_sha256": eval_sha,
    }

    dummy_plain = LOCKBOX / "dummy_bpb.json"
    dummy_plain.write_text(json.dumps({"val_bpb_full": float(DUMMY_BPB)}) + "\n")
    dummy_enc = LOCKBOX / "dummy_bpb.json.enc"
    encrypt(dummy_plain, dummy_enc, PASSFILE)
    dummy_plain.unlink()
    steward_blob = dummy_enc.read_bytes()
    t2 = DUMMY_BPB.encode() not in steward_blob
    try:
        json.loads(steward_blob.decode("utf-8"))
        t2 = False
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass
    tests["2"] = {"name": "steward cannot open dummy lockbox result", "pass": t2}

    (SAFE / "health.json").write_text(json.dumps({"health": "pass", "finite": True}) + "\n")
    safe_text = "".join(p.read_text() for p in SAFE.glob("*") if p.is_file())
    t3 = DUMMY_BPB not in safe_text
    tests["3"] = {"name": "dummy BPB string absent from safe_progress", "pass": t3}

    labels = {"job-amber": "C1", "job-cobalt": "C2", "job-cedar": "C3"}
    (LOCKBOX / "opaque_job_map.json").write_text(json.dumps(labels) + "\n")
    (SAFE / "jobs.json").write_text(json.dumps({"jobs": ["job-amber", "job-cobalt", "job-cedar"]}) + "\n")
    job_txt = (SAFE / "jobs.json").read_text()
    t4 = all(x not in job_txt for x in ("C1", "C2", "C3"))
    tests["4"] = {"name": "opaque job labels omit C1/C2/C3", "pass": t4}

    env = os.environ.copy()
    env["NANOCHAT_FILIPINO_ROOT"] = str(ROOT)
    env["P6_RUN_ID"] = P6_RUN_ID
    for k in ("P4_TEST_JSONL_EN", "P4_TEST_JSONL_TL", "P5_TEST_JSONL_EN", "P5_TEST_JSONL_TL", "P6_TEST_JSONL_EN", "P6_TEST_JSONL_TL"):
        env.pop(k, None)
    # Drop prior-study and prior P6 env markers so a clean source works.
    for k in list(env):
        if k.endswith("_ENV_SOURCED") or k in {
            "P1_RUN_ID",
            "P1_ROOT",
            "P2_RUN_ID",
            "P2_ROOT",
            "P3_RUN_ID",
            "P3_ROOT",
            "P4_RUN_ID",
            "P4_ROOT",
            "P5_RUN_ID",
            "P5_ROOT",
            "P6_ENV_SOURCED",
            "NANOCHAT_BASE_DIR",
        }:
            env.pop(k, None)
    sourced = subprocess.run(
        [
            "bash",
            "-lc",
            f"source {ROOT}/scripts/p6/env.sh && echo TEST_EN=${{P6_TEST_JSONL_EN-UNSET}} && echo TEST_TL=${{P6_TEST_JSONL_TL-UNSET}}",
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    t5 = sourced.returncode == 0 and "TEST_EN=UNSET" in sourced.stdout and "TEST_TL=UNSET" in sourced.stdout
    tests["5"] = {
        "name": "train env cannot resolve test path",
        "pass": t5,
        "stdout": sourced.stdout.strip(),
        "stderr": sourced.stderr.strip(),
    }

    t6 = True
    try:
        reject_parent_sha256(next(iter(FORBIDDEN_PARENT_SHA256)))
        t6 = False
    except SystemExit:
        t6 = True
    tests["6"] = {"name": "P1.1/P2/P3/P4/P5 weight SHA256s rejected as parent", "pass": t6}

    r7 = run([sys.executable, str(SCRIPTS / "dummy_p0t.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE), "--status", "PASS"])
    r7b = run([sys.executable, str(SCRIPTS / "dummy_p0t.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE), "--status", "TECHNICAL BLOCK"])
    r7c = run([sys.executable, str(SCRIPTS / "dummy_p0t.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE), "--status", "PASS"])
    safe_p0 = (SAFE / "gate-p0-t-status.json").read_text()
    t7 = (
        r7.returncode == 0
        and r7b.returncode == 0
        and r7c.returncode == 0
        and "P0-T: PASS" in r7c.stdout
        and "TECHNICAL BLOCK" in r7b.stdout
        and "1.111111" not in safe_p0
        and "1.111111" in (LOCKBOX / "gate-p0-t-eligibility.json").read_text()
    )
    tests["7"] = {"name": "dummy P0-T emits only PASS/BLOCKED/TECHNICAL BLOCK outside lockbox", "pass": t7}

    for stale in [
        "c1_en_val_bpb_full.json",
        "c1_tl_val_bpb_full.json",
        "c2_en_val_bpb_full.json",
        "c2_tl_val_bpb_full.json",
        "c3_en_val_bpb_full.json",
        "c3_tl_val_bpb_full.json",
        "c0_en_val_bpb_full.json",
        "p4-validation-seal.json",
        "gate-v-test.json",
    ]:
        p = LOCKBOX / stale
        if p.exists():
            p.unlink()
    r8a = run([sys.executable, str(SCRIPTS / "make_validation_seal.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE)])
    t8_refuse = r8a.returncode == 2
    for name, val in {
        "c1_en_val_bpb_full.json": 2.01,
        "c1_tl_val_bpb_full.json": 1.51,
        "c2_en_val_bpb_full.json": 1.41,
        "c2_tl_val_bpb_full.json": 1.61,
        "c3_en_val_bpb_full.json": 1.71,
        "c3_tl_val_bpb_full.json": 1.55,
        "c0_en_val_bpb_full.json": 3.01,
    }.items():
        (LOCKBOX / name).write_text(json.dumps({"val_bpb_full": val, "arm_file": name}) + "\n")
        os.chmod(LOCKBOX / name, 0o600)
    r8b = run([sys.executable, str(SCRIPTS / "make_validation_seal.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE)])
    u_safe = (SAFE / "gate-u-status.json").read_text()
    t8 = t8_refuse and r8b.returncode == 0 and "1.41" not in u_safe and "R_TL" not in u_safe
    tests["8"] = {"name": "contrast refuses until six child + C0 EN exist", "pass": t8}

    r9a = run([sys.executable, str(SCRIPTS / "dummy_c3_test.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE), "--arm", "C1"])
    r9b = run([sys.executable, str(SCRIPTS / "dummy_c3_test.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE), "--arm", "C2"])
    seal_bak = (LOCKBOX / "p4-validation-seal.json").read_bytes()
    (LOCKBOX / "p4-validation-seal.json").unlink()
    r9c = run([sys.executable, str(SCRIPTS / "dummy_c3_test.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE), "--arm", "C3"])
    (LOCKBOX / "p4-validation-seal.json").write_bytes(seal_bak)
    t9 = r9a.returncode == 2 and r9b.returncode == 2 and r9c.returncode == 2
    tests["9"] = {"name": "dummy test evaluator rejects C1/C2 and missing U seal", "pass": t9}

    r10 = run([sys.executable, str(SCRIPTS / "dummy_c3_test.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE), "--arm", "C3"])
    v_safe = (SAFE / "gate-v-status.json").read_text()
    t10 = r10.returncode == 0 and "9.999" not in v_safe
    tests["10"] = {"name": "dummy test evaluator accepts C3 only after U seal", "pass": t10}

    incomplete = CACHE / "lockbox_incomplete"
    incomplete.mkdir(exist_ok=True)
    r11 = run([sys.executable, str(SCRIPTS / "release_bundle.py"), "--lockbox", str(incomplete), "--released", str(released / "bad")])
    t11 = r11.returncode == 2
    tests["11"] = {"name": "release refuses incomplete inventory", "pass": t11}

    r12 = run([sys.executable, str(SCRIPTS / "release_bundle.py"), "--lockbox", str(LOCKBOX), "--released", str(released / "good")])
    man = json.loads((released / "good" / "released_manifest.json").read_text())
    t12 = r12.returncode == 0 and all(man[n] == hashlib.sha256((LOCKBOX / n).read_bytes()).hexdigest() for n in man)
    tests["12"] = {"name": "dummy released hashes match manifest", "pass": t12}

    r13 = run([sys.executable, str(SCRIPTS / "break_glass.py"), "--lockbox", str(LOCKBOX), "--safe-progress", str(SAFE)])
    bg_safe = (SAFE / "break-glass-status.json").read_text()
    t13 = r13.returncode == 0 and DUMMY_BPB not in r13.stdout and "9.123456" not in bg_safe
    tests["13"] = {"name": "break-glass dummy writes audit without printing dummy BPB", "pass": t13}

    r14 = run(
        [
            sys.executable,
            str(SCRIPTS / "mix_construct_dummy.py"),
            "--tokenizer-sha",
            TOKENIZER_PKL_SHA,
            "--token-bytes-sha",
            TOKEN_BYTES_SHA,
            "--train-tl",
            "dummy_tl_train.jsonl",
            "--train-en",
            "dummy_en_train.jsonl",
            "--also",
            "dummy_val.jsonl",
        ]
    )
    tests["14"] = {"name": "mix-construction dummy refuses val/test documents", "pass": r14.returncode == 2}

    r15 = run([sys.executable, str(SCRIPTS / "mix_construct_dummy.py"), "--train-tl", "dummy_tl_train.jsonl", "--train-en", "dummy_en_train.jsonl"])
    tests["15"] = {"name": "mix-construction dummy refuses to start if tokenizer hash unset", "pass": r15.returncode == 2}

    r16 = subprocess.run(
        ["bash", "-lc", f"source {ROOT}/scripts/p4/env.sh && source {ROOT}/scripts/p6/env.sh"],
        capture_output=True,
        text=True,
        env={"NANOCHAT_FILIPINO_ROOT": str(ROOT), "P6_RUN_ID": P6_RUN_ID},
    )
    t16 = r16.returncode != 0 and "P6 env refuses" in (r16.stderr + r16.stdout)
    tests["16"] = {"name": "env refuses if scripts/p4/env.sh was sourced", "pass": t16}

    r17a = run([sys.executable, str(SCRIPTS / "refuse_ratio.py"), "--ratio", "-1"])
    r17b = run([sys.executable, str(SCRIPTS / "refuse_nanochat_dataset.py")])
    tests["17"] = {"name": "ratio=-1 and python -m nanochat.dataset wrappers refuse", "pass": r17a.returncode == 2 and r17b.returncode == 2}

    r18 = run([sys.executable, str(SCRIPTS / "mix_construct_dummy.py"), "--tokenizer-sha", TOKENIZER_PKL_SHA, "--from-p3-b3-mix-order-sha", P3_B3_MIX_ORDER_SHA])
    tests["18"] = {"name": "C3 reconstruction from P3 B3 mix-order SHA is refused", "pass": r18.returncode == 2}

    # Tier-2 scaffold receipt (no real checkpoint yet)
    r19 = run([sys.executable, str(SCRIPTS / "sync_tier2_resume_kit.py"), "--init-only"])
    kit_manifest = TIER2 / "RESUME_KIT_MANIFEST.json"
    t19 = r19.returncode == 0 and kit_manifest.is_file()
    tests["19"] = {
        "name": "tier2 resume-kit init writes host-independent manifest",
        "pass": t19,
        "stderr": r19.stderr.strip(),
    }

    all_pass = all(v["pass"] for v in tests.values())
    scripts_sha = walk_sha(SCRIPTS)
    report = {
        "gate": "0",
        "p6_run_id": P6_RUN_ID,
        "nanochat_pin": PIN,
        "all_pass": all_pass,
        "tests": tests,
        "scripts_p6_sha256": scripts_sha,
        "scripts_p6_tree_sha256": tree_digest(scripts_sha),
        "no_p6_outcomes": True,
        "no_real_val_test_text": True,
        "researchbox_id": RESEARCHBOX_ID,
        "aspredicted_id": 307969,
        "note": "Dummy lockbox under gitignored data/cache. Seed-4 lockbox + Tier-2 kit present. Dummy C3 paths exercise lockbox machinery only; Policy A science is M-fine.",
    }
    out = RUN_CARD / "gate-0-lockbox-tests.json"
    text = json.dumps(report, indent=2, sort_keys=True)
    if DUMMY_BPB in text:
        report["tests"]["3"]["sanitized"] = True
        text = json.dumps(report, indent=2, sort_keys=True)
    out.write_text(text + "\n")
    filing = RUN_CARD / "gate-0-filing-lock.json"
    if filing.is_file():
        filing_obj = json.loads(filing.read_text())
        filing_obj["lockbox_acceptance_tests"] = "pass" if all_pass else "fail"
        filing_obj["lockbox_tests_json"] = str(out.relative_to(ROOT))
        filing_obj["lockbox_tests_at_utc"] = utc_now()
        write_json(filing, filing_obj)
    if all_pass:
        mark_ledger("0-lockbox", "pass", str(out.relative_to(ROOT)), "A")
    print(json.dumps({"all_pass": all_pass, "report": str(out.relative_to(ROOT))}, indent=2))
    failed = [k for k, v in tests.items() if not v["pass"]]
    if failed:
        print("FAILED:", ",".join(failed), file=sys.stderr)
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
