#!/usr/bin/env python3
"""Build ResearchBox #8869 bingo CSVs and zips. No test.jsonl, no .pt, no passcode."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
BINGO = ROOT / "docs" / "run-cards" / "p4" / "researchbox-bingo"
RUN = ROOT / "docs" / "run-cards" / "p4" / "p4-20260821T060032Z-92d63d4"
PAPERS = ROOT / "docs" / "papers" / "p4-token-share-mix"
RELEASED = ROOT / "data" / "cache" / "p4-20260821T060032Z-92d63d4" / "released"
SCRIPTS = ROOT / "scripts" / "p4"
TRANSFER = ROOT / "transfer" / "p4-researchbox-8869-bingo"
DOWNLOADS = Path.home() / "Downloads" / "p4-researchbox-8869-bingo"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def cell(name: str) -> float:
    return float(load(RELEASED / f"{name}_val_bpb_full.json")["val_bpb_full"])


def fmt(x: float) -> str:
    return f"{x:.12f}"


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
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


def main() -> int:
    BINGO.mkdir(parents=True, exist_ok=True)
    seal = load(RELEASED / "p4-validation-seal.json")
    v = load(RELEASED / "gate-v-test.json")
    tests = {e["component"]: float(e["bpb"]) for e in v["events"]}
    c0_en, c0_tl = cell("c0_en"), cell("c0_tl")
    c1_en, c1_tl = cell("c1_en"), cell("c1_tl")
    c2_en, c2_tl = cell("c2_en"), cell("c2_tl")
    c3_en, c3_tl = cell("c3_en"), cell("c3_tl")
    r_tl, a_en = float(seal["R_TL"]), float(seal["A_EN"])

    write_csv(
        BINGO / "p4_arm_language_crosstab.csv",
        [
            {
                "arm": "C0",
                "role": "frozen_TL0_d20_parent",
                "tl_val_bpb_full": fmt(c0_tl),
                "en_val_bpb_full": fmt(c0_en),
                "en_note": "descriptive_only_excluded_from_contrasts",
                "c3_en_test_bpb": "",
                "c3_tl_test_bpb": "",
                "R_TL": "",
                "A_EN": "",
                "c3_is_not_p3_b3": "true",
                "grammar": "",
            },
            {
                "arm": "C1",
                "role": "extra_Tagalog_control",
                "tl_val_bpb_full": fmt(c1_tl),
                "en_val_bpb_full": fmt(c1_en),
                "en_note": "",
                "c3_en_test_bpb": "",
                "c3_tl_test_bpb": "",
                "R_TL": "",
                "A_EN": "",
                "c3_is_not_p3_b3": "true",
                "grammar": "",
            },
            {
                "arm": "C2",
                "role": "pure_English_comparator",
                "tl_val_bpb_full": fmt(c2_tl),
                "en_val_bpb_full": fmt(c2_en),
                "en_note": "",
                "c3_en_test_bpb": "",
                "c3_tl_test_bpb": "",
                "R_TL": "",
                "A_EN": "",
                "c3_is_not_p3_b3": "true",
                "grammar": "",
            },
            {
                "arm": "C3",
                "role": "token_share_mix_qTL_0.50_not_P3_B3",
                "tl_val_bpb_full": fmt(c3_tl),
                "en_val_bpb_full": fmt(c3_en),
                "en_note": "",
                "c3_en_test_bpb": fmt(tests["english"]),
                "c3_tl_test_bpb": fmt(tests["tagalog"]),
                "R_TL": fmt(r_tl),
                "A_EN": fmt(a_en),
                "c3_is_not_p3_b3": "true",
                "grammar": "both",
            },
        ],
        [
            "arm",
            "role",
            "tl_val_bpb_full",
            "en_val_bpb_full",
            "en_note",
            "c3_en_test_bpb",
            "c3_tl_test_bpb",
            "R_TL",
            "A_EN",
            "c3_is_not_p3_b3",
            "grammar",
        ],
    )

    facts = [
        ("study_id", "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE", "Study identifier"),
        ("aspredicted_id", "307591", "AsPredicted registration number"),
        ("researchbox_id", "8869", "ResearchBox deposit number"),
        ("ascollected_url", "https://ascollected.org/DJ6_FL3", "AsCollected Version 1 URL (project 2455)"),
        ("p4_run_id", "p4-20260821T060032Z-92d63d4", "Execution run id"),
        ("nanochat_pin", "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd", "Pinned nanochat commit"),
        ("designed_after_p3", "true", "Post-P3 study; not confirmation of P3; not P3 B3 fixed"),
        ("c3_is_not_p3_b3", "true", "C3 is a new token-share mix, not P3 B3"),
        ("q_tl", "0.50", "Filed Tagalog source-content token share"),
        ("delta_bpb", "0.01", "Filed co-primary cutoff; equality at -delta counts"),
        ("R_TL", fmt(r_tl), "TL(C3)-TL(C2); filed prediction <= -0.01; observed"),
        ("A_EN", fmt(a_en), "EN(C3)-EN(C1); filed prediction <= -0.01; observed"),
        ("grammar", "both", "Predeclared four-way conclusion category"),
        ("c0_en_val_bpb_full", fmt(c0_en), "Descriptive only; excluded from contrasts"),
        ("c1_tl_val_bpb_full", fmt(c1_tl), "Primary cell"),
        ("c1_en_val_bpb_full", fmt(c1_en), "Primary cell"),
        ("c2_tl_val_bpb_full", fmt(c2_tl), "Primary cell"),
        ("c2_en_val_bpb_full", fmt(c2_en), "Primary cell"),
        ("c3_tl_val_bpb_full", fmt(c3_tl), "Primary cell"),
        ("c3_en_val_bpb_full", fmt(c3_en), "Primary cell"),
        ("c3_en_test_bpb", fmt(tests["english"]), "Secondary Gate V; C3 only"),
        ("c3_tl_test_bpb", fmt(tests["tagalog"]), "Secondary Gate V; C3 only"),
        ("test_access_at_seal", "0", "Gate U seal test_access"),
        ("test_access_after_v", "1", "After one C3-only two-component event"),
        ("one_seed", "true", "Point estimates only; no CI/p-value"),
        ("hub_status", "deferred", "C0+C1+C2+C3 together or none; never C3 alone"),
        ("raw_test_text_in_box", "false", "Held-out text not redistributed"),
    ]
    write_csv(
        BINGO / "p4_facts_long.csv",
        [{"variable": a, "value": b, "description": c} for a, b, c in facts],
        ["variable", "value", "description"],
    )

    write_csv(
        BINGO / "p4_codebook.csv",
        [
            {"name": "arm", "type": "string", "definition": "Branch label C0/C1/C2/C3"},
            {"name": "role", "type": "string", "definition": "Registered role of the arm"},
            {"name": "tl_val_bpb_full", "type": "float", "definition": "Tagalog full-validation bits per UTF-8 byte"},
            {"name": "en_val_bpb_full", "type": "float", "definition": "English full-validation bits per UTF-8 byte"},
            {"name": "en_note", "type": "string", "definition": "Notes; C0 English is descriptive only"},
            {"name": "c3_en_test_bpb", "type": "float", "definition": "Secondary English holdout BPB; C3 only"},
            {"name": "c3_tl_test_bpb", "type": "float", "definition": "Secondary Tagalog legacy holdout BPB; C3 only"},
            {"name": "R_TL", "type": "float", "definition": "TL(C3)-TL(C2); co-primary; C3 row only"},
            {"name": "A_EN", "type": "float", "definition": "EN(C3)-EN(C1); co-primary; C3 row only"},
            {"name": "c3_is_not_p3_b3", "type": "string", "definition": "true; C3 is not P3 B3"},
            {"name": "grammar", "type": "string", "definition": "both / only_R / only_A / neither"},
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

    hash_rows = [
        ("aspredicted_pdf", "docs/run-cards/p4/AsPredicted-307591.pdf", "463b29fcff8d7c8099790325fa19d6bcf9ee29f64424c373a380566a6fe9011c"),
        ("protocol_md", "docs/papers/p4-token-share-mix/PROTOCOL-p4-token-share-mix.md", "22c28f2bc632f132d9c95bbbcc9d1facbddf0b6b821445487e451c472ea58d4b"),
        ("gate_bible_md", "docs/papers/p4-token-share-mix/PROTOCOL-p4-GATES-EXHAUSTIVE.md", "b389b70e0b8e3af869e8dea314b1c7c6b91df313e49d1bf11d9d07961b4a5a42"),
        ("addendum_md", "docs/papers/p4-token-share-mix/P4-PREFILING-ADDENDUM-DRAFT.md", "f056a6f75c73a4d8dc3401ba8d7219d406aa7e498e5b0799d3d0373f9f74c216"),
        ("nanochat_pin", "vendor/nanochat @ 92d63d4", "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd"),
        ("tokenizer_pkl", "carry-forward P3 tokenizer.pkl", "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8"),
        ("token_bytes_pt", "carry-forward P3 token_bytes.pt", "a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132"),
        ("evaluate_bpb_py", "scripts/p4/evaluate_bpb.py", "9afebdb405aaac0bb4287051d9b6f5d16f56d6dd9269a1e6c2c5df29becbced1"),
        ("tl_train_jsonl", "frozen P1.1 train", "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687"),
        ("tl_val_jsonl", "frozen P1.1 val", "4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c"),
        ("tl_test_jsonl", "frozen P1.1 test hash only; text not in box", "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf"),
        ("en_train_jsonl", "frozen WT103-raw train", "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a"),
        ("en_val_jsonl", "frozen WT103-raw val", "874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b"),
        ("en_test_jsonl", "WT103-raw test hash only; text not in box", "2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e"),
        ("mix_manifest", "manifests/p4/p4_mix_manifest.json", "f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107"),
        ("c0_ckpt", "p4-c0-tl-d20 / I d20", "34e069646be4158979809c023691188439047d6cbee08a141db432c78bcf02e2"),
        ("c1_ckpt", "p4-c1-tl-d20", "87b9f55146de72dd6ae53598b9aea8d99079ff0f9492b7f9ea4fdce550664c55"),
        ("c2_ckpt", "p4-c2-en-d20", "0787aed0f13a0ab3ec144baf6802b144a18412780a2d00a64ca7adcb67a4a375"),
        ("c3_ckpt", "p4-c3-mix-d20", "eef9a4e11c4840ac036d42c3bf4d87a2139ea1fa5809e1c756df2770fe0609f3"),
        ("validation_seal", "released/p4-validation-seal.json", "5c7287752ba1abb39245acab43b9917ea9e089c0309959ec24990015e1ad580f"),
        ("paper_pdf", "docs/papers/p4-token-share-mix/paper_outputs/paper.pdf", "d0bf73d30bd43b3984441f3d567ce49c886194376575148354494b7f7892da71"),
    ]
    write_csv(
        BINGO / "p4_hashes.csv",
        [{"artifact": a, "path_or_label": b, "sha2_256": f"sha2-256:{c}"} for a, b, c in hash_rows],
        ["artifact", "path_or_label", "sha2_256"],
    )

    gate_map = {
        "break_glass.py": ("incident", "any", "Break-glass / deviation event writer"),
        "continue_from_frozen.py": ("train", "R,S,T", "Continue from frozen C0 with fresh optimizer"),
        "dummy_c3_test.py": ("test", "0", "Dummy lockbox / unit harness (nonconfirmatory)"),
        "dummy_p0t.py": ("test", "0", "Dummy lockbox / unit harness (nonconfirmatory)"),
        "env.cuda.sh": ("env", "H–W", "CUDA pod environment; never p1/p2/p3 env"),
        "env.sh": ("env", "A–W", "CPU/local environment; never p1/p2/p3 env"),
        "evaluate_bpb.py": ("evaluator", "P0-T,U,V", "Official val/test BPB; frozen formula"),
        "fill_p4_tables.py": ("gateX", "X", "Recompute contrasts from released seals only"),
        "forbidden_parents.py": ("lib", "R–T", "Reject P1.1/P2/P3/smoke/d8 as parent"),
        "gate0_accept.py": ("gate0", "0", "Lockbox acceptance / filing lock"),
        "gate_a_source_pin.py": ("gateA", "A", "Source pin verification"),
        "gate_b_raw_assets.py": ("gateB", "B", "Raw assets / corpus identity"),
        "gate_c_hygiene.py": ("gateC", "C", "Hygiene (no ClimbMix, no test in train)"),
        "gate_child_common.sh": ("gateRST", "R–T", "Shared child-train launcher"),
        "gate_d_split_freeze.py": ("gateD", "D", "Split freeze"),
        "gate_e_c3_mix.py": ("gateE", "E", "C3 token-share mix freeze"),
        "gate_e_shards.py": ("gateE", "E", "C1/C2 packed shards"),
        "gate_f_tokenizer.py": ("gateF", "F", "Carry-forward tokenizer freeze (before E)"),
        "gate_g_budget.py": ("gateG", "G", "Budget / command freeze"),
        "gate_h_accept.py": ("gateH", "H", "CUDA smoke accept (not parent)"),
        "gate_h_preflight.py": ("gateH", "H", "CUDA smoke preflight"),
        "gate_h_smoke.sh": ("gateH", "H", "CUDA d4 smoke launcher"),
        "gate_i_accept.py": ("gateI", "I", "TL0 d8+d20 parent training"),
        "gate_i_preflight.py": ("gateI", "I", "TL0 preflight"),
        "gate_i_progress.py": ("gateI", "I", "TL0 safe progress"),
        "gate_i_tl0.sh": ("gateI", "I", "TL0 confirmatory train"),
        "gate_p0t.sh": ("gateP0T", "P0-T", "P0-T eligibility launcher"),
        "gate_p0t_accept.py": ("gateP0T", "P0-T", "P0-T accept"),
        "gate_p0t_preflight.py": ("gateP0T", "P0-T", "P0-T preflight"),
        "gate_p0t_progress.py": ("gateP0T", "P0-T", "P0-T safe progress"),
        "gate_phase2_accept.py": ("gateRST", "R–T", "Accept helper for phase-2 arms"),
        "gate_q_c0_freeze.py": ("gateQ", "Q", "C0 freeze (= TL0 d20)"),
        "gate_q_to_v.sh": ("orchestrator", "Q–V", "Q-to-V orchestrator"),
        "gate_qv_progress.py": ("orchestrator", "Q–V", "Q-to-V safe progress"),
        "gate_r_c1.sh": ("gateR", "R", "C1 extra Tagalog"),
        "gate_s_c2.sh": ("gateS", "S", "C2 pure English"),
        "gate_t_c3.sh": ("gateT", "T", "C3 frozen mix"),
        "gate_u_seal.py": ("gateU", "U", "Validation seal (six cells + C0 EN descriptive)"),
        "gate_v_c3_test.py": ("gateV", "V", "C3-only secondary tests; do not re-run"),
        "gate_w_closeout.py": ("gateW", "W", "Closeout manifest (no new science)"),
        "gate_x_preflight.py": ("gateX", "X", "Status-only unblinding preflight"),
        "gate_x_unblind.py": ("gateX", "X", "One-time sealed release"),
        "make_validation_seal.py": ("seal", "U", "Build sealed validation bundle"),
        "mix_construct_dummy.py": ("test", "0", "Dummy mix construction (nonconfirmatory)"),
        "p4_common.py": ("lib", "0–W", "Shared P4 helpers"),
        "pack_parquet.py": ("gateE", "E", "Pack JSONL to parquet shards"),
        "phase2_common.py": ("lib", "R–T", "Phase-2 helpers"),
        "refuse_nanochat_dataset.py": ("lib", "any", "Refuse python -m nanochat.dataset"),
        "refuse_ratio.py": ("lib", "any", "Refuse ratio=-1"),
        "release_bundle.py": ("release", "X", "Incomplete-inventory refuse helper"),
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
                "code_id": f"P4-CODE-{i:03d}",
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
                "researchbox_id": "8869",
                "aspredicted_id": "307591",
                "p4_run_id": "p4-20260821T060032Z-92d63d4",
                "zip_member_path": f"scripts_p4/{p.name}",
                "upload_note": "Row crosswalks Code.zip member ↔ gate ↔ purpose ↔ file digest",
            }
        )
    fields = list(code_rows[0].keys())
    write_csv(BINGO / "p4_code_crosswalk.csv", code_rows, fields)

    col_desc = {
        "code_id": "Stable row identifier for each file in the P4 Code inventory.",
        "relative_path": "Repository-relative path under scripts/p4/.",
        "filename": "Basename only.",
        "extension": "File extension including the leading dot.",
        "bytes": "On-disk byte length at inventory time.",
        "sha2_256": "SHA-256 of file bytes with sha2-256: prefix. Not a participant ID.",
        "language": "python or bash.",
        "role_family": "Functional family tag.",
        "gates_crosswalk": "Which P4 gate(s) the file serves.",
        "purpose": "Operational description, not a numerical result.",
        "header_or_docstring": "Leading comment/docstring if present.",
        "bingo_column": "Always Code for this inventory.",
        "researchbox_id": "8869",
        "aspredicted_id": "307591",
        "p4_run_id": "p4-20260821T060032Z-92d63d4",
        "zip_member_path": "Path inside Code.zip.",
        "upload_note": "This inventory is code provenance, not test.jsonl or weights.",
    }
    write_csv(
        BINGO / "p4_code_crosswalk_3_columns.csv",
        [
            {"Variable": f"var{i}", "Variable Name": name, "Description": col_desc[name]}
            for i, name in enumerate(fields, start=1)
        ],
        ["Variable", "Variable Name", "Description"],
    )

    (BINGO / "DEAR-READER-8869.txt").write_text(
        (BINGO / "DEAR-READER-8869.md").read_text(encoding="utf-8"), encoding="utf-8"
    )

    lock = load(PAPERS / "LOCK.json")
    lock["researchbox_passcode"] = None
    lock["note"] = (
        (lock.get("note") or "")
        + " Sanitized for ResearchBox: passcode omitted. C3 is not P3 B3."
    )
    (BINGO / "LOCK.sanitized.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

    staging = TRANSFER / "_staging"
    if staging.exists():
        shutil.rmtree(staging)
    mat = staging / "Materials"
    code = staging / "Code" / "scripts_p4"
    other = staging / "Other"
    other_rel = other / "released"
    for d in (mat, code, other_rel):
        d.mkdir(parents=True, exist_ok=True)

    copies = {
        mat / "P4-MATERIALS.md": BINGO / "P4-MATERIALS.md",
        mat / "PROTOCOL-p4-token-share-mix.md": PAPERS / "PROTOCOL-p4-token-share-mix.md",
        mat / "PROTOCOL-p4-GATES-EXHAUSTIVE.md": PAPERS / "PROTOCOL-p4-GATES-EXHAUSTIVE.md",
        mat / "P4-PREFILING-ADDENDUM-DRAFT.md": PAPERS / "P4-PREFILING-ADDENDUM-DRAFT.md",
        mat / "P4-REPORTING-GRAMMAR.md": PAPERS / "P4-REPORTING-GRAMMAR.md",
        mat / "LOCK.sanitized.json": BINGO / "LOCK.sanitized.json",
        mat / "README-study.md": ROOT / "docs" / "p4" / "README.md",
        mat / "ASCOLLECTED-2455.md": BINGO / "ASCOLLECTED-2455.md",
        mat / "HF-HUB-STUB.md": ROOT / "docs" / "hub" / "p4-token-share-mix" / "README.md",
        mat / "paper.tex": PAPERS / "paper.tex",
        mat / "paper.pdf": PAPERS / "paper_outputs" / "paper.pdf",
        mat / "DEAR-READER-8869.md": BINGO / "DEAR-READER-8869.md",
        other / "P4-CODE.md": BINGO / "P4-CODE.md",
        other / "P4-OTHER.md": BINGO / "P4-OTHER.md",
        other / "00-BINGO-PLACEMENT.md": BINGO / "00-BINGO-PLACEMENT.md",
        other / "P4_UNBLINDING_EVENT.json": RUN / "P4_UNBLINDING_EVENT.json",
        other / "p4_closeout_manifest.json": RUN / "p4_closeout_manifest.json",
        other / "SHA256SUMS": RUN / "SHA256SUMS",
        other / "p4_test_access_log.json": ROOT / "manifests" / "p4" / "p4_test_access_log.json",
        other / "p4_gate_ledger.json": ROOT / "manifests" / "p4" / "p4_gate_ledger.json",
        other / "p4_mix_manifest.json": ROOT / "manifests" / "p4" / "p4_mix_manifest.json",
        other / "p4_budget_manifest.json": ROOT / "manifests" / "p4" / "p4_budget_manifest.json",
        other / "P4-EXPLICIT-PREREGISTRATION-CLOSEOUT-CHECKLIST.md": RUN
        / "P4-EXPLICIT-PREREGISTRATION-CLOSEOUT-CHECKLIST.md",
        other / "P4-SIX-LAYER-PREREGISTRATION-CLOSEOUT-AUDIT.md": RUN
        / "P4-SIX-LAYER-PREREGISTRATION-CLOSEOUT-AUDIT.md",
        other / "results_p4_tables.json": ROOT / "results" / "p4" / "tables.json",
    }
    for dst, src in copies.items():
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    for p in RUN.glob("gate-*.json"):
        shutil.copy2(p, other / p.name)
    if (RUN / "released").is_dir():
        for p in (RUN / "released").glob("*.json"):
            shutil.copy2(p, other_rel / p.name)
    else:
        for p in RELEASED.glob("*.json"):
            shutil.copy2(p, other_rel / p.name)

    for p in [*SCRIPTS.glob("*.py"), *SCRIPTS.glob("*.sh")]:
        shutil.copy2(p, code / p.name)

    TRANSFER.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    zip_dir(mat, TRANSFER / "Materials.zip")
    # ResearchBox rejects mixed Code.zip (CSV = Data, .py = Code).
    zip_dir(code, TRANSFER / "Code.zip")
    zip_dir(other, TRANSFER / "Other.zip")
    data = TRANSFER / "Data"
    data.mkdir(exist_ok=True)
    for name in (
        "p4_arm_language_crosstab.csv",
        "p4_facts_long.csv",
        "p4_codebook.csv",
        "p4_hashes.csv",
        "p4_code_crosswalk.csv",
        "p4_code_crosswalk_3_columns.csv",
    ):
        shutil.copy2(BINGO / name, data / name)
        shutil.copy2(BINGO / name, DOWNLOADS / name)

    for name in ("Materials.zip", "Code.zip", "Other.zip"):
        shutil.copy2(TRANSFER / name, DOWNLOADS / name)
    shutil.copy2(BINGO / "DEAR-READER-8869.md", DOWNLOADS / "DEAR-READER-8869.md")
    shutil.copy2(BINGO / "00-BINGO-PLACEMENT.md", DOWNLOADS / "00-BINGO-PLACEMENT.md")

    # inventory sanity
    banned = []
    for zpath in (TRANSFER / "Materials.zip", TRANSFER / "Code.zip", TRANSFER / "Other.zip"):
        with zipfile.ZipFile(zpath) as z:
            for n in z.namelist():
                low = n.lower()
                if low.endswith(".pt") or low.endswith("test.jsonl") or ("passcode" in low and low.endswith(".txt")):
                    banned.append(f"{zpath.name}:{n}")
                if zpath.name == "Code.zip" and not low.endswith((".py", ".sh")):
                    banned.append(f"{zpath.name}:non_code:{n}")
    print(json.dumps({
        "bingo": str(BINGO),
        "transfer": str(TRANSFER),
        "downloads": str(DOWNLOADS),
        "n_code": len(code_rows),
        "banned_hits": banned,
        "spotcheck": {"R_TL": fmt(r_tl), "A_EN": fmt(a_en), "grammar": "both"},
    }, indent=2))
    return 1 if banned else 0


if __name__ == "__main__":
    raise SystemExit(main())
