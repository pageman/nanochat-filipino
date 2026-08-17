# Data card — WikiText-103 raw (P2 Gate B)

**Study:** NANOCHAT-FILIPINO P2-EN→TL (AsPredicted #306935)  
**Role:** English pretrain corpus for EN0 / A1. Not the Tagalog continuation corpus.  
**Gate:** B pass, 2026-08-17T15:13:38Z, run `p2-20260817T150944Z-de99f8a`

## Identity

| Field | Value |
|---|---|
| Dataset | Hugging Face `Salesforce/wikitext` |
| Config | `wikitext-103-raw-v1` (named in #306935) |
| HF revision | `b08601e04326c79dfdd32d625aee71d232d685c3` (lastModified 2024-01-04) |
| Paper | Merity, Xiong, Bradbury, Socher 2016, arXiv:1609.07843 |
| License | Wikipedia CC BY-SA; HF card lists cc-by-sa-3.0 and GFDL (README body also mentions CC BY-SA 4.0) |
| Domain | English Wikipedia **Good + Featured** articles (not a translation of WikiText-TL-39) |

WikiText-TL-39 (Cruz & Cheng 2019) is a **recipe analogue** of this corpus (all A–Z tl.wikipedia, no Good list). Do not call TL-39 a translation of WikiText-103.

## What was downloaded

Only `wikitext-103-raw-v1/*.parquet`. Not WikiText-2. Not `wikitext-103-v1` (word-level / `<unk>`). Not ClimbMix / FineWeb / DCLM. Not WikiText-TL-39. Files were not copied into `data/processed/wikitext-tl39/`.

| File | Split | Bytes (`wc -c`) | SHA256 | Rows |
|---|---|---:|---|---:|
| `train-00000-of-00002.parquet` | train | 156,987,808 | `74da360f23826045b3e6ac6375411fdb15f003030aa74f2596ed08b857cb9212` | 900,675 |
| `train-00001-of-00002.parquet` | train | 157,088,770 | `ba090ac30dbf5461e8dcbdd1a1b8e6f3cf9c2c756d64f0c1220450acd514f720` | 900,675 |
| `validation-00000-of-00001.parquet` | validation | 657,209 | `204929b7ff9d6184953f867dedb860e40aa69c078fc1e54b3baaa8fb28511c4c` | 3,760 |
| `test-00000-of-00001.parquet` | test | 732,610 | `5f1bea067869d04849c0f975a2b29c4ff47d867f484f5010ea5e861eab246d91` | 4,358 |

SHA256 matches the Hugging Face LFS oid. Total bytes 315,466,397 = HF `download_size`. Row counts match the dataset card. Files are mode `0444`. Official Merity train/validation/test splits are kept (Gate D must not re-hash 70/15/15).

## Surface (raw, not word-level)

- `<unk>` rows: **0** (word-level `wikitext-103-v1` would not look like this).
- Nonempty / empty rows: 1,170,381 / 639,087 (blank lines are normal in this dump).
- Article-like `= Title =` headers: 29,566 (article inventory is Gate D, not this gate).
- Residual `@-@` / `@,@` still occur in this HF raw dump. That is **not** the Cruz & Cheng Moses WikiText-TL-39 surface. Record it; do not detokenize for confirmatory P2.

Literature Table 1 (word-level paper): ~28,475 train articles / ~103M Moses tokens. BPE `T_en_train` is Gate G.

## Path

`data/raw/wikitext-103-raw/wikitext-103-raw-v1/` (gitignored blobs). Hashes live in `gate-b-english-archive.json`.
