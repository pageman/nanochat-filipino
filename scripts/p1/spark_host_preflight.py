#!/usr/bin/env python3
"""DGX Spark architecture-aware CUDA preflight. Does not train. Does not name the host.

Run on the Spark after env setup. Writes manifests/spark_host_preflight.json.
If this fails, leave gpu_host_for_H_I null and classify the Spark as blocked.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("P1_ROOT", Path(__file__).resolve().parents[2]))
RUN_ID = "p1-20260816T025911Z-0067a57"
VENDOR = ROOT / "vendor" / "nanochat"

EXPECTED = {
    "train.parquet": "706d706496e3a085cf4506f97aa8b03faa20d4773d69453eaab4e3ca8f33caf9",
    "train.jsonl": "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687",
    "val.jsonl": "4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c",
    "test.jsonl": "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf",
    "shard_00000.parquet": "aaf81d95e577742dcd33a44be2f144c253a5d5650e34b3e622e8b262ff2b6dc9",
    "shard_00001.parquet": "c57c11a2625c38f7f12d1e4018e71bf1f38a56d68fcc9b4952e1b8bded854976",
    "shard_00002.parquet": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
    "tokenizer.pkl": "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8",
    "token_bytes.pt": "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132",
}

PATHS = {
    "train.parquet": ROOT / "data" / "raw" / "wikitext-tl39" / "train.parquet",
    "train.jsonl": ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl",
    "val.jsonl": ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl",
    "test.jsonl": ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl",
    "shard_00000.parquet": ROOT / "data" / "processed" / "wikitext-tl39" / "active" / "shard_00000.parquet",
    "shard_00001.parquet": ROOT / "data" / "processed" / "wikitext-tl39" / "active" / "shard_00001.parquet",
    "shard_00002.parquet": ROOT / "data" / "processed" / "wikitext-tl39" / "active" / "shard_00002.parquet",
    "tokenizer.pkl": ROOT / "data" / "cache" / RUN_ID / "tokenizer" / "tokenizer.pkl",
    "token_bytes.pt": ROOT / "data" / "cache" / RUN_ID / "tokenizer" / "token_bytes.pt",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str]) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return (proc.stdout or proc.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {exc}"


def main() -> int:
    sys.path.insert(0, str(VENDOR))
    checks: list[dict] = []
    failed = False

    def record(name: str, ok: bool, detail: object) -> None:
        nonlocal failed
        checks.append({"name": name, "ok": ok, "detail": detail})
        if not ok:
            failed = True

    record("uname_m_aarch64", platform.machine() in {"aarch64", "arm64"}, platform.machine())
    record("data_dir_is_tagalog_active", os.environ.get("NANOCHAT_DATA_DIR", "").endswith("wikitext-tl39/active"), os.environ.get("NANOCHAT_DATA_DIR"))
    record("dataset_downloader_not_requested", True, "this script never calls nanochat.dataset")

    hashes = {}
    for key, path in PATHS.items():
        if not path.is_file():
            record(f"hash_{key}", False, f"missing {path}")
            continue
        actual = sha256_file(path)
        hashes[key] = actual
        record(f"hash_{key}", actual == EXPECTED[key], {"expected": EXPECTED[key], "actual": actual})

    active = ROOT / "data" / "processed" / "wikitext-tl39" / "active"
    test_hits = [p.name for p in active.iterdir() if "test" in p.name.lower()] if active.is_dir() else ["active_missing"]
    record("test_absent_from_active", test_hits == [], test_hits)

    cuda_info: dict = {}
    try:
        import torch

        cuda_info = {
            "torch": torch.__version__,
            "torch_cuda": torch.version.cuda,
            "cuda_available": bool(torch.cuda.is_available()),
            "device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
        }
        if torch.cuda.is_available():
            cuda_info["device_name"] = torch.cuda.get_device_name(0)
            cuda_info["capability"] = list(torch.cuda.get_device_capability(0))
            a = torch.randn(64, 64, device="cuda")
            b = torch.randn(64, 64, device="cuda")
            c = (a @ b).sum().item()
            cuda_info["matmul_finite"] = bool(__import__("math").isfinite(c))
            record("cuda_available", True, cuda_info)
            record("cuda_matmul_finite", cuda_info["matmul_finite"], c)
        else:
            record("cuda_available", False, cuda_info)
    except Exception as exc:  # noqa: BLE001
        record("torch_import", False, str(exc))

    inst = []
    if VENDOR.is_dir() and cuda_info.get("cuda_available"):
        from nanochat.gpt import GPT, GPTConfig
        import torch

        for depth in (4, 8, 12, 16, 20):
            base_dim = depth * 64
            model_dim = ((base_dim + 127) // 128) * 128
            heads = model_dim // 128
            try:
                with torch.device("cuda"):
                    model = GPT(
                        GPTConfig(
                            sequence_len=2048,
                            vocab_size=32768,
                            n_layer=depth,
                            n_head=heads,
                            n_kv_head=heads,
                            n_embd=model_dim,
                            window_pattern="SSSL",
                        )
                    )
                    p_total = int(model.num_scaling_params()["total"])
                inst.append({"depth": depth, "ok": True, "p_total": p_total, "t": 2048})
                del model
                torch.cuda.empty_cache()
            except Exception as exc:  # noqa: BLE001
                inst.append({"depth": depth, "ok": False, "error": str(exc), "t_shrunk": False})
        record("instantiate_t2048_all_registered_plus_d4", all(row["ok"] for row in inst), inst)
    else:
        record("instantiate_skipped", False, "CUDA or vendor/nanochat missing")

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "purpose": "dgx_spark_cuda_preflight_before_naming_host",
        "names_the_official_host": False,
        "official_gate_h_started": False,
        "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "nvidia_smi": run(["nvidia-smi"]),
        "nvcc": run(["nvcc", "--version"]),
        "uname": run(["uname", "-a"]),
        "hashes": hashes,
        "instantiation": inst,
        "checks": checks,
        "ok": not failed,
        "next_if_ok": "Fill manifests/execution_host.spark.template.json, copy into execution_host.json gpu_host_for_H_I, then run official p1-smoke-d4.",
        "next_if_fail": "Leave gpu_host_for_H_I null. Record blocked. Do not start official H.",
    }
    out = ROOT / "manifests" / "spark_host_preflight.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
