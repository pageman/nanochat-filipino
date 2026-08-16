#!/usr/bin/env python3
"""Protocol §16.6 gzip -9 bits/byte on val text. Not a confirmatory DV."""

from __future__ import annotations

import gzip
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAL = ROOT / "data" / "interim" / "wikitext-tl39" / "splits" / "val.jsonl"
EXPECTED = "4d51644b84d05050bfc8c515079e60f6e437082b6cce2122e9ed00e7b1db2b1c"


def main() -> int:
    raw = VAL.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED:
        raise SystemExit(f"val hash mismatch: {actual}")
    texts = [json.loads(line)["text"] for line in raw.decode("utf-8").splitlines() if line]
    blob = "".join(texts).encode("utf-8")
    compressed = gzip.compress(blob, compresslevel=9)
    bpb = (len(compressed) * 8) / len(blob)
    out = {
        "study_id": "NANOCHAT-FILIPINO-P1.1",
        "kind": "gzip_minus9_val_not_confirmatory",
        "val_jsonl_sha256": actual,
        "uncompressed_bytes": len(blob),
        "gzip9_bytes": len(compressed),
        "gzip9_bits_per_byte": bpb,
        "nll_equivalent_note": "compressor bits/byte, not a causal LM",
        "evaluated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ln2": math.log(2),
    }
    dest = ROOT / "artifacts" / "p1" / "p1-20260816T025911Z-0067a57" / "gate-j" / "gzip9_val.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
