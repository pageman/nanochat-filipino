# AsPredicted step-by-step guide for Protocol P1.0

**What this is:** a click-level, field-level manual for turning the local P1.0 protocol into an actual AsPredicted pre-registration.  
**What this is not:** the pre-registration itself. Until you complete §7 and have a time-stamped PDF URL, nothing is registered.  
**Official site:** [https://aspredicted.org/](https://aspredicted.org/)  
**Companion protocol:** [PROTOCOL-project1-wikitext-tl39.md](PROTOCOL-project1-wikitext-tl39.md) (P1.1)  
**Do not file P1.0 answers.** Use [run-cards/aspredicted-answers-p1.txt](run-cards/aspredicted-answers-p1.txt) after [RECONCILE-p1.1.md](RECONCILE-p1.1.md).  
**Character cap:** 2,900 characters **per answer**. The 1,251-line protocol will not fit. You register a *compressed confirmatory plan* and point at a frozen hash of the long protocol.

AsPredicted is run by the Wharton Credibility Lab (University of Pennsylvania). It is a short, psychology-shaped form: eight scientific questions plus title / study type / data source. It produces a one-page time-stamped PDF with a unique URL. It does **not** issue a DOI. It does **not** accept file uploads. It does **not** let you edit after creation.

---

## 0. Decide whether AsPredicted is the right box

### 0.1 What AsPredicted is good for

- A timestamp that you stated H1–H4, the primary DV (`val_bpb`), the run matrix, and the exclusion rules *before* you trained.  
- A one-page PDF reviewers can open in ten seconds.  
- A private record until you choose to mint a shareable PDF.

### 0.2 What AsPredicted cannot do

| Need | AsPredicted | Do this instead or in addition |
|---|---|---|
| Upload the 1,251-line protocol | No | Freeze a git tag / OSF file with SHA256; put the hash in Q8 |
| DOI | No | OSF Registration if you need a DOI |
| Embargo that auto-publishes | No (stays private until you make a PDF) | OSF embargo (max 4 years) |
| Searchable catalog | No useful on-site search | Assume only people with the URL will find it |
| Amend in place | No | Reject + recreate, or file a dated deviation in the paper |
| Secondary-data template | No dedicated template | Answer Q1 as **Yes** (archival corpus exists) and explain |
| Pin nanochat commit + parquet SHA | No attachments | Put both in Q8 and in the frozen protocol |

**Recommended stack for P1.0:** AsPredicted (confirmatory one-pager) **plus** a frozen git tag of this repo (full protocol). AsPredicted alone is too small to carry P1.0.

### 0.3 When you are allowed to click Submit

You MAY submit only if **all** of the following are true:

1. You have not run `scripts.base_train` except a failed smoke that produced no `val_bpb` you will use.  
2. You have not computed `val_bpb` or `test_bpb` on a trained P1 model.  
3. You have not selected a winning depth after seeing likelihoods.  
4. You are willing to treat any later change as a **deviation**, not a silent edit.

You MAY have already: read Cruz & Cheng (2019), looked at the Hugging Face dataset *card*, written the protocol, cloned nanochat. That is design work, not outcome peeking.

You MUST treat as peeking (and then Q1 is an even stronger Yes): opening the parquet and computing split-level likelihoods, training a tokenizer and inspecting test fertility to *choose* vocab, running d4 and then changing H3.

**Hard stop:** if Gate I (primary pretrain) has started, do not create an AsPredicted that claims “no data collected” and do not pretend the registration preceded the run.

---

## 1. Freeze the protocol *before* you open the website

AsPredicted cannot hold the long protocol. Freeze it first so Q8 can cite an immutable object.

### 1.1 Stop editing confirmatory sections

Do not change these after the AsPredicted is created, except as a labeled deviation:

- RQ1–RQ5, H1–H4  
- Primary DV = `val_bpb`  
- Forbidden primary claims (CORE, train loss)  
- Document-level 70/15/15 hash split  
- Train-only tokenizer  
- Depth set {4, 6, 8, 12}, d24 out of primary  
- Test touched once after freeze

You MAY still fix typos in the long protocol. You MUST NOT change the confirmatory plan and keep the same AsPredicted number.

### 1.2 Hash the protocol file

From the repo root:

```bash
shasum -a 256 docs/PROTOCOL-project1-wikitext-tl39.md
git add docs/PROTOCOL-project1-wikitext-tl39.md docs/GUIDE-aspredicted-p1.md
git status
```

Create a tag only after you commit (commit when you choose; this guide does not commit for you):

```bash
git tag -a p1.0-aspredicted -m "Frozen P1.0 protocol at AsPredicted submission"
git rev-parse HEAD
git rev-parse p1.0-aspredicted
```

Write these four strings on paper or in `docs/run-cards/aspredicted-draft.md` **before** you submit:

- Protocol SHA256  
- Git commit SHA  
- Tag name `p1.0-aspredicted`  
- Date-time UTC

### 1.3 Draft offline in plain ASCII

AsPredicted counts **bytes after special-character encoding**. Word “smart quotes,” em dashes (`—`), and curly apostrophes can push you over 2,900 even when Word says you are under.

Rules for every paste:

- Use a plain-text editor, not Google Docs / Word.  
- Use straight quotes `"` and `'` only.  
- Use hyphen `-` not em dash.  
- Use `val_bpb` not Unicode subscripts.  
- No emoji.  
- Paste into a character counter that counts Unicode code points *and* then subtract ~50 as a safety margin.  
- Target **≤ 2,700 characters per box**.

### 1.4 Decide participating authors (max 5)

AsPredicted allows **up to 5 participating authors**. Each must approve by email before the registration is saved.

- Participating author = can approve, can later mint the public PDF.  
- Extra names go in Q8 as a list. They cannot mint the PDF.  
- If a coauthor never clicks the email, the registration is not completed. Nudge them or omit them from the participating list and name them in Q8.  
- You cannot add a participating coauthor later.  
- You cannot change answers later (only participating-author email updates).

For a solo P1.0: one email, no coauthor delay.

### 1.5 Choose the email you will still have in two years

Sign-in is email-based. If you lose the inbox, recovery is painful (`I no longer have access to the email account i have used in the past` on the homepage). Prefer an institutional address you control.

---

## 2. Click-by-click: create the draft on the site

Do this on a laptop, not a phone. Use a second window with this guide.

### 2.1 Open the site

1. Go to [https://aspredicted.org/](https://aspredicted.org/).  
2. If Cloudflare “security verification” appears, wait. Do not refresh in a loop.  
3. Click **New Pre-registration** (homepage also says “Create a New Pre-Registration”).

### 2.2 Enter email

1. You land on `create_email_enter.php`.  
2. Type the email from §1.5.  
3. Click **Continue**.  
4. Check the inbox (and spam) for an AsPredicted link.  
5. Open the link in the same browser. That *is* your login. There is no password to invent.

If the email does not arrive in 10 minutes: check spam, try a different address, do not create a second draft you will forget.

### 2.3 If you already have pre-registrations

Use **SIGN IN** / **Your Pre-registrations** on the homepage, same email-link flow. Do not create a duplicate P1.0.

### 2.4 Title, study type, data source

These appear around the eight questions (wording varies slightly by year; fill all of them).

**Title (recommended):**

```text
P1.0: Compute-appropriate Tagalog nanochat base on WikiText-TL-39 (held-out bits-per-byte)
```

**Type of study:** choose **Observational/archival study** or **Other**.  
If Other is free text, write: `computational language-modeling experiment on a public archival corpus`.

Do **not** choose Experiment, Survey, or Class project. There are no human participants.

**Data source:** choose **Other**.  
If free text: `Public Hugging Face dataset linkanjarad/Wikitext-TL39 (WikiText-TL-39; Cruz and Cheng 2019). Not Prolific, MTurk, or a university lab.`

### 2.5 Add participating authors (or skip)

If solo: leave coauthor fields empty and continue.  
If not: enter up to four additional emails. Warn them that an approval email is coming and that the registration will not exist until they click.

### 2.6 Work in this order

Fill Q1 last among the scientific boxes if the UI lets you, because Q1 is the honesty tripwire. Otherwise fill Q1 first with the archival Yes (see §3). Draft every other box in a local file, then paste. Do not compose long answers in the browser; a refresh can eat them.

---

## 3. Question 1 — Have any data been collected for this study already?

### 3.1 What they are asking

This is the most important box on the form. AsPredicted was built for lab/online experiments. “Data collected” means: do you already have the observations you will analyze?

For P1.0 the observations are **held-out bits-per-byte of models you have not trained yet**. The *corpus* was collected by Cruz and Cheng in 2019 and is public.

### 3.2 What you MUST select

Select **Yes** (data already exist / some or all data have been collected).

Selecting **No** is the common error. A reviewer who knows WikiText-TL-39 is a 2019 public dump will treat “No” as either ignorant or dishonest.

### 3.3 How to stay confirmatory after Yes

Yes does not kill the pre-registration if you state **what has and has not happened**. The confirmatory claim is: you have not yet produced the DV.

If the UI is radio-only with no text, put the paragraph in Q8. If Q1 allows a sentence, use the paste below.

### 3.4 Ready-to-paste (put in Q1 if there is a text box; else Q8)

```text
Yes. The pretraining corpus is archival and public: WikiText-TL-39 (Cruz and Cheng 2019), currently accessed as Hugging Face dataset linkanjarad/Wikitext-TL39. We did not collect those documents. For THIS study we have not yet (a) frozen a document-level train/val/test split and trained a tokenizer on it, (b) trained a nanochat language model, or (c) computed validation or test bits-per-byte (val_bpb, test_bpb). Those outcomes do not exist yet. This pre-registration is filed before any confirmatory training run (Protocol P1.0 Gate I). A d4 engineering smoke test, if run, will not be used to choose depth, hypotheses, or reported BPB.
```

### 3.5 If you already peeked

If you already computed `val_bpb` on a trained model, you cannot honestly pre-register H1–H4 as confirmatory. File AsPredicted only for **future** runs (new seeds, new corpus) and write in Q1 that exploratory training already occurred. Do not back-date.

---

## 4. Question 2 — Main question or hypothesis

### 4.1 What they want

One main question, written so a stranger can score whether you were right. Not five RQs and a literature review.

### 4.2 Pitfalls

- Listing RQ1–RQ5 without a primary.  
- Saying “we will explore Tagalog LMs.”  
- Predicting “GPT-2 grade” or CORE.  
- Claiming you will recover Cruz and Cheng’s exact 2019 document IDs.

### 4.3 Ready-to-paste

```text
Primary question: On a document-held-out split of WikiText-TL-39, does a compute-appropriate nanochat GPT (depth D in {4,6,8,12}, 32768 BPE trained on train documents only, official tok_train/base_train/base_eval) achieve validation bits-per-byte (val_bpb) strictly below both (i) a randomly initialized model of the same depth and (ii) a train-estimated UTF-8 byte-unigram baseline?

Confirmatory hypotheses:
H1. The trained model val_bpb is strictly below both baselines.
H2. A tokenizer trained on train+val+test will show lower test fertility (tokens/byte) than a train-only tokenizer (tokenizer leakage); measured once, not used to pick the primary tokenizer.
H3. At a one-epoch token budget, val_bpb improves from D=4 to a minimum in {6,8} and does not improve further at D=12.
H4. A second epoch at the winning depth D* lowers val_bpb; a fourth epoch increases the train-val BPB gap (overfit).

Out of scope (not confirmatory): English DCLM CORE, dengue/hate-speech accuracy, OSCAR/TLUnified, d24/d26 speedrun models, chat SFT.
```

---

## 5. Question 3 — Key dependent variable(s)

### 5.1 What they want

Name the DV, the unit, the instrument, and the selection rule.

### 5.2 Ready-to-paste

```text
Primary DV: validation bits-per-byte (val_bpb_full) on the held-out validation documents, using the official nanochat token_bytes.pt conversion so the number is tokenizer-vocab invariant. Computed once on the full val set after training (not the truncated --eval-tokens stream used during optimization).

Secondary confirmatory DV: test_bpb, same formula and context/stride as val, computed ONCE after the winning checkpoint is frozen. Model selection uses val_bpb only.

Definition: mean token NLL / (ln(2) * mean UTF-8 bytes per token), special tokens excluded as in nanochat.

Baselines (same val bytes): (1) untrained same-architecture model; (2) UTF-8 byte-unigram fitted on train text only.

Explicitly not DVs for confirmatory claims: training NLL, token perplexity (appendix only, with tokenizer hash), DCLM CORE, MMLU/ARC/GSM8K, anecdotal sample quality, downstream classification.

Measurement stack: karpathy/nanochat scripts.base_train and scripts.base_eval / loss_eval; nanochat commit pinned in Q8; isolated NANOCHAT_BASE_DIR; no ClimbMix download.
```

---

## 6. Question 4 — Conditions / assignment

### 6.1 What they want

This box says “participants.” You have none. Translate to **experimental factors you assign**.

### 6.2 Ready-to-paste

```text
No human participants. Units are Wikipedia documents and trained models.

All confirmatory runs share: same parquet snapshot, same document hash-split (seed 20260816, 70/15/15), same train-only 32768 BPE, same nanochat commit, detokenized Moses text, --core-metric-every=-1.

Assigned conditions (model runs):
- MUST: depth D=4, 1 epoch, seed 0
- MUST if tokens/params allow (Protocol P1.0 Gate G): D=6 and D=8, 1 epoch, seed 0
- SHOULD if Gate G allows: D=12, 1 epoch, seed 0
- SHOULD: 2 epochs at winning depth D*
- MAY: 4 epochs at D*; extra seeds 1 and 2 at D* (required if we claim a depth ranking)

D=24/26 are not confirmatory conditions.

Assignment of documents: deterministic hash u=sha256(f"{SPLIT_SEED}:{doc_id}") to train/val/test. Not a line-level random split. Test documents never enter tokenizer training or base_train shards.
```

---

## 7. Question 5 — Analyses

### 7.1 What they want

The exact comparison that decides H1–H4. Not “we will look at loss curves.”

### 7.2 Ready-to-paste

```text
H1: Compare trained val_bpb_full to random-init val_bpb and to byte-unigram val_bpb. Success if trained < both. Point estimates; no p-value. Difference < 0.01 BPB is not interpreted without a seed sweep.

H3: Among completed one-epoch MUST/SHOULD depths, D* = argmin val_bpb_full. Ranking is exploratory with 1 seed and confirmatory only if seeds 0,1,2 are run at those depths. Report mean +/- sample SD if >=3 seeds.

H4: At D*, compare val_bpb_full at 1 vs 2 epochs (and 4 if run). Overfit if train-val BPB gap increases at 4 epochs.

H2: Compare test-set bytes/token of train-only vs all-split tokenizers. Primary LM uses train-only tokenizer regardless.

Test_bpb: computed once on the val-best checkpoint; no retuning.

Reporting table: run name, D, P, tokens_seen, rho=tokens_seen/P, epochs, val_bpb_full, test_bpb, GPU-hours, nanochat commit.

Software: official nanochat trainer only. --num-iterations set from T_train and batch so epoch count is explicit. --eval-tokens <= 50% of T_val during training; final val_bpb_full uses all val tokens.

No CORE in the primary table. If base_eval emits CORE, it is appendix-only and labeled English DCLM, not a Tagalog result.
```

---

## 8. Question 6 — Outliers and exclusions

### 8.1 What they want

Rules you will apply *without looking at BPB*.

### 8.2 Ready-to-paste

```text
Document exclusions (before training): drop a reconstructed article only if n_chars < 40 or n_chars > 200000. If drops exceed 5% of documents, stop and inspect; do not train. Do not drop stubs for being short.

Split exclusions: any document whose id appears in more than one split (must be 0). Exact sha256(text) duplicates across splits: 0. If character-share of a split falls outside 12-18% (val/test) or 65-75% (train), replace the split with a length-tertile stratified hash split (same seed) and label it.

Run exclusions (do not enter the confirmatory table): NaN/Inf val_bpb; data-dir contamination (ClimbMix/English shards or fluent English-Congress samples); shard SHA256 change mid-run; any run that used test documents in tok_train or base_train; smoke-test d4 (30 steps) used only as an engineering gate.

Checkpoint rule: keep last and best-val. Test set is write-protected and read once.

We will not exclude depths post hoc because they look bad. If Gate G forbids a depth (rho too low), that depth is skipped before training and recorded, not dropped after seeing BPB.
```

---

## 9. Question 7 — Sample size / stopping

### 9.1 What they want

A rule that tells a stranger when you stop collecting. “Until it looks good” is invalid. They say you need not justify, but you must be precise.

### 9.2 Ready-to-paste

```text
Corpus size is fixed: the public WikiText-TL-39 parquet (linkanjarad/Wikitext-TL39; expected ~1.52e6 rows, ~119MB). We do not collect more documents for P1.0. We do not add OSCAR, CC-100, or extra Wikipedia dumps in this registration.

Document split: 70% train / 15% val / 15% test by hash (seed 20260816), document as the unit.

Training sample (tokens seen): one epoch = one pass over T_train BPE tokens measured after tokenizer training. Primary confirmatory runs are 1 epoch. Optional 2 and 4 epochs only at D* as specified in Q4.

Number of confirmatory model runs: 2 to 4 one-epoch depths (D=4 plus those allowed by Gate G: skip D if T_train/P < 8 unless we instead declare a multi-epoch d4 as primary before training). Plus optional 2-epoch and 4-epoch runs at D* and optional 2 extra seeds.

Stopping: stop a run on NaN/Inf, preemption without checkpoint, or shard checksum change. Do not stop a one-epoch run early because val_bpb looks good. For multi-epoch runs, stop if val_bpb at epoch k exceeds val_bpb at epoch k-1 by more than 0.02.

We will not download ClimbMix or otherwise grow the corpus to chase a better number.
```

---

## 10. Question 8 — Anything else

### 10.1 What this box is for

Everything AsPredicted’s psych template cannot express: archival nature, nanochat pin, protocol hash, forbidden claims, ablations labeled exploratory.

### 10.2 Ready-to-paste (fill the hashes at submit time)

```text
Full protocol: nanochat-filipino docs/PROTOCOL-project1-wikitext-tl39.md SHA256=[PASTE] git=[PASTE] tag=p1.0-aspredicted. That document is the methods record; this form is the confirmatory subset.

Data: do not use the dead S3 zip (HTTP 404). Primary file is the HF parquet. The mirror is a single train split; we reconstruct =Title= articles and re-split. We do not claim we recovered the 2019 document IDs.

Pipeline: official nanochat only. NANOCHAT_BASE_DIR isolated. Never python -m nanochat.dataset (ClimbMix). Last parquet file is val; we write >=2 train shards plus val last. Test shards stay outside the train dir.

Tokenizer: 32768 BPE, train docs only, Moses detokenize default (@-@ -> -).

Exploratory ablations (not confirmatory unless a new AsPredicted is filed): Moses-as-is; line-level split; English nanochat tokenizer; vocab 8192; max_seq_len 2048.

Downstream dengue/hate-speech probes are later protocols (P8/P9), not this study.

Additional authors not in the 5-person approval list: [NONE or NAMES].

Contact: [YOUR EMAIL].
```

After pasting, replace `[PASTE]` and `[YOUR EMAIL]`. Re-count characters.

---

## 11. Pre-submit checklist (do this in the browser, slowly)

Print or tick:

- [ ] Every box is ASCII, ≤ 2,700 characters.  
- [ ] Q1 is **Yes** (archival corpus), with the no-training-yet sentence.  
- [ ] Primary DV is `val_bpb_full`, not CORE, not train loss.  
- [ ] d24 is not a confirmatory condition.  
- [ ] Test-once rule is in Q3 or Q5.  
- [ ] Protocol SHA256 and git SHA are real, not the word PASTE.  
- [ ] Title names WikiText-TL-39 and nanochat.  
- [ ] Study type is archival/other, not Experiment.  
- [ ] Coauthor emails are correct (or none).  
- [ ] You have not started Gate I.  
- [ ] You saved a local copy of all eight answers in `docs/run-cards/aspredicted-answers-p1.txt`.

Save the local copy **before** you click the final button. AsPredicted will not give you a Word file of the draft.

---

## 12. Submit and coauthor approval

### 12.1 Click the create / submit control

Wording is typically **Create** / **Submit** / **Register**. After this, **answers cannot be edited**.

### 12.2 What happens next

1. You receive a confirmation email.  
2. Each participating coauthor receives an approval email.  
3. The pre-registration is **not finished** until all participating authors approve.  
4. If someone never approves: you wait, or you reject and recreate without them (they can be listed in Q8).  
5. Rejected drafts are deleted; the form is pre-filled so you can resubmit. That is the only “edit” path. See [https://aspredicted.org/messages/edit.php](https://aspredicted.org/messages/edit.php).

### 12.3 After approval, it is still private

Private means: no public URL, no Wayback copy, no reviewer access. That is intentional (AsPredicted “why private” policy: you share when you choose, often at paper submission).

**Private is not the same as registered-for-reviewers.** A reviewer cannot verify a private-only record. You still need §13 when you want the timestamp to be *usable*.

---

## 13. Mint the PDF (this is the actual citable object)

### 13.1 When to mint

| Moment | What to do |
|---|---|
| Right after approval | Optional: mint an **anonymous** PDF and store the URL in the run card. This is the first time a third party *could* see it if they had the URL. |
| Paper / thesis submission | Include the PDF URL. Switch to named authors if the venue wants names. |
| After publication | Leave it public. Public PDFs are copied to the Internet Archive. |

Minting a PDF is the act that creates a **permanent URL**. AsPredicted’s terms: once a PDF/URL exists it cannot be deleted, even if created in error. The URL looks like `https://aspredicted.org/b3c3d-e41h.pdf` (example pattern from their help).

### 13.2 Anonymous vs named

You can regenerate the PDF with or without author names. The URL stays the same class of object; treat the first mint as irreversible publicity. Assume search engines may index it once it is a shareable PDF (their terms say to assume this).

### 13.3 What to store locally

In `docs/run-cards/aspredicted-p1.md`:

```text
AsPredicted number: #
PDF URL:
Anonymous: yes/no
Created (UTC):
Approved (UTC):
PDF minted (UTC):
Protocol SHA256:
Git commit:
```

Also download the PDF and put a copy in `artifacts/` (gitignored if you prefer privacy until mint). The local PDF is a backup; the URL is the proof.

### 13.4 How to cite

In the paper:

> We pre-registered the confirmatory plan on AsPredicted (https://aspredicted.org/XXXX.pdf). The full methods protocol (hash `...`) is in the project repository, tag `p1.0-aspredicted`.

In text when results differ:

> Contrary to H3, depth 12 had the lowest val_bpb. We report this as a deviation from AsPredicted #N.

That “contrary to / unexpectedly / in addition we also ran” language is what AsPredicted’s homepage is for.

---

## 14. After registration: how to live with a frozen plan

### 14.1 Allowed

- Execute Gates A–L as written.  
- Skip a depth because Gate G (tokens/params) forbids it *before* training.  
- Label extra analyses “exploratory” in the paper.  
- File a new AsPredicted for a new study (CC-100, OSCAR, P8/P9).

### 14.2 Forbidden

- Edit the AsPredicted.  
- Quietly change H3 after seeing d12 win.  
- Train, then register, then pretend the date is earlier.  
- Use the smoke-test BPB as the confirmatory number.  
- Add ClimbMix because val_bpb was disappointing.

### 14.3 If you must change the plan

1. Do not edit. You cannot.  
2. Either **reject before approval** and resubmit (§12.2), or  
3. After approval: keep #N as the original, write a dated `docs/run-cards/deviation-YYYYMMDD.md`, and in the paper say “we deviate from AsPredicted #N as follows.”  
4. If the change is a new confirmatory claim, file **AsPredicted #N+1** before that run.

### 14.4 Lost email

Use the homepage link “I no longer have access to the email account i have used in the past.” Do this before you lose the inbox if you are graduating / changing jobs: add a second participating author with a stable address next time (too late for #N).

---

## 15. Granular execution list (do in this order)

1. Read this guide and Protocol P1.0 §1–§4.  
2. Confirm Gate I has not started.  
3. Freeze confirmatory text; stop editing H1–H4.  
4. SHA256 the protocol file.  
5. Commit and tag if you are ready (or at least record the working-tree hash).  
6. Write all eight answers in `docs/run-cards/aspredicted-answers-p1.txt` in ASCII.  
7. Count characters; cut to ≤ 2,700 each.  
8. Replace `[PASTE]` hashes.  
9. Decide participating authors (≤ 5).  
10. Open https://aspredicted.org/  
11. New Pre-registration.  
12. Enter email; open the login link.  
13. Set title, archival study type, Other data source.  
14. Paste Q2–Q8, then Q1 = Yes plus the archival paragraph.  
15. Run the §11 checklist.  
16. Save the local answers file again.  
17. Submit.  
18. Approve from your email if required.  
19. Wait for coauthors.  
20. Record the AsPredicted number in the run card.  
21. Optionally mint the anonymous PDF and store the URL.  
22. Only then start Gate A / data download for the confirmatory run.  
23. When writing results, quote #N and list deviations in plain language.

---

## 16. Limits you should tell a reviewer yourself

AsPredicted #N will prove you filed *these eight boxes* at *this time*. It will not prove:

- that the 1,251-line protocol was unchanged (unless you also froze the git hash in Q8 and that object is still retrievable);  
- that you did not train privately before filing (Q1 is an honor statement);  
- that the analysis is peer-reviewed (it is not a Registered Report);  
- that the record has a DOI.

If a venue wants a DOI and an embargo, file an OSF registration **in addition**, using the same text, after or at the same time. Do not file OSF *after* seeing results and call it the original plan.

---

## 17. Official pages (re-check if the UI moved)

- Home / create: https://aspredicted.org/  
- Create (email): https://aspredicted.org/create_email_enter.php  
- Help (2900-char note, PDF privacy): https://aspredicted.org/help  
- Editing / reject-to-revise: https://aspredicted.org/messages/edit.php  
- More than 5 authors: https://aspredicted.org/messages/authors5.php  
- Terms (private until PDF; no delete after URL; Wayback for public): https://aspredicted.org/terms@  

UI copy changes. If a label differs, follow the numbered scientific questions; they have been stable across public PDFs (#10917 through #214824 and later): data already collected; hypothesis; DVs; conditions; analyses; exclusions; sample size; other.
