#!/usr/bin/env python3
"""Gate J: confirmatory full-split BPB via official evaluate_bpb + BOS-bestfit.

One pass only (no shard wrap). Test phase is a separate invocation after D*.
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

RUN_ID = "p1-20260816T025911Z-0067a57"
EXPECTED = {
    "train_jsonl": "2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687",
    "val_jsonl": "4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c",
    "val_shard": "13409b3cb78dca87abf1cb1766cd68082b53b704951c38b5d618e97ba7bcfe02",
    "test_jsonl": "3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf",
    "tokenizer": "04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8",
}
DEPTHS = {
    8: "p1-fixed-d8-3x",
    12: "p1-fixed-d12-3x",
    16: "p1-fixed-d16-3x",
    20: "p1-fixed-d20-3x",
}
UNTRAINED_SEED = 0
PACKING = "bos_bestfit_buffer1000_one_pass_no_wrap"
STRIDE = "non_overlapping_T_official_bos_bestfit"


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


def byte_unigram(train_texts: list[str], heldout_texts: list[str]) -> dict:
    counts = [0] * 256
    n_train = 0
    for text in train_texts:
        raw = text.encode("utf-8")
        n_train += len(raw)
        for b in raw:
            counts[b] += 1
    if n_train == 0:
        raise SystemExit("empty train byte stream")
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
    print(f"{label} bpb={out['bpb']:.6f} nats={out['total_nats']:.4f} bytes={out['total_bytes']} tokens={out['n_scored_tokens']} {out['wall_sec']:.1f}s", flush=True)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["val_baselines", "val_one", "bootstrap_val", "test"], required=True)
    parser.add_argument("--device-type", default="cuda")
    parser.add_argument("--device-batch-size", type=int, default=8)
    parser.add_argument("--model-tag", default=None, help="Required for val_one / bootstrap_val / test")
    parser.add_argument("--step", type=int, default=None, help="Checkpoint step; default is last (294 for D_3x, 98 for D_1x)")
    parser.add_argument("--test-jsonl", default=None)
    parser.add_argument("--out-dir", default="/workspace/exports/gate_j")
    args = parser.parse_args()

    os.environ.setdefault("P1_ROOT", str(ROOT))
    os.environ.setdefault("RUN_ID", RUN_ID)
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / RUN_ID))
    os.environ.setdefault("NANOCHAT_DATA_DIR", str(ROOT / "data" / "processed" / "wikitext-tl39" / "active"))

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tok_path = Path(os.environ["NANOCHAT_BASE_DIR"]) / "tokenizer" / "tokenizer.pkl"
    require_hash(tok_path, EXPECTED["tokenizer"], "tokenizer")

    device_type = args.device_type
    compute_init(device_type)
    device = torch.device(device_type)
    B = args.device_batch_size
    T = 2048

    if args.phase == "val_baselines":
        active = Path(os.environ["NANOCHAT_DATA_DIR"])
        val_shard = active / "shard_00002.parquet"
        train0 = active / "shard_00000.parquet"
        train1 = active / "shard_00001.parquet"
        require_hash(val_shard, EXPECTED["val_shard"], "val_shard")
        train_jsonl = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "train.jsonl"
        val_jsonl = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl"
        require_hash(train_jsonl, EXPECTED["train_jsonl"], "train_jsonl")
        require_hash(val_jsonl, EXPECTED["val_jsonl"], "val_jsonl")
        if (ROOT / "data" / "processed" / "wikitext-tl39" / "test" / "test.jsonl").exists():
            raise SystemExit("test.jsonl is present under the standard test path; refuse val phase")

        print("computing byte unigram on val", flush=True)
        unigram = byte_unigram(jsonl_texts(train_jsonl), jsonl_texts(val_jsonl))
        unigram_public = {k: v for k, v in unigram.items() if k != "c"}
        unigram_public["val_bpb_unigram"] = unigram["bpb"]
        (out_dir / "byte_unigram_val.json").write_text(json.dumps({**unigram_public, "c": unigram["c"]}, indent=2) + "\n")
        print(f"unigram val_bpb={unigram['bpb']:.6f}", flush=True)

        # Load tokenizer via first model, pack once, reuse batches across depths.
        first_tag = DEPTHS[8]
        model0, tokenizer, meta0 = load_model("base", device, phase="eval", model_tag=first_tag, step=294)
        token_bytes = get_token_bytes(device=device)
        assert meta0["model_config"]["sequence_len"] == T
        val_texts = parquet_texts(val_shard)
        train_texts = parquet_texts(train0) + parquet_texts(train1)
        print(f"packing val docs={len(val_texts)}", flush=True)
        val_batches, val_pack = pack_one_pass(val_texts, tokenizer, B, T, device)
        print(f"packing train docs={len(train_texts)}", flush=True)
        train_batches, train_pack = pack_one_pass(train_texts, tokenizer, B, T, device)
        del model0
        torch.cuda.empty_cache()

        results = {
            "study_id": "NANOCHAT-FILIPINO-P1.1",
            "gate": "J",
            "phase": "val_baselines",
            "started_at_utc": utc_now(),
            "selection_rule": "exact_minimum_final_val_bpb_full",
            "evaluation_checkpoint_rule": "final_checkpoint_at_fixed_budget",
            "test_selection_source": "validation_only",
            "test_read_count": 0,
            "checkpoint_step": 294,
            "untrained_seed": UNTRAINED_SEED,
            "byte_unigram": unigram_public,
            "depths": {},
        }
        for depth, tag in DEPTHS.items():
            print(f"=== {tag} trained ===", flush=True)
            model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=tag, step=294)
            assert meta["step"] == 294
            assert meta["model_config"]["n_layer"] == depth
            token_bytes = get_token_bytes(device=device)
            trained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{tag}/trained_val")
            trained_train = eval_model(model, train_batches, token_bytes, train_pack, f"{tag}/trained_train")
            print(f"=== {tag} untrained seed={UNTRAINED_SEED} ===", flush=True)
            torch.manual_seed(UNTRAINED_SEED)
            if device_type == "cuda":
                torch.cuda.manual_seed(UNTRAINED_SEED)
            model.init_weights()
            model.eval()
            untrained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{tag}/untrained_val")
            gap = trained_train["bpb"] - trained_val["bpb"]
            beats_untrained = trained_val["bpb"] < untrained_val["bpb"]
            beats_unigram = trained_val["bpb"] < unigram["bpb"]
            row = {
                "depth": depth,
                "model_tag": tag,
                "checkpoint_step": 294,
                "val_bpb_full": trained_val["bpb"],
                "train_bpb_full": trained_train["bpb"],
                "train_val_gap_bpb": gap,
                "random_val_bpb": untrained_val["bpb"],
                "val_bpb_unigram": unigram["bpb"],
                "beats_untrained": beats_untrained,
                "beats_unigram": beats_unigram,
                "baseline_pass": beats_untrained and beats_unigram,
                "trained_val": trained_val,
                "trained_train": trained_train,
                "untrained_val": untrained_val,
                "card_eval_val_bpb_262144": meta.get("val_bpb"),
            }
            results["depths"][str(depth)] = row
            (out_dir / f"{tag}_val_baselines.json").write_text(json.dumps(row, indent=2) + "\n")
            del model
            torch.cuda.empty_cache()

        eligible = {
            d: r["val_bpb_full"]
            for d, r in results["depths"].items()
            if r["baseline_pass"] and r["trained_val"]["finite"]
        }
        if not eligible:
            results["D_star"] = None
            results["D_star_note"] = "no depth passed both baselines"
        else:
            d_star = min(eligible, key=lambda d: (eligible[d], int(d)))
            vals = {d: results["depths"][d]["val_bpb_full"] for d in results["depths"]}
            margin = None
            others = [v for d, v in vals.items() if d != d_star]
            if others:
                margin = abs(vals[d_star] - min(others))
            results["D_star"] = int(d_star)
            results["D_star_model_tag"] = DEPTHS[int(d_star)]
            results["D_star_val_bpb_full"] = vals[d_star]
            results["D_star_margin_to_next"] = margin
            results["practically_indistinguishable_0.01"] = margin is not None and margin < 0.01
            results["all_final_val_bpb_full"] = vals
        results["ended_at_utc"] = utc_now()
        (out_dir / "val_baselines_summary.json").write_text(json.dumps(results, indent=2) + "\n")
        print(json.dumps({k: results[k] for k in results if k != "depths"}, indent=2), flush=True)
        return 0

    if args.phase in {"val_one", "bootstrap_val"}:
        if not args.model_tag:
            raise SystemExit(f"{args.phase} requires --model-tag")
        active = Path(os.environ["NANOCHAT_DATA_DIR"])
        val_shard = active / "shard_00002.parquet"
        train0 = active / "shard_00000.parquet"
        train1 = active / "shard_00001.parquet"
        require_hash(val_shard, EXPECTED["val_shard"], "val_shard")
        model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=args.model_tag, step=args.step)
        token_bytes = get_token_bytes(device=device)
        if args.phase == "val_one":
            val_batches, val_pack = pack_one_pass(parquet_texts(val_shard), tokenizer, B, T, device)
            train_batches, train_pack = pack_one_pass(
                parquet_texts(train0) + parquet_texts(train1), tokenizer, B, T, device
            )
            trained_val = eval_model(model, val_batches, token_bytes, val_pack, f"{args.model_tag}/trained_val")
            trained_train = eval_model(model, train_batches, token_bytes, train_pack, f"{args.model_tag}/trained_train")
            unigram_path = out_dir / "byte_unigram_val.json"
            unigram_bpb = None
            if unigram_path.exists():
                unigram_bpb = json.loads(unigram_path.read_text())["bpb"]
            row = {
                "model_tag": args.model_tag,
                "checkpoint_step": int(meta["step"]),
                "val_bpb_full": trained_val["bpb"],
                "train_bpb_full": trained_train["bpb"],
                "train_val_gap_bpb": trained_train["bpb"] - trained_val["bpb"],
                "val_minus_train_gap_bpb": trained_val["bpb"] - trained_train["bpb"],
                "val_bpb_unigram": unigram_bpb,
                "beats_unigram": (trained_val["bpb"] < unigram_bpb) if unigram_bpb is not None else None,
                "trained_val": trained_val,
                "trained_train": trained_train,
                "evaluated_at_utc": utc_now(),
                "note": "Secondary or extra-seed val. Not used to reopen seed-0 D*. Test not read.",
            }
            (out_dir / f"{args.model_tag}_val_one.json").write_text(json.dumps(row, indent=2) + "\n")
            print(json.dumps({k: row[k] for k in row if k not in {"trained_val", "trained_train"}}, indent=2), flush=True)
            return 0

        # Per-document val NLL for the registered optional bootstrap.
        texts = parquet_texts(val_shard)
        bos = tokenizer.get_bos_token_id()
        per_doc = []
        batch_x = []
        batch_y = []
        batch_meta = []

        def flush():
            if not batch_x:
                return
            x = torch.stack(batch_x, dim=0).to(device)
            y = torch.stack(batch_y, dim=0).to(device)
            with torch.no_grad():
                loss2d = model(x, y, loss_reduction="none")
            for i, info in enumerate(batch_meta):
                row_loss = loss2d[i]
                row_y = y[i]
                valid = row_y >= 0
                y_safe = torch.where(valid, row_y, torch.zeros_like(row_y))
                nbytes = torch.where(valid, token_bytes[y_safe], torch.zeros_like(row_y, dtype=token_bytes.dtype))
                scored = nbytes > 0
                nats = float((row_loss * scored).sum().item())
                bcount = int(nbytes.sum().item())
                per_doc.append({
                    "doc_index": info["doc_index"],
                    "n_bytes": bcount,
                    "nll_nats": nats,
                    "n_chars": info["n_chars"],
                })
            batch_x.clear()
            batch_y.clear()
            batch_meta.clear()

        for di, text in enumerate(texts):
            ids = tokenizer.encode([text], prepend=bos)[0]
            # Non-overlapping T-blocks of the BOS-prefixed document; last short block ignore-padded.
            pos = 0
            while pos < len(ids) - 1:
                chunk = ids[pos : pos + (T + 1)]
                row = torch.zeros(T + 1, dtype=torch.long)
                pad = torch.zeros(T + 1, dtype=torch.bool)
                row[: len(chunk)] = torch.tensor(chunk, dtype=torch.long)
                if len(chunk) < T + 1:
                    pad[len(chunk) :] = True
                x = row[:-1]
                y = row[1:].clone()
                y[pad[1:]] = -1
                batch_x.append(x)
                batch_y.append(y)
                batch_meta.append({"doc_index": di, "n_chars": len(text)})
                if len(batch_x) == B:
                    flush()
                pos += T
        flush()
        # Merge chunks of the same document.
        merged: dict[int, dict] = {}
        for rec in per_doc:
            cur = merged.setdefault(rec["doc_index"], {"doc_index": rec["doc_index"], "n_bytes": 0, "nll_nats": 0.0, "n_chars": rec["n_chars"]})
            cur["n_bytes"] += rec["n_bytes"]
            cur["nll_nats"] += rec["nll_nats"]
        docs = [merged[i] for i in sorted(merged)]
        rng = torch.Generator()
        rng.manual_seed(0)
        n = len(docs)
        boot = []
        for _ in range(1000):
            idx = torch.randint(0, n, (n,), generator=rng).tolist()
            nats = sum(docs[i]["nll_nats"] for i in idx)
            bts = sum(docs[i]["n_bytes"] for i in idx)
            boot.append(nats / (math.log(2) * bts) if bts else float("inf"))
        boot_sorted = sorted(boot)
        point_nats = sum(d["nll_nats"] for d in docs)
        point_bytes = sum(d["n_bytes"] for d in docs)
        point = point_nats / (math.log(2) * point_bytes)
        payload = {
            "model_tag": args.model_tag,
            "checkpoint_step": int(meta["step"]),
            "n_docs": n,
            "val_bpb_document_sum": point,
            "bootstrap_n": 1000,
            "bootstrap_seed": 0,
            "bootstrap_mean": sum(boot) / len(boot),
            "bootstrap_ci95": [boot_sorted[24], boot_sorted[974]],
            "evaluated_at_utc": utc_now(),
            "note": "Document-level bootstrap on val only. Optional AsPredicted Q5. Not used to choose D*. Test not read.",
        }
        (out_dir / f"{args.model_tag}_bootstrap_val.json").write_text(json.dumps(payload, indent=2) + "\n")
        print(json.dumps(payload, indent=2), flush=True)
        return 0

    if not args.model_tag or not args.test_jsonl:
        raise SystemExit("test phase requires --model-tag and --test-jsonl")
    test_path = Path(args.test_jsonl)
    require_hash(test_path, EXPECTED["test_jsonl"], "test_jsonl")
    # Isolated eval dir: one parquet, used only as the val shard. Never the active train dir.
    isolated = out_dir / "test_isolated_data"
    isolated.mkdir(parents=True, exist_ok=True)
    for stale in isolated.glob("*.parquet"):
        stale.unlink()
    import pyarrow as pa

    texts = jsonl_texts(test_path)
    table = pa.Table.from_pydict({"text": texts})
    test_parquet = isolated / "shard_00000.parquet"
    pq.write_table(
        table,
        test_parquet,
        row_group_size=1024,
        use_dictionary=False,
        compression="zstd",
        compression_level=3,
        write_statistics=False,
    )
    os.environ["NANOCHAT_DATA_DIR"] = str(isolated)
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=args.model_tag, step=294)
    token_bytes = get_token_bytes(device=device)
    batches, pack = pack_one_pass(parquet_texts(test_parquet), tokenizer, B, T, device)
    test_out = eval_model(model, batches, token_bytes, pack, f"{args.model_tag}/test")
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "gate": "J",
        "phase": "test",
        "evaluated_at_utc": utc_now(),
        "model_tag": args.model_tag,
        "checkpoint_step": 294,
        "test_jsonl_sha256": EXPECTED["test_jsonl"],
        "test_parquet_sha256": sha256_file(test_parquet),
        "test_read_count": 1,
        "test_bpb": test_out["bpb"],
        "components": test_out,
        "note": "Single confirmatory test read after validation-only D* selection. Not used to choose D*.",
    }
    (out_dir / f"{args.model_tag}_test_bpb.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
