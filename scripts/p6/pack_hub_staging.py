#!/usr/bin/env python3
"""Stage P6-M Hub siblings from RELEASE_MANIFEST.json. Refuses partial inventory.

Paths are hub-relative + cache-relative templates only — no absolute Mac/pod paths
are stored in the manifest. Resolve sources via:

  P6_CACHE_ROOT or NANOCHAT_BASE_DIR  →  cache_root / entry.source_relpath
  else repo_root / data/cache/{run_id} / entry.source_relpath

Hub object names are entry.hub_path (also mirrored in checksums keys).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUB_DOCS = ROOT / "docs/hub/p6-m-schedule-topology"
MANIFEST = HUB_DOCS / "RELEASE_MANIFEST.json"
STAGING = ROOT / "transfer/p6-hub-pageman-nanochat-filipino-p6-m-schedule-topology"
DOC_SKIP = {".DS_Store"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def link_or_copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def cache_root(manifest: dict) -> Path:
    for env in manifest.get("path_scheme", {}).get("cache_root_env", ["P6_CACHE_ROOT", "NANOCHAT_BASE_DIR"]):
        v = os.environ.get(env)
        if v:
            return Path(v).expanduser().resolve()
    run_id = manifest["run_id"]
    return (ROOT / "data" / "cache" / run_id).resolve()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    keys = manifest["logical_keys"]
    entries = manifest["entries"]
    if set(keys) != set(entries):
        print("manifest logical_keys/entries mismatch", file=sys.stderr)
        return 2
    expect_n = int(manifest["expected_weightish_object_count"])
    if len(keys) != expect_n:
        print(f"expected {expect_n} keys, got {len(keys)}", file=sys.stderr)
        return 2

    root = cache_root(manifest)
    print(f"cache_root={root}")

    missing: list[str] = []
    mismatches: list[str] = []
    planned: list[tuple[str, Path, str]] = []
    for key in keys:
        row = entries[key]
        hub_path = row["hub_path"]
        src = root / row["source_relpath"]
        expect = row["sha256"]
        if not src.is_file():
            missing.append(f"{key}: missing {src}")
            continue
        got = sha256(src)
        if got != expect:
            mismatches.append(f"{key}: {got} != {expect}")
            continue
        if hub_path != key and key not in ("tokenizer.pkl", "token_bytes.pt"):
            # hub_path is authoritative for weight objects
            pass
        checksum_key = hub_path
        if checksum_key not in manifest["checksums"] or manifest["checksums"][checksum_key] != expect:
            mismatches.append(f"{key}: checksums map mismatch for {checksum_key}")
            continue
        planned.append((hub_path, src, expect))

    if missing or mismatches:
        for line in missing + mismatches:
            print(line, file=sys.stderr)
        print(
            "hub staging refuses incomplete inventory "
            f"(have {len(planned)}/{expect_n})",
            file=sys.stderr,
        )
        return 3

    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    shutil.copytree(HUB_DOCS, STAGING, dirs_exist_ok=True, ignore=shutil.ignore_patterns(*DOC_SKIP))

    sum_lines: list[str] = []
    for hub_path, src, expect in planned:
        link_or_copy(src, STAGING / hub_path)
        sum_lines.append(f"{expect}  {hub_path}")

    # Stable order matches logical_keys via hub_path
    ordered = []
    for key in keys:
        hub_path = entries[key]["hub_path"]
        ordered.append(f"{entries[key]['sha256']}  {hub_path}")
    (STAGING / "SHA256SUMS.txt").write_text("\n".join(ordered) + "\n", encoding="utf-8")
    (STAGING / "SHA256SUMS-weights.txt").write_text("\n".join(ordered) + "\n", encoding="utf-8")

    staged_manifest = dict(manifest)
    staged_manifest["status"] = "staged"
    staged_manifest["cache_root_resolved_note"] = "ephemeral local resolve only; not a deposit path"
    staged_manifest.pop("cache_root_resolved", None)
    (STAGING / "RELEASE_MANIFEST.json").write_text(
        json.dumps(staged_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    n_weightish = sum(
        1
        for p in STAGING.rglob("*")
        if p.is_file() and (p.name.endswith(".pt") or p.name == "tokenizer.pkl")
    )
    # tokenizer.pkl + token_bytes.pt + 7 model pts = 9; exclude eval docs
    weight_names = {entries[k]["hub_path"] for k in keys}
    present = {str(p.relative_to(STAGING)) for p in STAGING.rglob("*") if p.is_file()}
    if not weight_names.issubset(present):
        print("staged hub_path coverage failed", weight_names - present, file=sys.stderr)
        return 4
    print(STAGING)
    print(f"staged_weightish={len(weight_names)} files_on_disk_weightish={n_weightish}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
