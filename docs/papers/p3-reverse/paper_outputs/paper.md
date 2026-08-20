**Keywords:** Tagalog retention; English acquisition; continual pretraining; WikiText-TL-39; WikiText-103; bits-per-byte; equal exposure; nanochat; preregistration; reverse-direction; post-P2.

**arXiv categories:** cs.CL, cs.LG.

**Registration and deposits:** AsPredicted #307342 (<https://aspredicted.org/wd2pc8.pdf>); ResearchBox #8834 (<https://researchbox.org/8834>); AsCollected <https://ascollected.org/F36_C2C>; code <https://github.com/pageman/nanochat-filipino>; Hub <https://huggingface.co/pageman/nanochat-filipino-p3-tl-then-en>. Run ID: `p3-20260819T192700Z-92d63d4`.

# Introduction {#sec:intro}

Pajo [@pajo2026p11] measured equal-exposure Tagalog BPB across nanochat depths on WikiText-TL-39 (AsPredicted #306780). Pajo [@pajo2026p2] then asked the forward continual-pretraining question: after an English WikiText-103 parent clears an English eligibility gate, does matched Tagalog continuation raise English held-out BPB more than extra English, and does Tagalog BPB fall (AsPredicted #306935)? That forward study is complete. It does not answer the reverse arrow.

P3 asks the reverse causal question under the same instrument family: after a *fresh* Tagalog parent clears a Tagalog eligibility gate, does matched *English* continuation raise Tagalog held-out BPB more than extra Tagalog, and does English held-out BPB fall? The study was designed after P2 Gate U/V unblinding on 19 August 2026. It is therefore a prospectively preregistered **post-P2** reverse-direction study [@aspredicted307342]. It is not an outcome-independent confirmation of P2 and does not amend #306780 or #306935.

The confirmatory question, locked before any P3 tokenizer, TL0, B0--B3, validation BPB, or test BPB existed, is:

> After a newly trained P3-specific Tagalog nanochat parent (TL0) passes P0-T, does English continuation raise Tagalog held-out BPB more than matched extra Tagalog, and does English held-out BPB fall?

Filed directional predictions at depth 20: $$\begin{align}
C_{\mathrm{tl}}&=\mathrm{TL}(B2)-\mathrm{TL}(B1)\ge 0.01,\\
G_{\mathrm{en}}&=\mathrm{EN}(B2)-\mathrm{EN}(B1)\le -0.01.
\end{align}$$ B3 is a predeclared 50/50-*document* trade-off arm, not mitigation.

This paper contributes: (i) a locked reverse-direction equal-budget nanochat run with fresh P3 weights and tokenizer; (ii) P0-T before any English child token; (iii) six child validation cells plus descriptive B0 English, sealed before one B2-only secondary test touch; (iv) a Gate X release that reports both primary filed patterns as **observed** in this one-seed apparatus.

# Related work {#sec:related}

## Filipino resources and prior nanochat filings

Cruz and Cheng constructed WikiText-TL-39 [@cruz2019eval]. P1.1 used a reconstructed-article $70/15/15$ split and selected $D^*=20$ by exact minimum `val_bpb_full` [@pajo2026p11; @aspredicted306780]. P2 reversed the usual "Tagalog base then English" folklore by starting from English [@pajo2026p2; @aspredicted306935]. P3 closes the remaining arrow without loading P1.1 or P2 weights as parents.

## Continual pretraining and forgetting

Sequential interference is classical [@mccloskey1989catastrophic; @french1999cf]. LLM work often continues an English or multilingual base on a new language or task [@luo2023forgetting; @ramasesh2021forgetscale; @shi2024continual]. P3 stays inside WikiText-family text, nanochat depth dial, and BPB rather than CORE or chat [@karpathy2026nanochat]. Equal token budgets follow P1.1/P2 so stream identity is not confounded with compute [@kaplan2020scaling; @hoffmann2022chinchilla; @muennighoff2023dataconstrained].

## Evaluation

WikiText established clean Wikipedia LM evaluation in English [@merity2017pointer]. BPB remains comparable across vocabularies [@shannon1951prediction; @brown2020gpt3]. Official P3 BPB is mean token NLL divided by $\ln 2$ times mean UTF-8 bytes per token, full split, $T=2048$, BOS-best-fit. In-loop trainer BPB is not confirmatory.

## Preregistration

Preregistration reduces undisclosed flexibility [@nosek2018prereg; @wagenmakers2012confirmatory]. AsPredicted #307342 locked the reverse question, P0-T, arms, budgets, cutoffs, one B2-only test touch, and post-P2 disclosure before P3 outcomes existed [@aspredicted307342].

# Glossary {#sec:glossary}

::: description
Prior filings #306780 / #306935. Not amended. Not P3 parents.

Fresh Tagalog-from-scratch P3 parent (d8 and d20).

Tagalog eligibility: TL0 beats untrained and Tagalog-train add-1 byte-unigram floors by $\ge 0.01$ BPB at both depths before English child tokens.

Frozen TL0 d20 parent; no additional train tokens at freeze.

Extra-Tagalog continuation, $D_{\mathrm{phase2}}$ (active control).

English WikiText-103-raw continuation, $D_{\mathrm{phase2}}$ (intervention). Only tested arm.

Pre-frozen 50/50-*document* EN/TL mix, $D_{\mathrm{phase2}}$. Trade-off, not mitigation.

Tagalog `val_bpb_full`(B2)${}-{}$`val_bpb_full`(B1). Filed $\ge 0.01$.

English `val_bpb_full`(B2)${}-{}$`val_bpb_full`(B1). Filed $\le -0.01$.

Official full-split validation BPB after the final checkpoint. Primary DV.

Same formula on legacy external holdouts. Secondary. B2 only, after val seal.

$294\times 65{,}536=19{,}267{,}584$ model-visible tokens.

Context length, frozen at $2048$.
:::

# Methods {#sec:methods}

## Registration and authority

AsPredicted #307342 governs.

- PDF SHA-256:\

- Protocol SHA-256 at filing:\

ResearchBox #8834 is the deposit. AsCollected records public-data provenance at <https://ascollected.org/F36_C2C>. Authority: filed PDF $\gg$ protocol $\gg$ `LOCK.json` $\gg$ dated deviations $\gg$ this manuscript. The study does not amend #306780 or #306935.

## Pin and pipeline

nanochat commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`. Pipeline: `tok_train` $\rightarrow$ `base_train` / `continue_from_frozen` $\rightarrow$ `scripts/p3/evaluate_bpb.py`. CORE off. No Hugging Face `Trainer`. No attention patch relative to the pin. No P1.1/P2 weights as parents.

## Corpora and splits

Tagalog train/val/test documents are the frozen P1.1 reconstructed-article $70/15/15$ manifests (train SHA-256 prefix `2b0474c5`; val `4d51644b`; test `3bd19345`). English uses official WikiText-103-raw Merity splits from Hugging Face `Salesforce/wikitext`, config `wikitext-103-raw-v1`, revision prefix `b08601e0` (val document manifest `874dec29`; test `2bccabc0`). Cleaning: LF normalization; drop null/empty or documents $>200{,}000$ characters; stop if drops $>5\%$. Tests stay outside train/tokenizer mounts.

## Tokenizer

A new P3 Tagalog 32,768-merge BPE is trained on Tagalog *train* only (tokenizer SHA-256 prefix `04436b85`; full hash in Appendix [8](#app:hashes){reference-type="ref" reference="app:hashes"}). The same tokenizer is used for all arms and both languages' confirmatory BPB.

## TL0, P0-T, and B0

TL0 is trained at depths 8 and 20 from fresh weights on Tagalog train with $T=2048$, $B=65{,}536$, and ceiling budget $N_{\mathrm{TL0}}=\lceil 3T_{\mathrm{tl\_train}}/65536\rceil=294$. P0-T requires both depths to beat untrained and add-1 byte-unigram floors by $\ge 0.01$ BPB on Tagalog val before any English child token. On PASS, freeze final d20 as B0 (checkpoint SHA-256 prefix `ae621be2`).

## Mechanical carry-forward of budgets and cutoffs

The phase-two step count $N=294$, contrast cutoff $0.01$ BPB, and B3 50/50-*document* mix recipe were carried forward as filed post-P2 *mechanics* matching the P2 apparatus (same $B$, $T$, and equal-budget design language). They were not tuned to P2 contrast magnitudes, signs, or Gate V test numbers. P3 remains a prospective filing of the reverse arrow after P2 unblinding, not a magnitude-matched replication of P2.

## Phase-two arms

From identical B0 weights, with `load_optimizer=False` and fresh Muon+AdamW, peak LR $=0.3\times$ TL0 peak, warmup $14$:

- B1: Tagalog stream only (`p3-b1-extra-tl-d20`, SHA prefix `3f98784b`).

- B2: English stream only (`p3-b2-en-d20`, SHA prefix `5ee34b20`).

- B3: pre-frozen 50/50-document mix (seed 42, $K=28472$, frozen before TL0 validation; checkpoint SHA prefix `521bea16`; mix-order SHA prefix `b6ae432b`).

Each arm runs exactly $N=294$ new steps ($D_{\mathrm{phase2}}=19{,}267{,}584$). Terminal checkpoint only; no mid-run selection.

## B3 document mix versus realized exposure

B3 is defined on *documents*, not tokens. Gate E froze a 50/50 EN/TL document mix ($K=28472$ per language after SHA-sorted selection, seed 42) before TL0 validation. Because English Wikipedia documents are longer on average, realized UTF-8 byte shares in the frozen mix are heavily English-skewed (Table [1](#tab:b3exp){reference-type="ref" reference="tab:b3exp"}). BPE token shares were not a Gate E seal field; byte shares are the sealed exposure disclosure.

  Quantity                                          English            Tagalog
  ------------------------------------- ------------------- ------------------
  Document share (filed mix rule)                    $0.50$             $0.50$
  UTF-8 byte share (realized; Gate E)       $\approx 0.961$    $\approx 0.039$
  UTF-8 bytes in mix (Gate E)             $539{,}903{,}397$   $21{,}726{,}972$

  : B3 exposure: documented mix rule versus Gate E realized UTF-8 byte shares. {#tab:b3exp}

Mix-order SHA-256 prefix `b6ae432b`; full hash in Appendix [8](#app:hashes){reference-type="ref" reference="app:hashes"}. B3 remains a trade-off coordinate, not a mitigation claim.

## Gate S recovery

Early Gate S attempts failed when English training data were missing or corrupted (including AppleDouble junk), yielding a non-official zero-step/partial path. The official disposition, recorded in the Gate X preflight, was: quarantine the partial attempt; clean restart from frozen B0 with fresh optimizer on a cleaned English staging path (`en-clean`); complete exactly $294$ steps with exit code 0. No result-informed change of arms, budgets, cutoffs, or metrics---no result shopping. The quarantined partial is not an official B2 outcome.

## Evaluation and access control

Gate U seals six child cells B1/B2/B3 $\times$ {TL, EN} plus one descriptive B0 English `val_bpb_full`, with `test_access`=0 at seal. B0 English is excluded from contrasts. After the seal, Gate V performs one authorized B2-only event with two legacy external holdouts (English WT103-raw test manifest; Tagalog P1.1 `test.jsonl`), then `test_access`=1. B1 and B3 are not tested. Gate X is a status-only preflight plus one-time release of the sealed package. Raw test text remains restricted.

## Compute note

TL0 d8 and d20 both completed $N=294$ steps on a Runpod A40 (`bef5h2lzy6f3mp`). Wall-clock hours were not sealed as confirmatory fields in the Gate I receipts and are omitted here.

# Results {#sec:results}

## Primary sealed validation table

Table [2](#tab:primary){reference-type="ref" reference="tab:primary"} reports full-split `val_bpb_full` after final checkpoints (one seed; point estimates only).

  Arm   Role                               Tagalog `val_bpb_full`   English `val_bpb_full`
  ----- ----------------------- --------------------------------- ------------------------
  B0    Frozen TL0 d20 parent     (via P0-T; not recomputed at U)               $2.618891$
  B1    Extra Tagalog                                  $1.468600$               $3.032277$
  B2    English continuation                           $2.492084$               $1.334322$
  B3    50/50-document mix                             $1.193565$               $1.348593$

  : Primary P3 validation cells (Gate U seal). Lower BPB is better. B0 English is descriptive only. {#tab:primary}

## Registered contrasts

$$\begin{align}
C_{\mathrm{tl}}&=2.492084-1.468600=1.023484\ge 0.01 &&\text{\textbf{observed}},\\
G_{\mathrm{en}}&=1.334322-3.032277=-1.697955\le -0.01 &&\text{\textbf{observed}}.
\end{align}$$ Trade-off contrasts (not success criteria; B3 is not mitigation): $$\begin{align}
C_{\mathrm{tl}}(B3)&=\mathrm{TL}(B3)-\mathrm{TL}(B1)=-0.275035,\\
G_{\mathrm{en}}(B3)&=\mathrm{EN}(B3)-\mathrm{EN}(B1)=-1.683684.
\end{align}$$ In this apparatus, English continuation raised Tagalog BPB relative to extra Tagalog by more than the $0.01$ cutoff, and lowered English BPB relative to extra Tagalog by more than the $0.01$ cutoff. B3 improved Tagalog relative to B1 while remaining near B2 on English; that pattern is reported as a trade-off coordinate, not as mitigation of the primary contrast.

## Secondary B2-only tests

After the validation seal, one authorized Gate V event on B2 only scored English test BPB $1.357842$ and Tagalog legacy-holdout BPB $2.493197$ under the P3 Tagalog BPE. These are secondary legacy/external holdout outcomes. They are not a test-set $C_{\mathrm{tl}}$/$G_{\mathrm{en}}$, do not alter the sealed contrasts, and must not be confused with P1.1's native-BPE `test_bpb` or with P2 Gate V numbers (explicit non-reuse in Section [6.3](#sec:nonreuse){reference-type="ref" reference="sec:nonreuse"}).

# Discussion {#sec:discussion}

## What is claimed

Within this one-seed, fixed-parent, fixed-budget, P3-tokenizer apparatus, both filed primary directional patterns were observed. The study supports a narrow causal claim about the registered English-versus-extra-Tagalog continuation streams after a P0-T-cleared Tagalog parent.

## What is not claimed

The paper does not claim a universal catastrophic-forgetting law, a population effect, a chat/SFT system, a CORE score, that "deeper is better," that B3 mitigates forgetting, or that P3 confirms P2. Gaps below $0.01$ BPB would not have been ranked; here both primary gaps exceed the cutoff with the filed signs.

## Explicit non-reuse of prior confirmatory numbers {#sec:nonreuse}

Do *not* cite P1.1 native-BPE `test_bpb`=$1.164768$ as a P3 result. Do *not* cite P2 Gate V English or Tagalog test BPB as P3 outcomes. P3 confirmatory numbers are only the sealed Gate U `val_bpb_full` cells, the filed $C_{\mathrm{tl}}$/$G_{\mathrm{en}}$ contrasts, and the one authorized Gate V B2-only secondary pair under the P3 tokenizer ($1.357842$ EN / $2.493197$ TL).

## Post-P2 honesty

Because P3 was designed after P2 unblinding, carry-forward budget and cutoff choices are mechanical relative to the P2 apparatus but are not outcome-independent discoveries. Public narratives must retain that disclosure [@aspredicted307342].

## Limitations

One seed; Wikipedia-domain text; BOS-best-fit packing crops long documents; reconstructed Tagalog split (original 2019 files unrecovered); no human evaluation; Gate S required a documented clean restart after missing English data; qualitative generation samples, if ever shown, are nonconfirmatory.

# Conclusion {#sec:conclusion}

P3 is a preregistered, post-P2 reverse-direction nanochat continual-pretraining study. Fresh Tagalog TL0 parents cleared P0-T; B0 was frozen; B1/B2/B3 continued under equal budget; validation was sealed before one B2-only secondary test touch. Gate X released $C_{\mathrm{tl}}=1.023484$ (**observed**) and $G_{\mathrm{en}}=-1.697955$ (**observed**). The contribution is the locked reverse-direction measurement, not a general bilingual forgetting theorem.

# Novelty statement {#novelty-statement .unnumbered}

The paper replaces an informal "continue Tagalog nanochat on English" story with a filed reverse-direction design: fresh P3 weights and tokenizer, P0-T before English children, matched B1/B2/B3 budgets, sealed dual-language BPB, and explicit post-P2 disclosure. Empirically, both primary filed patterns were observed in this one-seed apparatus.

# Availability {#availability .unnumbered}

- AsPredicted #307342: <https://aspredicted.org/wd2pc8.pdf>

- ResearchBox #8834: <https://researchbox.org/8834>

- AsCollected: <https://ascollected.org/F36_C2C>

- GitHub: <https://github.com/pageman/nanochat-filipino>\
  P3-only trees: `scripts/p3/`, `docs/p3/`, `docs/papers/p3-reverse/`, `docs/run-cards/p3/`, `results/p3/`, `docs/hub/p3-tl-then-en/`

- Hub: <https://huggingface.co/pageman/nanochat-filipino-p3-tl-then-en>\
  (B0+B1+B2+B3 together; not on P1.1/P2 Hub repos)

Held-out test text is not redistributed. Secrets and host credentials are not published.

# Ethics {#ethics .unnumbered}

Public Wikipedia-derived corpora. No human-subjects experiment. Secrets (host credentials, box passcodes) are not published. Cheng is not a coauthor.

# Acknowledgements {#acknowledgements .unnumbered}

Thanks to Manus 1.6 and Cursor.com(Auto) for the drafting, formatting, and solutioning of the paper. WikiText-TL-39 is due to Cruz and Cheng [@cruz2019eval]. WikiText-103 is due to Merity et al. [@merity2017pointer]. nanochat is due to Karpathy [@karpathy2026nanochat]. Errors remain the author's.

# Funding {#funding .unnumbered}

No dedicated grant. GPU time (Runpod A40) was paid by the author.

# Artifact hashes (prefixes OK in body; full here) {#app:hashes}

Body text uses 8-character prefixes. Full SHA-256 digests:

::: flushleft
AsPredicted PDF\
\
Protocol at filing\
\
Tokenizer .pkl\
\
B0 / B1 / B2 / B3 model_000294.pt\
\
\
\
\
B3 mix-order\
\
TL train / val / test manifests\
\
\
\
EN val / test manifests\
\
:::

::: thebibliography
99

P. Pajo. Equal-exposure depth and held-out Tagalog bits-per-byte on WikiText-TL-39. August 2026. <https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39>.

P. Pajo. Held-out English bits-per-byte after matched-budget Tagalog continuation of a WikiText-103 nanochat parent. August 2026. AsPredicted #306935 / ResearchBox #8763.

P. Pajo. NANOCHAT-FILIPINO P1.1: WikiText-TL-39 fixed-budget depth vs held-out BPB. AsPredicted #306780, 15 August 2026. <https://aspredicted.org/6r6v4v.pdf>.

P. Pajo. P2: EN retention after TL continuation (nanochat, WikiText-103 then TL-39). AsPredicted #306935, 17 August 2026. <https://aspredicted.org/xa56bs.pdf>.

P. Pajo. P3: TL retention after EN continuation (nanochat, TL-39 then WikiText-103). AsPredicted #307342, 19 August 2026. <https://aspredicted.org/wd2pc8.pdf>.

J. C. B. Cruz and C. Cheng. Evaluating language model finetuning techniques for low-resource languages. *arXiv:1907.00409*, 2019.

S. Merity, C. Xiong, J. Bradbury, and R. Socher. Pointer sentinel mixture models. *ICLR*, 2017.

A. Karpathy. nanochat. . <https://github.com/karpathy/nanochat>.

H. Shi et al. Continual learning of large language models: A comprehensive survey. *arXiv:2404.16789*, 2024.

Y. Luo et al. An empirical study of catastrophic forgetting in large language models during continual fine-tuning. *arXiv:2308.08747*, 2023.

V. V. Ramasesh, A. Lewkowycz, and E. Dyer. Effect of scale on catastrophic forgetting in neural networks. *ICLR*, 2022.

M. McCloskey and N. J. Cohen. Catastrophic interference in connectionist networks: The sequential learning problem. *Psychology of Learning and Motivation*, 24:109--165, 1989.

R. M. French. Catastrophic forgetting in connectionist networks. *Trends in Cognitive Sciences*, 3(4):128--135, 1999.

J. Kaplan et al. Scaling laws for neural language models. *arXiv:2001.08361*, 2020.

J. Hoffmann et al. Training compute-optimal large language models. *NeurIPS*, 2022.

N. Muennighoff et al. Scaling data-constrained language models. *NeurIPS*, 2023.

C. E. Shannon. Prediction and entropy of printed English. *Bell System Technical Journal*, 30(1):50--64, 1951.

T. Brown et al. Language models are few-shot learners. *NeurIPS*, 2020.

B. A. Nosek et al. The preregistration revolution. *PNAS*, 115(11):2600--2606, 2018.

E.-J. Wagenmakers et al. An agenda for purely confirmatory research. *Perspectives on Psychological Science*, 7(6):632--638, 2012.
:::
