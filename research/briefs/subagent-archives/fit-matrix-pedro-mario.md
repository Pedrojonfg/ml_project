# Archive: fit-matrix-pedro-mario
**Agent ID:** 1e2632d5-c50f-4961-84a4-fed2b3414f0a

---

# FIT MATRIX — Pedro × Mario (IE ML Project)

**Purpose:** Score candidate projects; do **not** pick the final project here.  
**Constraint:** Hard veto = health/omics. Finance only if innovative (Pedro) / natural fit (Mario).

---

## 1. Overlap heatmap narrative (where to hunt)

Think of the joint space as a heat map over domains × method stacks. Bright zones = both can defend joy + syllabus fit without forcing a veto or a “generic student ML” trap.

### Hot (hunt first)

| Zone | Why it lights up | Method stack that fits both |
|------|------------------|-----------------------------|
| **Robotics + perception / control-adjacent ML** | Pedro 10 / Mario 9; CyPhy + open-source CV signal; Mario gets model comparison + clear metrics | Trees/NN/deep + RL or classical baselines; optional PINNs if dynamics known |
| **Physics-informed / scientific ML (PINNs, surrogate models, hybrid models)** | Pedro core identity; Mario physics 8 + methodological curiosity; strong oral story (“physics prior + data”) | PINNs, NN surrogates, GP/Bayesian optional (Pedro likes; Mario indifferent — use sparingly or as one arm) |
| **Quantum-adjacent ML (simulation, embedding, hybrid classical–quantum framing)** | Both 8–10; deeptech credibility; differentiable if scoped to classical ML + quantum-inspired / small sim | Classical ML + clear quantum *problem framing*; avoid “we need a real QPU” as blocker |
| **Satellite / Earth observation + climate-adjacent ML** | Pedro satellite + climate 7; Mario climate 7 / vision 7; public datasets often strong | Vision/tabular + temporal models; unsupervised/pretrain hooks for Mario |
| **Vision with a non-generic task** | Pedro 9; Mario 7; open-source CV signal; “speechless researchers” if problem is unusual | Deep + classical baselines; strong eval protocol (Mario’s success definition) |

### Warm (good if scoped well)

| Zone | Condition to stay warm |
|------|------------------------|
| **Finance + ML that is *innovative*** | Not churn prediction / generic credit scoring. Needs a novel data view, market microstructure quirk, recommenders-with-a-twist, or physics/robotics-adjacent finance metaphor that Mario can own analytically |
| **NLP × robotics / physics / education tooling** | Mario NLP 9; Pedro education 9. Warm only if NLP is *instrument* (e.g. structured extraction for sim logs, curriculum, docs→features), not “fine-tune a chatbot” |
| **Recommenders in a deeptech context** | Mario strength; Pedro engages if recs sit on satellite scenes, lab assets, experiment configs, open-source CV datasets — not Netflix clones |
| **Abduction / “LLMs can’t jump” curiosity** | Pedro joy spike; keep as *research question or analysis chapter*, not sole deliverable unless Mario gets crisp hypotheses + baselines |

### Cool (pass unless a killer dataset appears)

- Pure classical finance / banking KPIs without innovation  
- Generic Kaggle vision or tabular “compare XGBoost vs NN”  
- Neuro / health / omics (Mario hard veto; do not negotiate)  
- Pure Bayesian theory showcase (Pedro joy, Mario indifference → asymmetric grind)  
- VC-as-product (interesting chat, weak 6-week ML artifact)

### Heatmap story in one line

**Hunt where robotics/vision/physics priors meet public or lab-accessible data, with Mario owning the evaluation spine and Pedro owning the non-generic scientific hook.**

---

## 2. Conflict zones and how to resolve

| Conflict | Pedro pole | Mario pole | Resolution rule |
|----------|------------|------------|-----------------|
| **Ambition vs finishability** | Outside syllabus 10; invent; speechless researchers | Outside 8; reproduce paper; well-defined + comparison | Cap invention to **one** novel hook; rest = reproduce + extend + ablate. Score Feasibility ≥7 or kill. |
| **Research prestige vs portfolio clarity** | Portfolio 10 / research 10 / impact 9 | Portfolio 7 / research 5 / impact 5 | Dual-output: (A) crisp demo + metrics table for portfolio; (B) short “research memo” / novelty claim. Never optimize only for a paper. |
| **Bayesian/GP depth** | High joy | Indifferent | At most **one** Bayesian/GP experiment; default stack = trees + NN/deep + (PINN or RL if justified). |
| **Finance domain** | Only if innovative | Natural domain | Finance projects must pass Pedro’s “innovative” gate **and** Mario’s data/definition gate — else drop. |
| **Success aesthetic** | Wow researchers | Original + defined + data + comparison + analysis | Oral defense script: Mario opens with problem/data/metrics; Pedro closes with why the scientific framing is non-obvious. |
| **Work rhythm** | Mixed flexible | Mixed + **frequent short check-ins** | Process constraint (not topic): weekly mini-demos, shared board of “done this week,” freeze scope at week 2. |
| **Easy path temptation** | easy-path 0 | easy 4 | If a candidate scores Easy >6 for both, treat as **anti-fit** unless Differentiability ≥8. |
| **Health adjacency** | — | Hard veto | Instant discard; no “adjacent biomarker” loopholes. |

**Governance for the pair:** Pedro has veto on *genericness*; Mario has veto on *undefined problem / weak data / health*; jointly veto if 6-week Feasibility <6.

---

## 3. Scoring rubric (weights sum = 1.00)

Score each criterion **1–10**. Final = weighted sum. Use the same rubric for every candidate; do not invent projects here — only score them when listed elsewhere.

| Criterion | Weight | What “10” looks like | What “3” looks like |
|-----------|--------|----------------------|---------------------|
| **Ambition** | **0.12** | Research-adjacent invent or sharp extension; might impress domain researchers | Syllabus homework + mild twist |
| **Dataset quality** | **0.15** | Accessible in week 1; licenses clear; enough volume/labels or strong unsupervised path; leakage controllable | Scraped mess, paywall, or “we’ll collect later” |
| **Course-articulability** | **0.10** | Maps cleanly to IE ML methods + learning outcomes; easy to explain to faculty | Feels like an ECE/physics thesis with ML sprinkled on |
| **Pedro joy** | **0.15** | Physics/robotics/quantum/vision/deeptech; invent signal; not finance-generic | Generic applied ML; pure recsys/finance vanilla |
| **Mario joy** | **0.12** | Clear definition, comparison theater, finance/recsys/NLP/robotics hooks; analysis room | Fuzzy research art project with no eval spine |
| **Feasibility (6 weeks)** | **0.18** | MVP by week 3; stretch goals optional; compute & data realistic | Depends on lab access, QPU, new hardware, multi-month labeling |
| **Differentiability** | **0.10** | Won’t look like 50 other student repos; portfolio-readable uniqueness | Another churn / CIFAR / house-price variant |
| **Oral-defendability** | **0.08** | Crisp claim → method → evidence → limitation; both can speak | “We tried many models”; hand-wavy novelty |

### Interpretation bands (joint score)

| Score | Label | Action |
|-------|-------|--------|
| **≥ 8.0** | Strong fit | Shortlist; pressure-test Feasibility + Dataset only |
| **7.0–7.9** | Contender | Keep if Ambition band OK and no veto |
| **6.0–6.9** | Rescue needed | Re-scope dataset or shrink novelty hook |
| **< 6.0** | Drop | Unless one criterion was mis-scored |

### Tie-breakers (in order)

1. Feasibility (6w)  
2. Dataset quality  
3. Differentiability  
4. Pedro joy (anti-generic veto)  
5. Mario joy (analysis spine)

### Pre-score: **overlap zones** (not projects)

Zone scores = how fertile the *area* is for this pair before a concrete idea exists. Use as hunt priority, then score real candidates with the same rubric.

| Overlap zone | Amb | Data* | Course | Pedro | Mario | Feas* | Diff | Oral | **Weighted** | Hunt priority |
|--------------|-----|-------|--------|-------|-------|-------|------|------|--------------|---------------|
| Robotics + vision/control ML | 8 | 7 | 8 | 10 | 9 | 7 | 8 | 8 | **8.05** | **1** |
| Physics-informed / PINN–hybrid | 9 | 6 | 8 | 10 | 7 | 6 | 9 | 8 | **7.69** | **2** |
| Satellite / EO + climate ML | 8 | 8 | 8 | 8 | 7 | 7 | 8 | 8 | **7.73** | **2** |
| Quantum-adjacent (classical ML + Q framing) | 9 | 5 | 7 | 10 | 8 | 5 | 9 | 7 | **7.21** | **3** — only with locked dataset/sim |
| Innovative finance + ML / deeptech recsys | 7 | 7 | 8 | 6 | 9 | 7 | 7 | 8 | **7.25** | **3** — Pedro innovation gate |
| NLP as instrument (not chatbot) | 7 | 7 | 8 | 7 | 9 | 7 | 7 | 8 | **7.37** | **3** |
| Abduction / LLM-limits as *chapter* | 9 | 6 | 6 | 10 | 6 | 5 | 9 | 6 | **6.95** | **4** — attach to hotter zone |
| Generic finance / generic CV | 3 | 8 | 9 | 2 | 7 | 9 | 2 | 6 | **5.71** | **Kill** |
| Health / omics | — | — | — | — | — | — | — | — | **Veto** | **Kill** |

\*Data & Feasibility are *zone priors* (optimistic public/lab-accessible). Re-score per concrete dataset.

**Weighted example (Robotics + vision):**  
`0.12×8 + 0.15×7 + 0.10×8 + 0.15×10 + 0.12×9 + 0.18×7 + 0.10×8 + 0.08×8 = 8.05`

---

## 4. Portfolio vs research trade-off (this pair)

| Axis | Pedro | Mario | Joint implication |
|------|-------|-------|-------------------|
| Portfolio weight | 10 | 7 | Artifact must be **demoable + readable** (repo, figures, metrics). Non-negotiable. |
| Research weight | 10 | 5 | Research is **seasoning**, not the meal. One clear novelty or sharp reproduction+extension. |
| Impact | 9 | 5 | Prefer *credible* impact story (lab, open data, open-source) over NGO/startup theater. |
| Ambition | 10 | 7 | Bias ambitious **problem framing**, conservative **execution plan**. |
| Easy path | 0 | 4 | Reject comfort projects; accept Mario’s need for structure (milestones, comparison table). |

**Optimal trade shape for Pedro×Mario**

```
[Research hook: 20–30% of effort]
   → unusual question, physics prior, CyPhy/satellite/quantum framing, or paper extension

[Evaluation spine: 40–50%]
   → Mario-led: baselines, ablations, error analysis, clear success metrics

[Portfolio packaging: 20–30%]
   → joint: reproducible pipeline, README, 1 killer figure, oral narrative
```

**Failure modes**

- Pedro-only path → unfinished invention, weak comparison → Mario demotivated, faculty “so what?”  
- Mario-only path → solid but forgettable comparison study → Pedro veto on genericness  
- Dual-max research + dual-max polish → scope death in week 5  

**Success mode:** *One* speechless-researcher sentence + *one* airtight comparison table + *one* runnable demo.

---

## 5. Recommended ambition band

**Target joint Ambition score: 7.0–8.2**  
**Target joint Feasibility: ≥ 7.0** (hard floor **6.5** after week-1 data check)

| Band | Ambition | Meaning for this pair | Verdict |
|------|----------|------------------------|---------|
| Too safe | ≤ 6 | Clean comparison on a tired task; Mario comfort, Pedro alienation | Reject |
| **Sweet spot** | **7.0–8.2** | Non-generic framing; methods from shared toolbox; MVP + optional stretch (PINN/RL/quantum-inspired) | **Select here** |
| Stretch | 8.3–9.0 | Allowed only if Dataset ≥8 and Feasibility still ≥7 after scoping | Conditional |
| Unfinishable | ≥ 9.0 with Feasibility <7 | Full invent + new data + deep method stack | Reject / amputate hook |

**Ambition-band operating rules**

1. **Novelty budget:** exactly one of {new problem framing, new hybrid method, non-obvious dataset use}. Not all three.  
2. **Method budget:** 2–3 model families max (e.g. strong classical + deep + optional PINN/RL).  
3. **Reproduce-or-extend:** prefer “reproduce core of paper X, then extend to setting Y” over blank-canvas invent — satisfies Mario outside=8 and Pedro invent hunger via the extension.  
4. **Check-in cadence:** short sync ≥2×/week for first 3 weeks (Mario need); freeze scope end of week 2.  
5. **Kill criteria:** health/omics; no data by end of week 1; Ambition >8.5 with Feasibility <7; Pedro labels it “generic student project.”

---

### How to use this matrix next

1. Generate candidate list **elsewhere** (brainstorm / faculty / lab).  
2. Instant-kill: health/omics + obvious generics.  
3. Score survivors on the 8 criteria.  
4. Keep only Ambition ∈ [7.0, 8.2] **or** stretch with Dataset≥8 & Feasibility≥7.  
5. Prefer candidates sitting in hunt-priority zones 1–2 from the pre-scored overlap table.