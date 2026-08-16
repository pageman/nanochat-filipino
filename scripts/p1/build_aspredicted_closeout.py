#!/usr/bin/env python3
"""Build AsPredicted #306780 close-out records, bundle, and filled checklist.

Does not retrain, reread WikiText test, or reopen D*. Reconstructs the named
selection_record.json from the sealed val_baselines_summary.json that already
existed at 2026-08-16T07:56:24Z with test_read_count=0.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/paulpajo/Projects/nanochat-filipino")
RUN_ID = "p1-20260816T025911Z-0067a57"
ART = ROOT / "artifacts" / "p1" / RUN_ID
GATE_J = ART / "gate-j"
CKPT = ART / "checkpoints"
LOGS = ART / "train-logs"
BUNDLE = ROOT / "transfer" / "p1.1-closeout-bundle-20260816"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

CKPT_SHA = {
    8: "9c407f4fbc6f5bb2b40a36ae49fb38d088fa025b4f317e1ddaa629cc2068bbea",
    12: "5dfccc27b8b27c7c03faaeb92c1cbf1c884659b03795baa18921386d15e5277e",
    16: "525301ebe3bc80875b31dd3f7fa19e12fc5405565f7b973811c0647168445cbf",
    20: "9e30fff3d6effc7c71af92e8488f9375a5d70cf1962ba371bee0e639836dde38",
}
TAGS = {8: "p1-fixed-d8-3x", 12: "p1-fixed-d12-3x", 16: "p1-fixed-d16-3x", 20: "p1-fixed-d20-3x"}
TRAIN_UTC = {
    8: ("2026-08-16T07:04:33Z", "2026-08-16T07:08:19Z"),
    12: ("2026-08-16T07:08:20Z", "2026-08-16T07:14:21Z"),
    16: ("2026-08-16T07:14:21Z", "2026-08-16T07:24:50Z"),
    20: ("2026-08-16T07:24:50Z", "2026-08-16T07:41:32Z"),
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump_json(path: Path, obj) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha256_file(path)


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def main() -> None:
    summary = json.loads((GATE_J / "val_baselines_summary.json").read_text())
    unigram = json.loads((GATE_J / "byte_unigram_val.json").read_text())
    test_bpb = json.loads((GATE_J / "p1-fixed-d20-3x_test_bpb.json").read_text())
    budget = json.loads((ROOT / "manifests" / "budget_manifest.json").read_text())
    depths_budget = {d["depth"]: d for d in budget["depths"]}

    hashes = {
        "aspredicted_pdf": sha256_file(ROOT / "docs" / "run-cards" / "AsPredicted-306780.pdf"),
        "clarifications": sha256_file(ROOT / "docs" / "EXECUTION-CLARIFICATIONS-p1.1.md"),
        "val_baselines_summary": sha256_file(GATE_J / "val_baselines_summary.json"),
        "byte_unigram": sha256_file(GATE_J / "byte_unigram_val.json"),
        "test_bpb": sha256_file(GATE_J / "p1-fixed-d20-3x_test_bpb.json"),
        "evaluator": sha256_file(ROOT / "scripts" / "p1" / "gate_j_full_bpb.py"),
        "hook_patch": sha256_file(ROOT / "patches" / "nanochat-NANOCHAT_DATA_DIR.patch"),
        "results": sha256_file(ROOT / "docs" / "run-cards" / "RESULTS-p1.1-aspredicted-306780.md"),
        "source_manifest": sha256_file(ROOT / "manifests" / "source_manifest.json"),
        "split_manifest": sha256_file(ROOT / "manifests" / "split_manifest.json"),
        "shard_manifest": sha256_file(ROOT / "manifests" / "shard_manifest.json"),
        "tokenizer_manifest": sha256_file(ROOT / "manifests" / "tokenizer_manifest.json"),
        "budget_manifest": sha256_file(ROOT / "manifests" / "budget_manifest.json"),
        "test_manifest": sha256_file(ROOT / "manifests" / "test_manifest.json"),
        "gate_j": sha256_file(ROOT / "manifests" / "gate_j.json"),
        "runpod_gate_i_preflight": sha256_file(ROOT / "manifests" / "runpod_gate_i_preflight.json"),
        "execution_host": sha256_file(ROOT / "manifests" / "execution_host.json"),
        "execution_clarifications_name": "docs/EXECUTION-CLARIFICATIONS-p1.1.md",
    }
    for d, tag in TAGS.items():
        hashes[f"val_{d}"] = sha256_file(GATE_J / f"{tag}_val_baselines.json")
        hashes[f"meta_{d}"] = sha256_file(CKPT / tag / "meta_000294.json")
        hashes[f"runcard_{d}"] = sha256_file(ROOT / "docs" / "run-cards" / "gate-i" / f"{tag}.md")
        hashes[f"trainlog_{d}"] = sha256_file(LOGS / f"{tag}.train.log")
        hashes[f"export_sha_{d}"] = sha256_file(LOGS / f"{tag}.SHA256")

    # --- selection_record.json (reconstructed from sealed 07:56:24Z summary) ---
    candidates = []
    for d in (8, 12, 16, 20):
        row = summary["depths"][str(d)]
        candidates.append(
            {
                "depth": d,
                "model_tag": TAGS[d],
                "checkpoint_sha256": CKPT_SHA[d],
                "val_bpb_full": row["val_bpb_full"],
                "train_bpb_full": row["train_bpb_full"],
                "validation_artifact_sha256": hashes[f"val_{d}"],
                "eligibility": "eligible",
                "baseline_pass": row["baseline_pass"],
            }
        )
    selection_body = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "registration": "AsPredicted #306780",
        "run_id": RUN_ID,
        "selection_rule": "exact_minimum_final_val_bpb_full",
        "evaluation_checkpoint_rule": "final_checkpoint_at_fixed_budget",
        "one_seed_interpretation": "gaps_below_0.01_bpb_practically_indistinguishable",
        "candidates": candidates,
        "selected_depth": 20,
        "selected_model_tag": "p1-fixed-d20-3x",
        "selected_checkpoint_sha256": CKPT_SHA[20],
        "selected_val_bpb_full": summary["D_star_val_bpb_full"],
        "nearest_competitor_depth": 8,
        "nearest_competitor_gap_bpb": summary["D_star_margin_to_next"],
        "practically_indistinguishable_0.01": True,
        "selection_timestamp_utc": "2026-08-16T07:56:24Z",
        "sealed_selection_artifact": "artifacts/p1/p1-20260816T025911Z-0067a57/gate-j/val_baselines_summary.json",
        "sealed_selection_artifact_sha256": hashes["val_baselines_summary"],
        "sealed_artifact_test_read_count": 0,
        "named_file_materialized_at_utc": NOW,
        "named_file_note": (
            "The filename manifests/selection_record.json was written after the one "
            "permitted test read. The sealed selection already existed in "
            "val_baselines_summary.json at 2026-08-16T07:56:24Z with test_read_count=0, "
            "before the 2026-08-16T07:58:35Z test mount. This file reconstructs that "
            "sealed decision; it does not reopen D*."
        ),
        "test_bpb_before_selection": False,
        "test_access_events_before_selection": 0,
    }
    rec_bytes = json.dumps(selection_body, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    selection_body["record_sha256"] = sha256_bytes(rec_bytes)
    sel_path = ROOT / "manifests" / "selection_record.json"
    hashes["selection_record"] = dump_json(sel_path, selection_body)

    # --- final_checkpoint_manifest.json ---
    ckpt_manifest = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "run_id": RUN_ID,
        "registration": "AsPredicted #306780",
        "written_at_utc": NOW,
        "host": {
            "pod_id": "68bei7d3vx4krc",
            "pod_name": "p1-gate-i",
            "gpu": "NVIDIA A40 48GB",
            "data_center": "EU-SE-1",
            "image": "runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404",
            "torch": "2.9.1+cu128",
            "device_batch_size": 8,
        },
        "nanochat_commit": "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd",
        "hook_patch_sha256": hashes["hook_patch"],
        "evaluator_sha256": hashes["evaluator"],
        "archive_root": f"artifacts/p1/{RUN_ID}/checkpoints/",
        "runs": {},
    }
    for d, tag in TAGS.items():
        b = depths_budget[d]
        ckpt_manifest["runs"][str(d)] = {
            "run_tag": tag,
            "final_checkpoint_path": f"artifacts/p1/{RUN_ID}/checkpoints/{tag}/model_000294.pt",
            "final_checkpoint_sha256": CKPT_SHA[d],
            "meta_path": f"artifacts/p1/{RUN_ID}/checkpoints/{tag}/meta_000294.json",
            "meta_sha256": hashes[f"meta_{d}"],
            "run_card_path": f"docs/run-cards/gate-i/{tag}.md",
            "run_card_sha256": hashes[f"runcard_{d}"],
            "train_log_path": f"artifacts/p1/{RUN_ID}/train-logs/{tag}.train.log",
            "train_log_sha256": hashes[f"trainlog_{d}"],
            "pod_export_sha256_file": f"artifacts/p1/{RUN_ID}/train-logs/{tag}.SHA256",
            "step": 294,
            "exists": True,
            "exit_status": 0,
            "started_at_utc": TRAIN_UTC[d][0],
            "ended_at_utc": TRAIN_UTC[d][1],
            "p_total": b["p_total"],
            "p_scaling": b["p_scaling"],
            "target_param_data_ratio": b["target_param_data_ratio"],
            "total_batch_size": 65536,
            "num_iterations": 294,
            "d_actual": 19267584,
            "command": (
                f"python -m scripts.base_train --device-type=cuda --depth={d} "
                f"--max-seq-len=2048 --device-batch-size=8 --total-batch-size=65536 "
                f"--num-iterations=294 --target-param-data-ratio={b['target_param_data_ratio']} "
                f"--eval-tokens=262144 --eval-every=50 --core-metric-every=-1 "
                f"--sample-every=200 --save-every=200 --warmup-steps=14 "
                f"--run={tag} --model-tag={tag}"
            ),
        }
    hashes["final_checkpoint_manifest"] = dump_json(
        ROOT / "manifests" / "final_checkpoint_manifest.json", ckpt_manifest
    )

    # --- primary table + components ---
    results_dir = ART / "closeout"
    results_dir.mkdir(parents=True, exist_ok=True)
    csv_path = results_dir / "primary_table.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "depth",
                "run_tag",
                "seed",
                "p_total",
                "p_scaling",
                "ratio",
                "d_actual",
                "train_bpb_full",
                "val_bpb_full",
                "train_val_gap_bpb",
                "untrained_val_bpb",
                "unigram_val_bpb",
                "eligible",
                "rank_note",
                "checkpoint_sha256",
            ]
        )
        notes = {
            8: "2nd; gap to D* 0.006887 BPB; practically indistinguishable at one seed",
            12: "3rd; gap to D* 0.008576 BPB; practically indistinguishable at one seed",
            16: "4th; highest val_bpb_full",
            20: "D* exact minimum; not a meaningful depth ranking vs d8 at 0.01",
        }
        for d in (8, 12, 16, 20):
            row = summary["depths"][str(d)]
            b = depths_budget[d]
            gap = row["val_bpb_full"] - row["train_bpb_full"]
            w.writerow(
                [
                    d,
                    TAGS[d],
                    0,
                    b["p_total"],
                    b["p_scaling"],
                    b["target_param_data_ratio"],
                    19267584,
                    row["train_bpb_full"],
                    row["val_bpb_full"],
                    gap,
                    row["random_val_bpb"],
                    row["val_bpb_unigram"],
                    "eligible",
                    notes[d],
                    CKPT_SHA[d],
                ]
            )
    hashes["primary_table"] = sha256_file(csv_path)

    components = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "run_id": RUN_ID,
        "evaluator_sha256": hashes["evaluator"],
        "packing": "bos_bestfit_buffer1000_one_pass_no_wrap",
        "max_seq_len": 2048,
        "device_batch_size": 8,
        "packed_val_bytes": 5868797,
        "packed_val_scored_tokens": 1286864,
        "packed_val_excluded_specials": 7472,
        "unigram_train_bytes_N": unigram["train_bytes_N"],
        "unigram_val_bytes_M": unigram["heldout_bytes_M"],
        "unigram_nll_nats": unigram["nll_nats"],
        "unigram_bpb": unigram["bpb"],
        "unigram_byte_counts_sha256": unigram["byte_counts_sha256"],
        "depths": {str(d): summary["depths"][str(d)] for d in (8, 12, 16, 20)},
        "D_star": 20,
        "test_bpb": test_bpb["test_bpb"],
        "test_components": test_bpb["components"],
        "test_artifact_sha256": hashes["test_bpb"],
        "selection_record_sha256": hashes["selection_record"],
    }
    hashes["result_components"] = dump_json(results_dir / "result_components.json", components)

    # --- test_access_log F2 enrichment (do not invent a second test read) ---
    tal_path = ROOT / "manifests" / "test_access_log.json"
    tal = json.loads(tal_path.read_text())
    tal["f2_authorization"] = {
        "event_type": "confirmatory_test_evaluation",
        "utc_time": "2026-08-16T07:58:35Z",
        "operator_or_job": "Paul Pajo / scripts/p1/gate_j_full_bpb.py --phase test on 68bei7d3vx4krc",
        "selected_depth": 20,
        "selected_checkpoint_sha256": CKPT_SHA[20],
        "selection_record_sha256": hashes["selection_record"],
        "sealed_selection_artifact_sha256": hashes["val_baselines_summary"],
        "test_manifest_sha256": "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf",
        "test_access_count_before_event": 0,
        "intended_access_count_after_event": 1,
        "evaluator_command_hash": hashes["evaluator"],
        "host_environment_fingerprint_hash": hashes["runpod_gate_i_preflight"],
        "reason": "Registered secondary test_bpb only; not model selection.",
        "note": (
            "F2 fields were filled into this log after the named selection_record.json "
            "was materialized. The live authorization at 07:58:35Z used "
            "val_baselines_summary.json (test_read_count=0) as the sealed selection."
        ),
    }
    hashes["test_access_log"] = dump_json(tal_path, tal)

    # --- ledger named events (backfill with original times + recorded_at) ---
    ledger_path = ROOT / "manifests" / "gate_ledger.json"
    ledger = json.loads(ledger_path.read_text())
    backfill = [
        {
            "at_utc": "2026-08-16T07:50:27Z",
            "kind": "final_validation_preflight_passed",
            "depth": 8,
            "recorded_at_utc": NOW,
            "note": "Gate J used the already-passed I-host preflight (runpod_gate_i_preflight.json ok=true, test absent). Evaluator gate_j_full_bpb.py; no test path.",
        },
        {
            "at_utc": "2026-08-16T07:50:27Z",
            "kind": "final_validation_preflight_passed",
            "depth": 12,
            "recorded_at_utc": NOW,
            "note": "Same shared Gate J job / I-host preflight as d8. Test absent.",
        },
        {
            "at_utc": "2026-08-16T07:50:27Z",
            "kind": "final_validation_preflight_passed",
            "depth": 16,
            "recorded_at_utc": NOW,
            "note": "Same shared Gate J job / I-host preflight as d8. Test absent.",
        },
        {
            "at_utc": "2026-08-16T07:50:27Z",
            "kind": "final_validation_preflight_passed",
            "depth": 20,
            "recorded_at_utc": NOW,
            "note": "Same shared Gate J job / I-host preflight as d8. Test absent.",
        },
        {
            "at_utc": "2026-08-16T07:56:24Z",
            "kind": "final_validation_completed",
            "depth": 8,
            "result_artifact_sha256": hashes["val_8"],
            "recorded_at_utc": NOW,
            "note": "val_bpb_full=1.179134743718777; finite; no rank stated in this event.",
        },
        {
            "at_utc": "2026-08-16T07:56:24Z",
            "kind": "final_validation_completed",
            "depth": 12,
            "result_artifact_sha256": hashes["val_12"],
            "recorded_at_utc": NOW,
            "note": "val_bpb_full=1.180823927886072; finite; no rank stated in this event.",
        },
        {
            "at_utc": "2026-08-16T07:56:24Z",
            "kind": "final_validation_completed",
            "depth": 16,
            "result_artifact_sha256": hashes["val_16"],
            "recorded_at_utc": NOW,
            "note": "val_bpb_full=1.1955463669138386; finite; no rank stated in this event.",
        },
        {
            "at_utc": "2026-08-16T07:56:24Z",
            "kind": "final_validation_completed",
            "depth": 20,
            "result_artifact_sha256": hashes["val_20"],
            "recorded_at_utc": NOW,
            "note": "val_bpb_full=1.172247965803217; finite; no rank stated in this event.",
        },
        {
            "at_utc": "2026-08-16T07:56:24Z",
            "kind": "validation_selection_frozen",
            "D_star": 20,
            "sealed_artifact_sha256": hashes["val_baselines_summary"],
            "selection_record_sha256": hashes["selection_record"],
            "test_read_count_at_freeze": 0,
            "recorded_at_utc": NOW,
            "note": "Exact minimum final val_bpb_full is d20. Named selection_record.json reconstructed later from the sealed 07:56:24Z summary.",
        },
        {
            "at_utc": NOW,
            "kind": "closeout_checklist_filled",
            "note": "Super-Exhaustive Close-Out Checklist filled from sealed Gate J artifacts. Bundle at transfer/p1.1-closeout-bundle-20260816/. D* and test_bpb unchanged.",
        },
    ]
    existing_kinds = {(e.get("kind"), e.get("depth"), e.get("at_utc")) for e in ledger["event_log"]}
    for ev in backfill:
        key = (ev.get("kind"), ev.get("depth"), ev.get("at_utc"))
        if key not in existing_kinds:
            ledger["event_log"].append(ev)
    hashes["gate_ledger"] = dump_json(ledger_path, ledger)

    # --- close-out bundle (no weights, no test text) ---
    if BUNDLE.exists():
        shutil.rmtree(BUNDLE)
    BUNDLE.mkdir(parents=True)

    copy_file(ROOT / "docs" / "run-cards" / "AsPredicted-306780.pdf", BUNDLE / "00_registration" / "aspredicted_306780.pdf")
    (BUNDLE / "00_registration" / "aspredicted_306780.sha256").write_text(hashes["aspredicted_pdf"] + "\n")
    copy_file(ROOT / "docs" / "EXECUTION-CLARIFICATIONS-p1.1.md", BUNDLE / "00_registration" / "execution_clarifications_p1_1.md")
    (BUNDLE / "00_registration" / "execution_clarifications_p1_1.sha256").write_text(hashes["clarifications"] + "\n")

    for name in (
        "gate_ledger.json",
        "selection_record.json",
        "test_access_log.json",
        "final_checkpoint_manifest.json",
        "gate_j.json",
    ):
        copy_file(ROOT / "manifests" / name, BUNDLE / "01_protocol_and_ledger" / name)
    for card in (ROOT / "docs" / "run-cards" / "deviations").glob("*.md"):
        copy_file(card, BUNDLE / "01_protocol_and_ledger" / "deviation_cards" / card.name)

    for name in (
        "source_manifest.json",
        "split_manifest.json",
        "shard_manifest.json",
        "tokenizer_manifest.json",
        "budget_manifest.json",
        "test_manifest.json",
        "corpus_audit.json",
        "token_statistics.json",
    ):
        src = ROOT / "manifests" / name
        if src.exists():
            copy_file(src, BUNDLE / "02_input_provenance" / name)
    copy_file(ART / "gate_d_split.json", BUNDLE / "02_input_provenance" / "article_reconstruction_audit" / "gate_d_split.json")
    for p in (ART / "split_recovery").glob("*"):
        if p.is_file():
            copy_file(p, BUNDLE / "02_input_provenance" / "article_reconstruction_audit" / p.name)

    (BUNDLE / "03_code_and_environment").mkdir(parents=True, exist_ok=True)
    (BUNDLE / "03_code_and_environment" / "nanochat_commit.txt").write_text(
        "92d63d4e8bb4df75c3b71618f31ddde2378b2bcd\n"
    )
    copy_file(ROOT / "patches" / "nanochat-NANOCHAT_DATA_DIR.patch", BUNDLE / "03_code_and_environment" / "data_hook.patch")
    copy_file(ART / "uv.lock", BUNDLE / "03_code_and_environment" / "lockfile")
    (BUNDLE / "03_code_and_environment" / "container_image.txt").write_text(
        "runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404\ntorch 2.9.1+cu128\n"
    )
    copy_file(ROOT / "manifests" / "execution_host.json", BUNDLE / "03_code_and_environment" / "host_fingerprints" / "execution_host.json")
    copy_file(ROOT / "manifests" / "runpod_gate_i_preflight.json", BUNDLE / "03_code_and_environment" / "preflight_outputs" / "runpod_gate_i_preflight.json")
    copy_file(ROOT / "scripts" / "p1" / "gate_j_full_bpb.py", BUNDLE / "03_code_and_environment" / "gate_j_full_bpb.py")

    for d, tag in TAGS.items():
        dest = BUNDLE / "04_runs" / f"d{d}"
        copy_file(CKPT / tag / "meta_000294.json", dest / "meta_000294.json")
        copy_file(LOGS / f"{tag}.train.log", dest / "train.log")
        copy_file(LOGS / f"{tag}.SHA256", dest / "SHA256")
        copy_file(ROOT / "docs" / "run-cards" / "gate-i" / f"{tag}.md", dest / "run_card.md")
        (dest / "CHECKPOINT_POINTER.txt").write_text(
            f"model_000294.pt SHA-256 {CKPT_SHA[d]}\n"
            f"Mac archive: artifacts/p1/{RUN_ID}/checkpoints/{tag}/model_000294.pt\n"
            "Weights omitted from this bundle (size). Hash-verify against final_checkpoint_manifest.json.\n"
        )

    for d, tag in TAGS.items():
        dest = BUNDLE / "05_validation" / f"full_eval_d{d}"
        copy_file(GATE_J / f"{tag}_val_baselines.json", dest / f"{tag}_val_baselines.json")
    copy_file(GATE_J / "val_baselines_summary.json", BUNDLE / "05_validation" / "val_baselines_summary.json")
    for d, tag in TAGS.items():
        copy_file(
            GATE_J / f"{tag}_val_baselines.json",
            BUNDLE / "05_validation" / "untrained_baselines" / f"{tag}_untrained_in_val_baselines.json",
        )
    # unigram without the 256-count array to keep the public pack smaller? keep full — it's the evidence
    copy_file(GATE_J / "byte_unigram_val.json", BUNDLE / "05_validation" / "byte_unigram" / "byte_unigram_val.json")

    copy_file(GATE_J / "p1-fixed-d20-3x_test_bpb.json", BUNDLE / "06_test_selected_dstar" / "test_eval_output" / "p1-fixed-d20-3x_test_bpb.json")
    (BUNDLE / "06_test_selected_dstar" / "TEST_TEXT_NOT_INCLUDED.txt").write_text(
        "Protected test.jsonl is not in this bundle.\n"
        "SHA-256 3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf\n"
        "See manifests/test_manifest.json and manifests/test_access_log.json.\n"
    )

    copy_file(csv_path, BUNDLE / "07_results" / "primary_table.csv")
    copy_file(results_dir / "result_components.json", BUNDLE / "07_results" / "result_components.json")
    copy_file(ROOT / "docs" / "run-cards" / "RESULTS-p1.1-aspredicted-306780.md", BUNDLE / "07_results" / "RESULTS-p1.1-aspredicted-306780.md")
    copy_file(ROOT / "docs" / "run-cards" / "MODEL-CARD-p1-fixed-d20-3x.md", BUNDLE / "07_results" / "MODEL-CARD-p1-fixed-d20-3x.md")
    copy_file(ROOT / "docs" / "run-cards" / "SIGNOFF-gate-l.md", BUNDLE / "07_results" / "SIGNOFF-gate-l.md")
    (BUNDLE / "07_results" / "figures").mkdir(parents=True, exist_ok=True)
    (BUNDLE / "07_results" / "figures" / "README.txt").write_text(
        "No confirmatory figure is required. Primary evidence is primary_table.csv and result_components.json.\n"
    )

    # first MANIFEST (before filled checklist, so checklist can cite it)
    manifest_lines = []
    for p in sorted(BUNDLE.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(BUNDLE).as_posix()
        if rel.startswith("08_integrity/"):
            continue
        manifest_lines.append(f"{sha256_file(p)}  {rel}")
    man_text = "\n".join(manifest_lines) + "\n"
    man_path = BUNDLE / "08_integrity" / "MANIFEST.sha256"
    man_path.parent.mkdir(parents=True, exist_ok=True)
    man_path.write_text(man_text)
    hashes["archive_manifest"] = sha256_file(man_path)

    archive_meta = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "registration": "AsPredicted #306780",
        "run_id": RUN_ID,
        "bundle_path": "transfer/p1.1-closeout-bundle-20260816/",
        "created_at_utc": NOW,
        "access_policy": "No ResearchBox passcode. No test.jsonl. No API keys. Checkpoint weights omitted; SHA-256 pointers only.",
        "retention": "Keep with the Mac project tree and ResearchBox #8735 deposit pack.",
        "manifest_sha256": hashes["archive_manifest"],
        "selection_record_sha256": hashes["selection_record"],
        "test_result_sha256": hashes["test_bpb"],
        "weights_location": f"artifacts/p1/{RUN_ID}/checkpoints/",
        "pod_id_at_export": "68bei7d3vx4krc",
    }
    dump_json(BUNDLE / "08_integrity" / "archive_metadata.json", archive_meta)
    (BUNDLE / "08_integrity" / "verification_log.txt").write_text(
        f"created_at_utc {NOW}\n"
        f"files_in_manifest {len(manifest_lines)}\n"
        f"manifest_sha256 {hashes['archive_manifest']}\n"
        "verified_locally by scripts/p1/build_aspredicted_closeout.py after write\n"
        "weights omitted; verify model_000294.pt against manifests/final_checkpoint_manifest.json\n"
        "test text omitted; verify test.jsonl SHA against manifests/test_manifest.json if redistributing privately\n"
    )

    # verify manifest
    bad = []
    for line in manifest_lines:
        digest, rel = line.split("  ", 1)
        got = sha256_file(BUNDLE / rel)
        if got != digest:
            bad.append(rel)
    if bad:
        raise SystemExit(f"manifest mismatch: {bad}")

    hashes["now"] = NOW
    (ART / "closeout" / "hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    print(json.dumps({k: hashes[k] for k in (
        "selection_record", "final_checkpoint_manifest", "archive_manifest",
        "test_bpb", "val_baselines_summary", "evaluator", "gate_ledger",
        "primary_table", "aspredicted_pdf", "clarifications",
        "trainlog_8", "trainlog_12", "trainlog_16", "trainlog_20",
        "val_8", "val_12", "val_16", "val_20", "meta_8", "meta_12", "meta_16", "meta_20",
        "runcard_8", "runcard_12", "runcard_16", "runcard_20",
    )}, indent=2))


if __name__ == "__main__":
    main()
