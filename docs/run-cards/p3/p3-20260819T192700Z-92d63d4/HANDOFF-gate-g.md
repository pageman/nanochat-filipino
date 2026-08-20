# Gate G handoff — P3 #307342 / ResearchBox #8834

**Host:** Mac/CPU. **GPU:** no through Gate G.

| Item | Value |
|---|---|
| AsPredicted | [#307342](https://aspredicted.org/wd2pc8.pdf) |
| ResearchBox | [#8834](https://researchbox.org/8834) |
| RUN_ID | `p3-20260819T192700Z-92d63d4` |
| Gates A–G | **PASS** |
| `N_TL0` | 294 |
| `T_tl_train` | 6,401,013 |
| P3 tokenizer | fresh `tok_train`; SHA matches P1.1 fixed point (`04436b85…`) |
| B3 mix frozen | K=28472; doc 50/50; byte share EN ≈0.961 |

**Blinding:** fertility diagnostics in lockbox only. No P3 BPB. Safe to proceed to Gate H smoke on CUDA.

**Next:** Gate H (d4 smoke, not TL0) on A40-class NVIDIA. Then Gate I / P0-T with lockbox. Rotate lockbox passphrase before real eval.

Receipts: `docs/run-cards/p3/p3-20260819T192700Z-92d63d4/gate-*.json`
