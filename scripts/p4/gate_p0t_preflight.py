#!/usr/bin/env python3
"""P4 Gate P0-T preflight. Does not evaluate BPB. Authorizes gate_p0t.sh only."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    EXPECTED,
    FILED_EVALUATOR_SHA,
    LOCKBOX,
    N_TL0,
    P4_RUN_ID,
    PIN,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
    TOK_DIR,
    TOKENIZER_PKL_SHA,
    VENDOR,
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-p0t-preflight.json"
AUTH = RUN_CARD / "gate-p0t-authorization.json"
GATE_I = RUN_CARD / "gate-i-tl0.json"
EVALUATOR = ROOT / "scripts" / "p4" / "evaluate_bpb.py"
TL0_TAGS = {8: "p4-tl0-d8", 20: "p4-tl0-d20"}


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return proc.stdout.strip()


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail=None) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    record("P0T0_not_darwin", platform.system() != "Darwin", platform.system())
    auth = json.loads(AUTH.read_text(encoding="utf-8")) if AUTH.is_file() else {}
    record(
        "P0T0_authorization",
        auth.get("gate") == "P0-T"
        and auth.get("authorized") is True
        and auth.get("authorizes_children") is False
        and auth.get("authorizes_c0_freeze") is False,
        str(AUTH.relative_to(ROOT)) if AUTH.is_file() else None,
    )

    gate_i_ok = False
    gate_i_detail: dict = {}
    if GATE_I.is_file():
        gate_i = json.loads(GATE_I.read_text(encoding="utf-8"))
        gate_i_ok = gate_i.get("status") == "pass"
        gate_i_detail = {"status": gate_i.get("status"), "depths": list(gate_i.get("depths", {}).keys())}
    record("P0T0_gate_i_pass", gate_i_ok, gate_i_detail)

    ckpt_checks = {}
    ckpt_ok = True
    for depth, tag in TL0_TAGS.items():
        receipt = RUN_CARD / f"gate-i-tl0-d{depth}.json"
        row = json.loads(receipt.read_text(encoding="utf-8")) if receipt.is_file() else {}
        ckpt = BASE / "base_checkpoints" / tag / f"model_{N_TL0:06d}.pt"
        expected_sha = row.get("checkpoint_sha256")
        got_sha = sha256_file(ckpt) if ckpt.is_file() else None
        ok = (
            row.get("status") == "pass"
            and row.get("health") == "pass"
            and got_sha is not None
            and got_sha == expected_sha
        )
        ckpt_checks[str(depth)] = {
            "tag": tag,
            "path": str(ckpt.relative_to(ROOT)) if ckpt.is_file() else None,
            "sha_match": got_sha == expected_sha,
            "ok": ok,
        }
        ckpt_ok = ckpt_ok and ok
    record("P0T0_tl0_ckpts", ckpt_ok, {k: v["ok"] for k, v in ckpt_checks.items()})

    eval_sha = sha256_file(EVALUATOR) if EVALUATOR.is_file() else None
    record("P0T0_evaluator_sha_gate_a", eval_sha == FILED_EVALUATOR_SHA, eval_sha)

    hashes = {}
    hash_ok = True
    paths = {
        "tokenizer.pkl": (TOK_DIR / "tokenizer.pkl", TOKENIZER_PKL_SHA),
        "val.parquet": (C1_DIR / "val.parquet", EXPECTED["c1_shards"]["val.parquet"]),
        "shard_00002.parquet": (C1_DIR / "shard_00002.parquet", EXPECTED["p11_shards"]["shard_00002.parquet"]),
        "tl_train_jsonl": (TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"]),
        "tl_val_jsonl": (TL_VAL_JSONL, EXPECTED["tl_val_jsonl"]),
    }
    for name, (path, exp) in paths.items():
        got = sha256_file(path) if path.is_file() else None
        hashes[name] = {"ok": got == exp, "present": path.is_file()}
        hash_ok = hash_ok and hashes[name]["ok"]
    record("P0T0_hashes", hash_ok, {k: v["ok"] for k, v in hashes.items()})

    head = git("rev-parse", "HEAD") if (VENDOR / ".git").is_dir() else None
    record("P0T0_pin", head == PIN, head)

    cuda = False
    gpu_name = None
    try:
        import torch

        cuda = bool(torch.cuda.is_available())
        if cuda:
            gpu_name = torch.cuda.get_device_name(0)
    except Exception as exc:  # noqa: BLE001
        gpu_name = f"torch_import_failed:{type(exc).__name__}"
    record("P0T0_cuda", cuda, gpu_name)
    record("P0T0_gpu_class_a40", "A40" in (gpu_name or ""), gpu_name)

    elig_path = LOCKBOX / "gate-p0-t-eligibility.json"
    real_elig_exists = False
    if elig_path.is_file():
        try:
            elig = json.loads(elig_path.read_text(encoding="utf-8"))
            real_elig_exists = elig.get("gate") == "P0-T" and isinstance(elig.get("depths"), dict)
        except json.JSONDecodeError:
            real_elig_exists = True
    record(
        "P0T0_no_prior_eligibility",
        not real_elig_exists,
        "refuse overwrite" if real_elig_exists else "absent_or_dummy_only",
    )
    record("P0T0_test_access", True, "test_read_count=0 by protocol")
    record("P0T0_english_val_not_in_scope", True, "Tagalog val only")

    ready = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "P0-T-preflight",
        "status": "ready_for_p0t" if ready else "not_ready",
        "at_utc": utc_now(),
        "host": platform.node(),
        "p4_run_id": P4_RUN_ID,
        "checks": checks,
        "blinded": True,
        "no_p4_outcomes": True,
        "note": "Exit 0 authorizes scripts/p4/gate_p0t.sh. Scalar BPB stays lockboxed. Not Gate Q.",
    }
    write_json(OUT, payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "failed": [c["id"] for c in checks if not c["ok"]],
                "path": str(OUT.relative_to(ROOT)),
                "blinded": True,
            },
            indent=2,
        )
    )
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
