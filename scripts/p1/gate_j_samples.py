#!/usr/bin/env python3
"""Protocol §16.7 qualitative samples. Not a confirmatory metric. No test read."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "nanochat"
sys.path.insert(0, str(VENDOR))

from nanochat.checkpoint_manager import load_model  # noqa: E402
from nanochat.common import compute_init  # noqa: E402

PROMPTS = [
    "Ang Pilipinas ay",
    "Noong ika-",
    "= Kasaysayan =",
]


@torch.no_grad()
def nucleus_generate(model, tokenizer, prompt: str, *, max_tokens: int, temperature: float, top_p: float, seed: int) -> str:
    device = model.get_device()
    bos = tokenizer.get_bos_token_id()
    ids = tokenizer.encode([prompt], prepend=bos)[0]
    x = torch.tensor([ids], dtype=torch.long, device=device)
    rng = torch.Generator(device=device)
    rng.manual_seed(seed)
    for _ in range(max_tokens):
        logits = model.forward(x)[:, -1, :] / temperature
        probs = F.softmax(logits, dim=-1)
        sorted_probs, sorted_idx = torch.sort(probs, descending=True)
        cdf = torch.cumsum(sorted_probs, dim=-1)
        mask = cdf - sorted_probs > top_p
        sorted_probs = sorted_probs.masked_fill(mask, 0.0)
        sorted_probs = sorted_probs / sorted_probs.sum(dim=-1, keepdim=True)
        pick = torch.multinomial(sorted_probs, 1, generator=rng)
        nxt = sorted_idx.gather(-1, pick)
        x = torch.cat([x, nxt], dim=1)
        if int(nxt.item()) == bos:
            break
    return tokenizer.decode(x[0].tolist())


def main() -> int:
    os.environ.setdefault("NANOCHAT_BASE_DIR", str(ROOT / "data" / "cache" / "p1-20260816T025911Z-0067a57"))
    os.environ.setdefault("NANOCHAT_DATA_DIR", str(ROOT / "data" / "processed" / "wikitext-tl39" / "active"))
    out = Path(os.environ.get("P1_SAMPLE_OUT", "/workspace/exports/gate_j/samples_d20.json"))
    compute_init("cuda")
    device = torch.device("cuda")
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag="p1-fixed-d20-3x", step=294)
    rows = []
    for prompt in PROMPTS:
        for seed in (0, 1):
            for k in range(5):
                text = nucleus_generate(
                    model,
                    tokenizer,
                    prompt,
                    max_tokens=100,
                    temperature=0.8,
                    top_p=0.95,
                    seed=seed * 1000 + k,
                )
                rows.append({"prompt": prompt, "decoding_seed": seed, "continuation_index": k, "text": text})
                print(f"--- {prompt!r} seed={seed} k={k} ---\n{text}\n", flush=True)
    payload = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "kind": "qualitative_samples_not_a_metric",
        "model_tag": "p1-fixed-d20-3x",
        "checkpoint_step": 294,
        "temperature": 0.8,
        "top_p": 0.95,
        "max_tokens": 100,
        "native_speaker_ratings": None,
        "native_speaker_note": "No rater available at write time. Do not invent scores.",
        "evaluated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "samples": rows,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
