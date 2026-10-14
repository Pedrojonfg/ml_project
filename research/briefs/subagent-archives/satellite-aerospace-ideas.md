# Archive: satellite-aerospace-ideas
**Agent ID:** 6b089652-5b1a-42cb-a1c3-ff8c5d13f333

---

# Satellite / EO / Aerospace ML — Project Idea Cluster
**Team:** Pedro + Mario · **Course:** IE BAM ML (Fall 2026) · **Stack:** sklearn + PyTorch · **Horizon:** ~6 weeks · **Deliverable:** scientific-paper style  
**Constraints:** real data · ambition graded · **HEALTH veto** · Pedro aerospace/satellites 10 · Mario physics 8 / climate 7 / robotics 9

---

## Ranking criteria (how Top 3 were chosen)

| Criterion | Weight |
|-----------|--------|
| Pedro aerospace signal | high |
| Mario physics / climate / robotics fit | high |
| Ambition visible in a paper (baselines to beat, fusion, uncertainty) | high |
| 6-week feasibility with public data | hard gate |
| Clean sklearn → PyTorch ladder | medium |

---

## TOP 3 (recommended shortlist)

### 🥇 #1 — ESA Collision Avoidance: forecast final conjunction risk from CDM time series
**Cluster:** Debris / SSA · **Pedro 10 · Mario 9**

| Field | Detail |
|-------|--------|
| **Pitch** | Predict the *final* collision risk of a close-approach event from the sequence of Conjunction Data Messages (CDMs) that arrive before TCA — operational SSA ML, not “just another CNN on RGB.” |
| **RQ** | Given a partial CDM time series, can a model forecast the risk in the *last* CDM better than static feature baselines, and does incorporating miss-distance / covariance physics features reduce false alarms at high-Pc tails? |
| **Datasets + URLs** | ESA Kelvins Collision Avoidance Challenge (Zenodo): https://zenodo.org/records/4463683 · challenge/paper context: https://kelvins.esa.int/collision-avoidance-challenge/ · arXiv competition paper: https://arxiv.org/pdf/2008.03069.pdf · optional complement: Mendeley LEO conjunctions (TLEs): https://data.mendeley.com/datasets/yfcn6b52yz/1 · TraCSS screening test set (ephemeris/CDM answer keys): https://space.commerce.gov/dataset-for-conjunction-assessment-verification/ |
| **Methods (course)** | Feature engineering on CDMs; RF / GBDT / logistic / calibration (sklearn); event-level CV; PR-AUC / Brier / reliability diagrams |
| **Methods (stretch)** | LSTM / Transformer on CDM sequences (PyTorch); uncertainty (MC dropout / ensembles); physics-inspired features (Pc proxies, Mahalanobis miss); optional comparison to SOCRATES-style geometric features |
| **Ambition angle** | Real ops problem + published competition baseline; paper can claim better early-warning trade-off (risk vs lead time) |
| **6-week feasibility** | **High** — tabular/time-series, no heavy EO I/O; W1 data/EDA, W2–3 baselines, W4–5 DL, W6 ablations + paper |
| **Trade-offs** | Extremely strong Pedro fit; Mario physics shines; weaker “pretty maps” for slides; class imbalance / rare high-risk events need careful metrics |

---

### 🥈 #2 — OPS-SAT CubeSat telemetry anomaly detection (beat the public benchmark)
**Cluster:** CubeSat telemetry · **Pedro 10 · Mario 8.5**

| Field | Detail |
|-------|--------|
| **Pitch** | Detect anomalies in *real* ESA OPS-SAT CubeSat telemetry using the official OPSSAT-AD benchmark — spacecraft ops ML with operator-labeled anomalies. |
| **RQ** | On OPSSAT-AD, do deep sequence models outperform classical unsupervised detectors on rare telemetry anomalies, and which channels / feature sets drive detection? |
| **Datasets + URLs** | OPSSAT-AD Zenodo: https://zenodo.org/records/15108715 (also v1 https://zenodo.org/records/12588359) · code: https://github.com/kplabs-pl/OPS-SAT-AD · Scientific Data paper: https://www.nature.com/articles/s41597-025-05035-3 · arXiv: https://arxiv.org/html/2407.04730v1 |
| **Methods (course)** | Isolation Forest, One-Class SVM, LOF, RF on 18 handcrafted features; stratified split as published; F1 / AUROC / AUPRC |
| **Methods (stretch)** | Autoencoder / LSTM-AE / Transformer AD (PyTorch); channel-conditioned models; compare raw segments vs engineered features; optional onboard-constraint discussion (model size) |
| **Ambition angle** | 30 published baselines exist → “we beat / explain the benchmark” is a crisp paper story; pure aerospace |
| **6-week feasibility** | **High** — small AI-ready dataset (~2.1k fragments); W1 reproduce baselines, W2–4 models, W5 error analysis by channel, W6 paper |
| **Trade-offs** | Best Pedro narrative; Mario robotics/physics OK; less climate; risk of “just another AD bake-off” unless you add interpretability / ops lead-time analysis |

---

### 🥉 #3 — YieldSAT: multimodal crop-yield prediction (EO time series + weather/soil/topo)
**Cluster:** Crop + multi-modal EO+tabular · **Pedro 7.5 · Mario 8.5**

| Field | Detail |
|-------|--------|
| **Pitch** | Predict field- and pixel-level crop yield by fusing Sentinel-2 time series with weather, soil, and topography — textbook multimodal scientific ML with climate relevance. |
| **RQ** | How much does multimodal fusion (S2 + tabular env) improve yield RMSE vs S2-only or tabular-only models, and does performance transfer across countries/crops? |
| **Datasets + URLs** | YieldSAT: https://yieldsat.github.io/ · RAISE overview: https://raise4science.eu/practice/yieldsat/ · (paper PDF via DFKI/site) · lighter alternative if download is heavy: CropHarvest https://github.com/nasaharvest/cropharvest · Zenodo https://zenodo.org/record/5533193 |
| **Methods (course)** | Ridge / RF / GBDT on NDVI aggregates + weather; spatial/temporal CV; MAE/RMSE |
| **Methods (stretch)** | CNN/LSTM/Transformer on S2 (PyTorch); early/late/attention fusion with tabular branch; domain shift (country leave-one-out) |
| **Ambition angle** | Fresh multimodal benchmark (2016–2024, 4 countries, 4 crops); fusion + transfer experiments read as research, not homework |
| **6-week feasibility** | **Medium–High** if you **subset** (1–2 crops, 1–2 countries); full 12M pixels is too big — scope ruthlessly |
| **Trade-offs** | Strong Mario climate; Pedro EO solid but less “space systems”; data volume / storage is the main risk |

---

## Remaining ideas (ranked 4–11)

### #4 — Sen2Fire / SeasFire: satellite wildfire detection & drivers
**Cluster:** Wildfire · **Pedro 8 · Mario 9**

| Field | Detail |
|-------|--------|
| **Pitch** | Detect active fire / burned area from Sentinel (+ aerosol) and/or model fire occurrence from multivariate EO cubes — climate + EO. |
| **RQ** | Which spectral band subsets / indices maximize wildfire detection F1, and does adding Sentinel-5P aerosol (Sen2Fire) or climate drivers (SeasFire) improve skill beyond optical-only? |
| **Datasets + URLs** | Sen2Fire Zenodo: https://zenodo.org/records/10881058 · arXiv: https://arxiv.org/pdf/2403.17884 · FLOGA (Greece burn mapping): https://github.com/Orion-AI-Lab/FLOGA · SeasFire cube: https://pmc.ncbi.nlm.nih.gov/articles/PMC11876342/ · TS-SatFire: https://www.nature.com/articles/s41597-025-06271-3 · FIRMS/VIIRS: https://www.earthdata.nasa.gov/ |
| **Methods** | Course: RF on indices (NBR, NDVI), sklearn metrics · Stretch: U-Net / temporal CNN (PyTorch); class imbalance; optional SeasFire forecasting |
| **Ambition** | Band ablation + multi-sensor fusion paper; Mario climate peak |
| **6-week** | **High** (Sen2Fire patches) / **Medium** (SeasFire cube modeling) |
| **Trade-offs** | Great Mario; Pedro EO good; less “spacecraft” than #1–2; cloud/false-alarm analysis needed |

---

### #5 — SEN12-FLOOD / S1GFloods: SAR (+ optical) flood mapping
**Cluster:** SAR + multi-modal fusion · **Pedro 8.5 · Mario 8**

| Field | Detail |
|-------|--------|
| **Pitch** | Map floods with Sentinel-1 SAR (all-weather) and optionally fuse Sentinel-2 optical — physics of radar + disaster EO. |
| **RQ** | Does S1+S2 fusion outperform SAR-only under cloud, and how well do models generalize across continents/events? |
| **Datasets + URLs** | SEN12-FLOOD: https://github.com/ClmRmb/SEN12-FLOOD · ESA Source: https://source.coop/esa/sen12flood/imagery/0 · S1GFloods: https://github.com/tamer-saleh/s1gflood-detection · STURM-Flood Zenodo: https://zenodo.org/records/12748983 · BigEarthNet (general S1/S2): https://bigearth.net/ |
| **Methods** | Course: thresholding VV/VH, RF on SAR features · Stretch: Siamese/U-Net change detection (PyTorch); early/late fusion S1+S2 |
| **Ambition** | Cloud-robust SAR story + geographic OOD evaluation |
| **6-week** | **High–Medium** (use S1GFloods 256×256 pairs for speed) |
| **Trade-offs** | Strong technical EO; Mario physics (radar) good; less pure “space ops” than debris/CubeSat |

---

### #6 — OSCD / S2Looking: Sentinel urban change detection
**Cluster:** Sentinel/Landsat change detection · **Pedro 8 · Mario 6.5**

| Field | Detail |
|-------|--------|
| **Pitch** | Pixel-level urban change maps from bi-temporal Sentinel-2 (OSCD) — classic remote-sensing DL benchmark. |
| **RQ** | Do Siamese FCNs / transformers beat spectral-index + RF baselines on OSCD, and which bands matter most for urban change? |
| **Datasets + URLs** | OSCD: https://rcdaudt.github.io/oscd/ · IEEE DataPort: https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection · S2Looking: https://github.com/S2Looking/Dataset · LEVIR-CD+ (VHR, Google Earth): via same repo · OPTIMUS time-series (HF): https://huggingface.co/datasets/optimus-change/optimus-dataset · DynamicEarthNet paper: https://openaccess.thecvf.com/content/CVPR2022/html/Toker_DynamicEarthNet_Daily_Multi-Spectral_Satellite_Dataset_for_Semantic_Change_Segmentation_CVPR_2022_paper.html |
| **Methods** | Course: NDVI differencing, RF · Stretch: Siamese U-Net / BIT (PyTorch); band ablation |
| **Ambition** | Saturated field — need a twist (few-shot cities, band efficiency, uncertainty maps) |
| **6-week** | **High** (OSCD is small: 24 pairs) |
| **Trade-offs** | Easy to finish; risk of looking incremental vs Top 3; Mario interest lower |

---

### #7 — Urban Heat MiniCubes / Landsat LST: urban heat prediction & modality fusion
**Cluster:** Urban heat · **Pedro 7 · Mario 8.5**

| Field | Detail |
|-------|--------|
| **Pitch** | Predict / downscale urban land-surface temperature using Landsat LST + optical + SAR (+ optional GOES), for UHI science. |
| **RQ** | Can multimodal EO (reflectance + SAR roughness + coarse IR) predict fine LST better than land-cover indices alone, across cities? |
| **Datasets + URLs** | Urban Heat MiniCubes (NCAR): https://impacts.ucar.edu/en/datasets/urban-heat-minicubes/ · arXiv: https://arxiv.org/html/2606.11534v1 · HF LandsatTemperature (103 US cities): https://huggingface.co/datasets/JesseGuerrero/LandsatTemperature · USGS annual LST urban: https://doi.org/10.5066/P9H6E1FZ · GeoTwin-Heat (Mumbai package): https://github.com/nilkamalpmore/GeoTwin-Heat |
| **Methods** | Course: RF/GBDT on NDVI/NDBI/DEM · Stretch: CNN regressor; cross-city transfer; SAR ablation |
| **Ambition** | Climate + cities + multimodal; strong applied impact story |
| **6-week** | **Medium** (MiniCubes can be heavy — start with HF 103-cities or one city) |
| **Trade-offs** | Mario climate win; Pedro moderate; LST ≠ air temperature (must state carefully in paper) |

---

### #8 — PASTIS-R: optical + SAR crop parcel segmentation (multi-modal EO)
**Cluster:** Crop + SAR fusion · **Pedro 8 · Mario 8**

| Field | Detail |
|-------|--------|
| **Pitch** | Semantic/panoptic segmentation of crop parcels from Sentinel-2 time series, fused with Sentinel-1 — gold-standard multimodal EO. |
| **RQ** | Does S1+S2 fusion improve mIoU over S2-only under cloudy seasons, and which fusion strategy (early/late/attention) wins? |
| **Datasets + URLs** | PASTIS Zenodo: https://zenodo.org/records/5012942 · benchmark/code: https://github.com/VSainteuf/pastis-benchmark · PASTIS-R (S1+S2) linked from same repo |
| **Methods** | Course: RF on pixel temporal stats · Stretch: U-TAE / temporal CNN (PyTorch); fusion ablations |
| **Ambition** | Strong CV + remote sensing paper; published fusion baselines to cite |
| **6-week** | **Medium** — PASTIS ~29–54 GB; use subset of patches / semantic-only (skip panoptic) |
| **Trade-offs** | Technically impressive; GPU/storage hungry; less “aerospace ops” than #1–2 |

---

### #9 — OpenSky ADS-B: climb / trajectory / takeoff-weight style prediction
**Cluster:** Aviation / ADS-B · **Pedro 7 · Mario 8**

| Field | Detail |
|-------|--------|
| **Pitch** | Learn aircraft performance from ADS-B trajectories (climb prediction or related regression) — aerospace-adjacent, robotics/control flavored. |
| **RQ** | Can ML models predict altitude/speed over a 10-min climb horizon better than BADA-style baselines using only pre-departure / early-climb features? |
| **Datasets + URLs** | OpenSky scientific datasets: https://opensky-network.org/data/scientific · climbing segments ML set (linked there) · API docs: https://openskynetwork.github.io/opensky-api/rest.html · Eurocontrol PRC 2024 ATOW challenge (large): https://github.com/euranova/aviation-data-challenge-2024 · cleaned LHR–ZRH trajectories: https://zenodo.org/records/18916312 |
| **Methods** | Course: GBDT on climb features · Stretch: seq models (LSTM) on trajectories; physics residual learning vs BADA |
| **Ambition** | Physics + ML residual story; Mario robotics/physics strong |
| **6-week** | **Medium** — prefer OpenSky *published* climb dataset over full Trino (university access + data volume) |
| **Trade-offs** | Not Earth observation; weaker Pedro “satellites” story unless framed as ATM + space traffic adjacency |

---

### #10 — CropHarvest: global crop / non-crop classification with S1+S2+climate
**Cluster:** Crop + EO+tabular · **Pedro 7 · Mario 8**

| Field | Detail |
|-------|--------|
| **Pitch** | Lightweight, sklearn-friendly global agricultural classification with Sentinel + ERA5 — great if YieldSAT is too heavy. |
| **RQ** | How does geographic domain shift affect crop classifiers, and do Sentinel-1 / climate features stabilize transfer across continents? |
| **Datasets + URLs** | https://github.com/nasaharvest/cropharvest · Zenodo https://zenodo.org/record/5533193 · NeurIPS benchmarks paper PDF via GitHub |
| **Methods** | Course: RF (official demo) · Stretch: temporal CNN; leave-region-out evaluation |
| **Ambition** | Domain generalization focus upgrades a “simple” dataset into a research paper |
| **6-week** | **Very high** |
| **Trade-offs** | Safer grade path; less wow than YieldSAT / SSA / OPS-SAT |

---

### #11 — Multi-modal EO + tabular “systems” mini-project: wildfire or heat with auxiliary tables
**Cluster:** Explicit multi-modal fusion EO+tabular · **Pedro 7.5 · Mario 9**

| Field | Detail |
|-------|--------|
| **Pitch** | Same scientific spine as #3/#4/#7 but framed as *fusion methodology*: images/cubes + ERA5/soil/DEM tables with controlled ablations. |
| **RQ** | Under what missing-data regimes (cloudy S2, sparse labels) does tabular context recover predictive skill lost by EO-only models? |
| **Datasets + URLs** | Pair any of: Sen2Fire + ERA5; Urban Heat MiniCubes; YieldSAT ADMs; SeasFire multivariate cube |
| **Methods** | Course: stacking (EO embeddings → sklearn head) · Stretch: gated multimodal nets; modality dropout training |
| **Ambition** | Methods paper angle (“when fusion helps”) rather than only application SOTA |
| **6-week** | **Medium** — pick **one** application domain and freeze it in week 1 |
| **Trade-offs** | Flexible; risk of unfocused scope if you chase too many modalities |

---

## Fit matrix (quick view)

| # | Idea | Pedro | Mario | Ambition | 6-wk ease | Paper punch |
|---|------|------:|------:|----------|-----------|-------------|
| 1 | ESA CDM collision risk | 10 | 9 | ★★★★★ | ★★★★★ | ★★★★★ |
| 2 | OPS-SAT AD | 10 | 8.5 | ★★★★★ | ★★★★★ | ★★★★★ |
| 3 | YieldSAT multimodal yield | 7.5 | 8.5 | ★★★★★ | ★★★★ | ★★★★★ |
| 4 | Wildfire Sen2Fire/SeasFire | 8 | 9 | ★★★★ | ★★★★★ | ★★★★ |
| 5 | SAR flood SEN12/S1G | 8.5 | 8 | ★★★★ | ★★★★ | ★★★★ |
| 6 | OSCD change detection | 8 | 6.5 | ★★★ | ★★★★★ | ★★★ |
| 7 | Urban heat LST | 7 | 8.5 | ★★★★ | ★★★ | ★★★★ |
| 8 | PASTIS-R S1+S2 crops | 8 | 8 | ★★★★★ | ★★★ | ★★★★★ |
| 9 | ADS-B OpenSky | 7 | 8 | ★★★★ | ★★★ | ★★★★ |
| 10 | CropHarvest | 7 | 8 | ★★★ | ★★★★★ | ★★★ |
| 11 | EO+tabular fusion method | 7.5 | 9 | ★★★★ | ★★★ | ★★★★ |

---

## Cross-cutting recommendations

1. **If maximizing Pedro’s aerospace passion:** shortlist **#1 (SSA)** and **#2 (OPS-SAT)**; pick one primary, keep the other as backup.
2. **If balancing Mario climate:** pair aerospace primary with **#3 YieldSAT** or **#4 wildfire** as the compromise pick.
3. **Ambition without dying in data eng:** prefer AI-ready Zenodo/HF benchmarks (OSCD, OPSSAT-AD, Sen2Fire, ESA CDMs) over raw Copernicus downloads in week 1.
4. **Paper template that graders like:** problem → baselines (sklearn) → deep model (PyTorch) → ablation → limitations → ethics/ops impact.
5. **Hard no:** health (honored). Soft caution: pure OSCD without a twist may look less ambitious than SSA/CubeSat.

---

## Suggested decision path (next 48h)

1. Pedro/Mario each independently rank Top 3 from this list.  
2. Kill anything both score &lt;7 on personal fit.  
3. Verify download + one end-to-end sklearn baseline in a weekend (feasibility gate).  
4. Lock scope: **one primary RQ + two ablations max**.

**Default recommendation:** start with **#1 ESA Collision Avoidance**; if you want more “satellite platform” romance than “catalog risk,” switch to **#2 OPS-SAT**; if climate must share the spotlight, take **#3 YieldSAT (subsetted)**.