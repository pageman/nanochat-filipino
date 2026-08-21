#!/usr/bin/env python3
"""Pre-frozen P4 table/paper check. Reads Gate X released seals only. Adds no metrics."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_common import BASE, ROOT, RUN_CARD, sha256_file, utc_now, write_json  # noqa: E402

RELEASED = BASE / "released"
PAPER = ROOT / "docs" / "papers" / "p4-token-share-mix" / "paper.tex"
OUT = ROOT / "results" / "p4" / "tables.json"
DELTA = 0.01


def cell(name: str) -> float:
    return float(json.loads((RELEASED / f"{name}_val_bpb_full.json").read_text())["val_bpb_full"])


def fmt6(x: float) -> str:
    return f"{x:.6f}"


def main() -> int:
    seal = json.loads((RELEASED / "p4-validation-seal.json").read_text(encoding="utf-8"))
    cells = {
        "c1_en": cell("c1_en"),
        "c1_tl": cell("c1_tl"),
        "c2_en": cell("c2_en"),
        "c2_tl": cell("c2_tl"),
        "c3_en": cell("c3_en"),
        "c3_tl": cell("c3_tl"),
        "c0_en": cell("c0_en"),
    }
    r_tl = cells["c3_tl"] - cells["c2_tl"]
    a_en = cells["c3_en"] - cells["c1_en"]
    if abs(r_tl - float(seal["R_TL"])) > 1e-9 or abs(a_en - float(seal["A_EN"])) > 1e-9:
        print("recomputed contrasts disagree with seal", file=sys.stderr)
        return 2
    both = r_tl <= -DELTA and a_en <= -DELTA
    only_r = r_tl <= -DELTA and not (a_en <= -DELTA)
    only_a = a_en <= -DELTA and not (r_tl <= -DELTA)
    neither = not (r_tl <= -DELTA) and not (a_en <= -DELTA)
    if both:
        grammar = "both"
        sentence = (
            "Under this preregistered token-share-locked mixture, P4 observed lower Tagalog BPB "
            "than pure English continuation and lower English BPB than extra Tagalog continuation "
            "in the stated apparatus."
        )
        mitigation = (
            "A measured reduction in the P3-style relative Tagalog retention cost within this "
            "frozen P4 apparatus, not a general mitigation of catastrophic forgetting."
        )
    elif only_r:
        grammar = "only_R"
        sentence = (
            "The specified mixture improved Tagalog retention relative to pure English continuation "
            "but did not meet the preregistered English-acquisition criterion."
        )
        mitigation = None
    elif only_a:
        grammar = "only_A"
        sentence = (
            "The specified mixture improved English acquisition relative to extra Tagalog continuation "
            "but did not meet the preregistered Tagalog-retention criterion."
        )
        mitigation = None
    else:
        grammar = "neither"
        sentence = "The specified mixture did not meet either preregistered trade-off criterion."
        mitigation = None

    six = {k: fmt6(v) for k, v in cells.items()}
    six["R_TL"] = fmt6(r_tl)
    six["A_EN"] = fmt6(a_en)
    tex = PAPER.read_text(encoding="utf-8") if PAPER.is_file() else ""
    missing = [s for s in six.values() if s not in tex]
    if missing:
        print("paper.tex missing sealed decimals:", missing, file=sys.stderr)
        return 3
    compact_l = " ".join(tex.split()).lower()
    if "independently confirmed p3" in compact_l:
        print("paper.tex forbidden phrase: independently confirmed P3", file=sys.stderr)
        return 4
    if "confirms p3" in compact_l and "does not independently confirm p3" not in compact_l:
        print("paper.tex forbidden phrase: confirms P3", file=sys.stderr)
        return 4
    if "p3 b3 fixed" in compact_l and "not" not in compact_l.split("p3 b3 fixed")[0][-40:]:
        print("paper.tex forbidden affirmative: P3 B3 fixed", file=sys.stderr)
        return 4
    if mitigation and mitigation not in tex.replace("\n", " "):
        # allow line wraps in TeX
        compact = " ".join(tex.split())
        if mitigation not in compact:
            print("both-criteria paper must include the narrow mitigation sentence", file=sys.stderr)
            return 5
    if (not both) and "mitigation" in PAPER.name:
        pass
    title_has_mit = "mitigation" in tex.split("\\begin{abstract}")[0].lower()
    if title_has_mit and not both:
        print("mitigation in title without both criteria", file=sys.stderr)
        return 6

    payload = {
        "study_id": "NANOCHAT-FILIPINO-P4-C3-TOKEN-SHARE",
        "aspredicted_id": 307591,
        "at_utc": utc_now(),
        "source": "released seals only",
        "no_new_metrics": True,
        "cells_6dp": six,
        "delta": DELTA,
        "grammar": grammar,
        "both_criteria_met": both,
        "neither": neither,
        "sentence": sentence,
        "narrow_mitigation_sentence": mitigation,
        "c3_is_not_p3_b3": True,
        "one_seed": True,
        "paper_decimals_match_seal": True,
        "seal_sha256": sha256_file(RELEASED / "p4-validation-seal.json"),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_json(OUT, payload)
    write_json(RUN_CARD / "gate-x-tables.json", payload)
    print(json.dumps({"grammar": grammar, "both": both, "path": str(OUT.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
