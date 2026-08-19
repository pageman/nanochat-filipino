# P2 public status (for website / project index)

Do not blend this table with P1.1 results. P1.1 remains a separate fixed-budget depth study.

| Field | Content |
|---|---|
| Study status | P2 empirical execution complete: Gates A–W recorded |
| Primary result | English-cost pattern **not observed**; Tagalog-gain pattern **observed**, one-seed scope |
| Test boundary | One A2-only secondary test event completed; A1/A3 were not tested |
| AsPredicted | https://aspredicted.org/xa56bs.pdf (#306935) |
| Code | https://github.com/pageman/nanochat-filipino |
| Hub | https://huggingface.co/pageman/nanochat-filipino-p2-en-then-tl (**documentation-only** until A0/A1/A2/A3 `.pt` upload together) |
| GitHub subtree | `results/p2/` (seals) · `docs/p2/` (study index) · `docs/hub/p2-en-then-tl/` (Hub documentation pack) |
| ResearchBox | https://researchbox.org/8763 (upload still a human step) |
| Paper | Current source `docs/papers/p2-cf-english/paper.tex`. Do not ship the obsolete 16 August PDF. |
| Data safety | No raw protected holdout files or credentials on this page |
| Follow-on | P3 is a **post-P2** follow-up unless an earlier independent freeze exists (none on file). P4 is a future multi-seed/robustness design. P1.1 close-out is separate. |

## Technical summary

P2 is a preregistered one-seed continual-pretraining experiment that compared frozen Tagalog continuation (A2) against a matched extra-English continuation control (A1), both initialized from the same immutable English d20 parent under equal phase-2 model-visible-token budgets. On sealed validation, the registered English-retention-cost prediction was not observed: \(C_{EN}=EN(A2)-EN(A1)=-0.073991\). The registered Tagalog-adaptation-gain pattern was observed: \(G_{TL}=TL(A2)-TL(A1)=-3.883048\). A3, a pre-frozen 50/50-document mix, is reported as a trade-off arm rather than mitigation. A2 alone received the one registered secondary English and legacy-Tagalog test evaluation.

## Lay summary

The study trained a small English-language model and then compared three equally sized follow-up lessons: more English, Tagalog, or a fixed English–Tagalog mix. In this specific controlled setup, learning Tagalog greatly improved the model’s ability to predict held-out Tagalog text. It did **not** produce the predicted loss on held-out English text when compared with giving the model more English practice. This is one carefully controlled model experiment, not proof that all language models or all languages behave this way.
