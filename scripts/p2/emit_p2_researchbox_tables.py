#!/usr/bin/env python3
"""Emit ResearchBox-legal CSV/TSV tables from sealed P2 JSON. No test.jsonl, no passcodes."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def public_name(name: str) -> str:
    """Avoid ResearchBox Prolific-ID false positives on *sha256* column names."""
    return name.replace("checkpoint_sha256", "model_weights_file_digest").replace("sha256", "file_digest")


def public_value(value: object) -> str:
    if value is None:
        return ""
    s = str(value)
    if HEX64.fullmatch(s):
        return "sha2-256:" + s.lower()
    return s


STUDY_PREAMBLE = (
    "P2 (study_id NANOCHAT-FILIPINO-P2-EN-TL; AsPredicted #306935; ResearchBox 8763; "
    "run p2-20260817T150944Z-de99f8a) is a one-seed nanochat language-model experiment: "
    "WikiText-103 English then WikiText-TL-39 Tagalog. It does not amend AsPredicted #306780 "
    "or ResearchBox 8735. There are no human participants, no surveys, and no Prolific IDs. "
    "Cells that look like long hex strings are SHA-2-256 fingerprints of files (weights, "
    "jsonl, tokenizer), prefixed sha2-256:, not people."
)

FAMILY_BLURB = {
    "identity": "Immutable study lock metadata (passcode never stored).",
    "val_bpb_full": "Sealed full-validation bits-per-byte (Gate U). Primary C_en and G_tl use A1 vs A2 at depth 20 only.",
    "val_eval_detail": "Packing/scoring diagnostics for the Gate U full-val pass (nats, bytes, token counts). Same BPB as val_bpb_full.",
    "checkpoint": "Which trained weight file this arm used. Hex digest is the model_*.pt file, not a person.",
    "contrast": "Registered contrasts. C_en = EN(A2)-EN(A1), filed >=0.01 (not observed). G_tl = TL(A2)-TL(A1), filed <=-0.01 (observed in this one-seed apparatus). A3 contrasts are descriptive trade-offs, not mitigation.",
    "gate_u_meta": "Gate U seal protocol (evaluator, packing, tokenizer identity, test-read count at seal time was 0).",
    "test_bpb": "Gate V secondary test BPB, A2 only. Does not alter sealed C_en/G_tl. A1 and A3 were never tested.",
    "gate_v_meta": "Gate V authorization and protocol. One authorized touch; two component evaluations.",
    "test_ledger": "P2 test-access ledger (not the P1.1 ledger). Authorized touches=1.",
    "a3_shares": "A3 50/50-document mix realization. Documents are equated, bytes and BPE tokens are not. Not a mitigation arm.",
    "exposure": "Unique documents/bytes/BPE tokens in each phase-2 stream and revisit = D_phase2 / unique_BPE_tokens. Not used to pick arms.",
    "drop_audit": "Audit of frozen kept train jsonl under length/empty rules. Units already absent from the kept file are not reconstructable here.",
    "q8": "AsPredicted Q8 descriptive items (trajectory, PTPP R_d, fertility, P1.1-on-English OOD). Several items were not collected; that is reported, not rescued post-outcome.",
    "bpe_counts": "English-BPE token/byte/document counts on frozen train text with no BOS, packing, or crop.",
    "p0_baselines": "Gate P0 English val floors (untrained, byte-unigram, EN0 d8/d20). P0-E requires EN0 to beat untrained by >=0.01 BPB.",
    "fertility": "Descriptive bytes/token of the English 32768 BPE on val text. Not forgetting evidence.",
    "tokenizer": "Gate F English BPE train (vocab 32768). P1.1 tokenizer was not reused.",
    "budget": "Gate G token budget: T_en_train, N_EN0=5415, D_phase2=19267584, B=65536.",
    "byte_unigram": "Laplace-add-one byte unigram BPB on English val. A floor, not a neural model.",
}

ARM_BLURB = {
    "Untrained": "Same-depth randomly initialized network (no EN0). English val floor only.",
    "A0": "Frozen EN0 d20 parent after English-only pretraining (5415 steps). No additional phase-2 tokens.",
    "A0_d8": "Shallower EN0 diagnostic (depth 8). Not an input to confirmatory C_en/G_tl.",
    "A1": "Phase-2 extra-English control (294 steps from frozen A0). Never tested.",
    "A2": "Phase-2 Tagalog continuation (treatment; 294 steps from frozen A0). Only arm with authorized test reads.",
    "A3": "Phase-2 50/50-document English+Tagalog mix (trade-off, not mitigation). Never tested.",
    "P1.1_d20_descriptive": "P1.1 native Tagalog BPE result. Different tokenizer; not a C_en/G_tl input. Do not reuse P1.1 test_bpb=1.164768.",
}

LANG_BLURB = {
    "english": "English / WikiText-103-raw under P2 English 32768 BPE.",
    "tagalog": "Tagalog / WikiText-TL-39 under the same P2 English BPE (not P1.1 native BPE).",
}

SPLIT_BLURB = {
    "train": "Training stream (or mix). Raw test jsonl is never in this packet.",
    "val": "Official validation. Confirmatory metric is val_bpb_full, not in-loop val.",
    "test": "Holdout. English = official WT103-raw test; Tagalog = P1.1 legacy test.jsonl. Raw text excluded; identity digest only. A2 only.",
}

FIELD_BLURB = {
    "val_bpb_full": "Bits per UTF-8 byte on the full official val set (not the in-loop eval cap).",
    "bpb": "Bits per UTF-8 byte = total_nats / (total_bytes * ln 2).",
    "total_nats": "Sum of token NLL in nats over scored positions.",
    "total_bytes": "UTF-8 byte denominator for BPB.",
    "n_scored_tokens": "Token positions contributing to NLL (BOS/pad excluded per packing rules).",
    "n_excluded_positions": "Positions present in packed rows but not scored.",
    "n_source_docs": "Documents drawn from the split for this packed pass.",
    "n_rows": "Packed sequences of length T.",
    "n_batches": "Forward batches at device_batch_size=8.",
    "n_docs_packed": "Documents that entered best-fit packing.",
    "n_cropped_fills": "Packing fills that cropped a document to finish a row.",
    "n_padded_positions": "Pad tokens inserted after best-fit packing.",
    "wall_sec": "Wall-clock seconds for that eval pass (not a scientific outcome).",
    "model_weights_file_digest": "SHA-2-256 of model_*.pt weights. File fingerprint, not a participant ID.",
    "checkpoint_step": "Optimizer/data step index of the saved weights (EN0=5415; phase-2 children=294).",
    "model_tag": "Run directory tag for this arm.",
    "C_en.delta": "EN_val_bpb_full(A2)-EN_val_bpb_full(A1). Filed prediction >=0.01; observed -0.073991 (not observed as filed).",
    "G_tl.delta": "TL_val_bpb_full(A2)-TL_val_bpb_full(A1). Filed prediction <=-0.01; observed -3.883048 (observed in this one-seed apparatus).",
    "revisit_epochs": "D_phase2 / unique_BPE_tokens in the phase-2 stream. Values <1 mean the unique stream was not fully replayed.",
    "document_share_en": "Fraction of A3 mix documents that are English (0.5 by construction; K=28472).",
    "document_share_tl": "Fraction of A3 mix documents that are Tagalog (0.5 by construction).",
    "byte_share_en": "UTF-8 byte share of the A3 mix that is English (~0.961). Not token-equated.",
    "byte_share_tl": "UTF-8 byte share of the A3 mix that is Tagalog (~0.039). Not token-equated.",
    "token_share_en": "English-BPE token share of the A3 mix that is English (~0.933). Not the registered mix unit.",
    "token_share_tl": "English-BPE token share of the A3 mix that is Tagalog (~0.067). Not the registered mix unit.",
    "does_not_amend_306780": "Legal/preregistration independence: P2 does not change P1.1.",
    "aspredicted_id": "AsPredicted preregistration number 306935.",
    "researchbox_id": "ResearchBox deposit 8763.",
    "packing": "bos_bestfit_buffer1000_one_pass_no_wrap: BOS-aware best-fit packing, one pass, no wrap.",
    "stride": "non_overlapping_T_official_bos_bestfit: non-overlapping length-T rows.",
    "T": "Sequence length 2048.",
    "device_batch_size": "Per-step microbatch 8 on the eval GPU.",
    "bytes_per_token": "Mean UTF-8 bytes per BPE token on that val set (fertility; descriptive).",
    "val_bpb_unigram": "Byte-unigram (Laplace +1) BPB on English val (~4.583).",
    "untrained_english_val_bpb": "Untrained d20 English val BPB (~3.247).",
    "D_phase2": "Phase-2 token budget 19,267,584 = 294 * 65536 (P1.1 D_actual, not English D_3x).",
    "N_EN0": "EN0 iterations 5415 = ceil(D_3x_en / 65536).",
    "N_phase2": "Phase-2 iterations 294.",
    "B": "Global token batch 65536.",
    "t_en_train": "English train BPE tokens with no BOS/pack/crop (118,286,771).",
    "authorized_touches": "Count of authorized P2 test-set openings. Final=1 (Gate V).",
    "test_read_count": "Test-read events recorded at that gate. Gate U sealed with 0; Gate V then used the one authorized touch.",
    "p11_test_bpb_not_reused": "P1.1 native-BPE test_bpb=1.164768 is not a P2 number.",
    "a1_tested": "Whether A1 official tests were run. False.",
    "a3_tested": "Whether A3 official tests were run. False.",
    "one_seed_point_estimates_only": "No multi-seed interval. Point estimates from this apparatus only.",
    "inloop_val_is_not_val_bpb_full": "Trainer in-loop Validation bpb is a capped diagnostic, not the sealed metric.",
}


def field_key(field: str) -> str:
    f = public_name(field)
    if f in FIELD_BLURB:
        return f
    tail = f.split(".")[-1]
    if tail in FIELD_BLURB:
        return tail
    return f


def confirmatory_role(row: dict) -> str:
    family = row.get("family", "")
    field = row.get("field", "")
    arm = row.get("arm", "")
    lang = row.get("language", "")
    if family == "val_bpb_full" and arm in {"A1", "A2"} and field == "val_bpb_full":
        return "primary_input_to_C_en_or_G_tl"
    if family == "contrast" and ("C_en." in field and "A3" not in field):
        return "primary_C_en"
    if family == "contrast" and ("G_tl." in field and "A3" not in field):
        return "primary_G_tl"
    if family in {"test_bpb", "test_ledger"}:
        return "secondary_A2_test_does_not_alter_seal"
    if family in {"a3_shares", "exposure", "q8", "fertility", "byte_unigram", "p0_baselines"}:
        return "descriptive_registered_or_floor"
    if family == "identity":
        return "study_identity_metadata"
    return "supporting_protocol_or_diagnostic"


def privacy_class(row: dict) -> str:
    val = str(row.get("value", ""))
    field = str(row.get("field", ""))
    if val.startswith("sha2-256:") or "digest" in field or "file_digest" in field:
        return "file_fingerprint_not_participant"
    return "not_human_identifier"


def describe_fact(row: dict) -> str:
    family = row.get("family", "")
    arm = row.get("arm", "")
    lang = row.get("language", "")
    split = row.get("split", "")
    field = row.get("field", "")
    value = row.get("value", "")
    unit = row.get("unit", "")
    source = row.get("source_file", "")
    authority = row.get("authority", "")
    note = row.get("note", "")
    table = row.get("table_name", "")
    parts = [STUDY_PREAMBLE, FAMILY_BLURB.get(family, f"Family `{family}` is supporting P2 documentation.")]
    if arm:
        parts.append("Arm " + arm + ": " + ARM_BLURB.get(arm, arm + " is a P2 training or reference condition."))
    if lang:
        parts.append(LANG_BLURB.get(lang, f"Language `{lang}`."))
    if split:
        parts.append("Split `" + split + "`: " + SPLIT_BLURB.get(split, split + "."))
    fk = field_key(field)
    fblurb = FIELD_BLURB.get(fk) or FIELD_BLURB.get(field.split(".")[-1], "")
    if not fblurb:
        if "file_digest" in field or field.endswith("_digest"):
            fblurb = (
                "SHA-2-256 fingerprint of a file (weights, tokenizer, jsonl, or mix-order). "
                "Prefixed sha2-256:. Not a Prolific ID and not a human participant."
            )
        elif field.endswith("_at_utc") or field.endswith("at_utc"):
            fblurb = "UTC timestamp when that gate or eval finished."
        elif field.endswith("_status"):
            fblurb = "Gate status recorded in the lock (pass / pass_with_operator_remainder)."
        elif "json" in field and field.endswith("json"):
            fblurb = "Repository path of the JSON receipt that is the authority for a sibling fact. Receipts live in Other, not as loose Data json."
        elif field.startswith("gate_"):
            fblurb = "Protocol/lock field for a sequential P2 gate (A–W). Not a human-subjects variable."
        else:
            fblurb = (
                "Protocol, hash, count, or flag from the named source JSON. "
                "Interpret with family/table_name; do not treat as a survey item or participant ID."
            )
    parts.append(f"Field `{field}`: {fblurb}")
    unit_bit = f" Unit: {unit}." if unit else ""
    parts.append(f"Recorded value: {value}.{unit_bit}")
    parts.append(f"Table `{table}`; source file `{source}`; authority `{authority}`.")
    role = confirmatory_role(row)
    parts.append(f"Confirmatory role: {role}.")
    parts.append(f"Privacy class: {privacy_class(row)}.")
    if note:
        parts.append("Row note: " + note + ".")
    parts.append(
        "Empty value means not measured for this arm/language/split, not a missing participant. "
        "Do not reuse P1.1 native-BPE test_bpb=1.164768. In-loop Validation bpb is not val_bpb_full. "
        "Raw english_test.jsonl and tagalog test.jsonl are excluded from this deposit."
    )
    return " ".join(parts)

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
CARDS = ROOT / "docs/run-cards/p2/p2-20260817T150944Z-de99f8a"
PAPER = ROOT / "docs/papers/p2-cf-english"
SKIP_KEYS = {"c", "researchbox_passcode"}
SKIP_PREFIXES = ("gpu_host",)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def flatten(obj, prefix: str = "") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in SKIP_KEYS or k.startswith(SKIP_PREFIXES):
                continue
            key = f"{prefix}.{k}" if prefix else str(k)
            out.extend(flatten(v, key))
        return out
    if isinstance(obj, list):
        if not obj:
            out.append((prefix, ""))
            return out
        if all(isinstance(x, (str, int, float, bool)) or x is None for x in obj):
            if len(obj) > 32:
                out.append((prefix, f"<list_len_{len(obj)}>"))
            else:
                out.append((prefix, " | ".join("" if x is None else str(x) for x in obj)))
            return out
        for i, item in enumerate(obj):
            out.extend(flatten(item, f"{prefix}[{i}]"))
        return out
    if obj is None:
        out.append((prefix, ""))
    elif isinstance(obj, bool):
        out.append((prefix, "true" if obj else "false"))
    else:
        out.append((prefix, str(obj)))
    return out


def write_tsv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def emit(dest: Path) -> dict:
    dest.mkdir(parents=True, exist_ok=True)
    seal = load(CARDS / "gate-u-seal.json")
    gate_v = load(CARDS / "gate-v-test.json")
    reporting = load(CARDS / "registered-reporting-q3-q8.json")
    lock = load(PAPER / "LOCK.json")
    lock.pop("researchbox_passcode", None)
    p0 = load(CARDS / "gate_p0_val_baselines.json")
    gate_f = load(CARDS / "gate-f-tokenizer.json")
    gate_g = load(CARDS / "gate-g-budget.json")
    byte_u = load(CARDS / "byte_unigram_english_val.json")
    ledger = load(ROOT / "docs/run-cards/p2/test_access_log.json")

    study = "NANOCHAT-FILIPINO-P2-EN-TL"
    asp = "306935"
    run = "p2-20260817T150944Z-de99f8a"

    long_fields = [
        "study_id",
        "aspredicted_id",
        "run_id",
        "family",
        "arm",
        "language",
        "split",
        "field",
        "value",
        "description",
        "unit",
        "table_name",
        "confirmatory_role",
        "privacy_class",
        "source_file",
        "authority",
        "note",
    ]
    long_rows: list[dict] = []

    def add(**kwargs) -> None:
        row = {
            "study_id": study,
            "aspredicted_id": asp,
            "run_id": run,
            "family": "",
            "table_name": "",
            "arm": "",
            "language": "",
            "split": "",
            "field": "",
            "value": "",
            "unit": "",
            "source_file": "",
            "authority": "",
            "note": "",
        }
        row.update(kwargs)
        row["field"] = public_name(str(row.get("field", "")))
        row["value"] = public_value(row.get("value"))
        row["confirmatory_role"] = confirmatory_role(row)
        row["privacy_class"] = privacy_class(row)
        row["description"] = describe_fact(row)
        long_rows.append(row)

    # --- identity / lock (no passcode) ---
    for field, value in flatten(lock):
        add(
            family="identity",
            table_name="LOCK",
            field=field,
            value=value,
            source_file="LOCK.json",
            authority="lock_sanitized",
            note="passcode stripped",
        )

    # --- Gate U table + cells + contrasts ---
    for arm, cell in seal["table_d20"].items():
        add(
            family="val_bpb_full",
            table_name="gate_u_table_d20",
            arm=arm,
            language="english",
            split="val",
            field="val_bpb_full",
            value=cell.get("english_val_bpb_full"),
            unit="bpb",
            source_file="gate-u-seal.json",
            authority="gate_u_seal",
            note=cell.get("note") or cell.get("tagalog_note") or "",
        )
        add(
            family="val_bpb_full",
            table_name="gate_u_table_d20",
            arm=arm,
            language="tagalog",
            split="val",
            field="val_bpb_full",
            value=cell.get("tagalog_val_bpb_full"),
            unit="bpb",
            source_file="gate-u-seal.json",
            authority="gate_u_seal",
            note=cell.get("note") or cell.get("tagalog_note") or "",
        )
    for arm, cell in seal["cells"].items():
        for lang in ("english", "tagalog"):
            pack = cell[lang]
            for field, value in pack.items():
                unit = "bpb" if field == "bpb" else ""
                add(
                    family="val_eval_detail",
                    table_name="gate_u_cells",
                    arm=arm,
                    language=lang,
                    split="val",
                    field=field,
                    value=value,
                    unit=unit,
                    source_file="gate-u-seal.json",
                    authority="gate_u_seal",
                )
        add(
            family="checkpoint",
            table_name="gate_u_cells",
            arm=arm,
            field="model_weights_file_digest",
            value=cell["checkpoint_sha256"],
            source_file="gate-u-seal.json",
            authority="gate_u_seal",
        )
        add(
            family="checkpoint",
            table_name="gate_u_cells",
            arm=arm,
            field="checkpoint_step",
            value=cell["checkpoint_step"],
            source_file="gate-u-seal.json",
            authority="gate_u_seal",
        )
        add(
            family="checkpoint",
            table_name="gate_u_cells",
            arm=arm,
            field="model_tag",
            value=cell["model_tag"],
            source_file="gate-u-seal.json",
            authority="gate_u_seal",
        )
    for name, c in seal["contrasts"].items():
        for field, value in c.items():
            add(
                family="contrast",
                table_name="gate_u_contrasts",
                field=f"{name}.{field}",
                value=value,
                unit="bpb" if field in {"delta", "abs_delta"} else "",
                source_file="gate-u-seal.json",
                authority="gate_u_seal",
            )
    for field, value in flatten({k: v for k, v in seal.items() if k not in {"table_d20", "cells", "contrasts"}}):
        add(
            family="gate_u_meta",
            table_name="gate_u_seal",
            field=field,
            value=value,
            source_file="gate-u-seal.json",
            authority="gate_u_seal",
        )

    # --- Gate V / test (A2 only) ---
    for lang in ("english", "tagalog"):
        pack = gate_v[lang]
        for field, value in pack.items():
            add(
                family="test_bpb",
                table_name="gate_v_test",
                arm="A2",
                language=lang,
                split="test",
                field=field,
                value=value,
                unit="bpb" if field == "bpb" else "",
                source_file="gate-v-test.json",
                authority="gate_v_test",
                note="secondary; does not alter C_en/G_tl; A1/A3 never tested",
            )
    for field, value in flatten({k: v for k, v in gate_v.items() if k not in {"english", "tagalog"}}):
        add(
            family="gate_v_meta",
            table_name="gate_v_test",
            arm="A2",
            field=field,
            value=value,
            source_file="gate-v-test.json",
            authority="gate_v_test",
        )
    for i, ev in enumerate(ledger["events"]):
        for field, value in ev.items():
            add(
                family="test_ledger",
                table_name="test_access_log",
                arm="A2",
                language=ev.get("component", ""),
                split="test",
                field=f"event[{i}].{field}",
                value=value,
                source_file="test_access_log.json",
                authority="p2_test_ledger",
            )
    for field, value in flatten({k: v for k, v in ledger.items() if k != "events"}):
        add(
            family="test_ledger",
            table_name="test_access_log",
            field=field,
            value=value,
            source_file="test_access_log.json",
            authority="p2_test_ledger",
        )

    # --- exposure / A3 shares / Q8 ---
    for field, value in flatten(reporting["a3_realized_shares"]):
        add(
            family="a3_shares",
            table_name="a3_realized_shares",
            arm="A3",
            field=field,
            value=value,
            source_file="registered-reporting-q3-q8.json",
            authority="registered_reporting_reconstruction",
            note="50/50 documents not token-equated; not mitigation",
        )
    for row in reporting["exposure_table"]:
        arm = row["arm"]
        for field, value in row.items():
            if field == "arm":
                continue
            add(
                family="exposure",
                table_name="exposure_by_arm",
                arm=arm,
                field=field,
                value=value,
                source_file="registered-reporting-q3-q8.json",
                authority="registered_reporting_reconstruction",
            )
    for field, value in flatten(reporting["drop_audit"]):
        add(
            family="drop_audit",
            table_name="drop_audit",
            field=field,
            value=value,
            source_file="registered-reporting-q3-q8.json",
            authority="registered_reporting_reconstruction",
        )
    for field, value in flatten(reporting["q8_descriptive_status"]):
        add(
            family="q8",
            table_name="q8_descriptive_status",
            field=field,
            value=value,
            source_file="registered-reporting-q3-q8.json",
            authority="registered_reporting_reconstruction",
        )
    for field, value in flatten(reporting["a2_full_tagalog_train_bpe"]):
        add(
            family="bpe_counts",
            table_name="a2_full_tagalog_train_bpe",
            arm="A2",
            language="tagalog",
            split="train",
            field=field,
            value=value,
            source_file="registered-reporting-q3-q8.json",
            authority="registered_reporting_reconstruction",
        )
    for field, value in flatten(reporting["a3_mix_tagalog_subset_bpe"]):
        add(
            family="bpe_counts",
            table_name="a3_mix_tagalog_subset_bpe",
            arm="A3",
            language="tagalog",
            split="train",
            field=field,
            value=value,
            source_file="registered-reporting-q3-q8.json",
            authority="registered_reporting_reconstruction",
        )

    # --- floors / tokenizer / budget ---
    for field, value in flatten(p0):
        add(
            family="p0_baselines",
            table_name="gate_p0_val_baselines",
            field=field,
            value=value,
            source_file="gate_p0_val_baselines.json",
            authority="gate_p0",
        )
    fert = gate_f.get("fertility", {})
    for lang_key, lang in (("english_val", "english"), ("tagalog_val", "tagalog")):
        pack = fert.get(lang_key, {})
        for field, value in pack.items():
            add(
                family="fertility",
                table_name="gate_f_tokenizer",
                language=lang,
                split="val",
                field=field,
                value=value,
                source_file="gate-f-tokenizer.json",
                authority="gate_f_descriptive",
                note="not forgetting evidence",
            )
    for field, value in flatten({k: v for k, v in gate_f.items() if k != "fertility"}):
        add(
            family="tokenizer",
            table_name="gate_f_tokenizer",
            field=field,
            value=value,
            source_file="gate-f-tokenizer.json",
            authority="gate_f",
        )
    for field, value in flatten(gate_g):
        add(
            family="budget",
            table_name="gate_g_budget",
            field=field,
            value=value,
            source_file="gate-g-budget.json",
            authority="gate_g",
        )
    for field, value in flatten({k: v for k, v in byte_u.items() if k != "c"}):
        add(
            family="byte_unigram",
            table_name="byte_unigram_english_val",
            language="english",
            split="val",
            field=field,
            value=value,
            unit="bpb" if field in {"bpb", "val_bpb_unigram"} else "",
            source_file="byte_unigram_english_val.json",
            authority="byte_unigram",
        )

    n_data = len(long_rows)
    manifest = {k: "" for k in long_fields}
    manifest.update(
        {
            "study_id": study,
            "aspredicted_id": asp,
            "run_id": run,
            "family": "file_manifest",
            "table_name": "p2_facts_long",
            "field": "this_file",
            "value": str(n_data),
            "unit": "sealed_fact_rows_after_this_manifest",
            "source_file": "p2_facts_long.csv",
            "authority": "emit_p2_researchbox_tables.py",
            "confirmatory_role": "file_manifest",
            "privacy_class": "not_human_identifier",
            "description": (
                "p2_facts_long.csv and p2_facts_long.tsv are regenerated with a description on every row. "
                "They are at /Users/paulpajo/Downloads/nanochat-filipino/P2/Data/ "
                f"({n_data} sealed-fact rows plus this manifest row). "
                "Open the .csv in Excel/Numbers as comma-separated; open the .tsv as tab-separated. "
                "Column description is the 10th column, immediately after value. "
                "If a viewer shows only the first few columns, scroll right to description, or use p2_facts_readable.csv "
                "which is field, value, description only. Every subsequent row has a non-empty description. "
                "P2 has no human participants; hex file digests are not Prolific IDs."
            ),
        }
    )
    long_rows.insert(0, manifest)
    write_tsv(dest / "p2_facts_long.tsv", long_rows, long_fields)
    write_csv(dest / "p2_facts_long.csv", long_rows, long_fields)
    readable_fields = ["field", "value", "description", "family", "arm", "language", "split", "confirmatory_role"]
    write_csv(dest / "p2_facts_readable.csv", long_rows, readable_fields)
    with (dest / "p2_row_descriptions.csv").open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["row", "family", "arm", "language", "split", "field", "value", "description"],
        )
        w.writeheader()
        for i, r in enumerate(long_rows, start=1):
            w.writerow(
                {
                    "row": i,
                    "family": r.get("family", ""),
                    "arm": r.get("arm", ""),
                    "language": r.get("language", ""),
                    "split": r.get("split", ""),
                    "field": r.get("field", ""),
                    "value": r.get("value", ""),
                    "description": r.get("description", ""),
                }
            )

    # --- super-exhaustive arm × language × split crosstab ---
    shares = reporting["a3_realized_shares"]
    exp = {r["arm"]: r for r in reporting["exposure_table"]}
    cells = seal["cells"]
    table = seal["table_d20"]
    copied = seal["copied_not_recomputed"]

    def cell_pack(arm: str, lang: str) -> dict:
        if arm in cells:
            return cells[arm][lang]
        return {}

    crosstab_fields = [
        "study_id",
        "aspredicted_id",
        "run_id",
        "arm",
        "depth",
        "role",
        "model_tag",
        "checkpoint_step",
        "model_weights_file_digest",
        "english_val_bpb_full",
        "tagalog_val_bpb_full",
        "english_test_bpb",
        "tagalog_test_bpb",
        "C_en_vs_A1",
        "G_tl_vs_A1",
        "filed_C_en_rule",
        "filed_G_tl_rule",
        "C_en_observed_as_filed",
        "G_tl_observed_as_filed",
        "english_val_total_nats",
        "english_val_total_bytes",
        "english_val_n_scored_tokens",
        "english_val_n_excluded_positions",
        "english_val_n_source_docs",
        "english_val_n_rows",
        "english_val_n_batches",
        "english_val_n_docs_packed",
        "english_val_n_cropped_fills",
        "english_val_n_padded_positions",
        "english_val_wall_sec",
        "tagalog_val_total_nats",
        "tagalog_val_total_bytes",
        "tagalog_val_n_scored_tokens",
        "tagalog_val_n_excluded_positions",
        "tagalog_val_n_source_docs",
        "tagalog_val_n_rows",
        "tagalog_val_n_batches",
        "tagalog_val_n_docs_packed",
        "tagalog_val_n_cropped_fills",
        "tagalog_val_n_padded_positions",
        "tagalog_val_wall_sec",
        "english_test_total_nats",
        "english_test_total_bytes",
        "english_test_n_scored_tokens",
        "english_test_file_digest",
        "english_test_at_utc",
        "tagalog_test_total_nats",
        "tagalog_test_total_bytes",
        "tagalog_test_n_scored_tokens",
        "tagalog_test_file_digest",
        "tagalog_test_at_utc",
        "phase2_unique_documents",
        "phase2_canonical_utf8_bytes",
        "phase2_unique_bpe_tokens_no_bos",
        "D_phase2",
        "revisit_epochs",
        "phase2_stream",
        "a3_document_share_en",
        "a3_document_share_tl",
        "a3_byte_share_en",
        "a3_byte_share_tl",
        "a3_token_share_en",
        "a3_token_share_tl",
        "a3_utf8_bytes_en",
        "a3_utf8_bytes_tl",
        "a3_bpe_tokens_en",
        "a3_bpe_tokens_tl",
        "a3_K",
        "a3_mix_order_file_digest",
        "tokenizer_pkl_file_digest",
        "token_bytes_pt_file_digest",
        "english_val_fertility_bytes_per_token",
        "tagalog_val_fertility_bytes_per_token",
        "byte_unigram_english_val_bpb",
        "T",
        "device_batch_size",
        "packing",
        "stride",
        "test_authorized_for_this_arm",
        "alters_sealed_C_en_or_G_tl",
        "p11_test_bpb_must_not_reuse",
        "one_seed_point_estimate",
        "does_not_amend_306780",
        "note",
    ]

    tok_pkl = "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6"
    tok_pt = "5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42"
    fert_en = fert.get("english_val", {}).get("bytes_per_token", "")
    fert_tl = fert.get("tagalog_val", {}).get("bytes_per_token", "")

    def base_row(arm: str, role: str, note: str) -> dict:
        en_pack = cell_pack(arm, "english")
        tl_pack = cell_pack(arm, "tagalog")
        tcell = table.get(arm, {})
        e = exp.get(arm, {})
        ck = cells.get(arm, {})
        row = {k: "" for k in crosstab_fields}
        row.update(
            {
                "study_id": study,
                "aspredicted_id": asp,
                "run_id": run,
                "arm": arm,
                "depth": 20,
                "role": role,
                "model_tag": ck.get("model_tag", ""),
                "checkpoint_step": ck.get("checkpoint_step", ""),
                "model_weights_file_digest": public_value(ck.get("checkpoint_sha256", "")),
                "english_val_bpb_full": tcell.get("english_val_bpb_full", ""),
                "tagalog_val_bpb_full": tcell.get("tagalog_val_bpb_full", ""),
                "filed_C_en_rule": ">=0.01",
                "filed_G_tl_rule": "<=-0.01",
                "C_en_observed_as_filed": "false",
                "G_tl_observed_as_filed": "true",
                "english_val_total_nats": en_pack.get("total_nats", ""),
                "english_val_total_bytes": en_pack.get("total_bytes", ""),
                "english_val_n_scored_tokens": en_pack.get("n_scored_tokens", ""),
                "english_val_n_excluded_positions": en_pack.get("n_excluded_positions", ""),
                "english_val_n_source_docs": en_pack.get("n_source_docs", ""),
                "english_val_n_rows": en_pack.get("n_rows", ""),
                "english_val_n_batches": en_pack.get("n_batches", ""),
                "english_val_n_docs_packed": en_pack.get("n_docs_packed", ""),
                "english_val_n_cropped_fills": en_pack.get("n_cropped_fills", ""),
                "english_val_n_padded_positions": en_pack.get("n_padded_positions", ""),
                "english_val_wall_sec": en_pack.get("wall_sec", ""),
                "tagalog_val_total_nats": tl_pack.get("total_nats", ""),
                "tagalog_val_total_bytes": tl_pack.get("total_bytes", ""),
                "tagalog_val_n_scored_tokens": tl_pack.get("n_scored_tokens", ""),
                "tagalog_val_n_excluded_positions": tl_pack.get("n_excluded_positions", ""),
                "tagalog_val_n_source_docs": tl_pack.get("n_source_docs", ""),
                "tagalog_val_n_rows": tl_pack.get("n_rows", ""),
                "tagalog_val_n_batches": tl_pack.get("n_batches", ""),
                "tagalog_val_n_docs_packed": tl_pack.get("n_docs_packed", ""),
                "tagalog_val_n_cropped_fills": tl_pack.get("n_cropped_fills", ""),
                "tagalog_val_n_padded_positions": tl_pack.get("n_padded_positions", ""),
                "tagalog_val_wall_sec": tl_pack.get("wall_sec", ""),
                "phase2_unique_documents": e.get("unique_documents", ""),
                "phase2_canonical_utf8_bytes": e.get("canonical_utf8_bytes", ""),
                "phase2_unique_bpe_tokens_no_bos": e.get("unique_bpe_tokens_no_bos", ""),
                "D_phase2": 19267584,
                "revisit_epochs": e.get("revisit_epochs", ""),
                "phase2_stream": e.get("stream", ""),
                "tokenizer_pkl_file_digest": public_value(tok_pkl),
                "token_bytes_pt_file_digest": public_value(tok_pt),
                "english_val_fertility_bytes_per_token": fert_en,
                "tagalog_val_fertility_bytes_per_token": fert_tl,
                "byte_unigram_english_val_bpb": copied["byte_unigram_english_val_bpb"],
                "T": 2048,
                "device_batch_size": 8,
                "packing": seal["packing"],
                "stride": seal["stride"],
                "test_authorized_for_this_arm": "false",
                "alters_sealed_C_en_or_G_tl": "false",
                "p11_test_bpb_must_not_reuse": "1.164768",
                "one_seed_point_estimate": "true",
                "does_not_amend_306780": "true",
                "note": note,
            }
        )
        for k, v in list(row.items()):
            if v is None:
                row[k] = ""
            else:
                row[k] = public_value(v) if HEX64.fullmatch(str(v)) else v
        return row

    rows = []
    rows.append(
        base_row(
            "Untrained",
            "same-depth untrained English floor",
            "Tagalog val not required for C_en/G_tl; not recomputed",
        )
    )
    a0 = base_row(
        "A0",
        "frozen EN0 d20 parent",
        "English from P0-E; Tagalog CUDA Gate Q; additional train tokens 0",
    )
    a0["model_weights_file_digest"] = public_value("bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d")
    a0["checkpoint_step"] = 5415
    a0["model_tag"] = "p2-en0-d20"
    rows.append(a0)

    a0d8 = base_row("A0_d8", "diagnostic shallower EN0; not C_en/G_tl", "d8 English val 0.983292; Tagalog 4.082488; not confirmatory table")
    a0d8["depth"] = 8
    a0d8["english_val_bpb_full"] = lock["a0_d8_english_val_bpb_full"]
    a0d8["tagalog_val_bpb_full"] = lock["a0_d8_tagalog_val_bpb_full"]
    a0d8["model_weights_file_digest"] = public_value(lock["gate_i_en0_d8_ckpt_sha256"])
    a0d8["model_tag"] = "p2-en0-d8"
    rows.append(a0d8)

    a1 = base_row("A1", "extra-English control", "Phase-2 extra English; never tested")
    a1["C_en_vs_A1"] = 0
    a1["G_tl_vs_A1"] = 0
    rows.append(a1)

    a2 = base_row("A2", "Tagalog continuation (treatment)", "Only arm with authorized test; secondary; does not alter C_en/G_tl")
    a2["C_en_vs_A1"] = seal["contrasts"]["C_en"]["delta"]
    a2["G_tl_vs_A1"] = seal["contrasts"]["G_tl"]["delta"]
    a2["english_test_bpb"] = gate_v["english"]["bpb"]
    a2["tagalog_test_bpb"] = gate_v["tagalog"]["bpb"]
    a2["english_test_total_nats"] = gate_v["english"]["total_nats"]
    a2["english_test_total_bytes"] = gate_v["english"]["total_bytes"]
    a2["english_test_n_scored_tokens"] = gate_v["english"]["n_scored_tokens"]
    a2["english_test_file_digest"] = public_value(gate_v["english"]["sha256"])
    a2["english_test_at_utc"] = gate_v["english"]["at_utc"]
    a2["tagalog_test_total_nats"] = gate_v["tagalog"]["total_nats"]
    a2["tagalog_test_total_bytes"] = gate_v["tagalog"]["total_bytes"]
    a2["tagalog_test_n_scored_tokens"] = gate_v["tagalog"]["n_scored_tokens"]
    a2["tagalog_test_file_digest"] = public_value(gate_v["tagalog"]["sha256"])
    a2["tagalog_test_at_utc"] = gate_v["tagalog"]["at_utc"]
    a2["test_authorized_for_this_arm"] = "true"
    rows.append(a2)

    a3 = base_row("A3", "50/50-document mix trade-off", "Not mitigation; never tested")
    a3["C_en_vs_A1"] = seal["contrasts"]["C_en_A3"]["delta"]
    a3["G_tl_vs_A1"] = seal["contrasts"]["G_tl_A3"]["delta"]
    a3["a3_document_share_en"] = shares["document_share_en"]
    a3["a3_document_share_tl"] = shares["document_share_tl"]
    a3["a3_byte_share_en"] = shares["byte_share_en"]
    a3["a3_byte_share_tl"] = shares["byte_share_tl"]
    a3["a3_token_share_en"] = shares["token_share_en"]
    a3["a3_token_share_tl"] = shares["token_share_tl"]
    a3["a3_utf8_bytes_en"] = shares["utf8_bytes_en"]
    a3["a3_utf8_bytes_tl"] = shares["utf8_bytes_tl"]
    a3["a3_bpe_tokens_en"] = shares["bpe_tokens_en"]
    a3["a3_bpe_tokens_tl"] = shares["bpe_tokens_tl"]
    a3["a3_K"] = shares["K"]
    a3["a3_mix_order_file_digest"] = public_value(shares["mix_order_sha256"])
    rows.append(a3)

    p11 = base_row(
        "P1.1_d20_descriptive",
        "native Tagalog BPE; different tokenizer; not a C_en/G_tl input",
        "Do not equate P1.1 test_bpb=1.164768 to P2 A2 Tagalog test 1.160154",
    )
    p11["english_val_bpb_full"] = ""
    p11["tagalog_val_bpb_full"] = table["P1.1_d20_descriptive"]["tagalog_val_bpb_full"]
    p11["tokenizer_pkl_file_digest"] = public_value(gate_f["p11_tokenizer_pkl_not_reused"])
    p11["token_bytes_pt_file_digest"] = ""
    p11["packing"] = ""
    p11["stride"] = ""
    rows.append(p11)

    write_csv(dest / "p2_arm_language_crosstab.csv", rows, crosstab_fields)

    codebook = [
        {"variable": "p2_arm_language_crosstab.csv", "definition": "One row per arm. Columns are English/Tagalog val, A2-only tests, eval diagnostics, phase-2 exposure, A3 shares, hashes. Empty cell = not measured for that arm."},
        {"variable": "p2_facts_long.csv", "definition": "Same table as p2_facts_long.tsv in comma-separated form. Column description is immediately after value. First data row is the file_manifest."},
        {"variable": "p2_facts_readable.csv", "definition": "Same facts with only field, value, description first so the prose is visible without scrolling."},
        {"variable": "arm", "definition": "Untrained, A0, A0_d8, A1, A2, A3, or P1.1_d20_descriptive. Confirmatory C_en/G_tl use A1 vs A2 at depth 20 only."},
        {"variable": "english_val_bpb_full", "definition": "Bits per UTF-8 byte on official WT103-raw val, full pass, English 32768 BPE. Gate U."},
        {"variable": "tagalog_val_bpb_full", "definition": "Bits per UTF-8 byte on frozen P1.1 Tagalog val shard under P2 English BPE. Gate U."},
        {"variable": "C_en_vs_A1", "definition": "EN_val_bpb_full(arm)-EN_val_bpb_full(A1). Filed prediction for A2: >=0.01. Observed A2: -0.073991 (not observed as filed)."},
        {"variable": "G_tl_vs_A1", "definition": "TL_val_bpb_full(arm)-TL_val_bpb_full(A1). Filed prediction for A2: <=-0.01. Observed A2: -3.883048 (observed in this one-seed apparatus)."},
        {"variable": "english_test_bpb", "definition": "A2 only. Official WT103-raw test. Secondary. Does not alter C_en/G_tl. Raw test jsonl not in this packet."},
        {"variable": "tagalog_test_bpb", "definition": "A2 only. P1.1 legacy test.jsonl under P2 English BPE. Not P1.1 native-BPE 1.164768. Secondary."},
        {"variable": "revisit_epochs", "definition": "D_phase2 / unique_BPE_tokens in the phase-2 stream. <1 means the unique stream was not fully replayed."},
        {"variable": "a3_*_share_*", "definition": "A3 mix is 50/50 documents (K=28472), not token-equated. Byte share EN 0.961314 / TL 0.038686. Not mitigation."},
        {"variable": "p11_test_bpb_must_not_reuse", "definition": "1.164768 is P1.1 native Tagalog BPE test and is not a P2 observation."},
        {"variable": "does_not_amend_306780", "definition": "P2 AsPredicted 306935 / ResearchBox 8763 does not amend 306780 / ResearchBox 8735."},
        {"variable": "description", "definition": "Super-exhaustive prose for that row: study identity, no-human-subjects statement, family, arm, language, split, field meaning, value, source, confirmatory role, privacy class."},
    ]
    write_csv(dest / "p2_codebook.csv", codebook, ["variable", "definition"])

    # compact companion tables (also legal Data)
    hash_rows = [
            {"artifact": "english_train_jsonl", "file_digest": public_value("09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a"), "in_data_packet": "hash_only"},
            {"artifact": "english_val_jsonl", "file_digest": public_value("874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b"), "in_data_packet": "hash_only"},
            {"artifact": "english_test_jsonl", "file_digest": public_value("2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e"), "in_data_packet": "excluded_raw"},
            {"artifact": "tagalog_train_jsonl", "file_digest": public_value("2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687"), "in_data_packet": "hash_only"},
            {"artifact": "tagalog_test_jsonl", "file_digest": public_value("3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf"), "in_data_packet": "excluded_raw"},
            {"artifact": "tokenizer.pkl", "file_digest": public_value(tok_pkl), "in_data_packet": "hash_only"},
            {"artifact": "token_bytes.pt", "file_digest": public_value(tok_pt), "in_data_packet": "hash_only"},
            {"artifact": "A0_d20", "file_digest": public_value("bd35a8587b5df72c85e93c440cbd79ec506f712cf618f77c21b5625362272e1d"), "in_data_packet": "hash_only"},
            {"artifact": "A1", "file_digest": public_value("e2881049b194898203a954464bcb00939aa1d94b9b41131001ab705c2c92385d"), "in_data_packet": "hash_only"},
            {"artifact": "A2", "file_digest": public_value("2b01acf8fac0e8c783162582cbb384e8ce1c37795aae2f7dd4ae34c2a5c76026"), "in_data_packet": "hash_only"},
            {"artifact": "A3", "file_digest": public_value("d6c62bb793a57c7c23d98c5bd62ec36b41606234524f76855b4459d98c42b368"), "in_data_packet": "hash_only"},
            {"artifact": "a3_mix_order", "file_digest": public_value(shares["mix_order_sha256"]), "in_data_packet": "hash_only"},
            {"artifact": "aspredicted_306935_pdf", "file_digest": public_value(lock["aspredicted_pdf_sha256"]), "in_data_packet": "hash_only"},
            {"artifact": "protocol", "file_digest": public_value(lock["protocol_sha256_at_draft"]), "in_data_packet": "hash_only"},
        ]
    write_csv(dest / "p2_hashes.csv", hash_rows, ["artifact", "file_digest", "in_data_packet"])

    return {
        "n_long_rows": len(long_rows),
        "n_crosstab_rows": len(rows),
        "n_crosstab_cols": len(crosstab_fields),
        "dest": str(dest),
    }


def main() -> None:
    print(json.dumps(emit(ROOT / "transfer/p2-researchbox-8763-bingo/Data"), indent=2))


if __name__ == "__main__":
    main()
