#!/usr/bin/env python3
"""P5 Gate A: pin nanochat, isolated cache, P5 evaluator, seed-knob proof. Blinded."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p5_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    LOCK_PATH,
    P5_RUN_ID,
    PIN,
    ROOT,
    RUN_CARD,
    VENDOR,
    blinded_print,
    mark_ledger,
    seed_lockbox_dirs,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-a-source-pin.json"
SENTINEL = BASE / "SENTINEL_P5_ONLY"
P5_EVAL = ROOT / "scripts" / "p5" / "evaluate_bpb.py"
P4_EVAL_SRC = ROOT / "scripts" / "p4" / "evaluate_bpb.py"
PATCH = ROOT / "patches" / "nanochat-NANOCHAT_DATA_DIR.patch"


def git(*args: str, must_succeed: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if must_succeed and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return (proc.stdout or "").strip()


def sync_evaluator() -> str:
    src = P4_EVAL_SRC.read_text(encoding="utf-8")
    dst = src.replace("from p4_common import", "from p5_common import")
    dst = dst.replace("P4_RUN_ID", "P5_RUN_ID")
    dst = dst.replace("scripts/p4/", "scripts/p5/")
    dst = dst.replace("NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE", "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED")
    dst = dst.replace("p4-", "p5-")
    if "nats / (math.log(2) * nbytes)" not in dst:
        raise SystemExit("evaluator missing frozen BPB formula")
    P5_EVAL.write_text(dst, encoding="utf-8")
    return sha256_file(P5_EVAL)


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    head = git("rev-parse", "HEAD")
    record("A1_pin_checkout", head == PIN, {"head": head, "expected": PIN})

    full_names = git("diff", "--name-only", PIN, must_succeed=False).splitlines()
    allowed_names = {"nanochat/dataset.py", "nanochat/common.py"}
    disallowed = [n for n in full_names if n and n not in allowed_names]
    dataset_py = VENDOR / "nanochat" / "dataset.py"
    hook_present = dataset_py.is_file() and "NANOCHAT_DATA_DIR" in dataset_py.read_text(encoding="utf-8")
    record("A2_allowed_diff_only_data_hook", disallowed == [] and hook_present, {"disallowed": disallowed})

    BASE.mkdir(parents=True, exist_ok=True)
    seed_lockbox_dirs()
    SENTINEL.write_text(
        f"p5_run_id={P5_RUN_ID}\npin={PIN}\naspredicted={ASPREDICTED_ID}\nutc={utc_now()}\n",
        encoding="utf-8",
    )
    record("A3_sentinel", SENTINEL.is_file(), str(SENTINEL.relative_to(ROOT)))

    env_p5 = (ROOT / "scripts/p5/env.sh").read_text(encoding="utf-8")
    record("A4_base_dir_is_p5_cache", f"data/cache/${{P5_RUN_ID}}" in env_p5 or P5_RUN_ID in env_p5, True)
    record("A5_p5_env_not_prior_copy", "scripts/p4/env.sh" in env_p5 and "MUST NOT" in env_p5, True)
    record(
        "A6_env_scan_no_prior_cache",
        "p4-" not in str(os.environ.get("NANOCHAT_BASE_DIR", "")).split("cache/")[-1]
        and os.environ.get("P4_RUN_ID") is None,
        {"NANOCHAT_BASE_DIR": os.environ.get("NANOCHAT_BASE_DIR")},
    )
    p5_ckpts = list(BASE.glob("**/*.pt"))
    record("A7_no_checkpoints_in_p5_cache", p5_ckpts == [], [str(p) for p in p5_ckpts])

    eval_sha = sync_evaluator()
    record("A8_evaluator_formula_frozen", P5_EVAL.is_file(), eval_sha)

    fp = ROOT / "scripts/p5/forbidden_parents.py"
    record("A9_forbidden_parents", fp.is_file(), str(fp.relative_to(ROOT)))

    proc = subprocess.run([sys.executable, str(ROOT / "scripts/p5/prove_parent_seed_knob.py")], capture_output=True, text=True)
    knob = json.loads(proc.stdout.strip().splitlines()[-1]) if proc.stdout.strip() else {}
    record("A10_seed_knob_proof", proc.returncode == 0 and knob.get("distinct") is True, knob)

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED",
        "aspredicted_id": ASPREDICTED_ID,
        "gate": "A",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p5_run_id": P5_RUN_ID,
        "script": "scripts/p5/gate_a_source_pin.py",
        "nanochat_pin": PIN,
        "evaluator_sha256": eval_sha,
        "checks": checks,
        "no_p5_outcomes": True,
        "next_gate": "B",
    }
    write_json(OUT, payload)
    if ok:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["A"] = "pass"
        lock["evaluate_bpb_official_sha256"] = eval_sha
        lock["status"] = "gate_a_pass"
        write_json(LOCK_PATH, lock)
        mark_ledger("A", "pass", str(OUT.relative_to(ROOT)), "B")
    blinded_print("A", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
