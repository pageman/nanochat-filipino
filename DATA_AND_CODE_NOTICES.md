# Data and code notices

This model was pretrained on WikiText-TL-39 (Cruz & Cheng, 2019), a Tagalog Wikipedia-derived language-modeling corpus. Wikipedia text is available under the Creative Commons Attribution-ShareAlike License. This is not an official De La Salle University, Cruz, or Cheng release.

| Artifact | Terms | Obligation |
|---|---|---|
| Tagalog Wikipedia text | CC BY-SA (dump-stated version) | Attribution; share-alike if you redistribute a derived corpus |
| WikiText-TL-39 compilation | Cite Cruz & Cheng 2019, arXiv:1907.00409 | Cite the paper in every report |
| Hugging Face mirror `linkanjarad/Wikitext-TL39` | Hub dataset terms plus upstream | Record dataset id and file hash (`706d7064…`) |
| nanochat trainer | MIT, commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd` | Retain copyright in any clone |
| This repository | MIT for code; research-only for weights | See [LICENSE](LICENSE) and [LICENSE-RESEARCH.md](LICENSE-RESEARCH.md) |

Split label in every caption: `reconstructed_article_70_15_15`. The original 2019 train/validation/test files were not recovered.

Held-out `test.jsonl` is not redistributed here. ResearchBox credentials are not published.

P4 weights, if used, are the complete C0+C1+C2+C3 bundle at https://huggingface.co/pageman/nanochat-filipino-p4-token-share-mix. Do not treat C3 alone as the P4 model. C3 is not P3 B3.
