#!/usr/bin/env python3
"""Build P6-M ResearchBox #8918 bingo CSVs and zips. No test.jsonl, no .pt, no passcode."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
BINGO = ROOT / "docs" / "run-cards" / "p6" / "researchbox-bingo"
RUN = ROOT / "docs" / "run-cards" / "p6" / "p6-20260824T155226Z-769f807a"
PAPERS = ROOT / "docs" / "papers" / "p6-m-schedule-topology"
RELEASED = ROOT / "data" / "cache" / "p6-20260824T155226Z-769f807a" / "released"
SCRIPTS = ROOT / "scripts" / "p6"
TRANSFER = ROOT / "transfer" / "p6-researchbox-8918-bingo"
DOWNLOADS = Path.home() / "Downloads" / "p6-researchbox-8918-bingo"
DL_P6M = Path.home() / "Downloads" / "nanochat-filipino" / "P6-M" / "researchbox-8918-bingo"

RB_ID = "8918"
ASP_ID = "307969"
RUN_ID = "p6-20260824T155226Z-769f807a"

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


def fmt6(x: float | None) -> str:
    if x is None:
        return ""
    return f"{x:.6f}"


def main() -> int:
    released = load(RELEASED / "p6-s4-released-contrasts.json")
    lock = load(PAPERS / "LOCK.json")
    cells = released["cells_val_bpb_full"]
    deltas = released["delta_vs_m_fine"]
    contextual = released["contextual"]
    test = released["secondary_m_fine_test"]
    test_en = next(e["bpb"] for e in test["events"] if e["component"] == "english")
    test_tl = next(e["bpb"] for e in test["events"] if e["component"] == "tagalog")

    BINGO.mkdir(parents=True, exist_ok=True)

    # --- primary contrasts ---
    primary_rows = []
    for tau in ("m-coarse", "m-blocked", "m-rand"):
        d = deltas[tau]
        primary_rows.append(
            {
                "seed": "4",
                "tau": tau,
                "delta_tl": fmt6(d["Delta_TL"]),
                "delta_tl_class": d["Delta_TL_class"],
                "delta_en": fmt6(d["Delta_EN"]),
                "delta_en_class": d["Delta_EN_class"],
                "delta": "0.01",
                "reference_arm": "m-fine",
                "primary": "true",
            }
        )
    write_csv(
        BINGO / "p6_primary_contrasts.csv",
        primary_rows,
        [
            "seed",
            "tau",
            "delta_tl",
            "delta_tl_class",
            "delta_en",
            "delta_en_class",
            "delta",
            "reference_arm",
            "primary",
        ],
    )

    # --- arm crosstab ---
    arm_meta = [
        ("C0", "frozen_TL0_d20_parent", None, "c0_en"),
        ("C1", "extra_Tagalog_control", "c1_tl", "c1_en"),
        ("C2", "pure_English_comparator", "c2_tl", "c2_en"),
        ("M-fine", "fine_EN_first_2048_blocks", "m-fine_tl", "m-fine_en"),
        ("M-coarse", "coarse_EN_first_1204224_blocks", "m-coarse_tl", "m-coarse_en"),
        ("M-blocked", "all_TL_then_all_EN", "m-blocked_tl", "m-blocked_en"),
        ("M-rand", "precomputed_Random42_blocks", "m-rand_tl", "m-rand_en"),
    ]
    arm_rows = []
    for arm, role, tl_key, en_key in arm_meta:
        arm_rows.append(
            {
                "seed": "4",
                "arm": arm,
                "role": role,
                "tl_val_bpb_full": fmt6(cells[tl_key]) if tl_key else "",
                "en_val_bpb_full": fmt6(cells[en_key]),
                "en_note": "descriptive_only_excluded_from_topology"
                if arm == "C0"
                else "",
                "m_fine_en_test_bpb": fmt6(test_en) if arm == "M-fine" else "",
                "m_fine_tl_test_bpb": fmt6(test_tl) if arm == "M-fine" else "",
                "test_excluded_from_topology": "true" if arm == "M-fine" else "",
                "not_p5_recurrence_primary": "true",
            }
        )
    write_csv(
        BINGO / "p6_arm_language_crosstab.csv",
        arm_rows,
        [
            "seed",
            "arm",
            "role",
            "tl_val_bpb_full",
            "en_val_bpb_full",
            "en_note",
            "m_fine_en_test_bpb",
            "m_fine_tl_test_bpb",
            "test_excluded_from_topology",
            "not_p5_recurrence_primary",
        ],
    )

    # --- contextual ---
    ctx_rows = []
    for tau in ("m-fine", "m-coarse", "m-blocked", "m-rand"):
        c = contextual[tau]
        ctx_rows.append(
            {
                "seed": "4",
                "tau": tau,
                "R_TL": fmt6(c["R_TL"]),
                "A_EN": fmt6(c["A_EN"]),
                "R_TL_def": "TL(M-tau)-TL(C2)",
                "A_EN_def": "EN(M-tau)-EN(C1)",
                "role": "descriptive_secondary_contextual",
            }
        )
    write_csv(
        BINGO / "p6_contextual_contrasts.csv",
        ctx_rows,
        ["seed", "tau", "R_TL", "A_EN", "R_TL_def", "A_EN_def", "role"],
    )

    # --- facts ---
    facts = [
        ("study_id", "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY", "Study identifier"),
        ("aspredicted_id", ASP_ID, "AsPredicted registration number"),
        ("researchbox_id", RB_ID, "ResearchBox deposit number"),
        ("researchbox_url", f"https://researchbox.org/{RB_ID}", "FOR PEER REVIEW; not Make Public"),
        ("researchbox_code", "RAOZFR", "Peer-review access code (not a secret passcode file)"),
        ("ascollected_id", "", "Pending — Results Provenance NOT DOCUMENTED yet"),
        ("p6_run_id", RUN_ID, "Execution run id"),
        ("parent_seed", "4", "Exactly one parent-init seed"),
        ("nanochat_pin", lock["nanochat_pin"], "Pinned nanochat commit"),
        ("designed_after_p5", "true", "Post-P5; not confirmation of P4/P5"),
        ("does_not_confirm_p4", "true", "Filed claim discipline"),
        ("does_not_confirm_p5", "true", "Filed claim discipline"),
        ("not_p5_recurrence_primary", "true", "Primary is topology Δ vs M-fine"),
        ("q_tl", "0.50", "Fixed Tagalog source-content token share"),
        ("quota_tl", "9633792", "Exact Tagalog source-content tokens per mixed arm"),
        ("quota_en", "9633792", "Exact English source-content tokens per mixed arm"),
        ("d_phase2", "19267584", "Model-visible phase-two tokens per child"),
        ("n_steps", "294", "Updates per child"),
        ("delta_bpb", "0.01", "Primary classification cutoff"),
        ("policy_a_test_arm", "m-fine", "One restricted-test arm only"),
        ("test_access_count_seed4", "1", "Authorized touches"),
        ("eligible_n", "1", "One-seed apparatus"),
        ("no_mean", "true", "No across-seed mean"),
        ("no_ci", "true", "No confidence interval"),
        ("no_pvalue", "true", "No p-value"),
        ("hub_status", "deferred", "Nine sibling objects together or none"),
        ("raw_test_text_in_box", "false", "Held-out text not redistributed"),
        ("aspredicted_pdf_sha256", lock.get("aspredicted_pdf_sha256", ""), "Local prereg PDF digest"),
        ("addendum_sha256", lock.get("addendum_sha256", ""), "Filed addendum digest"),
        ("gate_plan_sha256", lock.get("gate_plan_sha256", ""), "Filed gate-plan digest"),
        ("topology_manifest_sha256", lock.get("topology_manifest_sha256", ""), "Topology manifest digest"),
        ("c0_sha256", lock.get("c0_checkpoint_sha256", ""), "Frozen parent"),
        ("m_coarse_delta_tl_class", deltas["m-coarse"]["Delta_TL_class"], "Primary class"),
        ("m_coarse_delta_en_class", deltas["m-coarse"]["Delta_EN_class"], "Primary class"),
        ("m_blocked_delta_tl_class", deltas["m-blocked"]["Delta_TL_class"], "Primary class"),
        ("m_blocked_delta_en_class", deltas["m-blocked"]["Delta_EN_class"], "Primary class"),
        ("m_rand_delta_tl_class", deltas["m-rand"]["Delta_TL_class"], "Primary class"),
        ("m_rand_delta_en_class", deltas["m-rand"]["Delta_EN_class"], "Primary class"),
        ("u_contrasts_match", str(released.get("u_contrasts_match")).lower(), "Seal vs X match"),
        ("gate_x_script_hash_match_gate0", "false", "Documented deviation; filed analysis authority"),
    ]
    write_csv(
        BINGO / "p6_facts_long.csv",
        [{"variable": a, "value": b, "description": c} for a, b, c in facts],
        ["variable", "value", "description"],
    )

    write_csv(
        BINGO / "p6_codebook.csv",
        [
            {"name": "seed", "type": "int", "definition": "Parent-init seed (always 4)"},
            {"name": "arm", "type": "string", "definition": "C0/C1/C2/M-fine/M-coarse/M-blocked/M-rand"},
            {"name": "tau", "type": "string", "definition": "Topology alternative key"},
            {"name": "role", "type": "string", "definition": "Registered role of the arm"},
            {"name": "tl_val_bpb_full", "type": "float", "definition": "Tagalog full-validation BPB"},
            {"name": "en_val_bpb_full", "type": "float", "definition": "English full-validation BPB"},
            {"name": "delta_tl", "type": "float", "definition": "TL(M-tau)-TL(M-fine)"},
            {"name": "delta_en", "type": "float", "definition": "EN(M-tau)-EN(M-fine)"},
            {"name": "delta_tl_class", "type": "string", "definition": "better/worse/within_delta vs M-fine"},
            {"name": "delta_en_class", "type": "string", "definition": "better/worse/within_delta vs M-fine"},
            {"name": "R_TL", "type": "float", "definition": "TL(M-tau)-TL(C2); contextual"},
            {"name": "A_EN", "type": "float", "definition": "EN(M-tau)-EN(C1); contextual"},
            {"name": "m_fine_en_test_bpb", "type": "float", "definition": "Secondary English holdout BPB; M-fine only"},
            {"name": "m_fine_tl_test_bpb", "type": "float", "definition": "Secondary Tagalog holdout BPB; M-fine only"},
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
    released_json = RELEASED / "p6-s4-released-contrasts.json"
    seal_json = RELEASED / "p6-s4-validation-seal.json"
    hash_rows = [
        ("aspredicted_pdf", "docs/run-cards/p6/AsPredicted-307969.pdf", lock.get("aspredicted_pdf_sha256", "")),
        ("addendum_md", "docs/papers/p6-m-schedule-topology/P6-M-PREFILING-ADDENDUM.md", lock.get("addendum_sha256", "")),
        ("gate_plan_md", "docs/papers/p6-m-schedule-topology/P6-M-GATE-PLAN-FILED.md", lock.get("gate_plan_sha256", "")),
        ("topology_manifest", "manifests/p6/p6_topology_schedule_manifest.json", lock.get("topology_manifest_sha256", "")),
        ("nanochat_pin", "vendor/nanochat @ 92d63d4", lock["nanochat_pin"]),
        ("evaluate_bpb_py", "scripts/p6/evaluate_bpb.py", lock.get("evaluate_bpb_official_sha256", "")),
        ("mix_manifest", "manifests/p6/p6_mix_identity.json", lock.get("mix_manifest_sha256", "")),
        ("paper_pdf", "docs/papers/p6-m-schedule-topology/paper_outputs/paper.pdf", sha256_file(paper_pdf) if paper_pdf.is_file() else ""),
        ("released_contrasts", "released/p6-s4-released-contrasts.json", sha256_file(released_json)),
        ("validation_seal", "released/p6-s4-validation-seal.json", sha256_file(seal_json) if seal_json.is_file() else ""),
        ("unblinding_event", f"docs/run-cards/p6/.../P6_UNBLINDING_EVENT.json", sha256_file(RUN / "P6_UNBLINDING_EVENT.json")),
        ("c0_checkpoint", "p6-s4-c0-tl-d20/model_000294.pt", lock.get("c0_checkpoint_sha256", "")),
    ]
    write_csv(
        BINGO / "p6_hashes.csv",
        [{"artifact": a, "path_or_label": b, "sha2_256": f"sha2-256:{c}" if c else ""} for a, b, c in hash_rows],
        ["artifact", "path_or_label", "sha2_256"],
    )

    gate_map = {
        "break_glass.py": ("incident", "any", "Break-glass / deviation event writer"),
        "continue_from_frozen.py": ("train", "R,S,T", "Continue from frozen C0"),
        "dummy_c3_test.py": ("test", "0", "Dummy lockbox harness"),
        "dummy_p0t.py": ("test", "0", "Dummy lockbox harness"),
        "env.cuda.sh": ("env", "H–W", "CUDA pod environment"),
        "env.sh": ("env", "A–W", "CPU/local environment"),
        "evaluate_bpb.py": ("evaluator", "P0-T,U,V", "Official val/test BPB"),
        "fill_paper_from_released.py": ("paper", "W", "Insert released scalars into paper"),
        "forbidden_parents.py": ("lib", "R–T", "Reject foreign parents"),
        "gate0_accept.py": ("gate0", "0", "Lockbox acceptance"),
        "gate0_filing_lock.py": ("gate0", "0", "Filing lock writer"),
        "gate_a_source_pin.py": ("gateA", "A", "Source pin verification"),
        "gate_b_raw_assets.py": ("gateB", "B", "Raw assets"),
        "gate_c_hygiene.py": ("gateC", "C", "Hygiene"),
        "gate_child_common.sh": ("gateRST", "R–T", "Shared child-train launcher"),
        "gate_d_split_freeze.py": ("gateD", "D", "Split freeze"),
        "gate_e_streams.py": ("gateE", "E", "Packed streams + topology"),
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
        "gate_p0t_authorize.py": ("gateP0T", "P0-T", "P0-T authorization"),
        "gate_phase2_accept.py": ("gateRST", "R–T", "Phase-2 accept helper"),
        "gate_q_authorize.py": ("gateQ", "Q", "C0 freeze authorization"),
        "gate_q_c0_freeze.py": ("gateQ", "Q", "C0 freeze"),
        "gate_r_authorize.py": ("gateR", "R", "C1 authorization"),
        "gate_r_c1.sh": ("gateR", "R", "C1 extra Tagalog"),
        "gate_s_authorize.py": ("gateS", "S", "C2 authorization"),
        "gate_s_c2.sh": ("gateS", "S", "C2 pure English"),
        "gate_t_authorize.py": ("gateT", "T", "Topology authorization"),
        "gate_t_c3.sh": ("gateT", "T", "Legacy C3 launcher name; topology wrapper"),
        "gate_t_technical_accept.py": ("gateT", "T", "Technical accept (e.g. ENOSPC)"),
        "gate_t_topology.sh": ("gateT", "T", "Serial M-fine..M-rand launcher"),
        "gate_u_authorize.py": ("gateU", "U", "Seal authorization"),
        "gate_u_seal.py": ("gateU", "U", "12-cell validation seal"),
        "gate_v_authorize.py": ("gateV", "V", "Test authorization"),
        "gate_v_c3_test.py": ("gateV", "V", "M-fine-only secondary test"),
        "gate_w_closeout.py": ("gateW", "W", "Closeout manifest"),
        "gate_x_authorize.py": ("gateX", "X", "Unblinding authorization"),
        "gate_x_preflight.py": ("gateX", "X", "Unblinding preflight"),
        "gate_x_unblind.py": ("gateX", "X", "One-time topology release"),
        "make_validation_seal.py": ("seal", "U", "Build sealed validation bundle"),
        "mix_construct_dummy.py": ("test", "0", "Dummy mix construction"),
        "pack_parquet.py": ("gateE", "E", "Pack JSONL to parquet"),
        "pack_researchbox_bingo.py": ("deposit", "W", "Build ResearchBox bingo zips"),
        "p6_common.py": ("lib", "0–W", "Shared P6 helpers"),
        "parent_train.py": ("train", "I", "Parent training helper"),
        "prefile_topology_schedules.py": ("prefile", "0", "Build topology TSVs"),
        "prove_parent_seed_knob.py": ("lib", "A", "Parent seed knob proof"),
        "refuse_nanochat_dataset.py": ("lib", "any", "Refuse nanochat.dataset"),
        "refuse_ratio.py": ("lib", "any", "Refuse ratio=-1"),
        "release_bundle.py": ("release", "X", "Incomplete-inventory refuse helper"),
        "sync_tier2_resume_kit.py": ("ops", "H–W", "Tier-2 resume kit sync"),
        "validate_prefile_topology_schedules.py": ("prefile", "0", "Validate topology digests"),
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
                "code_id": f"P6-CODE-{i:03d}",
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
                "researchbox_id": RB_ID,
                "aspredicted_id": ASP_ID,
                "p6_run_id": RUN_ID,
                "zip_member_path": f"scripts_p6/{p.name}",
                "upload_note": "Row crosswalks Code.zip member ↔ gate ↔ purpose ↔ file digest",
            }
        )
    fields = list(code_rows[0].keys())
    write_csv(BINGO / "p6_code_crosswalk.csv", code_rows, fields)

    col_desc = {
        "code_id": "Stable row identifier for each file in the P6 Code inventory.",
        "relative_path": "Repository-relative path under scripts/p6/.",
        "filename": "Basename only.",
        "extension": "File extension including the leading dot.",
        "bytes": "On-disk byte length at inventory time.",
        "sha2_256": "SHA-256 digest prefixed sha2-256:; file hash, not a participant ID.",
        "language": "python for .py; bash for .sh.",
        "role_family": "Functional family tag.",
        "gates_crosswalk": "Which P6 gate(s) the file serves.",
        "purpose": "Short operational description; not a numerical result.",
        "header_or_docstring": "First leading comment/docstring line if present.",
        "bingo_column": "Always Code for this inventory; crosswalk CSV uploads under Data.",
        "researchbox_id": f"{RB_ID} — ResearchBox for P6-M (FOR PEER REVIEW).",
        "aspredicted_id": f"{ASP_ID} — AsPredicted preregistration for P6-M.",
        "p6_run_id": f"Execution run identifier {RUN_ID}.",
        "zip_member_path": "Path inside Code.zip (scripts_p6/<filename>).",
        "upload_note": "Code provenance inventory; not test.jsonl, not weights, not primary scalars.",
    }
    write_csv(
        BINGO / "p6_code_crosswalk_3_columns.csv",
        [
            {"Variable": f"var{i}", "Variable Name": name, "Description": col_desc[name]}
            for i, name in enumerate(fields, start=1)
        ],
        ["Variable", "Variable Name", "Description"],
    )

    lock_out = dict(lock)
    lock_out.pop("researchbox_passcode", None)
    lock_out["researchbox_id"] = int(RB_ID)
    lock_out["researchbox_url"] = f"https://researchbox.org/{RB_ID}"
    lock_out["note"] = (
        (lock_out.get("note") or "")
        + " Sanitized for ResearchBox #8918: passcode omitted. Not a P5 recurrence study. Does not confirm P4/P5."
    )
    (BINGO / "LOCK.sanitized.json").write_text(json.dumps(lock_out, indent=2) + "\n", encoding="utf-8")

    staging = TRANSFER / "_staging"
    if staging.exists():
        shutil.rmtree(staging)
    mat = staging / "Materials"
    code = staging / "Code" / "scripts_p6"
    data = staging / "Data"
    other = staging / "Other"
    other_rel = other / "released"
    for d in (mat, code, data, other_rel):
        d.mkdir(parents=True, exist_ok=True)

    copies = {
        mat / "P6-MATERIALS.md": BINGO / "P6-MATERIALS.md",
        mat / "P6-M-GATE-PLAN-FILED.md": PAPERS / "P6-M-GATE-PLAN-FILED.md",
        mat / "P6-M-PREFILING-ADDENDUM.md": PAPERS / "P6-M-PREFILING-ADDENDUM.md",
        mat / "LOCK.sanitized.json": BINGO / "LOCK.sanitized.json",
        mat / "HF-HUB-STUB.md": BINGO / "HF-HUB-STUB.md",
        mat / "ASCOLLECTED-PENDING.md": BINGO / "ASCOLLECTED-PENDING.md",
        mat / "paper.tex": PAPERS / "paper.tex",
        mat / "paper.pdf": PAPERS / "paper_outputs" / "paper.pdf",
        mat / "DEAR-READER-8918.md": BINGO / "DEAR-READER-8918.md",
        other / "P6-CODE.md": BINGO / "P6-CODE.md",
        other / "P6-OTHER.md": BINGO / "P6-OTHER.md",
        other / "00-BINGO-PLACEMENT.md": BINGO / "00-BINGO-PLACEMENT.md",
        other / "P6_UNBLINDING_EVENT.json": RUN / "P6_UNBLINDING_EVENT.json",
        other / "p6_closeout_manifest.json": RUN / "p6_closeout_manifest.json",
        other / "SHA256SUMS": RUN / "SHA256SUMS",
        other / "RUNPOD-SHUTDOWN.json": RUN / "RUNPOD-SHUTDOWN.json",
        other / "p6_topology_schedule_manifest.json": ROOT / "manifests" / "p6" / "p6_topology_schedule_manifest.json",
        other / "p6_mix_identity.json": ROOT / "manifests" / "p6" / "p6_mix_identity.json",
        other / "RELEASE_MANIFEST.json": ROOT / "docs" / "hub" / "p6-m-schedule-topology" / "RELEASE_MANIFEST.json",
    }
    for dst, src in copies.items():
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    # optional checklist overlays from Downloads
    for name in (
        "P6-M Explicit Preregistration Requirements Checklist.md",
        "P6-M Six-Layer Preregistration Requirements Checklist.md",
    ):
        src = Path.home() / "Downloads" / name
        if src.is_file():
            shutil.copy2(src, other / name.replace(" ", "_"))

    for p in RUN.glob("gate-*.json"):
        if p.name not in EXCLUDE_NAMES:
            shutil.copy2(p, other / p.name)
    seed_dir = RUN / "seed-4"
    if seed_dir.is_dir():
        seed_other = other / "seed-4"
        seed_other.mkdir(parents=True, exist_ok=True)
        for p in seed_dir.glob("*.json"):
            shutil.copy2(p, seed_other / p.name)
    for p in RELEASED.glob("*.json"):
        shutil.copy2(p, other_rel / p.name)

    for p in [*SCRIPTS.glob("*.py"), *SCRIPTS.glob("*.sh")]:
        shutil.copy2(p, code / p.name)

    data_names = (
        "p6_primary_contrasts.csv",
        "p6_arm_language_crosstab.csv",
        "p6_contextual_contrasts.csv",
        "p6_facts_long.csv",
        "p6_codebook.csv",
        "p6_hashes.csv",
        "p6_code_crosswalk.csv",
        "p6_code_crosswalk_3_columns.csv",
    )
    for name in data_names:
        shutil.copy2(BINGO / name, data / name)

    TRANSFER.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    DL_P6M.mkdir(parents=True, exist_ok=True)
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
        for dest_root in (DOWNLOADS, DL_P6M):
            shutil.copy2(csv_path, dest_root / name)
            shutil.copy2(data_upload / zip_name, dest_root / zip_name)

    (data_upload / "README-DATA-UPLOAD.txt").write_text(
        "ResearchBox Data column: upload ONE file per chip.\n"
        "Use each *.zip here (single CSV inside) OR drag the bare *.csv.\n"
        "Do NOT upload a multi-file Data.zip to the Data column.\n"
        "Pair p6_code_crosswalk.csv with p6_code_crosswalk_3_columns.csv as its column codebook.\n"
        f"Box: https://researchbox.org/{RB_ID}\n",
        encoding="utf-8",
    )
    shutil.copy2(data_upload / "README-DATA-UPLOAD.txt", DOWNLOADS / "README-DATA-UPLOAD.txt")
    shutil.copy2(data_upload / "README-DATA-UPLOAD.txt", DL_P6M / "README-DATA-UPLOAD.txt")

    zip_dir(mat, TRANSFER / "Materials.zip")
    zip_dir(code, TRANSFER / "Code.zip")
    zip_dir(other, TRANSFER / "Other.zip")

    for name in ("Materials.zip", "Code.zip", "Other.zip"):
        for dest_root in (DOWNLOADS, DL_P6M):
            shutil.copy2(TRANSFER / name, dest_root / name)
    for name in ("DEAR-READER-8918.md", "00-BINGO-PLACEMENT.md"):
        if (BINGO / name).is_file():
            for dest_root in (DOWNLOADS, DL_P6M):
                shutil.copy2(BINGO / name, dest_root / name)

    # copy AsPredicted PDF into Downloads for Preregistration column convenience
    asp = ROOT / "docs" / "run-cards" / "p6" / "AsPredicted-307969.pdf"
    if asp.is_file():
        for dest_root in (DOWNLOADS, DL_P6M):
            shutil.copy2(asp, dest_root / "AsPredicted-307969.pdf")

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
                "downloads_p6m": str(DL_P6M),
                "researchbox": RB_ID,
                "n_code": len(code_rows),
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
