# Research Brief: PHBench (Option B) — IE BAM ML Course Project

**Depth**: deep  
**Date**: 2026-10-11  
**Audience**: Pedro + Mario decision + ASAP proposal drafting  
**Constraint**: no health / omics  
**Stack**: sklearn + PyTorch · ~6 weeks  

## Executive Summary

PHBench is a **real 2026 research benchmark** (not a tired Kaggle clone): predict whether a Product Hunt *featured* launch raises a **Series A within 18 months**, using launch-day signals only. Universe = **67,292** launches (2019–2025), **528** positives (**0.78%**). Author champion (Top-3 tree ensemble) gets **test AP = 0.037** (~**4.7×** random) and **F₀.₅ = 0.097** vs LR baseline AP 0.024 / F₀.₅ 0.045 — so the bar is *beatable in principle* but **validation numbers are inflated** (best-of-144 on 53 positives).  

**Verdict for this team:** **Strong yes IF Hugging Face / email access lands in week 0–1.** Framing as **ranking / deal-flow prioritization** (Mario recommender lens) + **honest leakage, calibration, temporal OOD** (research spine) beats “another XGBoost vs NN table.” Pivot to **VCBench** only if PHBench gate fails — do **not** run both as dual cores.

**Do tomorrow:** (1) request HF gated access, (2) email `benchmark@vela.partners` subject `PHBench Data Access`, (3) clone GitHub baselines, (4) draft proposal from §6 outline.

---

## 1. Plain-language problem + research questions

### Everyday problem

Hundreds of products launch publicly. Almost none raise a Series A in the next year and a half (~**1 in 127** featured PH launches). Investors and analysts cannot read everything. Product Hunt packs a **24-hour** snapshot of social proof (votes, comments, ranks, makers, topics). The useful ML product is not “predict the future with certainty” — it is a **ranked shortlist**: which launches deserve 10 minutes of human attention this week?

### Precise research questions (ranking preferred)

**RQ1 (primary — ranking):**  
Given only features available at Product Hunt *featured* launch time, which model families produce the best **precision-weighted ranking** of Series A within 18 months — measured by **Average Precision (AP / PR-AUC)** and **Precision@k (k ∈ {50,100})** — under the official split and under a **temporal holdout** (train ≤2023, evaluate 2024–2025)?

**RQ2 (multimodal / feature value):**  
Do **topic structure + text *surface* stats** (and, if raw text ever becomes available, embeddings) add lift beyond engagement/rank baselines, or is predictive mass concentrated in **rank × team × B2B** interactions already documented by the authors?

**RQ3 (reliability / deployment realism):**  
How **calibrated** are predicted probabilities (ECE / reliability diagrams), and how sensitive are rankings to known **leakage** (maker follower scrape-time) and **selection bias** (featured-only PH, Crunchbase FN labels)? What is the **lift@k vs base rate** for a fixed weekly review budget?

Optional oral stretch (not week-1 scope): Are ML top-k and zero-shot LLM “picks” **complementary** (authors report ~6% top-50 overlap on val, all true positives in that overlap)?

---

## 2. Dataset access: GitHub, HF, phbench.com

### Canonical URLs

| Resource | URL |
|----------|-----|
| Website / leaderboard | https://phbench.com/ |
| Paper (arXiv) | https://arxiv.org/abs/2605.02974 |
| Paper HTML | https://arxiv.org/html/2605.02974v1 |
| GitHub (code + baselines) | https://github.com/ihlamury/phbench |
| Hugging Face dataset | https://huggingface.co/datasets/ihlamury/phbench |
| Data card (in repo) | https://github.com/ihlamury/phbench/blob/main/data/benchmark/data_card.md |
| Live predictions API docs | https://phbench.com/api-docs |
| License deed (CC BY 4.0) | https://creativecommons.org/licenses/by/4.0/ |
| Submission / data email | benchmark@vela.partners |

### Gating (critical path)

1. **Hugging Face — gated.** Page states you must **agree to share contact information** before downloading. Log in → accept conditions → download. License metadata: **CC BY 4.0**. Size ~**29.3 MB**.  
2. **Paper / README dual path:** public anonymized splits also described as **available on request** — email **`benchmark@vela.partners`** with subject **`PHBench Data Access`**. Files named: `phbench_public_train.csv`, `phbench_public_validation.csv`, `phbench_public_test.csv` (+ sample submission).  
3. **Test labels are private.** Score by mailing prediction CSV (`anon_id`, `series_a_prob`) to the same email; maintainers score server-side and can post to leaderboard.  
4. **API** (optional portfolio spice): weekly scored launches need an API key from the same email (`x-api-key`). Useful for demo, **not** for supervised training labels.

**Risk:** access denial / delay → week-1 blocked. Mitigate: request **both** HF + email **Day 0**; keep **VCBench** warm (see §12).

### License & prohibited use

- **CC BY 4.0** — share/adapt with attribution.  
- Benchmark add-on (README/data card): **may not be used to target or solicit specific companies or individuals**; commercial investment use of labels requires independent verification.  
- Course project + citation of Ihlamur et al. is the intended academic use.

### Train / val / test

| Split | Posts | Positives | Rate | Labels |
|-------|------:|----------:|-----:|--------|
| Train | 47,071 | 372 | 0.79% | Public |
| Validation | 6,753 | 53 | 0.78% | Public |
| Test | 13,468 | 103 | 0.76% | **Withheld** |
| **Total** | **67,292** | **528** | **0.78%** | |

- Split: ~70/10/20, **stratified** on `year_bucket × topic_bucket × label`, with **company-level grouping** (`cb_permalink`) so all launches of one CB company stay in one split (anti-relauch leakage). Seed = 42.  
- Year buckets (data card): pre_covid (≤2019), covid_boom (2020–2021), vc_winter (2022–2023), ai_era (2024–2025).  
- **Important:** official split is **stratified IID across years**, *not* a pure temporal holdout. Authors themselves flag temporal holdout as **future work** — a high-value originality track for you.

### What is *not* in the public anonymized release

Paper §3.6 strips: **product name, slug, tagline, description, website URL, maker names, Crunchbase fields, `days_to_series_a`**.  
Retained: **61 engineered numeric/categorical features** (+ `maker_tier` released but unused by authors), engagement, ranks, topic flags, temporal buckets, **text *length* / has_number style features**, and (in HF preview) pipe-separated **`topics`** string.

**Implication:** “Sentence-BERT on tagline” is **not** a free week-1 feature unless you get non-anonymized text or a future text release. Pitch **surface text + topics**, not semantic NLP, unless access expands.

### Feature list summary (61 used / 62 released)

| Group | # | Examples |
|-------|--:|----------|
| Engagement | 6 | `log_votes`, `log_comments`, `log_reviews`, `votes_per_comment`, `has_reviews`, `review_rating` |
| Rank | 8 | `daily_rank`, `weekly_rank`, `monthly_rank`, logs, `rank_bucket` (0–5), has_* flags |
| Maker | 4 | `maker_count`, `has_makers`, `maker_followers_total`, `log_maker_followers` |
| Temporal | 7 | `launch_dow/month/year/quarter`, `is_weekday`, `is_prime_window` (Tue–Thu), `days_since_ph_launch` |
| Topics | 24 | 20 binary topic flags + `topic_count` + `is_ai_topic` / `is_b2b_topic` / `is_consumer_topic` |
| Text (surface) | 8 | tagline/desc length & word count, `has_description`, `tagline_has_{number,percent,dollar}` |
| Interactions | 4 | `votes_x_rank_bucket`, `makers_x_votes`, `prime_window_x_votes`, `ai_topic_x_year` |
| Extra released | 1 | `maker_tier` (authors dropped; noise / collinear) |

Author-reported **strong** signals (site + paper): daily rank / rank bucket (~**3.5×** lift for top-3 day rank), votes×rank, maker followers (⚠ leakage), votes-per-comment, B2B cluster, AI×year, reviews. **Weaker / noise-ish:** raw upvote log alone, bare “AI” flag, tagline word count, day-of-week alone, maker_tier.

### Leakage risks (must discuss in proposal)

| Risk | Mechanism | Mitigation |
|------|-----------|------------|
| **Maker followers scrape-time** | Followers scraped ~2026, not at launch; post-success founders accumulate followers → encodes future success, worse for older cohorts | Ablate both follower features; report ΔAP; prefer models that don’t depend on them |
| **Company relaunch** | Same company, multiple PH posts | Official company-grouped split — verify zero CB permalink overlap |
| **Post-level ≠ company-level base rate** | Multiple posts inflate/deflate rates | State post-level task clearly |
| **Crunchbase false negatives** | No domain match / missing CB → labeled 0 even if funded (~conservative matching; ~12% featured match rate) | Treat labels as noisy; discuss FN bias in oral |
| **Announcement vs close date** | CB announcement can lag close by 1–3 months | Window is approximate |
| **Right-censoring 2025** | 18mo window incomplete for late launches; ~&lt;35 possible future flips | Note April 2026 snapshot as frozen truth |
| **Featured-only selection** | 288k posts → 67k featured | External validity to all startups is limited (see §7) |
| **Identity leakage to LLMs** | If you ever use names/taglines with LLMs | Follow authors’ anonymized protocol for fair LLM arms |
| **Val overfitting** | 53 positives, 144 configs; val AP ≫ test AP | Bootstrap CIs; temporal holdout; don’t tune on test; optional blind submit once |

---

## 3. Published baselines / leaderboard insights

### Numbers that matter

| Model | Val F₀.₅ | Val AP | Test F₀.₅ | Test AP | Notes |
|-------|---------:|-------:|----------:|--------:|-------|
| **Top-3 Ensemble** (champion) | 0.284 | 0.126 | **0.097** | **0.037** | avg(ENS_avg, ENS_ISO, XGB_m21) |
| ENS_avg / LGBM+ISO / XGB+ISO | 0.22–0.27 | 0.07–0.09 | — | — | Trees + calibration dominate val board |
| **LR FS4** (official baseline) | 0.127 | 0.047 | **0.045** | **0.024** | Must beat this on val *and* argue test |
| Gemini 3 Flash (zero-shot, anon nums) | 0.129 | 0.034 | — | — | Beats LR on F₀.₅ point estimate; loses on AP |
| Gemini 2.5 / 3.1 Pro | worse | worse | — | — | **Bigger ≠ better** on anon tabular |
| Random | — | ~0.008 | — | — | ≈ base rate |

**Operational read (authors):** screening top-50 from a quarterly batch of ~2,400 featured posts surfaces ~**5** true Series A (~**10%** precision) — ~1 genuine raise every ~10 days if reviewing top weekly ranks.

### What is already strong

- **Gradient boosting + interaction features (FS4)** + **simple ensembles**.  
- **Class weights / `scale_pos_weight ≈ 125.5`**.  
- **Isotonic calibration** (with known val-overfit caveat on P@k).  
- **Rank / maker / B2B structure** — not raw vote count alone.

### What is weak / open (originality angles)

Authors explicitly leave open (steal these):

1. **Temporal holdout track** (train 2019–2023 → test 2024–2025) — market-regime OOD; currently missing from official leaderboard.  
2. **Nested / CV calibration** — they fit isotonic on the same val used for metrics; you can do it *right*.  
3. **Semantic text** — only surface stats today; embeddings planned, not released.  
4. **Maker-follower leakage ablation** on test / per-cohort — left to future work.  
5. **Hybrid LLM filter + ML ranker** — partial top-k complementarity observed.  
6. **Multi-task** (seed auxiliary → Series A) — denser label.  
7. **False-negative audit** of CB matching.  
8. **Neural tabular** (PyTorch) vs trees — not the champion story yet.  
9. **Proper uncertainty / cost-sensitive ranking** for a fixed analyst budget (Mario recommender framing).

**Do not claim originality for:** “we ran XGBoost”; “imbalance is hard”; “LLMs can do VC” without the anonymized protocol.

---

## 4. Methodology ladder + metrics

### Ladder (build in order)

**L0 — Sanity & leakage hygiene**  
Reproduce official metrics on val with LR + XGB from `phbench/baseline.py`. Confirm positive rates. Drop or ablate `maker_followers_*`. Plot year×label rates (boom vs winter).

**L1 — Strong classical (Mario spine)**  
- Logistic Regression (`class_weight='balanced'`)  
- Random Forest / HistGradientBoosting  
- XGBoost / LightGBM (`scale_pos_weight`)  
- Feature sets: engagement+rank only → +topics → +interactions (mirror FS3→FS4 story)  
- Early stopping on **AUC** (authors: F₀.₅/AP too noisy with 53 val positives)

**L2 — Imbalance & ranking objectives**  
- Threshold sweep for F₀.₅ (precision-weighted)  
- Optional under/over-sampling **only inside train folds**  
- Focal loss / weighted BCE in PyTorch  
- Report **lift@k = P@k / base_rate**

**L3 — Temporal generalization (killer extension)**  
- Primary report: official split (comparability)  
- Secondary: **temporal split** train≤2023 / val mid / test 2024–2025  
- Expect AP collapse vs boom years (authors: ML AP drops ~**42×** from 2021→2024 cohorts) — that *is* the scientific story

**L4 — Text + tabular (honest scope)**  
- **Available now:** topic flags + surface text stats + optional bag-of-topics from `topics` string  
- **PyTorch:** MLP / simple FT-Transformer-style tabular net on standardized features; optional embedding of topic tokens  
- **Not week-1:** full tagline SBERT unless text is granted

**L5 — Calibration & ensembling**  
- Platt vs isotonic vs temperature scaling with **held-out calibration fold** (not the metric val)  
- Reliability diagrams + ECE  
- Small ensemble of diverse families (trees + LR + NN) — average probs  
- Optional: one anonymized LLM zero-shot arm (reproduce finding: picker≠ranker)

**L6 — Error analysis (oral gold)**  
- False positives: high-rank consumer apps?  
- False negatives: B2B with low PH engagement (PH ≠ enterprise sales)  
- Cohort slices: AI era vs covid boom  

### Metrics (use this stack)

| Metric | Role |
|--------|------|
| **AP / PR-AUC** | Threshold-free ranking; primary scientific metric under extreme imbalance |
| **F₀.₅** | Official leaderboard primary; precision &gt; recall (analyst time cost) |
| **P@50 / P@100 / lift@k** | “Weekly review budget” story — Mario recommender language |
| **AUC-ROC** | Secondary only (can look good while precision is useless) |
| **Calibration** | ECE, reliability curve, mean predicted prob vs 0.78% base rate |
| **Bootstrap 95% CIs** | Mandatory on val (n₊=53); B≈1000–2000 |

**Avoid as primary:** accuracy, macro-F1 without context, ROC-only claims.

---

## 5. Six-week plan

| Week | Focus | Exit criteria |
|------|-------|---------------|
| **0 (ASAP)** | Access + proposal | HF accepted *or* email reply; proposal draft §6; VCBench backup cloned |
| **1** | Data + EDA + leakage | Train/val loaded; base rates; year plots; follower ablation; LR/XGB reproduced within ε of paper val |
| **2** | Classical ladder + metrics harness | Full sklearn/boosting comparison table; AP/F₀.₅/P@k/lift@k; freeze feature recipe |
| **3** | Temporal holdout + calibration | Temporal results written; nested calibration; reliability plots |
| **4** | PyTorch tabular + optional LLM arm | NN vs trees comparison; one ablation panel; no new data sources |
| **5** | Error analysis + portfolio packaging | Confusion slices; 1 killer figure (lift@k / PR curves); README; optional blind test submit |
| **6** | Report + oral | 2-page→full report; hard-question rehearsals (§7); demo notebook |

**Scope freeze:** end of week 2 — at most **one** stretch from {temporal track, NN, LLM complementarity}.  
**Check-ins:** ≥2 short syncs/week (Mario process need).

---

## 6. Proposal 2-page outline

**Title:** Ranking Product Hunt launches for Series A outcomes: an imbalanced, leakage-aware study on PHBench  

**§1 Problem (½ page)**  
- Deal-flow prioritization analogy; base rate 0.78%; **not** stock prediction / credit scoring.  
- Task definition: featured PH launch → Series A ≤18 months.  
- Cite PHBench (arXiv:2605.02974), site, HF.

**§2 Data (⅓ page)**  
- N, splits, company-grouped stratification, CC BY 4.0 + contact gate.  
- Feature groups (table).  
- Explicit limitations: CB FN, featured selection, maker-follower leakage.

**§3 Research questions (short)**  
- RQ1–RQ3 from §1.

**§4 Methods (½ page)**  
- Ladder L0–L5; sklearn + PyTorch.  
- Official split + temporal secondary track.  
- Metrics: AP, F₀.₅, lift@k, calibration + bootstrap CIs.

**§5 Expected contribution (¼ page)**  
- Reproduce baselines; **honest** generalization + calibration story; ranking-for-budget framing.  
- Optional leaderboard submit.

**§6 Timeline & risks (¼ page)**  
- 6-week table; HF denial → VCBench pivot; extreme imbalance; Kaggle-lookalike avoidance via RQs above.

**§7 Ethics (short)**  
- No targeting individuals; research use; not investment advice; selection bias.

---

## 7. Oral hard questions (prep answers)

### Ethics
- **Q:** Are you helping discriminate against founders?  
  **A:** Research on *aggregate* public launch signals; anonymized IDs; prohibited use includes solicitation; model encodes market biases (US CB, B2B, gameable votes) — we document, not deploy as sole gate.
- **Q:** Is this investment advice?  
  **A:** No — ranking experiment with high error; labels noisy; CC/data card forbid unverified commercial use.

### Causality
- **Q:** Do upvotes *cause* Series A?  
  **A:** No. Predictive association under confounding (team quality, category, marketing budget, macro cycle). We do **not** claim causal effects; PH success and fundraising share common causes.
- **Q:** Then what’s the point?  
  **A:** Decision support under a **budget constraint** (who to review), with calibrated uncertainty — same as spam ranking, not structural causal models.

### Leakage
- **Q:** Isn’t maker followers leaking the future?  
  **A:** Yes — documented by authors; we ablate and report. Any model that collapses without it is rejected for “deployment realism.”
- **Q:** Could test labels leak via the public API?  
  **A:** API exposes *current* scored launches with funding fields — not the anonymized historical test map. We won’t reverse-engineer `anon_id` ↔ PH id.

### Selection bias of Product Hunt
- **Q:** Who launches on PH?  
  **A:** Consumer/devtool-heavy, launch-savvy teams; **featured** posts only (~23% of all PH posts in their crawl). Non-PH startups, stealth B2B, non-English, infra without a “launch day” are out of frame.
- **Q:** Does high PH rank just mean “paid hustle”?  
  **A:** Engagement is **gameable**; we treat it as a signal of *mobilization*, not pure product quality — and show topic/prior base rates matter too.
- **Q:** Why is the positive rate so low — bad model or bad world?  
  **A:** Mostly **world** + **label conservatism** (unmatched funded cos → 0). Models can beat random ~4–5× and still have single-digit P@k — that’s the honest VC screen story.

### Metrics / ambition
- **Q:** Your val AP looks amazing — why?  
  **A:** Best-of-many on 53 positives; paper’s own test AP is ~3× lower. We report CIs and temporal OOD.
- **Q:** Why not just use GPT?  
  **A:** On *anonymized numbers*, Gemini loses to LR on AP; LLMs behave as high-precision “pickers,” not full rankers. Trees win this regime.

---

## 8. Ambition vs fake ambition

| Real ambition | Fake ambition |
|---------------|---------------|
| Temporal OOD + boom/bust analysis | “We’ll predict unicorns” |
| Leakage ablation + nested calibration | Stacking 15 models to climb val F₀.₅ |
| Lift@k for a fixed review budget | Accuracy 99.2% headlines |
| Clear RQ: ranking under 0.78% base rate | “End-to-end VC AI platform” |
| Reproduce paper then **one** extension | Ignore baselines; reinvent features blindly |
| Bootstrap CIs; admit CB false negatives | Claim causality from feature importance |
| Optional blind test submit | Overfit val until oral night |

**Sweet spot for Pedro×Mario:** Ambition **7.5–8.5** with Feasibility ≥7 — *reproduce PHBench, extend with temporal + calibration + ranking budget metrics, one PyTorch arm.*

---

## 9. Pedro / Mario fit scores

Scored 1–10 for **this option** (not the whole idea space).

| Dimension | Pedro | Mario | Notes |
|-----------|------:|------:|-------|
| Domain joy | **8** | **10** | Pedro: VC-curious, anti-generic stocks/credit — this clears the gate. Not physics/robotics identity (would be 10). Mario: finance + ranking/recsys home turf. |
| Data quality joy | **8** | **10** | Curated benchmark, documented features, public baselines. |
| Method fit (sklearn+PT) | **8** | **9** | Trees + calibration + PT tabular; Mario comparison theater. |
| Portfolio / interview story | **10** | **8** | “Deal-flow ranking on a 2026 benchmark” travels well. |
| Research adjacency | **9** | **7** | Real arXiv + leaderboard; Mario cares more about clean analysis than paper chasing. |
| Differentiability vs classmates | **9** | **9** | Far from churn/credit/house prices. |
| Feasibility (6w, assuming access) | **8** | **8** | Access gate is the main Feasibility haircut. |
| Oral defendability | **8** | **9** | Hard questions are answerable if you own bias/leakage. |
| **Overall fit** | **8.5** | **9.5** | Joint: **strong shortlist**; Pedro must sell “innovative VC / ranking,” not “finance homework.” |

**Governance:** Pedro veto if story slides into generic fintech; Mario veto if metrics/labels stay fuzzy; joint kill if no data by end of week 1.

---

## 10. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **HF / email access denial or slow** | Med | **Blocker** | Dual request Day 0; 72h timeout → **VCBench pivot** |
| **Extreme imbalance (0.78%)** | Certain | High variance metrics | AP/F₀.₅/lift@k; bootstrap; don’t chase accuracy |
| **Looks like Kaggle** | Med | Pedro alienation + weak oral | Lead with RQs, leakage, temporal OOD, ranking budget — not model zoo |
| **Val–test gap / overclaim** | High if careless | Credibility | Pre-register temporal track; one test submit |
| **Maker follower leakage** | Certain if ignored | Method fail in oral | Ablate by default |
| **No raw text** | High | Kills “NLP multimodal” pitch | Scope to topics + surface text; don’t promise SBERT |
| **Overlap with VCBench (Option 7)** | If both chosen | Diluted story | **One** VC core only |
| **Right-censored 2025 labels** | Low–med | Mild label noise | Disclose snapshot date |
| **Engagement gameability** | Certain socially | Validity | Discuss as limitation, not bug to “fix” |

---

## 11. Killer differentiators

1. **Temporal holdout as first-class track** (authors’ own future work — you ship it in a course project).  
2. **Analyst-budget metrics:** lift@k, expected true positives per week, cost of false positives — recommender language.  
3. **Leakage-honest models:** performance *with and without* scrape-time follower features.  
4. **Calibration done correctly** (nested), calling out authors’ isotonic-on-val artifact.  
5. **PyTorch tabular vs tuned trees** under the same ranking metrics — syllabus-visible, not hand-wavy deep learning.  
6. **Regime story:** models that “work” in 2020–21 and fail in VC winter — market structure, not magic.  
7. **Optional:** ML↔LLM top-k complementarity without pretending LLMs win anon tabular.  
8. **Portfolio artifact:** reproducible pipeline + one figure that an interviewer remembers (PR curve + lift@k bars).

---

## 12. Backup: VCBench if PHBench access fails

| | **PHBench** | **VCBench** |
|--|-------------|-------------|
| URL | https://phbench.com/ · https://github.com/ihlamury/phbench | https://vcbench.com/ · https://github.com/Vela-Engineering/VCBench-Starter-Kit |
| Paper | https://arxiv.org/abs/2605.02974 | https://arxiv.org/abs/2509.14448 |
| Input | PH launch tabular (+ surface text) | Anonymized **founder profiles** (text-heavy) |
| Label | Series A ≤18mo | Mega-success (exit/IPO/funding **&gt;$500M**) |
| N / base rate | 67k / **0.78%** | 9k / **~9%** |
| Public train | 47k labeled | ~4.5k public (starter CSV) |
| Access | **HF gate + email** | Starter kit CSV (historically easier; still private test) |
| Natural methods | Trees, calibration, PT tabular | LLMs + text classifiers; classical on structured fields |
| Imbalance difficulty | Extreme | Hard but manageable |
| Same org ecosystem | Vela / Oxford-adjacent authors | Same research family |
| Fit if PH fails | — | Still innovative VC; more LLM-shaped; less “launch day ranking” |

**Pivot rule:** If no PHBench files by **end of week 1**, switch to VCBench **ranking/classification of founder success** with sklearn baselines + one PT text encoder — keep the same ethics/leakage oral spine. **Do not** dual-core both.

---

## Immediate checklist (proposal ASAP)

1. [ ] HF: https://huggingface.co/datasets/ihlamury/phbench — request access  
2. [ ] Email: `benchmark@vela.partners` — subject `PHBench Data Access`  
3. [ ] Clone: `git clone https://github.com/ihlamury/phbench`  
4. [ ] Read: data card + paper §§3–5, 8  
5. [ ] Warm backup: VCBench starter kit + https://vcbench.com/  
6. [ ] Draft proposal from §6; freeze RQs as ranking-first  

---

## Sources

- Ihlamur, Griffin, Chen — *PHBench* — https://arxiv.org/abs/2605.02974 · https://arxiv.org/html/2605.02974v1  
- https://phbench.com/ · https://phbench.com/api-docs  
- https://github.com/ihlamury/phbench · README · `data/benchmark/data_card.md`  
- https://huggingface.co/datasets/ihlamury/phbench  
- https://creativecommons.org/licenses/by/4.0/  
- Chen et al. — *VCBench* — https://arxiv.org/abs/2509.14448 · https://vcbench.com/ · https://github.com/Vela-Engineering/VCBench-Starter-Kit · https://vela.partners/research/vcbench  
- Prior local briefs: `research/briefs/research-brief-project-ideas-deep.md`, `research/briefs/subagent-archives/fintech-vc-ideas.md`, `research/briefs/subagent-archives/fit-matrix-pedro-mario.md`, `presentations/top10-options/options/02-phbench.tex`
