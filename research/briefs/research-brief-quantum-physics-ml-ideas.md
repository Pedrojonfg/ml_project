# Research Brief: Quantum / Physics-Informed / Dynamical-Systems ML Ideas
**Depth**: wide  
**Date**: 2026-10-11  
**Cluster**: Quantum ML · physics-informed ML · dynamical systems · hard-science ML  
**Constraints**: Pedro (quantum/physics 10, invent/research-wow) + Mario (physics/quantum ~8, paper-reproduce, **no health**) · Prof Nacho Molina (probabilistic + physics-informed) · stack sklearn + PyTorch · ~6 weeks · real data · paper-style report  

## Executive Summary

Best bets combine **(i)** a reproducible paper core Mario can own, **(ii)** one inventable scientific twist for Pedro, and **(iii)** uncertainty / probabilistic evaluation for the professor—without collapsing into “toy PINN on Burgers.” Top 3: **(1)** stochastic/dissipative HNN–LNN + conservation-law discovery on real + chaotic systems; **(2)** quantum-chemistry force/energy surrogates (revised MD17 / QM9) with physics constraints + UQ; **(3)** classical ML of simulated quantum-circuit outcomes with scalable transfer and calibration.

## Scoring rubric (0–10)

| Axis | Meaning |
|------|---------|
| **Pedro** | Research-wow, quantum/physics depth, room to invent |
| **Mario** | Clear paper to reproduce, tractable pipeline |
| **Prof** | Physics-informed and/or probabilistic story |
| **Ambition** | How impressive if it works |
| **Feasibility** | Realistic in ~6 weeks with sklearn+PyTorch |

**Toy risk** = likely to read as generic student demo (Burgers PINN, ideal mass-spring only, Kaggle-without-physics).

---

## Idea catalogue (11)

### 1. Quantum chemistry surrogate: energies + forces (MD17 revised / QM9)
| Field | Detail |
|-------|--------|
| **RQ** | Can a PyTorch GNN (or SchNet-style message-passing) predict DFT energies/forces with force–energy consistency, and do calibrated ensembles beat sklearn baselines under out-of-distribution conformations? |
| **Datasets** | **Revised MD17** (energies + forces, PyG `MD17`); optional **QM9** (~134k molecules, HOMO/LUMO/gap via PyG); stretch: ANI-1x subset |
| **Methods** | sklearn RF/GB baselines on fingerprints/descriptors; PyTorch GNN; physics loss \(F = -\nabla_R E\); ensemble / MC-dropout UQ; MAE vs DFT |
| **Ambition** | High — real quantum many-body surrogate |
| **Feasibility** | High (data + loaders exist); GNN learning curve is the bottleneck |
| **Scores** | Pedro **9** · Mario **8** · Prof **8** · Ambition **8** · Feasibility **8** |
| **Trade-offs** | QM9 property-only is safer but more “done”; MD17 forces are more physics-informed but need careful train splits. Equivariant nets (e3nn) raise ambition and implementation risk. |
| **Toy risk** | **Low–medium** if you stop at QM9 HOMO regression with bare MLP. **Mitigate**: forces + consistency + OOD + UQ. |

### 2. Matbench bandgap (composition / structure) with multi-fidelity UQ
| Field | Detail |
|-------|--------|
| **RQ** | How well can sklearn + PyTorch models predict PBE/experimental bandgaps, and can multi-fidelity (DFT→expt) or conformal prediction improve calibrated errors on rare chemistries? |
| **Datasets** | Matbench `mp_gap` (~106k structure→PBE gap), `expt_gap` (~4.6k composition→expt); optional 2025 Shef-AIRE multi-fidelity bandgap set |
| **Methods** | Magpie/composition features + RF/XGBoost; CGCNN-lite or ALIGNN-level if time; nested CV per Matbench protocol; conformal / quantile regression |
| **Ambition** | Medium–high (materials genomics, clear leaderboard) |
| **Feasibility** | Very high |
| **Scores** | Pedro **7** · Mario **9** · Prof **7** · Ambition **7** · Feasibility **9** |
| **Trade-offs** | Strong Mario/prof deliverable; less “quantum invent” unless you invent a physics prior (e.g. element-wise gap bounds, formation-energy constraints). Easy to look like a standard materials Kaggle if no physics/UQ twist. |
| **Toy risk** | **Medium** — leaderboard cloning without scientific question. **Mitigate**: multi-fidelity + calibration + OOD by chemistry family. |

### 3. PINNs / hybrid solvers on *non-toy* PDEs (sparse-data reconstruction)
| Field | Detail |
|-------|--------|
| **RQ** | Given sparse DNS observations, can a physics-informed network reconstruct Navier–Stokes wake / Allen–Cahn / shallow-water fields better than pure data-driven U-Net, with uncertainty on unobserved regions? |
| **Datasets** | PDEBench (DaRUS) 2D NS / shallow-water / reaction–diffusion; Raissi cylinder-wake sparse PINN setting; DeepXDE demos as scaffolding |
| **Methods** | Data-only U-Net/FNO baseline; PINN residual loss; optional DeepONet/FNO surrogate; ensemble residuals as UQ |
| **Ambition** | High if framed as *data assimilation / sparse reconstruction*, not “solve Burgers from scratch” |
| **Feasibility** | Medium — PINNs are finicky; NS data-free is known to fail (SciPy experience report) |
| **Scores** | Pedro **7** · Mario **7** · Prof **9** · Ambition **8** · Feasibility **6** |
| **Trade-offs** | Perfect prof fit; training instability can eat the timeline. Prefer **sparse-data PINN** over data-free CFD replacement. |
| **Toy risk** | **HIGH** if Burgers/1D advection only. **Mitigate**: PDEBench NS or shallow-water + compare FNO vs PINN + report failure modes. |

### 4. Learning conservation laws from trajectories
| Field | Detail |
|-------|--------|
| **RQ** | Without knowing the ODE, can neural methods recover the number and form of conserved quantities on Hamiltonian and near-integrable systems, and detect breakdown of approximate conservation under chaos/noise? |
| **Datasets** | Simulated: harmonic, Kepler, double pendulum, magnetic mirror, 3-body (AI Poincaré suite); **dysts** chaotic systems; optional real double-pendulum videos/trajectories (ConservNet) |
| **Methods** | Reproduce AI Poincaré / ConservNet / neural deflation; compare to SINDy (sklearn sparse regression); phase-transition detection via \(n_{\mathrm{eff}}\) |
| **Ambition** | Very high conceptually (discovery, not just prediction) |
| **Feasibility** | Medium–high on simulated data; symbolic recovery is hard |
| **Scores** | Pedro **10** · Mario **8** · Prof **9** · Ambition **9** · Feasibility **7** |
| **Trade-offs** | Invention space huge; risk of “only simulated toys.” Pair with noisy/chaotic regimes and a real trajectory if possible. |
| **Toy risk** | **Medium** if only ideal HO. **Mitigate**: multi-system benchmark + noise + detect approximate conservation failure. |

### 5. Hamiltonian / Lagrangian Neural Networks (energy-conserving dynamics)
| Field | Detail |
|-------|--------|
| **RQ** | Do HNNs/LNNs outperform black-box Neural ODEs on long-horizon rollout and energy drift, and can a *learned* dissipative / stochastic extension capture real pendulum friction while quantifying predictive uncertainty? |
| **Datasets** | Greydanus HNN suite (spring, pendulum, 2-/3-body, **real pendulum**); Cranmer LNN double pendulum; gym pixel-pendulum; optional dysts |
| **Methods** | Reproduce HNN (PyTorch ports exist) + LNN (originally JAX—reimplement core in PyTorch); Neural ODE / MLP baselines; invent: contact Hamiltonian, Rayleigh dissipation, or probabilistic HNN (ensemble energy) |
| **Ambition** | High — flagship physics-informed ML |
| **Feasibility** | High for reproduction; medium for invent layer |
| **Scores** | Pedro **9** · Mario **9** · Prof **10** · Ambition **9** · Feasibility **8** |
| **Trade-offs** | Pure reproduction of Greydanus alone can look expected; the invent layer (dissipation/noise/UQ) is what separates you. |
| **Toy risk** | **Medium–high** if only ideal mass-spring. **Mitigate**: real pendulum + chaos + dissipation/UQ. |

### 6. Chaos prediction with physics-aware metrics
| Field | Detail |
|-------|--------|
| **RQ** | Across the dysts catalogue, which models maximize valid prediction time, and does embedding physics (conservation residuals, spectral constraints) or probabilistic ensembles beat vanilla LSTM under noise? |
| **Datasets** | **dysts** (135 systems, NeurIPS 2021); Lorenz-96 / Kuramoto–Sivashinsky; ReservoirPy generators |
| **Methods** | sklearn/RF windowed baselines; LSTM/TCN PyTorch; Echo-State / reservoir; Neural ODE; metrics: valid time, attractor statistics, Lyapunov-aware scores; deep ensembles |
| **Ambition** | High if multi-system + probabilistic + physics metrics |
| **Feasibility** | High |
| **Scores** | Pedro **8** · Mario **8** · Prof **8** · Ambition **8** · Feasibility **8** |
| **Trade-offs** | Less “quantum” on the surface; easy to invent by coupling with HNN/SINDy (hybrid Idea 4+5+6). Single Lorenz-63 LSTM is a classic toy. |
| **Toy risk** | **HIGH** for single Lorenz + LSTM only. **Mitigate**: dysts multi-system, KS/L96, probabilistic valid-time. |

### 7. Plasma / tokamak disruption prediction (public data)
| Field | Detail |
|-------|--------|
| **RQ** | Can ML forecast disruptions from multi-signal time series with calibrated alert lead times transferable across devices? |
| **Datasets** | **MAST** via DisruptionPy (open S3); ITPA Disruption Database (multi-tokamak, public with access instructions); DIII-D/C-Mod need credentials (yellow); EAST restricted |
| **Methods** | sklearn classifiers on engineered plasma features; LSTM/TCN; class imbalance / survival-style lead-time metrics; physics features (q-profile proxies, locked modes) |
| **Ambition** | Very high (ITER-relevant) |
| **Feasibility** | **Low–medium** for 6 weeks — data access + domain onboarding dominate |
| **Scores** | Pedro **8** · Mario **6** · Prof **7** · Ambition **9** · Feasibility **4** |
| **Trade-offs** | Spectacular if data arrives week 1; catastrophic if stuck on MDSplus access. Prefer only if MAST/ITPA download is verified in week 0. |
| **Toy risk** | **Low** scientifically; **project-risk high** operationally. |

### 8. Gravitational-wave glitch classification (Gravity Spy)
| Field | Detail |
|-------|--------|
| **RQ** | Beyond accuracy, can probabilistic / multi-view models improve calibration and discovery of novel glitch morphologies under distribution shift (O1–O3 → O4-like)? |
| **Datasets** | Gravity Spy (~8.5k labeled Q-transform images, 22 classes); Zenodo O1–O3 ML classifications; O4 multi-view papers |
| **Methods** | CNN baselines (sklearn on handcrafted spectrogram features); PyTorch multi-duration fusion + attention; temperature scaling / conformal prediction; open-set / novelty detection |
| **Ambition** | Medium–high (real LIGO ops problem) |
| **Feasibility** | High |
| **Scores** | Pedro **7** · Mario **8** · Prof **7** · Ambition **7** · Feasibility **9** |
| **Trade-offs** | Baseline accuracy already ~98% on closed set—**must** pivot to UQ, shift, or open-set. More CV than physics-informed unless you inject detector physics features. |
| **Toy risk** | **Medium** if “CNN beats RF on Gravity Spy.” **Mitigate**: calibration + shift + physics metadata. |

### 9. Climate / Earth-system PDE surrogates
| Field | Detail |
|-------|--------|
| **RQ** | Can a neural operator (FNO) or constrained MLP emulate ClimateBench spatial responses to forcings, and do energy/mass soft constraints improve OOD SSP scenarios? |
| **Datasets** | **ClimateBench** (NorESM2/CMIP6 forcings→T/precip/…); PDEBench climate-adjacent PDE tasks; ERA5 downscaling papers as methods refs |
| **Methods** | sklearn spatial baselines; FNO/U-Net PyTorch; soft conservation constraints; probabilistic ensembles across ensemble members |
| **Ambition** | High societal relevance + SciML |
| **Feasibility** | Medium (data volume, geo tooling) |
| **Scores** | Pedro **6** · Mario **7** · Prof **8** · Ambition **8** · Feasibility **6** |
| **Trade-offs** | Fits prof; weaker quantum pull for Pedro. Climate politics/noise can distract from hard-science ML story. |
| **Toy risk** | **Low–medium**. Avoid trivial global-mean regression only. |

### 10. Classical ML of quantum circuit outcomes (no hardware)
| Field | Detail |
|-------|--------|
| **RQ** | Can classical models (CNN/MLP + sklearn) learn the map from circuit descriptors → Pauli expectation values from exact simulation, extrapolate to larger/deeper circuits, and when does learning *fail* (barren / scrambling regimes)? |
| **Datasets** | Generate with **Qiskit / PennyLane** statevector sims (n≤10–12, controlled depth); reproduce Cantori et al. (scalable CNNs on random circuits); SRE-Estimation-style feature pipelines |
| **Methods** | Gate one-hot / angle encodings → CNN; RF on gate histograms; transfer learning small→large n; ensemble UQ; compare wall-clock vs exact simulation |
| **Ambition** | High for this team (quantum + invent + clear failure analysis) |
| **Feasibility** | High (you generate the data) |
| **Scores** | Pedro **10** · Mario **8** · Prof **7** · Ambition **9** · Feasibility **8** |
| **Trade-offs** | “Real data” is simulated—argue as *ab initio computational experiment* (same as QM9). Need a sharp scientific claim (extrapolation limits, not just fit). |
| **Toy risk** | **Medium** if tiny circuits + perfect accuracy. **Mitigate**: scaling laws, failure regimes, calibration vs depth. |

### 11. Probabilistic Neural ODEs / Bayesian dynamics on physical systems
| Field | Detail |
|-------|--------|
| **RQ** | Do probabilistic Neural ODEs (ensemble / Laplace / dropout) give better-calibrated trajectory forecasts than point HNNs on noisy physical data, and can physics residuals act as a second loss for better coverage? |
| **Datasets** | Real pendulum (HNN repo); dysts noisy variants; optional MD17 as continuous dynamics on latent reaction coordinates |
| **Methods** | Neural ODE (torchdiffeq); deep ensembles; energy/residual regularizers; reliability diagrams on rollout |
| **Ambition** | High for prof (explicitly probabilistic) |
| **Feasibility** | Medium (training Neural ODEs + UQ is slow) |
| **Scores** | Pedro **8** · Mario **7** · Prof **10** · Ambition **8** · Feasibility **6** |
| **Trade-offs** | Excellent framing; overlaps heavily with Ideas 5–6—best as the *evaluation layer* of a top pick, not a standalone vague project. |
| **Toy risk** | **Medium** without a concrete physical system. |

---

## Toy-risk watchlist (avoid or harden)

| Pattern | Why it looks generic | Harden by… |
|---------|----------------------|------------|
| PINN on Burgers / 1D heat only | Every SciML tutorial | PDEBench NS / shallow-water + sparse data |
| Ideal mass-spring HNN only | Greydanus Fig. 1 demo | Real pendulum + dissipation + chaos |
| Single Lorenz-63 LSTM | Undergraduate chaos homework | dysts multi-system + probabilistic valid time |
| QM9 MLP on fingerprints only | MoleculeNet homework | Forces, equivariance, consistency, OOD |
| Gravity Spy CNN accuracy chase | Saturated closed-set task | Calibration, shift, open-set |
| Matbench leaderboard clone | Automatminer redux | Multi-fidelity + conformal + physics priors |

---

## Ranked Top 3 (this team, 6 weeks)

### #1 — Dissipative / probabilistic HNN–LNN + conservation-law discovery
**Blend of Ideas 4 + 5 (+6 metrics).**  
Mario reproduces Greydanus HNN + Cranmer LNN on standard systems; Pedro invents a dissipative/stochastic extension and/or AI-Poincaré-style conservation discovery; both evaluate long-horizon energy drift, \(n_{\mathrm{eff}}\), and calibrated uncertainty on real pendulum + selected dysts systems.  
**Why #1**: max joint fit (physics-informed × invent × reproduce × prof). Clear paper lineage, still research-wow if the invent layer works.  
**6-week sketch**: W1–2 reproduce HNN/LNN · W3 real pendulum + baselines · W4 invent dissipative/UQ · W5 conservation-law module · W6 ablations + paper.

### #2 — Quantum chemistry energy–force surrogates with physics constraints + UQ
**Idea 1 (MD17 revised primary; QM9 optional).**  
Sklearn baselines → PyTorch GNN → force–energy consistency → ensemble calibration on OOD conformers.  
**Why #2**: Strong quantum story for Pedro, clean ML workflow for Mario, “real” computational-physics data, less dynamical-systems than #1 but more quantum-chemistry wow.  
**Risk**: GNN debugging time; keep architecture simple (SchNet-like) not SOTA equivariant unless ahead of schedule.

### #3 — Classical learning of quantum circuit outcomes (simulation-generated)
**Idea 10.**  
Generate circuits with PennyLane/Qiskit; train scalable CNN/MLP + sklearn; study extrapolation in \(n\) and depth; map failure when entanglement/scrambling grows; report calibration.  
**Why #3**: Unique quantum-ML identity without hardware; invent room (when classical learners beat/lose to simulation); Mario has a concrete paper to mirror. Slightly weaker “physics-informed PDE” signal for the prof unless you add Hamiltonian simulation / Ising Trotter structure.

### Close runners-up
- **Chaos + dysts probabilistic forecasting (#6)** — excellent if merged into #1.  
- **Matbench multi-fidelity bandgap (#2 catalogue)** — safest grade, less wow.  
- **Sparse PINN/FNO on PDEBench NS (#3 catalogue)** — only if team accepts training pain.  
- **Gravity Spy UQ (#8)** — strong deliverable, thinner physics-informed core.  
- **Tokamak (#7)** — park unless data access proven day 0.

---

## Suggested decision rule

1. If you want **maximum research-wow + prof alignment**: pick **Top #1**.  
2. If you want **quantum chemistry identity**: pick **Top #2**.  
3. If you want **explicit Quantum ML branding without hardware**: pick **Top #3**.  
4. Do **not** start a Burgers-only PINN or single-Lorenz LSTM.

## Sources (key)

- Matbench / Materials Project tasks: https://matbench.materialsproject.org/  
- QM9 / MD17 via PyTorch Geometric docs  
- Greydanus HNN: https://github.com/greydanus/hamiltonian-nn · Cranmer LNN: https://github.com/MilesCranmer/lagrangian_nns  
- AI Poincaré (PRL 2021); ConservNet (arXiv:2102.04008); SINDy (PNAS 2016)  
- PDEBench (NeurIPS 2022); DeepXDE; SciPy PINN fluids experience report  
- dysts / Gilpin NeurIPS 2021 chaos benchmark  
- DisruptionPy (MAST open); ITPA disruption DB  
- Gravity Spy dataset + O4 multi-view fusion papers  
- ClimateBench (Zenodo / JAMES 2022)  
- Cantori et al. supervised learning of random quantum circuits; PennyLane/Qiskit simulators  
- Course constraints: `docs/decisions/LEDGER.md`, syllabus (real data, sklearn+PyTorch, paper+oral)
