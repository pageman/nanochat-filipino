# P3 pre-outcome audit (Gate 0)

Filed AsPredicted [#307342](https://aspredicted.org/wd2pc8.pdf). Protocol SHA256 `899ba83f0b36f2b4bf4c16b3c675e58788d7763cb439f8a8c3a3c061bda2b986` (do not edit that file without a dated deviation).

| ID | Status |
|---|---|
| F-01 | LOCKED in PDF: P1.1 reconstructed_article_70_15_15 documents; new P3 Tagalog 32768 BPE |
| F-02 | LOCKED: WT103-raw document manifests; re-download at Gate B |
| F-03 | LOCKED: train-only Tagalog 32768 |
| F-04 | LOCKED: 3x T_tl_train; B=65536; T=2048 |
| F-05 | LOCKED: P0-T both depths, 0.01, fail → no children |
| F-06 | LOCKED: B0 = d20 |
| F-07 | LOCKED: B1 extra TL; B2 EN train; B3 mix; tests not in train |
| F-08 | LOCKED: 50/50-document mix seed 42 |
| F-09 | LOCKED: D_phase2=19267584; fresh Muon+AdamW load_optimizer=False |
| F-10 | LOCKED: full official evaluate_bpb |
| F-11 | LOCKED: named legacy holdouts; B2-only |
| F-12 | one-person encrypted lockbox + dated audit (weak fallback) |
| F-13 | post-P2; one-seed; B3 not mitigation; tests secondary |

ResearchBox: **#8834** ([researchbox.org/8834](https://researchbox.org/8834)). Passcode must stay gitignored.

No P3 `tok_train` / `base_train` / `evaluate_bpb` run. Dummy lockbox tests use synthetic numbers only.
