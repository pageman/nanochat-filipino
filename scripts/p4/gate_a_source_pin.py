#!/usr/bin/env python3
"""P4 Gate A: pin nanochat, isolated cache, official evaluator copy. Blinded."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    LOCKBOX,
    LOCK_PATH,
    P4_RUN_ID,
    PIN,
    RESEARCHBOX_ID,
    RESEARCHBOX_URL,
    ROOT,
    RUN_CARD,
    SAFE,
    VENDOR,
    blinded_print,
    freeze_file,
    mark_ledger,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-a-source-pin.json"
SENTINEL = BASE / "SENTINEL_P4_ONLY"
P3_EVAL = ROOT / "scripts" / "p3" / "evaluate_bpb.py"
P4_EVAL = ROOT / "scripts" / "p4" / "evaluate_bpb.py"
HUB = ROOT / "docs" / "hub" / "p4-token-share-mix" / "README.md"
PATCH = ROOT / "patches" / "nanochat-NANOCHAT_DATA_DIR.patch"


def git(*args: str, must_succeed: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if must_succeed and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return (proc.stdout or "").strip()


def copy_evaluator() -> str:
    src = P3_EVAL.read_text(encoding="utf-8")
    formula_ok = "def evaluate_bpb_components" in src and "nats / (math.log(2) * nbytes)" in src
    if not formula_ok:
        raise SystemExit("P3 evaluator missing frozen BPB formula")
    dst = src.replace("from p3_common import", "from p4_common import")
    dst = dst.replace("P3_RUN_ID", "P4_RUN_ID")
    dst = dst.replace("ROOT as P3_ROOT", "ROOT")
    dst = dst.replace("P3_ROOT", "ROOT")
    dst = dst.replace("NANOCHAT-FILIPINO-P3-TL-EN", "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE")
    dst = dst.replace("p3-tl0-d8", "p4-tl0-d8")
    dst = dst.replace("p3-tl0-d20", "p4-tl0-d20")
    dst = dst.replace('TOKENIZER_SHA = EXPECTED["p11_tok"]', "TOKENIZER_SHA = TOKENIZER_PKL_SHA")
    dst = dst.replace("TL_TEST", "TL_TEST_JSONL")
    dst = dst.replace("scripts/p3/", "scripts/p4/")
    dst = dst.replace(
        "    TL_DIR,\n",
        "    C1_DIR as TL_DIR,\n    TOKENIZER_PKL_SHA,\n",
    )
    dst = dst.replace(
        "All scalar BPB output goes to --out-dir (lockbox). Operator must redirect stdout.",
        "P4 copy of the P3 evaluator. MUST NOT change the BPB formula. Scalars go to --out-dir (lockbox).",
    )
    if P4_EVAL.exists():
        P4_EVAL.chmod(0o644)
    P4_EVAL.write_text(dst, encoding="utf-8")
    if "nats / (math.log(2) * nbytes)" not in dst:
        raise SystemExit("evaluator copy lost BPB formula")
    if "P3_RUN_ID" in dst or "p3-tl0-d20" in dst:
        raise SystemExit("evaluator copy still has P3 run-id constants")
    return sha256_file(P4_EVAL)


def write_hub_stub() -> None:
    HUB.parent.mkdir(parents=True, exist_ok=True)
    HUB.write_text(
        """# nanochat-filipino P4 (token-share mix)

Hub card **stub**. No weights uploaded. No confirmatory scalars. No outcome table.

P4 is a new study after a fresh Tagalog parent. C3 is a newly constructed token-share mixture. C3 is not P3 B3.

Do not upload onto P1.1, P2, or P3 Hub repositories. Do not Make Public ResearchBox files from this stub.

Weights, tokenizer, and evaluation JSON are added only after Gate W / release plan.
""",
        encoding="utf-8",
    )


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    head = git("rev-parse", "HEAD") if VENDOR.is_dir() else None
    record("A1_pin_checkout", head == PIN, {"head": head, "expected": PIN})

    allowed_diff = ""
    disallowed = []
    if VENDOR.is_dir():
        stat = git("diff", "--stat", PIN, must_succeed=False)
        allowed_diff = git("diff", PIN, "--", "nanochat/dataset.py", "nanochat/common.py", must_succeed=False)
        full_names = git("diff", "--name-only", PIN, must_succeed=False).splitlines()
        allowed_names = {"nanochat/dataset.py", "nanochat/common.py"}
        disallowed = [n for n in full_names if n and n not in allowed_names]
    dataset_py = VENDOR / "nanochat" / "dataset.py"
    hook_present = dataset_py.is_file() and "NANOCHAT_DATA_DIR" in dataset_py.read_text(encoding="utf-8")
    record(
        "A2_allowed_diff_only_data_hook",
        disallowed == [] and hook_present and "flash_attention" not in allowed_diff,
        {
            "patch_sha256": sha256_file(PATCH) if PATCH.is_file() else None,
            "diff_chars": len(allowed_diff),
            "disallowed": disallowed,
            "hook_present": hook_present,
        },
    )

    BASE.mkdir(parents=True, exist_ok=True)
    SAFE.mkdir(parents=True, exist_ok=True)
    LOCKBOX.mkdir(parents=True, exist_ok=True)
    SENTINEL.write_text(
        f"p4_run_id={P4_RUN_ID}\npin={PIN}\naspredicted={ASPREDICTED_ID}\nresearchbox={RESEARCHBOX_ID}\nutc={utc_now()}\n",
        encoding="utf-8",
    )
    record("A3_sentinel", SENTINEL.is_file(), str(SENTINEL.relative_to(ROOT)))

    env_p4 = (ROOT / "scripts/p4/env.sh").read_text(encoding="utf-8")
    record(
        "A4_base_dir_is_p4_cache",
        f"data/cache/${{P4_RUN_ID}}" in env_p4 or P4_RUN_ID in env_p4,
        {"NANOCHAT_BASE_DIR": os.environ.get("NANOCHAT_BASE_DIR")},
    )
    record(
        "A5_p4_env_not_prior_copy",
        "P3_RUN_ID" in env_p4 and "MUST NOT" in env_p4 and "scripts/p3/env.sh" in env_p4,
        True,
    )
    record(
        "A6_env_scan_no_prior_cache",
        not str(os.environ.get("NANOCHAT_BASE_DIR", "")).endswith(tuple(["p1-", "p2-", "p3-"]))
        and "p3-" not in str(os.environ.get("NANOCHAT_BASE_DIR", "")).split("cache/")[-1]
        and os.environ.get("P3_RUN_ID") is None
        and os.environ.get("P2_RUN_ID") is None
        and os.environ.get("P1_RUN_ID") is None
        and os.environ.get("NANOCHAT_DATA_DIR") in (None, ""),
        {
            "NANOCHAT_BASE_DIR": os.environ.get("NANOCHAT_BASE_DIR"),
            "NANOCHAT_DATA_DIR": os.environ.get("NANOCHAT_DATA_DIR"),
        },
    )
    p4_ckpts = list(BASE.glob("**/*.pt"))
    record("A7_no_checkpoints_in_p4_cache", p4_ckpts == [], [str(p) for p in p4_ckpts])

    eval_sha = copy_evaluator()
    record("A8_evaluator_copied_formula_frozen", P4_EVAL.is_file() and "evaluate_bpb_components" in P4_EVAL.read_text(), eval_sha)

    fp = ROOT / "scripts/p4/forbidden_parents.py"
    record("A9_forbidden_parents", fp.is_file(), str(fp.relative_to(ROOT)))

    write_hub_stub()
    hub_text = HUB.read_text(encoding="utf-8")
    record(
        "A10_hub_stub_no_scalars",
        HUB.is_file() and "bpb" not in hub_text.lower() and re.search(r"\d+\.\d{2,}", hub_text) is None,
        str(HUB.relative_to(ROOT)),
    )

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "researchbox_url": RESEARCHBOX_URL,
        "gate": "A",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "script": "scripts/p4/gate_a_source_pin.py",
        "nanochat_pin": PIN,
        "nanochat_head": head,
        "allowed_diff_sha256": hashlib.sha256(allowed_diff.encode()).hexdigest() if allowed_diff else None,
        "sentinel": str(SENTINEL.relative_to(ROOT)),
        "evaluator_sha256": eval_sha,
        "checks": checks,
        "no_p4_outcomes": True,
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
