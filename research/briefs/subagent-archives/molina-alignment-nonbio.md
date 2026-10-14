# Archive: molina-alignment-nonbio
**Agent ID:** da4898e0-3bf2-4e3c-b46d-1f7ab7666f78

---

# Maximizing Originality & Ambition for Molina (Non-Bio)

**Verdict:** Steal his *method DNA* (interpretable latents + mechanistic priors + probabilistic comparison on real systems), not his *domain*. Bio is optional flavor; physics-trained, mechanism-hungry ML is the signal he will notice.

Sources: [IE faculty profile](https://www.ie.edu/university/about/faculty/nacho-molina/), [Faculty Spotlight](https://www.ie.edu/school-science-technology/news/faculty-spotlight-with-nacho-molina/), syllabus ML-AM.2.S.A, his toolkits (DeepCycle / FourierCycle / FateCompass / ActiVAE / HiddenFoot).

---

## 0. His research taste in one sentence

He wants models where **a low-dimensional latent has physical/mechanistic meaning**, trained on **messy real data**, with **uncertainty + model comparison**, producing **mechanistic insight**—not leaderboard points.

| His toolkit | What it actually encodes |
|---|---|
| DeepCycle | Structured latent (circular phase) via AE + known geometry |
| FourierCycle | Latent phase → **ODE rates** via mechanistic fit |
| FateCompass | Probabilistic transitions + **interpretable activity** model |
| ActiVAE | VAE decoder **constrained by prior interaction structure** |
| HiddenFoot | Biophysical stats mech + ML on molecule-scale data |
| Course spine | Bayesian comparison, kernels/GPs, manifold geometry (Bishop/Murphy) |

**Public values (Spotlight):** interpretability, transparency, validation, humility; “insight > black-box prediction.”

---

## 1. Non-bio project archetypes that still resonate

Ranked by taste-fit × course-feasibility (BAM semester project).

| # | Archetype | Why it clicks | Course anchors | Bio analog (do NOT do) |
|---|---|---|---|---|
| **A** | **Structured-latent hybrid** | Latents = phases / modes / states with geometry or conservation | AE/VAE + PCA/FA + manifolds | DeepCycle θ |
| **B** | **Physics/mech-informed decoder** | Known ODE/PDE/constitutive law in decoder; NN fills residuals | NNs + Bayesian LVM | ActiVAE / FourierCycle |
| **C** | **Probabilistic latent dynamics** | GPLVM / GP prior on latent traj; UQ on trajectories | GPs, kernels, Bayesian comparison | sc latent dynamics |
| **D** | **Nonlinear manifold + geometry** | Geodesic / spectral / periodic embeddings that *mean something* | Isomap, Laplacian Eigenmaps, MDS | cell-state manifolds |
| **E** | **Hybrid mechanistic + residual ML** | Baseline physics → learn discrepancy with GP/NN; ablate prior strength | GPs, ridge/Bayesian, NNs | HiddenFoot-style |
| **F** | **Interpretable “activity” / driver inference** | Infer latent drivers of high-dim observations under a linear/kernel generative map | FA, PPCA, kernels | FateCompass TF activities |
| **G** | **Spatial / field structure (non-omics)** | Space as inductive bias (kernels, graphs), not “CNN flex” | Kernels, spectral methods | spatial transcriptomics |

**Deprioritize (weak fit or fake ambition):** pure supervised Kaggle, RL demos, transformer-from-scratch, generic PINN-on-toy-PDE with no data story, black-box forecasting without latents/mechanisms.

**Hard rule:** domain ≠ bio; **question format** should still be: *“Given high-dim observations of a dynamical system, can we recover interpretable latent structure + parameters that a pure black-box misses?”*

---

## 2. Ambition signals vs fake ambition

### Graders notice (real ambition)

| Signal | What it looks like in the repo/report |
|---|---|
| **Scientific question first** | One falsifiable claim (“latent phase recovers known regimes better than PCA under noise X”) |
| **Hybrid model with a prior you can turn off** | Ablation: full hybrid vs no-physics vs no-latent |
| **Probabilistic comparison** | Marginal likelihood / ELBO / WAIC / CV log-score—not only RMSE |
| **Latents you can plot and narrate** | Phase portraits, mode amplitudes, uncertainty bands tied to physics |
| **Real data + known failure modes** | Missingness, sensor bias, regime shifts; you diagnose them |
| **Small model, deep understanding** | You derive why the decoder / kernel / ODE term is there |
| **Git history of science** | Commits: data → baseline → hybrid → ablation → insight (not dump-at-deadline) |
| **Negative results that teach** | “Physics prior helps OOD, hurts IID; here’s why” |

### Fake ambition (looks big, scores poorly with him)

| Fake signal | Why it fails |
|---|---|
| Huge DL / transformers “because SOTA” | Black-box; fights his interpretability creed |
| Toy PINN on Burgers/Lorenz only | No real-data struggle; textbook demo |
| Generic Kaggle + Autogluon | No originality; no mechanistic insight |
| “We implemented 12 models” | Breadth without a thesis |
| Fancy jargon without math | Oral Q&A kills this instantly |
| Bio-adjacent fluff with no method depth | Domain cosplay ≠ method resonance |
| One giant notebook, no baselines | Implementation without science |
| Claims of “new architecture” with no ablation | Originality theater |

**Ambition = hard scientific constraint + honest comparison**, not parameter count.

---

## 3. Five “wow” framing strategies (proposal writing)

Use these as opening frames; pick **one** primary.

### 1. “ActiVAE without genes”
> We embed **domain prior structure into the generative model** so latents are *named* quantities (torques, modes, regimes), not anonymous z’s. Compare constrained vs unconstrained VAE on the same data.

### 2. “DeepCycle without cells”
> High-dim observations live on a **known manifold** (periodic orbit, energy shell, SO(3)). We force the latent to respect that geometry and recover a continuous phase/angle that unsupervised PCA cannot.

### 3. “FourierCycle without RNA”
> Latent state → **ODE/PDE rates** via a mechanistic layer; ML only where the mechanism is incomplete. Report recovered parameters + predictive residual.

### 4. “Insight under uncertainty”
> Lead with **Bayesian model comparison**: which inductive bias explains the data? Show posterior predictive checks and where uncertainty spikes at regime boundaries.

### 5. “Humility as method” (mirrors his Spotlight language)
> Explicit limits: when the prior is misspecified, what breaks? Deliver a **validation protocol** (held-out regimes, sensor dropouts) as part of the contribution—not an apology.

**Proposal template (one paragraph):**
> **Problem.** [Real system + data]. **Gap.** Black-box ML predicts but doesn’t recover [mechanism/latent]. **Approach.** [Structured latent / GP / mech decoder] with [prior]. **Proof of ambition.** Ablate prior; compare vs PCA/GP/NN on IID + OOD; interpret latents against known physics. **Impact.** [One concrete decision or scientific claim].

---

## 4. Eight project directions (method DNA, new domain)

Each: **hook · method mix · data · ambition spike · oral trap to prepare for**.

### P1 — Satellite / orbital dynamics as structured latents
- **Hook:** Recover interpretable orbital elements / anomaly phase from noisy tracking or simulated TLEs + residuals.
- **Methods:** Circular/structured AE or GP-VAE; Keplerian (or SGP4-lite) decoder + learned residual GP.
- **Data:** public TLE / CSSI / CelesTrak; or high-fid sim with controlled process noise.
- **Ambition spike:** OOD on maneuver / drag regime; show physics prior beats black-box on scarce data.
- **Oral:** “What does each latent mean physically? Show ablation.”

### P2 — Soft-robot / continuum mechanics hybrid
- **Hook:** Predict continuum deformation with **Port-Hamiltonian / energy-aware** constraints + GP residual (SciML pattern already published for soft objects).
- **Methods:** Physics-constrained GP or mech decoder; UQ on tip pose.
- **Data:** public soft-robot datasets / SOFA sims / simple pneumatic actuator logs.
- **Ambition spike:** Compositionality / energy conservation checks; uncertainty for safe control.
- **Oral:** “Where does the model violate physics if unconstrained?”

### P3 — Materials microstructure → property with interpretable latents
- **Hook:** VAE/GPLVM on microstructure images or spectra; latents tied to process parameters (temperature, strain).
- **Methods:** Semi-physics decoder (constitutive / radiative-transfer-style layer) + free latents for unknowns (p3VAE-style idea).
- **Data:** open materials datasets (MatBench subsets, AFM/SEM public sets)—**avoid biomedical tissue**.
- **Ambition spike:** Disentangle acquisition artifacts vs material factors.
- **Oral:** “Name the latents; show intervention/extrapolation.”

### P4 — Climate / ocean field dynamics with physics-informed GPs
- **Hook:** Spatiotemporal GP with PDE/conservation constraints on currents, SST, or wind fields.
- **Methods:** State-space / variational GP + linear/nonlinear physics constraints; compare to pure GP and neural forecaster.
- **Data:** NOAA / Copernicus / ERA5 slices (keep spatial patch small for feasibility).
- **Ambition spike:** Forecast skill **and** constraint residual; UQ calibration.
- **Oral:** “Which physical constraint actually earned its keep?”

### P5 — Markets as noisy dynamical systems (not “stock prediction Kaggle”)
- **Hook:** Latent regime / factor dynamical system; compare linear SSM vs GP latent vs VAE-SSM; emphasize **model evidence**, not alpha bragging.
- **Methods:** Bayesian state-space, GPLVM, regime GMM/HMM baseline; stress-test nonstationarity.
- **Data:** FRED macros, crypto order-book snippets, or energy prices (cleaner story than equities hype).
- **Ambition spike:** Recover interpretable regimes around known events; show when mechanism-free models overfit.
- **Oral:** “This isn’t finance porn—show latent regimes and predictive checks.”

### P6 — Robotics perception under uncertainty
- **Hook:** Probabilistic latent state from high-dim sensors (depth, IMU, vision features) with known kinematics prior.
- **Methods:** Physics-enhanced GP-VAE / Φ-DVAE-style; Kalman/GP smoother on latents.
- **Data:** EuRoC, TUM RGB-D, or MuJoCo/Isaac logged trajectories.
- **Ambition spike:** Sensor dropout / lighting shift → calibrated uncertainty.
- **Oral:** “When is the encoder wrong but the physics prior saves you?”

### P7 — Structural / mechanical vibration modal discovery
- **Hook:** Nonlinear dim reduction that recovers modal coordinates / phase of vibrating structures.
- **Methods:** Laplacian Eigenmaps / Isomap vs circular AE; GP dynamics on modal latents; optional ODE modal model.
- **Data:** open SHM / beam vibration / NASA prognostics subsets.
- **Ambition spike:** Map latent angle to physical phase; detect damage as latent geometry change.
- **Oral:** “Relate embedding geometry to modal analysis textbook.”

### P8 — Energy systems / battery / grid as mechanistic hybrid
- **Hook:** Equivalent-circuit or thermal ODE prior + ML residual for SOH / load dynamics.
- **Methods:** Hybrid ODE decoder + Bayesian residual; compare pure NN vs pure circuit vs hybrid.
- **Data:** NASA battery, Oxford battery, or open grid load + weather.
- **Ambition spike:** Parameter recovery (R, C, fade rates) that a black-box never yields.
- **Oral:** “Show identified parameters vs nameplate / literature ranges.”

---

## 5. Practical selection matrix (for your team)

| Direction | Molina taste | Real data ease | Oral risk | Fake-ambition risk |
|---|---|---|---|---|
| P1 Satellite | ★★★★★ | ★★★★ | Med | Low if residual GP is real |
| P2 Soft robot | ★★★★★ | ★★★ | High math | Med (sim-only trap) |
| P3 Materials | ★★★★ | ★★★ | Med | Med (CNN cosplay) |
| P4 Climate GP | ★★★★★ | ★★★★ | Med | Med (too much data wrangling) |
| P5 Markets-as-dynamics | ★★★ | ★★★★★ | High (skeptical audience) | **High** if framed as trading |
| P6 Robot perception | ★★★★ | ★★★★ | Med | Med (SLAM cosplay) |
| P7 Vibration modalities | ★★★★★ | ★★★ | Low–Med | Low |
| P8 Battery hybrid | ★★★★ | ★★★★★ | Low | Low |

**Top shortlist for “impress without bio”:** **P1, P4, P7, P8** (best balance). Stretch wow: **P2**.

---

## 6. Rubric mapping (how to farm all 25% buckets)

| Rubric slice | How to score it with a non-bio Molina-aligned project |
|---|---|
| **Originality / Ambition (25%)** | One hybrid inductive bias + ablation of that bias; OOD regime test |
| **Implementation (25%)** | Clean PyTorch/sklearn pipeline; reproducible seeds; Git history; baselines runnable |
| **Insights / Impact (25%)** | Named latents, recovered parameters, failure analysis, decision-relevant UQ |
| **Understanding (25%)** | Oral: derive ELBO / GP marginal / ODE residual; know every modeling choice |
| **Comm (separate)** | Paper structure: question → model → evidence → limits (his humility frame) |

**Course fit tip:** stay fluent in syllabus objects (Bayesian comparison, kernels/GPs, PCA/FA, manifolds, optional AE). A light VAE/ODE layer is “outside syllabus but justified,” not a rewrite of NeurIPS.

---

## 7. Concrete do / don’t for the proposal sentence

**Do write:**
> “We learn a **mechanistically constrained latent dynamical model** of [system], compare it to unconstrained GP/NN/PCA baselines under IID and regime-shift splits, and interpret recovered latents against known physics.”

**Don’t write:**
> “We apply deep learning / PINNs / transformers to predict X with high accuracy on dataset Y.”

---

## 8. Immediate next step (if you want one)

Pick **two** from {P1, P4, P7, P8}, each with a **one-page mini-spec**: data URL, 3 baselines, hybrid prior, 2 ablations, 1 OOD split, oral Q list. Then kill one after a 48h data-viability check.