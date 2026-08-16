#!/usr/bin/env python3
"""Mac MPS one-step Gate I infrastructure dry runs. Not confirmatory."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

from nanochat.gpt import GPT, GPTConfig  # noqa: E402

BUDGET = json.loads((ROOT / "manifests" / "budget_manifest.json").read_text(encoding="utf-8"))
RUN_ID = BUDGET["run_id"]
PYTHON = VENDOR / ".venv" / "bin" / "python"
LOG_DIR = ROOT / "artifacts" / "p1" / RUN_ID / "m4_mps_gatei_preflight"
DEPTHS = (8, 12, 16, 20)
ASPECT_RATIO = 64
HEAD_DIM = 128


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def instantiate(depth: int, vocab_size: int = 32768) -> dict:
    base_dim = depth * ASPECT_RATIO
    model_dim = ((base_dim + HEAD_DIM - 1) // HEAD_DIM) * HEAD_DIM
    num_heads = model_dim // HEAD_DIM
    expected = next(r for r in BUDGET["depth_details"] if r["depth"] == depth)
    with torch.device("meta"):
        model = GPT(
            GPTConfig(
                sequence_len=2048,
                vocab_size=vocab_size,
                n_layer=depth,
                n_head=num_heads,
                n_kv_head=num_heads,
                n_embd=model_dim,
                window_pattern="SSSL",
            )
        )
        counts = model.num_scaling_params()
    ok = (
        int(counts["total"]) == expected["p_total"]
        and model.config.sequence_len == 2048
        and model.config.n_embd == expected["n_embd"]
    )
    return {
        "depth": depth,
        "ok": ok,
        "n_embd": model.config.n_embd,
        "n_head": model.config.n_head,
        "sequence_len": model.config.sequence_len,
        "p_total": int(counts["total"]),
        "matches_budget": ok,
    }


def run_one(depth: int) -> dict:
    rec = next(r for r in BUDGET["depths"] if r["depth"] == depth)
    tag = f"p1-m4-mps-gatei-preflight-d{depth}"
    log_path = LOG_DIR / f"d{depth}_base_train.log"
    env = os.environ.copy()
    env["NANOCHAT_BASE_DIR"] = str(ROOT / "data" / "cache" / RUN_ID)
    env["NANOCHAT_DATA_DIR"] = str(ROOT / "data" / "processed" / "wikitext-tl39" / "active")
    env.pop("PYTORCH_ENABLE_MPS_FALLBACK", None)
    env["OMP_NUM_THREADS"] = "1"
    env["WANDB_RUN"] = "dummy"
    cmd = [
        str(PYTHON),
        "-m",
        "scripts.base_train",
        "--device-type=mps",
        f"--depth={depth}",
        "--max-seq-len=2048",
        "--device-batch-size=1",
        "--total-batch-size=2048",
        "--num-iterations=1",
        f"--target-param-data-ratio={rec['target_param_data_ratio']}",
        "--eval-every=-1",
        "--eval-tokens=2048",
        "--core-metric-every=-1",
        "--sample-every=-1",
        "--save-every=1",
        "--warmup-steps=1",
        "--run=dummy",
        f"--model-tag={tag}",
    ]
    started = utc_now()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(VENDOR),
            env=env,
            capture_output=True,
            text=True,
            timeout=1800,
        )
    except subprocess.TimeoutExpired:
        return {
            "depth": depth,
            "model_tag": tag,
            "status": "timeout",
            "confirmatory_eligible": False,
            "started_at_utc": started,
            "ended_at_utc": utc_now(),
        }
    log_path.write_text(proc.stdout + "\n" + proc.stderr, encoding="utf-8")
    oom = "out of memory" in (proc.stdout + proc.stderr).lower() or proc.returncode == 137
    ckpt = ROOT / "data" / "cache" / RUN_ID / "base_checkpoints" / tag / "model_000001.pt"
    result = {
        "depth": depth,
        "model_tag": tag,
        "status": "pass" if proc.returncode == 0 and ckpt.is_file() else ("oom" if oom else "fail"),
        "returncode": proc.returncode,
        "checkpoint_written": ckpt.is_file(),
        "oom": oom,
        "t_shrunk": False,
        "confirmatory_eligible": False,
        "platform": "macos-mps",
        "purpose": "gate_i_infrastructure_preflight",
        "started_at_utc": started,
        "ended_at_utc": utc_now(),
        "log": str(log_path.relative_to(ROOT)),
        "train_loss_finite": None,
        "reload_finite": None,
    }
    if proc.returncode == 0:
        result["train_loss_finite"] = "loss:" in proc.stdout and "nan" not in proc.stdout.lower()
        reload = subprocess.run(
            [
                str(PYTHON),
                str(ROOT / "scripts" / "p1" / "check_checkpoint_finite.py"),
                "--model-tag",
                tag,
                "--step",
                "1",
                "--device-type",
                "mps",
                "--seq-len",
                "2048",
            ],
            cwd=str(VENDOR),
            env=env,
            capture_output=True,
            text=True,
            timeout=600,
        )
        (LOG_DIR / f"d{depth}_reload.json").write_text(reload.stdout or reload.stderr, encoding="utf-8")
        try:
            payload = json.loads(reload.stdout)
            result["reload_finite"] = bool(payload.get("finite"))
            result["reload_numeric_redacted"] = True
        except json.JSONDecodeError:
            result["reload_finite"] = False
            result["reload_error"] = (reload.stderr or reload.stdout)[-500:]
        if not result["reload_finite"]:
            result["status"] = "fail"
    return result


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    inst = [instantiate(d) for d in DEPTHS]
    dry = []
    for depth in DEPTHS:
        dry.append(run_one(depth))
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "label": "p1-m4-mps-gatei-preflight",
        "platform": "macos-mps",
        "purpose": "gate_i_infrastructure_preflight",
        "confirmatory_eligible": False,
        "official_gate_h": "not_started",
        "official_gate_i_started": False,
        "checked_at_utc": utc_now(),
        "instantiation": inst,
        "dry_runs": dry,
        "comparison_performed": False,
        "d_star_selected": False,
        "test_read": False,
        "note": "Finite/non-finite only. Do not rank these depths. Do not copy into the confirmatory table.",
    }
    out = ROOT / "manifests" / "mac_mps_gatei_preflight.json"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    inst_ok = all(row["ok"] for row in inst)
    hard_fail = any(row["status"] in {"fail", "timeout"} for row in dry)
    return 0 if inst_ok and not hard_fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
