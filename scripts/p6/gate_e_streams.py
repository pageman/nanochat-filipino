#!/usr/bin/env python3
"""P6 Gate E: C1/C2 copy + four topology packed streams from filed schedules.

M-fine reuses P4 C3 byte-identically (same origin-mask SHA).
M-coarse / M-blocked / M-rand are built from TSV schedules on the shared
within-language token streams. Mac/CPU. Blinded. No BPB.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import shutil
import stat
import sys
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "vendor" / "nanochat"))

from pack_parquet import pack_dir  # noqa: E402
from p6_common import (  # noqa: E402
    ASPREDICTED_ID,
    BASE,
    C1_DIR,
    C2_DIR,
    D_PHASE2,
    DOC_ORDER_SEED,
    EN_TRAIN_JSONL,
    EXPECTED,
    LOCKBOX,
    LOCK_PATH,
    MIX_MANIFEST_SHA,
    P4_BASE,
    P6_RUN_ID,
    ROOT,
    RUN_CARD,
    TL_TRAIN_JSONL,
    TOK_DIR,
    TOKEN_BYTES_SHA,
    TOKENIZER_PKL_SHA,
    TOPOLOGY_ARMS,
    TOPOLOGY_MANIFEST,
    TOPOLOGY_MANIFEST_SHA,
    blinded_print,
    freeze_file,
    mark_ledger,
    sha256_file,
    utc_now,
    write_json,
)

OUT = RUN_CARD / "gate-e-packed-streams.json"
IDENTITY = ROOT / "manifests" / "p6" / "p6_mix_identity.json"
P4_MANIFEST = ROOT / "manifests" / "p4" / "p4_mix_manifest.json"
STREAMS = BASE / "streams"


def copy_tree(src_dir: Path, dst_dir: Path, expected: dict[str, str]) -> list[dict]:
    rows = []
    dst_dir.mkdir(parents=True, exist_ok=True)
    try:
        dst_dir.chmod(dst_dir.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
    except OSError:
        pass
    for name, exp in expected.items():
        src = src_dir / name
        dst = dst_dir / name
        if not src.is_file():
            raise SystemExit(f"missing artifact {src}")
        if dst.exists():
            dst.chmod(0o644)
        shutil.copy2(src, dst)
        got = sha256_file(dst)
        freeze_file(dst)
        rows.append({"file": name, "expected": exp, "sha256": got, "ok": got == exp})
    try:
        dst_dir.chmod(0o555)
    except OSError:
        pass
    return rows


def load_train(path: Path, expected: str) -> list[dict]:
    if "val" in path.name.lower() or "test" in path.name.lower():
        raise SystemExit(f"mix refuses val/test path {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise SystemExit(f"hash mismatch {path}: {actual}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sha_sort_then_shuffle(rows: list[dict], seed: int) -> list[dict]:
    ordered = sorted(rows, key=lambda r: hashlib.sha256(r["text"].encode("utf-8")).hexdigest())
    rng = random.Random(seed)
    rng.shuffle(ordered)
    return ordered


def fill_quota(docs: list[dict], encode_one, target: int, language: str) -> array:
    tokens = array("I")
    n = len(docs)
    cache: dict[int, list[int]] = {}
    i = 0
    while len(tokens) < target:
        j = i % n
        if j not in cache:
            ids = encode_one(docs[j]["text"])
            cache[j] = ids
            if i and i % 400 == 0:
                print(json.dumps({"mix_progress": language, "docs_encoded": len(cache), "tokens": len(tokens), "target": target}), flush=True)
        ids = cache[j]
        if not ids:
            i += 1
            continue
        need = target - len(tokens)
        if len(ids) <= need:
            tokens.extend(ids)
        else:
            tokens.extend(ids[:need])
        i += 1
    return tokens


def read_schedule(path: Path) -> list[tuple[str, int, int]]:
    blocks = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            blocks.append((row["language"], int(row["source_offset_tokens"]), int(row["length_tokens"])))
    return blocks


def apply_schedule(en: array, tl: array, blocks: list[tuple[str, int, int]]) -> tuple[array, bytearray]:
    mixed = array("I")
    mask = bytearray()
    for lang, offset, length in blocks:
        src = en if lang == "EN" else tl
        if lang not in ("EN", "TL"):
            raise SystemExit(f"bad language {lang}")
        take = src[offset : offset + length]
        if len(take) != length:
            raise SystemExit(f"schedule slice miss {lang}@{offset}+{length}")
        mixed.extend(take)
        mask.extend((b"\x00" if lang == "EN" else b"\x01") * length)
    return mixed, mask


def pack_mixed_arm(arm_id: str, mixed: array, mask: bytearray, tokenizer, dest: Path, expected_mask_sha: str) -> dict:
    LOCKBOX.mkdir(parents=True, exist_ok=True)
    mask_path = LOCKBOX / f"{arm_id}_language_origin_mask.bin"
    if mask_path.exists():
        mask_path.chmod(0o644)
    mask_path.write_bytes(bytes(mask))
    mask_path.chmod(0o600)
    mask_sha = sha256_file(mask_path)
    if mask_sha != expected_mask_sha:
        raise SystemExit(f"{arm_id} mask SHA mismatch got={mask_sha} expected={expected_mask_sha}")

    # Decode as schedule blocks for parquet rows (variable block sizes OK)
    block_texts = []
    # Use contiguous decode chunks of up to 2048 for packing density similar to P4
    chunk = 2048
    for i in range(0, len(mixed), chunk):
        ids = mixed[i : i + chunk].tolist()
        block_texts.append({"doc_id": f"{arm_id}-block-{i // chunk:05d}", "text": tokenizer.decode(ids)})

    dest.mkdir(parents=True, exist_ok=True)
    try:
        dest.chmod(dest.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
    except OSError:
        pass
    for stale in dest.glob("*.parquet"):
        stale.chmod(0o644)
        stale.unlink()
    dummy_val = [{"doc_id": "placeholder", "text": "placeholder"}]
    pack = pack_dir(dest, block_texts, dummy_val)
    # Replace val with C2 val (English validation holdout for training loop)
    src_val = C2_DIR / "val.parquet"
    dst_val = dest / "val.parquet"
    if dst_val.exists():
        dst_val.chmod(0o644)
    shutil.copy2(src_val, dst_val)
    freeze_file(dst_val)
    try:
        dest.chmod(0o555)
    except OSError:
        pass

    train_shards = sorted(dest.glob("train_*.parquet"))
    h = hashlib.sha256()
    shard_rows = []
    for p in train_shards:
        s = sha256_file(p)
        h.update(s.encode())
        h.update(p.name.encode())
        shard_rows.append({"file": p.name, "sha256": s})
    shard_rows.append({"file": "val.parquet", "sha256": sha256_file(dst_val)})
    return {
        "arm": arm_id,
        "dir": str(dest.relative_to(ROOT)),
        "mask_sha256": mask_sha,
        "full_stream_sha256": h.hexdigest(),
        "len_tokens": len(mixed),
        "achieved_tl": mask.count(1),
        "achieved_en": mask.count(0),
        "shards": shard_rows,
        "pack": pack,
    }


def main() -> int:
    checks = []

    def record(cid: str, ok: bool, detail) -> None:
        checks.append({"id": cid, "ok": bool(ok), "detail": detail})

    topo_sha = sha256_file(TOPOLOGY_MANIFEST)
    record("E0_topology_manifest", topo_sha == TOPOLOGY_MANIFEST_SHA, topo_sha)
    topo = json.loads(TOPOLOGY_MANIFEST.read_text(encoding="utf-8"))
    by_id = {t["id"]: t for t in topo["topologies"]}

    c1 = copy_tree(P4_BASE / "streams" / "c1_tl", C1_DIR, EXPECTED["c1_shards"])
    c2 = copy_tree(P4_BASE / "streams" / "c2_en", C2_DIR, EXPECTED["c2_shards"])
    record("E1_c1_hashes", all(r["ok"] for r in c1), c1)
    record("E2_c2_hashes", all(r["ok"] for r in c2), c2)

    m_fine_dir = STREAMS / "m-fine"
    m_fine = copy_tree(P4_BASE / "streams" / "c3_mix", m_fine_dir, EXPECTED["m_fine_shards"])
    record("E3_m_fine_reuse_p4_c3", all(r["ok"] for r in m_fine), m_fine)

    mask_src = P4_BASE / "lockbox" / "c3_language_origin_mask.bin"
    mask_dst = LOCKBOX / "m-fine_language_origin_mask.bin"
    LOCKBOX.mkdir(parents=True, exist_ok=True)
    if mask_dst.exists():
        mask_dst.chmod(0o644)
    shutil.copy2(mask_src, mask_dst)
    mask_dst.chmod(0o600)
    m_fine_mask = sha256_file(mask_dst)
    freeze_file(mask_dst)
    record(
        "E4_m_fine_mask",
        m_fine_mask == EXPECTED["language_origin_mask_sha256_m_fine"] == by_id["m-fine"]["language_origin_mask_sha256"],
        m_fine_mask,
    )

    p4_manifest_sha = sha256_file(P4_MANIFEST) if P4_MANIFEST.is_file() else None
    record("E5_p4_mix_manifest_reference", p4_manifest_sha == MIX_MANIFEST_SHA, p4_manifest_sha)

    # Build shared within-language streams once, then apply each non-fine schedule
    tok_sha = sha256_file(TOK_DIR / "tokenizer.pkl")
    bytes_sha = sha256_file(TOK_DIR / "token_bytes.pt")
    if tok_sha != TOKENIZER_PKL_SHA or bytes_sha != TOKEN_BYTES_SHA:
        raise SystemExit("tokenizer SHA mismatch at E")

    from nanochat.tokenizer import RustBPETokenizer

    tokenizer = RustBPETokenizer.from_directory(str(TOK_DIR))

    def encode_one(text: str) -> list[int]:
        return tokenizer.encode(text)

    target_tl = target_en = D_PHASE2 // 2
    print(json.dumps({"gate": "E", "phase": "fill_quota", "target_tl": target_tl, "target_en": target_en}), flush=True)
    tl_docs = sha_sort_then_shuffle(load_train(TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"]), DOC_ORDER_SEED)
    en_docs = sha_sort_then_shuffle(load_train(EN_TRAIN_JSONL, EXPECTED["en_train_jsonl"]), DOC_ORDER_SEED)
    tl_tokens = fill_quota(tl_docs, encode_one, target_tl, "tl")
    en_tokens = fill_quota(en_docs, encode_one, target_en, "en")
    record("E6_within_language_quotas", len(tl_tokens) == target_tl and len(en_tokens) == target_en, {"tl": len(tl_tokens), "en": len(en_tokens)})

    built = {"m-fine": {"dir": str(m_fine_dir.relative_to(ROOT)), "mask_sha256": m_fine_mask, "reuse": "p4_c3_byte_identical"}}
    for arm_id in ("m-coarse", "m-blocked", "m-rand"):
        meta = by_id[arm_id]
        sched_path = ROOT / meta["schedule_file"]
        got_sched = sha256_file(sched_path)
        if got_sched != meta["schedule_file_sha256"]:
            raise SystemExit(f"{arm_id} schedule file SHA mismatch")
        blocks = read_schedule(sched_path)
        print(json.dumps({"gate": "E", "phase": "apply_schedule", "arm": arm_id, "blocks": len(blocks)}), flush=True)
        mixed, mask = apply_schedule(en_tokens, tl_tokens, blocks)
        if len(mixed) != D_PHASE2:
            raise SystemExit(f"{arm_id} mixed length {len(mixed)} != {D_PHASE2}")
        row = pack_mixed_arm(arm_id, mixed, mask, tokenizer, STREAMS / arm_id, meta["language_origin_mask_sha256"])
        built[arm_id] = row
        record(f"E7_{arm_id}_quotas", row["achieved_tl"] == target_tl and row["achieved_en"] == target_en, row)

    # Schedule file hashes for all four
    sched_ok = True
    sched_detail = {}
    for arm_id in TOPOLOGY_ARMS:
        meta = by_id[arm_id]
        path = ROOT / meta["schedule_file"]
        got = sha256_file(path)
        sched_detail[arm_id] = {"got": got, "expected": meta["schedule_file_sha256"], "ok": got == meta["schedule_file_sha256"]}
        sched_ok = sched_ok and sched_detail[arm_id]["ok"]
    record("E8_schedule_files", sched_ok, sched_detail)

    identity = {
        "p6_run_id": P6_RUN_ID,
        "topology_manifest_sha256": TOPOLOGY_MANIFEST_SHA,
        "mix_manifest_sha256_p4_reference": MIX_MANIFEST_SHA,
        "within_language_stream_rule": "shared P4-lineage EN/TL token streams; only cross-language schedule differs",
        "m_fine_reuse": "byte_identical_p4_c3",
        "arms": built,
        "created_utc": utc_now(),
    }
    write_json(IDENTITY, identity)
    freeze_file(IDENTITY)

    ok = all(c["ok"] for c in checks)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P6-M-SCHEDULE-TOPOLOGY",
        "aspredicted_id": ASPREDICTED_ID,
        "gate": "E",
        "status": "pass" if ok else "fail",
        "at_utc": utc_now(),
        "host": "Mac/CPU",
        "gpu": False,
        "blinded": True,
        "p6_run_id": P6_RUN_ID,
        "script": "scripts/p6/gate_e_streams.py",
        "checks": checks,
        "mix_identity": str(IDENTITY.relative_to(ROOT)),
        "topology_arms": list(TOPOLOGY_ARMS),
        "no_p6_outcomes": True,
        "no_bpb": True,
        "next_gate": "G",
    }
    write_json(OUT, payload)
    if ok:
        lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        lock["gate_statuses"]["E"] = "pass"
        lock["status"] = "gate_e_pass"
        lock["p6_mix_identity"] = str(IDENTITY.relative_to(ROOT))
        write_json(LOCK_PATH, lock)
        mark_ledger("E", "pass", str(OUT.relative_to(ROOT)), "G")
    blinded_print("E", payload["status"], {"path": str(OUT.relative_to(ROOT)), "failed": [c["id"] for c in checks if not c["ok"]]})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
