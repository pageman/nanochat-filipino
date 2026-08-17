**Keywords:** catastrophic forgetting; English retention; Tagalog acquisition; WikiText-103; WikiText-TL-39; bits-per-byte; provenance; equal-exposure; nanochat; preregistration.

**arXiv categories:** cs.CL, cs.LG.

**Status:** Stage 1. Direction recalibrated 16 August 2026. English parents and Tagalog continuation have not been run.

**P1.1 (frozen, A/P/C/L/N $=25$):** <https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39>; code <https://github.com/pageman/nanochat-filipino>; weights <https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x>.

**This study (new repos, not written onto P1.1):** `pageman/nanochat-filipino-p2-en-then-tl` on GitHub and Hugging Face.

**Direction lock:** `docs/papers/p2-cf-english/DIRECTION-RECALIBRATION.md`.

# What changed, and why P1.1 cannot be the CF parent {#sec:flip}

The question is: after English pretraining, how much English is lost when the same decoder is continued on Filipino Wikipedia text, and did it actually learn Filipino?

WikiText-TL-39 is a corpus, not a model that was "pretrained in English." English pretraining is a separate nanochat run on WikiText-103 raw [@merity2017pointer]. Filipino tuning uses the frozen P1.1 train split of WikiText-TL-39 [@cruz2019eval; @pajo2026p11].

P1.1 Hub checkpoints are a pure Tagalog speedrun [@karpathy2026nanochat; @aspredicted306780]. Using them as the CF parent would measure Tagalog retention under English data --- the opposite causal arrow. That draft is retired.

P1.1 remains the measurement instrument for Filipino and the negative control for English (a model that was *not* English-pretrained).

# Glossary {#sec:glossary}

::: description
Frozen Tagalog-from-scratch study. Not the English parent.

English-from-scratch nanochat on WikiText-103 raw. This *is* the CF parent.

Provenance battery, scored before any Tagalog training token.

Frozen EN0, dual eval (English before, Tagalog before).

Extra English continuation, $D_{\mathrm{phase2}}$ (drift).

Tagalog continuation on P1.1 train, $D_{\mathrm{phase2}}$ (CF intervention).

50/50 English/Tagalog documents, $D_{\mathrm{phase2}}$.

English `val_bpb_full`(A2)$-$`val_bpb_full`(A1). Positive: Tagalog data hurt English more than more English did.

Tagalog `val_bpb_full`(A2) versus P1.1 Table 2 (from-scratch ceiling) and versus A0 (English parent before Filipino).

After A2, English val BPB $\ge$ EN0 untrained, or $\Delta_{\mathrm{en}}\ge 1.0$ versus A0, or English val BPB no longer beats the English byte unigram. Not a $0.02$ bump.

Bits per UTF-8 byte. Fair across the English BPE and the P1.1 Tagalog BPE. Do not mix tokenizers in one training run.
:::

# P1.1 facts used as references, not as parents {#sec:p11}

Tagalog `val_bpb_full` seed 0: d8 $1.179135$, d12 $1.180824$, d16 $1.195546$, d20 $1.172248$. Untrained $\approx 3.289$; unigram $4.453225$. Split `reconstructed_article_70_15_15`. nanochat `92d63d4`. $T=2048$. One Tagalog test BPB $1.164768$ on d20; this study does not reuse it as a post-continuation number.

# Confirmatory question {#sec:question}

File a new AsPredicted before EN0 confirmatory BPB (pilots allowed). Then:

> When an English-pretrained nanochat (EN0), whose English provenance has passed P0, is continued for $D_{\mathrm{phase2}}$ tokens on WikiText-TL-39 train, does English held-out BPB rise more than under matched extra-English continuation, and does Tagalog held-out BPB fall toward the P1.1 from-scratch ceiling?

Prediction: $C_{\mathrm{en}}>0$ by at least $0.01$ BPB at the registered depths. Tagalog A2 BPB will be strictly below A0 Tagalog BPB (learning Filipino) but need not match P1.1 d20 (different tokenizer, different init). Depth rankings of $C_{\mathrm{en}}$ require the $0.01$ rule and more than one seed. P0 failure aborts A2.

# Provenance battery P0 {#sec:p0}

"Was it really pretrained in English?" is an empirical gate, not a README claim.

On a frozen English validation split, before any Tagalog train token:

1.  EN0 English `val_bpb_full` $<$ same-depth untrained.

2.  EN0 English `val_bpb_full` $<$ P1.1 d20 English `val_bpb_full` on the same UTF-8 (P1.1 Tagalog BPE), by $\ge 0.01$ BPB.

3.  EN0 Tagalog `val_bpb_full` $>$ P1.1 d20 Tagalog `val_bpb_full` (has not learned Filipino yet), by $\ge 0.01$ BPB.

4.  English-train BPE hashes recorded; train log names WikiText-103 only; no ClimbMix.

If any check fails, EN0 is not an English parent.

# Related work {#sec:related}

Catastrophic interference is sequential overwriting of old knowledge [@mccloskey1989catastrophic; @french1999cf; @goodfellow2013cf]. Typical LLM CF starts from an English (or multilingual) base and adds a new task [@luo2023forgetting; @ramasesh2021forgetscale]. This paper stays in that causal direction, but keeps P1.1's purity: WikiText-family corpora, nanochat depth dial, BPB rather than CORE [@merity2017pointer; @cruz2019eval; @karpathy2026nanochat; @pajo2026p11]. EWC and replay are later [@kirkpatrick2017ewc; @lopezpaz2017gem]. Equal-exposure arithmetic is copied from P1.1 so English pretraining is not a silent compute confound [@kaplan2020scaling; @hoffmann2022chinchilla; @muennighoff2023dataconstrained].

# Methods {#sec:methods}

## Lineage

New AsPredicted. New GitHub/Hub `pageman/nanochat-filipino-p2-en-then-tl`. P1.1 repos read-only. Authority: new PDF $>$ `DIRECTION-RECALIBRATION.md` $>$ this manuscript $>$ ledger $>$ deviation.

## nanochat-only contract

Every trained weight in this study is a nanochat decoder from commit `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`, plus the documented `NANOCHAT_DATA_DIR` hook and no other model-file edits. English BPE: `python -m scripts.tok_train` on WikiText-103 raw train. English pretrain, extra-English, Tagalog continuation, and joint mix: `python -m scripts.base_train` with `--depth`, `--max-seq-len=2048`, `--core-metric-every=-1`. Both language scores: official `evaluate_bpb` through a copy of `scripts/p1/gate_j_full_bpb.py`. P1.1 d20 used as a negative control is the already-published nanochat checkpoint, not a retrained Hugging Face model. Forbidden: Hugging Face `Trainer` or `from_pretrained` as the language model, llama.cpp, `python -m nanochat.dataset`, CORE, SFT, a second architecture, or loading P1.1 `model_000294.pt` as the English parent.

## English phase (EN0)

Corpus: WikiText-103 *raw*. LF-only. Article-hash 70/15/15. Tokenizer: 32,768 BPE on English *train* only. Trainer: nanochat `92d63d4`, $T=2048$, $B=65{,}536$, $N$ from English $D_{3x}=3\times T_{\mathrm{en,train}}$ with explicit `--num-iterations`, ratio never $-1$, CORE off. Depths: 8 and 20 required; 12 and 16 if budget. Seed 0 confirmatory for EN0; extra seeds later.

## Tagalog phase (A2)

Data: frozen P1.1 train JSONL only (hash `2b0474c5…`). Encode with the *English* BPE. $D_{\mathrm{phase2}}=19{,}267{,}584$ English-BPE tokens unless the PDF names English $D_{3x}$. Fresh optimizer, peak LR $=0.3\times$ EN0 peak, warmup 14. Do not load P1.1 `model_000294.pt` as the start weight.

## Arms

::: center
  Arm   Start    Phase-2 stream
  ----- -------- --------------------------
  EN0   random   English train (pretrain)
  A0    EN0      none (dual eval)
  A1    EN0      more English
  A2    EN0      P1.1 Tagalog train
  A3    EN0      50/50 documents
:::

## Dual evaluators

Same `evaluate_bpb` wrapper as P1.1, two data roots. English val never in Tagalog paths. Seal English $C_{\mathrm{en}}$ and Tagalog acquisition on validation with both tests unread. Then at most one English test and at most one Tagalog test, predeclared. Loop `eval-tokens=262144` is diagnostic.

## What is not done

No ClimbMix. No `python -m nanochat.dataset`. No P1.1 weight as English parent. No overwrite of `p1-fixed-d20-3x`. No Hugging Face `Trainer`. No confirmatory SFT/CORE/EWC. No invented rater scores. No mixing tokenizers in one run.

# Analysis plan {#sec:analysis}

Primary: $\bar C_{\mathrm{en}}$ at d8 and d20, seeds as registered, threshold $0.01$. Secondary: Tagalog A2 versus P1.1 Table 2 and versus A0; A3; collapse binary on English. Falsification of forgetting: $C_{\mathrm{en}}$ not material. Falsification of acquisition: Tagalog A2 not better than A0 by $0.01$. Neither revives a P1.1 depth ranking.

# Results {#sec:results}

P1.1 Tagalog table is cited, not rerun. EN0, P0, and A0--A3 cells are empty until the new PDF exists and the runs complete [@simmons2011falsepositive; @wagenmakers2012confirmatory; @nosek2018prereg].

# Discussion rules {#sec:discussion}

If $C_{\mathrm{en}}$ is material and Tagalog A2 improved versus A0, the model learned Filipino and paid an English cost beyond extra English training. If Tagalog did not improve, it did not learn Filipino; do not call that English CF due to Filipino competence. If $C_{\mathrm{en}}\approx 0$ and Tagalog improved, sequential Tagalog at this budget did not overwrite English on BPB. P0 is what licenses the sentence "pretrained in English."

# Limitations {#sec:limits}

No EN0 numbers yet. English BPE on Tagalog text shreds Tagalog; BPB still compares bytes. WikiText-103 $\neq$ web English. P1.1 reconstructed split. One parent seed unless extra seeds run. Shared named entities across Wikipedias. No chat.

# Conclusion {#sec:conclusion}

Paper 1 stays a pure Tagalog base. Paper 2 trains an English nanochat, proves provenance, continues on WikiText-TL-39, and reports English forgetting and Filipino acquisition on the same BPB instrument. That is the pipeline. It is not a rewrite of AsPredicted #306780.

# Ethics {#ethics .unnumbered}

Public Wikipedia text. No passcodes, no `test.jsonl` in public repos. Hub license `other`. Cheng is not a coauthor.

# Acknowledgements {#acknowledgements .unnumbered}

Thanks to AI/LLM models Manus 1.6 and Cursor Grok 4.6 High Fast for drafting, formatting, and solutioning. Special thanks to Dr. Cheng for guidance. WikiText-TL-39: Cruz and Cheng [@cruz2019eval]. WikiText-103: Merity et al. [@merity2017pointer]. nanochat: Karpathy [@karpathy2026nanochat]. Errors are the author's.

::: thebibliography
99

P. Pajo. Equal-exposure depth and held-out Tagalog bits-per-byte on WikiText-TL-39. August 2026. <https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39>.

P. Pajo. NANOCHAT-FILIPINO P1.1: WikiText-TL-39 fixed-budget depth vs held-out BPB. AsPredicted #306780, 15 August 2026. <https://aspredicted.org/6r6v4v.pdf>.

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
