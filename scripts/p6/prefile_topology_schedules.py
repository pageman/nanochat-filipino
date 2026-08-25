#!/usr/bin/env python3
"""Generate P6-M prefiling schedule files and a hash-pinned manifest.

This script is outcome-free. It defines language-origin schedules only; it does
not read corpora, checkpoints, validation data, or test data.
"""

from __future__ import annotations

import hashlib
import json
import platform
import random
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "manifests" / "p6" / "topology-schedules"
MANIFEST_PATH = ROOT / "manifests" / "p6" / "p6_topology_schedule_manifest.json"

D_PHASE2 = 19_267_584
TARGET_TL = 9_633_792
TARGET_EN = 9_633_792
FINE_BLOCK = 2_048
COARSE_BLOCK = 1_204_224  # TARGET_{TL,EN} / 8: exactly 8 blocks per language.
RAND_BLOCK = 2_048
RAND_SEED = 42

PLAN_SHA256 = "d8a63608608c59d2c4d9882e5346625462056c331094942a8a01d496697a1c79"
P4_SCHEDULE_DIGEST = "9a2c828d79ebd8c4c3a3463eb69c27345c55796d29002929583abe31f13878f2"
P4_ORIGIN_MASK_SHA256 = "140e174a427a7ddf2126553c53352ec049f72fbed475e2404cd4ef122b309c46"

# (language, source-language offset, length)
Block = Tuple[str, int, int]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def language_units(language: str, quota: int, block_length: int) -> List[Tuple[str, int]]:
    """Partition one language quota; the final unit is the exact residual."""
    units: List[Tuple[str, int]] = []
    remaining = quota
    while remaining:
        take = min(block_length, remaining)
        units.append((language, take))
        remaining -= take
    return units


def with_offsets(units: Sequence[Tuple[str, int]]) -> List[Block]:
    offsets = {"EN": 0, "TL": 0}
    blocks: List[Block] = []
    for language, length in units:
        blocks.append((language, offsets[language], length))
        offsets[language] += length
    return blocks


def alternating(block_length: int, first: str = "EN") -> List[Block]:
    per_language = {
        "EN": language_units("EN", TARGET_EN, block_length),
        "TL": language_units("TL", TARGET_TL, block_length),
    }
    order = (first, "TL" if first == "EN" else "EN")
    units: List[Tuple[str, int]] = []
    n = max(len(per_language["EN"]), len(per_language["TL"]))
    for i in range(n):
        for language in order:
            if i < len(per_language[language]):
                units.append(per_language[language][i])
    return with_offsets(units)


def blocked_tl_then_en() -> List[Block]:
    units = language_units("TL", TARGET_TL, TARGET_TL)
    units.extend(language_units("EN", TARGET_EN, TARGET_EN))
    return with_offsets(units)


def randomized_blocks() -> List[Block]:
    units = language_units("EN", TARGET_EN, RAND_BLOCK)
    units.extend(language_units("TL", TARGET_TL, RAND_BLOCK))
    random.Random(RAND_SEED).shuffle(units)
    return with_offsets(units)


def validate(name: str, blocks: Sequence[Block]) -> Dict[str, int]:
    totals = {"EN": 0, "TL": 0}
    next_offset = {"EN": 0, "TL": 0}
    for language, offset, length in blocks:
        if language not in totals:
            raise ValueError(f"{name}: invalid language {language}")
        if length <= 0:
            raise ValueError(f"{name}: non-positive block length")
        if offset != next_offset[language]:
            raise ValueError(
                f"{name}: noncontiguous {language} offset {offset} != {next_offset[language]}"
            )
        totals[language] += length
        next_offset[language] += length
    if totals != {"EN": TARGET_EN, "TL": TARGET_TL}:
        raise ValueError(f"{name}: quota mismatch {totals}")
    if sum(totals.values()) != D_PHASE2:
        raise ValueError(f"{name}: total mismatch")
    return totals


def serialize_tsv(blocks: Sequence[Block]) -> bytes:
    lines = ["block_index\tlanguage\tsource_offset_tokens\tlength_tokens"]
    lines.extend(
        f"{index}\t{language}\t{offset}\t{length}"
        for index, (language, offset, length) in enumerate(blocks)
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def origin_mask_sha256(blocks: Iterable[Block]) -> str:
    """Hash one byte per scheduled source-content token: EN=0, TL=1."""
    h = hashlib.sha256()
    for language, _offset, length in blocks:
        byte = b"\x00" if language == "EN" else b"\x01"
        chunk = byte * min(length, 1 << 20)
        remaining = length
        while remaining:
            take = min(remaining, len(chunk))
            h.update(chunk[:take])
            remaining -= take
    return h.hexdigest()


def topology_record(
    name: str,
    blocks: Sequence[Block],
    algorithm: str,
    block_length: int,
    start_rule: str,
    randomization: Dict[str, object],
) -> Dict[str, object]:
    totals = validate(name, blocks)
    path = OUT_DIR / f"{name}.tsv"
    path.write_bytes(serialize_tsv(blocks))
    return {
        "id": name,
        "role": "schedule_topology",
        "algorithm": algorithm,
        "block_unit": "source-content tokens under the carried-forward tokenizer",
        "nominal_block_length_tokens": block_length,
        "start_rule": start_rule,
        "final_partial_block_rule": (
            "for each language, use min(nominal_block_length, remaining_quota); "
            "the filed quotas are exactly divisible, so no partial block occurs"
        ),
        "no_wrap_rule": (
            "consume this precomputed schedule exactly once in block_index order; "
            "no runtime reshuffle, epoch regeneration, or wrap"
        ),
        "block_count": len(blocks),
        "english_block_count": sum(1 for language, _, _ in blocks if language == "EN"),
        "tagalog_block_count": sum(1 for language, _, _ in blocks if language == "TL"),
        "target_en_tokens": totals["EN"],
        "target_tl_tokens": totals["TL"],
        "schedule_file": str(path.relative_to(ROOT)),
        "schedule_file_sha256": sha256_file(path),
        "language_origin_mask_sha256": origin_mask_sha256(blocks),
        "randomization": randomization,
    }


def combined_digest(records: Sequence[Dict[str, object]]) -> str:
    h = hashlib.sha256()
    for record in sorted(records, key=lambda value: str(value["id"])):
        h.update(str(record["id"]).encode("utf-8"))
        h.update(b"\0")
        h.update(str(record["schedule_file_sha256"]).encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUT_DIR.glob("*.tsv"):
        stale.unlink()

    schedules = {
        "m-fine": alternating(FINE_BLOCK, first="EN"),
        "m-coarse": alternating(COARSE_BLOCK, first="EN"),
        "m-blocked": blocked_tl_then_en(),
        "m-rand": randomized_blocks(),
    }

    records = [
        topology_record(
            "m-fine",
            schedules["m-fine"],
            "alternate EN then TL blocks until both exact quotas are exhausted",
            FINE_BLOCK,
            "EN first; then strict EN/TL alternation",
            {"used": False, "seed": None},
        ),
        topology_record(
            "m-coarse",
            schedules["m-coarse"],
            "alternate eight EN and eight TL blocks until both exact quotas are exhausted",
            COARSE_BLOCK,
            "EN first; then strict EN/TL alternation",
            {"used": False, "seed": None},
        ),
        topology_record(
            "m-blocked",
            schedules["m-blocked"],
            "consume the complete TL quota, then the complete EN quota",
            TARGET_TL,
            "TL first; the language boundary is exactly token 9,633,792",
            {"used": False, "seed": None},
        ),
        topology_record(
            "m-rand",
            schedules["m-rand"],
            (
                "create 4,704 EN and 4,704 TL blocks of 2,048 tokens, shuffle the "
                "9,408-label multiset once, then persist the resulting sequence"
            ),
            RAND_BLOCK,
            "the first language is fixed by the persisted shuffled schedule",
            {
                "used": True,
                "library": "Python standard-library random.Random (MT19937)",
                "operation": "random.Random(42).shuffle on the complete block-label list",
                "seed": RAND_SEED,
                "unit": "2,048-source-content-token language block",
                "precomputed_once": True,
                "runtime_randomization_forbidden": True,
                "python_version_used": platform.python_version(),
            },
        ),
    ]

    generator_sha = sha256_file(Path(__file__))
    manifest = {
        "schema": "p6-m-prefiling-topology-schedules-v1",
        "status": "prefiling_no_outcomes",
        "study": "P6-M schedule-topology mechanism study",
        "authority_note": (
            "This manifest becomes controlling only if its SHA-256 is bound by the "
            "filed AsPredicted PDF or its SHA-bound addendum."
        ),
        "generator": str(Path(__file__).relative_to(ROOT)),
        "generator_sha256": generator_sha,
        "source_plan_sha256": PLAN_SHA256,
        "fixed_exposure": {
            "q_tl_source_content": 0.5,
            "q_en_source_content": 0.5,
            "d_phase2_model_visible_tokens": D_PHASE2,
            "target_tl_source_content_tokens": TARGET_TL,
            "target_en_source_content_tokens": TARGET_EN,
            "rounding_rule": "round-half-to-even TL target; EN is the exact residual",
            "english_document_order_seed": 42,
            "tagalog_document_order_seed": 42,
            "within_language_stream_rule": (
                "all arms consume the same preconstructed P4-lineage EN and TL token "
                "streams; only the cross-language block schedule differs"
            ),
            "within_language_document_order_rule": (
                "sort eligible train documents by SHA-256 of raw UTF-8 text, then "
                "independently apply Python random.Random(42).shuffle per language"
            ),
            "within_language_quota_fill_rule": (
                "follow the shuffled document list cyclically until the exact language "
                "quota is reached; truncate only the final document at a token boundary"
            ),
            "document_revisit_policy": (
                "carry forward P4 cyclic_per_language quota construction unchanged; "
                "P6-M does not vary this policy"
            ),
            "trainer_consumption_rule": (
                "consume the final mixed schedule once in stored block-index order with "
                "no trainer wrap or runtime reshuffle"
            ),
            "english_train_split_sha256": (
                "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a"
            ),
            "tagalog_train_split_sha256": (
                "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687"
            ),
            "tokenizer_sha256": (
                "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"
            ),
            "token_bytes_sha256": (
                "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132"
            ),
        },
        "p4_positive_control_reference": {
            "interleave_algorithm": "alternate_en_tl_blocks_of_K_blk_en_first",
            "k_blk": 2048,
            "block_schedule_digest": P4_SCHEDULE_DIGEST,
            "language_origin_mask_sha256": P4_ORIGIN_MASK_SHA256,
        },
        "schedule_serialization": (
            "UTF-8 TSV with one header and ordered rows: "
            "block_index, language, source_offset_tokens, length_tokens"
        ),
        "topologies": records,
        "combined_schedule_files_sha256": combined_digest(records),
        "outcomes_accessed": False,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "manifest": str(MANIFEST_PATH.relative_to(ROOT)),
                "manifest_sha256": sha256_file(MANIFEST_PATH),
                "combined_schedule_files_sha256": manifest[
                    "combined_schedule_files_sha256"
                ],
                "topologies": {
                    record["id"]: {
                        "blocks": record["block_count"],
                        "schedule_file_sha256": record["schedule_file_sha256"],
                        "language_origin_mask_sha256": record[
                            "language_origin_mask_sha256"
                        ],
                    }
                    for record in records
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
