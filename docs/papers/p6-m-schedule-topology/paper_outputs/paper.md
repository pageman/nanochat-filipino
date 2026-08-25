**Keywords:** schedule topology; block order; token budget; Tagalog; English; bits-per-byte; nanochat; preregistration; post-P5; one seed.

**arXiv categories:** cs.CL, cs.LG.

**Registration and deposits (P6-M):** AsPredicted #307969 (<https://aspredicted.org/bk6m9d.pdf>); study record <https://github.com/pageman/nanochat-filipino/tree/main/docs/papers/p6-m-schedule-topology>; GitHub trees `scripts/p6/`, `docs/run-cards/p6/`, `manifests/p6/`, `docs/hub/p6-m-schedule-topology/` under <https://github.com/pageman/nanochat-filipino>; provisional Hub ID `pageman/nanochat-filipino-p6-m-schedule-topology` (upload deferred). ResearchBox and AsCollected deposit IDs are deferred at Gate W closeout. Run ID: `p6-20260824T155226Z-769f807a`. Manuscript version: v1.0.

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

- Prefiling addendum SHA-256:\

- Unmodified gate-plan SHA-256:\

- Topology-manifest SHA-256:\

Authority order: filed PDF $\gg$ SHA-bound addendum $\gg$ unmodified gate plan $\gg$ `LOCK.json`, manifests, and deterministic receipts $\gg$ this manuscript (v1.0). The study does not amend #306780, #306935, #307342, #307591, or #307836. ResearchBox and Hub uploads were deferred at Gate W; local archive and paper hashes are recorded in the run-card closeout.

## Sources, tokenizer, and hosts

Tagalog train/val/test documents are the frozen WikiText-TL-39 P1.1-eligible splits. English train/val/test documents are the frozen WikiText-103 P2-eligible splits. The tokenizer is the carry-forward P4 pair: `tokenizer.pkl` and `token_bytes.pt` . P1.1--P5 weights were not loaded as parents. Official GPU gates used NVIDIA CUDA A40. Official evaluation used `scripts/p6/evaluate_bpb.py` with formula-equivalent hash .

## Parent, P0-T, and C0 freeze

Parent-initialization seed is exactly $s=4$. After P0-T PASS, d20 was copied to an immutable C0 directory with `additional_train_tokens`=0. C0 SHA-256: . Smoke and d8 checkpoints are not C0.

## Children and fixed topology treatments

C1, C2, M-fine, M-coarse, M-blocked, and M-rand each continued the same frozen C0 for $N=294$ steps, $B=65{,}536$, $D_{\mathrm{phase2}}=19{,}267{,}584$ tokens, serial R$\to$S$\to$T1--T4, `load_optimizer=False`, child peak learning rate $0.3\times$ the parent peak, warmup 14, terminal checkpoint only. Mixed arms share identical within-language streams and stored no-wrap schedules:

- **M-fine:** EN-first alternating blocks of $2{,}048$ tokens ($4{,}704$ blocks per language).

- **M-coarse:** EN-first alternating blocks of $1{,}204{,}224$ tokens (eight blocks per language).

- **M-blocked:** all Tagalog then all English (one block per language).

- **M-rand:** one precomputed shuffle of $4{,}704$ EN and $4{,}704$ TL blocks of length $2{,}048$, shuffled once with Python `random.Random(42)` and hash-pinned before filing.

Each mixed arm uses exactly $9{,}633{,}792$ Tagalog and $9{,}633{,}792$ English source-content tokens. Mix-manifest SHA-256: .

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

  $\tau$       $\Delta$TL               TL class              $\Delta$EN             EN class
  ----------- ------------- -------------------------------- ------------ -------------------------------
  M-coarse     $-0.041617$   better than M-fine by $\delta$   $0.047305$   worse than M-fine by $\delta$
  M-blocked    $0.202606$    worse than M-fine by $\delta$    $0.089027$   worse than M-fine by $\delta$
  M-rand       $0.001087$           within $\delta$           $0.001075$          within $\delta$

  : Primary contrasts versus M-fine at $\delta=0.01$. $\Delta=\mathrm{BPB}(M\textrm{-}\tau)-\mathrm{BPB}(\textrm{M-fine})$. Lower BPB is better. {#tab:primary}

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

One seed; one tokenizer; WikiText-family text only; no chat, SFT, CORE, FilBench, or larger-model transfer. Confirmatory GPU work used a rented NVIDIA A40. Raw test JSONL remains restricted. Hub weight release, if any, must ship C0+C1+C2+topology children together with tokenizer and meta; never overwrite P4/P5 Hub IDs. Document-revisit (P7-M), optimizer-state (P8-M), replay/protection, and tokenizer/transfer studies remain separate filings.

# Deviations {#sec:dev}

No protocol stop. No break-glass. No additional confirmatory validation or test eval after Gate X. Gate S attempt 1 failed as a *preflight* block when the C2 English packed stream was missing on the pod path ($checkpoint\_sha256=\texttt{null}$); after syncing the filed stream, one clean authorized C2 launch completed. M-rand wrote a valid terminal model checkpoint, then hit ENOSPC during optimizer save; the terminal model was hash- and reload-verified and accepted without retraining (`technical_accept=true`). Gate 0 had pinned a P5-rename unblind script hash that reads `c3_*` cells and emits recurrence counts; Gate U wrote topology-named cells, so Gate X executed a topology-contrast script under filed-analysis authority. The script-hash mismatch is documented in the unblinding event; the filed primary remains $\Delta$TL/$\Delta$EN versus M-fine. Frozen English train JSONL contains intra-split duplicate rows ($28{,}472$ rows / $28{,}232$ unique); they were not dropped. Cross-split overlap was 0.

# Availability {#availability .unnumbered}

- AsPredicted #307969: <https://aspredicted.org/bk6m9d.pdf>

- Study record (GitHub):\
  <https://github.com/pageman/nanochat-filipino/tree/main/docs/papers/p6-m-schedule-topology>

- Code and audit trees (GitHub):\
  <https://github.com/pageman/nanochat-filipino>\
  P6-only: `scripts/p6/`, `docs/papers/p6-m-schedule-topology/`, `docs/run-cards/p6/`, `manifests/p6/`, `docs/hub/p6-m-schedule-topology/`

- Weights (Hugging Face Hub): provisional ID\
  <https://huggingface.co/pageman/nanochat-filipino-p6-m-schedule-topology>\
  (upload deferred at Gate W; never write onto P4/P5 Hub IDs).

- ResearchBox / AsCollected: deferred at Gate W closeout.

Held-out test text is not redistributed. Host credentials are not published. GitHub holds protocol, receipts, sealed/released JSON, and paper; Hugging Face is reserved for optional weight bundles after independent remote re-hash.

# Ethics {#ethics .unnumbered}

Public Wikipedia-derived corpora. No human-subjects experiment. Any future ResearchBox remains passcode-protected for peer review until explicitly made public.

# Acknowledgements {#acknowledgements .unnumbered}

Thanks to Manus 1.6 and Cursor.com(Auto) for the drafting, formatting, and solutioning of the paper. WikiText-TL-39 is due to Cruz and Cheng [@cruz2019eval]. WikiText-103 is due to Merity et al. [@merity2017pointer]. nanochat is due to Karpathy [@karpathy2026nanochat]. Errors remain the author's.

# Funding {#funding .unnumbered}

No dedicated grant. GPU time (Runpod A40) was paid by the author.

# Selected hashes {#app:hashes}

- Pin / nanochat:

- AsPredicted PDF:

- Gate plan:

- Addendum:

- Topology manifest:

- Mix manifest:

- Evaluator (P6 path):

- C0:

- C1 / C2: /

- M-fine / M-coarse / M-blocked / M-rand: / / /

- U seal:

- Released contrasts:

# GitHub versus Hugging Face {#app:split}

GitHub `pageman/nanochat-filipino` is the study record: scripts, paper, lock, ledgers, run-card receipts, sealed/released JSON, and Hub *documentation*. Hugging Face `pageman/nanochat-filipino-p6-m-schedule-topology` is the optional weight deposit (deferred): C0+C1+C2+topology children plus tokenizer and evaluation JSON. Never a single topology child alone. Never write onto P1.1/P2/P3/P4/P5 Hub IDs. Raw test JSONL, passcodes, SSH keys, optimizer states, and HOST operator cards belong in neither public tree.

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
