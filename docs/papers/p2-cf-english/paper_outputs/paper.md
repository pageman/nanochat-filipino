**Keywords:** catastrophic forgetting; English retention; Tagalog acquisition; WikiText-103; WikiText-TL-39; bits-per-byte; equal-exposure; nanochat; preregistration; continual pretraining.

**arXiv categories:** cs.CL, cs.LG.

**Code and weights:** study repository <https://github.com/pageman/nanochat-filipino> (P2 subtree); model card and (when uploaded as a complete set) branch checkpoints at <https://huggingface.co/pageman/nanochat-filipino-p2-en-then-tl>. Registration: <https://aspredicted.org/xa56bs.pdf>. ResearchBox: <https://researchbox.org/8763>. P1.1 paper and weights remain separate: <https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39>; <https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x>.

# Introduction {#sec:intro}

Pajo [@pajo2026p11] trained nanochat from scratch on WikiText-TL-39 and measured held-out Tagalog BPB under equal exposure (AsPredicted #306780). That study is complete and is not amended here. Those Tagalog-only checkpoints never saw English, so they cannot answer whether a model "forgot English because it learned Tagalog." WikiText-TL-39 is a corpus, not an English-pretrained model [@cruz2019eval]. English pretraining is a separate nanochat run on WikiText-103 raw [@merity2017pointer].

Typical large-model forgetting work starts from an English or multilingual base and adds a new task [@luo2023forgetting; @ramasesh2021forgetscale; @mccloskey1989catastrophic]. This paper stays in that causal direction and keeps P1.1's purity: WikiText-family text, nanochat depth dial, BPB rather than CORE [@karpathy2026nanochat; @pajo2026p11]. The Tagalog stage is sequential continued pretraining under language shift, not classifier fine-tuning [@shi2024continual; @cruz2019eval]. Equal-exposure arithmetic is copied from P1.1 so English pretraining is not a silent compute confound [@kaplan2020scaling; @hoffmann2022chinchilla; @muennighoff2023dataconstrained].

The confirmatory question, filed before confirmatory continuation BPB existed, is:

> When an English-pretrained nanochat (EN0), whose English provenance has passed P0, is continued for $D_{\mathrm{phase2}}$ tokens on WikiText-TL-39 train, does English held-out BPB rise more than under matched extra-English continuation, and does Tagalog held-out BPB fall toward the P1.1 from-scratch ceiling?

The registered English-cost prediction was $C_{\mathrm{en}}\ge 0.01$. The registered Tagalog-gain prediction was $G_{\mathrm{tl}}\le -0.01$. The filing stated that the study would not claim a population effect, would not reuse P1.1's native-BPE test BPB as a P2 observation, and is not a CORE, chat, or classification test [@aspredicted306935].

This paper contributes four things.

1.  A preregistered English-then-Tagalog nanochat run with frozen A0 parent, matched phase-2 budget, and dual full-split BPB, independent of #306780.

2.  A recoverable English path: Hugging Face WikiText-103-raw revision, official Merity splits, train-only 32,768 BPE, and isolated test text that is not redistributed.

3.  A one-test-touch evaluation: seal English $C_{\mathrm{en}}$ and Tagalog $G_{\mathrm{tl}}$ on validation with both tests unread, then one A2-only secondary test event.

4.  A locked reading of this one-seed apparatus: the Tagalog-gain pattern was observed; the English-cost pattern was not observed (opposite sign on $C_{\mathrm{en}}$).

The paper follows the close-out record for AsPredicted #306935. It does not amend #306780.

# Related work {#sec:related}

## Filipino and Tagalog language resources

Cruz and Cheng constructed WikiText-TL-39 as a Tagalog analogue of WikiText [@cruz2019eval]. P1.1 measured equal-exposure depth versus Tagalog BPB on a reconstructed-article split of that package [@pajo2026p11; @aspredicted306780]. Later Filipino encoder and mixed-corpus work answers a different question. Those resources do not say what happens to English held-out BPB when a decoder that was actually pretrained on WikiText-103 is continued on frozen WikiText-TL-39 train at a matched token budget.

## Language-modeling evaluation

WikiText established a clean Wikipedia language-modeling setup in English [@merity2017pointer]. BPB remains the fair comparison when vocabularies differ [@shannon1951prediction; @melis2018eval; @brown2020gpt3]. This study uses official `evaluate_bpb`: mean token negative log-likelihood divided by $\ln 2$ times mean UTF-8 bytes per token. In-loop trainer validation is diagnostic and is not `val_bpb_full`.

## Scaling, depth, and data constraints

Kaplan et al. described loss versus compute, data, and parameters [@kaplan2020scaling]. Hoffmann et al. argued that many large models were undertrained relative to parameter count [@hoffmann2022chinchilla]. Muennighoff et al. studied repeated epochs when unique data are scarce [@muennighoff2023dataconstrained]. P1.1 held $D_{3x}$ fixed across depths. P2 holds $D_{\mathrm{phase2}}=D_{\mathrm{actual}}^{\mathrm{P1.1}}=19{,}267{,}584$ fixed across A1, A2, and A3 so the forgetting contrast is not a compute contrast.

## Catastrophic forgetting and continual pretraining

Sequential overwriting of old knowledge is the classical interference problem [@mccloskey1989catastrophic; @french1999cf; @goodfellow2013cf]. LLM papers often start from an English base and add a new language or task [@luo2023forgetting; @ramasesh2021forgetscale; @shi2024continual]. Elastic weight consolidation and replay are later, named follow-ons, not this experiment [@kirkpatrick2017ewc; @lopezpaz2017gem]. P1.1 Hub checkpoints are a Tagalog-from-scratch speedrun. Using them as the P2 parent would measure Tagalog retention under English data---the opposite causal arrow.

## Preregistration and confirmatory practice

Preregistration reduces undisclosed flexibility [@simmons2011falsepositive; @wagenmakers2012confirmatory; @nosek2018prereg]. AsPredicted #306935 locked the question, parent, arms, budgets, dual BPB, $0.01$ practical cutoff, one-test-touch rule, and independence from #306780 before confirmatory continuation BPB existed [@aspredicted306935].

# Glossary {#sec:glossary}

::: description
Frozen Tagalog-from-scratch equal-exposure study. Not the English parent.

English-from-scratch nanochat on WikiText-103 raw. This is the CF parent.

Provenance battery before any Tagalog train token. P0-E: EN0 English `val_bpb_full` beats untrained and byte-unigram floors by $\ge 0.01$.

Frozen EN0 d20 parent; dual eval; no additional train tokens.

Extra-English continuation, $D_{\mathrm{phase2}}$ (active control).

Tagalog continuation on frozen P1.1 train, $D_{\mathrm{phase2}}$ (intervention). Only tested arm.

50/50 English/Tagalog *documents*, $D_{\mathrm{phase2}}$. Trade-off arm, not mitigation.

English `val_bpb_full`(A2)$-$`val_bpb_full`(A1). Filed $\ge 0.01$.

Tagalog `val_bpb_full`(A2)$-$`val_bpb_full`(A1). Filed $\le -0.01$.

Bits per UTF-8 byte. Lower is better.

Official full-split validation BPB after the final checkpoint. Primary DV.

Same formula on an isolated test split. Secondary. A2 only, after the val seal.

Phase-2 model-visible tokens: $294\times 65{,}536=19{,}267{,}584$.

Context length. Frozen at 2048.

English 32,768-merge tokenizer, WikiText-103 raw *train* only.

One-pass packing with BOS, length-$T$ rows, no wrap.

Excluded from confirmatory P2.
:::

# Methods {#sec:methods}

## Registration and authority

AsPredicted #306935 is the governing record (PDF SHA-256 prefix `d6dff034`) [@aspredicted306935]. ResearchBox #8763 is the deposit box. Authority: PDF #306935 $>$ protocol $>$ this manuscript $>$ ledger $>$ deviation. The study does not amend #306780 or ResearchBox #8735. Exploratory items named in the form stay outside the primary table.

## Corpus and canonical text

English: Hugging Face `Salesforce/wikitext`, config `wikitext-103-raw-v1`, revision prefix `b08601e0`, downloaded 2026-08-17. Canonical English text is LF-only. No detokenize, NFC, language filter, or dedup. Residual `@-@` marks in the HF raw dump were left as released.

Tagalog continuation text is the frozen P1.1 train jsonl (SHA-256 prefix `2b0474c5`), not a new scrape.

## Split

English uses official Merity train/validation/test article splits (Gate D), not a 70/15/15 re-hash. Counts: train 28,472 documents, val 60, test 60. English train jsonl SHA-256 prefix `09ae691c`. Tagalog evaluation uses the P1.1 reconstructed validation shard under the *English* BPE. Exact document-hash overlap across English train/val/test is 0. Drop-audit on frozen kept train jsonl files: 0 null/empty units and 0 documents $>200{,}000$ characters.

## Tokenizer

One English 32,768 BPE, train shards only (tokenizer SHA-256 prefixes `946a04ef` / `5ae2ea1d`). P1.1 Tagalog BPE is not used in P2 training. Fertility is descriptive (English val $4.603$ bytes/token; Tagalog val $2.574$ bytes/token) and is not forgetting evidence.

## Model and budget

Every trained weight is a nanochat decoder from commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`, plus the documented `NANOCHAT_DATA_DIR` hook and no other model-file edits. EN0: $T=2048$, $B=65{,}536$, $N_{\mathrm{EN0}}=5415$ from English $D_{3x}=3\times T_{\mathrm{en,train}}$ with explicit `--num-iterations` (ratio never $-1$), CORE off. Confirmatory continuation is depth 20 only. Children load frozen A0 with a fresh optimizer; the pin has no `--load`. $D_{\mathrm{phase2}}=19{,}267{,}584$. Forbidden: Hugging Face `Trainer` or `from_pretrained` as the language model, loading P1.1 `model_000294.pt` as the English parent, `python -m nanochat.dataset`.

::: center
  Arm   Start     Phase-2 stream
  ----- --------- ------------------------------------------
  EN0   random    English train (pretrain)
  A0    EN0 d20   none (dual eval)
  A1    A0        official WT103-raw train
  A2    A0        frozen P1.1 Tagalog train
  A3    A0        seed-42 50/50-document mix, $K=28{,}472$
:::

## Host

Official EN0 d20 and phase-2 children ran on Runpod Secure A40 (48 GB), EU-SE-1, pod tag `p2-en0-d20`. A separate A40 smoke pod established the CUDA path. Environment: `scripts/p2/env.sh` / `scripts/p2/env.cuda.sh` only (never `scripts/p1/env.sh`).

## Evaluation

Evaluator: `scripts/p2/evaluate_bpb.py` via Gate U/V wrappers. Packing: one-pass BOS-bestfit, $T=2048$, device batch 8, non-overlapping stride. Packed UTF-8 bytes: English val 624,360; Tagalog val 5,205,755. Seal: Gate U at 2026-08-19T07:17:53Z with `test_read_count=0`. Test: one authorized Gate V touch, A2 only (English then Tagalog component). A1 and A3 were not tested. In-loop `eval-tokens` is not `val_bpb_full`.

## What was not done

No ClimbMix. No overwrite of `p1-fixed-d20-3x`. No confirmatory SFT, CORE, EWC, or replay. No mixing tokenizers in one run. No reuse of P1.1 native-BPE test BPB $1.164768$ as a P2 observation. No P1.1-weights-on-English OOD as a post-outcome rescue. Native-speaker ratings were not collected and were not invented.

# Results {#sec:results}

Phase-2 cells are one-seed d20 point estimates after AsPredicted #306935 [@aspredicted306935; @simmons2011falsepositive; @wagenmakers2012confirmatory; @nosek2018prereg]. P1.1 Tagalog Table 2 is cited, not rerun.

## Primary confirmatory table

Table [1](#tab:primary){reference-type="ref" reference="tab:primary"} is the sealed Gate U validation table. $C_{\mathrm{en}}=\mathrm{EN}(A2)-\mathrm{EN}(A1)=-0.073991$. $G_{\mathrm{tl}}=\mathrm{TL}(A2)-\mathrm{TL}(A1)=-3.883048$.

  Arm           English val BPB   Tagalog val BPB
  ----------- ----------------- -----------------
  Untrained            3.246978               ---
  A0                   1.389990          4.917650
  A1                   1.459675          5.054664
  A2                   1.385684          1.171616
  A3                   1.279433          1.528858

  : Primary confirmatory outcomes. Seed 0, depth 20, $N_{\mathrm{phase2}}=294$, $D_{\mathrm{phase2}}=19{,}267{,}584$, English 32,768 BPE, official `evaluate_bpb`, $T=2048$. P1.1 d20 Tagalog $1.172248$ uses a different tokenizer and is descriptive only. {#tab:primary}

## Prediction outcome

The filed English-cost pattern ($C_{\mathrm{en}}\ge 0.01$) was **not observed**: A2 English BPB was lower than A1 by $0.073991$ BPB (opposite sign; $\lvert\Delta\rvert$ is material at $0.01$). This does not license a general claim that Tagalog improves English beyond this one-seed, fixed-data, fixed-budget apparatus.

The filed Tagalog-gain pattern ($G_{\mathrm{tl}}\le -0.01$) was **observed** in this one-seed apparatus. A2 Tagalog BPB was substantially below A1 under the shared English BPE.

A3 versus A1: $\mathrm{EN}(A3)-\mathrm{EN}(A1)=-0.180242$; $\mathrm{TL}(A3)-\mathrm{TL}(A1)=-3.525806$. A3 is the predeclared 50/50-*document* mix trade-off arm, not token-equated, and is **not** registered as mitigation. Realized mix shares (frozen seed-42 order `b6ae432b…`): documents $50/50$; UTF-8 bytes English $0.961314$ / Tagalog $0.038686$; English-BPE tokens English $0.933232$ / Tagalog $0.066768$. A0 Tagalog is parent provenance; A0$\rightarrow$A2 Tagalog change is descriptive only.

## Secondary confirmatory test

After the val seal, one authorized secondary test touch scored A2 only. English WT103-raw test BPB $1.392015$. The P1.1 Tagalog `test.jsonl` is a legacy external holdout scored under P2 English BPE: $1.160154$. These secondary results do not alter sealed $C_{\mathrm{en}}$ or $G_{\mathrm{tl}}$. P1.1's native-BPE test BPB $1.164768$ is not reused. A1 and A3 were not tested.

## Required baselines

EN0 English `val_bpb_full` beat both an untrained same-depth model and a train-fitted add-one UTF-8 byte unigram ($4.582801$) by $\ge 0.01$ at depths 8 and 20 (Table [2](#tab:p0e){reference-type="ref" reference="tab:p0e"}). P0-E therefore passed; the d20 parent may be called English-pretrained. Confirmatory continuation uses the frozen d20 parent only.

  Model             val BPB   Untrained   Gap vs untrained
  -------------- ---------- ----------- ------------------
  EN0 d8           0.983292    3.246994           2.263702
  EN0 d20 (A0)     1.389990    3.246978           1.856988

  : P0-E English provenance, official `evaluate_bpb`, $T=2048$. Byte unigram $=4.582801$. {#tab:p0e}

## Secondary analyses, not used for $C_{\mathrm{en}}$ or $G_{\mathrm{tl}}$

Table [3](#tab:exposure){reference-type="ref" reference="tab:exposure"} reports unique-stream exposure. Revisit $=D_{\mathrm{phase2}}/T_{\mathrm{unique}}$. These descriptors were not used to pick arms.

  Arm       Docs   Canonical bytes   Unique BPE tokens   Revisit
  ----- -------- ----------------- ------------------- ---------
  A1      28,472       539,903,397         118,286,771     0.163
  A2      37,602        29,165,137          11,352,473     1.697
  A3      56,944       561,630,369         126,749,578     0.152

  : Phase-2 unique-stream exposure. $D_{\mathrm{phase2}}=19{,}267{,}584$. Not confirmatory DVs. {#tab:exposure}

Registered Question 8 items that are not primary DVs: A2 English trajectory was **not collected** (A2 in-loop validation used the Tagalog last shard). PTPP $R_d(\mathrm{step})=\mathrm{step}/294$ is defined; an English-BPB-versus-$R_d$ plot was not made. Fertility is reported above. P1.1 d20 on English UTF-8 was **not run** and will not be added as a post-outcome P2 rescue.

# Discussion {#sec:discussion}

Required narrow reading: in this preregistered, one-seed, fixed-parent, fixed-budget apparatus, the predicted English-retention-cost pattern was not observed; the A2-versus-A1 validation contrast instead favored A2 on English BPB, while the preregistered Tagalog-gain pattern was observed. Sequential Tagalog at $D_{\mathrm{phase2}}$ therefore did not overwrite English on the primary BPB contrast. This is not a claim that Tagalog continuation causes English improvement in general. P0-E still licenses "pretrained in English" for the d20 parent. Do not equate A2 Tagalog val $1.171616$ with P1.1's $1.172248$. Spark/MPS paths, if mentioned, are non-confirmatory.

A study designed after these Gate U numbers were seen is a post-P2 follow-up, not an outcome-independent mirror.

# Limitations {#sec:limits}

- One parent seed: point estimates only. No $p$-value, confidence interval, seed interval, or population-effect claim.

- The $0.01$ BPB rule is a practical cutoff, not a significance test; $\lvert C\rvert$ or $\lvert G\rvert<0.01$ is not a ranking.

- Confirmatory A1/A2/A3 at d20 only.

- English BPE on Tagalog text; BPB still compares bytes.

- Mix is 50/50 documents, $96.13\%$ English by UTF-8 and $93.32\%$ by BPE tokens.

- WikiText-103 is not web English. P1.1 uses a reconstructed split. Named entities may overlap.

- No chat. Tests are secondary and A2-only.

- Exploratory items named in the form (d8 continuation, replay, FilBench, EWC, tokenizer swap, CORE, SFT, Spark/MPS) were not run as P2 confirmation.

# Future research {#sec:future}

These directions are *not* P2, do not amend AsPredicted #306935, and must not reopen sealed $C_{\mathrm{en}}$, $G_{\mathrm{tl}}$, or the A2-only test ledger. An informal plain-language comment that restates "train EN0, pass P0-E, run matched continuation, then one test touch" is educational only. It must not become a new governing rule, a replacement for #306935, or a post-hoc selection criterion. That comment, if used uncorrected, omits A3, compresses the two-depth P0-E gate into "the English base," and can be misread as authorizing an A1/A3 test comparison. P2 already executed the filed sequence: both EN0 d8 and d20 passed P0-E; A1, A2, and A3 ran at d20 from frozen A0; validation sealed first; one A2-only secondary test event followed.

Do not insert a **P2.1 intermezzo** before P3 merely because the wrapper, freeze, or archive were operationally complex. Those belong in run cards unless they change treatment, outcome, or selection. A forward replication with a fresh seed is valuable, but it is a separately preregistered study (best as a P4 component), not an emergency patch on #306935. If designed after Gate U was unblinded, label it a post-result replication, not independent confirmation.

Do not add to a future filing, as if they were silent P2 repairs: a new loss-based early-stop, a d8 continuation parent (d20 was the confirmatory continuation depth), a new mixture ratio chosen after seeing Table [1](#tab:primary){reference-type="ref" reference="tab:primary"}, a seed interval computed from this one seed, a new test benchmark, SFT, a downstream task used to pick a branch, or a post-hoc A1/A3 test contrast. Do not switch the parent to d8 because EN0 d8 English val BPB was lower than d20. Do not skip A3 to save cost in a study that filed A3. Do not treat A0 Tagalog BPB as $G_{\mathrm{tl}}$. Do not treat P0-E floors as proof that d20 is globally strong. Permissions (`chmod 444`) are not lineage proof; hashes and receipts are. A fresh optimizer is part of the treatment definition.

## P3: reverse-direction continual pretraining

P3 answers a question P2 cannot: whether a specified frozen *English* continuation stream changes retained Tagalog and acquired English predictive fit relative to matched extra-Tagalog continuation, after a *fresh* Tagalog parent has cleared a Tagalog eligibility gate. It must be a **separate** AsPredicted/ResearchBox record, filed with an explicit statement that it was designed after P2 Gate U unblinding on 19 August 2026 if that is when it is written. It must not reuse P2 or P1.1 weights as the P3 parent, must not assume the forward result is symmetric, and must not use P2 outcomes to choose P3's budget, tokenizer, mix ratio, cutoff, test, or preferred direction.

Recommended mirror (names are illustrative; the P3 PDF governs):

::: center
  P2 (done)                                           P3 analogue (future filing)
  --------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------------
  Fresh English EN0 parent                            Fresh Tagalog parent TL0 under a frozen P3 protocol
  P0-E on d8 and d20 English val                      P0-T: TL0 d8 and d20 beat untrained and Tagalog-train byte-unigram floors on full Tagalog val before English tokens enter a child
  A1 extra English                                    B1 matched extra Tagalog
  A2 Tagalog intervention                             B2 English continuation
  A3 pre-frozen EN--TL document mix                   B3 separately pre-frozen TL--EN mix with reported document/byte/token shares
  $C_{\mathrm{en}}=\mathrm{EN}(A2)-\mathrm{EN}(A1)$   $C_{\mathrm{tl}}=\mathrm{TL}(B2)-\mathrm{TL}(B1)$ (Tagalog retention cost)
  $G_{\mathrm{tl}}=\mathrm{TL}(A2)-\mathrm{TL}(A1)$   $G_{\mathrm{en}}=\mathrm{EN}(B2)-\mathrm{EN}(B1)$ (English acquisition gain)
  A2-only post-seal test                              B2-only post-seal test, sources locked before P3 outcomes
:::

Wording to use: P3 is a separately preregistered reverse-direction continual-pretraining study. It does not confirm P2. Wording to avoid: "P3 confirms P2," "English is more/less destructive," or "we chose P3 because P2 showed $C_{\mathrm{en}}<0$."

## P4 and other named follow-ons

P4 is the natural home for a fresh-seed exact forward replication of P2's A2-minus-A1 validation contrast under the same frozen corpus/tokenizer/budget/branch definitions, optionally beside a fresh-seed reverse replication and a *predeclared* directional-asymmetry synthesis. If only one post-P2 study can be afforded, choose deliberately between that forward replication and P3; do not hide the choice inside a vague "P2.1."

Other exploratory items, each requiring its own registration if confirmatory: replay or EWC; P1.1-weights-on-English UTF-8 as never-trained-on-English OOD (not BWT, not P2 rescue); A2 English in-loop trajectories under a protocol that does not reread P2 tests; downstream Philippine tasks as transfer probes; chat SFT and CORE as named follow-ons.

# Conclusion {#sec:conclusion}

This paper reported a preregistered, equal-exposure English-then-Tagalog nanochat run. P1.1 stays a pure Tagalog base and is not amended. P2 trained an English parent, passed P0-E, continued A1/A2/A3 at $D_{\mathrm{phase2}}=19{,}267{,}584$, and sealed dual `val_bpb_full` before one A2-only secondary test touch. In this one-seed d20 run the registered Tagalog-gain pattern was observed and the registered English-cost pattern was not observed.

The original contribution is the locked measurement: same parent, same tokens, same tokenizer, three phase-2 streams, one test touch, and a refusal to rewrite #306780. The paper does not claim a general Filipino--English law, a chat system, or that Tagalog improves English outside this apparatus.

# Novelty statement {#novelty-statement .unnumbered}

The paper advances Tagalog/English language-modeling evidence by replacing an informal "continue a Tagalog nanochat" story with a preregistered English parent, a matched extra-English control, and dual full-split BPB. It records that P1.1 checkpoints cannot be the catastrophic-forgetting parent, and it separates confirmatory validation from one secondary A2 test. The empirical advance is mixed at the study's own threshold: Tagalog adaptation was large; the predicted English cost versus extra English was not observed.

# Data, code, and weights {#data-code-and-weights .unnumbered}

English source: Hugging Face `Salesforce/wikitext` / `wikitext-103-raw-v1`. Tagalog train: frozen P1.1 jsonl. Registration: AsPredicted #306935. Code, evaluator, and run cards: <https://github.com/pageman/nanochat-filipino>. Model card: <https://huggingface.co/pageman/nanochat-filipino-p2-en-then-tl> (complete A0--A3 `.pt` set deferred until uploaded together). Held-out `test.jsonl` is not redistributed in public zips. ResearchBox #8763 is the metadata deposit; AsCollected #2416 records the WikiText-103 download. P1.1 weights remain at <https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x> and are not this study's parent.

# Ethics {#ethics .unnumbered}

The corpora are public Wikipedia-derived text. No human-subjects experiment was run. Sample ratings were not fabricated. Secrets (host credentials, box passcodes) are not published with this paper. Cheng is not a coauthor.

# Acknowledgements {#acknowledgements .unnumbered}

Thanks to AI/LLM models Manus 1.6 and Cursor Grok 4.6 High Fast for drafting, formatting, and solutioning. Special thanks to Dr. Cheng for guidance. WikiText-TL-39 is due to Cruz and Cheng [@cruz2019eval]. WikiText-103 is due to Merity et al. [@merity2017pointer]. nanochat is due to Karpathy [@karpathy2026nanochat]. Cheng is not a coauthor of this study. Errors are the author's.

# Funding {#funding .unnumbered}

This work was not supported by a dedicated grant. GPU time was paid by the author.

::: thebibliography
99

P. Pajo. Equal-exposure depth and held-out Tagalog bits-per-byte on WikiText-TL-39. August 2026. <https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39>.

P. Pajo. NANOCHAT-FILIPINO P1.1: WikiText-TL-39 fixed-budget depth vs held-out BPB. AsPredicted #306780, 15 August 2026. <https://aspredicted.org/6r6v4v.pdf>.

P. Pajo. P2: EN retention after TL continuation (nanochat, WikiText-103 then TL-39). AsPredicted #306935, 17 August 2026. <https://aspredicted.org/xa56bs.pdf>.

H. Shi et al. Continual learning of large language models: A comprehensive survey. *arXiv:2404.16789*, 2024.

J. C. B. Cruz and C. Cheng. Evaluating language model finetuning techniques for low-resource languages. *arXiv:1907.00409*, 2019.

S. Merity, C. Xiong, J. Bradbury, and R. Socher. Pointer sentinel mixture models. In *International Conference on Learning Representations*, 2017.

A. Karpathy. nanochat. Software repository, 2026. <https://github.com/karpathy/nanochat>.

M. McCloskey and N. J. Cohen. Catastrophic interference in connectionist networks: The sequential learning problem. In *Psychology of Learning and Motivation*, volume 24, pages 109--165, 1989.

R. M. French. Catastrophic forgetting in connectionist networks. *Trends in Cognitive Sciences*, 3(4):128--135, 1999.

I. J. Goodfellow, M. Mirza, D. Xiao, A. Courville, and Y. Bengio. An empirical investigation of catastrophic forgetting in gradient-based neural networks. *arXiv:1312.6211*, 2013.

J. Kirkpatrick et al. Overcoming catastrophic forgetting in neural networks. *Proceedings of the National Academy of Sciences*, 114(13):3521--3526, 2017.

D. Lopez-Paz and M. Ranzato. Gradient episodic memory for continual learning. In *Advances in Neural Information Processing Systems*, 2017.

Y. Luo et al. An empirical study of catastrophic forgetting in large language models during continual fine-tuning. *arXiv:2308.08747*, 2023.

V. V. Ramasesh, A. Lewkowycz, and E. Dyer. Effect of scale on catastrophic forgetting in neural networks. In *International Conference on Learning Representations*, 2022.

J. Kaplan et al. Scaling laws for neural language models. *arXiv:2001.08361*, 2020.

J. Hoffmann et al. Training compute-optimal large language models. *arXiv:2203.15556*, 2022.

N. Muennighoff et al. Scaling data-constrained language models. In *Advances in Neural Information Processing Systems*, 2023.

C. E. Shannon. Prediction and entropy of printed English. *Bell System Technical Journal*, 30(1):50--64, 1951.

G. Melis, C. Dyer, and P. Blunsom. On the state of the art of evaluation in neural language models. In *International Conference on Learning Representations*, 2018.

T. B. Brown et al. Language models are few-shot learners. In *Advances in Neural Information Processing Systems*, 2020.

J. P. Simmons, L. D. Nelson, and U. Simonsohn. False-positive psychology. *Psychological Science*, 22(11):1359--1366, 2011.

E.-J. Wagenmakers et al. An agenda for purely confirmatory research. *Perspectives on Psychological Science*, 7(6):632--638, 2012.

B. A. Nosek et al. The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11):2600--2606, 2018.
:::
