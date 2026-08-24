#!/usr/bin/env python3
"""Stage C0+C1+C2+C3 per eligible seed + tokenizer for Hub upload. Refuses partial inventory."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data/cache/p5-20260823T160632Z-439d1de5"
HUB_DOCS = ROOT / "docs/hub/p5-p4-multi-seed"
MANIFEST = HUB_DOCS / "RELEASE_MANIFEST.json"
STAGING = ROOT / "transfer/p5-hub-pageman-nanochat-filipino-p5-p4-multi-seed"

DOC_SKIP = {".DS_Store"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
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


def build_weights() -> dict[str, tuple[Path, str]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    checksums = manifest["checksums"]
    out: dict[str, tuple[Path, str]] = {}
    for seed in (1, 2, 3):
        for arm, sub in (
            ("c0", f"p5-s{seed}/c0/frozen/p5-s{seed}-c0-tl-d20/model_000294.pt"),
            ("c1", f"base_checkpoints/p5-s{seed}-c1-tl-d20/model_000294.pt"),
            ("c2", f"base_checkpoints/p5-s{seed}-c2-en-d20/model_000294.pt"),
            ("c3", f"base_checkpoints/p5-s{seed}-c3-mix-d20/model_000294.pt"),
        ):
            rel = f"seed-{seed}/{arm}/p5-s{seed}-{arm.replace('c0', 'c0-tl').replace('c1', 'c1-tl').replace('c2', 'c2-en').replace('c3', 'c3-mix')}-d20-model_000294.pt"
            if arm == "c0":
                hub_name = f"seed-{seed}/c0/p5-s{seed}-c0-tl-d20-model_000294.pt"
            elif arm == "c1":
                hub_name = f"seed-{seed}/c1/p5-s{seed}-c1-tl-d20-model_000294.pt"
            elif arm == "c2":
                hub_name = f"seed-{seed}/c2/p5-s{seed}-c2-en-d20-model_000294.pt"
            else:
                hub_name = f"seed-{seed}/c3/p5-s{seed}-c3-mix-d20-model_000294.pt"
            src = CACHE / sub
            expect = checksums[f"seed-{seed}/{arm}"]
            out[hub_name] = (src, expect)
    out["tokenizer.pkl"] = (CACHE / "tokenizer/tokenizer.pkl", checksums["tokenizer.pkl"])
    out["token_bytes.pt"] = (CACHE / "tokenizer/token_bytes.pt", checksums["token_bytes.pt"])
    return out


def main() -> int:
    weights = build_weights()
    missing = [str(src) for src, _ in weights.values() if not src.is_file()]
    if missing:
        print("hub staging refuses incomplete inventory:", *missing, sep="\n", file=sys.stderr)
        return 2
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    shutil.copytree(HUB_DOCS, STAGING, dirs_exist_ok=True, ignore=shutil.ignore_patterns(*DOC_SKIP))
    sum_lines: list[str] = []
    for rel, (src, expect) in sorted(weights.items()):
        got = sha256(src)
        if got != expect:
            print(f"hash mismatch {rel}: {got} != {expect}", file=sys.stderr)
            return 3
        link_or_copy(src, STAGING / rel)
        sum_lines.append(f"{got}  {rel}")
    (STAGING / "SHA256SUMS.txt").write_text("\n".join(sum_lines) + "\n", encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["status"] = "staged"
    manifest["researchbox"] = 8904
    manifest["ascollected"] = {"id": 2503, "url": "https://ascollected.org/HC8_G2F", "version": 1}
    (STAGING / "RELEASE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(STAGING)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
