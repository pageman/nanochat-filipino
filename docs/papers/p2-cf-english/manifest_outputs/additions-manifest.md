**Parent paper:** <https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39>\
**Parent code:** <https://github.com/pageman/nanochat-filipino>\
**Parent weights:** <https://huggingface.co/pageman/nanochat-filipino-p1-fixed-d20-3x>\
**Stage-1 CF manuscript:** `docs/papers/p2-cf-english/paper.tex`\
**This manifest:** `docs/papers/p2-cf-english/additions-manifest.tex`\
**Intended new code repo:** `pageman/nanochat-filipino-p2-cf-en`\
**Intended new Hub repo:** `pageman/nanochat-filipino-p2-cf-en`

# How to read this document {#sec:howto}

A naive CF checklist ("add EWC, add replay, measure accuracy drop") would be a wrong answer here. P1.1 is not an English classifier. It is a Tagalog language-modeling measurement with four locked depths, a common $D_{\mathrm{actual}}=19{,}267{,}584$ tokens, a reconstructed split label, a 0.01 BPB interpretation rule, and a one-test-touch clock. Every addition below is anchored to that architecture.

Wrong answers, named so they can be rejected on sight:

1.  Describe generic CF methodology without Table 2's exact BPB values (d8 $1.179135$, d12 $1.180824$, d16 $1.195546$, d20 $1.172248$).

2.  Ignore equal exposure as the structural asset, or call the parents "trained to convergence" (they were not; $R_d$ is $0.458$ at d8 and $0.044$ at d20).

3.  Treat "English" as a monolith: no file, no raw-versus-Moses decision, no token-count basis, no domain control.

4.  Skip the registration-authority chain (new PDF $>$ this manifest $>$ P2 ledger $>$ deviation card).

5.  Reuse P1.1's one `test_bpb`=1.164768 as a post-English number.

6.  Write new weights into the parent Hub repository.

7.  Use loop `val_bpb` from `meta_000294.json` (d20 $1.117213$) as $\mathrm{BPB}_{\mathrm{before}}$.

8.  Retrain the tokenizer after seeing English fertility.

9.  Conflate forgetting, collapse, and retention without predeclared bins.

10. Put Design B (Cebuano) or SFT into the first confirmatory table.

Layer confidence, as used while writing: explicit 99%; residual 95%; implicit 90%; inferred 85%; extrapolated 80%; hidden 75%. Hidden items are the most load-bearing and the easiest to miss.

# Frozen parent anchors (do not recompute) {#sec:anchors}

::: center
  Quantity                                      d8          d12          d16            d20
  ----------------------------------- ------------ ------------ ------------ --------------
  `val_bpb_full` (DV)                     1.179135     1.180824     1.195546   **1.172248**
  `train_bpb_full`                        0.836702     0.528818     0.458045       0.672393
  val$-$train gap                         0.342432     0.652006     0.737501       0.499855
  untrained val                           3.289109     3.289358     3.289354       3.289106
  byte unigram val                        4.453225     4.453225     4.453225       4.453225
  Hub loop `val_bpb`                      1.124545     1.125139     1.137399       1.117213
  $P_{\mathrm{scaling}}$                     41.9M       110.1M       234.9M         435.2M
  $R_d=D_{3x}/P_{\mathrm{scaling}}$       0.457834     0.174413     0.081756       0.044129
  checkpoint SHA prefix                 `9c407f4f`   `5dfccc27`   `525301eb`     `9e30fff3`
:::

Shared: nanochat `92d63d4e8bb4df75c3b71618f31ddde2378b2bcd`; tokenizer `04436b85…bc5a8`; `token_bytes.pt` `a5dbc1c8…2132`; $T=2048$; $B=65{,}536$; $N=294$; split `reconstructed_article_70_15_15`; packed val target bytes $5{,}868{,}797$; one parent test read on d20 only. Extra-seed sample SD at d8 $\approx 0.010318$ (val only; not used to pick $D^{\ast}$).

# Master table of 27 additions {#sec:master}

::: center
  ID   Layer          One-line name                                     Blocking?    First artifact
  ---- -------------- ------------------------------------------------- ------------ ------------------------------
  E1   Explicit       Multi-seed phase-2 matrix                         Yes          `manifests/seed_matrix.json`
  E2   Explicit       Split label on every CF caption                   Yes          caption template
  E3   Explicit       BOS-bestfit crop accounting                       Yes          crop audit JSON
  E4   Explicit       No native-speaker ratings                         No           ethics paragraph
  E5   Explicit       No downstream classifiers                         Yes          exclusions list
  I1   Implicit       English corpus/split/tokenizer                    Yes          `source_manifest_en.json`
  I2   Implicit       Two-phase train + LR lock                         Yes          `phase2_train.yaml`
  I3   Implicit       $\Delta\mathrm{BPB}_{\mathrm{tag}}$ + 0.01 rule   Yes          analysis plan
  I4   Implicit       Forward-transfer English BPB                      Yes          `results/en_val.json`
  I5   Implicit       Joint-training ceiling (A3)                       Yes          arm A3 run cards
  N1   Inferred       Depth-stability hypothesis                        Yes          AsPredicted box
  N2   Inferred       Equal-exposure as CF control                      Yes          intro paragraph
  N3   Inferred       Inherit 0.01 as $\Delta$ threshold                Yes          glossary
  N4   Inferred       $R_d$ as plasticity index                         Yes          Table $R_d$ vs $\Delta$
  X1   Extrapolated   EWC baseline (secondary family)                   After A2     `arm-EWC/`
  X2   Extrapolated   Experience-replay baseline                        After A2     `arm-ER/`
  X3   Extrapolated   Stability--plasticity scatter                     After A2     figure spec
  X4   Extrapolated   BWT/FWT sign conventions                          Yes          metric card
  X5   Extrapolated   Collapse/forgetting/retention bins                Yes          category card
  R1   Residual       Extra-seed matrix reuse                           Yes          copy P1.1 seeds
  R2   Residual       Post-phase-2 document bootstrap                   No           bootstrap script
  R3   Residual       Mid-run Tagalog BPB trajectory                    Diagnostic   eval-every log
  R4   Residual       gzip entropy normalization                        No           gzip JSON
  R5   Residual       $D_{1x}$ English pilots                           Yes          pilot run cards
  H1   Hidden         Tagalog-news domain control                       Yes          arm A4 spec
  H2   Hidden         Tokenizer fertility asymmetry                     Yes          fertility table
  H3   Hidden         Second Tagalog test-read clock                    Yes          `test_access_log_p2.json`
  H4   Hidden         Null P1.1 as CF asset                             Yes          intro reframing
  H5   Hidden         New AsPredicted, not an amendment                 Yes          new PDF
  H6   Hidden         English-native from-scratch baseline              Yes          arm EN0
:::

**Critical path (do not reorder):** R1/E1 seed matrix $\rightarrow$ R5 English $D_{1x}$ pilots $\rightarrow$ H5 CF registration PDF $\rightarrow$ H6 English-native baseline $\rightarrow$ I1--I5 + H1 full phase-2 grid $\rightarrow$ X1--X3 secondary methods $\rightarrow$ paper/GitHub/Hub close-out.

X1--X3 are *not* the first confirmatory table. They start after untreated A2$-$A1 exists, unless the new PDF names them confirmatory (not recommended for paper 1).

# Layer 1 --- Explicit additions (E1--E5) {#sec:L1}

These are things P1.1 already names as missing or constrained. A CF paper that ignores them repeats the parent limitation as if it were unknown.

### E1. Multiple seeds (blocking) {#e1.-multiple-seeds-blocking .unnumbered}

P1.1's four-depth table is one seed (torch 42). Extra seeds 1--2 exist only at d8/d12 on validation, sample SD $\approx 0.010$ at d8, which already swallows the $0.006887$ d20--d8 parent gap. CF deltas will sit in that noise. Specification: continuation seeds $\{0,1,2\}$ on arms A1 and A2 at all four depths ($4\times 2\times 3=24$ confirmatory trainings). A0 and A3 at seed 0 unless budget allows parity. GitHub: `manifests/seed_matrix.json` with parent seed versus continuation seed. Hub: `d{8,12,16,20}/a2/seed{0,1,2}/`. Pass: three finite Tagalog `val_bpb_full` values per cell; sample SD reported; no ranking if the seed interval of A2$-$A1 contains 0.

### E2. Split label on every CF caption (blocking) {#e2.-split-label-on-every-cf-caption-blocking .unnumbered}

P1.1 never recovered 2019 files. Label `reconstructed_article_70_15_15` must appear on every Tagalog retention table, including after English training. The English split gets its own label, e.g. `wikitext103raw_article_70_15_15`, never mixed into Tagalog captions. GitHub: caption lint in `scripts/p2/check_captions.py`. Pass: zero Tagalog tables without the reconstructed label.

### E3. BOS-bestfit crop asymmetry (blocking) {#e3.-bos-bestfit-crop-asymmetry-blocking .unnumbered}

Packed Tagalog val scores $5{,}868{,}797$ target bytes versus $6{,}771{,}275$ raw UTF-8 (13.3% below). English documents have a different length distribution, so crop rate will change. If packing is unchanged, Tagalog packed-byte count after phase 2 must still equal $5{,}868{,}797$ or the evaluator moved. GitHub: `results/packing_audit.json` with `n_cropped_fills` for Tagalog and English. Pass: Tagalog packed bytes identical to parent; English crop rate reported, not "fixed" after seeing $\Delta$.

### E4. Native-speaker ratings remain absent (non-blocking, must declare) {#e4.-native-speaker-ratings-remain-absent-non-blocking-must-declare .unnumbered}

P1.1 invented no 1--5 ratings. CF samples after English continuation will look like mixed Taglish or broken English. Do not score them. Ethics paragraph only. Hub: no sample leaderboard.

### E5. No downstream classification / CORE / SFT as primary (blocking) {#e5.-no-downstream-classification-core-sft-as-primary-blocking .unnumbered}

P1.1 excluded CORE, chat, dengue, hate-speech, NLI. CF paper primary remains BPB. Permuted-MNIST-style accuracy is not this study. GitHub exclusions YAML. Pass: no CORE flag other than `-1`; no SFT data in confirmatory trains.

# Layer 2 --- Implicit additions (I1--I5) {#sec:L2}

Structurally required by any two-phase LM CF design, never spelled as a CF protocol in P1.1.

### I1. English corpus, split, and tokenizer specification (blocking) {#i1.-english-corpus-split-and-tokenizer-specification-blocking .unnumbered}

English is not "some English." Lock: WikiText-103 *raw* (not Moses `@-@` WT103) so both languages are encyclopedia prose [@merity2017pointer]. Canonical: LF only. Split: SHA-256 of UTF-8, 70/15/15, independent of Tagalog. Tokenizer: *parent Tagalog 32,768 BPE only*. Token budget counted as $\sum\mathrm{len}(\tau(d))$ under that BPE, not GPT-2 tokens, not words. Record file SHA, $T_{\mathrm{en,train}}$, fertility (bytes/token) on English train/val. If raw WT103 is unavailable, stop and file a deviation *before* using tokenized WT103. Do not substitute TLUnified, OSCAR, ClimbMix, or C4 as the confirmatory English stream (domain shift stacked on language). GitHub: `manifests/source_manifest_en.json`, `split_manifest_en.json`, `fertility_en.json`. Hub README: English source hash, not the text.

### I2. Two-phase training protocol and learning-rate lock (blocking) {#i2.-two-phase-training-protocol-and-learning-rate-lock-blocking .unnumbered}

Phase 1 is finished: load `model_000294.pt` only. Parent optimizer states were never published, so Adam moments cannot resume. Phase 2: fresh optimizer; $T=2048$; $B=65{,}536$; $N=294$; $D_{\mathrm{phase2}}=19{,}267{,}584$; `--num-iterations 294` explicit; `--target-param-data-ratio` $=$ parent $R_d$ for that depth, never $-1$; CORE off; device-batch 8, halve only for VRAM. Peak LR $=0.3\times$ parent scheduled peak (from `meta_000294.json` or trainer formula). Warmup $\min(40,\lfloor 0.05N\rfloor)=14$. This is continuation, not a second pretrain. GitHub: `configs/phase2.yaml`, command generator mirroring `scripts/p1/generate_gate_i_runcards.py`. Hub: each run folder stores the exact command string.

### I3. Forgetting metric $\Delta\mathrm{BPB}_{\mathrm{tag}}$ and threshold (blocking) {#i3.-forgetting-metric-deltamathrmbpb_mathrmtag-and-threshold-blocking .unnumbered}

$$\Delta\mathrm{BPB}_{\mathrm{tag}}(d,a,s)=\mathrm{val\_bpb\_full}_{\mathrm{after}}(d,a,s)-\mathrm{val\_bpb\_full}_{\mathrm{P1.1}}(d).$$ Before-score is Table 2, not Hub loop val. Confirmatory contrast: $$C(d,s)=\mathrm{val\_bpb\_full}(d,\mathrm{A2},s)-\mathrm{val\_bpb\_full}(d,\mathrm{A1},s).$$ Positive $C$ means English hurt Tagalog more than extra Tagalog did. Material if $|\bar C|\ge 0.01$. Evaluator: copy `scripts/p1/gate_j_full_bpb.py` byte-identical except output paths. GitHub: `results/delta_tagalog.json`. Pass: parent before-scores match Table 2 to printed precision.

### I4. Forward-transfer / plasticity metric (blocking) {#i4.-forward-transfer-plasticity-metric-blocking .unnumbered}

Retention without acquisition is incomplete. Secondary: English `val_bpb_full` after A2 (and A3, EN0). Not used to pick depth. Same `evaluate_bpb`, English val JSONL, $T=2048$. GitHub: `results/en_val.json`. Sign convention: lower English BPB is better plasticity; do not subtract it from Tagalog $\Delta$ into one scalar.

### I5. Joint-training upper bound (blocking) {#i5.-joint-training-upper-bound-blocking .unnumbered}

Arm A3: 50/50 *document* mix of Tagalog train and English train, same $D_{\mathrm{phase2}}$, shuffled at document level, never concatenating a Tagalog article to an English article inside one packed row as a silent curriculum. A3 is a ceiling on retention under mixed exposure, not a proof of "no forgetting." GitHub: mixer script with seed. Pass: token counts 50/50 $\pm$ documented remainder $<B$.

# Layer 3 --- Inferred additions (N1--N4) {#sec:L3}

Follow-on logic from Table 2's actual pattern, not from a generic "deeper is more stable" slogan.

### N1. Depth-stability hypothesis (preregister as directional, not as a ranking) {#n1.-depth-stability-hypothesis-preregister-as-directional-not-as-a-ranking .unnumbered}

Table 2 train--val gaps: d8 $0.342$, d12 $0.652$, d16 $0.738$, d20 $0.500$. The widest gap is d16, not d20; d20 is the `val_bpb_full` minimum by $0.006887$ over d8. Inferred directional guess for *untreated* English forgetting: $$\bar C(d16)\;>\;\bar C(d20)\;>\;\bar C(d8)$$ i.e. mid-depth most unstable, deepest not automatically most stable, shallowest least overfit and maybe most robust. This is a hypothesis to put in the new AsPredicted box. It is *not* a license to rank depths if gaps $<0.01$ or seed intervals overlap. Alternative reading: $R_d$ not gap predicts $C$; then $C$ should fall as $R_d$ rises (d8 most data-rich, least plastic). Pre-register *which* of gap-order vs $R_d$-order is primary; the other is secondary. Recommendation: primary = $R_d$-order test (d8 vs d20 contrast of $\bar C$); gap-order is specified secondary because it uses P1.1's most distinctive shape.

### N2. Equal-exposure as CF control (intro load-bearing paragraph) {#n2.-equal-exposure-as-cf-control-intro-load-bearing-paragraph .unnumbered}

Most CF depth claims confound size with extra pretraining tokens. P1.1 removed that confound for phase 1. The CF intro must say: parents saw the same $19.27$M tokens; therefore a later depth effect on $C$ cannot be dismissed as "d20 simply trained longer in phase 1." Residual: they are still not equally optimized ($R_d$ differs). Caption that residual every time N2 is invoked.

### N3. 0.01 BPB threshold inheritance {#n3.-0.01-bpb-threshold-inheritance .unnumbered}

P1.1 used $0.01$ so a $0.006887$ dip was not a ranking. CF inherits $0.01$ as the material-forgetting threshold for $\bar C$ and for d20$-$d8 of $\bar C$, unless the new PDF names another number *before* phase-2 BPB. Do not tighten to $0.001$ after seeing a small $C$.

### N4. $R_d$ as plasticity index {#n4.-r_d-as-plasticity-index .unnumbered}

Plot $\bar C$ against $R_d\in\{0.458,0.174,0.082,0.044\}$. If $|C|$ rises as $R_d$ falls, the story is residual undertraining, not "depth is a stability dial." GitHub: `results/rd_vs_C.json`. Hub model card: one sentence that $R_d$ is not a hyperparameter sweep.

# Layer 4 --- Extrapolated additions (X1--X5) {#sec:L4}

What the CF canon expects if this paper is to be readable next to EWC/GEM/ER. These are integration points, not replacements for A2$-$A1.

### X1. EWC baseline (secondary family, after untreated A2) {#x1.-ewc-baseline-secondary-family-after-untreated-a2 .unnumbered}

Kirkpatrick et al. elastic weight consolidation on the parent, then English A2-budget [@kirkpatrick2017ewc]. Fisher estimated on Tagalog train only, $\lambda$ predeclared (recommend a two-value grid $\{10,100\}$ as exploratory unless PDF says otherwise). Same tokenizer, $T$, $B$, $N$. Do not tune $\lambda$ on Tagalog val after seeing $C$. GitHub: `scripts/p2/ewc_train.py`, `arm-EWC/`. Hub: separate folders, `parent_sha256` pinned. Not confirmatory for paper 1 unless the PDF says so.

### X2. Experience replay (secondary) {#x2.-experience-replay-secondary .unnumbered}

Replay buffer = frozen Tagalog train documents. Mix ratios $\{0,0.05,0.20,0.50\}$ of phase-2 tokens, remainder English, total still $D_{\mathrm{phase2}}$. Ratio $0$ is A2; do not double-count. Selection of ratio is not allowed from Tagalog test. This is Design D; paper 1 may report seed-0 d20 only as exploratory.

### X3. Stability--plasticity scatter {#x3.-stabilityplasticity-scatter .unnumbered}

$x$ = Tagalog $\Delta\mathrm{BPB}_{\mathrm{tag}}$ (A2; higher $x$ = more forgetting). $y$ = English val BPB (higher $y$ = worse acquisition). One point per depth$\times$seed. Joint A3 and EN0 as reference symbols. No Pareto claim without the 0.01 rule.

### X4. BWT and FWT with BPB sign conventions {#x4.-bwt-and-fwt-with-bpb-sign-conventions .unnumbered}

Standard accuracy BWT is after-minus-before on old tasks (negative = forgetting). For BPB, *positive* after-minus-before on Tagalog is forgetting. Define: $$\begin{align*}
\mathrm{BWT}_{\mathrm{BPB}} &= \mathrm{val\_bpb\_full}^{\mathrm{tag}}(\mathrm{after})-\mathrm{val\_bpb\_full}^{\mathrm{tag}}(\mathrm{P1.1}),\\
\mathrm{FWT}_{\mathrm{BPB}} &= \mathrm{val\_bpb\_full}^{\mathrm{en}}(\mathrm{A2})-\mathrm{val\_bpb\_full}^{\mathrm{en}}(\mathrm{EN0}).
\end{align*}$$ FWT uses the English-native from-scratch model (H6) as the reference, not a random init. Negative FWT$_{\mathrm{BPB}}$ means the Tagalog parent helped English (forward transfer). Publish the formulas in a metric card so reviewers do not flip signs.

### X5. Category pre-registration: retention / forgetting / collapse {#x5.-category-pre-registration-retention-forgetting-collapse .unnumbered}

Bins on Tagalog A2 `val_bpb_full` relative to parent:

- **Retention:** $\bar C < 0.01$ and no collapse flag.

- **Forgetting:** $\bar C \ge 0.01$ and not collapse.

- **Collapse:** after A2, Tagalog val BPB $\ge$ parent untrained, or $\ge 4.453225$, or $\Delta\ge 1.0$.

A run cannot be titled "collapse" because $\Delta=0.02$. GitHub: `results/category.json`.

# Layer 5 --- Residual additions (R1--R5) {#sec:L5}

P1.1 suppressed or sidelined items that become CF assets.

### R1. Extra-seed matrix {#r1.-extra-seed-matrix .unnumbered}

P1.1 extra seeds at d8/d12 are secondary for $D^{\ast}$ and primary for noise-scale planning. Copy the protocol: validation only, no test, same evaluator. Extend to d16/d20 *before* claiming CF seed needs. If P1.1 extra-seed files exist only on a stopped pod, treat them as unavailable and rerun rather than inventing SD.

### R2. Document-level bootstrap after phase 2 {#r2.-document-level-bootstrap-after-phase-2 .unnumbered}

P1.1 bootstrap used per-document non-overlap, not BOS-bestfit; all four 95% CIs overlapped ($\sim 1.23$--$1.39$). Re-run the same bootstrap on post-A2 Tagalog val as a secondary packing, labeled not-`val_bpb_full`. Do not pick depth from it.

### R3. Mid-run Tagalog BPB trajectory during English training {#r3.-mid-run-tagalog-bpb-trajectory-during-english-training .unnumbered}

P1.1 forbade selecting $D^{\ast}$ from step-200 d12 min $1.084991$. CF still *records* Tagalog val every 50 steps at `eval-tokens=262144` during A2 as a diagnostic curve of when forgetting happens. Primary remains final-step full BPB. GitHub: `results/trajectories/` with an explicit `not_primary: true` flag.

### R4. gzip entropy normalization {#r4.-gzip-entropy-normalization .unnumbered}

P1.1 gzip $-9$ on raw val UTF-8 was $2.739$ bits/byte. After A2, gzip of Tagalog val does not change (data are frozen). gzip is not a forgetting metric. Optional: gzip of English val as a compressor baseline for plasticity, never as BWT.

### R5. $D_{1x}$ English pilots (blocking on the critical path) {#r5.-d_1x-english-pilots-blocking-on-the-critical-path .unnumbered}

P1.1 $D_{1x}$ pilots (step 98) showed d8/d12 worse than $D_{3x}$. Before spending 24 confirmatory A1/A2 runs, run d8 and d20, seed 0, $N=98$, English only, Tagalog val_bpb_full. Purpose: wiring, VRAM, fertility shock, not $C$. If Tagalog BPB becomes NaN, stop. GitHub: `docs/run-cards/p2-pilots/`. These pilots must finish *or be waived by a dated deviation* before the confirmatory PDF claims the grid is feasible. They must not leak into the confirmatory table.

# Layer 6 --- Hidden additions (H1--H6) {#sec:L6}

Frame shifts P1.1 could suppress because it never left Tagalog Wikipedia. In a CF paper they become load-bearing.

### H1. Language-versus-domain confound (blocking for the phrase "relative to English") {#h1.-language-versus-domain-confound-blocking-for-the-phrase-relative-to-english .unnumbered}

A2 on English Wikipedia changes language *and* dump statistics. To isolate language, add arm A4: matched-budget continuation on **Tagalog news** (TLUnified or a predeclared news dump), same tokenizer, same $D_{\mathrm{phase2}}$ [@cruz2022tlunified]. Contrast of interest for "English caused it": $$C_{\mathrm{lang}}=C_{\mathrm{A2}}-C_{\mathrm{A4}}.$$ If A4 forgets as much as A2, the cause is domain shift or extra training, not English. A4 is confirmatory for the title phrase "relative to English"; if compute forces a cut, the title must drop that phrase and say "relative to extra Tagalog Wikipedia" (A2$-$A1 only). Do not harvest TLUnified after seeing A2.

### H2. Tokenizer fertility asymmetry (blocking) {#h2.-tokenizer-fertility-asymmetry-blocking .unnumbered}

Parent BPE was trained on Tagalog only. P1.1 val fertility $\approx 4.53$ bytes/token versus GPT-2 $\approx 2.76$. On English, the same BPE will over-segment ("shred") English into shorter tokens, raising English token counts for the same UTF-8 bytes and making English acquisition look harder than a GPT-2-tokenized English LM. That is part of the intervention. Report English bytes/token before any phase-2 claim. Forbidden fix: train a bilingual tokenizer after seeing English BPB. Optional later paper: matched-fertility byte-level models.

### H3. Test-set authority chain and a second Tagalog test read (blocking) {#h3.-test-set-authority-chain-and-a-second-tagalog-test-read-blocking .unnumbered}

P1.1: `test_read_events`=1, d20 only, $1.164768$, SHA `3bd19345…`. A CF paper that wants a Tagalog *test* $\Delta$ needs a **new** predeclared event: one test read after all validation $C$ are sealed, on a predeclared subset (recommend d20 seed-0 A1 and A2 only, or all depths seed-0 A2 only --- pick in the PDF). Clock: `test_access_log_p2.json` starts at 0. P1.1's $1.164768$ is the parent before-test for d20 only; other depths have no parent test BPB and cannot have a test $\Delta$ without a new parent test, which P1.1 forbade. Therefore confirmatory Tagalog test $\Delta$ is d20-only, or the PDF must say "validation only, no test $\Delta$." Recommended: validation $C$ is primary; one d20 A2 test BPB is secondary; no test for d8/d12/d16.

### H4. Null-result reframing (intro) {#h4.-null-result-reframing-intro .unnumbered}

P1.1's non-ranking at $0.01$ is the CF paper's strongest asset: depth was not a performance dial, so a later depth effect on $C$ is new information rather than "bigger models were already better." Write that paragraph before methods. Do not reopen $D^{\ast}$.

### H5. Separate AsPredicted / ResearchBox (blocking) {#h5.-separate-aspredicted-researchbox-blocking .unnumbered}

New PDF, new box. Authority: new PDF $>$ this manifest $>$ `docs/papers/p2-cf-english/paper.tex` $>$ P2 ledger $>$ deviation. Filing occurs after R5 pilots show feasibility and before any confirmatory A2 `val_bpb_full`. Draft: `docs/papers/p2-cf-english/aspredicted-draft-p2.txt` (extend it with H1/H6/N1 before filing).

### H6. English-native from-scratch baseline (blocking for "relative to English") {#h6.-english-native-from-scratch-baseline-blocking-for-relative-to-english .unnumbered}

The title phrase is not only "Tagalog model then English data." It also requires an English-native model trained *from scratch* on the same English stream, same $D_{\mathrm{phase2}}$, same Tagalog BPE (fair tokenizer), same depths, seed 0: arm EN0. Plasticity FWT compares A2 English BPB to EN0. A Tagalog parent that reaches EN0 English BPB has transferred; one that is far worse has paid a tokenizer-and-initialization tax. EN0 is not a parent of forgetting (it never saw Tagalog). GitHub: `runs/en0-d{8,12,16,20}/`. Hub: `en0/` not inside `p1-fixed-d20-3x`.

# Unified experimental grid (after PDF) {#sec:grid}

Confirmatory family (paper 1):

::: center
  Arm   Parent     Phase-2 stream            Role
  ----- ---------- ------------------------- ------------------------------
  A0    P1.1 $d$   none                      Eval drift
  A1    P1.1 $d$   Tagalog Wiki train        Continued-training drift
  A2    P1.1 $d$   English WT103-raw train   Language+dump intervention
  A3    P1.1 $d$   50/50 documents           Joint ceiling
  A4    P1.1 $d$   Tagalog news train        Domain control (H1)
  EN0   random     English WT103-raw train   English-native baseline (H6)
:::

Primary contrast: $\bar C(d)=\overline{\mathrm{A2}-\mathrm{A1}}$ over seeds $\{0,1,2\}$. Language isolation: $\overline{\mathrm{A2}-\mathrm{A4}}$ at seed 0 if A4 is confirmatory. Plasticity: A2 English BPB versus EN0. Secondary after freeze: EWC, ER ratios.

# Super-granular procedure {#sec:steps}

Execute in order. A later gate may not start if the previous gate's JSON `status` is not `pass`. Deviation cards cannot make a departed run confirmatory after seeing BPB.

## Gate P2-0 --- Freeze the parent (read-only)

1.  Verify local or Hub SHA-256 for d8/d12/d16/d20 `model_000294.pt` against §[2](#sec:anchors){reference-type="ref" reference="sec:anchors"}.

2.  Verify tokenizer.pkl and token_bytes.pt hashes.

3.  Copy `scripts/p1/gate_j_full_bpb.py` into the new repo without editing packing math.

4.  Write `PARENT.md` with ResearchGate URL, GitHub URL, Hub URL, commit `92d63d4`, AsPredicted #306780, and "do not amend."

5.  Do not run Tagalog test BPB. Do not touch `test.jsonl`.

## Gate P2-1 --- Create empty P2 GitHub repository

1.  `gh repo create pageman/nanochat-filipino-p2-cf-en --public`.

2.  Orphan first commit (same discipline as P1.1 public-main): no passcodes, no `transfer/`, no `test.jsonl`, no `.pt` weights.

3.  Root files: `LICENSE` (MIT), `LICENSE-RESEARCH.md`, `DATA_AND_CODE_NOTICES.md` (WikiText-TL-39 + WikiText-103 + news dump if A4), `PARENT.md`, `README.md` (claim / not-claim / Quick Start / bibtex / DeepWiki / parent links).

4.  Tree:

        p2-cf-en/
          README.md PARENT.md LICENSE LICENSE-RESEARCH.md
          DATA_AND_CODE_NOTICES.md
          configs/phase2.yaml
          docs/PROTOCOL-p2-cf-en.md
          docs/papers/   (this manifest + Stage-1 paper)
          docs/run-cards/p2-pilots/
          manifests/  (seed, source_en, split_en, fertility, budget_phase2,
                       gate_ledger, test_access_log_p2, selection_record_p2)
          patches/    (copy NANOCHAT_DATA_DIR.patch)
          reproducibility/
          results/    (empty JSON schemas with nulls)
          scripts/p2/

5.  `.gitignore`: `*.pt`, `*.pkl`, `*.parquet`, `artifacts/`, `vendor/nanochat/`, passcode files.

6.  Push orphan `main` only. Do not force-push parent history that contains secrets.

## Gate P2-2 --- Create empty P2 Hugging Face repository

1.  `hf repo create pageman/nanochat-filipino-p2-cf-en --type model --private` then make public after card review, or public immediately if card has no secrets.

2.  YAML: `license: other`; languages `tl`, `en`; tags `nanochat`, `catastrophic-forgetting`, `bits-per-byte`; datasets `linkanjarad/Wikitext-TL39` plus the locked English id.

3.  README **Paper** / **Code** / **Parent** block:

        parent_base_repo: pageman/nanochat-filipino-p1-fixed-d20-3x
        parent_paper: https://www.researchgate.net/publication/412302216_...
        parent_code: https://github.com/pageman/nanochat-filipino
        this_code: https://github.com/pageman/nanochat-filipino-p2-cf-en

4.  Folder schema (create `.gitkeep` only until weights exist):

        d8/a0/ d8/a1/seed0/ d8/a2/seed{0,1,2}/ d8/a3/ d8/a4/ d8/en0/
        ... same for d12 d16 d20
        ewc/  er/   # secondary, later

5.  Each future weight folder: `model_*.pt`, `meta_*.json`, `SHA256`, command string. No optimizer states required. No Tagalog `test.jsonl`.

6.  Do not push into `p1-fixed-d20-3x`.

## Gate P2-3 --- English and news corpus audit (I1, H1, H2)

1.  Download WikiText-103 raw; hash; LF-only canonical; article reconstruct; 70/15/15 hash split; write `split_manifest_en.json`.

2.  Encode train with frozen parent BPE; write $T_{\mathrm{en,train}}$, bytes/token, compare to Tagalog $4.53$.

3.  If A4 is confirmatory: lock Tagalog news source, same pipeline, `split_manifest_news.json`. News val/test never enter Tagalog Wikipedia val/test.

4.  Place shards via `NANOCHAT_DATA_DIR` hook. Never `python -m nanochat.dataset`.

5.  Write-protect English test JSONL; keep out of active train dir.

## Gate P2-4 --- $D_{1x}$ English pilots (R5)

1.  Host card: named NVIDIA GPU, image, torch, device-batch.

2.  d8 seed0 A2 $N=98$; d20 seed0 A2 $N=98$.

3.  Tagalog `val_bpb_full` once at end (full evaluator), plus loop logs.

4.  Pass: finite BPB, hashes unchanged, no test read, VRAM fit at $T=2048$.

5.  Fail: stop confirmatory; deviation or smaller device-batch only (not smaller $T$).

## Gate P2-5 --- File the new AsPredicted (H5)

1.  Expand `aspredicted-draft-p2.txt` with N1 (which depth order is primary), H1 (A4 yes/no), H6 (EN0 required), H3 (test policy), X5 bins, 0.01 rule, equal $D_{\mathrm{phase2}}$, frozen tokenizer.

2.  File PDF. Store SHA-256. ResearchBox deposit without passcode in git.

3.  Set ledger `registration.url`. No confirmatory A2 full BPB before this timestamp.

## Gate P2-6 --- English-native from-scratch EN0 (H6)

1.  From random init, depths 8 and 20 seed 0 at minimum; 12 and 16 if budget.

2.  Same English train stream, $N=294$, Tagalog BPE, $T=2048$.

3.  English val BPB only until sealed; English test at most once later.

4.  Upload to Hub `en0/d8`, `en0/d20`. GitHub manifests only.

## Gate P2-7 --- Confirmatory phase-2 grid

1.  Serial or documented-parallel: for $d\in\{8,12,16,20\}$, A0 (eval only), A1 seeds 0--2, A2 seeds 0--2, A3 seed 0, A4 seed 0 if confirmatory.

2.  After each run: finite check; SHA of weights; Tagalog full val BPB; do not look at Tagalog test.

3.  Write per-cell JSON: nats, bytes, excluded specials, packed bytes (must match parent on Tagalog).

4.  A0 must recover Table 2 within documented host noise; if not, stop (evaluator/host drift).

## Gate P2-8 --- Seal $C$, then optional test (H3, I3)

1.  Compute $\bar C(d)$ and sample SD from A1/A2 seeds. Write `selection_record_p2.json` with `test_read_count=0`.

2.  Apply 0.01 rule and X5 bins. Do not drop depths.

3.  If PDF allows: one Tagalog test read on predeclared cells; append `test_access_log_p2.json`; never use test to choose depth.

4.  English test at most once, after English val sealed, not mixed with Tagalog test in one command.

## Gate P2-9 --- Secondary methods (X1--X3), optional

Only after Gate P2-8 JSON exists. EWC/ER cannot rewrite $C$. Label exploratory unless the PDF already included them (it should not, for paper 1).

## Gate P2-10 --- Paper compilation

1.  Fill Stage-1 `docs/papers/p2-cf-english/paper.tex` Table phase-2 with real numbers; do not edit P1.1 Table 2.

2.  Intro uses H4+N2. Methods use I1--I5, H2, H6. Results: $C(d)$, A4 if run, EN0, scatter X3, categories X5.

3.  Limitations: single parent seed, $R_d$ residual, fertility shredding, reconstructed split, packing crop.

4.  Acknowledgements may match P1.1. Cheng is not coauthor.

5.  Build `tex,md,txt,html,docx,pdf`. Cite parent ResearchGate URL.

6.  Do not claim "deeper is always more stable." Do not claim P1.1 showed forgetting.

## Gate P2-11 --- Publish GitHub and Hub close-out

1.  GitHub: results JSON, run cards, deviation cards, paper outputs (no `test.jsonl`).

2.  Hub: upload only new run folders; model card copies $\Delta$ table and points at GitHub `results/` for audit; parent SHAs listed; loop vs full BPB distinction restated.

3.  Tag Hub revision. Record commit in `final_checkpoint_manifest_p2.json`.

4.  DeepWiki link after GitHub is public: `https://deepwiki.com/pageman/nanochat-filipino-p2-cf-en`.

# Paper section $\leftrightarrow$ addition map {#sec:map}

::: center
  CF paper section   Additions that must appear
  ------------------ ---------------------------------------------------
  Title / abstract   H4, H5, H6, I3, X5, N3
  Introduction       H4, N2, N1 (as hypothesis), parent Table 2 cite
  Related work       X1, X2, X4, McCloskey/French/Luo
  Registration       H5, H3, E1, N3
  English data       I1, H1, H2
  Phase-2 train      I2, E3, R5, R3 (diagnostic)
  Metrics            I3, I4, X4, X5, N4
  Arms               I5, H1, H6, A0--A4, EN0
  Results            E1, N1 test, X3, R2 optional
  Limitations        E2, E4, E5, $R_d$, fertility, reconstructed split
  Ethics / lineage   parent URLs, no passcode, no parent-Hub overwrite
:::

# GitHub README claim / not-claim (copy text) {#sec:readme}

**Claim:** This repository is the close-out archive for a preregistered equal-exposure continuation study: frozen P1.1 Tagalog nanochat parents, matched $D_{\mathrm{phase2}}$, Tagalog `val_bpb_full` contrast A2$-$A1, optional language-versus-news control, English-native from-scratch reference.

**Not-claim:** Not P1.1. Not a chat model. Not CORE. Not proof that deeper models forget less. Not an amendment of AsPredicted #306780. Not a dump of `test.jsonl`. Checkpoints live on Hugging Face `pageman/nanochat-filipino-p2-cf-en`. Parent weights stay at `pageman/nanochat-filipino-p1-fixed-d20-3x`.

# What remains out of paper 1 {#sec:out}

Design B (Cebuano/Ilocano/Hiligaynon). PackNet / GEM as confirmatory. SFT arm E. Changing tokenizer. ClimbMix. Reopening $D^{\ast}$. Using loop val as BWT. Native-speaker scores. Downstream NER/GCE as forgetting metrics.

# Per-addition operator card (copy into the ledger) {#app:cards}

For each ID, the operator writes one JSON object before the next ID starts. Fields: `id`, `layer`, `started_at_utc`, `ended_at_utc`, `operator`, `status` $\in$ {`not_started`,`pass`,`fail`,`deferred`}, `artifacts[]`, `hashes{}`, `notes`, `confirmatory` (bool). Deferred is allowed only for X1, X2, X3, R2, R4, and for A4 if the PDF dropped the phrase "relative to English." Deferred is not allowed for H5, I3, E1, I1, H2, H3, H6 if the title keeps "relative to English."

# JSON schemas (GitHub `manifests/` and `results/`) {#app:json}

## `seed_matrix.json` (E1, R1)

Keys: `parent_seed` (always 0 / torch 42), `continuation_seeds` $[0,1,2]$, `arms_requiring_three_seeds` $[\mathrm{A1},\mathrm{A2}]$, `arms_seed0_only` $[\mathrm{A0},\mathrm{A3},\mathrm{A4},\mathrm{EN0}]$ unless upgraded, `n_confirmatory_trainings` (24 if A1/A2 $\times$ 4 depths $\times$ 3 seeds).

## `source_manifest_en.json` (I1)

Keys: `dataset_id`, `revision`, `raw_not_moses` (must be true), `file_sha256`, `n_rows`, `canonical` `LF_only`, `tokenizer_sha256` (must equal `04436b85…`), `t_en_train`, `bytes_per_token_train`, `bytes_per_token_val`, `gpt2_bytes_per_token_val` (descriptive only).

## `budget_phase2.json` (I2)

Keys: `N` $294$, `B` $65536$, `D_phase2` $19267584$, `token_unit` `parent_tagalog_bpe`, `lr_peak_fraction` $0.3$, `warmup` $14$, `fresh_optimizer` true, `never_ratio_minus_one` true, `core_metric_every` $-1$.

## `delta_tagalog.json` (I3)

Per depth and seed: `bpb_before` (copied from Table 2, not recomputed as a new truth), `bpb_a0`, `bpb_a1`, `bpb_a2`, `bpb_a3`, `C` $=\mathrm{a2}-\mathrm{a1}$, `Delta_a2` $=\mathrm{a2}-\mathrm{before}$, `packed_bytes` (must be $5868797$ on Tagalog val), `n_excluded`, `finite`.

## `test_access_log_p2.json` (H3)

Starts `test_read_events`: $0$. Each event: `at_utc`, `kind` (`tagalog_test_bpb` or `english_test_bpb`), `depth`, `arm`, `seed`, `bpb`, `file_sha256`, `used_to_select`: false. Forbidden: reading P1.1 test without a new event; using P1.1's $1.164768$ as `after`.

## `category.json` (X5)

Per depth: `C_bar`, `C_sd`, `bin` $\in$ {`retention`,`forgetting`,`collapse`}, `collapse_flags` (untrained, unigram, delta_ge_1).

# Command templates (do not improvise flags) {#app:cmd}

Parent load is always the Hub or local SHA-pinned `model_000294.pt`. Phase-2 train (A2 shown; A1 swaps data dir to Tagalog train shards; A4 to news shards):

    python -m scripts.base_train \
      --device-type=cuda --depth=DEPTH --max-seq-len=2048 \
      --device-batch-size=8 --total-batch-size=65536 \
      --num-iterations=294 \
      --target-param-data-ratio=PARENT_RD \
      --eval-tokens=262144 --eval-every=50 --core-metric-every=-1 \
      --sample-every=200 --save-every=50 --warmup-steps=14 \
      --run=p2-a2-dDEPTH-sSEED --model-tag=p2-a2-dDEPTH-sSEED

Load-from-checkpoint flag must be whatever the pinned nanochat commit actually implements; record the exact flag in the run card *before* launch. If the trainer cannot load a custom `.pt`, stop and write a deviation; do not reimplement `load_model` ad hoc after seeing loss.

Tagalog full eval after train (validation phase only):

    python scripts/p2/gate_j_full_bpb.py --phase val \
      --depth DEPTH --model-tag TAG --checkpoint-step FINAL

`--phase test` is illegal until `test_access_log_p2.json` says count $0$ and `selection_record_p2.json` exists.

EN0 omits parent load, same English shards, same $N,B,T$, Tagalog BPE still mounted.

# Hugging Face README body (paste) {#app:hf}

Paste after YAML. Keep the loop-versus-full warning:

    # nanochat-filipino-p2-cf-en

    Paper (Stage 1 until numbers exist): see GitHub docs/papers/p2-cf-english/
    Parent paper: https://www.researchgate.net/publication/412302216_...
    Parent weights: pageman/nanochat-filipino-p1-fixed-d20-3x
    Parent code: https://github.com/pageman/nanochat-filipino
    This code: https://github.com/pageman/nanochat-filipino-p2-cf-en

    This repo is continuation and English-native runs, not the P1.1 parents.
    Do not rank forgetting from meta_*.json val_bpb (eval_tokens=262144).
    Primary: Tagalog val_bpb_full contrast A2-A1. Threshold 0.01 BPB.
    Tokenizer is the frozen Tagalog 32,768 BPE. English is WikiText-103 raw.
    No test.jsonl. No SFT. No ClimbMix. License field other.

# Paper paragraph inserts (do not paraphrase into hype) {#app:paras}

**Intro (H4+N2).** "Pajo (2026) showed that under $D_{3x}$ on WikiText-TL-39, nanochat depths 8--20 are not a held-out Tagalog BPB ranking at $0.01$ BPB (exact minimum at depth 20, margin $0.006887$ to depth 8). That null is useful here: if depth later changes the English-continuation contrast $C$, the change is not a restatement of a phase-1 performance ranking. Phase-1 exposure was matched ($D_{\mathrm{actual}}=19{,}267{,}584$); residual $R_d$ still differs and is reported with $C$."

**Methods tokenizer (H2).** "English is encoded with the parent Tagalog BPE. Fertility on English is expected to be worse than GPT-2. Bytes/token are reported. The tokenizer is not retrained."

**Methods English-native (H6).** "Arm EN0 trains the same depths from scratch on the English stream with the same BPE and $D_{\mathrm{phase2}}$. FWT$_{\mathrm{BPB}}$ is A2 English val BPB minus EN0 English val BPB. EN0 never sees Tagalog and is not a forgetting parent."

**Results rule (N3+X5).** "We report $\bar C$ and sample SD. Values below $0.01$ are not a ranking. Collapse is reserved for the predeclared binary."

# Gate file checklist (tick in the ledger, not in chat) {#app:ticks}

P2-0: four weight SHAs, two tokenizer SHAs, `PARENT.md`, evaluator copy, zero test reads.\
P2-1: public GitHub, orphan commit, gitignore, MIT + research notices, empty results schemas.\
P2-2: Hub repo, YAML `other`, parent block, empty arm folders, no parent-repo push.\
P2-3: English raw hash, split label, fertility table, write-protected English test, no ClimbMix.\
P2-4: d8 and d20 $N=98$ pilots, finite Tagalog val, host card, VRAM at $T=2048$.\
P2-5: new AsPredicted PDF SHA, ResearchBox without passcode in git, ledger URL.\
P2-6: EN0 d8/d20 at least, English val sealed.\
P2-7: 24 A1/A2 runs + A0/A3/(A4), packed bytes match, A0 recovers Table 2.\
P2-8: `C` sealed at test count 0; optional one d20 test; categories assigned.\
P2-9: EWC/ER only if labeled secondary.\
P2-10: paper table filled, P1.1 table untouched, six formats built.\
P2-11: GitHub results public, Hub weights in p2 repo only, DeepWiki link.

# Compute sketch (not a budget promise) {#app:compute}

P1.1 seed-0 $D_{3x}$ wall times on A40 were about $0.027/0.061/0.119/0.204$ hours for d8/d12/d16/d20. Phase-2 is the same $N$ and $B$, plus eval. Order-of-magnitude: 24 A1/A2 trains $\approx$ $6\times$ a four-depth seed-0 sweep if depths are balanced, plus EN0, A3, A4, pilots. Record actual hours on the host card. Do not cut d20 after seeing $C$.

# Failure modes mapped to addition IDs {#app:fail}

NaN Tagalog BPB after A2 $\rightarrow$ stop, E1/R5. Packed byte count changed $\rightarrow$ evaluator moved, E3. A0 $\neq$ Table 2 $\rightarrow$ host/eval drift, P2-7. English Moses `@-@` used silently $\rightarrow$ I1 fail. Tokenizer retrained $\rightarrow$ H2 fail. Test read before seal $\rightarrow$ H3 fail. Weights pushed to parent Hub $\rightarrow$ lineage fail. $C$ computed from loop val $1.117213$ $\rightarrow$ I3 fail. Title says "relative to English" but A4 and EN0 absent $\rightarrow$ H1/H6 fail. Collapse claimed at $\Delta=0.02$ $\rightarrow$ X5 fail. #306780 edited $\rightarrow$ H5 fail.

# Status {#status .unnumbered}

This manifest is a specification. Phase-2 BPB does not exist here. Filling $C(d)$ before H5 is a protocol break.

::: thebibliography
9 P. Pajo. Equal-exposure depth and held-out Tagalog bits-per-byte on WikiText-TL-39. 2026. <https://www.researchgate.net/publication/412302216_Equal-Exposure_Depth_and_Held-Out_Tagalog_Bits-per-Byte_on_WikiText-TL-39>. S. Merity et al. Pointer sentinel mixture models. ICLR, 2017. J. C. B. Cruz and C. Cheng. Improving large-scale language models and resources for Filipino. LREC, 2022. J. Kirkpatrick et al. Overcoming catastrophic forgetting in neural networks. PNAS, 2017.
:::
