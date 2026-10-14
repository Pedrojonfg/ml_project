# Research Brief: ESA Collision Avoidance Challenge (Kelvins) — IE BAM Project Option A

**Depth**: deep  
**Date**: 2026-10-11  
**Research time**: deep pass (official challenge + competition paper + winners + post-2019 literature + local project context)  
**Audience**: Pedro + Mario decision / ASAP 2-page proposal  
**Stack constraint**: sklearn + PyTorch · ~6 weeks · health veto · ambition 25% · oral 50% ML  

---

## Executive Summary

ESA’s Kelvins Collision Avoidance Challenge is a **real ops SSA problem**: from a truncated time series of Conjunction Data Messages (CDMs), predict the **final collision risk** at closest approach. The dataset is public, licensed (CC BY 4.0), and scientifically documented. The hard truth from the competition: the **naive “last known risk” baseline (LRP) is extremely strong** — only **12/97 teams** beat it — so a course project that only “tunes XGBoost for leaderboard” reads as **fake ambition**. Ambition that grades well: **rigorous evaluation under imbalance + mission shift**, **uncertainty-aware predictions**, **physics/cov-informed features**, and a clear story of **when the model helps an operator vs when it fails**.

**Verdict for this team**: excellent Pedro fit; solid Mario fit if framed as clean bake-off + calibration/rare-event analysis (finance-adjacent risk framing). Feasible in 6 weeks. Proposal must claim an **angle beyond replaying Kelvins**.

---

## 1. Exact problem statement + technical RQs

### Plain language

Low Earth Orbit is crowded. When two objects might get too close, operators receive a **CDM**: a structured alert with miss distance, covariances (uncertainty), object type, and a **self-computed collision risk**. Over ~1 week before closest approach (TCA), several CDMs arrive (~3/day). Uncertainty usually shrinks; risk often collapses toward “safe.” Operators typically start planning a possible avoidance manoeuvre **~2 days before TCA** and decide ~1 day before.

**The ML task**: using only CDMs available **≥ 2 days before TCA**, predict the risk in the **last CDM** (best knowledge near TCA). Goal is not pretty accuracy on the 97% “obviously safe” events — it is to **not miss the rare events that stay (or become) high-risk**, and to estimate their risk magnitude when they are high-risk.

Analogy: with the 10:00 weather briefing, forecast whether the 18:00 storm is still dangerous — knowing most days the “storm risk” evaporates.

### Technical setup (competition-faithful)

| Element | Definition |
|--------|------------|
| Unit of analysis | One **close-approach event** (`event_id`) = series of CDMs |
| Input \(x\) | All CDMs with `time_to_tca ≥ 2` days |
| Target \(y\) | Final `risk` from last CDM (log₁₀ scale in the released tables) |
| High-risk class | \(r \geq 10^{-6}\) (competition notification threshold; ops often use \(10^{-5}\)–\(10^{-4}\) for manoeuvre) |
| Primary competition loss | \(L = \mathrm{MSE}_{HR} / F_2\) (lower better) |

Official blurbs:  
- Home: https://kelvins.esa.int/collision-avoidance-challenge/  
- Challenge: https://kelvins.esa.int/collision-avoidance-challenge/challenge/  
- Scoring: https://kelvins.esa.int/collision-avoidance-challenge/scoring/

### Research question options (pick 1 primary + optional secondary)

**RQ-A (recommended primary — course-natural):**  
*Given CDMs truncated at −2 days to TCA, which model family (linear/trees vs sequence NN) best improves upon the LRP baseline on \(F_2\) and \(\mathrm{MSE}_{HR}\), and which physical features drive gains?*

**RQ-B (ambition / oral gold):**  
*Can an uncertainty-aware model (predicting a risk distribution or calibrated high-risk probability) reduce false negatives on “jump” events that all top-10 teams missed, relative to point-estimate LRP and GBDT?*

**RQ-C (operations / lead-time framing):**  
*How does predictive skill degrade as lead time increases (e.g. −4d vs −3d vs −2d), and what is the precision–recall trade-off for an earlier go/watch recommendation?*

**RQ-D (stretch — only if W1–W2 are clean):**  
*Does leave-mission-out evaluation change the ranking of methods vs random event CV (mission_id shift is known to matter)?*

Avoid claiming “we will beat ESA ops” or “solve Kessler syndrome.” Claim: **academic study of early risk forecasting with transparent failure modes**.

---

## 2. Dataset: size, schema, labels, download, license, pitfalls, imbalance

### Downloads & license

| Resource | URL | Notes |
|----------|-----|-------|
| Kelvins data page | https://kelvins.esa.int/collision-avoidance-challenge/data/ | `train_data.zip`, `test_data.csv` |
| Zenodo (preferred citation + full release) | https://zenodo.org/records/4463683 | DOI **10.5281/zenodo.4463683** · zip **~221 MB** · includes labels kept private during competition |
| Competition paper (arXiv) | https://arxiv.org/abs/2008.03069 · PDF https://arxiv.org/pdf/2008.03069.pdf | Design, winners, post-comp ML |
| Springer Astrodynamics version | https://link.springer.com/article/10.1007/s42064-021-0101-5 | Same content, cite either |
| License | **Creative Commons Attribution 4.0 International (CC BY 4.0)** | Credit ESA ACT + Space Debris Office; OK for course paper |

**Cite creators**: Uriot, Izzo, Martinez-Heras, Letizia, Siminski, Merz (ESA ACT + Space Debris Office). Data: CDMs **2015–2019**, anonymised; thanks US Space Surveillance Network for underlying surveillance data.

### Size (official)

| Split | Rows (CDMs) | Unique events | ~CDMs / event |
|-------|-------------|-----------------|---------------|
| Training | 162,634 | 13,154 | ~12 |
| Testing | 24,484 | 2,167 | ~11 |
| Full DB (paper Table 1) | 199,082 | 15,321 | avg 13 (min 1, max 23) |

Attributes: **103 columns per CDM** (almost all numeric; `c_object_type` categorical).

### Schema (what matters)

**Event keys / target**
- `event_id`, `mission_id`, `time_to_tca` (days to TCA)
- `risk` — self-computed collision risk at CDM epoch, **base-10 log** in the challenge tables. In test, predict final risk per `event_id`.

**Geometry / kinematics**
- `miss_distance`, `relative_speed`, relative position/velocity in R/N/T; `azimuth`, `elevation`, `geocentric_latitude`

**Risk-related**
- `max_risk_estimate`, `max_risk_scaling` (max Pc by scaling combined covariance)

**Object / orbit (prefix `t_` target = ESA sat, `c_` chaser)**
- size/RCS: `x_span`, `x_rcs_estimate`
- orbit: `x_h_apo`, `x_h_per`, `x_ecc`, `x_j2k_inc`, `x_j2k_sma`, ballistic/SR coeffs, `x_sedr`
- OD quality: obs available/used, residuals, OD span, weighted RMS, last-obs timing
- **6×6 covariance pieces**: sigmas + correlations in R/N/T position & velocity; `x_position_covariance_det`

**Environment**
- `F10`, `AP`, `F3M`, `SSN` (space weather)

Full column dictionary: https://kelvins.esa.int/collision-avoidance-challenge/data/

### Labels

- Supervision: **final CDM’s `risk`** per event (not a separate “collision happened” label — almost no actual collisions; this is **forecasting operational risk estimates**).
- Binary high-risk for \(F_2\): \(r \geq 10^{-6}\).
- Zenodo release includes competition-private labels → you can evaluate on official test without Kelvins submission.

### Class imbalance (from paper Table 1 + design)

| Threshold | # events (full DB 15,321) | Approx. rate |
|-----------|---------------------------|--------------|
| \(r \geq 10^{-4}\) | 30 | **0.20%** |
| \(r \geq 10^{-5}\) | 131 | **0.85%** |
| \(r \geq 10^{-6}\)** (competition HR)** | **515** | **~3.4%** |

Additional skew: **9,505 events** have final risk \(\leq -30\) (log₁₀) — extreme low-risk mass (paper Fig. 4).

**Train/test are NOT random** (by design, to enrich operationally meaningful / high-risk cases):

- Test eligibility: ≥2 CDMs; last CDM with `time_to_tca < 1`; early CDMs with `time_to_tca ≥ 2`; CDMs with `time_to_tca < 2` **removed from features**.
- Eligible high-risk after filters: **216** of 515 → **150 in test, 66 in train** (remaining 299 HR left in train but not necessarily test-like).
- Test HR rate ≈ **150/2167 ≈ 6.9%** (enriched vs ~3.4% overall).
- Paper Fig. 10(b): **150 positives / 2017 negatives** on test for FP/FN analysis.

### Known pitfalls (treat as first-class risks)

1. **LRP baseline is brutally strong** (\(L=0.694\)); CRP constant \(\hat r=-5\) is \(L=2.5\). Beating LRP is the bar, not “accuracy > 95%.”
2. **Train ≠ test distribution** (HR enrichment, mission_id imbalance among HR events). Teams reported **poor val↔test correlation**; 50% tried to build test-like val and mostly failed.
3. **Metric gaming**: clipping all low predictions to \(-6.001\) is optimal under the competition loss; winners used **threshold ladders** informed by metric + test construction — easy to look clever, hard to defend scientifically unless framed carefully.
4. **Manoeuvre cases removed / truncated** — highest real-risk operational cases may be underrepresented (selection bias).
5. **Anonymisation**: absolute times/states → relative; mission names → `mission_id`. Physics still usable; orbital “storytelling” limited.
6. **Missing values** present; LightGBM-style models handle them; sklearn pipelines need explicit imputation.
7. **Heterogeneous series length** (1–23 CDMs); naive padding hurts.
8. **65% of surveyed teams treated the problem as static** (latest CDM or aggregates) — temporal signal may be weak for many events; hard cases are **discontinuous jumps** near TCA with **high covariance**.
9. **Mission shift**: PCA clusters by `mission_id`; HR mission mix differs train vs test (missions 2/15/19 over-represented in test HR).
10. Helper libraries exist (e.g. **Kessler** CDM loaders) — useful, but do not outsource the analysis story: https://kesslerlib.github.io/kessler/notebooks/kelvins_dataset.html

---

## 3. Prior work / winners — and what is STILL open

### Competition snapshot

- Oct–Dec 2019 · **96–97 teams** · **862 submissions**
- Only **12 teams** beat LRP on final full-test score
- Survey (22 teams, all top teams): 65% addressed imbalance; 65% framed problem as **static**; 30% admitted **test probing** via trial-and-error (including winners)

Leaderboard (historical): https://kelvins.esa.int/collision-avoidance-challenge/leaderboard/

### Winner approaches (high-level)

| Rank | Team | Score \(L\) | MSE_HR | F₂ | Approach gist |
|------|------|-------------|--------|-----|----------------|
| — | LRP baseline | 0.694 | 0.513 | 0.739 | Clip last known risk |
| 1 | **sesc** (Honda Research Institute Europe) | **0.556** | **0.407** | 0.733 | Metric-aware **rule cascade** on \(r_{-2}\): promote borderline low→high for recall; hard “safe” rules (payload / small `t_span` / large miss); clip high risks; some manual adj. Early AutoML/RF/tsfresh **overfit** |
| 2 | dietmarw | 0.571 | 0.437 | **0.765** | Best F₂ on Pareto with sesc (details less published in paper) |
| 3 | **Magpies** | 0.585 | 0.441 | 0.753 | **Manhattan-LSTM (siamese)** on 7 physics-ish features + series aggregates; detect low→high **anomalies**; majority vote ensemble |

sesc write-up context: https://www.honda-ri.de/hri-eu-achieved-first-place-at-esa-collision-avoidance-challenge/  
Engineered decision-tree talk: “Engineered Decision Tree for Judging Spacecraft Collision Risks,” 8th European Conference on Space Debris, 2021 (Rebhan & Einecke) — https://www.honda-ri.de/publications/publications/?pubid=4717  

Post-competition ESA paper experiments: LightGBM predicting **risk residual** \(h = r - r_{-2}\) (quantile-transformed) → ~**+1.27% F₂** vs LRP under their CV protocol — gains exist but **generalization is fragile**; aggregated competition loss correlates poorly with true OOD skill.

### Hard residual problem (paper §5.4)

**11/150** HR events were **false negatives for all top-10 teams**; also many shared FPs. Common trait: **large risk jumps** near TCA + **elevated uncertainties** (e.g. `t_sigma_rdot`). Paper explicitly suggests **predicting a risk distribution**, not a point estimate.

### Post-2019 literature (open angles)

| Direction | Example | Why it matters for originality |
|-----------|---------|--------------------------------|
| Bayesian / HMM risk evolution | Catulo et al. arXiv:2311.10633 — https://arxiv.org/pdf/2311.10633v1 | Markov-ish structure of CDMs; probabilistic framing |
| CDM arrival as (non)homogeneous Poisson | arXiv:2303.15074 · arXiv:2311.05426 | Ops question: wait for next CDM? |
| Kessler library: Bayesian LSTM + generative CDMs | https://kesslerlib.github.io/kessler/ · SDC8 paper https://conference.sdo.esoc.esa.int/proceedings/sdc8/paper/226/SDC8-paper226.pdf | Synthetic data / uncertainty; don’t reinvent parsers |
| Predict covariances → recompute Pc | Metz MSc (cited in paper) | Physics-in-the-loop |
| EU SST escalation / CDM-field prediction | IAC-22 ML PDF https://www.eusst.eu/sites/default/files/documents/IAC-22_Machine_Learning.pdf | Escalation vs de-escalation |
| Go/No-go decision ML | Orbital Debris 2023 https://www.hou.usra.edu/meetings/orbitaldebris2023/pdf/6043.pdf | Different label (analyst decision), small N |

### Still open for a 6-week student project (do NOT claim “SOTA Kelvins”)

1. **Uncertainty-first models** (paper’s own open door): conformal prediction, quantile regression, MC-dropout LSTM, reliability diagrams on HR vs jump events.  
2. **Lead-time curves** (−4/−3/−2 days): operationally meaningful, under-emphasized in leaderboard culture.  
3. **Mission-aware / leave-mission-out** evaluation (paper admits split ignored mission balance).  
4. **Physics feature ablations** with fixed protocol: miss distance, Mahalanobis distance, covariance determinants, OD quality — Magpies picked 7; you can do a cleaner SHAP/permutation study.  
5. **Two-head models**: classifier (HR vs LR) + regressor on HR only — matches metric structure scientifically without metric gaming.  
6. **Compare static vs sequence** under **identical features and CV** (competition survey left this murky).  
7. Optional light touch of Kessler generative CDMs for **sensitivity / data augmentation** (careful: synthetic ≠ real ops).

**Closed / saturated for course wow:** pure leaderboard hacking; “we used XGBoost”; Autogluon without analysis; claiming temporal transformers without beating LRP + explaining failures.

---

## 4. Recommended methodology ladder + metrics

### Ladder (course → stretch)

| Stage | Methods | Role |
|-------|---------|------|
| 0. Protocol | Event-level splits; filter train to test-like specs where fair; fix seed; freeze test | Scientific hygiene |
| 1. Baselines | CRP; **LRP**; “always −6.001”; simple threshold promote | Must beat / contextualize |
| 2. Course classical | Logistic (HR class); Ridge/Huber on residual \(h\); RF / HistGBDT / XGBoost-sklearn; calibration (Platt/Isotonic) | Mario strength |
| 3. Feature engineering | Latest CDM + deltas (risk, miss, cov det) + aggregates (n_CDM, mean/std risk) + physics proxies (Mahalanobis if rebuildable, max_risk_*) | Pedro strength |
| 4. Imbalance toolkit | class_weight, focal-ish sample weights, threshold tuning on **PR / F₂**, not accuracy | Oral defense |
| 5. PyTorch stretch | Small MLP on engineered vector; **LSTM/GRU** on selected channels; optional siamese “anomaly” head (Magpies-inspired, simpler) | Ambition signal |
| 6. Ambition differentiator | Quantile / heteroscedastic head **or** conformal intervals; error analysis on jump events; lead-time sweep | What grades as “not homework” |
| 7. Optional | Light GP on low-dim physics features; Kessler only as loader/aux | Only if 1–6 solid |

### Evaluation metrics (report a dashboard, not a single number)

**Competition-aligned (cite and reimplement):**
- \(F_2\) on HR (\(r \geq -6\) in log space / \(10^{-6}\) linear)
- \(\mathrm{MSE}_{HR}\) on true HR events
- Combined \(L = \mathrm{MSE}_{HR}/F_2\)

**Course-honest extras (oral gold):**
- PR-AUC / Average Precision (imbalance-aware)
- Recall@k false-positive budget; precision–recall curve
- Brier score + **reliability diagrams** for \(P(\mathrm{HR})\)
- Residual plots vs miss distance / covariance volume
- **Lead-time curves**; **leave-mission-out** table
- Case study of the ~11 “hard FN” style events (reproduce difficulty analysis)

**Do not lead with accuracy / overall MSE.**

---

## 5. Six-week plan

| Week | Focus | Exit criteria |
|------|-------|---------------|
| **W1** | Download Zenodo; schema EDA; event reconstruction; reproduce LRP/CRP scores on held-out protocol; document imbalance & mission shift; freeze RQ + metric dashboard | Notebook 01 + one-pager protocol |
| **W2** | Feature store (latest + deltas + aggregates); train/val that respects events; classical models (logreg, RF, GBDT); threshold analysis | Beat or explain failure vs LRP on val; feature importance v0 |
| **W3** | Physics ablations; calibration; PR curves; error taxonomy (stable-low / stable-high / jump-up / jump-down) | Written error taxonomy + figures for proposal→paper |
| **W4** | PyTorch sequence or MLP residual model; fair comparison vs W2 under **same splits/features** | Table: baseline vs trees vs NN |
| **W5** | Differentiator: uncertainty **or** lead-time **or** leave-mission-out; stress-test hard events | “Killer slide” result locked |
| **W6** | Ablations polish; limitations; 2-page→paper conversion; oral dry runs with hostile Qs | Final figures + script |

**Parallel roles:** Pedro — domain features, hard-event physics, oral narrative · Mario — CV protocol, metrics, model comparison tables, calibration.

**Buffer rule:** if NN underperforms trees by W4 Friday, keep NN as ablation and deepen uncertainty/lead-time — oral rewards insight over architecture vanity.

---

## 6. Proposal outline (2 pages)

**Page 1 — Problem & data**
1. Title + one-sentence pitch (ESA CDMs → early final-risk forecast).  
2. Motivation: ops manoeuvre cost vs missed conjunction; LEO congestion (cite Kelvins home stats).  
3. Precise task + diagram (series truncated at −2d → final risk).  
4. Dataset: Zenodo DOI, n events/CDMs, 103 feats, CC BY 4.0, 2015–2019.  
5. Challenge: extreme imbalance (~3.4% HR; test enriched ~7%); LRP strong baseline.

**Page 2 — Method, ambition, plan**
6. RQ (pick A+B or A+C).  
7. Methods ladder (baselines → trees → PyTorch → uncertainty/lead-time).  
8. Metrics dashboard (\(F_2\), MSE_HR, PR-AUC, calibration).  
9. Ambition paragraph: **not** “win Kelvins”; **yes** “operator-relevant early warning + honest failure modes / uncertainty.”  
10. 6-week milestones + roles.  
11. Ethics/limitations: historical anonymised alerts; no live commanding; selection bias (manoeuvres removed).  
12. Key refs: Kelvins pages + arXiv:2008.03069 + Zenodo.

Keep prose tight; one figure max (CDM timeline). Spanish OK if the course language is Spanish.

---

## 7. Oral defense — hard questions

Prepare crisp answers:

1. **Why not just use the last CDM risk?** → LRP is the baseline; show where it fails (jumps, high σ) and what you add.  
2. **Isn’t this just replaying a 2019 Kaggle-like contest?** → Different scientific claim: evaluation protocol / uncertainty / lead-time / mission shift — competition winners optimized a quirky loss.  
3. **Did you leak future CDMs?** → Explicit truncation `time_to_tca ≥ 2`; unit = event.  
4. **Accuracy looks great — so what?** → Trap; show PR and FN on HR.  
5. **Can you deploy this at ESOC?** → No; decision support research only; Pc itself is model-based; labels are risk estimates not collisions.  
6. **Why \(10^{-6}\) not \(10^{-4}\)?** → Competition/notification vs manoeuvre threshold; sensitivity analysis.  
7. **Train/test mismatch — how did you validate?** → Event CV + test-like filter + leave-mission-out; report correlation honestly.  
8. **Did temporal models help?** → Survey said often no; your controlled static vs seq comparison.  
9. **Class imbalance tricks?** → Weights + threshold on F₂/PR; not SMOTE-without-theory.  
10. **Ethics of space surveillance data?** → Anonymised public release under ESA agreement; CC BY attribution; no attempt to de-anonymise missions.  
11. **Compute?** → Tabular/CPU-first; GPU optional for LSTM.  
12. **What’s novel vs Magpies/sesc?** → One concrete differentiator (uncertainty / lead-time / mission OOD) with ablation.

---

## 8. Ambition signals vs fake ambition

| Real ambition (grade-positive) | Fake ambition (looks busy, grades poorly) |
|--------------------------------|-------------------------------------------|
| Beat **and dissect** LRP | “We tried 12 architectures” |
| Dashboard for rare HR events | Overall accuracy / RMSE on all events |
| Uncertainty or lead-time study | Deeper transformer with no protocol |
| Mission-shift / jump-event analysis | Metric clipping tricks without science |
| Physics feature causal story | Black-box AutoML leaderboard chase |
| Clear operator decision framing | “AI will automate collision avoidance” hype |
| Limitations = selection bias, manoeuvre holes | Pretending dataset = ground-truth collisions |

Ambition 25% here is earned by **problem hardness + evaluation maturity + aerospace narrative**, not by parameter count.

---

## 9. Fit scores: Pedro vs Mario

| Dimension | Pedro | Mario | Justification |
|-----------|------:|------:|---------------|
| Domain passion | **10** | 7 | Pedro aerospace-loving; Mario OK if rigorous, not finance-first |
| Data cleanliness / comparison | 7 | **9** | Fixed schema, strong need for CV/metrics — Mario’s sweet spot |
| Anti-generic / wow | **10** | 7 | ESA + SSA interviews; not another Titanic |
| Oral (50% ML) | **9** | **8** | Pedro tells ops story; Mario defends metrics/imbalance |
| Ambition visibility | **9** | 8 | Real agency data + hard baseline |
| 6-week feasibility | **8** | **8** | No EO downloads; compute light; risk is scientific (LRP) not infra |
| Finance interest alignment | 3 | **6** | Not finance, but **risk, thresholds, calibration, rare events** transfer |
| Health veto | OK | OK | Non-health |

**Aggregate recommendation scores (this option alone):** Pedro **9.5/10** · Mario **7.5–8/10** · Team joint **8.5–9/10** if Mario owns evaluation design.

Mario risk: boredom if project becomes “Pedro physics lore + one GBDT.” Mitigation: give Mario ownership of **protocol, metrics, calibration, model card**.

---

## 10. Concrete risks

| Category | Risk | Mitigation |
|----------|------|------------|
| **Data** | Train/test mismatch; poor CV signal | Test-like filters; nested CV; report negative results |
| **Data** | Tiny HR count (515 total; 150 test) | Bootstrap CIs; case studies; don’t overclaim |
| **Data** | Manoeuvre / selection bias | Limitations section; don’t claim ops readiness |
| **Compute** | Low risk | CPU GBDT sufficient; Colab for LSTM |
| **Novelty** | Saturated competition narrative | Pivot to uncertainty / lead-time / mission OOD |
| **Novelty** | Accidentally re-implement sesc rules | Cite them; position as baseline, not contribution |
| **Ethics** | Space surveillance sensitivity | Use only released anonymised data; no re-ID; CC BY credit |
| **Ethics** | Safety overclaim | “Decision-support study,” not autonomous manoeuvres |
| **Course** | Over-index on DL | Keep course methods as equal citizens in tables |
| **Team** | Mario under-engaged | Explicit deliverables: metric suite + comparison chapter |
| **Proposal ASAP** | Scope creep (Kessler generative + PINN + …) | Freeze RQ in W1; stretch backlog only |

---

## 11. Killer differentiators they could claim

Pick **one primary** (two max):

1. **Uncertainty-aware early warning:** intervals / quantiles that expand on high-σ events; show coverage on the hard FN cohort.  
2. **Lead-time operating curves:** skill vs days-to-TCA with fixed FP budget — directly ops-relevant.  
3. **Mission-OOD stress test:** leave-`mission_id`-out rankings vs pooled CV (paper flagged this gap).  
4. **Physics-gated residual learning:** predict \(h = r - r_{-2}\) only when covariance / OD features say LRP is untrustworthy (mixture of experts lite).  
5. **Two-stage decision model:** \(P(\mathrm{HR})\) calibrated head + magnitude regressor — aligns with how \(F_2\) + MSE_HR decompose, without opaque threshold ladders.  
6. **Failure atlas:** publish a reproducible taxonomy of jump events with feature signatures (oral unforgettable).

**Recommended combo for Pedro+Mario:** **(5) two-stage + (2) lead-time curves**, with (6) as oral centerpiece. Trees carry the main result; a small PyTorch sequence model is the stretch ablation.

---

## Reusable from this repo

| Asset | Path | Use |
|-------|------|-----|
| Slide narrative (ES) | `presentations/top10-options/options/01-esa.tex` | Proposal/oral language |
| Cluster ranking | `research/briefs/research-brief-project-ideas-deep.md` §A1 | Cross-option comparison |
| Aerospace shortlist | `research/briefs/subagent-archives/satellite-aerospace-ideas.md` | Adjacent options (OPS-SAT, etc.) |

---

## Suggested phases (build order)

1. Protocol + LRP reproduction  
2. Classical bake-off + features  
3. Differentiator (uncertainty or lead-time)  
4. PyTorch ablation  
5. Paper + oral  

---

## Sources (primary)

1. https://kelvins.esa.int/collision-avoidance-challenge/  
2. https://kelvins.esa.int/collision-avoidance-challenge/challenge/  
3. https://kelvins.esa.int/collision-avoidance-challenge/data/  
4. https://kelvins.esa.int/collision-avoidance-challenge/scoring/  
5. https://kelvins.esa.int/collision-avoidance-challenge/leaderboard/  
6. https://zenodo.org/records/4463683 (CC BY 4.0, DOI 10.5281/zenodo.4463683)  
7. https://arxiv.org/abs/2008.03069 · https://arxiv.org/pdf/2008.03069.pdf  
8. https://link.springer.com/article/10.1007/s42064-021-0101-5  
9. https://www.honda-ri.de/hri-eu-achieved-first-place-at-esa-collision-avoidance-challenge/  
10. https://www.honda-ri.de/publications/publications/?pubid=4717  
11. https://kesslerlib.github.io/kessler/  
12. https://conference.sdo.esoc.esa.int/proceedings/sdc8/paper/226/SDC8-paper226.pdf  
13. https://arxiv.org/pdf/2311.10633v1  
14. https://arxiv.org/html/2303.15074  
15. https://www.eusst.eu/sites/default/files/documents/IAC-22_Machine_Learning.pdf  
16. https://www.hou.usra.edu/meetings/orbitaldebris2023/pdf/6043.pdf  

---

## Bottom line for the decision

**Option A is proposal-ready and ambitious if you refuse leaderboard cosplay.** Anchor the 2-pager on: ESA CDMs + LRP baseline honesty + rare-event metrics + one differentiator (uncertainty or lead-time). Pedro will love it; Mario stays engaged if he owns the evaluation spine.
