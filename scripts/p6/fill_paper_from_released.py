#!/usr/bin/env python3
"""Insert Gate X released scalars into paper.tex. Reads released JSON only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REL = ROOT / "data/cache/p6-20260824T155226Z-769f807a/released/p6-s4-released-contrasts.json"
EVENT = ROOT / "docs/run-cards/p6/p6-20260824T155226Z-769f807a/P6_UNBLINDING_EVENT.json"
OUT = ROOT / "docs/papers/p6-m-schedule-topology/paper.tex"


def f(x: float) -> str:
    return f"{x:.6f}"


def main() -> int:
    row = json.loads(REL.read_text())
    event = json.loads(EVENT.read_text())
    c = row["cells_val_bpb_full"]
    d = row["delta_vs_m_fine"]
    ctx = row["contextual"]
    test = {e["component"]: e["bpb"] for e in row["secondary_m_fine_test"]["events"]}
    at = event["at_utc"]

    tex = rf"""% P6-M paper — values inserted from released Gate X JSON only
% Source: {REL.relative_to(ROOT)}
% Event: {EVENT.relative_to(ROOT)} at {at}
\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{booktabs}}
\usepackage{{hyperref}}
\title{{P6-M: Schedule Topology under a Frozen English--Tagalog Token-Share Bundle}}
\author{{Anonymous for review}}
\date{{}}
\begin{{document}}
\maketitle

\begin{{abstract}}
P6-M is a one-seed (seed 4) schedule-topology mechanism study. Holding P4
source-content token quotas fixed, four mixed schedules from one frozen Tagalog
parent are compared on bilingual validation bits-per-byte. Primary contrasts are
$\Delta$TL and $\Delta$EN versus M-fine at $\delta=0.01$. One seed does not
support population inference. WikiText-TL-39 is a Cruz--Cheng resource lineage;
this study is not an extension of Cheng catastrophic-forgetting methods and does
not assess downstream Filipino tasks.
\end{{abstract}}

\section{{Study identity}}
P6-M does not amend P1.1--P5 (AsPredicted \#307969). Confirmatory depth is d20.
Phase-two budget is $294\times 65{,}536=19{,}267{,}584$ tokens. Mixed-arm quotas
are $9{,}633{,}792$ Tagalog and $9{,}633{,}792$ English tokens. Policy A:
one M-fine restricted-test event after validation sealing; test values are
secondary and excluded from topology classification.

\section{{Methods (filed)}}
Six sibling continuations from frozen C0: C1 extra Tagalog, C2 pure English,
M-fine, M-coarse, M-blocked, M-rand. Optimizer state is reset at each child.
Evaluator packing is the frozen official BPB contract. Unblinding was a single
Gate X event.

\section{{Primary validation results}}
Values are full-split validation BPB from the sealed 12-cell matrix, released at
Gate X. Lower is better.

\begin{{tabular}}{{lcc}}
\toprule
Arm & TL BPB & EN BPB \\
\midrule
C1 & {f(c['c1_tl'])} & {f(c['c1_en'])} \\
C2 & {f(c['c2_tl'])} & {f(c['c2_en'])} \\
M-fine & {f(c['m-fine_tl'])} & {f(c['m-fine_en'])} \\
M-coarse & {f(c['m-coarse_tl'])} & {f(c['m-coarse_en'])} \\
M-blocked & {f(c['m-blocked_tl'])} & {f(c['m-blocked_en'])} \\
M-rand & {f(c['m-rand_tl'])} & {f(c['m-rand_en'])} \\
\bottomrule
\end{{tabular}}

C0 English descriptive BPB (excluded from topology classification): {f(c['c0_en'])}.

\subsection{{Primary contrasts versus M-fine}}
$\Delta = \mathrm{{BPB}}(M\text{{-}}\tau)-\mathrm{{BPB}}(\mathrm{{M\text{{-}}fine}})$.
Class uses $\delta=0.01$.

\begin{{tabular}}{{lcccc}}
\toprule
$\tau$ & $\Delta$TL & TL class & $\Delta$EN & EN class \\
\midrule
M-coarse & {f(d['m-coarse']['Delta_TL'])} & {d['m-coarse']['Delta_TL_class'].replace('_',' ')} & {f(d['m-coarse']['Delta_EN'])} & {d['m-coarse']['Delta_EN_class'].replace('_',' ')} \\
M-blocked & {f(d['m-blocked']['Delta_TL'])} & {d['m-blocked']['Delta_TL_class'].replace('_',' ')} & {f(d['m-blocked']['Delta_EN'])} & {d['m-blocked']['Delta_EN_class'].replace('_',' ')} \\
M-rand & {f(d['m-rand']['Delta_TL'])} & {d['m-rand']['Delta_TL_class'].replace('_',' ')} & {f(d['m-rand']['Delta_EN'])} & {d['m-rand']['Delta_EN_class'].replace('_',' ')} \\
\bottomrule
\end{{tabular}}

M-rand is within $\delta$ of M-fine on both languages. M-blocked is worse than
M-fine by more than $\delta$ on both languages. M-coarse is better than M-fine
on Tagalog and worse on English, each by more than $\delta$.

\subsection{{Contextual contrasts}}
$R_{{\mathrm{{TL}}}}=\mathrm{{TL}}(M\text{{-}}\tau)-\mathrm{{TL}}(\mathrm{{C2}})$;
$A_{{\mathrm{{EN}}}}=\mathrm{{EN}}(M\text{{-}}\tau)-\mathrm{{EN}}(\mathrm{{C1}})$.

\begin{{tabular}}{{lcc}}
\toprule
$\tau$ & $R_{{\mathrm{{TL}}}}$ & $A_{{\mathrm{{EN}}}}$ \\
\midrule
M-fine & {f(ctx['m-fine']['R_TL'])} & {f(ctx['m-fine']['A_EN'])} \\
M-coarse & {f(ctx['m-coarse']['R_TL'])} & {f(ctx['m-coarse']['A_EN'])} \\
M-blocked & {f(ctx['m-blocked']['R_TL'])} & {f(ctx['m-blocked']['A_EN'])} \\
M-rand & {f(ctx['m-rand']['R_TL'])} & {f(ctx['m-rand']['A_EN'])} \\
\bottomrule
\end{{tabular}}

\section{{Secondary restricted test (Policy A)}}
One M-fine test event (excluded from topology classification): English
{f(test['english'])}; Tagalog {f(test['tagalog'])}.

\section{{Limitations}}
One seed; no mean, CI, or $p$-value. P6-M does not claim Cheng catastrophic-forgetting
extension, Cruz--Cheng 2020 validation, all-Philippine-language coverage, or
downstream-task transfer. Gate X executed a topology-contrast script because the
Gate 0 pinned unblind hash was a P5-rename recurrence counter that cannot read the
filed 12-cell lockbox; the filed analysis is the authority.

\section{{Infrastructure}}
Lockout-resistant Tier-2 resume kits were required after GPU gates. M-rand model
weights were technically accepted after an optimizer-write ENOSPC; the model
checkpoint was terminal and not retrained.

\end{{document}}
"""
    OUT.write_text(tex, encoding="utf-8")
    print(str(OUT.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
