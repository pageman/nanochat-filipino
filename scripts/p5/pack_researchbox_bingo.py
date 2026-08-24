#!/usr/bin/env python3
"""Build P5 ResearchBox bingo CSVs and zips. No test.jsonl, no .pt, no passcode."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
BINGO = ROOT / "docs" / "run-cards" / "p5" / "researchbox-bingo"
RUN = ROOT / "docs" / "run-cards" / "p5" / "p5-20260823T160632Z-439d1de5"
PAPERS = ROOT / "docs" / "papers" / "p5-multi-seed-p4"
RELEASED = ROOT / "results" / "p5" / "released"
SCRIPTS = ROOT / "scripts" / "p5"
TRANSFER = ROOT / "transfer" / "p5-researchbox-bingo"
DOWNLOADS = Path.home() / "Downloads" / "p5-researchbox-bingo"

EXCLUDE_NAMES = {
    "panel-status-loop.pid",
    "wait-start-resume.log",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def zip_dir(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            if p.is_file() and p.name != ".DS_Store":
                z.write(p, p.relative_to(src))


def zip_one_file(src: Path, dest: Path) -> None:
    """ResearchBox Data column: exactly one member per zip."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(src, src.name)


def main() -> int:
    tables = load(ROOT / "results" / "p5" / "tables.json")
    lock = load(PAPERS / "LOCK.json")
    aspdf = ROOT / "docs" / "run-cards" / "p5" / "AsPredicted-307836.pdf"

    BINGO.mkdir(parents=True, exist_ok=True)

    arm_rows = []
    for seed in ("1", "2", "3"):
        s = tables["seeds"][seed]
        cells = s["cells_6dp"]
        for arm, role in (
            ("C0", "frozen_TL0_d20_parent"),
            ("C1", "extra_Tagalog_control"),
            ("C2", "pure_English_comparator"),
            ("C3", "token_share_mix_qTL_0.50_not_P3_B3"),
        ):
            if arm == "C0":
                tl_val = ""
                en_val = cells["c0_en"]
                en_note = "descriptive_only_excluded_from_contrasts"
            else:
                tl_val = cells[f"c{arm[1]}_tl"]
                en_val = cells[f"c{arm[1]}_en"]
                en_note = ""
            row = {
                "seed": seed,
                "arm": arm,
                "role": role,
                "tl_val_bpb_full": tl_val,
                "en_val_bpb_full": en_val,
                "en_note": en_note,
                "c3_en_test_bpb": s["c3_test_en"] if arm == "C3" else "",
                "c3_tl_test_bpb": s["c3_test_tl"] if arm == "C3" else "",
                "R_TL": s["R_TL"] if arm == "C3" else "",
                "A_EN": s["A_EN"] if arm == "C3" else "",
                "per_seed_class": s["class"] if arm == "C3" else "",
                "c3_is_not_p3_b3": "true",
            }
            arm_rows.append(row)

    write_csv(
        BINGO / "p5_arm_language_crosstab.csv",
        arm_rows,
        [
            "seed",
            "arm",
            "role",
            "tl_val_bpb_full",
            "en_val_bpb_full",
            "en_note",
            "c3_en_test_bpb",
            "c3_tl_test_bpb",
            "R_TL",
            "A_EN",
            "per_seed_class",
            "c3_is_not_p3_b3",
        ],
    )

    counts = tables["panel_count_table"]
    write_csv(
        BINGO / "p5_panel_count_table.csv",
        [
            {
                "category": "both",
                "k": counts["both"],
                "K_eligible": tables["eligible_n"],
                "description": "Both co-primary P4 criteria met at seed level",
            },
            {
                "category": "only-R",
                "k": counts["only-R"],
                "K_eligible": tables["eligible_n"],
                "description": "Only R_TL criterion met",
            },
            {
                "category": "only-A",
                "k": counts["only-A"],
                "K_eligible": tables["eligible_n"],
                "description": "Only A_EN criterion met",
            },
            {
                "category": "neither",
                "k": counts["neither"],
                "K_eligible": tables["eligible_n"],
                "description": "Neither criterion met",
            },
            {
                "category": "ineligible_parent",
                "k": counts["ineligible_parent"],
                "K_eligible": tables["eligible_n"],
                "description": "P0-T ineligible parent; excluded from K_elig",
            },
        ],
        ["category", "k", "K_eligible", "description"],
    )

    facts = [
        ("study_id", "NANOCHAT-FILIPINO-P5-P4-MULTI-SEED", "Study identifier"),
        ("aspredicted_id", "307836", "AsPredicted registration number"),
        ("researchbox_id", "8904", "ResearchBox deposit number"),
        ("researchbox_url", "https://researchbox.org/8904", "ResearchBox (FOR PEER REVIEW; not Make Public)"),
        ("ascollected_id", "2503", "AsCollected project number"),
        ("ascollected_url", "https://ascollected.org/HC8_G2F", "AsCollected Version 1 public URL"),
        ("p5_run_id", "p5-20260823T160632Z-439d1de5", "Execution run id"),
        ("panel_seeds", "1,2,3", "Closed panel; unused parent-init seeds"),
        ("nanochat_pin", lock["nanochat_pin"], "Pinned nanochat commit"),
        ("designed_after_p4", "true", "Post-P4 panel; not confirmation of P4 as law"),
        ("p4_seed0_not_a_p5_cell", "true", "P4 seed 0 is historical only"),
        ("c3_is_not_p3_b3", "true", "C3 is frozen P4 token-share mix, not P3 B3"),
        ("q_tl", "0.50", "Filed Tagalog source-content token share"),
        ("delta_bpb", "0.01", "Filed co-primary cutoff; equality at -delta counts"),
        ("K_eligible", str(tables["eligible_n"]), "Eligible seeds after P0-T"),
        ("k_both", str(counts["both"]), "Primary panel count"),
        ("k_only_R", str(counts["only-R"]), "Panel count"),
        ("k_only_A", str(counts["only-A"]), "Panel count"),
        ("k_neither", str(counts["neither"]), "Panel count"),
        ("k_ineligible_parent", str(counts["ineligible_parent"]), "Panel count"),
        ("no_mean", "true", "No across-seed mean of contrasts"),
        ("no_ci", "true", "No confidence interval"),
        ("no_pvalue", "true", "No p-value"),
        ("hub_status", "deferred", "C0+C1+C2+C3 per seed together or none"),
        ("raw_test_text_in_box", "false", "Held-out text not redistributed"),
        ("aspredicted_pdf_sha256", lock.get("aspredicted_pdf_sha256", ""), "Local prereg PDF digest"),
    ]
    for seed in ("1", "2", "3"):
        s = tables["seeds"][seed]
        facts.extend(
            [
                (f"seed{seed}_class", s["class"], f"Per-seed four-way class"),
                (f"seed{seed}_R_TL", s["R_TL"], "TL(C3)-TL(C2) at 6 dp"),
                (f"seed{seed}_A_EN", s["A_EN"], "EN(C3)-EN(C1) at 6 dp"),
            ]
        )
    write_csv(
        BINGO / "p5_facts_long.csv",
        [{"variable": a, "value": b, "description": c} for a, b, c in facts],
        ["variable", "value", "description"],
    )

    write_csv(
        BINGO / "p5_codebook.csv",
        [
            {"name": "seed", "type": "int", "definition": "Parent-init seed 1/2/3"},
            {"name": "arm", "type": "string", "definition": "Branch label C0/C1/C2/C3"},
            {"name": "role", "type": "string", "definition": "Registered role of the arm"},
            {"name": "tl_val_bpb_full", "type": "float", "definition": "Tagalog full-validation BPB"},
            {"name": "en_val_bpb_full", "type": "float", "definition": "English full-validation BPB"},
            {"name": "en_note", "type": "string", "definition": "C0 English is descriptive only"},
            {"name": "c3_en_test_bpb", "type": "float", "definition": "Secondary English holdout BPB; C3 only"},
            {"name": "c3_tl_test_bpb", "type": "float", "definition": "Secondary Tagalog holdout BPB; C3 only"},
            {"name": "R_TL", "type": "float", "definition": "TL(C3)-TL(C2); co-primary; C3 row only"},
            {"name": "A_EN", "type": "float", "definition": "EN(C3)-EN(C1); co-primary; C3 row only"},
            {"name": "per_seed_class", "type": "string", "definition": "both / only-R / only-A / neither"},
            {"name": "category", "type": "string", "definition": "Panel count category"},
            {"name": "k", "type": "int", "definition": "Count in category"},
            {"name": "K_eligible", "type": "int", "definition": "Eligible panel size"},
            {"name": "variable", "type": "string", "definition": "Long-facts variable name"},
            {"name": "value", "type": "string", "definition": "Long-facts value"},
            {"name": "description", "type": "string", "definition": "Long-facts description"},
            {"name": "artifact", "type": "string", "definition": "Hashed artifact role"},
            {"name": "path_or_label", "type": "string", "definition": "Relative path or label"},
            {
                "name": "sha2_256",
                "type": "string",
                "definition": "SHA-256 of a FILE with sha2-256: prefix; not a participant ID",
            },
        ],
        ["name", "type", "definition"],
    )

    paper_pdf = PAPERS / "paper_outputs" / "paper.pdf"
    hash_rows = [
        ("aspredicted_pdf", "docs/run-cards/p5/AsPredicted-307836.pdf", lock.get("aspredicted_pdf_sha256", "")),
        ("addendum_md", "docs/papers/p5-multi-seed-p4/P5-PREFILING-ADDENDUM-DRAFT.md", lock.get("addendum_sha256", "")),
        ("gate_plan_md", "docs/papers/p5-multi-seed-p4/P5-GATES-EXHAUSTIVE-PLAN.md", lock.get("gate_plan_sha256", "")),
        ("nanochat_pin", "vendor/nanochat @ 92d63d4", lock["nanochat_pin"]),
        ("evaluate_bpb_py", "scripts/p5/evaluate_bpb.py", lock.get("evaluate_bpb_official_sha256", "")),
        ("mix_manifest", "manifests/p5/p5_mix_identity.json", lock.get("mix_manifest_sha256", "")),
        ("paper_pdf", "docs/papers/p5-multi-seed-p4/paper_outputs/paper.pdf", sha256_file(paper_pdf) if paper_pdf.is_file() else ""),
        ("tables_json", "results/p5/tables.json", sha256_file(ROOT / "results/p5/tables.json")),
        ("unblinding_event", "docs/run-cards/p5/.../P5_UNBLINDING_EVENT.json", sha256_file(RUN / "P5_UNBLINDING_EVENT.json")),
    ]
    for seed in (1, 2, 3):
        seal = RELEASED / f"seed-{seed}" / f"p5-s{seed}-validation-seal.json"
        if seal.is_file():
            hash_rows.append(
                (f"validation_seal_s{seed}", f"released/seed-{seed}/p5-s{seed}-validation-seal.json", sha256_file(seal))
            )
    write_csv(
        BINGO / "p5_hashes.csv",
        [{"artifact": a, "path_or_label": b, "sha2_256": f"sha2-256:{c}" if c else ""} for a, b, c in hash_rows],
        ["artifact", "path_or_label", "sha2_256"],
    )

    gate_map = {
        "authorize_seed_gates.py": ("lib", "I–V", "Per-seed gate authorization"),
        "break_glass.py": ("incident", "any", "Break-glass / deviation event writer"),
        "continue_from_frozen.py": ("train", "R,S,T", "Continue from frozen C0"),
        "continue_from_u2_to_v3.sh": ("orchestrator", "panel", "Resume panel after S2 incident"),
        "dummy_c3_test.py": ("test", "0", "Dummy lockbox harness"),
        "dummy_p0t.py": ("test", "0", "Dummy lockbox harness"),
        "env.cuda.sh": ("env", "H–W", "CUDA pod environment"),
        "env.sh": ("env", "A–W", "CPU/local environment"),
        "evaluate_bpb.py": ("evaluator", "P0-T,U,V", "Official val/test BPB"),
        "forbidden_parents.py": ("lib", "R–T", "Reject foreign parents"),
        "gate0_accept.py": ("gate0", "0", "Lockbox acceptance"),
        "gate0_filing_lock.py": ("gate0", "0", "Filing lock writer"),
        "gate_a_source_pin.py": ("gateA", "A", "Source pin verification"),
        "gate_b_raw_assets.py": ("gateB", "B", "Raw assets"),
        "gate_c_hygiene.py": ("gateC", "C", "Hygiene"),
        "gate_child_common.sh": ("gateRST", "R–T", "Shared child-train launcher"),
        "gate_d_split_freeze.py": ("gateD", "D", "Split freeze"),
        "gate_e_streams.py": ("gateE", "E", "Packed streams + mix freeze"),
        "gate_f_tokenizer.py": ("gateF", "F", "Carry-forward tokenizer"),
        "gate_g_budget.py": ("gateG", "G", "Budget freeze"),
        "gate_h_accept.py": ("gateH", "H", "CUDA smoke accept"),
        "gate_h_authorize.py": ("gateH", "H", "CUDA smoke authorization"),
        "gate_h_preflight.py": ("gateH", "H", "CUDA smoke preflight"),
        "gate_h_smoke.sh": ("gateH", "H", "CUDA d4 smoke launcher"),
        "gate_i_accept.py": ("gateI", "I", "TL0 d8+d20 parent training"),
        "gate_i_authorize.py": ("gateI", "I", "TL0 authorization"),
        "gate_i_preflight.py": ("gateI", "I", "TL0 preflight"),
        "gate_i_tl0.sh": ("gateI", "I", "TL0 confirmatory train"),
        "gate_p0t.sh": ("gateP0T", "P0-T", "P0-T launcher"),
        "gate_p0t_accept.py": ("gateP0T", "P0-T", "P0-T accept"),
        "gate_phase2_accept.py": ("gateRST", "R–T", "Phase-2 accept helper"),
        "gate_q_c0_freeze.py": ("gateQ", "Q", "C0 freeze"),
        "gate_r_c1.sh": ("gateR", "R", "C1 extra Tagalog"),
        "gate_s_c2.sh": ("gateS", "S", "C2 pure English"),
        "gate_t_c3.sh": ("gateT", "T", "C3 frozen mix"),
        "gate_u_seal.py": ("gateU", "U", "Validation seal per seed"),
        "gate_v_c3_test.py": ("gateV", "V", "C3-only secondary tests"),
        "gate_w_closeout.py": ("gateW", "W", "Closeout manifest"),
        "gate_x_preflight.py": ("gateX", "X", "Panel unblinding preflight"),
        "gate_x_unblind.py": ("gateX", "X", "One-time panel release"),
        "make_validation_seal.py": ("seal", "U", "Build sealed validation bundle"),
        "mix_construct_dummy.py": ("test", "0", "Dummy mix construction"),
        "pack_parquet.py": ("gateE", "E", "Pack JSONL to parquet"),
        "pack_researchbox_bingo.py": ("deposit", "W", "Build ResearchBox bingo zips"),
        "p5_common.py": ("lib", "0–W", "Shared P5 helpers"),
        "parent_train.py": ("train", "I", "Parent training helper"),
        "prove_parent_seed_knob.py": ("lib", "A", "Parent seed knob proof"),
        "refuse_nanochat_dataset.py": ("lib", "any", "Refuse nanochat.dataset"),
        "refuse_ratio.py": ("lib", "any", "Refuse ratio=-1"),
        "release_bundle.py": ("release", "X", "Incomplete-inventory refuse helper"),
        "resume_after_s2_wrapper_death.sh": ("incident", "S2", "S2 pod-death resume"),
        "run_panel_to_x.sh": ("orchestrator", "panel", "Panel driver to Gate X"),
        "run_seed_panel.sh": ("orchestrator", "panel", "Single-seed panel slice"),
        "wait_start_and_resume_s2.sh": ("incident", "S2", "S2 wait/resume wrapper"),
    }

    code_rows = []
    for i, p in enumerate(sorted([*SCRIPTS.glob("*.py"), *SCRIPTS.glob("*.sh")]), start=1):
        fam, gates, purpose = gate_map.get(p.name, ("other", "any", p.name))
        text = p.read_text(encoding="utf-8", errors="replace")
        header = ""
        for line in text.splitlines()[:8]:
            s = line.strip()
            if s.startswith('"""') or s.startswith("'''") or s.startswith("#"):
                header = s[:180]
                break
        lang = "python" if p.suffix == ".py" else "bash"
        digest = sha256_file(p)
        code_rows.append(
            {
                "code_id": f"P5-CODE-{i:03d}",
                "relative_path": str(p.relative_to(ROOT)),
                "filename": p.name,
                "extension": p.suffix,
                "bytes": p.stat().st_size,
                "sha2_256": f"sha2-256:{digest}",
                "language": lang,
                "role_family": fam,
                "gates_crosswalk": gates,
                "purpose": purpose,
                "header_or_docstring": header,
                "bingo_column": "Code",
                "researchbox_id": "8904",
                "aspredicted_id": "307836",
                "p5_run_id": "p5-20260823T160632Z-439d1de5",
                "zip_member_path": f"scripts_p5/{p.name}",
                "upload_note": "Row crosswalks Code.zip member ↔ gate ↔ purpose ↔ file digest",
            }
        )
    fields = list(code_rows[0].keys())
    write_csv(BINGO / "p5_code_crosswalk.csv", code_rows, fields)

    col_desc = {
        "code_id": "Stable row identifier for each file in the P5 Code inventory (P5-CODE-001 through P5-CODE-054).",
        "relative_path": "Repository-relative path under scripts/p5/ in pageman/nanochat-filipino.",
        "filename": "Basename only (e.g. gate_x_unblind.py).",
        "extension": "File extension including the leading dot (.py or .sh).",
        "bytes": "On-disk byte length of the script at inventory time (2026-08-24).",
        "sha2_256": "SHA-256 digest of the file bytes, prefixed sha2-256:. This is a file hash, not a participant or Prolific ID.",
        "language": "python for .py files; bash for .sh launchers.",
        "role_family": "Functional family tag (gateX, lib, env, train, evaluator, orchestrator, incident, deposit, etc.).",
        "gates_crosswalk": "Which P5 gate(s) or panel stage the file serves (0, A–H, I–V per seed, X, W, panel, S2, etc.).",
        "purpose": "Short operational description of what the script does; not a numerical experimental result.",
        "header_or_docstring": "First leading comment or docstring line from the file, if present (truncated).",
        "bingo_column": "Always Code for this inventory; the crosswalk itself is uploaded under Data.",
        "researchbox_id": "8904 — ResearchBox deposit for P5 multi-seed panel (FOR PEER REVIEW; not #8869).",
        "aspredicted_id": "307836 — AsPredicted preregistration for P5 multi-seed panel.",
        "p5_run_id": "Execution run identifier p5-20260823T160632Z-439d1de5.",
        "zip_member_path": "Path of this file inside Code.zip (scripts_p5/<filename>).",
        "upload_note": "This inventory documents code provenance and gate crosswalk; it is not test.jsonl, not model weights, and not a confirmatory scalar result.",
    }
    write_csv(
        BINGO / "p5_code_crosswalk_3_columns.csv",
        [
            {"Variable": f"var{i}", "Variable Name": name, "Description": col_desc[name]}
            for i, name in enumerate(fields, start=1)
        ],
        ["Variable", "Variable Name", "Description"],
    )

    lock_out = dict(lock)
    lock_out.pop("researchbox_passcode", None)
    lock_out["note"] = (
        (lock_out.get("note") or "")
        + " Sanitized for ResearchBox: passcode omitted. C3 is not P3 B3. Does not confirm P4 as law."
    )
    (BINGO / "LOCK.sanitized.json").write_text(json.dumps(lock_out, indent=2) + "\n", encoding="utf-8")

    staging = TRANSFER / "_staging"
    if staging.exists():
        shutil.rmtree(staging)
    mat = staging / "Materials"
    code = staging / "Code" / "scripts_p5"
    data = staging / "Data"
    other = staging / "Other"
    other_rel = other / "released"
    for d in (mat, code, data, other_rel):
        d.mkdir(parents=True, exist_ok=True)

    copies = {
        mat / "P5-MATERIALS.md": BINGO / "P5-MATERIALS.md",
        mat / "P5-GATES-EXHAUSTIVE-PLAN.md": PAPERS / "P5-GATES-EXHAUSTIVE-PLAN.md",
        mat / "P5-PREFILING-ADDENDUM-DRAFT.md": PAPERS / "P5-PREFILING-ADDENDUM-DRAFT.md",
        mat / "LOCK.sanitized.json": BINGO / "LOCK.sanitized.json",
        mat / "README-study.md": ROOT / "docs" / "p5" / "README.md",
        mat / "HF-HUB-STUB.md": ROOT / "docs" / "hub" / "p5-p4-multi-seed" / "README.md",
        mat / "ASCOLLECTED-2503.md": BINGO / "ASCOLLECTED-2503.md",
        mat / "paper.tex": PAPERS / "paper.tex",
        mat / "paper.pdf": PAPERS / "paper_outputs" / "paper.pdf",
        mat / "DEAR-READER-P5.md": BINGO / "DEAR-READER-P5.md",
        other / "P5-CODE.md": BINGO / "P5-CODE.md",
        other / "P5-OTHER.md": BINGO / "P5-OTHER.md",
        other / "00-BINGO-PLACEMENT.md": BINGO / "00-BINGO-PLACEMENT.md",
        other / "P5_UNBLINDING_EVENT.json": RUN / "P5_UNBLINDING_EVENT.json",
        other / "p5_closeout_manifest.json": RUN / "p5_closeout_manifest.json",
        other / "SHA256SUMS": RUN / "SHA256SUMS",
        other / "p5_gate_ledger.json": ROOT / "manifests" / "p5" / "p5_gate_ledger.json",
        other / "p5_mix_identity.json": ROOT / "manifests" / "p5" / "p5_mix_identity.json",
        other / "p5_budget_manifest.json": ROOT / "manifests" / "p5" / "p5_budget_manifest.json",
        other / "results_p5_tables.json": ROOT / "results" / "p5" / "tables.json",
        other / "P5-SIX-LAYER-CHECKLIST-AUDITED.md": PAPERS / "P5-SIX-LAYER-CHECKLIST-AUDITED.md",
        other / "P5-PREREGISTRATION-AUDIT.md": PAPERS / "P5-PREREGISTRATION-AUDIT.md",
    }
    for dst, src in copies.items():
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    for p in RUN.glob("gate-*.json"):
        if p.name not in EXCLUDE_NAMES:
            shutil.copy2(p, other / p.name)
    for seed_dir in sorted(RUN.glob("seed-*")):
        seed_other = other / seed_dir.name
        seed_other.mkdir(parents=True, exist_ok=True)
        for p in seed_dir.glob("*.json"):
            shutil.copy2(p, seed_other / p.name)
    for seed_dir in sorted(RELEASED.glob("seed-*")):
        rel_seed = other_rel / seed_dir.name
        rel_seed.mkdir(parents=True, exist_ok=True)
        for p in seed_dir.glob("*.json"):
            shutil.copy2(p, rel_seed / p.name)

    for p in [*SCRIPTS.glob("*.py"), *SCRIPTS.glob("*.sh")]:
        shutil.copy2(p, code / p.name)

    data_names = (
        "p5_panel_count_table.csv",
        "p5_arm_language_crosstab.csv",
        "p5_facts_long.csv",
        "p5_codebook.csv",
        "p5_hashes.csv",
        "p5_code_crosswalk.csv",
        "p5_code_crosswalk_3_columns.csv",
    )
    for name in data_names:
        shutil.copy2(BINGO / name, data / name)

    TRANSFER.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    data_upload = TRANSFER / "Data"
    if data_upload.exists():
        shutil.rmtree(data_upload)
    data_upload.mkdir(parents=True)
    data_zips: list[str] = []
    for name in data_names:
        csv_path = data / name
        zip_name = name.replace(".csv", ".zip")
        zip_one_file(csv_path, data_upload / zip_name)
        data_zips.append(zip_name)
        shutil.copy2(csv_path, data_upload / name)
        shutil.copy2(csv_path, DOWNLOADS / name)
        shutil.copy2(data_upload / zip_name, DOWNLOADS / name.replace(".csv", ".zip"))

    (data_upload / "README-DATA-UPLOAD.txt").write_text(
        "ResearchBox Data column: upload ONE file per chip.\n"
        "Use each *.zip here (single CSV inside) OR drag the bare *.csv.\n"
        "Do NOT upload a multi-file Data.zip to the Data column.\n"
        "Pair p5_code_crosswalk.csv with p5_code_crosswalk_3_columns.csv as its column codebook.\n",
        encoding="utf-8",
    )

    zip_dir(mat, TRANSFER / "Materials.zip")
    zip_dir(code, TRANSFER / "Code.zip")
    zip_dir(other, TRANSFER / "Other.zip")

    for name in ("Materials.zip", "Code.zip", "Other.zip"):
        shutil.copy2(TRANSFER / name, DOWNLOADS / name)
    for name in ("DEAR-READER-P5.md", "00-BINGO-PLACEMENT.md"):
        if (BINGO / name).is_file():
            shutil.copy2(BINGO / name, DOWNLOADS / name)

    banned = []
    for zpath in (TRANSFER / "Materials.zip", TRANSFER / "Code.zip", TRANSFER / "Other.zip"):
        with zipfile.ZipFile(zpath) as z:
            for n in z.namelist():
                low = n.lower()
                if low.endswith(".pt") or low.endswith("test.jsonl") or ("passcode" in low and low.endswith(".txt")):
                    banned.append(f"{zpath.name}:{n}")
                if zpath.name == "Code.zip" and not low.endswith((".py", ".sh")):
                    banned.append(f"{zpath.name}:non_code:{n}")
    for zpath in data_upload.glob("*.zip"):
        with zipfile.ZipFile(zpath) as z:
            members = [n for n in z.namelist() if not n.endswith("/")]
            if len(members) != 1:
                banned.append(f"{zpath.name}:member_count={len(members)}")
            elif not members[0].lower().endswith(".csv"):
                banned.append(f"{zpath.name}:not_csv:{members[0]}")

    print(
        json.dumps(
            {
                "bingo": str(BINGO),
                "transfer": str(TRANSFER),
                "downloads": str(DOWNLOADS),
                "n_code": len(code_rows),
                "panel": tables["panel_count_table"],
                "banned_hits": banned,
                "column_zips": ["Materials.zip", "Code.zip", "Other.zip"],
                "data_upload": {
                    "dir": str(data_upload),
                    "single_file_zips": data_zips,
                    "note": "Upload each Data/*.zip separately; never multi-file Data.zip",
                },
            },
            indent=2,
        )
    )
    return 1 if banned else 0


if __name__ == "__main__":
    raise SystemExit(main())
