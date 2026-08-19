# P2 Data codebook (ResearchBox 8763)

ResearchBox **Data** cells reject `.md`, loose `.json`, and any zip with more than one file. Upload the seven `.txt`/`.csv` files in `Data/` **one at a time**. Put JSON receipts in **Other** (`P2-data-receipts.zip`). This markdown file is repo documentation only.

**Column:** Data  
**Section:** P2  
**Role:** Identity hashes, split/mix manifests, sealed numeric outcomes, and exposure tables. **Not** raw Wikipedia dumps and **not** protected holdouts.

WikiText-103 raw and WikiText-TL-39 train remain at their public/frozen sources. This packet records SHA-256 identities so a reviewer can verify a local copy without redistributing test text.

## What is deliberately absent

| Artifact | Why excluded | Identity recorded here |
|---|---|---|
| WT103-raw English test jsonl | Protected official test | SHA-256 `2bccabc020cbb8d09273cccdc42ed926957b83824ca767c96fb588041b8d434e` |
| P1.1 Tagalog `test.jsonl` | Legacy holdout; one P2 touch already used | SHA-256 `3bd193458f4c494d84dae345548c0c01cb6cd7275e98d6ed39a41d517a093baf` |
| Model `*.pt` | Weights belong on Hub, not this documentation box | See `checkpoint_sha256.txt` |
| ResearchBox passcode | Secret | Never deposited |

P1.1 native-BPE `test_bpb=1.164768` is **not** a P2 observation. P2 A2 Tagalog secondary test is `1.160154` under English BPE.

## Files in the ResearchBox Data packet (allowed extensions only)

| File | Role |
|---|---|
| `P2-DATA-CODEBOOK.txt` | This cover as `.txt` |
| `sealed_val_bpb.csv` | Gate U full validation table |
| `primary_contrasts.csv` | \(C_{EN}\), \(G_{TL}\), A3 contrasts, A2 tests |
| `a3_realized_shares.csv` | Document / byte / BPE-token shares |
| `exposure_by_arm.csv` | Unique docs, bytes, BPE tokens, revisit |
| `file_hashes.csv` | Train/val/tokenizer/checkpoint hashes |
| `checkpoint_sha256.txt` | A0/A1/A2/A3 and excluded-test identities |

JSON receipts (`LOCK.sanitized.json`, Gate U/V, etc.) are **Other** file `P2-data-receipts.zip`.

## Sealed primary table (authority: `gate-u-seal.json`)

| Arm | English val BPB | Tagalog val BPB |
|---|---:|---:|
| Untrained | 3.246978 | — |
| A0 | 1.389990 | 4.917650 |
| A1 | 1.459675 | 5.054664 |
| A2 | 1.385684 | 1.171616 |
| A3 | 1.279433 | 1.528858 |

\(C_{EN}=\mathrm{EN}(A2)-\mathrm{EN}(A1)=-0.073991\) (filed \(\ge 0.01\): **not observed**).  
\(G_{TL}=\mathrm{TL}(A2)-\mathrm{TL}(A1)=-3.883048\) (filed \(\le -0.01\): **observed** in this one-seed apparatus).

## A3 realized shares (document mix, not token-equated)

Documents 50/50 (K=28,472). UTF-8 bytes EN 0.961314 / TL 0.038686. English-BPE tokens EN 0.933232 / TL 0.066768.

## English train / Tagalog train hashes (not test)

- English train jsonl `09ae691caebb33a4bb81db4e570f630cac9ede11cb4116b2e08a3dbe08ef775a`
- English val jsonl `874dec29844b3d46fc39e5479ee2dc4b3ba37309d9baf3bba4b5654697f3ae3b`
- Tagalog train jsonl `2b0474c5700dc1eba14def572aa23cc227e4c59c10c2de3ce6b7bda75d137687`

## Tokenizer

- `tokenizer.pkl` `946a04ef05e73be625f24ea5e88bfa4531546ae7d7238fbe1b0fd68df016ace6`
- `token_bytes.pt` `5ae2ea1d214f2b7f98eeba606d461db62d04101e7a947a3201ec6bb2a7062d42`  
(binary tokenizer files are **not** in this Data zip; hashes only.)
