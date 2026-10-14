# Archive: robotics-cyphy-ideas
**Agent ID:** 63cb344d-583c-4b12-90a4-ff5b6846d10d

---

# Robotics / Control / Perception Cluster — Deep Research Brief

**Team:** Pedro (physics/robotics/quantum/aerospace, max ambition) + Mario (finance/recommenders, **hard veto health/omics**, wants original + data + model comparison)  
**Stack:** Python, sklearn, PyTorch · ~6 weeks · 2-page proposal soon · ambition = 25%  
**Prof signal:** Nacho Molina values probabilistic / physics-informed flavor (GPs, PINNs, VAEs) as *method* extensions — his own lab is Health & MedTech; robotics alignment is via **CyPhy / IE Robotics & AI Lab**, not Nacho’s domain.

---

## 1. Concrete project ideas (10)

### Idea A — Continuum-robot shape & force: PINN vs classical ML
| Field | Content |
|--------|---------|
| **Pitch** | Learn tendon→shape (and force-aware) maps for a continuum arm, comparing PINNs that bake kinematics priors against GP / boosting / neural baselines. |
| **RQ** | Does a physics-informed neural network reduce data hunger and improve OOD shape estimation under external loads vs pure data-driven models? |
| **Datasets** | [RoboArm Shape Estimation (IEEE DataPort)](https://ieee-dataport.org/documents/tendon-driven-continuum-robot-roboarm-shape-estimation-dataset) — dual-camera + 6 tendon tensions, free-motion & loaded; optional sim priors via [SoMoGym](https://github.com/GrauleM/somogym). |
| **Methods** | Regression, kernels/GP, trees/boosting, NN, **PINN extension**, PCA on image/marker features. |
| **Why ambitious** | Soft/continuum robotics + PINNs = interview-wow and Nacho-aligned; rare in BAM-style courses. |
| **Risks / 6w** | Image pipeline + PINN training can eat weeks; mitigate by using marker/feature vectors first, PINN as stretch. **Feasible if scoped.** |
| **Fit** | Pedro **10** · Mario **4** (model comparison only). |
| **Trade-offs** | Max originality & ambition; Mario engagement weaker unless he owns the full model bake-off + uncertainty analysis. |

---

### Idea B — TrajAir: socially-aware aircraft trajectory prediction
| Field | Content |
|--------|---------|
| **Pitch** | Predict multi-aircraft trajectories in non-towered terminal airspace, conditioning on history, social interactions, and weather. |
| **RQ** | Which inductive bias wins for 3D social aerial prediction: GPs, gradient boosting, sequence NNs, or a hybrid (boosting residuals + NN)? |
| **Datasets** | [TrajAir](https://theairlab.org/trajair/) · code [trajairnet](https://github.com/castacks/trajairnet) · paper [arXiv:2109.15158](https://arxiv.org/abs/2109.15158) (ADS-B + METAR, 111 days). |
| **Methods** | Regression, kernels/SVM, trees/boosting, NN, optional **GP** / clustering of traffic patterns. |
| **Why ambitious** | Real aerospace social navigation; clean public benchmark + room for original model comparison. |
| **Risks / 6w** | Sequence modeling complexity; stick to fixed horizons + ADE/FDE vs constant-velocity. **Highly feasible.** |
| **Fit** | Pedro **10** · Mario **6** (feature engineering, weather, model tournament). |
| **Trade-offs** | Strong Pedro story; less “weird”; Mario isn’t in finance territory but has a clear analytical role. |

---

### Idea C — ALFA UAV: probabilistic fault detection from flight logs
| Field | Content |
|--------|---------|
| **Pitch** | Detect and classify injected flight faults on a real autonomous UAV from telemetry, with calibrated uncertainty. |
| **RQ** | Can unsupervised autoencoders / PCA / GMM flag faults early, and do supervised trees/NN + GP classifiers improve type ID and calibration? |
| **Datasets** | [ALFA Dataset](https://theairlab.org/alfa-dataset/) · [tools](https://github.com/castacks/alfa-dataset-tools) — 47 autonomous sequences, 8 fault types, CSV/MAT (ROS optional). |
| **Methods** | PCA/clustering, autoencoders, logistic/trees/boosting, NN, optional **GP** / VAE. |
| **Why ambitious** | Real flight failures + reliability narrative; aerospace + probabilistic ML. |
| **Risks / 6w** | Class imbalance / few sequences; need careful CV. **Feasible** (CSV path avoids ROS pain). |
| **Fit** | Pedro **9** · Mario **5**. |
| **Trade-offs** | Safer than soft robotics; less “original question” unless you add early-warning curves + calibration. |

---

### Idea D — RODEO-flavored robot service marketplace (CyPhy-aligned, no lab)
| Field | Content |
|--------|---------|
| **Pitch** | Treat robots as economic agents: learn to *verify* task success from telemetry and *recommend* which robot/skill should bid next (matching market). |
| **RQ** | Can ML recover a reliable “proof-of-work” signal from physical execution logs, and does a recommender improve task–robot matching vs greedy baselines? |
| **Datasets** | Constructed marketplace layer on top of [voraus-AD](https://github.com/vorausrobotik/voraus-ad-dataset) and/or [BotFails](https://huggingface.co/datasets/kantine/BotFails); optional narrative tie to [RODEO](https://cyphy.life/projects/rodeo-robotic-decentralized-organization/). |
| **Methods** | Anomaly detection (AE/PCA), classification, clustering of behaviors, **recommender** (collaborative / content / ranking), optional VAE embeddings. |
| **Why ambitious** | Original framing; CyPhy ROBOPRENEUR/RODEO alignment **without hardware or blockchain**; Mario’s finance brain + Pedro’s systems brain. |
| **Risks / 6w** | “Constructed” market must be principled (not toy); scope verification ML first, recommender as Week 4–6. **Feasible with discipline.** |
| **Fit** | Pedro **8** · Mario **9**. |
| **Trade-offs** | Best team balance; risk of looking “gimmicky” if market is fake—mitigate with clear protocol + ablations. |

---

### Idea E — Open X-Embodiment skill retrieval recommender
| Field | Content |
|--------|---------|
| **Pitch** | Embed robot episodes and build a retrieval/recommender that proposes the best prior demonstrations for a new task/embodiment. |
| **RQ** | Do language + proprioception + action embeddings beat vision-only retrieval for cross-embodiment skill recommendation? |
| **Datasets** | [Open X-Embodiment](https://robotics-transformer-x.github.io/) · [GitHub](https://github.com/google-deepmind/open_x_embodiment) — **use 1–3 small constituent datasets**, not the full 1M traj. |
| **Methods** | PCA/clustering, autoencoders/VAE, NN encoders, ranking metrics (Recall@K), sklearn baselines on engineered features. |
| **Why ambitious** | Foundation-robotics adjacent; Mario gets a real recommender; Pedro gets embodiment/control framing. |
| **Risks / 6w** | Data engineering hell if you go too big; **must** subset aggressively. Medium–high risk. |
| **Fit** | Pedro **7** · Mario **10**. |
| **Trade-offs** | Mario-optimal; ambition high but reproducibility fragile unless dataset IDs are frozen in the proposal. |

---

### Idea F — Soft-arm imitation: ManiSoft policy bake-off
| Field | Content |
|--------|---------|
| **Pitch** | Imitation learning on soft continuum arm demos; compare classical (trees on state) vs NN behavioral cloning vs latent AE features. |
| **RQ** | On soft manipulation, do simple state-based models close the gap to deep BC when demos are noisy/randomized? |
| **Datasets** | [ManiSoft](https://github.com/buaa-colalab/ManiSoft) (HF demos, 6300 eps, COLL/ALN/ARR/STK). |
| **Methods** | Regression, trees/boosting, NN, AE, clustering of skills. |
| **Why ambitious** | Soft robotics + modern benchmark; rare course topic. |
| **Risks / 6w** | Sim stack / deps; may be heavy for BAM timeline. Medium risk. |
| **Fit** | Pedro **9** · Mario **4**. |
| **Trade-offs** | Cool but Mario-thin; prefer Idea A if choosing soft robotics. |

---

### Idea G — DIGIT tactile contact / force: AE + supervised heads
| Field | Content |
|--------|---------|
| **Pitch** | From vision-based tactile images, learn contact geometry and/or 3-axis force, with unsupervised tactile embeddings. |
| **RQ** | Do autoencoder/VAE tactile latents transfer across objects for contact localization and force regression better than raw-pixel CNNs? |
| **Datasets** | [YCB-Slide (DIGIT)](https://github.com/rpl-cmu/YCB-Slide) · [GelSight force (HF)](https://huggingface.co/datasets/facebook/gelsight-force-estimation) · [3D Cal DIGIT/GelSight (Zenodo)](https://zenodo.org/records/18462608). |
| **Methods** | PCA, AE/VAE, CNN regression/classification, kernels on latent features, clustering of contact modes. |
| **Why ambitious** | Perception that interviews love; multimodal + probabilistic latents. |
| **Risks / 6w** | Image DL compute; keep resolution/models small. Feasible. |
| **Fit** | Pedro **8** · Mario **3**. |
| **Trade-offs** | Strong science report visuals; weak Mario ownership unless he owns evaluation design. |

---

### Idea H — MuJoCo residual dynamics: GP vs NN vs boosting
| Field | Content |
|--------|---------|
| **Pitch** | Learn residual dynamics (Δstate predictors) from offline MuJoCo trajectories and quantify when GPs beat deep nets. |
| **RQ** | For low-data regime control datasets, do GPs with physics features outperform NN/boosting on multi-step prediction and uncertainty? |
| **Datasets** | [Minari MuJoCo](https://minari.farama.org/datasets/mujoco/index.html) / [D4RL→Minari](https://minari.farama.org/datasets/D4RL/index.html); env via [Gymnasium](https://gymnasium.farama.org/). |
| **Methods** | Regression, kernels/GP, trees, NN, PCA; optional short-horizon MPC-style rollout eval (not full RL). |
| **Why ambitious** | Control-theoretic + probabilistic; clean scientific comparison for Nacho. |
| **Risks / 6w** | Can look “homework-y” unless RQ is sharp (sample complexity curves). Low technical risk. |
| **Fit** | Pedro **8** · Mario **5**. |
| **Trade-offs** | Safest GitHub repro; ambition depends on framing (must emphasize uncertainty + residual physics). |

---

### Idea I — Swarm foraging outcome prediction (CyPhy swarm-adjacent, constructed)
| Field | Content |
|--------|---------|
| **Pitch** | Simulate robot swarms, predict mission success / resource allocation from partial observations — “see the unseen” without a projector. |
| **RQ** | Can latent embeddings + classifiers predict swarm mission success from local traces better than handcrafted graph features? |
| **Datasets** | Construct with PettingZoo / simple multi-agent sim; optional inspiration from [Tangible Swarm](https://www.cyphy.life/projects/tangible-swarm/) & [secure swarm cooperation](https://www.cyphy.life/projects/secure-cooperation-in-robot-swarms/). |
| **Methods** | Clustering, PCA, trees/NN, AE on trajectories, graph features. |
| **Why ambitious** | Direct thematic line to CyPhy swarm work without lab access. |
| **Risks / 6w** | Constructed data must be justified as realistic; reviewers may discount sim-only. Medium risk. |
| **Fit** | Pedro **7** · Mario **6** (if framed as resource/market allocation). |
| **Trade-offs** | Narrative alignment high; scientific credibility lower than TrajAir/ALFA unless you publish the generator. |

---

### Idea J — Industrial robot anomaly + “charge/service” decision policy
| Field | Content |
|--------|---------|
| **Pitch** | Detect anomalies on industrial arm time-series, then learn a simple policy/recommender for when to pause, reassign, or “pay for maintenance.” |
| **RQ** | Which detector (AE vs IsolationForest vs boosting) maximizes early AUROC, and does a cost-sensitive recommender reduce downtime in a simulated ops layer? |
| **Datasets** | [voraus-AD](https://github.com/vorausrobotik/voraus-ad-dataset); optional [kitting anomaly ROS bags](https://github.com/birlrobotics/kitting_anomaly_dataset) (heavier). |
| **Methods** | PCA, AE, trees/boosting, logistic, clustering; ops recommender on top. |
| **Why ambitious** | Factory-adjacent (IE lab “smart factories” station); Mario cost/ops angle. |
| **Risks / 6w** | voraus-AD is solid; ROS bags are a trap for 6 weeks. Feasible if CSV-only. |
| **Fit** | Pedro **6** · Mario **8**. |
| **Trade-offs** | Less flashy than soft robots/aerospace; strong reproducibility and team balance. |

---

## 2. What IE CyPhy / Robotical AI works on — and how to align without lab access

### CyPhy Life ([cyphy.life](https://cyphy.life/))
Student research group under **Eduardo Castelló** (IEX Labs / School of Science & Technology). Interest areas:
- Digital↔physical experiences  
- Robots interfacing with humans individually / collectively / **institutionally**  
- **Decentralized technologies** for cyber-physical institutions  

**Research lines**
| Line | Examples |
|------|----------|
| **ROBOPRENEUR** | Robot economic agents; [RODEO](https://cyphy.life/projects/rodeo-robotic-decentralized-organization/) — blockchain task registry, verifiable execution proofs, token payment, trash→charge loop |
| **Tangible User Interfaces** | SPICE (projected cooking), DJESTHESIA, GAME, Alfred companion |
| **Swarm Robotics** | [Tangible Swarm](https://www.cyphy.life/projects/tangible-swarm/) (camera–sim–projector overlay); [secure/secret swarm cooperation](https://www.cyphy.life/projects/secure-cooperation-in-robot-swarms/) (Merkle-tree mission proofs) |

### IE Robotics & AI Lab
Physical workspace (IE Tower): smart factories, embedded, humanoids, smart transportation, AI/CV. GitHub org [IERoboticsAILab](https://github.com/IERoboticsAILab) (BOTZO dog, WidowX arm, OptiTrack demos). CyPhy is the selective research overlay on top of this lab.

### Nacho Molina (course ML flavor ≠ robotics lab)
Head of **Health & MedTech Lab**; probabilistic / biophysics-informed DL background. For *this* project: use GPs/PINNs/VAEs as **methodology**, keep domain **non-health** (Mario veto).

### Alignment **without** lab access (recommend these hooks in the proposal)
| CyPhy theme | No-lab project hook |
|-------------|---------------------|
| RODEO / robopreneur | Ideas **D, J** — verification + marketplace/recommender on public logs |
| Swarm / tangible swarm | Idea **I** — predict/visualize latent swarm state from trajectories |
| Smart factories / arms | Ideas **J, F, H** |
| Aerospace-ish “smart transportation” | Ideas **B, C** |
| Perception station | Idea **G** |

You do **not** need OptiTrack, WidowX, or blockchain to cite CyPhy as *motivation*; cite the research question (verification, institutional robots, swarm observability) and stay on public data.

---

## 3. Open dataset map (robotics cluster)

| Domain | Dataset | URL | Notes for 6 weeks |
|--------|---------|-----|-------------------|
| **Manipulation / OXE** | Open X-Embodiment | https://robotics-transformer-x.github.io/ | Subset only |
| **MuJoCo / offline** | Minari MuJoCo + D4RL | https://minari.farama.org/ | Clean, reproducible |
| **Soft / continuum** | RoboArm shape | https://ieee-dataport.org/documents/tendon-driven-continuum-robot-roboarm-shape-estimation-dataset | PINN-ready |
| | SoMoGym / SoMo-RL | https://github.com/GrauleM/somogym | Sim toolkit |
| | ManiSoft | https://github.com/buaa-colalab/ManiSoft | Soft IL demos |
| **Tactile** | YCB-Slide DIGIT | https://github.com/rpl-cmu/YCB-Slide | Contact + pose |
| | GelSight force | https://huggingface.co/datasets/facebook/gelsight-force-estimation | Force/slip |
| | 3D Cal DIGIT/GelSight | https://zenodo.org/records/18462608 | Probe localization |
| **UAV / aerospace** | TrajAir | https://theairlab.org/trajair/ | Social aerial traj |
| | ALFA faults | https://theairlab.org/alfa-dataset/ | Real fault labels |
| | ProjectAirSim kinematics | https://huggingface.co/datasets/qincheng037/ProjectAirSim-UAV-Kinematic-Trajectories | Sim UAV |
| **Anomaly / ops** | voraus-AD | https://github.com/vorausrobotik/voraus-ad-dataset | Industrial TS |
| | BotFails | https://huggingface.co/datasets/kantine/BotFails | Multimodal fails |
| | Baxter kitting bags | https://github.com/birlrobotics/kitting_anomaly_dataset | Heavy ROS |
| **Tactile sim** | tactile_envs | https://github.com/carlosferrazza/tactile_envs | MuJoCo+tactile |

**Avoid for 6 weeks:** full OXE training, large ROS-bag corpora, full RL on soft robots, anything requiring IE lab hardware for the *core* result.

---

## 4. Top 3 for this team

| Rank | Idea | Why this team |
|------|------|----------------|
| **1** | **D — RODEO-flavored verification + robot-service recommender** | Best Pedro×Mario joint product: physical ML (anomaly/success) + finance-style matching. CyPhy-aligned without lab. Original for a BAM report. Ambition narrative writes itself. |
| **2** | **A — Continuum shape/force with PINN bake-off** | Max interview-wow for Pedro; Nacho-grade methods; Mario runs the full classical-vs-PINN comparison. Slightly weaker Mario “domain” but strongest *scientific* ambition. |
| **3** | **B — TrajAir social aerial prediction** | Cleanest path to a polished 10–12 page scientific report in 6 weeks; Pedro aerospace identity; model comparison is first-class. Less CyPhy-flavored, more “will definitely finish.” |

**Decision heuristic for the 2-pager**
- Want **CyPhy name-drop + team balance** → **#1 (D)**  
- Want **max ambition / physics-ML** → **#2 (A)**  
- Want **lowest execution risk before proposal** → **#3 (B)**  

**Honorable mention:** **E (OXE skill recommender)** if Mario must lead the research question; only if you pre-commit to 1–2 named OXE subsets in the proposal.

---

### Proposal tip (one sentence)
Lead with a sharp RQ + frozen dataset IDs + a 3-tier model ladder (sklearn baselines → PyTorch NN/AE → one Nacho-extension: GP **or** PINN **or** VAE)—that structure scores ambition *and* feasibility under a 6-week clock.