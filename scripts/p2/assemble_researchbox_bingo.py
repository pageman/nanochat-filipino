#!/usr/bin/env python3
"""Assemble ResearchBox 8763 bingo packets. No test.jsonl, no passcodes, no .pt."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import zipfile
from pathlib import Path

# ResearchBox Data: tables only. .txt prose is auto-moved to Other.
DATA_EXTS = {".csv", ".tsv"}

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
SRC_DOCS = ROOT / "docs/run-cards/p2/researchbox-bingo"
CARDS = ROOT / "docs/run-cards/p2/p2-20260817T150944Z-de99f8a"
PAPER = ROOT / "docs/papers/p2-cf-english"
SCRIPTS = ROOT / "scripts/p2"
OUT = ROOT / "transfer/p2-researchbox-8763-bingo"
EXCLUDE_NAMES = {
    "HOST-8ik4ix7j8iju9u.md",
    "HOST-xk8orhscuk2jsu.md",
    "paper-OBSOLETE-stage1-20260816.pdf",
    "aspredicted-p2-submitted.txt",
    "aspredicted-p1-submitted.txt",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy(src: Path, dest: Path) -> None:
    if src.name in EXCLUDE_NAMES:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def zip_dir(folder: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(folder))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    mats = OUT / "Materials"
    data = OUT / "Data"
    code = OUT / "Code"
    other = OUT / "Other"
    for d in (mats, data, code, other):
        d.mkdir(parents=True)

    copy(SRC_DOCS / "00-BINGO-PLACEMENT.md", OUT / "00-BINGO-PLACEMENT.md")
    copy(SRC_DOCS / "P2-MATERIALS.md", mats / "P2-MATERIALS.md")
    copy(PAPER / "PROTOCOL-p2-en-then-tl.md", mats / "PROTOCOL-p2-en-then-tl.md")
    copy(PAPER / "paper.tex", mats / "paper.tex")
    copy(PAPER / "paper_outputs/paper.pdf", mats / "paper.pdf")
    copy(PAPER / "paper_outputs/paper.md", mats / "paper.md")
    copy(PAPER / "paper_outputs/paper_build_receipt.txt", mats / "paper_build_receipt.txt")
    copy(ROOT / "docs/run-cards/p2/HF-MODEL-CARD-p2.md", mats / "HF-MODEL-CARD-p2.md")
    copy(ROOT / "docs/run-cards/p2/PUBLIC-STATUS.md", mats / "PUBLIC-STATUS.md")
    copy(CARDS / "DATA-CARD-wikitext-103.md", mats / "DATA-CARD-wikitext-103.md")
    copy(PAPER / "DIRECTION-RECALIBRATION.md", mats / "DIRECTION-RECALIBRATION.md")
    copy(PAPER / "aspredicted-answers-p2.txt", mats / "aspredicted-answers-p2.txt")

    spec = importlib.util.spec_from_file_location(
        "emit_p2_researchbox_tables", SCRIPTS / "emit_p2_researchbox_tables.py"
    )
    emit_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(emit_mod)
    emit_mod.emit(data)
    copy(SRC_DOCS / "P2-DATA-CODEBOOK.txt", other / "P2-DATA-CODEBOOK.txt")

    receipts = OUT / "_json_receipts_staging"
    receipts.mkdir()
    lock = json.loads((PAPER / "LOCK.json").read_text())
    lock.pop("researchbox_passcode", None)
    (receipts / "LOCK.sanitized.json").write_text(json.dumps(lock, indent=2) + "\n")
    for name in [
        "gate-b-english-archive.json",
        "gate-d-english-split.json",
        "gate-e-shards.json",
        "gate-f-tokenizer.json",
        "gate-g-budget.json",
        "gate_p0_val_baselines.json",
        "gate-u-seal.json",
        "gate-v-test.json",
        "byte_unigram_english_val.json",
        "registered-reporting-q3-q8.json",
    ]:
        copy(CARDS / name, receipts / name)
    copy(ROOT / "docs/run-cards/p2/test_access_log.json", receipts / "test_access_log.json")
    zip_dir(receipts, other / "P2-data-receipts.zip")
    shutil.rmtree(receipts)

    copy(SRC_DOCS / "P2-CODE.md", code / "P2-CODE.md")
    for p in sorted(SCRIPTS.iterdir()):
        if p.suffix in {".py", ".sh"}:
            copy(p, code / p.name)

    data_names = {
        "gate-b-english-archive.json",
        "gate-d-english-split.json",
        "gate-e-shards.json",
        "gate-f-tokenizer.json",
        "gate-g-budget.json",
        "gate_p0_val_baselines.json",
        "gate-u-seal.json",
        "gate-v-test.json",
        "byte_unigram_english_val.json",
        "registered-reporting-q3-q8.json",
        "test_access_log.json",
        "LOCK.json",
    }
    copy(SRC_DOCS / "P2-OTHER.md", other / "P2-OTHER.md")
    copy(SRC_DOCS / "P2-DATA-CODEBOOK.md", other / "P2-DATA-CODEBOOK.md")
    copy(SRC_DOCS / "00-BINGO-PLACEMENT.md", other / "00-BINGO-PLACEMENT.md")
    for p in sorted(CARDS.iterdir()):
        if p.name in EXCLUDE_NAMES or p.name in data_names:
            continue
        if p.suffix in {".json", ".md"}:
            copy(p, other / p.name)
        elif p.suffix == ".log" and p.name.startswith("p2-gate"):
            copy(p, other / p.name)
    copy(ROOT / "docs/run-cards/p2/SIX-LAYER-CLOSEOUT.md", other / "SIX-LAYER-CLOSEOUT.md")
    copy(ROOT / "docs/run-cards/p2/PREREG-REPORTING-AUDIT.md", other / "PREREG-REPORTING-AUDIT.md")
    copy(ROOT / "docs/run-cards/p2/CLOSEOUT-CHECKLIST.md", other / "CLOSEOUT-CHECKLIST.md")
    copy(ROOT / "docs/run-cards/p2/p2-20260817T150944Z-de99f8a/p2_closeout_manifest.json", other / "p2_closeout_manifest.json")

    # exclusion scan
    hits = []
    for p in OUT.rglob("*"):
        if not p.is_file():
            continue
        n = p.name.lower()
        if n.endswith("test.jsonl") or n == "english_test.jsonl" or p.suffix == ".pt" and "token_bytes" not in n:
            hits.append(str(p))
        if "passcode" in n or n.endswith(".pem") or n.startswith("id_"):
            hits.append(str(p))
    illegal_data = [
        str(p)
        for p in data.iterdir()
        if p.is_file() and p.suffix.lower() not in DATA_EXTS
    ]
    if illegal_data:
        raise SystemExit(f"Data column rejects these extensions: {illegal_data}")
    if hits:
        raise SystemExit(f"exclusion hits: {hits}")

    lines = ["# ResearchBox 8763 bingo pack hashes", ""]
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "HASHES.txt":
            rel = p.relative_to(OUT).as_posix()
            lines.append(f"{sha256_file(p)}  {rel}")
    (other / "HASHES.txt").write_text("\n".join(lines) + "\n")
    (OUT / "HASHES.txt").write_text("\n".join(lines) + "\n")

    zip_dir(mats, OUT / "Materials.zip")
    zip_dir(code, OUT / "Code.zip")
    zip_dir(other, OUT / "Other.zip")
    print(json.dumps({
        "out": str(OUT),
        "n_files": sum(1 for p in OUT.rglob("*") if p.is_file()),
        "zips": ["Materials.zip", "Code.zip", "Other.zip"],
        "data_upload": "individual csv/tsv tables only; never Data.zip or prose txt",
        "exclusion_hits": hits,
    }, indent=2))


if __name__ == "__main__":
    main()
