**Keywords:** schedule topology; block order; token budget; Tagalog; English; bits-per-byte; nanochat; preregistration; post-P5; one seed.

**arXiv categories:** cs.CL, cs.LG.

**Registration and deposits (P6-M):**

- AsPredicted #307969: <https://aspredicted.org/bk6m9d.pdf>

- ResearchBox #8918 (<https://researchbox.org/8918>; FOR PEER REVIEW, not Make Public)

- AsCollected #2541 Version 1:\
  <https://ascollected.org/XZ8_TI5>\
  (project `NANOCHAT-FILIPINO P6-M`; linked from box #8918)

- Study record: <https://github.com/pageman/nanochat-filipino/tree/main/docs/p6>

- GitHub trees under <https://github.com/pageman/nanochat-filipino>:\
  `scripts/p6/`, `docs/papers/p6-m-schedule-topology/`,\
  `docs/run-cards/p6/`, `manifests/p6/`, `results/p6/`,\
  `docs/hub/p6-m-schedule-topology/`

- Hub: <https://huggingface.co/pageman/nanochat-filipino-p6-m-schedule-topology>\
  (uploaded commit `5d3872b0`; C0/C1/C2/tokenizer original; four topology children technical recreate)

- Run ID: `p6-20260824T155226Z-769f807a`. Manuscript version: v1.1.

# Introduction {#sec:intro}

Pajo [@pajo2026p11] measured equal-exposure Tagalog BPB across nanochat depths on WikiText-TL-39 (AsPredicted #306780). Pajo [@pajo2026p2] asked the forward continual-pretraining question from an English parent (AsPredicted #306935). Pajo [@pajo2026p3] asked the reverse from a fresh Tagalog parent (AsPredicted #307342). Pajo [@pajo2026p4] locked source-content token share at $q_{\mathrm{TL}}=0.50$ after a fresh Tagalog parent (AsPredicted #307591). Pajo [@pajo2026p5] counted how often that frozen mix recurred on three unused initializations (AsPredicted #307836).

P6-M was designed after those released P1.1--P5 findings were known. It is therefore a prospectively preregistered **post-P5** schedule-topology mechanism study [@aspredicted307969]. It is not an amendment, correction, rescue, replication, or independent confirmation of P4 or P5. It does not treat recurrence counts as primary. It holds the P4 token-share bundle fixed and varies only the filed block schedules.

The confirmatory question, locked before any P6 confirmatory BPB existed, is:

> After a newly trained seed-4 Tagalog parent passes P0-T, freeze d20 as C0 and continue it for one shared phase-two token budget on C1, C2, and four mixed topologies that share identical within-language streams and exact per-language quotas. Relative to M-fine, how do M-coarse, M-blocked, and M-rand classify on Tagalog and English validation BPB at $\delta=0.01$?

This paper contributes: (i) one eligible seed-4 Tagalog parent frozen as C0; (ii) six sibling children under a fixed token budget; (iii) a sealed twelve-cell validation matrix before one M-fine-only secondary test; (iv) one Gate X release whose primary result is the six primary $\Delta$TL/$\Delta$EN classifications versus M-fine.

# Related work {#sec:related}

Cruz and Cheng constructed WikiText-TL-39 [@cruz2019eval]. Sequential interference is classical [@mccloskey1989catastrophic; @french1999cf]. LLM continual-pretraining work often continues an English or multilingual base [@luo2023forgetting; @ramasesh2021forgetscale; @shi2024continual]. P6-M stays inside WikiText-family text, the nanochat depth dial, and BPB rather than CORE or chat [@karpathy2026nanochat]. Equal token budgets follow the family so stream identity is not confounded with compute [@kaplan2020scaling; @hoffmann2022chinchilla; @muennighoff2023dataconstrained]. WikiText established clean Wikipedia LM evaluation in English [@merity2017pointer]. BPB remains comparable across vocabularies [@shannon1951prediction; @brown2020gpt3]. Official P6 BPB is mean token NLL divided by $\ln 2$ times mean UTF-8 bytes per token, full split, $T=2048$, BOS-best-fit. In-loop trainer BPB is not confirmatory. Preregistration reduces undisclosed flexibility [@nosek2018prereg; @wagenmakers2012confirmatory]. Curriculum learning motivates asking whether presentation order matters when exposure totals are locked [@bengio2009curriculum]; surveys of continual LLM training likewise treat schedule and interference as open mechanism questions [@shi2024continual]. P6-M answers the block-order question only inside this one-seed BPB apparatus. WikiText-TL-39 is a Cruz--Cheng resource lineage; this study is not an extension of Cheng catastrophic-forgetting methods and does not assess downstream Filipino tasks [@cruz2020degradation].

# Methods {#sec:methods}

## Registration and authority

AsPredicted #307969 governs [@aspredicted307969].

- PDF: <https://aspredicted.org/bk6m9d.pdf>

- PDF SHA-256:\
  [769f807a00264a996b02c38b83ee2cf6c23c4981e36fb477dfc1959fa918a1e7](769f807a00264a996b02c38b83ee2cf6c23c4981e36fb477dfc1959fa918a1e7){.uri}

- Prefiling addendum SHA-256:\
  [df49664809ada69d23dcd2c799e75b30f0fdb9afd7aee12b071ac24ef2f81082](df49664809ada69d23dcd2c799e75b30f0fdb9afd7aee12b071ac24ef2f81082){.uri}

- Unmodified gate-plan SHA-256:\
  [d8a63608608c59d2c4d9882e5346625462056c331094942a8a01d496697a1c79](d8a63608608c59d2c4d9882e5346625462056c331094942a8a01d496697a1c79){.uri}

- Topology-manifest SHA-256:\
  [d1e7d5af7247a572e319ee003b5f4e3da5d1fb1592e5ed9ff6b22eeec15ea606](d1e7d5af7247a572e319ee003b5f4e3da5d1fb1592e5ed9ff6b22eeec15ea606){.uri}

Authority order: filed PDF $\gg$ SHA-bound addendum $\gg$ unmodified gate plan $\gg$ `LOCK.json`, manifests, and deterministic receipts $\gg$ this manuscript (v1.1). The study does not amend #306780, #306935, #307342, #307591, or #307836. ResearchBox #8918 remains FOR PEER REVIEW and is not made public by this paper. AsCollected #2541 Version 1 (<https://ascollected.org/XZ8_TI5>) records public-corpus provenance and is linked from the box. Hub weights were uploaded after Gate W with independent remote re-hash; the four topology children on Hub are a technical recreate (new SHAs), while C0, C1, C2, and the tokenizer pair remain the original study artifacts.

## Sources, tokenizer, and hosts

Tagalog train/val/test documents are the frozen WikiText-TL-39 P1.1-eligible splits. English train/val/test documents are the frozen WikiText-103 P2-eligible splits. The tokenizer is the carry-forward P4 pair: `tokenizer.pkl` [04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8](04436b854e0841025a3dd2b46baaeeea07a7ccc252e9f99a19171306f00bc5a8){.uri} and `token_bytes.pt` [a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132](a5dbc1c88f6292696108263072d77115718cc2d8357f7ad4859adfa517cc2132){.uri}. P1.1--P5 weights were not loaded as parents. Official GPU gates used NVIDIA CUDA A40. Official evaluation used `scripts/p6/evaluate_bpb.py` with formula-equivalent hash [a22a566b71ac9b768543e052e78576f6b079d5c88066f3ec2f8bfef600e17481](a22a566b71ac9b768543e052e78576f6b079d5c88066f3ec2f8bfef600e17481){.uri}.

## Parent, P0-T, and C0 freeze

Parent-initialization seed is exactly $s=4$. After P0-T PASS, d20 was copied to an immutable C0 directory with `additional_train_tokens`=0. C0 SHA-256: [7fbd24de792aa4ee27d841866db2114e0fb45b1fdcaa4edcc9b24582220123c9](7fbd24de792aa4ee27d841866db2114e0fb45b1fdcaa4edcc9b24582220123c9){.uri}. Smoke and d8 checkpoints are not C0.

## Children and fixed topology treatments

C1, C2, M-fine, M-coarse, M-blocked, and M-rand each continued the same frozen C0 for $N=294$ steps with $B=65{,}536$ and $D_{\mathrm{phase2}}=19{,}267{,}584$ tokens. Launches were serial R$\to$S$\to$T1--T4 with `load_optimizer=False`, child peak learning rate $0.3\times$ the parent peak, warmup 14, and terminal checkpoint only. Mixed arms share identical within-language streams and stored no-wrap schedules:

- **M-fine:** EN-first alternating blocks of $2{,}048$ tokens ($4{,}704$ blocks per language).

- **M-coarse:** EN-first alternating blocks of $1{,}204{,}224$ tokens (eight blocks per language).

- **M-blocked:** all Tagalog then all English (one block per language).

- **M-rand:** one precomputed shuffle of $4{,}704$ EN and $4{,}704$ TL blocks of length $2{,}048$, shuffled once with Python `random.Random(42)` and hash-pinned before filing.

Each mixed arm uses exactly $9{,}633{,}792$ Tagalog and $9{,}633{,}792$ English source-content tokens. Mix-manifest SHA-256:\
[f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107](f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107){.uri}.

## Lockbox, analysis, and tests

Validation BPB was lockboxed until one Gate X. Gate U sealed twelve child cells (six conditions $\times$ two languages) with `test_access`=0. Policy A authorized exactly one M-fine-only secondary restricted-test event after U (Gate V). C1, C2, M-coarse, M-blocked, and M-rand were not tested. Primary contrasts use sealed validation cells; tests are secondary and excluded from topology classification. Equality outside $(-\delta,+\delta)$ at $\delta=0.01$ defines directional classes. No composite score, mean, confidence interval, $p$-value, across-seed average, or P5-style recurrence count.

# Results {#sec:results}

P0-T status is **PASS** for seed 4. All six children completed with reload-verified terminal checkpoints. Table [1](#tab:cells){reference-type="ref" reference="tab:cells"} reports the sealed twelve validation cells and descriptive C0 English. Table [2](#tab:primary){reference-type="ref" reference="tab:primary"} reports the six primary contrasts versus M-fine. Table [3](#tab:contextual){reference-type="ref" reference="tab:contextual"} reports contextual $R_{\mathrm{TL}}$ and $A_{\mathrm{EN}}$ for the four mixed topologies.

  Arm                   Tagalog val BPB   English val BPB
  -------------------- ----------------- -----------------
  C0 (frozen parent)          ---           $2.683814$
  C1 extra Tagalog        $0.564548$        $2.892551$
  C2 pure English         $2.219915$        $1.269724$
  M-fine                  $1.256292$        $1.440084$
  M-coarse                $1.214675$        $1.487389$
  M-blocked               $1.458898$        $1.529111$
  M-rand                  $1.257379$        $1.441159$

  : Full-split validation BPB after terminal d20 checkpoints. Six-decimal reporting as filed. C0 English is descriptive and excluded from topology classification. {#tab:cells}

  $\tau$       $\Delta$TL         TL class        $\Delta$EN       EN class
  ----------- ------------- -------------------- ------------ -------------------
  M-coarse     $-0.041617$   better by $\delta$   $0.047305$   worse by $\delta$
  M-blocked    $0.202606$    worse by $\delta$    $0.089027$   worse by $\delta$
  M-rand       $0.001087$     within $\delta$     $0.001075$    within $\delta$

  : Primary contrasts versus M-fine at $\delta=0.01$. $\Delta=\mathrm{BPB}(M\textrm{-}\tau)-\mathrm{BPB}(\textrm{M-fine})$. Lower BPB is better. Class labels: better/worse than M-fine by $\delta$, or within $\delta$. {#tab:primary}

  $\tau$       $R_{\mathrm{TL}}$   $A_{\mathrm{EN}}$
  ----------- ------------------- -------------------
  M-fine          $-0.963623$         $-1.452467$
  M-coarse        $-1.005239$         $-1.405162$
  M-blocked       $-0.761016$         $-1.363439$
  M-rand          $-0.962536$         $-1.451392$

  : Contextual contrasts (descriptive secondary). $R_{\mathrm{TL}}=\mathrm{TL}(M\textrm{-}\tau)-\mathrm{TL}(\mathrm{C2})$; $A_{\mathrm{EN}}=\mathrm{EN}(M\textrm{-}\tau)-\mathrm{EN}(\mathrm{C1})$. {#tab:contextual}

Under this preregistered fixed-budget schedule comparison, M-rand was within $\delta$ of M-fine on both languages; M-blocked was worse than M-fine by more than $\delta$ on both languages; M-coarse was better than M-fine on Tagalog and worse on English, each by more than $\delta$. This is a one-seed topology classification, not a confidence interval, not a population effect, and not a P5 recurrence count. P6-M does not amend #307591 or #307836.

One authorized M-fine-only secondary test event reported English test BPB $1.450423$ and Tagalog test BPB $1.260475$. Tests do not alter sealed contrasts and are not co-primary.

# Discussion {#sec:disc}

With token share held fixed, block order was not inert in this apparatus: coarse interleaving and complete blocking moved validation BPB relative to fine EN-first alternation, while a once-shuffled random block sequence stayed within $\delta$ of M-fine. That pattern is a mechanism observation under a frozen P4-style quota bundle, not a claim that M-fine is optimal, not a general forgetting-mitigation result, and not a law across seeds. Contextual $R_{\mathrm{TL}}$ and $A_{\mathrm{EN}}$ place each mixed arm relative to C2 and C1; they are not a second topology success rule. WikiText-TL-39 remains a Cruz--Cheng resource lineage; P6-M does not extend Cheng catastrophic-forgetting protocols and does not claim downstream Filipino-task or all-Philippine-language benefit.

# Limitations {#sec:limit}

One seed; one tokenizer; WikiText-family text only; no chat, SFT, CORE, FilBench, or larger-model transfer. Confirmatory GPU work used a rented NVIDIA A40. Raw test JSONL remains restricted. Hub weights ship C0+C1+C2+all four topology children together with tokenizer and meta; never overwrite P4/P5 Hub IDs. The Hub topology children are a post-loss technical recreate and are not bitwise identical to the original Gate T terminals that produced the sealed BPB table. Document-revisit (P7-M), optimizer-state (P8-M), replay/protection, and tokenizer/transfer studies remain separate filings.

# Deviations {#sec:dev}

No protocol stop. No break-glass. No additional confirmatory validation or test eval after Gate X. Gate S attempt 1 failed as a *preflight* block when the C2 English packed stream was missing on the pod path ($checkpoint\_sha256=\texttt{null}$); after syncing the filed stream, one clean authorized C2 launch completed. M-rand wrote a valid terminal model checkpoint, then hit ENOSPC during optimizer save; the terminal model was hash- and reload-verified and accepted without retraining (`technical_accept=true`). Gate 0 had pinned a P5-rename unblind script hash that reads `c3_*` cells and emits recurrence counts; Gate U wrote topology-named cells, so Gate X executed a topology-contrast script under filed-analysis authority. The script-hash mismatch is documented in the unblinding event; the filed primary remains $\Delta$TL/$\Delta$EN versus M-fine. Frozen English train JSONL contains intra-split duplicate rows ($28{,}472$ rows / $28{,}232$ unique); they were not dropped. Cross-split overlap was 0. After Gate W, original Gate T topology terminals were lost from the sticky study volume; under separate authorization, M-fine/M-coarse/M-blocked/M-rand were technically recreated for Hub deposit only (new SHAs). Science claims remain Gate X / filed Gate T receipts.

# Availability {#availability .unnumbered}

- AsPredicted #307969: <https://aspredicted.org/bk6m9d.pdf>

- Study record (GitHub):\
  <https://github.com/pageman/nanochat-filipino/tree/main/docs/p6>\
  Paper tree: <https://github.com/pageman/nanochat-filipino/tree/main/docs/papers/p6-m-schedule-topology>

- Code and audit trees (GitHub): <https://github.com/pageman/nanochat-filipino>\
  P6-only: `scripts/p6/`, `docs/papers/p6-m-schedule-topology/`,\
  `docs/run-cards/p6/`, `manifests/p6/`, `results/p6/`,\
  `docs/hub/p6-m-schedule-topology/`

- Weights (Hugging Face Hub):\
  <https://huggingface.co/pageman/nanochat-filipino-p6-m-schedule-topology>\
  Uploaded commit `5d3872b0`; topology children technical recreate; never write onto P4/P5 Hub IDs.

- ResearchBox #8918: <https://researchbox.org/8918>\
  (FOR PEER REVIEW; not Make Public).

- AsCollected #2541 Version 1: <https://ascollected.org/XZ8_TI5>\
  (project `NANOCHAT-FILIPINO P6-M`; linked from box #8918).

Held-out test text is not redistributed. Host credentials are not published. GitHub holds protocol, receipts, sealed/released JSON, and paper; Hugging Face holds the weight bundle after independent remote re-hash.

# Ethics {#ethics .unnumbered}

Public Wikipedia-derived corpora. No human-subjects experiment. ResearchBox #8918 remains passcode-protected for peer review until explicitly made public.

# Acknowledgements {#acknowledgements .unnumbered}

Thanks to Manus 1.6 and Cursor.com(Auto) for the drafting, formatting, and solutioning of the paper. WikiText-TL-39 is due to Cruz and Cheng [@cruz2019eval]. WikiText-103 is due to Merity et al. [@merity2017pointer]. nanochat is due to Karpathy [@karpathy2026nanochat]. Errors remain the author's.

# Funding {#funding .unnumbered}

No dedicated grant. GPU time (Runpod A40) was paid by the author.

# Selected hashes {#app:hashes}

- Pin / nanochat:\
  [92d63d4e8bb4df75c3b71618f31ddde2378b2bcd](92d63d4e8bb4df75c3b71618f31ddde2378b2bcd){.uri}

- AsPredicted PDF:\
  [769f807a00264a996b02c38b83ee2cf6c23c4981e36fb477dfc1959fa918a1e7](769f807a00264a996b02c38b83ee2cf6c23c4981e36fb477dfc1959fa918a1e7){.uri}

- Gate plan:\
  [d8a63608608c59d2c4d9882e5346625462056c331094942a8a01d496697a1c79](d8a63608608c59d2c4d9882e5346625462056c331094942a8a01d496697a1c79){.uri}

- Addendum:\
  [df49664809ada69d23dcd2c799e75b30f0fdb9afd7aee12b071ac24ef2f81082](df49664809ada69d23dcd2c799e75b30f0fdb9afd7aee12b071ac24ef2f81082){.uri}

- Topology manifest:\
  [d1e7d5af7247a572e319ee003b5f4e3da5d1fb1592e5ed9ff6b22eeec15ea606](d1e7d5af7247a572e319ee003b5f4e3da5d1fb1592e5ed9ff6b22eeec15ea606){.uri}

- Mix manifest:\
  [f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107](f203c615266bc8c33c358c1de397715791cae33536a9743c8a6bf8cd543cb107){.uri}

- Evaluator (P6 path):\
  [a22a566b71ac9b768543e052e78576f6b079d5c88066f3ec2f8bfef600e17481](a22a566b71ac9b768543e052e78576f6b079d5c88066f3ec2f8bfef600e17481){.uri}

- C0 (original / Hub):\
  [7fbd24de792aa4ee27d841866db2114e0fb45b1fdcaa4edcc9b24582220123c9](7fbd24de792aa4ee27d841866db2114e0fb45b1fdcaa4edcc9b24582220123c9){.uri}

- C1 / C2 (original / Hub):\
  [6223c116779ce3128c1e4cae0f2e03744b3068169ad7bb88f75a5146671a99bd](6223c116779ce3128c1e4cae0f2e03744b3068169ad7bb88f75a5146671a99bd){.uri}\
  [04c06c195e513c7b30752637b80591c29e740879d91c35c323fb75fafca8747d](04c06c195e513c7b30752637b80591c29e740879d91c35c323fb75fafca8747d){.uri}

- M-fine / M-coarse / M-blocked / M-rand (original Gate T; science):\
  [a0139607a8fdf2772d4b8e722b449b6a8db04056a8dc38cd177708af8f15eeab](a0139607a8fdf2772d4b8e722b449b6a8db04056a8dc38cd177708af8f15eeab){.uri}\
  [86588ee9f72ea4a85a821c2c882a363d55d3e50ccb325bdabaa0706e1e911dfe](86588ee9f72ea4a85a821c2c882a363d55d3e50ccb325bdabaa0706e1e911dfe){.uri}\
  [5ec45216eb0a09b5bc04f04f4622d85f7d8f7ff8861fdea6de5487f7c18fa526](5ec45216eb0a09b5bc04f04f4622d85f7d8f7ff8861fdea6de5487f7c18fa526){.uri}\
  [38580cd501c0d87a1a502397697f7c7e427134eb7cb64bdce2ba6be1a036f108](38580cd501c0d87a1a502397697f7c7e427134eb7cb64bdce2ba6be1a036f108){.uri}

- M-fine / M-coarse / M-blocked / M-rand (Hub technical recreate):\
  [69a5046ee756faba84f0f5e9c6a0f1330f886f9dd0344f02797798d1d2d0bfe7](69a5046ee756faba84f0f5e9c6a0f1330f886f9dd0344f02797798d1d2d0bfe7){.uri}\
  [c09072fe764f1debd9607f697e2aa8484ef394a96d2ef096f05bb1f0d6c518f7](c09072fe764f1debd9607f697e2aa8484ef394a96d2ef096f05bb1f0d6c518f7){.uri}\
  [ebfc4853b51cc8c81480ffb57640487d3fe344d38ec51ad5bb1eb7cf159272d2](ebfc4853b51cc8c81480ffb57640487d3fe344d38ec51ad5bb1eb7cf159272d2){.uri}\
  [16f6679310c379ce2403e587620eb0ef7d162d6e92ddfc9589d272915eff981d](16f6679310c379ce2403e587620eb0ef7d162d6e92ddfc9589d272915eff981d){.uri}

- U seal:\
  [23f9a94483532f5b7d51f4a27f77436cafd440f30c11fac5e0ea2dfa0aa095ae](23f9a94483532f5b7d51f4a27f77436cafd440f30c11fac5e0ea2dfa0aa095ae){.uri}

- Released contrasts:\
  [d376643af19969f2ee127afcc4696de3a4821c8188fa6e7003d190d5f4031911](d376643af19969f2ee127afcc4696de3a4821c8188fa6e7003d190d5f4031911){.uri}

# GitHub versus Hugging Face {#app:split}

GitHub `pageman/nanochat-filipino` is the study record: scripts, paper, lock, ledgers, run-card receipts, sealed/released JSON, and Hub documentation. Hugging Face hosts the weight deposit at <https://huggingface.co/pageman/nanochat-filipino-p6-m-schedule-topology> (C0+C1+C2+topology children plus tokenizer and evaluation JSON; uploaded; topology children technical recreate). Never a single topology child alone. Never write onto prior Hub IDs (P1.1, P2, P3, P4, or P5). Raw test JSONL, passcodes, SSH keys, optimizer states, and HOST operator cards belong in neither public tree.

::: thebibliography
99

P. Pajo. Equal-exposure depth and held-out Tagalog bits-per-byte on WikiText-TL-39. AsPredicted #306780, 2026.

P. Pajo. Held-out English bits-per-byte after matched-budget Tagalog continuation of a WikiText-103 nanochat parent. AsPredicted #306935, 2026.

P. Pajo. Tagalog retention and English acquisition under equal-budget nanochat continual pretraining. AsPredicted #307342, 2026.

P. Pajo. Token-share-locked English--Tagalog mixtures after a fresh Tagalog parent. AsPredicted #307591, 2026.

P. Pajo. How often a frozen mix recurs across unused initializations: a closed three-seed count, not a population estimate. AsPredicted #307836, 2026.

AsPredicted #307969. P6-M: schedule topology under a frozen English--Tagalog token-share bundle. <https://aspredicted.org/bk6m9d.pdf>, 2026.

J. C. B. Cruz and C. Cheng. Evaluating Filipino linguistic resources. .

J. C. B. Cruz and C. Cheng. Establishing baselines for text classification in low-resource languages. *arXiv:2005.02068*, 2020. Discussion-only robustness analogy for P6-M; not the BPB schedule-topology estimand.

A. Karpathy. nanochat. <https://github.com/karpathy/nanochat>, 2026.

S. Merity, C. Xiong, J. Bradbury, and R. Socher. Pointer sentinel mixture models. *ICLR*, 2017.

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

Y. Bengio, J. Louradour, R. Collobert, and J. Weston. Curriculum learning. *ICML*, 2009.
:::
