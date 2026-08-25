#!/usr/bin/env python3
"""Independently validate P6-M prefiling schedule and authority hashes."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "manifests" / "p6" / "p6_topology_schedule_manifest.json"
HASHES_PATH = (
    ROOT
    / "docs"
    / "papers"
    / "p6-m-schedule-topology"
    / "P6-M-PREFILING-HASHES.json"
)
Q8_PATH = (
    ROOT
    / "docs"
    / "papers"
    / "p6-m-schedule-topology"
    / "ASPREDICTED-Q8-DRAFT.md"
)

EXPECTED_TOTAL = 19_267_584
EXPECTED_PER_LANGUAGE = 9_633_792

Block = Tuple[str, int, int]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_schedule(path: Path) -> List[Block]:
    blocks: List[Block] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        expected_fields = [
            "block_index",
            "language",
            "source_offset_tokens",
            "length_tokens",
        ]
        if reader.fieldnames != expected_fields:
            raise ValueError(f"{path}: field mismatch {reader.fieldnames}")
        for expected_index, row in enumerate(reader):
            if int(row["block_index"]) != expected_index:
                raise ValueError(f"{path}: nonconsecutive block index")
            blocks.append(
                (
                    row["language"],
                    int(row["source_offset_tokens"]),
                    int(row["length_tokens"]),
                )
            )
    return blocks


def origin_mask_sha256(blocks: List[Block]) -> str:
    h = hashlib.sha256()
    for language, _offset, length in blocks:
        byte = b"\x00" if language == "EN" else b"\x01"
        remaining = length
        while remaining:
            take = min(remaining, 1 << 20)
            h.update(byte * take)
            remaining -= take
    return h.hexdigest()


def validate_offsets_and_totals(name: str, blocks: List[Block]) -> Dict[str, int]:
    offsets = {"EN": 0, "TL": 0}
    totals = {"EN": 0, "TL": 0}
    for language, offset, length in blocks:
        if language not in offsets or length <= 0:
            raise ValueError(f"{name}: invalid block")
        if offset != offsets[language]:
            raise ValueError(f"{name}: {language} offset mismatch")
        offsets[language] += length
        totals[language] += length
    if totals != {"EN": EXPECTED_PER_LANGUAGE, "TL": EXPECTED_PER_LANGUAGE}:
        raise ValueError(f"{name}: quota mismatch {totals}")
    if sum(totals.values()) != EXPECTED_TOTAL:
        raise ValueError(f"{name}: total mismatch")
    return totals


def validate_shape(name: str, blocks: List[Block]) -> None:
    languages = [language for language, _offset, _length in blocks]
    lengths = [length for _language, _offset, length in blocks]
    if name == "m-fine":
        if len(blocks) != 9_408 or any(length != 2_048 for length in lengths):
            raise ValueError("m-fine: block shape mismatch")
        if any(language != ("EN" if i % 2 == 0 else "TL") for i, language in enumerate(languages)):
            raise ValueError("m-fine: not strict EN-first alternation")
    elif name == "m-coarse":
        if len(blocks) != 16 or any(length != 1_204_224 for length in lengths):
            raise ValueError("m-coarse: block shape mismatch")
        if any(language != ("EN" if i % 2 == 0 else "TL") for i, language in enumerate(languages)):
            raise ValueError("m-coarse: not strict EN-first alternation")
    elif name == "m-blocked":
        if blocks != [
            ("TL", 0, EXPECTED_PER_LANGUAGE),
            ("EN", 0, EXPECTED_PER_LANGUAGE),
        ]:
            raise ValueError("m-blocked: exact TL-then-EN rule mismatch")
    elif name == "m-rand":
        if len(blocks) != 9_408 or any(length != 2_048 for length in lengths):
            raise ValueError("m-rand: block shape mismatch")
        if languages.count("EN") != 4_704 or languages.count("TL") != 4_704:
            raise ValueError("m-rand: label quota mismatch")
    else:
        raise ValueError(f"unexpected topology {name}")


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    hashes = json.loads(HASHES_PATH.read_text(encoding="utf-8"))

    if sha256_file(MANIFEST_PATH) != hashes["topology_manifest"]["sha256"]:
        raise SystemExit("topology manifest SHA mismatch")
    addendum = ROOT / hashes["addendum"]["path"]
    if sha256_file(addendum) != hashes["addendum"]["sha256"]:
        raise SystemExit("addendum SHA mismatch")
    generator = ROOT / hashes["schedule_generator"]["path"]
    if sha256_file(generator) != hashes["schedule_generator"]["sha256"]:
        raise SystemExit("generator SHA mismatch")

    plan = Path(hashes["gate_plan"]["path"])
    if not plan.is_file() or sha256_file(plan) != hashes["gate_plan"]["sha256"]:
        raise SystemExit("gate plan missing or SHA mismatch")

    records = manifest["topologies"]
    if {record["id"] for record in records} != {
        "m-fine",
        "m-coarse",
        "m-blocked",
        "m-rand",
    }:
        raise SystemExit("topology set mismatch")

    verified = {}
    for record in records:
        name = record["id"]
        path = ROOT / record["schedule_file"]
        if sha256_file(path) != record["schedule_file_sha256"]:
            raise SystemExit(f"{name}: schedule file SHA mismatch")
        blocks = read_schedule(path)
        totals = validate_offsets_and_totals(name, blocks)
        validate_shape(name, blocks)
        if origin_mask_sha256(blocks) != record["language_origin_mask_sha256"]:
            raise SystemExit(f"{name}: origin-mask SHA mismatch")
        verified[name] = {
            "blocks": len(blocks),
            "english_tokens": totals["EN"],
            "tagalog_tokens": totals["TL"],
            "schedule_file_sha256": record["schedule_file_sha256"],
            "language_origin_mask_sha256": record["language_origin_mask_sha256"],
        }

    q8 = Q8_PATH.read_text(encoding="utf-8")
    for required in (
        hashes["addendum"]["sha256"],
        hashes["gate_plan"]["sha256"],
        hashes["topology_manifest"]["sha256"],
        "P6 #307969",
        "source-content",
        "M-fine-only",
        "random.Random(42)",
    ):
        if required not in q8:
            raise SystemExit(f"Q8 draft missing required text: {required}")

    print(
        json.dumps(
            {
                "status": "pass",
                "prefiling_only": True,
                "outcomes_accessed": False,
                "verified": verified,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
