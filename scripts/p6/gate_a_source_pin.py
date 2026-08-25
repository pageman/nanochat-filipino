#!/usr/bin/env python3
"""P6 Gate A: pin nanochat, isolated cache, P6 evaluator, seed-knob, release skeleton."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    CHILD_ARMS,
    FILED_EVALUATOR_SHA,
    LOCK_PATH,
    P6_RUN_ID,
    PARENT_SEED,
    PIN,
    ROOT,
    RUN_CARD,
    TOPOLOGY_ARMS,
    VENDOR,
    blinded_print,
    mark_ledger,
    seed_lockbox_dirs,
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-a-source-pin.json"
SENTINEL = BASE / "SENTINEL_P6_ONLY"
P6_EVAL = ROOT / "scripts" / "p6" / "evaluate_bpb.py"
P4_EVAL_SRC = ROOT / "scripts" / "p4" / "evaluate_bpb.py"
RELEASE = ROOT / "docs" / "hub" / "p6-m-schedule-topology" / "RELEASE_MANIFEST.json"
SKILL_REG = ROOT / "manifests" / "p6" / "p6_gate_skill_registry.json"
SEED_PROOF = RUN_CARD / "seed-knob-proof.json"


def git(*args: str, must_succeed: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if must_succeed and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return (proc.stdout or "").strip()


def sync_evaluator() -> str:
    src = P4_EVAL_SRC.read_text(encoding="utf-8")
    dst = src.replace("from p4_common import", "from p6_common import")
    dst = dst.replace("P4_RUN_ID", "P6_RUN_ID")
    dst = dst.replace("scripts/p4/", "scripts/p6/")
    dst = dst.replace("NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE", "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY")
    dst = dst.replace("p4-", "p6-")
    if "nats / (math.log(2) * nbytes)" not in dst:
        raise SystemExit("evaluator missing frozen BPB formula")
    P6_EVAL.parent.mkdir(parents=True, exist_ok=True)
    P6_EVAL.write_text(dst, encoding="utf-8")
    return sha256_file(P6_EVAL)


def write_release_skeleton() -> None:
    entries = {
        "c0": {"role": "parent", "path_pending": True, "sha256": None},
        "c1": {"role": "child", "path_pending": True, "sha256": None},
        "c2": {"role": "child", "path_pending": True, "sha256": None},
    }
    for arm in TOPOLOGY_ARMS:
        entries[arm] = {"role": "topology_child", "path_pending": True, "sha256": None}
    entries["tokenizer.pkl"] = {"role": "tokenizer", "path_pending": True, "sha256": None}
    entries["token_bytes.pt"] = {"role": "tokenizer", "path_pending": True, "sha256": None}
    payload = {
        "study": "P6-M",
        "p6_run_id": P6_RUN_ID,
        "expected_weightish_object_count": 9,
        "logical_keys": list(entries.keys()),
        "entries": entries,
        "note": "Hashes filled as objects are produced; never add unplanned objects after outcome access.",
        "created_utc": utc_now(),
    }
    write_json(RELEASE, payload)


def write_skill_registry() -> None:
    gates = {
        "0": {"skills": ["nanochat-gate-spine", "nanochat-lockbox-blinding", "nanochat-study-identity"], "script": "scripts/p6/gate0_accept.py", "host": "laptop"},
        "A": {"skills": ["nanochat-new-study-from-prior", "nanochat-study-identity", "nanochat-bpb-eval"], "script": "scripts/p6/gate_a_source_pin.py", "host": "laptop"},
        "B": {"skills": ["nanochat-study-identity", "nanochat-mix-identity", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_b_raw_assets.py", "host": "laptop"},
        "C": {"skills": ["nanochat-study-identity", "nanochat-mix-identity", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_c_hygiene.py", "host": "laptop"},
        "D": {"skills": ["nanochat-study-identity", "nanochat-mix-identity", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_d_split_freeze.py", "host": "laptop"},
        "F": {"skills": ["nanochat-bpb-eval", "nanochat-study-identity"], "script": "scripts/p6/gate_f_tokenizer.py", "host": "laptop"},
        "E": {"skills": ["nanochat-mix-identity"], "script": "scripts/p6/gate_e_streams.py", "host": "laptop"},
        "G": {"skills": ["nanochat-gate-spine", "nanochat-bpb-eval", "nanochat-frozen-parent-continue", "nanochat-runpod-study-pod"], "script": "scripts/p6/gate_g_budget.py", "host": "laptop"},
        "H": {"skills": ["nanochat-runpod-study-pod"], "script": "scripts/p6/gate_h_smoke.sh", "host": "gpu"},
        "I": {"skills": ["nanochat-runpod-study-pod", "nanochat-study-identity", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_i_tl0.sh", "host": "gpu"},
        "P0-T": {"skills": ["nanochat-bpb-eval", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_p0t.sh", "host": "gpu"},
        "Q": {"skills": ["nanochat-frozen-parent-continue"], "script": "scripts/p6/gate_q_c0_freeze.py", "host": "cpu"},
        "R": {"skills": ["nanochat-frozen-parent-continue", "nanochat-runpod-study-pod", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_r_c1.sh", "host": "gpu"},
        "S": {"skills": ["nanochat-frozen-parent-continue", "nanochat-runpod-study-pod", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_s_c2.sh", "host": "gpu"},
        "T1-T4": {"skills": ["nanochat-frozen-parent-continue", "nanochat-mix-identity", "nanochat-runpod-study-pod", "nanochat-lockbox-blinding"], "script": "scripts/p6/gate_t_topology.sh", "host": "gpu"},
        "U": {"skills": ["nanochat-bpb-eval", "nanochat-lockbox-blinding", "nanochat-gate-spine"], "script": "scripts/p6/gate_u_seal.py", "host": "gpu"},
        "V": {"skills": ["nanochat-c3-only-test"], "script": "scripts/p6/gate_v_c3_test.py", "host": "gpu"},
        "X": {"skills": ["nanochat-lockbox-blinding", "nanochat-panel-count", "nanochat-paper-lock-build", "nanochat-gate-spine"], "script": "scripts/p6/gate_x_unblind.py", "host": "laptop"},
        "W": {"skills": ["nanochat-paper-lock-build", "nanochat-closeout-archive", "nanochat-deposit-split", "nanochat-hub-weights", "nanochat-researchbox-bingo"], "script": "scripts/p6/gate_w_closeout.py", "host": "laptop"},
    }
    write_json(
        SKILL_REG,
        {
            "study": "P6-M",
            "p6_run_id": P6_RUN_ID,
            "gates": gates,
            "created_utc": utc_now(),
        },
    )


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    RUN_CARD.mkdir(parents=True, exist_ok=True)
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
        f"p6_run_id={P6_RUN_ID}\npin={PIN}\naspredicted={ASPREDICTED_ID}\nparent_seed={PARENT_SEED}\nutc={utc_now()}\n",
        encoding="utf-8",
    )
    record("A3_sentinel", SENTINEL.is_file(), str(SENTINEL.relative_to(ROOT)))

    env_p6 = (ROOT / "scripts/p6/env.sh").read_text(encoding="utf-8")
    record("A4_base_dir_is_p6_cache", "data/cache/${P6_RUN_ID}" in env_p6, True)
    record("A5_p6_env_refuses_prior", "MUST NOT" in env_p6 and "P5_RUN_ID" in env_p6, True)
    record(
        "A6_env_scan_no_prior_cache",
        not any(x in str(os.environ.get("NANOCHAT_BASE_DIR", "")) for x in ("/p1-", "/p2-", "/p3-", "/p4-", "/p5-"))
        and os.environ.get("P4_RUN_ID") is None
        and os.environ.get("P5_RUN_ID") is None,
        {"NANOCHAT_BASE_DIR": os.environ.get("NANOCHAT_BASE_DIR")},
    )
    p6_ckpts = list(BASE.glob("**/*.pt"))
    record("A7_no_checkpoints_in_p6_cache", p6_ckpts == [], [str(p) for p in p6_ckpts])

    eval_sha = sync_evaluator()
    # Formula identity: same BPB expression as filed P4/P5 evaluator; file SHA differs after p6 renames.
    formula_ok = "nats / (math.log(2) * nbytes)" in P6_EVAL.read_text(encoding="utf-8")
    record("A8_evaluator_formula_frozen", formula_ok and P6_EVAL.is_file(), {"sha256": eval_sha, "p5_official_reference": FILED_EVALUATOR_SHA})

    fp = ROOT / "scripts/p6/forbidden_parents.py"
    record("A9_forbidden_parents", fp.is_file(), str(fp.relative_to(ROOT)))

    # Write seed proof to P6 run-card
    prove = ROOT / "scripts" / "p6" / "prove_parent_seed_knob.py"
    # Patch output path via env
    env = os.environ.copy()
    env["P6_RUN_ID"] = P6_RUN_ID
    env["NANOCHAT_FILIPINO_ROOT"] = str(ROOT)
    proc = subprocess.run([sys.executable, str(prove)], capture_output=True, text=True, env=env, cwd=str(ROOT))
    knob = {}
    if proc.stdout.strip():
        try:
            knob = json.loads(proc.stdout.strip().splitlines()[-1])
        except json.JSONDecodeError:
            knob = {"raw": proc.stdout[-500:]}
    # Also compare seed-4 vs forbidden panel seeds 1/2/3 if proof wrote rows
    record("A10_seed_knob_proof", proc.returncode == 0 and knob.get("distinct") is True, knob)

    write_release_skeleton()
    write_skill_registry()
    record("A11_release_manifest_skeleton", RELEASE.is_file() and len(json.loads(RELEASE.read_text())["logical_keys"]) == 9, str(RELEASE.relative_to(ROOT)))
    record("A12_skill_registry", SKILL_REG.is_file(), str(SKILL_REG.relative_to(ROOT)))

    validator = ROOT / "scripts" / "validate_p6m_cursor_skills.mjs"
    if validator.is_file():
        vproc = subprocess.run(["node", str(validator)], capture_output=True, text=True, cwd=str(ROOT))
        record("A13_skill_validator", vproc.returncode == 0, {"returncode": vproc.returncode, "stdout_tail": vproc.stdout[-300:]})
    else:
        record("A13_skill_validator", False, "missing validator")

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "gate": "A",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "script": "scripts/p6/gate_a_source_pin.py",
        "nanochat_pin": PIN,
        "parent_seed": PARENT_SEED,
        "child_arms": list(CHILD_ARMS),
        "evaluator_sha256": eval_sha,
        "release_manifest": str(RELEASE.relative_to(ROOT)),
        "skill_registry": str(SKILL_REG.relative_to(ROOT)),
        "checks": checks,
        "no_p6_outcomes": True,
        "next_gate": "B",
    }
    write_json(OUT, payload)
    if ok:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["A"] = "pass"
        lock["evaluate_bpb_official_sha256"] = eval_sha
        lock["evaluate_bpb_sha_note"] = "P6 file SHA after p6 rename; BPB formula unchanged from P4/P5"
        lock["status"] = "gate_a_pass"
        write_json(LOCK_PATH, lock)
        mark_ledger("A", "pass", str(OUT.relative_to(ROOT)), "B")
    blinded_print("A", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
