# P4 C3 mix construction specification

**Purpose:** Deterministic, auditable algorithm so a third party can reproduce the C3 stream from frozen train documents, tokenizer, and manifest.  
**Acceptance:** Implemented once at Gate E; read-only thereafter; second build only on predeclared integrity failure.

> **C3 is a newly constructed P4 tokenizer-token-share-locked mixture. It is not P3 `B3`, which was a separate pre-frozen equal-document mixture.**

## Exposure clock (one)

Quota is in **P4 Tagalog tokenizer tokens**, no BOS, no padding, no pack, no crop, counted **per training document** then concatenated. Trainer packing **MUST NOT** redefine the quota.

P4 **does not claim byte balancing**.

**Gate order:** Gate F (tokenizer frozen) **MUST** pass before this algorithm runs at Gate E. P3 could freeze B3 before tok_train because B3 was document-count; P4 cannot.

## Inputs (hashed)

- Frozen EN/TL **train** jsonl (val/test excluded).  
- Frozen `tokenizer.pkl` + `token_bytes.pt` (Gate F).  
- Filed \(q_{\mathrm{TL}}\), \(D_{\mathrm{phase2}}\), seeds, PRNG id, \(K_{\mathrm{blk}}\), rounding rule, revisit/truncation policies.

## Algorithm

1. Load document lists; verify split SHAs.  
2. For each document: encode; store `n_tokens`, `n_utf8_bytes`, sha of raw text.  
3. Shuffle each language list with filed PRNG+seed (independent seeds allowed; both filed).  
4. \(T_{\mathrm{TL}}^{\star}=\mathrm{round\_half\_to\_even}(q_{\mathrm{TL}} D_{\mathrm{phase2}})\); \(T_{\mathrm{EN}}^{\star}=D_{\mathrm{phase2}}-T_{\mathrm{TL}}^{\star}\).  
5. Walk each language list cyclically; append tokens; **truncate last document** of a language at a token boundary to hit the integer quota; record offset.  
6. Interleave into one stream with the filed **block schedule** (recommended: blocks of \(K_{\mathrm{blk}}\) tokens alternating so prefix deviation stays within \(\varepsilon_{\mathrm{path}}\)).  
7. Pack for nanochat under the filed last-shard policy. Mix **train** shards from C3; **val.parquet** = byte-identical C2 English val pack. **`val.parquet` is trainer-interface only** (not confirmatory; cannot set a gate; official DVs = frozen split JSONL at U).  
8. Write `p4_mix_manifest.json`; chmod read-only; write-probe must fail.  
9. Compute `full_stream_sha256` over packed **train** shards in sorted order. Also store `language_origin_mask_sha256`.  
10. **Pass:** language-origin token totals on the exact trainer-consumed packed train stream equal filed quotas; **no wrap/revisit** before \(N\times B\).

## Last-shard policy (to file)

**File:** mix **train** shards from C3 construction; **val.parquet** = byte-identical copy of English val pack used by C2 (hash match). `val.parquet` **MUST NOT** provide a gate signal. Confirmatory eval uses official split jsonl via `evaluate_bpb`.

## Forbidden

- Tuning interleave to reduce loss.  
- Skipping documents to chase byte share.  
- Using val/test documents.  
- Regenerating P3 B3.  
- A second mix because BPB “looked wrong.”
