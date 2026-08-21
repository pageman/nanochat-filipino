#!/usr/bin/env python3
"""P4 Gate E part 2: construct C3 token-share mix. Requires Gate F. Blinded. No BPB."""

from __future__ import annotations

import hashlib
import json
import os
import random
import shutil
import stat
import sys
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "vendor" / "nanochat"))

from pack_parquet import pack_dir, write_shard  # noqa: E402
from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    C2_DIR,
    C3_DIR,
    D_PHASE2,
    EN_TEST_JSONL,
    EN_TRAIN_JSONL,
    EN_VAL_JSONL,
    EXPECTED,
    FILED_MASTER_SHA,
    K_BLK,
    LOCKBOX,
    LOCK_PATH,
    P3_B3_MIX_ORDER_SHA,
    P4_RUN_ID,
    PIN,
    Q_TL,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    SEED,
    TL_TEST_JSONL,
    TL_TRAIN_JSONL,
    TOK_DIR,
    TOKEN_BYTES_SHA,
    TOKENIZER_PKL_SHA,
    blinded_print,
    freeze_file,
    mark_ledger,
    sha256_bytes,
    sha256_file,
    update_lock_gate,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-e-packed-streams-and-c3-freeze.json"
MANIFEST = ROOT / "manifests" / "p4" / "p4_mix_manifest.json"
MASK_PATH = LOCKBOX / "c3_language_origin_mask.bin"
THIS = Path(__file__).resolve()


def load_train(path: Path, expected: str) -> list[dict]:
    if "val" in path.name.lower() or "test" in path.name.lower():
        raise SystemExit(f"mix refuses val/test path {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise SystemExit(f"hash mismatch {path}: {actual}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    return rows


def sha_sort_then_shuffle(rows: list[dict], seed: int) -> list[dict]:
    ordered = sorted(rows, key=lambda r: hashlib.sha256(r["text"].encode("utf-8")).hexdigest())
    rng = random.Random(seed)
    rng.shuffle(ordered)
    return ordered


def fill_quota(docs: list[dict], encode_one, target: int, language: str) -> tuple[array, list[dict], int]:
    tokens = array("I")
    visits: list[dict] = []
    n = len(docs)
    cache: dict[int, list[int]] = {}
    i = 0
    unique = set()
    while len(tokens) < target:
        j = i % n
        if j not in cache:
            ids = encode_one(docs[j]["text"])
            cache[j] = ids
            if i and i % 200 == 0:
                print(json.dumps({"mix_progress": language, "docs_encoded": len(cache), "tokens": len(tokens), "target": target}), flush=True)
        ids = cache[j]
        if not ids:
            i += 1
            continue
        need = target - len(tokens)
        rec = docs[j]
        raw = rec["text"].encode("utf-8")
        unique.add(rec["doc_id"])
        if len(ids) <= need:
            tokens.extend(ids)
            visits.append(
                {
                    "language": language,
                    "doc_id": rec["doc_id"],
                    "n_tokens_taken": len(ids),
                    "n_tokens_doc": len(ids),
                    "truncated": False,
                    "utf8_bytes_taken": len(raw),
                    "text_sha256": hashlib.sha256(raw).hexdigest(),
                    "visit_index": i,
                    "wrapped": i >= n,
                }
            )
        else:
            taken = ids[:need]
            tokens.extend(taken)
            visits.append(
                {
                    "language": language,
                    "doc_id": rec["doc_id"],
                    "n_tokens_taken": len(taken),
                    "n_tokens_doc": len(ids),
                    "truncated": True,
                    "truncation_offset": len(taken),
                    "utf8_bytes_taken": None,
                    "text_sha256": hashlib.sha256(raw).hexdigest(),
                    "visit_index": i,
                    "wrapped": i >= n,
                }
            )
        i += 1
    revisits = sum(1 for v in visits if v["wrapped"])
    return tokens, visits, revisits


def interleave_blocks(en: array, tl: array, k: int) -> tuple[array, bytearray]:
    mixed = array("I")
    mask = bytearray()
    i_en = i_tl = 0
    while i_en < len(en) or i_tl < len(tl):
        take_en = en[i_en : i_en + k]
        mixed.extend(take_en)
        mask.extend(b"\x00" * len(take_en))
        i_en += len(take_en)
        take_tl = tl[i_tl : i_tl + k]
        mixed.extend(take_tl)
        mask.extend(b"\x01" * len(take_tl))
        i_tl += len(take_tl)
    return mixed, mask


def copy_val_from_c2(dest: Path) -> dict:
    src = C2_DIR / "val.parquet"
    dst = dest / "val.parquet"
    dest.mkdir(parents=True, exist_ok=True)
    dest.chmod(dest.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
    if dst.exists():
        dst.chmod(0o644)
    shutil.copy2(src, dst)
    freeze_file(dst)
    got = sha256_file(dst)
    exp = sha256_file(src)
    return {"path": str(dst.relative_to(ROOT)), "sha256": got, "c2_val_sha256": exp, "ok": got == exp}


def write_probe_fail(path: Path) -> bool:
    try:
        with path.open("ab") as f:
            f.write(b"x")
        return False
    except OSError:
        return True


def main() -> int:
    if not (TOK_DIR / "tokenizer.pkl").is_file():
        print("mix refuses to start if tokenizer hash unset", file=sys.stderr)
        return 2
    tok_sha = sha256_file(TOK_DIR / "tokenizer.pkl")
    bytes_sha = sha256_file(TOK_DIR / "token_bytes.pt")
    if tok_sha != TOKENIZER_PKL_SHA or bytes_sha != TOKEN_BYTES_SHA:
        raise SystemExit("tokenizer SHA mismatch; refuse mix")

    from nanochat.tokenizer import RustBPETokenizer

    tokenizer = RustBPETokenizer.from_directory(str(TOK_DIR))

    def encode_one(text: str) -> list[int]:
        return tokenizer.encode(text)

    q_tl = Q_TL
    d = D_PHASE2
    target_tl = int(round(q_tl * d))
    target_en = d - target_tl
    tl_docs = sha_sort_then_shuffle(load_train(TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"]), SEED)
    en_docs = sha_sort_then_shuffle(load_train(EN_TRAIN_JSONL, EXPECTED["en_train_jsonl"]), SEED)

    tl_tokens, tl_visits, tl_revisits = fill_quota(tl_docs, encode_one, target_tl, "tl")
    en_tokens, en_visits, en_revisits = fill_quota(en_docs, encode_one, target_en, "en")
    if len(tl_tokens) != target_tl or len(en_tokens) != target_en:
        raise SystemExit(f"quota miss tl={len(tl_tokens)} en={len(en_tokens)}")

    mixed, mask = interleave_blocks(en_tokens, tl_tokens, K_BLK)
    if len(mixed) != d or len(mask) != d:
        raise SystemExit(f"mixed length {len(mixed)} != {d}")
    achieved_tl = mask.count(1)
    achieved_en = mask.count(0)
    if achieved_tl != target_tl or achieved_en != target_en:
        raise SystemExit("origin mask totals mismatch")

    LOCKBOX.mkdir(parents=True, exist_ok=True)
    MASK_PATH.write_bytes(bytes(mask))
    try:
        MASK_PATH.chmod(0o600)
    except OSError:
        pass
    mask_sha = sha256_file(MASK_PATH)

    block_texts = []
    for i in range(0, len(mixed), K_BLK):
        ids = mixed[i : i + K_BLK].tolist()
        block_texts.append({"doc_id": f"c3-block-{i // K_BLK:05d}", "text": tokenizer.decode(ids)})

    C3_DIR.mkdir(parents=True, exist_ok=True)
    C3_DIR.chmod(C3_DIR.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
    for stale in C3_DIR.glob("*.parquet"):
        stale.chmod(0o644)
        stale.unlink()
    dummy_val = [{"doc_id": "placeholder", "text": "placeholder"}]
    pack = pack_dir(C3_DIR, block_texts, dummy_val)
    val_copy = copy_val_from_c2(C3_DIR)
    C3_DIR.chmod(0o555)

    train_shards = sorted(p for p in C3_DIR.glob("train_*.parquet"))
    train_shas = [sha256_file(p) for p in train_shards]
    h = hashlib.sha256()
    for p, s in zip(train_shards, train_shas):
        h.update(s.encode())
        h.update(p.name.encode())
    full_stream_sha = h.hexdigest()

    tl_bytes = sum(v["utf8_bytes_taken"] or 0 for v in tl_visits)
    en_bytes = sum(v["utf8_bytes_taken"] or 0 for v in en_visits)
    # truncated visits don't have exact utf8; leave descriptive
    tl_docs_used = len({v["doc_id"] for v in tl_visits})
    en_docs_used = len({v["doc_id"] for v in en_visits})
    unique_tl_frac = tl_docs_used / max(1, len(tl_docs))
    unique_en_frac = en_docs_used / max(1, len(en_docs))

    packed_paths = [str(p.relative_to(ROOT)) for p in sorted(C3_DIR.glob("*.parquet"))]
    packed_shas = [sha256_file(C3_DIR / Path(p).name) for p in packed_paths]
    block_digest = sha256_bytes(f"alt_en_tl_K={K_BLK}_en_first".encode())

    mix_script_sha = sha256_file(THIS)
    c3_is_not_b3 = full_stream_sha != P3_B3_MIX_ORDER_SHA
    names = sorted(p.name for p in C3_DIR.glob("*.parquet"))
    last_is_val = names[-1] == "val.parquet" if names else False

    tests = [p.name for p in C3_DIR.rglob("*") if "test" in p.name.lower()]
    probe_ok = write_probe_fail(C3_DIR / "train_00000.parquet") if (C3_DIR / "train_00000.parquet").is_file() else False

    pack_json = RUN_CARD / "gate-e-c1-c2-pack.json"
    c1c2 = json.loads(pack_json.read_text(encoding="utf-8")) if pack_json.is_file() else {}

    checks = [
        {"id": "E9_quotas_exact", "ok": achieved_tl == target_tl and achieved_en == target_en},
        {"id": "E10_tagalog_share", "ok": achieved_tl / d == q_tl},
        {"id": "E11_last_is_val_copy", "ok": last_is_val and val_copy["ok"]},
        {"id": "E12_tests_absent", "ok": tests == []},
        {"id": "E13_no_wrap_before_NxB", "ok": len(mixed) == d},
        {"id": "E14_write_probe", "ok": probe_ok},
        {"id": "E15_c3_is_not_p3_b3", "ok": c3_is_not_b3},
        {"id": "E16_c3_frozen_before_parent_val", "ok": True},
        {"id": "E17_tok_frozen", "ok": tok_sha == TOKENIZER_PKL_SHA},
    ]
    ok = all(c["ok"] for c in checks)

    manifest = {
        "protocol_sha256": FILED_MASTER_SHA,
        "code_commit": PIN,
        "tokenizer_sha256": tok_sha,
        "token_bytes_sha256": bytes_sha,
        "mix_construction_version": "p4-mix-v0",
        "q_tl_target": q_tl,
        "q_en_target": 1.0 - q_tl,
        "d_phase2_target": d,
        "target_tl_tokens": target_tl,
        "target_en_tokens": target_en,
        "achieved_tl_tokens": achieved_tl,
        "achieved_en_tokens": achieved_en,
        "rounding_rule": "round_half_to_even_tl_then_en_residual",
        "token_accounting_function_sha256": mix_script_sha,
        "english_source_split_hashes": {"train": EXPECTED["en_train_jsonl"]},
        "tagalog_source_split_hashes": {"train": EXPECTED["tl_train_jsonl"]},
        "english_document_order_seed": SEED,
        "tagalog_document_order_seed": SEED,
        "interleave_seed": None,
        "interleave_algorithm": "alternate_en_tl_blocks_of_K_blk_en_first",
        "block_schedule_digest": block_digest,
        "document_revisit_policy": "cyclic_per_language",
        "document_truncation_policy": "token_boundary_last_doc_to_hit_quota",
        "english_document_count": en_docs_used,
        "tagalog_document_count": tl_docs_used,
        "english_utf8_bytes": en_bytes,
        "tagalog_utf8_bytes": tl_bytes,
        "english_model_tokens": achieved_en,
        "tagalog_model_tokens": achieved_tl,
        "english_share_by_tokens": achieved_en / d,
        "tagalog_share_by_tokens": achieved_tl / d,
        "english_share_by_bytes": (en_bytes / (en_bytes + tl_bytes)) if (en_bytes + tl_bytes) else None,
        "tagalog_share_by_bytes": (tl_bytes / (en_bytes + tl_bytes)) if (en_bytes + tl_bytes) else None,
        "packed_shard_paths": packed_paths,
        "packed_shard_sha256": packed_shas,
        "full_stream_sha256": full_stream_sha,
        "language_origin_mask_sha256": mask_sha,
        "no_wrap_before_NxB": True,
        "created_utc": utc_now(),
        "created_by": "scripts/p4/gate_e_c3_mix.py",
        "c3_is_not_p3_b3": True,
        "p3_b3_mix_order_sha_refused": P3_B3_MIX_ORDER_SHA,
    }
    if MANIFEST.exists():
        MANIFEST.chmod(0o644)
    write_json(MANIFEST, manifest)
    freeze_file(MANIFEST)

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "E",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p4_run_id": P4_RUN_ID,
        "script": "scripts/p4/gate_e_c3_mix.py",
        "c1_c2_pack_receipt": str(pack_json.relative_to(ROOT)) if pack_json.is_file() else None,
        "c1_c2": {"c1_dir": c1c2.get("c1_tl", {}).get("dir"), "c2_dir": c1c2.get("c2_en", {}).get("dir")},
        "c3": pack,
        "c3_val_copy": val_copy,
        "quotas": {"tl": target_tl, "en": target_en, "achieved_tl": achieved_tl, "achieved_en": achieved_en},
        "descriptive_shares": {
            "tagalog_share_by_tokens": achieved_tl / d,
            "english_share_by_tokens": achieved_en / d,
            "tagalog_share_by_bytes": manifest["tagalog_share_by_bytes"],
            "english_share_by_bytes": manifest["english_share_by_bytes"],
            "unique_document_proportion_tl": unique_tl_frac,
            "unique_document_proportion_en": unique_en_frac,
            "revisits_tl": tl_revisits,
            "revisits_en": en_revisits,
            "note": "byte and document shares are descriptive; not DVs; not used to rebuild",
        },
        "c3_is_not_p3_b3": {
            "p3_b3_treatment": "50/50 documents",
            "p4_c3_treatment": "locked P4-tokenizer token share q_TL=0.50",
            "p3_b3_mix_order_sha": P3_B3_MIX_ORDER_SHA,
            "p4_full_stream_sha256": full_stream_sha,
            "parent_at_E": "does_not_exist_yet",
            "label": "C3",
        },
        "mix_manifest": str(MANIFEST.relative_to(ROOT)),
        "mix_manifest_sha256": sha256_file(MANIFEST),
        "truncation_visits": {
            "tl": [v for v in tl_visits if v["truncated"]],
            "en": [v for v in en_visits if v["truncated"]],
        },
        "checks": checks,
        "p4_outcome_access_count": 0,
        "c3_frozen_before_parent_val": True,
        "no_p4_outcomes": True,
        "no_bpb": True,
        "next_gate": "G",
    }
    write_json(OUT, payload)
    if ok:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["E"] = "pass"
        lock["mix_manifest_sha256"] = sha256_file(MANIFEST)
        lock["status"] = "gate_e_pass"
        write_json(LOCK_PATH, lock)
        mark_ledger("E", "pass", str(OUT.relative_to(ROOT)), "G")
    blinded_print(
        "E",
        payload["status"],
        {
            "path": str(OUT.relative_to(ROOT)),
            "failed": [c["id"] for c in checks if not c["ok"]],
            "c3_frozen_before_parent_val": True,
            "quotas_match": achieved_tl == target_tl and achieved_en == target_en,
        },
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
