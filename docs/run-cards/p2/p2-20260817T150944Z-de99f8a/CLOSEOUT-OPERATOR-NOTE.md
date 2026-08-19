# P2 close-out operator note (2026-08-19)

Scientific computation remains closed. This pass did archival/publication hygiene only.

## Done locally

- Hash-verified A0/A1/A2/A3, tokenizer, English/Tagalog/A3 shards, Gate U/V/W records, LOCK, test ledger (`authorized_touches=1`).
- Frozen documentation archive: `transfer/p2-closeout-archive-20260819` (read-only). Weights stay in `data/cache/p2-20260817T150944Z-de99f8a/` (already 444 on branch `.pt`).
- Refreshed ResearchBox pack (metadata only): `transfer/p2-researchbox-8763-20260819`.
- Compiled current paper with tectonic 0.17.0. Quarantined the 16 August PDF.
- Expanded Hub model card source. Did **not** upload `.pt` files (complete-set rule; deferred).
- Did **not** stop or terminate pods/volumes.

## Still human / live-web

1. Log in to ResearchBox 8763 and upload the local pack; spot-check one deposited file against `HASHES.md`.
2. Upload A0+A1+A2+A3 weights together to `pageman/nanochat-filipino-p2-en-then-tl`, then re-hash downloads.
3. Paste `docs/run-cards/p2/PUBLIC-STATUS.md` onto the public guide.
4. After those external copies exist, terminate the 80 GB volume. Not before.
