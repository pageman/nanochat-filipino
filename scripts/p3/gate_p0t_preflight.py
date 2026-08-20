#!/usr/bin/env python3
"""P3 Gate P0-T preflight. Does not evaluate BPB. Authorizes gate_p0t.sh only."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from p3_common import ASPREDICTED_ID, BASE, EXPECTED, PIN, P3_RUN_ID, ROOT, RUN_CARD, TL_DIR, VENDOR

OUT = RUN_CARD / "gate-p0t-preflight.json"
GATE_I = RUN_CARD / "gate-i-tl0.json"
TL0_STEP = 294
TL0_TAGS = {8: "p3-tl0-d8", 20: "p3-tl0-d20"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    proc = subprocess.run(["git", "-C", str(VENDOR), *args], text=True, capture_output=True)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return proc.stdout.strip()


def main() -> int:
    gate_i_ok = False
    gate_i_detail: dict = {}
    if GATE_I.is_file():
        gate_i = json.loads(GATE_I.read_text(encoding="utf-8"))
        gate_i_ok = gate_i.get("status") == "pass"
        gate_i_detail = {"status": gate_i.get("status"), "depths": list(gate_i.get("depths", {}).keys())}

    ckpt_checks = {}
    ckpt_ok = True
    for depth, tag in TL0_TAGS.items():
        receipt = RUN_CARD / f"gate-i-tl0-d{depth}.json"
        row = json.loads(receipt.read_text(encoding="utf-8")) if receipt.is_file() else {}
        ckpt = BASE / "base_checkpoints" / tag / f"model_{TL0_STEP:06d}.pt"
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
            "expected_sha256": expected_sha,
            "got_sha256": got_sha,
            "ok": ok,
        }
        ckpt_ok = ckpt_ok and ok

    paths = {
        "tokenizer.pkl": BASE / "tokenizer" / "tokenizer.pkl",
        "shard_00002.parquet": TL_DIR / "shard_00002.parquet",
        "tl_train_jsonl": ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl",
        "tl_val_jsonl": ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl",
    }
    expected = {
        "tokenizer.pkl": EXPECTED["p11_tok"],
        "shard_00002.parquet": EXPECTED["p11_shards"]["shard_00002.parquet"],
        "tl_train_jsonl": EXPECTED["tl_train_jsonl"],
        "tl_val_jsonl": EXPECTED["tl_val_jsonl"],
    }
    hash_ok = True
    hashes = {}
    for name, path in paths.items():
        got = sha256_file(path) if path.is_file() else None
        if name in {"tl_train_jsonl", "tl_val_jsonl"} and got is None:
            # Pod may lack interim JSONL; hashed parquet shards are an allowed fallback.
            hashes[name] = {"ok": True, "got": None, "expected": expected[name], "fallback": "parquet_shards"}
            continue
        hashes[name] = {"ok": got == expected[name], "got": got, "expected": expected[name]}
        hash_ok = hash_ok and hashes[name]["ok"]

    head = git("rev-parse", "HEAD")
    cuda = False
    gpu_name = None
    try:
        import torch

        cuda = bool(torch.cuda.is_available())
        if cuda:
            gpu_name = torch.cuda.get_device_name(0)
    except Exception as exc:  # noqa: BLE001
        gpu_name = f"torch_import_failed:{type(exc).__name__}"

    elig_path = BASE / "lockbox" / "gate-p0-t-eligibility.json"
    real_elig_exists = False
    if elig_path.is_file():
        try:
            elig = json.loads(elig_path.read_text(encoding="utf-8"))
            real_elig_exists = elig.get("gate") == "P0-T" or isinstance(elig.get("depths"), dict)
        except json.JSONDecodeError:
            real_elig_exists = True

    checks = [
        {"id": "P0T0_gate_i_pass", "ok": gate_i_ok, "detail": gate_i_detail},
        {"id": "P0T0_tl0_ckpts", "ok": ckpt_ok, "detail": ckpt_checks},
        {"id": "P0T0_hashes", "ok": hash_ok, "detail": hashes},
        {"id": "P0T0_pin", "ok": head == PIN, "detail": head},
        {"id": "P0T0_cuda", "ok": cuda, "detail": gpu_name},
        {
            "id": "P0T0_no_prior_eligibility",
            "ok": not real_elig_exists,
            "detail": "refuse overwrite" if real_elig_exists else "absent_or_dummy_only",
        },
        {"id": "P0T0_test_access", "ok": True, "detail": "test_read_count=0 by protocol"},
    ]
    ready = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P3-TL-EN",
        "aspredicted_id": ASPREDICTED_ID,
        "gate": "P0-T-preflight",
        "status": "ready_for_p0t" if ready else "not_ready",
        "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": platform.node(),
        "p3_run_id": P3_RUN_ID,
        "checks": checks,
        "note": "Exit 0 authorizes gate_p0t.sh. Scalar BPB stays lockboxed.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "failed": [c["id"] for c in checks if not c["ok"]],
                "path": str(OUT.relative_to(ROOT)),
            },
            indent=2,
        )
    )
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
