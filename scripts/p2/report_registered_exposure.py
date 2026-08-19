#!/usr/bin/env python3
"""P2 registered exposure / Q8 disclosure reconstruction.

Uses frozen English BPE and frozen TRAIN jsonl / mix_order only.
Refuses test.jsonl, english_test.jsonl, confirmatory BPB, and GPU.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

from nanochat.tokenizer import RustBPETokenizer  # noqa: E402

P2_RUN_ID = os.environ.get("P2_RUN_ID", "p2-20260817T150944Z-de99f8a")
BASE = Path(os.environ.get("NANOCHAT_BASE_DIR", ROOT / "data/cache" / P2_RUN_ID))
TOKENIZER_DIR = BASE / "tokenizer"
OUT = ROOT / "docs/run-cards/p2" / P2_RUN_ID / "registered-reporting-q3-q8.json"

EXPECTED_TOK = "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6"
EXPECTED_EN_TRAIN = "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a"
EXPECTED_TL_TRAIN = "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687"
EXPECTED_MIX = "b6ae432b625b6768f84db3f45c411378d1d5a5fdbd15cbfc0e5f6c511196b1a0"
FORBIDDEN = (
    "english_test.jsonl",
    "test.jsonl",
    "test/test.jsonl",
)
D_PHASE2 = 294 * 65536
# Gate G already counted English train BPE tokens (same tokenizer, no BOS).
GATE_G_EN_TRAIN = {
    "n_docs": 28472,
    "n_tokens": 118286771,
    "n_bytes": 539903397,
    "n_chars": 538902181,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def refuse_test(path: Path) -> None:
    posix = path.as_posix()
    for bad in FORBIDDEN:
        if posix.endswith(bad) or f"/{bad}" in posix:
            raise SystemExit(f"refused test path: {path}")


def load_jsonl(path: Path, expected: str) -> list[dict]:
    refuse_test(path)
    actual = sha256_file(path)
    if actual != expected:
        raise SystemExit(f"hash mismatch {path}: {actual}")
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line:
            rows.append(json.loads(line))
    return rows


def drop_audit(rows: list[dict], split: str) -> dict:
    n = len(rows)
    null_empty = 0
    over = 0
    for r in rows:
        text = r.get("text")
        if text is None or (isinstance(text, str) and text.replace("\r\n", "\n").strip() == ""):
            null_empty += 1
            continue
        if len(text) > 200_000:
            over += 1
    dropped = null_empty + over
    return {
        "split": split,
        "n_documents_kept": n,
        "null_or_empty_after_lf": null_empty,
        "length_gt_200000_chars": over,
        "dropped_if_rules_applied_to_kept_file": dropped,
        "drop_fraction_of_kept": dropped / n if n else None,
        "stop_threshold_5pct_crossed": (dropped / n > 0.05) if n else False,
        "note": "Audit of the frozen kept jsonl. Units already absent from this file are not reconstructable here.",
    }


def count_tokens(tokenizer, texts: list[str], batch_size: int = 256) -> dict:
    n_tokens = 0
    n_bytes = 0
    n_chars = 0
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        encoded = tokenizer.encode(batch)
        n_tokens += sum(len(ids) for ids in encoded)
        n_bytes += sum(len(t.encode("utf-8")) for t in batch)
        n_chars += sum(len(t) for t in batch)
    return {
        "n_docs": len(texts),
        "n_tokens": n_tokens,
        "n_bytes": n_bytes,
        "n_chars": n_chars,
        "bos_prepended": False,
        "packing": False,
        "crop": False,
    }


def main() -> None:
    tok_pkl = TOKENIZER_DIR / "tokenizer.pkl"
    actual_tok = sha256_file(tok_pkl)
    if actual_tok != EXPECTED_TOK:
        raise SystemExit(f"tokenizer mismatch {actual_tok}")
    tokenizer = RustBPETokenizer.from_directory(str(TOKENIZER_DIR))

    en_train = load_jsonl(ROOT / "data/interim/wikitext-103/english_train.jsonl", EXPECTED_EN_TRAIN)
    tl_train = load_jsonl(ROOT / "data/interim/wikitext-tl39/splits/train.jsonl", EXPECTED_TL_TRAIN)
    mix_path = ROOT / "data/interim/p2-mix-a3-50-50/mix_order.jsonl"
    refuse_test(mix_path)
    if sha256_file(mix_path) != EXPECTED_MIX:
        raise SystemExit("mix_order hash mismatch")
    mix_rows = [json.loads(line) for line in mix_path.read_text(encoding="utf-8").splitlines() if line]

    tl_by_id = {r["doc_id"]: r["text"] for r in tl_train}
    mix_tl_ids = [r["doc_id"] for r in mix_rows if r["language"] == "tl"]
    mix_en_n = sum(1 for r in mix_rows if r["language"] == "en")
    mix_tl_n = len(mix_tl_ids)
    if mix_en_n != 28472 or mix_tl_n != 28472:
        raise SystemExit(f"unexpected mix counts en={mix_en_n} tl={mix_tl_n}")

    tl_full = count_tokens(tokenizer, [r["text"] for r in tl_train])
    tl_mix = count_tokens(tokenizer, [tl_by_id[i] for i in mix_tl_ids])

    en = dict(GATE_G_EN_TRAIN)
    a3_tokens = en["n_tokens"] + tl_mix["n_tokens"]
    a3_bytes = en["n_bytes"] + tl_mix["n_bytes"]
    a3_docs = en["n_docs"] + tl_mix["n_docs"]

    def arm(name, n_docs, n_bytes, n_tokens, stream):
        epochs = D_PHASE2 / n_tokens if n_tokens else None
        return {
            "arm": name,
            "stream": stream,
            "unique_documents": n_docs,
            "canonical_utf8_bytes": n_bytes,
            "unique_bpe_tokens_no_bos": n_tokens,
            "D_phase2_model_visible_tokens": D_PHASE2,
            "revisit_epochs": epochs,
            "revisit_definition": "D_phase2 / unique_BPE_tokens_in_stream; values < 1 mean the unique stream was not fully replayed",
            "not_used_to_pick_arms": True,
        }

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
        "aspredicted_id": 306935,
        "role": "registered_reporting_reconstruction_not_confirmatory",
        "built_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "refused_test_reads": True,
        "computed_bpb": False,
        "tokenizer_pkl_sha256": actual_tok,
        "english_train_reused_from_gate_g": True,
        "drop_audit": [
            drop_audit(en_train, "english_train_jsonl"),
            drop_audit(tl_train, "tagalog_train_jsonl"),
        ],
        "a3_realized_shares": {
            "unit": "documents_not_tokens",
            "K": 28472,
            "n_en_docs": mix_en_n,
            "n_tl_docs": mix_tl_n,
            "document_share_en": 0.5,
            "document_share_tl": 0.5,
            "utf8_bytes_en": en["n_bytes"],
            "utf8_bytes_tl": tl_mix["n_bytes"],
            "byte_share_en": en["n_bytes"] / a3_bytes,
            "byte_share_tl": tl_mix["n_bytes"] / a3_bytes,
            "bpe_tokens_en": en["n_tokens"],
            "bpe_tokens_tl": tl_mix["n_tokens"],
            "token_share_en": en["n_tokens"] / a3_tokens,
            "token_share_tl": tl_mix["n_tokens"] / a3_tokens,
            "mix_order_sha256": EXPECTED_MIX,
            "not_mitigation": True,
        },
        "exposure_table": [
            arm("A1", en["n_docs"], en["n_bytes"], en["n_tokens"], "official WT103-raw train"),
            arm("A2", tl_full["n_docs"], tl_full["n_bytes"], tl_full["n_tokens"], "frozen P1.1 Tagalog train"),
            arm("A3", a3_docs, a3_bytes, a3_tokens, "seed-42 50/50-document mix of first K per language"),
        ],
        "a2_full_tagalog_train_bpe": tl_full,
        "a3_mix_tagalog_subset_bpe": tl_mix,
        "q8_descriptive_status": {
            "unique_docs_bytes_tokens_epochs": "published_in_this_record",
            "a2_english_trajectory": {
                "status": "registered_descriptive_item_not_completed_in_main_report",
                "reason": "A2 in-loop Validation bpb used the Tagalog data-dir last shard (diagnostic Tagalog), not English val. No A2 English BPB series was collected. Do not treat Tagalog in-loop numbers as an English trajectory.",
                "archived_a2_inloop_tagalog_val_bpb": [
                    {"step": 0, "R_d": 0.0, "inloop_val_bpb": 4.821579},
                    {"step": 50, "R_d": 50 / 294, "inloop_val_bpb": 1.586062},
                    {"step": 100, "R_d": 100 / 294, "inloop_val_bpb": 1.283334},
                    {"step": 150, "R_d": 150 / 294, "inloop_val_bpb": 1.181419},
                    {"step": 200, "R_d": 200 / 294, "inloop_val_bpb": 1.142912},
                    {"step": 250, "R_d": 250 / 294, "inloop_val_bpb": 1.123591},
                    {"step": 294, "R_d": 1.0, "inloop_val_bpb": 1.117633},
                ],
                "inloop_is_not_val_bpb_full": True,
            },
            "ptpp_R_d": {
                "status": "definition_and_arithmetic_reported; english_BPB_vs_R_d_plot_not_made",
                "phase2_definition": "R_d(step) = (step * 65536) / 19267584 = step/294",
                "en0_d20_data_over_p_scaling": 0.8154704414171663,
                "phase2_d20_D_over_p_scaling": 19267584 / 435160240,
                "source_gate_g": "docs/run-cards/p2/p2-20260817T150944Z-de99f8a/gate-g-budget.json",
                "not_a_primary_hypothesis": True,
            },
            "fertility": {
                "status": "computed_at_gate_f_descriptive_tokenizer_characterization",
                "english_val_bytes_per_token": 4.602618964388031,
                "tagalog_val_bytes_per_token": 2.573578318207698,
                "not_forgetting_evidence": True,
                "source": "docs/run-cards/p2/p2-20260817T150944Z-de99f8a/gate-f-tokenizer.json",
            },
            "p11_d20_on_english_utf8_ood": {
                "status": "registered_descriptive_item_not_run",
                "reason": "No P1.1-weights-on-WT103 English BPB was computed in P2. Not BWT. Will not be run as a post-outcome P2 rescue.",
            },
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"out": str(OUT), "a3_token_share_en": payload["a3_realized_shares"]["token_share_en"], "a3_token_share_tl": payload["a3_realized_shares"]["token_share_tl"], "A2_tokens": tl_full["n_tokens"], "A2_epochs": D_PHASE2 / tl_full["n_tokens"]}, indent=2))


if __name__ == "__main__":
    main()
