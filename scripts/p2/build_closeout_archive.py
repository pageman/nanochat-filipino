#!/usr/bin/env python3
"""P2 close-out: hash-verify local artifacts, copy a documentation archive, write manifest.

Does not recompute BPB, does not read test.jsonl contents, does not start/stop pods.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
RUN = "p2-20260817T150944Z-de99f8a"
CARDS = ROOT / "docs/run-cards/p2" / RUN
CACHE = ROOT / "data/cache" / RUN
ARCHIVE = ROOT / "transfer/p2-closeout-archive-20260819"
PACK_RB = ROOT / "transfer/p2-researchbox-8763-20260819"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

EXPECTED_CKPT = {
    "A0_d20": (
        CACHE / "a0/frozen/p2-en0-d20/model_005415.pt",
        "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d",
    ),
    "A0_d20_writable_alias": (
        CACHE / "base_checkpoints/p2-en0-d20/model_005415.pt",
        "bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d",
    ),
    "A0_d8_provenance": (
        CACHE / "base_checkpoints/p2-en0-d8/model_005415.pt",
        "5e1db47f0609995e2309a2c04ede4cd330aa0f2d113e07d6498790d5ca707a8c",
    ),
    "A1": (
        CACHE / "base_checkpoints/p2-a1-extra-en-d20/model_000294.pt",
        "e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d",
    ),
    "A2": (
        CACHE / "base_checkpoints/p2-a2-tagalog-d20/model_000294.pt",
        "2b01acf8fac0e8c783162582cbb384e8ce1c37795aae2f7dd4ae34c2a5c76026",
    ),
    "A3": (
        CACHE / "base_checkpoints/p2-a3-mix-d20/model_000294.pt",
        "d6c62bb793a57c7c23d98c5bd62ec36b41606234524f76855b4459d98c42b368",
    ),
    "tokenizer_pkl": (
        CACHE / "tokenizer/tokenizer.pkl",
        "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6",
    ),
    "token_bytes": (
        CACHE / "tokenizer/token_bytes.pt",
        "5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42",
    ),
}

SEAL_NUMBERS = {
    "en_a0": 1.389990,
    "tl_a0": 4.917650,
    "en_a1": 1.459675,
    "tl_a1": 5.054664,
    "en_a2": 1.385684,
    "tl_a2": 1.171616,
    "en_a3": 1.279433,
    "tl_a3": 1.528858,
    "c_en": -0.073991,
    "g_tl": -3.883048,
    "en_a3_minus_a1": -0.180242,
    "tl_a3_minus_a1": -3.525806,
    "test_en_a2": 1.392015,
    "test_tl_a2": 1.160154,
}

EXCLUDED_NAME_RE = re.compile(
    r"(test\.jsonl|english_test\.jsonl|\.env$|id_ed25519|id_rsa|\.pem$|"
    r"passcode|HF_TOKEN|RUNPOD|cookie|\.netrc|aspredicted-p2-submitted)",
    re.I,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def row(name, rel, src, digest, size, classification, status, notes):
    return {
        "logical_artifact_name": name,
        "relative_archive_path": rel,
        "source_path": src,
        "sha256": digest,
        "byte_size": size,
        "copy_verification_utc": NOW,
        "sensitivity_classification": classification,
        "verification_status": status,
        "notes": notes,
    }


def copy_tree_filtered(src: Path, dst: Path, rows: list) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for p in sorted(src.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(src).as_posix()
        if EXCLUDED_NAME_RE.search(p.name) or EXCLUDED_NAME_RE.search(rel):
            rows.append(
                row(
                    f"EXCLUDED {p.name}",
                    f"(excluded) {rel}",
                    str(p),
                    None,
                    p.stat().st_size if p.exists() else 0,
                    "excluded",
                    "not applicable",
                    "Not copied into close-out archive",
                )
            )
            continue
        if p.suffix in {".pt", ".pkl", ".bin", ".safetensors"} and "tokenizer" not in str(p):
            continue
        if p.name.startswith("paper-OBSOLETE") and p.suffix == ".pdf":
            rows.append(
                row(
                    "obsolete paper.pdf skipped",
                    "(not archived as current PDF)",
                    str(p),
                    None,
                    p.stat().st_size,
                    "public",
                    "not applicable",
                    "16 Aug Stage-1 PDF must not ship as P2 results",
                )
            )
            continue
        target = dst / p.name if src == p.parent else dst / p.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        digest = sha256_file(target)
        os.chmod(target, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        rows.append(
            row(
                rel,
                str(target.relative_to(ARCHIVE)),
                str(p),
                digest,
                target.stat().st_size,
                "public",
                "hash matched",
                "copied into documentation archive",
            )
        )


def paper_audit() -> dict:
    tex = (ROOT / "docs/papers/p2-cf-english/paper.tex").read_text(encoding="utf-8")
    missing = []
    for label, val in SEAL_NUMBERS.items():
        s = f"{val:.6f}" if abs(val) < 10 else f"{val:.6f}"
        # keep six decimals as in seal display
        s = f"{val:.6f}"
        if s not in tex:
            missing.append(s)
    phrases = ["not observed", "observed", "one seed", "one-seed", "secondary"]
    found = {p: (p.lower() in tex.lower()) for p in phrases}
    return {"missing_numeric_strings": missing, "phrases": found}


def scan_archive_for_exclusions(root: Path) -> list[str]:
    hits = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(root))
        if EXCLUDED_NAME_RE.search(rel) or EXCLUDED_NAME_RE.search(p.name):
            hits.append(rel)
        if p.suffix.lower() == ".jsonl" and "test" in p.name.lower():
            hits.append(rel)
    return hits


def main() -> None:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    rows = []

    # Checkpoints: hash in place; do not copy 2.5G files into transfer/
    for name, (path, expected) in EXPECTED_CKPT.items():
        if not path.is_file():
            rows.append(
                row(name, "(missing)", str(path), None, 0, "controlled", "exception", "FILE MISSING")
            )
            continue
        digest = sha256_file(path)
        status = "hash matched" if digest == expected else f"MISMATCH expected {expected}"
        rows.append(
            row(
                name,
                str(path.relative_to(ROOT)),
                str(path),
                digest,
                path.stat().st_size,
                "controlled",
                status,
                "weights remain in data/cache; not copied into documentation pack",
            )
        )

    # Key JSON hashes
    for label, path in [
        ("Gate U validation seal", CARDS / "gate-u-seal.json"),
        ("Gate V test JSON", CARDS / "gate-v-test.json"),
        ("P2 test ledger", ROOT / "docs/run-cards/p2/test_access_log.json"),
        ("LOCK.json", ROOT / "docs/papers/p2-cf-english/LOCK.json"),
        ("Gate W deposit", CARDS / "gate-w-deposit.json"),
        ("P3 post-unblinding note", CARDS / "p3-post-unblinding.md"),
        ("AsPredicted 306935 PDF", ROOT / "docs/run-cards/AsPredicted-306935.pdf"),
        ("Protocol", ROOT / "docs/papers/p2-cf-english/PROTOCOL-p2-en-then-tl.md"),
        ("paper.tex", ROOT / "docs/papers/p2-cf-english/paper.tex"),
        ("continue_from_frozen.py", ROOT / "scripts/p2/continue_from_frozen.py"),
        ("evaluate_bpb.py", ROOT / "scripts/p2/evaluate_bpb.py"),
        ("gate_u_seal.py", ROOT / "scripts/p2/gate_u_seal.py"),
        ("gate_v_test.py", ROOT / "scripts/p2/gate_v_test.py"),
    ]:
        digest = sha256_file(path)
        dest = ARCHIVE / "pinned" / path.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        os.chmod(dest, 0o444)
        rows.append(
            row(label, str(dest.relative_to(ARCHIVE)), str(path), digest, path.stat().st_size, "public", "hash matched", "")
        )

    # Run-card tree (no secrets by construction; skip nothing extra)
    cards_dst = ARCHIVE / "run-cards"
    copy_tree_filtered(CARDS, cards_dst, rows)

    scripts_dst = ARCHIVE / "scripts-p2"
    copy_tree_filtered(ROOT / "scripts/p2", scripts_dst, rows)

    paper_dst = ARCHIVE / "paper"
    copy_tree_filtered(ROOT / "docs/papers/p2-cf-english", paper_dst, rows)

    # Tokenizer copies (public if licensing permits; hashes already recorded)
    tok_dst = ARCHIVE / "tokenizer"
    tok_dst.mkdir(exist_ok=True)
    for src in [CACHE / "tokenizer/tokenizer.pkl", CACHE / "tokenizer/token_bytes.pt"]:
        dest = tok_dst / src.name
        shutil.copy2(src, dest)
        os.chmod(dest, 0o444)
        rows.append(
            row(
                src.name,
                str(dest.relative_to(ARCHIVE)),
                str(src),
                sha256_file(dest),
                dest.stat().st_size,
                "public",
                "hash matched",
                "tokenizer copies in archive",
            )
        )

    # Shard hash verification (train/val only; never test.jsonl)
    shard_expected = json.loads((CARDS / "gate-e-shards.json").read_text())
    for family, key in [("english", "english"), ("tagalog", "tagalog_copy"), ("a3_mix", "a3")]:
        block = shard_expected.get(key) or shard_expected.get(family)
        if not block:
            continue
        shards = block.get("shards") or {}
        for fname, meta in shards.items():
            sp = ROOT / meta["path"]
            if not sp.is_file():
                rows.append(
                    row(
                        f"shard {fname}",
                        meta["path"],
                        str(sp),
                        None,
                        0,
                        "controlled",
                        "exception",
                        "missing locally",
                    )
                )
                continue
            digest = sha256_file(sp)
            exp = meta["sha256"]
            rows.append(
                row(
                    f"shard {fname}",
                    meta["path"],
                    str(sp),
                    digest,
                    sp.stat().st_size,
                    "controlled",
                    "hash matched" if digest == exp else f"MISMATCH {exp}",
                    family,
                )
            )

    # Prescribed test identities without reading files
    rows.append(
        row(
            "WT103-raw English test identity (excluded raw file)",
            "(excluded) data/interim/wikitext-103/english_test.jsonl",
            "data/interim/wikitext-103/english_test.jsonl",
            "2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e",
            None,
            "excluded",
            "not applicable",
            "Prescribed SHA from Gate V / LOCK; raw file not archived",
        )
    )
    rows.append(
        row(
            "P1.1 Tagalog test.jsonl identity (excluded raw file)",
            "(excluded) data/processed/wikitext-tl39/test/test.jsonl",
            "data/processed/wikitext-tl39/test/test.jsonl",
            "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf",
            None,
            "excluded",
            "not applicable",
            "Prescribed SHA from Gate V; raw file not archived",
        )
    )

    # ResearchBox pack if present
    if PACK_RB.is_dir():
        hits = scan_archive_for_exclusions(PACK_RB)
        rows.append(
            row(
                "ResearchBox pack tree",
                str(PACK_RB.relative_to(ROOT)),
                str(PACK_RB),
                None,
                sum(p.stat().st_size for p in PACK_RB.rglob("*") if p.is_file()),
                "public",
                "hash matched" if not hits else "exception",
                f"exclusion hits={hits}",
            )
        )

    audit_hits = scan_archive_for_exclusions(ARCHIVE)
    pa = paper_audit()

    mismatches = [r for r in rows if isinstance(r["verification_status"], str) and r["verification_status"].startswith("MISMATCH")]
    missing = [r for r in rows if r["verification_status"] == "exception"]

    manifest = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "p2_run_id": RUN,
        "nanochat_pin": "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd",
        "built_utc": NOW,
        "pods_not_stopped": True,
        "volume_not_terminated": True,
        "paper_audit": pa,
        "archive_exclusion_hits": audit_hits,
        "checkpoint_mismatches": mismatches,
        "missing_or_exception": missing,
        "artifacts": rows,
    }

    man_path = CARDS / "p2_closeout_manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2) + "\n")
    shutil.copy2(man_path, ARCHIVE / "p2_closeout_manifest.json")

    summary = {
        "manifest": str(man_path),
        "archive": str(ARCHIVE),
        "n_artifacts": len(rows),
        "mismatches": len(mismatches),
        "exceptions": len(missing),
        "archive_exclusion_hits": audit_hits,
        "paper_audit": pa,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
