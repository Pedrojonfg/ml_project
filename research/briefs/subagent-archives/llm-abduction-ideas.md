# Archive: llm-abduction-ideas
**Agent ID:** 373e845a-bc1b-46fd-a2be-f7e0ef5712e6
**Title:** Research LLM abduction

---

(Canonical full brief: `../research-brief-llm-limits-compositionality-abduction.md`)

# Research Brief: LLM Limits / Compositionality / Abduction Cluster
**Depth**: wide  
**Date**: 2026-10-11  
**Cluster**: LLM limitations, compositionality, abduction, OOD reasoning, mech-interp lite, benchmark design  
**Constraints**: real dataset + ML analysis; course methods + stretch; ~6 weeks; oral-friendly; originality/ambition graded; health veto; no ChatGPT-API-only wrappers; AI prose banned, coding AI OK

## Executive Summary

The strongest projects **operationalize a philosophical claim as a measurable OOD failure**, then run a **classical vs neural bake-off** with controlled splits and a short stretch (probing, generation, or lite circuits). Best oral narrative: *“can models jump?”* via SCAN/COGS. Best Pedro–Mario joint: **abduction (αNLI/ART) + generative explanation**. Best philosophy-NLP without becoming an essay: **adversarial ARCT warrants**. Avoid full ARC-AGI, full LiveCodeBench, and pure API evals as primary deliverables.

## Fit Filter (this cluster)

| Criterion | Pass signal |
|-----------|-------------|
| Pedro | Abduction, “can’t jump”, philosophy if cool + empirical |
| Mario | NLP interest high; generative methods welcome as stretch |
| Course | Must include classical (logistic/trees/kernels/PCA) + NN; stretch OK |
| Oral | One crisp RQ + one memorable demo figure |
| Ambition | New split, diagnostic, or circuit story—not “we ran GPT-4 on X” |
| Veto | No health/clinical |

---

## Ranked Top 3

### #1 — Operationalize “models can’t jump”: compositional OOD on SCAN + COGS/ReCOGS
**RQ.** Do sequence models that succeed in-distribution fail when required to systematically recombine a held-out primitive (Lake & Baroni’s *jump*), and does the same failure appear in more linguistic COGS/ReCOGS splits?

**Datasets.** SCAN (esp. *add-jump*, *length*); COGS or ReCOGS generalization splits (HF/public releases). Optional tiny Colors dataset for low-resource story.

**Methods (classical + NN).**
- Classical: bag-of-n-grams / sparse TF-IDF → logistic or linear SVM for command→action *classification of first action / length / primitive ID* as diagnostic baselines; trees on handcrafted compositional features (presence of modifiers, nesting depth).
- NN: LSTM/GRU seq2seq; small Transformer encoder–decoder; optional frozen embeddings + probe.
- Stretch: few-shot eval of a small open LM (e.g. 1–3B) on the same splits *without* treating API chat as the model; CompSub-style augmentation as ablation if time.

**Ambition.** Publishable-feeling failure analysis: IID vs systematic OOD accuracy, seed variance, error typology (“knows jump, can’t compose jump twice”). Directly cites the Fodor/systematicity thought experiment that Pedro cares about—but as **ML measurement**.

**Feasibility (6 weeks).** High. Datasets tiny/synthetic; training is laptop/Colab-scale; literature is dense but demos are crystal clear for oral.

**Fit.** Excellent for Pedro; Mario gets solid NLP + optional generative decoding. Oral gold.

**Trade-offs.** Synthetic; some reviewers say SCAN is “solved” by specialized architectures—counter by (a) including COGS/ReCOGS, (b) emphasizing **diagnostic comparison** and **when** classical beats neural on OOD, (c) not claiming SOTA.

---

### #2 — Abduction as OOD reasoning: αNLI (ART) + compositional stress tests
**RQ.** When do models choose the more plausible abductive hypothesis (αNLI), and do they fail when observations require combining unfamiliar middle events or conflicting cues—i.e., an abductive “jump”?

**Datasets.** ART / `allenai/art` (αNLI MC); GEM/ART for αNLG stretch. ~20k contexts / 200k hypotheses; classic BERT ~69% vs human ~91%.

**Methods (classical + NN).**
- Classical: lexical overlap / embedding cosine features between (O1,O2) and each hypothesis; logistic regression, random forest, gradient boosting; PCA on sentence embeddings then linear classifier.
- NN: fine-tune DistilBERT/RoBERTa-base for pairwise ranking; optional Siamese encoder.
- Stretch (Mario): αNLG with a small seq2seq or instruction-tuned open model; evaluate with ROUGE/BERTScore **plus** human-style rubric on a small held-out set (20–50 items) you score yourselves.
- Originality lever: **construct an OOD split** (e.g., hold out hypothesis lexical clusters, temporal distance between O1–O2, or require multi-hop COMET-style inferences)—not pure philosophy essay.

**Ambition.** Ties Peirce/abduction to a standard NLP task; gap to humans is still narratively strong; your OOD split is the originality.

**Feasibility.** High–medium. Classification track is clean; generation track needs metric discipline (don’t overclaim BLEU = reasoning).

**Fit.** Best joint Pedro+Mario theme. Oral: one example where the correct hypothesis is non-obvious.

**Trade-offs.** ART is older; SOTA LMs may score higher now—frame as **fine-tuned small models + classical** under controlled compute, and stress **your** hard split. Avoid closed API as primary system.

---

### #3 — Philosophy-NLP without the essay: adversarial ARCT warrants + cue hunting
**RQ.** Can models recover the implicit warrant that makes a claim follow from a premise—and are high scores just spurious cue exploitation (negation/lexical artifacts)?

**Datasets.** Argument Reasoning Comprehension Task (ARCT, ~2k); **adversarial ARCT** (Niven & Kao / IKMLab `arct2`: train-swapped, adv-negated splits). Argument Annotated Essays as optional mining side-task if you want component labeling.

**Methods (classical + NN).**
- Classical: cue features (negation counts, warrant–claim overlap, length, polarity lexicons) → logistic / trees; show cues alone ≈ neural on original data.
- NN: BiLSTM attention (SemEval-era) + fine-tuned BERT; reproduce collapse to ~chance on adversarial test.
- Stretch: train a **cue detector** vs **warrant reasoner**; or simple probing of [CLS] for cue presence.

**Ambition.** Directly in philosophy of argument (Toulmin warrants) with hard empirical lesson: high accuracy ≠ understanding. Originality via modern small LMs + thorough cue audit, not a new theory paper.

**Feasibility.** High. Small data; known pitfalls are a feature (you study them).

**Fit.** Pedro philosophy-NLP sweet spot; Mario NLP methods. Oral: one premise/claim/warrant triple on a slide.

**Trade-offs.** Dataset small → variance; less “generative” unless you add warrant generation as stretch. Don’t drift into pure corpus linguistics without modeling.

---

## Additional Designs (ranked 4–11)

### #4 — Parametric vs retrieved knowledge: FaithEval / NQ-Swap conflicts
**RQ.** When context contradicts parametric memory, do models follow evidence—and can classical detectors predict *which* source they will trust?

**Datasets.** FaithEval (counterfactual / inconsistent / unanswerable contexts); NQ-Swap; optional ConflictQA.

**Methods.** Classical: conflict features (entity swap distance, embedding disagreement between context and closed-book answer) → logistic/RF predicting “follows context” vs “follows memory”. NN: fine-tune reader; probe open small LM with/without context. Stretch: residual-stream or layer-probe on a tiny model (lite mech-interp).

**Ambition / feasibility / fit.** High ambition, medium–high feasibility; strong ML story; slightly less “abduction/jump” unless framed as “jumping to prior belief.” Oral-friendly with moon/marshmallow-style counterfactuals.

**Trade-off.** Crowded literature; must own a **classifier/diagnostic**, not only LLM prompting.

---

### #5 — Hallucination detection as supervised ML (HaluEval + FaithDial critic)
**RQ.** Can classical and neural critics detect hallucinated vs faithful statements better than generative self-check heuristics?

**Datasets.** HaluEval (QA/dialogue/summarization hallucination labels); FaithDial (faithful dialogue edits) for critic training; optional BEGIN.

**Methods.** Classical: n-gram overlap with source, entity precision, embedding entailment scores → logistic/SVM/XGBoost. NN: cross-encoder NLI-style critic; contrast with generative LM “is this faithful?” prompts on open models only.

**Ambition / feasibility / fit.** Solid course-methods match; Mario generative contrast; less philosophical unless tied to “confabulation ≠ abduction.”

**Trade-off.** Easy to become metric soup—pre-register primary F1 on one task.

---

### #6 — Counterfactual conditionals: CRASS (BIG-bench) + CLadder rung analysis
**RQ.** Do models fail specifically on Pearl’s rung-3 counterfactuals vs rung-1 association, and do classical causal-graph solvers dominate verbalized LLMs?

**Datasets.** CRASS / BIG-bench `crass_ai` (small MC); CLadder (~10k NL causal questions with symbolic oracle).

**Methods.** Classical: implement/use simple SCM/do-calculus templates on symbolic form (or logistic on graph-features if you extract structure). NN: fine-tune classifier on verbalized CLadder; compare open LM few-shot. Stretch: CausalCoT-style structured prompting as baseline, not as the only method.

**Ambition / feasibility / fit.** High conceptual ambition (philosophy of causation); medium feasibility (CLadder parsing, verbalization noise). Good oral if you show one graph → three rungs.

**Trade-off.** Risk of becoming a prompting bake-off—keep a **trained** model + classical oracle comparison.

---

### #7 — Analogy as structured abduction: E-KAR + BATS vs SCAN-analogy
**RQ.** Do embedding arithmetic / classical relational features solve surface analogies (BATS) but fail holistic scientific/creative analogies (SCAN-analogy / E-KAR)—a “jump” across domains?

**Datasets.** BATS; Scientific & Creative Analogy (SCAN-analogy, not Lake SCAN); E-KAR (EN subset ~1.2k MC + explanations).

**Methods.** Classical: vector offset, pairwise similarity features, RF. NN: fine-tune MCQA encoder; optional explanation generation for Mario.

**Ambition / feasibility / fit.** Nice philosophy (analogy ≈ abduction of structure); medium data size; oral with atom/solar-system example.

**Trade-off.** E-KAR explanations hard to auto-eval; keep MC accuracy as primary.

---

### #8 — Lite mechanistic interpretability: induction heads / toy IOI on compositional copies
**RQ.** When a tiny transformer learns to “complete the pattern,” is the mechanism an induction circuit—and does that circuit fail under OOD compositional variants?

**Datasets.** Synthetic: random-token repeat sequences (Olsson-style); optional symbolic IOI; optional map of induction success → SCAN-like copy tasks.

**Methods.** Train 1- vs 2-layer attention-only Transformers; classical: logistic probes on residual stream for “previous token” / “duplicate” features; ablations / attention pattern metrics. Compare to n-gram / KNN baseline that also copies.

**Ambition / feasibility / fit.** High originality for a course; medium–high technical risk; oral demos of attention maps are excellent. Stretchy vs syllabus but still real training.

**Trade-off.** Can feel distant from “philosophy NLP” unless explicitly linked to compositionality/copying-as-fake-reasoning. Scope ruthlessly (toy only).

---

### #9 — BIG-bench diagnostic mini-suite + meta-predictor of failure
**RQ.** Across a fixed subset of BIG-bench Lite / reasoning tasks (include `crass_ai`, a compositionality-tagged task, an abduction-like task), can classical meta-features predict which items models will miss?

**Datasets.** BIG-bench Lite (24 JSON tasks)—**subset 3–5 tasks**, not all 200+.

**Methods.** Run small open models + fine-tuned baselines; build item-level feature store (length, vocab rarity, negation, # hops) → logistic/trees predicting error. NN: single multi-task head if time.

**Ambition / feasibility / fit.** Ambition via **benchmark design / meta-analysis**; feasibility OK if task count is capped. Fits “LLM limitations” cluster.

**Trade-off.** Easy to look shallow (“we evaluated…”). Must ship the **error predictor** and analysis, not leaderboard tourism.

---

### #10 — Design a tiny “Abductive Jump” benchmark (originality-max)
**RQ.** Can we construct a minimal dataset where success requires inferring an unobserved binder that compositionally explains two observations, and show systematic failure of bag-of-words vs seq models vs small LMs?

**Datasets.** **You build** 500–2000 synthetic or templated items (plus a small human-validated test); optionally seed templates from ART/COMET relations; release schema + splits (IID / lexical OOD / compositional OOD).

**Methods.** Same bake-off as #2; classical feature baselines mandatory; document construction validity (inter-annotator on 50 items).

**Ambition / feasibility / fit.** Highest originality; medium–high risk of messy data quality in 6 weeks. Best as **stretch sibling** to #2, or primary if team loves dataset design.

**Trade-off.** Grading risk if construction quality is weak—pair with a public dataset baseline.

---

### #11 — ARC-AGI / LiveCodeBench (managed, not primary)
**RQ (ARC).** Do program-synthesis or retrieval baselines beat neural guessers on a **tiny** public ARC subset when measured by exact grid match?  
**RQ (LiveCodeBench).** Does compositional library use predict failure on `code_generation_lite` for a small codegen model vs classical retrieval of similar solutions?

**Datasets.** ARC-AGI public eval subset (tens of tasks, not full contest); LiveCodeBench lite time-windowed slice.

**Methods.** ARC: classical DSL/search or object-centric features + RF; small NN pixel/CNN baseline; optional LLM only as one condition. Code: embedding retrieval + logistic difficulty model; fine-tune tiny codegen if GPU allows.

**Ambition / feasibility / fit.** High prestige, **low 6-week feasibility** as main project (eval harness, compute, contamination narrative). Mario generative interest helps for code; Pedro philosophy link is weaker for ARC unless framed as abstraction.

**Trade-off.** High chance of incomplete oral demo. Use only as **satellite experiment** under #1 or #9.

---

## Explicitly Deprioritize

| Idea | Why |
|------|-----|
| ChatGPT/Claude API as the only “model” | Violates “real ML”; graded as thin |
| Full ARC-AGI leaderboard chase | Scope/compute death |
| Full LiveCodeBench + many models | Harness + cost; little classical ML |
| Pure Peirce/Fodor essay | Course requires dataset + modeling |
| Health/clinical NLP | Hard veto |
| Multimodal CARV as main | Cool analogy story but vision stack + newness = scope risk |

---

## Method Palette (reuse across projects)

| Layer | Options |
|-------|---------|
| Classical | Logistic, linear SVM, RF/XGBoost, PCA + linear, TF-IDF/n-grams, hand features (negation, overlap, depth) |
| NN course-level | MLP, LSTM/GRU, small Transformer, DistilBERT fine-tune |
| Stretch | Open small LMs, probing/ablation, controlled data augmentation, tiny generative models |
| Eval | IID vs OOD splits, seed variance, error typology, calibration; generation only with automatic + small human check |

---

## Decision Guide (Pedro × Mario)

1. Want the cleanest oral + “can’t jump” slogan → **#1**.  
2. Want abduction + generative stretch → **#2** (optionally absorb #10 as stretch).  
3. Want philosophy of argument with empirical teeth → **#3**.  
4. Want hot LLM-systems angle → **#4**.  
5. Want mech-interp wow factor → **#8** (only if both enjoy low-level PyTorch).

**Recommended path:** commit to **#1 or #2** as spine; borrow one figure/method from **#3 or #4** for originality; ignore ARC/LiveCodeBench as core.

---

## Sources (key)

- Lake & Baroni (2018), SCAN — compositional “jump”  
- Kim & Linzen (2020), COGS; Wu et al., ReCOGS  
- Bhagavatula et al. (ICLR 2020), ART / αNLI / αNLG  
- Habernal et al. (NAACL 2018), ARCT; Niven & Kao adversarial ARCT  
- Frohberg & Binder, CRASS / BIG-bench `crass_ai`  
- Jin et al., CLadder (NeurIPS 2023)  
- Longpre et al., NQ-Swap; FaithEval (ICLR 2025)  
- Li et al., HaluEval; Dziri et al., FaithDial  
- E-KAR; BATS; Czulo et al. SCAN-analogy  
- Olsson et al., induction heads; Wang et al., IOI circuits  
- BIG-bench / BIG-bench Lite; LiveCodeBench; ARC-AGI public tooling  

---

## Open Questions for Team Sync

1. Prefer **synthetic clarity (#1)** or **commonsense abduction (#2)** as the spine?  
2. How far outside syllabus for Transformers / fine-tuning / probing (techo from decision 004)?  
3. GPU budget: Colab-only vs local? (Affects #8 and generative stretches.)  
4. Is releasing a tiny custom split (#10) worth one week of calendar risk?

