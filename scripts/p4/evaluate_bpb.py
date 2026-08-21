#!/usr/bin/env python3
"""P3 Gate P0-T: full Tagalog val_bpb_full + untrained + byte-unigram floors.

P4 copy of the P3 evaluator. MUST NOT change the BPB formula. Scalars go to --out-dir (lockbox).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

import pyarrow.parquet as pq
import torch

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402
from nanochat.tokenizer import get_token_bytes  # noqa: E402

from p4_common import (  # noqa: E402
    ASPREDICTED_ID,
    B,
    EXPECTED,
    P4_RUN_ID,
    RESEARCHBOX_ID,
    ROOT,
    RUN_CARD,
    T,
    C1_DIR as TL_DIR,
    TOKENIZER_PKL_SHA,
    TL_TRAIN_JSONL,
    TL_VAL_JSONL,
)

TL0_DEPTHS = {8: "p4-tl0-d8", 20: "p4-tl0-d20"}
TL0_STEP = 294
UNTRAINED_SEED = 0
P0_T_MARGIN = 0.01
PACKING = "bos_bestfit_buffer1000_one_pass_no_wrap"
STRIDE = "non_overlapping_T_official_bos_bestfit"
TOKENIZER_SHA = TOKENIZER_PKL_SHA


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_hash(path: Path, expected: str, label: str) -> str:
    actual = sha256_file(path)
    if actual != expected:
        raise SystemExit(f"hash mismatch {label} {path}: {actual} != {expected}")
    return actual


def parquet_texts(path: Path) -> list[str]:
    pf = pq.ParquetFile(path)
    texts: list[str] = []
    for i in range(pf.num_row_groups):
        texts.extend(pf.read_row_group(i).column("text").to_pylist())
    return texts


def jsonl_texts(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line:
            out.append(json.loads(line)["text"])
    return out


def pack_one_pass(texts: list[str], tokenizer, device_batch: int, seq_len: int, device: torch.device):
    bos = tokenizer.get_bos_token_id()
    row_capacity = seq_len + 1
    buffer_size = 1000
    tok_batch = 128
    doc_buffer: list[list[int]] = []
    src = deque(texts)

    def refill() -> bool:
        if not src:
            return False
        batch = [src.popleft() for _ in range(min(tok_batch, len(src)))]
        encoded = tokenizer.encode(batch, prepend=bos, num_threads=4)
        doc_buffer.extend(encoded)
        return True

    rows: list[torch.Tensor] = []
    row_pads: list[torch.Tensor] = []
    n_docs_packed = 0
    n_cropped = 0
    n_padded_positions = 0
    while True:
        while len(doc_buffer) < buffer_size and src:
            refill()
        if not doc_buffer:
            break
        row = torch.zeros(row_capacity, dtype=torch.long)
        pad = torch.zeros(row_capacity, dtype=torch.bool)
        pos = 0
        while pos < row_capacity:
            while len(doc_buffer) < buffer_size and src:
                refill()
            remaining = row_capacity - pos
            if not doc_buffer:
                pad[pos:] = True
                n_padded_positions += remaining
                break
            best_idx = -1
            best_len = 0
            for i, doc in enumerate(doc_buffer):
                doc_len = len(doc)
                if doc_len <= remaining and doc_len > best_len:
                    best_idx = i
                    best_len = doc_len
            if best_idx >= 0:
                doc = doc_buffer.pop(best_idx)
                row[pos : pos + len(doc)] = torch.tensor(doc, dtype=torch.long)
                pos += len(doc)
                n_docs_packed += 1
            else:
                shortest_idx = min(range(len(doc_buffer)), key=lambda i: len(doc_buffer[i]))
                doc = doc_buffer.pop(shortest_idx)
                row[pos : pos + remaining] = torch.tensor(doc[:remaining], dtype=torch.long)
                pos += remaining
                n_cropped += 1
                n_docs_packed += 1
        rows.append(row)
        row_pads.append(pad)

    batches = []
    for start in range(0, len(rows), device_batch):
        chunk = rows[start : start + device_batch]
        chunk_pad = row_pads[start : start + device_batch]
        missing = device_batch - len(chunk)
        if missing:
            chunk.extend([torch.zeros(row_capacity, dtype=torch.long)] * missing)
            chunk_pad.extend([torch.ones(row_capacity, dtype=torch.bool)] * missing)
            n_padded_positions += missing * row_capacity
        stacked = torch.stack(chunk, dim=0)
        stacked_pad = torch.stack(chunk_pad, dim=0)
        x = stacked[:, :-1].contiguous()
        y = stacked[:, 1:].clone()
        y[stacked_pad[:, 1:]] = -1
        batches.append((x.to(device), y.to(device)))

    meta = {
        "n_source_docs": len(texts),
        "n_rows": len(rows),
        "n_batches": len(batches),
        "n_docs_packed": n_docs_packed,
        "n_cropped_fills": n_cropped,
        "n_padded_positions": n_padded_positions,
        "device_batch_size": device_batch,
        "sequence_len": seq_len,
        "packing": PACKING,
        "stride": STRIDE,
    }
    return batches, meta


@torch.no_grad()
def evaluate_bpb_components(model, batches, token_bytes) -> dict:
    total_nats = torch.tensor(0.0, dtype=torch.float32, device=model.get_device())
    total_bytes = torch.tensor(0, dtype=torch.int64, device=model.get_device())
    n_scored = torch.tensor(0, dtype=torch.int64, device=model.get_device())
    n_excluded = torch.tensor(0, dtype=torch.int64, device=model.get_device())
    for x, y in batches:
        loss2d = model(x, y, loss_reduction="none").view(-1)
        yf = y.view(-1)
        valid = yf >= 0
        y_safe = torch.where(valid, yf, torch.zeros_like(yf))
        num_bytes = torch.where(valid, token_bytes[y_safe], torch.zeros_like(yf, dtype=token_bytes.dtype))
        scored = num_bytes > 0
        total_nats += (loss2d * scored).sum()
        total_bytes += num_bytes.sum()
        n_scored += scored.sum()
        n_excluded += (~scored).sum()
    nats = float(total_nats.item())
    nbytes = int(total_bytes.item())
    bpb = float("inf") if nbytes == 0 else nats / (math.log(2) * nbytes)
    return {
        "bpb": bpb,
        "total_nats": nats,
        "total_bytes": nbytes,
        "n_scored_tokens": int(n_scored.item()),
        "n_excluded_positions": int(n_excluded.item()),
        "finite": math.isfinite(bpb),
    }


def byte_unigram_tagalog(train_texts: list[str], heldout_texts: list[str]) -> dict:
    counts = [0] * 256
    n_train = 0
    for text in train_texts:
        raw = text.encode("utf-8")
        n_train += len(raw)
        for b in raw:
            counts[b] += 1
    if n_train == 0:
        raise SystemExit("empty Tagalog train byte stream for unigram")
    nll = 0.0
    n_held = 0
    log_denom = math.log(n_train + 256)
    for text in heldout_texts:
        raw = text.encode("utf-8")
        n_held += len(raw)
        for b in raw:
            nll += -(math.log(counts[b] + 1) - log_denom)
    bpb = nll / (n_held * math.log(2)) if n_held else float("inf")
    return {
        "smoothing": "laplace_add_one",
        "vocab_bytes": 256,
        "train_bytes_N": n_train,
        "heldout_bytes_M": n_held,
        "nll_nats": nll,
        "bpb": bpb,
        "byte_counts_sha256": hashlib.sha256(json.dumps(counts).encode()).hexdigest(),
        "c": counts,
    }


def eval_model(model, batches, token_bytes, pack_meta: dict, label: str) -> dict:
    t0 = time.time()
    out = evaluate_bpb_components(model, batches, token_bytes)
    out.update(pack_meta)
    out["label"] = label
    out["wall_sec"] = time.time() - t0
    print(
        f"{label} bpb={out['bpb']:.6f} bytes={out['total_bytes']} tokens={out['n_scored_tokens']} {out['wall_sec']:.1f}s",
        flush=True,
    )
    return out


def load_gate_i_ckpt_sha(depth: int) -> str:
    path = RUN_CARD / f"gate-i-tl0-d{depth}.json"
    if not path.is_file():
        raise SystemExit(f"missing Gate I receipt: {path}")
    row = json.loads(path.read_text(encoding="utf-8"))
    if row.get("status") != "pass":
        raise SystemExit(f"Gate I d{depth} not pass")
    return row["checkpoint_sha256"]


def floor_pass(trained_bpb: float, floor_bpb: float, margin: float = P0_T_MARGIN) -> bool:
    return math.isfinite(trained_bpb) and math.isfinite(floor_bpb) and (floor_bpb - trained_bpb) >= margin


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["p0t"], required=True)
    parser.add_argument("--device-type", default="cuda")
    parser.add_argument("--device-batch-size", type=int, default=8)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    os.environ.setdefault("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / P4_RUN_ID))
    os.environ.setdefault("NANOCHAT_DATA_DIR", str(TL_DIR))

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tok_path = Path(os.environ["NANOCHAT_BASE_DIR"]) / "tokenizer" / "tokenizer.pkl"
    require_hash(tok_path, TOKENIZER_SHA, "tokenizer")

    val_shard = TL_DIR / "shard_00002.parquet"
    train0 = TL_DIR / "shard_00000.parquet"
    train1 = TL_DIR / "shard_00001.parquet"
    require_hash(val_shard, EXPECTED["p11_shards"]["shard_00002.parquet"], "val_shard")
    require_hash(train0, EXPECTED["p11_shards"]["shard_00000.parquet"], "train0")
    require_hash(train1, EXPECTED["p11_shards"]["shard_00001.parquet"], "train1")
    has_jsonl = TL_TRAIN_JSONL.is_file() and TL_VAL_JSONL.is_file()
    if has_jsonl:
        require_hash(TL_TRAIN_JSONL, EXPECTED["tl_train_jsonl"], "tl_train_jsonl")
        require_hash(TL_VAL_JSONL, EXPECTED["tl_val_jsonl"], "tl_val_jsonl")

    test_path = ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl"
    if test_path.exists():
        # test exists on disk but MUST NOT be read in this gate
        pass

    compute_init(args.device_type)
    device = torch.device(args.device_type)
    device_batch = args.device_batch_size

    print("computing Tagalog byte unigram (train UTF-8 -> val UTF-8)", flush=True)
    if has_jsonl:
        train_texts_uni = jsonl_texts(TL_TRAIN_JSONL)
        val_texts_uni = jsonl_texts(TL_VAL_JSONL)
        unigram_source = "jsonl_splits"
    else:
        train_texts_uni = parquet_texts(train0) + parquet_texts(train1)
        val_texts_uni = parquet_texts(val_shard)
        unigram_source = "parquet_shards"
    unigram = byte_unigram_tagalog(train_texts_uni, val_texts_uni)
    unigram_public = {k: v for k, v in unigram.items() if k != "c"}
    unigram_public["val_bpb_unigram"] = unigram["bpb"]
    unigram_public["source"] = unigram_source
    (out_dir / "byte_unigram_tagalog_val.json").write_text(
        json.dumps({**unigram_public, "c": unigram["c"]}, indent=2) + "\n"
    )
    print(f"unigram val_bpb={unigram['bpb']:.6f}", flush=True)

    first_tag = TL0_DEPTHS[8]
    model0, tokenizer, meta0 = load_model("base", device, phase="eval", model_tag=first_tag, step=TL0_STEP)
    token_bytes = get_token_bytes(device=device)
    assert meta0["model_config"]["sequence_len"] == T

    val_texts = parquet_texts(val_shard)
    print(f"packing val docs={len(val_texts)}", flush=True)
    val_batches, val_pack = pack_one_pass(val_texts, tokenizer, device_batch, T, device)
    del model0
    torch.cuda.empty_cache()

    results = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": ASPREDICTED_ID,
        "researchbox_id": RESEARCHBOX_ID,
        "gate": "P0-T",
        "phase": "p0t",
        "p3_run_id": P4_RUN_ID,
        "started_at_utc": utc_now(),
        "p0_t_margin_bpb": P0_T_MARGIN,
        "tokenizer_sha256": TOKENIZER_SHA,
        "val_shard_sha256": EXPECTED["p11_shards"]["shard_00002.parquet"],
        "tl_train_jsonl_sha256": EXPECTED["tl_train_jsonl"],
        "tl_val_jsonl_sha256": EXPECTED["tl_val_jsonl"],
        "packing": PACKING,
        "T": T,
        "B_device_batch": device_batch,
        "total_batch_B": B,
        "checkpoint_step": TL0_STEP,
        "untrained_seed": UNTRAINED_SEED,
        "byte_unigram_tagalog": unigram_public,
        "test_read_count": 0,
        "english_val_used": False,
        "depths": {},
    }

    all_pass = True
    for depth, tag in TL0_DEPTHS.items():
        expected_ckpt_sha = load_gate_i_ckpt_sha(depth)
        ckpt_path = Path(os.environ["NANOCHAT_BASE_DIR"]) / "base_checkpoints" / tag / f"model_{TL0_STEP:06d}.pt"
        if not ckpt_path.is_file():
            raise SystemExit(f"missing checkpoint {ckpt_path}")
        actual_ckpt_sha = sha256_file(ckpt_path)
        if actual_ckpt_sha != expected_ckpt_sha:
            raise SystemExit(f"checkpoint SHA mismatch d{depth}: {actual_ckpt_sha} != {expected_ckpt_sha}")

        print(f"\n=== {tag} trained step {TL0_STEP} ===", flush=True)
        model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=tag, step=TL0_STEP)
        assert meta["step"] == TL0_STEP
        assert meta["model_config"]["n_layer"] == depth
        token_bytes = get_token_bytes(device=device)
        trained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{tag}/trained_val")

        print(f"=== {tag} untrained seed={UNTRAINED_SEED} ===", flush=True)
        torch.manual_seed(UNTRAINED_SEED)
        if args.device_type == "cuda":
            torch.cuda.manual_seed(UNTRAINED_SEED)
        model.init_weights()
        model.eval()
        untrained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{tag}/untrained_val")

        gap_untrained = untrained_val["bpb"] - trained_val["bpb"]
        gap_unigram = unigram["bpb"] - trained_val["bpb"]
        pass_untrained = floor_pass(trained_val["bpb"], untrained_val["bpb"])
        pass_unigram = floor_pass(trained_val["bpb"], unigram["bpb"])
        pass_both = pass_untrained and pass_unigram
        if not pass_both:
            all_pass = False

        print(
            f"P0-T d{depth}: pass_untrained={pass_untrained} pass_unigram={pass_unigram} overall={pass_both}",
            flush=True,
        )

        row = {
            "depth": depth,
            "model_tag": tag,
            "checkpoint_path": str(ckpt_path.relative_to(ROOT)),
            "checkpoint_sha256": actual_ckpt_sha,
            "checkpoint_step": TL0_STEP,
            "val_bpb_full": trained_val["bpb"],
            "untrained_val_bpb": untrained_val["bpb"],
            "byte_unigram_val_bpb": unigram["bpb"],
            "gap_vs_untrained": gap_untrained,
            "gap_vs_unigram": gap_unigram,
            "pass_untrained_floor": pass_untrained,
            "pass_unigram_floor": pass_unigram,
            "pass_both_floors": pass_both,
            "trained_val": trained_val,
            "untrained_val": untrained_val,
        }
        results["depths"][str(depth)] = row
        (out_dir / f"{tag}_p0t_val.json").write_text(json.dumps(row, indent=2) + "\n")
        del model
        torch.cuda.empty_cache()

    results["p0_t_all_pass"] = all_pass
    results["automated_status"] = "PASS" if all_pass else "BLOCKED"
    results["ended_at_utc"] = utc_now()
    detail_path = out_dir / "gate-p0-t-eval-detail.json"
    detail_path.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nP0-T automated_status={results['automated_status']}", flush=True)
    print(f"detail={detail_path}", flush=True)
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
