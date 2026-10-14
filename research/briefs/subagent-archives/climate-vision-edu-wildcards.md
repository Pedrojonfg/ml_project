# Archive: climate-vision-edu-wildcards
**Agent ID:** 0e433743-3336-43ba-9590-5f663219f0e7
**Title:** Research climate energy vision edu

---

# Deep Research Brief: Ambitious IE BAM ML Ideas (Pedro + Mario)

**Constraints baked in:** ~6 weeks · sklearn + PyTorch · ambition critical · VETO health · underexplored overlaps preferred · scores: Pedro C7/V9/E9/M8/Mu6/S6 · Mario C7/V7/E7/M5/Mu6/S6

**Scoring lens:** shared strength = climate + vision + education; Pedro can carry mobility; music/sport are stretch spice, not core.

---

## Cluster A — Climate / energy / sustainability (ambitious)

### A1. Cloud-motion PV nowcasting (satellite + ground fusion)
**Pitch:** Predict next 0.5–6h solar irradiance / PV yield from geostationary satellite stacks + station observations—not “temperature → energy” regression, but *cloud-field dynamics* as a spatiotemporal forecast problem.

**RQ:** Can a PyTorch spatiotemporal model (ConvLSTM / U-Net + temporal encoder) beat physics-derived and classical baselines on short-horizon solar radiation under held-out geographies?

**Datasets + URLs**
- SolarCube (NeurIPS 2024 D&B): https://doi.org/10.5281/zenodo.11498739 · code https://github.com/Ruohan-Li/SolarCube
- NASA POWER (meteo/solar ARD): https://power.larc.nasa.gov/ · https://data.nasa.gov/dataset/prediction-of-worldwide-energy-resources-power
- Optional UK PV ground truth: https://huggingface.co/datasets/openclimatefix/uk_pv

**Methods:** sklearn baselines (persistence, ridge on engineered sky features) → PyTorch image-timeseries encoder; point vs area forecasts; CRPS / skill scores vs clear-sky models.

**Ambition:** High (real grid-relevant nowcasting). **Feasibility:** Medium–high if you subset continents/stations; full SolarCube is heavy.

**Fit:** Both climate 7; Pedro vision 9 carries imagery. **Trade-offs:** Data plumbing eats week 1–2; Europe coverage limited in SolarCube 2018 slice.

---

### A2. Next-day wildfire spread as multimodal time-series CV
**Pitch:** Forecast tomorrow’s active-fire map from 23-channel stacks (fire history, fuel, topo, weather)—a rare *physics-messy, label-noisy, class-imbalanced* fusion showcase.

**RQ:** Does multi-day temporal context (T=5) + modality ablation beat mono-temporal CNNs on next-day fire spread under strict spatial/temporal CV?

**Datasets + URLs**
- WildfireSpreadTS: https://doi.org/10.5281/zenodo.8006177 · https://github.com/SebastianGer/WildfireSpreadTS
- Optional extension WSTS+: https://arxiv.org/abs/2502.12003 · https://huggingface.co/saadlahrichi/WSTSPlus
- FIRMS context: https://www.earthdata.nasa.gov/data/tools/firms

**Methods:** sklearn on tabularized channels → U-Net / U-TAE in PyTorch; PR-AUC / IoU; uncertainty + imbalance handling (not accuracy).

**Ambition:** Very high. **Feasibility:** Medium (48GB Zenodo + HDF5 conversion; need disk + GPU).

**Fit:** Climate + vision sweet spot. Frame as *Earth-system prediction*, not health. **Trade-offs:** Storage/ops risk; noisy labels; easy to overclaim causality.

---

### A3. Cross-climate building energy transfer (M&V, not plain load forecast)
**Pitch:** Reuse ASHRAE/BDG2 meters to learn *climate-invariant* building representations: predict under held-out weather regimes / sites for measurement & verification style transfer.

**RQ:** Can domain-adversarial or leave-one-climate-out transfer retain predictive skill when weather distributions shift, vs site-specific models?

**Datasets + URLs**
- Building Data Genome 2: https://github.com/buds-lab/building-data-genome-project-2 · https://www.kaggle.com/datasets/claytonmiller/buildingdatagenomeproject2
- Paper: https://www.nature.com/articles/s41597-020-00712-x
- ASHRAE GEPIII context: https://www.kaggle.com/c/ashrae-energy-prediction

**Methods:** Gradient boosting baselines → temporal CNN/Transformer; CORAL / DANN / FiLM weather conditioning; residual anomaly detection for M&V.

**Ambition:** High (transfer + uncertainty, not Kaggle redo). **Feasibility:** High (tabular/time-series friendly).

**Fit:** Climate 7 both; less vision flash. **Trade-offs:** Feels “safer” academically unless you nail transfer/eval story; Mario/Pedro both can own modeling.

---

## Cluster B — Computer vision / signals (non-health)

### B1. Fields of the World: zero-shot field-boundary generalization
**Pitch:** Instance/semantic segmentation of agricultural parcels from multi-date Sentinel-2; stress-test *geographic domain shift* (train Europe → Africa/Asia).

**RQ:** Which training-country mixtures maximize zero-shot IoU / boundary F1 on held-out continents, and can lightweight adapters beat full fine-tuning under a 6-week compute budget?

**Datasets + URLs**
- FTW site: https://fieldsofthe.world/
- Benchmark data: https://source.coop/kerner-lab/fields-of-the-world
- Baselines: https://github.com/fieldsoftheworld/ftw-baselines
- Paper: https://arxiv.org/abs/2409.16252

**Methods:** U-Net / Mask2Former-style seg; sklearn on spectral indices as weak baseline; country leave-out protocol; qualitative Ethiopia-style zero-shot demos.

**Ambition:** Very high (SOTA-adjacent remote sensing). **Feasibility:** Medium–high with country subsets.

**Fit:** Pedro vision 9 + climate/ag overlap; Mario vision 7 solid co-pilot. **Trade-offs:** License mix across countries; GPU needed; easy to become “just fine-tune baseline.”

---

### B2. Harvest piles as a proxy for smallholder cropland activity
**Pitch:** Detect ephemeral harvest piles in satellite imagery to map farming activity where classical cropland maps fail—weird, high-impact, under-copied.

**RQ:** Can a CNN classifier/detector trained on HarvestNet labels recover cropland signal beyond existing coverage maps, and how does it transfer across Ethiopian regions / years?

**Datasets + URLs**
- HarvestNet (AAAI 2024): https://github.com/jonxuxu/harvest-piles · data https://figshare.com/s/45a7b45556b90a9a11d2
- Paper: https://ojs.aaai.org/index.php/AAAI/article/view/30251

**Methods:** ResNet/EfficientNet + hard-negative mining; optional weakly supervised localization; compare to public cropland layers.

**Ambition:** High + distinctive. **Feasibility:** High (~7k labeled images).

**Fit:** Vision + climate/food systems; both scores align. **Trade-offs:** Narrow geography; label expert-dependence; storytelling must stay rigorous (proxy ≠ yield).

---

### B3. Global satellite → road *graph* extraction
**Pitch:** Not pixel road masks—predict topology (nodes/edges) for connectivity analytics (equity, logistics readiness).

**RQ:** Can a PyTorch model trained on Global-Scale Road Dataset recover graph connectivity metrics (completeness, connectivity) better than segmentation→skeletonization pipelines?

**Datasets + URLs**
- HF dataset: https://huggingface.co/datasets/gaetanbahl/Global-Scale-Road-Dataset
- Method/code: https://github.com/earth-insights/samroadplus
- Paper: https://arxiv.org/abs/2411.16733

**Methods:** Segmentation + graph heuristics vs end-to-end graph predictors; OSM as noisy labels; evaluate APLS / TOPO-style metrics.

**Ambition:** High. **Feasibility:** Medium (graph ML learning curve; imagery size).

**Fit:** Pedro mobility 8 + vision 9; Mario mobility 5 → Pedro leads eval framing. **Trade-offs:** OSM label bias; CVPR-level methods may exceed 6 weeks if not scoped.

---

## Cluster C — Education / learning analytics (ambitious)

### C1. Cross-course cognitive transfer (not single-course KT)
**Pitch:** Model whether mastery in course A predicts / transfers to course B for the *same students*—personalized learning’s hardest open problem.

**RQ:** Does a multi-task / shared-student embedding improve next-response prediction and cold-start in a second course vs independent KT models?

**Datasets + URLs**
- PTADisc (cross-course subsets): https://github.com/wahr0411/PTADisc
- EdNet (large interactive tutoring traces): https://github.com/riiid/ednet · paper https://arxiv.org/abs/1912.03072
- MoocRadar (fine-grained concepts + Bloom tags): https://github.com/THU-KEG/MOOC-Radar

**Methods:** sklearn logistic/GBDT on engineered histories → DKT/DKVMN/SAKT-style PyTorch; student-level nested CV; concept graphs as side info.

**Ambition:** Very high (underexplored vs vanilla KT). **Feasibility:** Medium (scale; Chinese-platform quirks; subset courses).

**Fit:** Education 9/7—team’s strongest shared non-vision lane. **Trade-offs:** Privacy/ethics narrative needed; compute on 680M logs requires ruthless sampling.

---

### C2. Curriculum-aware next-item recommendation with process data
**Pitch:** Go beyond “will they get it right?” to *which problem next*—using curriculum folder structure + process features (hints, attempts, timing).

**RQ:** Can an attention model using curricula hierarchy + process signals recommend next items that improve predicted mastery / engagement vs difficulty-only heuristics?

**Datasets + URLs**
- ASSISTments + process/curricula (OSF): https://osf.io/yrwuh/
- Classic ASSISTments 2009–10: https://sites.google.com/site/assistmentsdata/home/2009-2010-assistment-data
- Related framing: https://jedm.educationaldatamining.org/index.php/JEDM/article/download/689/215

**Methods:** Offline policy eval (IPS / sequential eval); bandit or ranking head on KT state; sklearn baselines (IRT, spaced practice rules).

**Ambition:** High (decision-making, not prediction-only). **Feasibility:** Medium–high.

**Fit:** Both education-strong; interpretability demo for BAM presentation. **Trade-offs:** Offline eval ≠ real classroom; avoid claiming causal learning gains without caveats.

---

### C3. Topic-linked educational video engagement (multimodal LA)
**Pitch:** Predict engagement from Wikipedia-linked lecture fragments + transcripts—explainable content features, not black-box watch-time only.

**RQ:** Which content representations (Wikipedia topics, transcript linguistics, fragment structure) best predict engagement, and do personalized models beat population baselines?

**Datasets + URLs**
- PEEK: https://ar5iv.labs.arxiv.org/html/2109.03154 · companion VLEngagement https://github.com/sahanbull/context-agnostic-engagement
- In-video STEM clickstreams + transcripts: https://pmc.ncbi.nlm.nih.gov/articles/PMC12555877/
- Optional hard multimodal stretch (slides↔speech): LPM https://openaccess.thecvf.com/content/ICCV2023/papers/Lee_Lecture_Presentations_Multimodal_Dataset_Towards_Understanding_Multimodality_in_Educational_Videos_ICCV_2023_paper.pdf

**Methods:** sklearn on topic TF-IDF / BERT PCA → PyTorch sequence models over fragments; SHAP/topic explanations; cold-start users.

**Ambition:** High + presentation-friendly. **Feasibility:** High for PEEK; LPM is stretch.

**Fit:** Education peak for Pedro; Mario co-owns NLP/features. **Trade-offs:** Engagement ≠ learning; informal OER ≠ formal courses.

---

## Cluster D — Mobility / cities / logistics

### D1. Industrial last-mile ETA + route behavior (LaDe)
**Pitch:** Learn courier spatiotemporal behavior for ETA / next-stop under real industrial constraints—closer to ops research × ML than toy traffic.

**RQ:** Can a spatiotemporal GNN / sequence model beat classical ETA baselines on LaDe delivery & pickup across cities with different densities?

**Datasets + URLs**
- LaDe (KDD’24): https://huggingface.co/datasets/Cainiao-AI/LaDe · mirror https://huggingface.co/datasets/tianyi1777/LaDe
- ACM: https://dl.acm.org/doi/10.1145/3637528.3671548

**Methods:** Feature-rich GBDT → Traj/GNN PyTorch; city transfer; time-window violation rates as business metric.

**Ambition:** High. **Feasibility:** Medium (data volume; domain unfamiliarity).

**Fit:** Pedro mobility 8 carries; Mario 5 → pair programming on features/eval. **Trade-offs:** China-city context; engineering-heavy; Mario interest risk.

---

### D2. Graph-augmented urban traffic forecasting (GO-MO Madrid)
**Pitch:** 10 years of intensity/speed/occupancy on a real sensor graph—multi-metric forecasting + shock detection (events, weather).

**RQ:** Does explicit road/route graph structure improve multi-horizon forecasts of intensity & speed jointly vs independent sensor models?

**Datasets + URLs**
- GO-MO: https://huggingface.co/datasets/dmariaa70/GO-MO
- City open data lineage: Madrid traffic open data (via GO-MO docs)

**Methods:** sklearn VAR/GBDT → ST-GCN / Graph WaveNet; multi-task heads; extreme-day evaluation.

**Ambition:** High. **Feasibility:** Medium (1.5B records → sample years/sensors).

**Fit:** Pedro mobility lead. **Trade-offs:** Classic ST forecasting crowded; ambition must come from multi-metric + graph ablations + extremes.

---

### D3. Bike-share demand under climate extremes (mobility × climate overlap)
**Pitch:** Predict station-level bike demand conditional on weather shocks (heatwaves, storms)—resilience analytics for cities.

**RQ:** Do models that explicitly encode extreme-weather regimes reduce error on shock days more than average-day RMSE improvements suggest?

**Datasets + URLs**
- UCTB Urban-Dataset (NYC/CHI/DC bikes): https://github.com/uctb/Urban-Dataset
- Raw systems: Citi Bike https://www.citibikenyc.com/system-data · Divvy · Capital Bikeshare
- Weather: NOAA / ERA5 / NASA POWER https://power.larc.nasa.gov/

**Methods:** Ridge/GBDT → temporal GNN; stratified metrics on extreme quantiles; counterfactual “no-shock” residuals.

**Ambition:** Medium–high (overlap novelty). **Feasibility:** High.

**Fit:** Pedro mobility + both climate. **Trade-offs:** Must avoid looking like “yet another bike forecast”; extreme-day protocol is the thesis.

---

## Cluster E — Wildcards (music / sport / OSS vehicle / fusion)

### E1. Open-source vehicle: Open Climate Fix PV site prediction contribution
**Pitch:** Ship a *real PR* (baseline model, eval harness, missing-data robustness, or satellite feature ablation) into an active climate-ML org—project = science + engineering artifact.

**RQ:** What model/feature choices improve UK PV site forecasts under realistic lag/NaN conditions in OCF’s framework, documented as reproducible experiments?

**Datasets + URLs**
- UK PV: https://huggingface.co/datasets/openclimatefix/uk_pv
- pv-site-prediction: https://github.com/openclimatefix/pv-site-prediction
- Org overview / related tooling: https://github.com/openclimatefix

**Methods:** Fit their config system; sklearn→PyTorch ablation; contribution-quality tests + docs.

**Ambition:** High (external impact). **Feasibility:** Medium (onboarding friction; “ease of contribution: hard” noted upstream).

**Fit:** Climate both; Pedro vision if sat features enter. **Trade-offs:** Scope depends on maintainers; risk of “tooling week” without ML depth—mitigate with a crisp experimental claim.

---

### E2. Audio → musician body motion (MOSA cross-modal MIR)
**Pitch:** Predict expressive body motion from audio (or reverse: expression semantics from motion/audio)—weird, demoable, non-health wearables/mocap.

**RQ:** Can a sequence model map audio features to joint trajectories with musically meaningful beat/phrase alignment better than frame-independent regressors?

**Datasets + URLs**
- MOSA GitHub: https://github.com/yufenhuang/MOSA-Music-mOtion-and-Semantic-Annotation-dataset
- Paper: https://arxiv.org/html/2406.06375

**Methods:** librosa + sklearn → Transformer/TCN; DTW / joint-angle metrics; optional expression classification head.

**Ambition:** High novelty. **Feasibility:** Medium (mocap formats; both music 6).

**Fit:** Wildcard spice; neither is music-primary. **Trade-offs:** Classical piano/violin niche; harder “IE BAM impact” narrative vs climate/edu.

---

### E3. Dense soccer ball-action spotting under label scarcity
**Pitch:** Spot high-frequency ball actions (12 classes) with only ~7 annotated games—semi-/self-supervised transfer from 500 SoccerNet games.

**RQ:** Does pretraining on sparse action spotting + unlabeled video improve mAP@1 on dense ball actions vs training from scratch on 7 games?

**Datasets + URLs**
- SoccerNet data hub: https://www.soccer-net.org/data
- Ball Action Spotting: https://www.soccer-net.org/tasks/ball-action-spotting
- HF 224p set: https://huggingface.co/datasets/OpenSportsLab/soccernetpro-localization-snbas
- Dev kit: https://github.com/SoccerNet/sn-spotting

**Methods:** Feature extractors + temporal CNN/Transformer; pseudo-labeling; sklearn on frozen features as baseline.

**Ambition:** High. **Feasibility:** Medium (video IO; sport 6/6).

**Fit:** Fun wildcard; weaker than vision-ag/edu for team identity. **Trade-offs:** Compute + download gating; “sports analytics” may feel less IE-core.

---

### E4. Fusion showcase: GOES smoke plume segmentation (SmokeViz)
**Pitch:** Segment ordinal smoke density from geostationary imagery at scale—climate × CV × signals; atmospheric framing (not clinical health).

**RQ:** Can a segmentation model recover ordinal smoke-density structure from SmokeViz, and does multi-band GOES input beat RGB-only under cloud confusion?

**Datasets + URLs**
- SmokeViz (NeurIPS D&B): https://noaa-gsl-experimental-pds.s3.amazonaws.com/index.html#SmokeViz/
- Paper PDF: https://papers.neurips.cc/paper_files/paper/2025/file/3b2116b636f64553d7fe33d87a701b06-Paper-Datasets_and_Benchmarks_Track.pdf
- Related Fire-D: https://zenodo.org/records/15109641

**Methods:** U-Net ordinal / multi-class; cloud/smoke confusion analysis; sklearn on spectral features.

**Ambition:** Very high. **Feasibility:** Medium (new dataset maturity; S3 plumbing).

**Fit:** Vision + climate. **Trade-offs:** Stay clear of health-impact claims (veto adjacency); dataset may still be experimental.

---

## Overall Top 5 (from this set)

| Rank | Idea | Why it wins for Pedro+Mario |
|------|------|-----------------------------|
| **1** | **B1 — FTW field-boundary domain generalization** | Hits Pedro’s vision peak + climate/ag mission; Mario can own training/eval; clear ambition; public baselines; 6-week-scopeable via country subsets. |
| **2** | **A1 — SolarCube / satellite PV nowcasting** | Shared climate strength + vision for Pedro; grid-relevant story; optional E1 OSS path if you want external impact. |
| **3** | **C1 — Cross-course knowledge transfer (PTADisc/EdNet)** | Best *education-ambition* fit (9/7); underexplored vs vanilla KT; sklearn→PyTorch ladder is clean. |
| **4** | **A2 — WildfireSpreadTS multimodal spread** | Pure fusion showcase; high weird/ambition; strong climate×vision; watch the 48GB ops tax. |
| **5** | **C3 — Topic-linked video engagement (PEEK)** | Ambitious LA with explainable topics; lighter infra than satellite; Pedro education 9 owns narrative. |

**Honorable near-misses:** B2 HarvestNet (most “weird-ok” CV), D3 bike×extremes (best mobility given Mario’s M5), E1 OCF contribution (if you want a portfolio artifact beyond a report).

---

## Practical shortlist strategy (2-week decision)

1. **If you want max BAM wow + CV portfolio:** B1 FTW (± B2 HarvestNet as backup if storage/GPU hurts).  
2. **If you want climate impact + possible OSS:** A1 SolarCube, with E1 as stretch deliverable.  
3. **If you want strongest shared education play:** C1 cross-course KT, with C2 as recommendation extension.  
4. **Avoid as primary** unless Pedro is hungry for mobility ownership: pure D1/D2 (Mario M5). Use D3 only as climate-overlap spice.  
5. **Wildcards E2/E3** only if the team explicitly wants demo energy over domain fit.

---

## Research notes (what “underexplored” meant here)

Crowded traps avoided: plain temperature regression, ImageNet-finetune for its own sake, single-course DKT reimplementation, vanilla bike/traffic RMSE races, health wearables.

Preferred wedges: **domain shift**, **cross-entity transfer** (course/climate/city), **multimodal fusion with honest noise**, **decision policies offline**, **topology not just pixels**, **OSS as vehicle**.
