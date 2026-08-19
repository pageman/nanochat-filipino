#!/usr/bin/env python3
"""Gate P0-E: confirmatory full-split English BPB via official evaluate_bpb + BOS-bestfit.

Frozen copy of scripts/p1/gate_j_full_bpb.py adapted for P2.
One pass only (no shard wrap). No test set read in this gate.
Packing: BOS-bestfit, T=2048, one epoch, non-overlapping T-blocks for bootstrap.

Usage (on pod, after sourcing env.cuda.sh):
  python scripts/p2/evaluate_bpb.py --phase val_baselines
  python scripts/p2/evaluate_bpb.py --phase val_one --model-tag p2-en0-d20 --step 5415
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

RUN_ID = "p2-20260817T150944Z-de99f8a"
EXPECTED = {
    "tokenizer": "946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6",
    "val_parquet": "b20942ae71823fa52ec0f8d019a76960059798958716184d923f646f64cc648f",
    "train_00000_parquet": "9bdee964368da85a9b97af0d8cd50c4cd13ec392a8045dbec602ce31bd587861",
    "train_00001_parquet": "7331e6219eec3bf619b92c38f686778395b77b500d267cfb25412abb41c6379c",
    "train_00002_parquet": "59bc144b0191d10009baa7698bbb96ba25c2c750b7ab8cdbc9bba52998c4d9f7",
    "train_00003_parquet": "ac693bfc6c1820e9f978f90958b1afb4bf82d91c9bcbba682467d6a357ebcb0b",
    "train_jsonl": "09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a",
    "val_jsonl": "874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b",
    "tl_val_shard": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
}
EN0_DEPTHS = {
    8: "p2-en0-d8",
    20: "p2-en0-d20",
}
EN0_STEP = 5415
UNTRAINED_SEED = 0
PACKING = "bos_bestfit_buffer1000_one_pass_no_wrap"
STRIDE = "non_overlapping_T_official_bos_bestfit"
P0_E_MARGIN = 0.01  # EN0 must beat untrained by at least this much


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


def pack_one_pass(texts: list[str], tokenizer, B: int, T: int, device: torch.device):
    """Official BOS-bestfit packing, first epoch only. Last incomplete row is ignore-padded."""
    bos = tokenizer.get_bos_token_id()
    row_capacity = T + 1
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
    for start in range(0, len(rows), B):
        chunk = rows[start : start + B]
        chunk_pad = row_pads[start : start + B]
        missing = B - len(chunk)
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
        "device_batch_size": B,
        "sequence_len": T,
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


def byte_unigram_english(train_texts: list[str], heldout_texts: list[str]) -> dict:
    """Fit byte unigram on English train UTF-8 (not P1.1 Tagalog 4.453225)."""
    counts = [0] * 256
    n_train = 0
    for text in train_texts:
        raw = text.encode("utf-8")
        n_train += len(raw)
        for b in raw:
            counts[b] += 1
    if n_train == 0:
        raise SystemExit("empty English train byte stream")
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
        "corpus": "wikitext-103-english",
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
    print(f"{label} bpb={out['bpb']:.6f} nats={out['total_nats']:.4f} bytes={out['total_bytes']} tokens={out['n_scored_tokens']} {out['wall_sec']:.1f}s", flush=True)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["val_baselines", "val_one"], required=True)
    parser.add_argument("--device-type", default="cuda")
    parser.add_argument("--device-batch-size", type=int, default=8)
    parser.add_argument("--model-tag", default=None, help="Required for val_one")
    parser.add_argument("--step", type=int, default=EN0_STEP, help=f"Checkpoint step (default {EN0_STEP})")
    parser.add_argument("--language", choices=["english", "tagalog"], default="english",
                        help="Validation corpus for val_one (English WT103 or P1.1 TL val shard)")
    parser.add_argument("--out-dir", default="/workspace/exports/gate_p0")
    args = parser.parse_args()

    os.environ.setdefault("P2_ROOT", str(ROOT))
    os.environ.setdefault("RUN_ID", RUN_ID)
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / RUN_ID))
    en_active = Path(os.environ.get("NANOCHAT_DATA_DIR_EN",
                     str(ROOT / "data" / "processed" / "wikitext-103" / "en-active")))
    tl_readonly = Path(os.environ.get("NANOCHAT_DATA_DIR_TL",
                      str(ROOT / "data" / "processed" / "p2-tl39-readonly")))
    os.environ["NANOCHAT_DATA_DIR"] = str(en_active)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tok_path = Path(os.environ["NANOCHAT_BASE_DIR"]) / "tokenizer" / "tokenizer.pkl"
    require_hash(tok_path, EXPECTED["tokenizer"], "tokenizer")

    val_parquet = en_active / "val.parquet"
    require_hash(val_parquet, EXPECTED["val_parquet"], "val_parquet")

    train_jsonl = ROOT / "data" / "interim" / "wikitext-103" / "english_train.jsonl"
    val_jsonl = ROOT / "data" / "interim" / "wikitext-103" / "english_val.jsonl"
    has_jsonl = train_jsonl.exists() and val_jsonl.exists()
    if has_jsonl:
        require_hash(train_jsonl, EXPECTED["train_jsonl"], "train_jsonl")
        require_hash(val_jsonl, EXPECTED["val_jsonl"], "val_jsonl")

    train_parquets = [
        en_active / "train_00000.parquet",
        en_active / "train_00001.parquet",
        en_active / "train_00002.parquet",
        en_active / "train_00003.parquet",
    ]
    for p, key in [
        (train_parquets[0], "train_00000_parquet"),
        (train_parquets[1], "train_00001_parquet"),
        (train_parquets[2], "train_00002_parquet"),
        (train_parquets[3], "train_00003_parquet"),
    ]:
        require_hash(p, EXPECTED[key], key)

    # Guard: refuse if English test.jsonl is somehow loaded
    test_jsonl = ROOT / "data" / "interim" / "wikitext-103" / "english_test.jsonl"
    if (out_dir / "test_read_count_nonzero").exists():
        raise SystemExit("test read sentinel present; refusing to run")

    compute_init(args.device_type)
    device = torch.device(args.device_type)
    B = args.device_batch_size
    T = 2048

    if args.phase == "val_baselines":
        print("computing English byte unigram on train UTF-8", flush=True)
        if has_jsonl:
            train_texts_for_unigram = jsonl_texts(train_jsonl)
            val_texts_for_unigram = jsonl_texts(val_jsonl)
            unigram_source = "jsonl_splits"
        else:
            # Pod images may not include interim JSONL; fall back to hashed parquet shards.
            train_texts_for_unigram = []
            for tp in train_parquets:
                train_texts_for_unigram.extend(parquet_texts(tp))
            val_texts_for_unigram = parquet_texts(val_parquet)
            unigram_source = "parquet_shards"
        unigram = byte_unigram_english(train_texts_for_unigram, val_texts_for_unigram)
        unigram_public = {k: v for k, v in unigram.items() if k != "c"}
        unigram_public["val_bpb_unigram"] = unigram["bpb"]
        unigram_public["source"] = unigram_source
        (out_dir / "byte_unigram_english_val.json").write_text(
            json.dumps({**unigram_public, "c": unigram["c"]}, indent=2) + "\n"
        )
        print(f"English unigram val_bpb={unigram['bpb']:.6f}", flush=True)

        # Load tokenizer via d8 model, pack once, reuse across depths.
        first_tag = EN0_DEPTHS[8]
        model0, tokenizer, meta0 = load_model("base", device, phase="eval", model_tag=first_tag, step=EN0_STEP)
        token_bytes = get_token_bytes(device=device)
        assert meta0["model_config"]["sequence_len"] == T, f"T mismatch: {meta0['model_config']['sequence_len']} vs {T}"

        val_texts = parquet_texts(val_parquet)
        print(f"packing val docs={len(val_texts)}", flush=True)
        val_batches, val_pack = pack_one_pass(val_texts, tokenizer, B, T, device)
        del model0
        torch.cuda.empty_cache()

        results = {
            "study_id": "NANOCHAT-FILIPINO-P2-EN-TL",
            "aspredicted_id": 306935,
            "gate": "P0",
            "phase": "val_baselines",
            "started_at_utc": utc_now(),
            "run_id": RUN_ID,
            "en0_step": EN0_STEP,
            "p0_e_margin_required": P0_E_MARGIN,
            "tokenizer_sha256": EXPECTED["tokenizer"],
            "val_parquet_sha256": EXPECTED["val_parquet"],
            "packing": PACKING,
            "T": T,
            "B": B,
            "untrained_seed": UNTRAINED_SEED,
            "byte_unigram_english": unigram_public,
            "inloop_val_is_not_val_bpb_full": True,
            "started_tagalog": False,
            "test_read_count": 0,
            "depths": {},
        }

        all_pass = True
        for depth, tag in EN0_DEPTHS.items():
            print(f"\n=== {tag} trained (step {EN0_STEP}) ===", flush=True)
            model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=tag, step=EN0_STEP)
            assert meta["step"] == EN0_STEP, f"step mismatch: {meta['step']} vs {EN0_STEP}"
            assert meta["model_config"]["n_layer"] == depth, f"depth mismatch: {meta['model_config']['n_layer']} vs {depth}"
            token_bytes = get_token_bytes(device=device)

            trained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{tag}/trained_val")

            print(f"=== {tag} untrained seed={UNTRAINED_SEED} ===", flush=True)
            torch.manual_seed(UNTRAINED_SEED)
            if args.device_type == "cuda":
                torch.cuda.manual_seed(UNTRAINED_SEED)
            model.init_weights()
            model.eval()
            untrained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{tag}/untrained_val")

            gap = untrained_val["bpb"] - trained_val["bpb"]
            p0_e_pass = trained_val["bpb"] < untrained_val["bpb"] and gap >= P0_E_MARGIN
            beats_unigram = trained_val["bpb"] < unigram["bpb"]
            if not p0_e_pass:
                all_pass = False

            print(f"\nP0-E {tag}: trained={trained_val['bpb']:.6f} untrained={untrained_val['bpb']:.6f} gap={gap:.6f} pass={'YES' if p0_e_pass else 'NO (FAIL)'}", flush=True)

            row = {
                "depth": depth,
                "model_tag": tag,
                "checkpoint_step": EN0_STEP,
                "val_bpb_full": trained_val["bpb"],
                "untrained_val_bpb": untrained_val["bpb"],
                "p0_e_gap": gap,
                "p0_e_pass": p0_e_pass,
                "beats_unigram": beats_unigram,
                "val_bpb_unigram_english": unigram["bpb"],
                "trained_val": trained_val,
                "untrained_val": untrained_val,
            }
            results["depths"][str(depth)] = row
            (out_dir / f"{tag}_p0e_val.json").write_text(json.dumps(row, indent=2) + "\n")
            del model
            torch.cuda.empty_cache()

        results["p0_e_all_pass"] = all_pass
        results["ended_at_utc"] = utc_now()
        summary_path = out_dir / "gate_p0_val_baselines.json"
        summary_path.write_text(json.dumps(results, indent=2) + "\n")
        print("\n" + "="*60, flush=True)
        print(f"P0-E result: {'ALL PASS' if all_pass else 'FAIL — do not start Tagalog'}", flush=True)
        for d, r in results["depths"].items():
            print(f"  d{d}: val_bpb_full={r['val_bpb_full']:.6f}  untrained={r['untrained_val_bpb']:.6f}  gap={r['p0_e_gap']:.6f}  pass={r['p0_e_pass']}", flush=True)
        print(f"  byte_unigram_english={unigram['bpb']:.6f}", flush=True)
        print(f"Summary: {summary_path}", flush=True)
        if not all_pass:
            return 1
        return 0

    if args.phase == "val_one":
        if not args.model_tag:
            raise SystemExit("val_one requires --model-tag")
        if args.language == "english":
            eval_parquet = val_parquet
            eval_label = "english"
            unigram_path = out_dir / "byte_unigram_english_val.json"
        else:
            eval_parquet = tl_readonly / "shard_00002.parquet"
            require_hash(eval_parquet, EXPECTED["tl_val_shard"], "tl_val_shard")
            eval_label = "tagalog"
            unigram_path = out_dir / "byte_unigram_english_val.json"
        model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=args.model_tag, step=args.step)
        token_bytes = get_token_bytes(device=device)
        val_texts = parquet_texts(eval_parquet)
        val_batches, val_pack = pack_one_pass(val_texts, tokenizer, B, T, device)
        trained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{args.model_tag}/{eval_label}_val")
        unigram_bpb = None
        if unigram_path.exists() and args.language == "english":
            unigram_bpb = json.loads(unigram_path.read_text())["bpb"]
        row = {
            "gate": "Q",
            "arm": "A0",
            "language": args.language,
            "model_tag": args.model_tag,
            "checkpoint_step": int(meta["step"]),
            "val_bpb_full": trained_val["bpb"],
            "val_bpb_unigram_english": unigram_bpb,
            "beats_unigram": (trained_val["bpb"] < unigram_bpb) if unigram_bpb is not None else None,
            "val_parquet": str(eval_parquet.relative_to(ROOT)),
            "val_parquet_sha256": sha256_file(eval_parquet),
            "trained_val": trained_val,
            "evaluated_at_utc": utc_now(),
            "test_read_count": 0,
            "started_tagalog_continuation": False,
        }
        suffix = "a0_tagalog_val" if args.language == "tagalog" else "val_one"
        out_path = out_dir / f"{args.model_tag}_{suffix}.json"
        out_path.write_text(json.dumps(row, indent=2) + "\n")
        print(json.dumps({k: row[k] for k in row if k != "trained_val"}, indent=2), flush=True)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
