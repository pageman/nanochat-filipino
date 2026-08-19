#!/usr/bin/env python3
"""P2 Gate Q: freeze EN0 as arm A0 (copy to a0/frozen/, stamp ledger).

English val_bpb_full is copied from Gate P0 (no recompute).
Tagalog val_bpb_full is scored once on frozen weights (eval only; not continuation).
No optimizer steps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "p2-20260817T150944Z-de99f8a"
CACHE = ROOT / "data" / "cache" / RUN_ID
OUT_DIR = ROOT / "docs" / "run-cards" / "p2" / RUN_ID
P0_SUMMARY = OUT_DIR / "gate_p0_val_baselines.json"

EN0_TAGS = {
    8: "p2-en0-d8",
    20: "p2-en0-d20",
}
EN0_STEP = 5415
EXPECTED_SHA = {
    8: "5e1db47f0609995e2309a2c04ede4cd330aa0f2d113e07d6498790d5ca707a8c",
    20: "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_frozen(depth: int, tag: str) -> dict:
    src_dir = CACHE / "base_checkpoints" / tag
    dst_dir = CACHE / "a0" / "frozen" / tag
    dst_dir.mkdir(parents=True, exist_ok=True)
    copied = {}
    for name in (f"meta_{EN0_STEP:06d}.json", f"model_{EN0_STEP:06d}.pt"):
        src = src_dir / name
        dst = dst_dir / name
        if not src.exists():
            raise SystemExit(f"missing source checkpoint: {src}")
        if dst.exists():
            if sha256_file(dst) == sha256_file(src):
                print(f"skip copy (hash match): {dst}", flush=True)
            else:
                raise SystemExit(f"frozen destination exists with different hash: {dst}")
        else:
            print(f"copy {src} -> {dst}", flush=True)
            shutil.copy2(src, dst)
        actual = sha256_file(dst)
        expected = EXPECTED_SHA[depth] if name.endswith(".pt") else None
        if expected and actual != expected:
            raise SystemExit(f"hash mismatch {dst}: {actual} != {expected}")
        copied[name] = {"path": str(dst.relative_to(ROOT)), "sha256": actual, "bytes": dst.stat().st_size}
    return copied


def english_from_p0() -> dict:
    if not P0_SUMMARY.exists():
        raise SystemExit(f"missing P0 summary: {P0_SUMMARY}")
    p0 = json.loads(P0_SUMMARY.read_text())
    p0_sha = sha256_file(P0_SUMMARY)
    expected_p0_sha = "3fe37fe90b43c45d1e59852fd83deb420d9d699c7e9504811a8dc7ac5ebb98c9"
    if p0_sha != expected_p0_sha:
        raise SystemExit(f"P0 summary hash changed: {p0_sha} != {expected_p0_sha}")
    out = {}
    for depth_str, row in p0["depths"].items():
        out[depth_str] = {
            "val_bpb_full": row["val_bpb_full"],
            "source": "gate_p0_val_baselines.json",
            "p0_summary_sha256": p0_sha,
            "recomputed": False,
        }
    return out


def run_tagalog_eval(device_type: str, device_batch_size: int) -> None:
    py = sys.executable
    script = ROOT / "scripts" / "p2" / "evaluate_bpb.py"
    for depth, tag in EN0_TAGS.items():
        cmd = [
            py,
            str(script),
            "--phase",
            "val_one",
            "--language",
            "tagalog",
            "--model-tag",
            tag,
            "--step",
            str(EN0_STEP),
            "--device-type",
            device_type,
            "--device-batch-size",
            str(device_batch_size),
            "--out-dir",
            str(OUT_DIR),
        ]
        print(" ".join(cmd), flush=True)
        subprocess.run(cmd, check=True, cwd=ROOT)


def load_tagalog_a0() -> dict:
    out = {}
    for depth, tag in EN0_TAGS.items():
        path = OUT_DIR / f"{tag}_a0_tagalog_val.json"
        if not path.exists():
            raise SystemExit(f"missing Tagalog A0 eval: {path}")
        row = json.loads(path.read_text())
        out[str(depth)] = {
            "val_bpb_full": row["val_bpb_full"],
            "source": str(path.relative_to(ROOT)),
            "source_sha256": sha256_file(path),
            "recomputed": True,
            "trained_val": row.get("trained_val"),
        }
    return out


def write_ledger(english: dict, tagalog: dict | None, host: str) -> Path:
    depths = {}
    for depth_str in ("8", "20"):
        depths[depth_str] = {
            "depth": int(depth_str),
            "model_tag": EN0_TAGS[int(depth_str)],
            "frozen_dir": f"data/cache/{RUN_ID}/a0/frozen/{EN0_TAGS[int(depth_str)]}",
            "checkpoint_step": EN0_STEP,
            "checkpoint_sha256": EXPECTED_SHA[int(depth_str)],
            "english_val_bpb_full": english[depth_str],
            "tagalog_val_bpb_full": tagalog[depth_str] if tagalog else {"status": "pending"},
        }
    doc = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "does_not_amend_306780": True,
        "gate": "Q",
        "arm": "A0",
        "status": "pass" if tagalog else "frozen_pending_tagalog_eval",
        "immutable": True,
        "additional_train_tokens": 0,
        "started_tagalog_continuation": False,
        "test_read_count": 0,
        "host": host,
        "at_utc": utc_now(),
        "run_id": RUN_ID,
        "en0_step": EN0_STEP,
        "primary_confirmatory_depth": 20,
        "english_bpe_tokenizer_sha256": "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6",
        "tagalog_val_shard": "data/processed/p2-tl39-readonly/shard_00002.parquet",
        "tagalog_val_shard_sha256": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
        "tagalog_val_packed_bytes_p11_invariant": 5868797,
        "depths": depths,
        "p0_summary": str(P0_SUMMARY.relative_to(ROOT)),
        "p0_summary_sha256": sha256_file(P0_SUMMARY),
        "note": "A0 is frozen EN0. English val copied from P0-E. Tagalog val is one eval on frozen EN0 under P2 English BPE (not Tagalog continuation). d20 is confirmatory parent for A1/A2/A3.",
    }
    path = OUT_DIR / "gate-q-a0.json"
    path.write_text(json.dumps(doc, indent=2) + "\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-copy", action="store_true", help="Assume a0/frozen already populated")
    parser.add_argument("--tagalog-eval", action="store_true", help="Run Tagalog val_bpb_full on frozen EN0")
    parser.add_argument("--device-type", default="cuda")
    parser.add_argument("--device-batch-size", type=int, default=8)
    parser.add_argument("--host", default="Mac/CPU")
    args = parser.parse_args()

    frozen = {}
    if not args.skip_copy:
        for depth, tag in EN0_TAGS.items():
            frozen[tag] = copy_frozen(depth, tag)

    english = english_from_p0()
    tagalog = None
    if args.tagalog_eval:
        run_tagalog_eval(args.device_type, args.device_batch_size)
        tagalog = load_tagalog_a0()
        args.host = f"{args.host}+{args.device_type}"

    path = write_ledger(english, tagalog, args.host)
    if tagalog is None:
        print(f"Gate Q partial: frozen copies done; Tagalog A0 eval still required.", flush=True)
        print(f"  python3 scripts/p2/gate_q_a0_freeze.py --skip-copy --tagalog-eval --device-type cuda", flush=True)
    else:
        print(f"Gate Q PASS: {path}", flush=True)
    print(json.dumps({"gate_q_json": str(path.relative_to(ROOT)), "immutable": True}, indent=2), flush=True)
    return 0 if tagalog else 2


if __name__ == "__main__":
    raise SystemExit(main())
