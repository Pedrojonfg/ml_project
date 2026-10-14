# Archive: fintech-vc-ideas
**Agent ID:** 7a7a209b-12f8-4e0e-bc81-3ca2b4ad7390
**Title:** Research innovative fintech VC

---

(Canonical full brief: `../research-brief-innovative-finance-vc-recommenders.md`)

# Research Brief: Innovative finance / VC / markets / recommenders (non-generic)
**Depth**: wide  
**Date**: 2026-10-11  
**Cluster**: IE BAM ML project (~6 weeks, sklearn + PyTorch)  
**Audience fit**: Mario (finance 9/10 + named recommender interest); Pedro (fintech only if innovative; VC intriguing; hates generic student projects); **veto health**.

## Executive Summary

Avoid Kaggle credit scoring and “predict next-day stock return.” The strongest dual-fit projects sit at **VC deal-flow / founder–investor matching** (Pedro’s VC pull + Mario’s recommenders) or **prediction-market microstructure / calibration** (genuinely non-commoditized markets ML with open APIs). Pure LOB / earnings-call projects can be ambitious but risk looking like “another student markets NLP” unless the research question is sharply non-generic. **Top 3**: (1) founder–investor matching recommender, (2) multi-source early-stage success / Series-A prediction, (3) Polymarket calibration & cross-market mispricing.

**Ambition scale used below**: A1 = solid course project · A2 = strong / paper-shaped · A3 = research-frontier stretch for 6 weeks.

---

## Idea catalogue (10)

### 1. Founder ↔ investor matching recommender (bipartite + ranking)
**RQ.** Given a startup’s stage, sector, geography, and thesis text, can we rank investors by *realized* fit (historical co-investment / portfolio adjacency) better than stage–sector filters and TF-IDF baselines?

**Datasets + URLs**
- Open Funding Data (7k+ investors, co-investment graph): https://openfundingdata.com/
- VCSheets investors (HF): https://huggingface.co/datasets/calebheinzman/VCSheets_Investors
- OpenBook (open VC DB): https://github.com/iloveitaly/openbook/
- SEC Form D (related persons / offerings): https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets · HF mirrors https://huggingface.co/datasets/XOOMAR/sec-form-d-offerings · https://huggingface.co/datasets/weio-ops/sec-form-d
- YC company index (Algolia / public lists) + Wikidata enrichment (used by commercial matchers; scrape carefully)
- Reference GNN pipeline (needs Crunchbase dump — **paid/risky**): https://github.com/sartaj04/Investor-Recommender

**Methods.** Classical CF / content-based (sklearn); embedding towers (sentence transformers → MLP); optional PyTorch bipartite GNN (GraphSAGE/GAT) on co-invest graph; ranking metrics (Recall@K, NDCG, MAP); temporal train/test by deal year.

**Why NOT generic.** Recommender framing + private-markets graph, not “classify default.” Commercial products exist, but open, auditable ranking with Form D evidence is rare in student work.

**Ambition.** A2 (A3 if GNN + Form D join).

**Feasibility (6 weeks).** High if scoped to open investor lists + reconstructed positive edges from public portfolios; Medium if insisting on full Crunchbase dump.

**Pedro / Mario fit.** Excellent dual fit: Pedro = VC world; Mario = recommenders + finance.

**Trade-offs.** Label noise (thesis text ≠ actual check); cold-start startups; graph sparsity; ethics of scraping emails (do **not** ship contact spam tooling — ranking only).

**Data-access risks.** Crunchbase dumps gated; Open Funding Data bulk export may be fair-use gated; Form D lacks clean “investor thesis” text.

---

### 2. Multi-source early-stage success / Series-A prediction (deal-flow scoring)
**RQ.** Using only information available *at launch / founding* (Product Hunt traction, founder pre-founding profile, sector), can we predict rare success (Series A ≤18m or mega-outcome) with calibrated probabilities that beat naive popularity baselines?

**Datasets + URLs**
- **PHBench** (67k Product Hunt launches → Series A labels): https://github.com/ihlamury/phbench · HF gated https://huggingface.co/datasets/ihlamury/phbench
- **VCBench** (9k anonymized founder–startup profiles; 4.5k public train): https://github.com/Vela-Engineering/VCBench-Starter-Kit · paper https://arxiv.org/abs/2509.14448
- Older Crunchbase-derived Kaggle dumps (1990–2013 era — use only as *negative example of generic*): avoid as sole data
- Optional enrichers: GitHub org activity (API), Similarweb-style web traffic (mostly paid)

**Methods.** Class imbalance (0.78% Series A in PHBench) → sklearn (logistic, RF, XGBoost/LightGBM) + calibration (Platt/isotonic); cost-sensitive / focal loss; PyTorch tabular MLP or multimodal (text embeddings of tagline + tabular); proper time-based splits; PR-AUC / lift@k / expected precision for a “sourcing budget.”

**Why NOT generic.** Not credit scoring; rare-event VC outcomes with **leakage-controlled** early features; new 2025 benchmarks (VCBench/PHBench) signal research maturity.

**Ambition.** A2–A3.

**Feasibility.** High on VCBench public CSV; Medium on PHBench (HF access request + severe imbalance).

**Pedro / Mario fit.** Pedro: peak interest. Mario: finance/risk OK; weaker recommender angle unless framed as “rank deal-flow queue.”

**Trade-offs.** Success definitions are extreme (>$500M) or rare (Series A); survivorship; anonymization limits interpretability; easy to accidentally leak post-founding info.

**Data-access risks.** PHBench test labels private (leaderboard); Crunchbase joins may violate ToS if re-scraped; HF gating delays week 1.

---

### 3. Polymarket prediction-market calibration & cross-market mispricing
**RQ.** Are Polymarket implied probabilities well-calibrated conditional on liquidity/OI, and can models using order-flow + external covariates improve resolution Brier/log-loss vs the raw market price (i.e., detect temporary mispricing without “predicting the election”)?

**Datasets + URLs**
- Polymarket Data API v2: https://docs.polymarket.com/api-reference/data-api/overview · price history https://docs.polymarket.com/api-reference/markets/get-prices-history
- Full-market HF archive (metadata + daily OHLC; watch leakage): https://huggingface.co/datasets/od2961/polymarket-full-market-dataset
- Research toolkit: https://github.com/sneddy/polymarket_research
- External covariates: BTC/ETH (Binance), rates/FX (FRED / yfinance)

**Methods.** Probability calibration curves; sklearn baselines on features (spread, volume, time-to-resolution, category); temporal models (PyTorch LSTM/TCN) on 5-min/ daily probability panels; market-making / mid-price drift as labels; strict pre-resolution feature cutoff.

**Why NOT generic.** Prediction markets ≠ stock forecasting; evaluation is scoring-rule based (Brier), not “directional accuracy on SPY.” Hot, timely, finance-native.

**Ambition.** A2 (A3 if microstructure + external signal fusion).

**Feasibility.** High — public APIs and ready HF dumps.

**Pedro / Mario fit.** Mario: markets 9/10. Pedro: innovative if framed as information aggregation / inefficiency, not “crypto gambling app.”

**Trade-offs.** Resolution label leakage; category heterogeneity (politics vs sports); regulatory/ethics narrative for oral defense; some markets illiquid → noisy probs.

**Data-access risks.** API grain limits (1-min only ~7 days); HF snapshot may include post-decision fields — must build temporal panels carefully.

---

### 4. Limit-order-book mid-price / volatility with DeepLOB-class models
**RQ.** On public LOB snapshots, does a convolutional/attention LOB model outperform logistic/GBDT on engineered imbalance features for short-horizon mid-price direction, and how fragile is that edge under walk-forward evaluation?

**Datasets + URLs**
- **FI-2010** (Nordic stocks, 10 days, 10 levels): https://service.tib.eu/ldmservice/en/dataset/fi-2010 · HF https://huggingface.co/datasets/shanehans/FI2010
- DeepLOB reference: https://github.com/zcakhaa/DeepLOB-Deep-Convolutional-Neural-Networks-for-Limit-Order-Books · paper https://arxiv.org/abs/1808.03668
- LOBSTER (NASDAQ academic waiver — **not free by default**): https://data.lobsterdata.com/ · samples only without waiver
- Crypto L2 dumps (ambitious alt path): https://huggingface.co/datasets/Goooddy/crypto-lob-stream · https://github.com/predict-quant/crypto-orderbook-dump

**Methods.** Feature baselines (OFI, microprice, book imbalance) + sklearn; PyTorch DeepLOB / Temporal Attention; event-time horizons; ablation on levels; compute cost reporting.

**Why NOT generic.** Microstructure ≠ predicting close-to-close stock returns; requires sequence DL and careful leakage control.

**Ambition.** A2–A3.

**Feasibility.** High on FI-2010 (but small/old universe); Medium–Low on LOBSTER (IE waiver timing may blow 6 weeks); Medium on crypto L2 (engineering heavy).

**Pedro / Mario fit.** Mario: strong markets. Pedro: OK if positioned as “not another Yahoo Finance LSTM”; less VC flavor.

**Trade-offs.** FI-2010 is a well-trodden benchmark → risk of “reproduction project”; tiny economic story; GPU helpful.

**Data-access risks.** LOBSTER institutional process; crypto dumps large (I/O/storage).

---

### 5. Earnings-call language → *surprise* / realized volatility (anti-generic NLP+markets)
**RQ.** Conditional on pre-call implied move / analyst estimate gap, does **dialogue structure** (Q&A hostility, CFO vs CEO language shift, hedging density) predict post-call absolute return or IV crush better than bag-of-words FinBERT sentiment alone?

**Datasets + URLs**
- Transcripts: https://huggingface.co/datasets/Bose345/sp500_earnings_transcripts (also `kurry/…`)
- Market-aligned episodes: https://huggingface.co/datasets/Amaanaush/earnings-call-data
- SEC 8-K / XBRL via EDGAR (in the augmented release)
- Prices: yfinance (ToS-aware)
- Example pipeline (avoid cloning wholesale): https://github.com/carolineb3/Earnings-Call-NLP-Pipeline

**Methods.** Speaker-turn features; FinBERT / Climate-agnostic finance embeddings; sklearn on engineered NLP + market controls; PyTorch hierarchical attention over turns; labels = |CAR|, IV change, not raw sign(return); SHAP for oral.

**Why NOT generic.** The *generic* trap is “sentiment → up/down.” The innovative RQ conditions on known information and targets **second-moment / surprise structure**.

**Ambition.** A2.

**Feasibility.** High — HF datasets already join text + returns.

**Pedro / Mario fit.** Mario: excellent. Pedro: only if RQ stays non-Kaggle; still public-markets, not VC.

**Trade-offs.** Crowded literature; easy to look generic in the oral if messaging slips; transcript license/ToS of upstream mirrors.

**Data-access risks.** yfinance instability; some HF mirrors may have murky redistribution rights — cite + don’t republish.

---

### 6. ESG “cheap talk” / greenwashing risk from corporate disclosures
**RQ.** Can we operationalize greenwashing risk as the gap between **commitment language** and **specificity / actionability**, and does that gap predict future controversy or emissions-path inconsistency better than raw ESG sentiment?

**Datasets + URLs**
- ClimateBERT suite: https://www.chatclimate.ai/climatebert
  - https://huggingface.co/datasets/climatebert/climate_detection
  - https://huggingface.co/datasets/climatebert/environmental_claims
  - https://huggingface.co/datasets/climatebert/climate_specificity
  - https://huggingface.co/datasets/climatebert/climate_commitments_actions
- Greenwashing-risk methodology paper: https://arxiv.org/pdf/2311.01469
- A3CG aspect–action dataset (ACL 2025): https://aclanthology.org/2025.acl-long.723.pdf
- Optional market link: returns / CDS — Yahoo/FRED (keep secondary)

**Methods.** Multi-head classifiers (sklearn on embeddings or fine-tune DistilRoBERTa in PyTorch); construct cheap-talk index; validate against external outcomes if available; error analysis by sector.

**Why NOT generic.** Not credit scoring; NLP + sustainable-finance risk narrative; supervisor-relevant.

**Ambition.** A2.

**Feasibility.** High for classification; Medium for linking to *market* outcomes (labels scarce).

**Pedro / Mario fit.** Mario: finance/risk OK. Pedro: innovative but **not VC**; may feel “climate NLP” more than deal-flow. Climate ≠ health veto, but keep away from clinical claims.

**Trade-offs.** Greenwashing ground truth is fuzzy; pure classification can feel narrow for BAM oral without an investor-use case.

**Data-access risks.** Low for HF ClimateBERT; A3CG report PDFs may need separate collection.

---

### 7. Systemic-risk networks: bank distress / rating with reconstructed interbank graphs
**RQ.** Do graph features / GNN message-passing on reconstructed interbank exposures improve next-quarter distress or relative rating prediction over tabular balance-sheet features alone?

**Datasets + URLs**
- AI4Risk interbank panel + code: https://github.com/AI4Risk/interbank · HFTCRNet https://github.com/AI4Risk/HFTCRNet
- FDIC Call Reports (public) for US reconstruction path: FDIC CDR portal (see ST-GAT paper https://arxiv.org/pdf/2604.14232)
- Classic DebtRank motivation: https://www.nature.com/articles/srep00541

**Methods.** Network metrics (DebtRank-style centrality) + sklearn; PyTorch Geometric GCN/GAT on quarterly snapshots; temporal validation across 2023 regional-bank stress.

**Why NOT generic.** Macro-finance networks, not stock picking; GNN + regulatory data story.

**Ambition.** A2–A3.

**Feasibility.** Medium — ready AI4Risk tables help; US ME reconstruction is a project by itself.

**Pedro / Mario fit.** Mario: risk/finance strong. Pedro: “not everyone does this,” but distant from VC/recommenders.

**Trade-offs.** Edges are **reconstructed**, not observed → scientific honesty required; learning curve for PyG; less “product demo.”

**Data-access risks.** Rating/SRISK provenance from Moody’s/vLab in AI4Risk — check license for redistribution; FDIC bulk download friction.

---

### 8. Crypto L2 microstructure (ambitious markets engineering)
**RQ.** Using reconstructed L2 books + trades + funding/OI, can short-horizon predictive signals for mid-price or volatility survive fees/latency assumptions better than trade-only baselines?

**Datasets + URLs**
- https://huggingface.co/datasets/Goooddy/crypto-lob-stream
- https://github.com/predict-quant/crypto-orderbook-dump → HF `predict-quant/binance-spot-orderbook`
- Trades/klines/funding lake: https://huggingface.co/datasets/KEDevO/crypto-market-datasets
- Binance public data: https://data.binance.vision/

**Methods.** Book reconstruction → features; sklearn baselines; PyTorch sequence models; realistic transaction-cost overlay; regime split (trend vs chop).

**Why NOT generic.** True microstructure; public crypto feeds are the rare free L2.

**Ambition.** A3 (engineering load).

**Feasibility.** Medium–Low in 6 weeks for two people unless ruthlessly scoped (1 symbol, 2 weeks of depth, clear baseline).

**Pedro / Mario fit.** Mario: markets yes. Pedro: innovative iff not “BTC price LSTM.”

**Trade-offs.** Storage/compute; easy to drown in data engineering; oral must emphasize research design not trading PnL cosplay.

**Data-access risks.** Dataset size; schema churn across exchanges; no institutional “ground truth.”

---

### 9. SEC Form D private-markets nowcasting (invented / open-data VC)
**RQ.** Can Amendment patterns, sold-vs-offered ratios, investor counts, and related-person networks in Form D predict subsequent financing intensity or time-to-next-raise better than industry–state baselines — i.e., a **public** private-markets signal without Crunchbase?

**Datasets + URLs**
- Official: https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets · schema https://www.sec.gov/files/Form_D.pdf
- HF: https://huggingface.co/datasets/XOOMAR/sec-form-d-offerings · https://huggingface.co/datasets/weio-ops/sec-form-d
- Optional labels: PHBench domains, YC batches, public press (noisy)

**Methods.** Panel/survival models (sklearn survival or discrete-time hazard); graph features on related persons recurring across filings; NLP light on issuer names/industries only; careful amendment de-duplication.

**Why NOT generic.** Almost no student projects use Form D as primary ML substrate; pure open regulatory data; VC-adjacent.

**Ambition.** A2 (A3 if network + survival done cleanly).

**Feasibility.** Medium — schema cleaning is non-trivial; outcome labels need creative but honest construction.

**Pedro / Mario fit.** Pedro: strong “not done by everyone.” Mario: private markets / fundraising risk; weak recommender unless combined with Idea 1.

**Trade-offs.** Form D is noisy, delayed, US-centric; “success” labels incomplete; amendments create leakage traps.

**Data-access risks.** Low (SEC public); high **label** risk (what is Y?).

---

### 10. Research-paper / method recommender as *quant research portfolio* signal
**RQ.** Can a citation/content recommender over finance–ML papers (OpenAlex / Papers with Code) surface works that *precede* adoption spikes in methods (e.g., sudden arXiv→GitHub star growth), framed as an information portfolio for a research desk — not movieLens clones?

**Datasets + URLs**
- OpenAlex API: https://developers.openalex.org/ · recipes https://developers.openalex.org/guides/recipes
- Linked Papers With Code: https://linkedpaperswithcode.com/ · paper https://ar5iv.labs.arxiv.org/html/2310.20475
- SPECTER2 embeddings (Semantic Scholar): https://allenai.org/blog/specter2-adapting-scientific-document-embeddings-to-multiple-fields-and-task-formats-c95686c06567
- Optional OSS twin: GFI issue rec datasets https://zenodo.org/records/6837711 · https://github.com/mcxwx123/RecGFI (weaker finance link)

**Methods.** Two-tower retrieval; citation-link prediction; sklearn on embedding distances; PyTorch contrastive fine-tune on finance subset; evaluate Recall@K against future citations / repo growth.

**Why NOT generic.** Recommender *plus* finance narrative (research alpha / method diffusion); Mario’s named interest; not stock prediction.

**Ambition.** A2.

**Feasibility.** High for recommender core; Medium for clean “portfolio signal” outcome metric.

**Pedro / Mario fit.** Mario: recommenders win. Pedro: only if story is sharp (method diffusion / VC diligence reading list); otherwise feels off-domain.

**Trade-offs.** Easy to become a pure IR project; “alpha” claim must stay metaphorical or carefully measured; API rate limits.

**Data-access risks.** OpenAlex API keys/rate limits; S2 embedding field availability; PW C dump size.

---

## Invented adjacents (shortlist, not fully fleshed)

| Sketch | One-line | Risk |
|--------|----------|------|
| **Syndicate link prediction** | Predict missing co-invest edges among VCs from partial public portfolios | Overlaps Idea 1 |
| **Prediction-market → equity spillover** | Does Polymarket shock on company-linked events forecast earnings CAR? | Entity linking hard |
| **OSS dependency risk for VC diligence** | GitHub star/issue/CVE dynamics as pre-Series-A risk features on PHBench | Feature engineering time |
| **Foot-traffic alt-data → retail** | Onspatial mobility https://github.com/onspatial/economic-sectors-mobility-data vs retail ETF | Pedro may call it “alt-data cosplay”; commercial card data closed |

---

## Comparative matrix

| # | Idea | Ambition | Feasibility | Pedro | Mario | Generic-risk |
|---|------|----------|-------------|-------|-------|--------------|
| 1 | Founder–investor matching | A2–A3 | High–Med | ★★★ | ★★★ | Low |
| 2 | VC success / PHBench–VCBench | A2–A3 | High–Med | ★★★ | ★★ | Low–Med |
| 3 | Polymarket calibration | A2–A3 | High | ★★ | ★★★ | Low |
| 4 | LOB / DeepLOB | A2–A3 | Med | ★★ | ★★★ | Med (FI-2010 crowded) |
| 5 | Earnings-call surprise | A2 | High | ★ | ★★★ | **High** if poorly framed |
| 6 | ESG greenwashing | A2 | High | ★★ | ★★ | Med |
| 7 | Systemic risk GNN | A2–A3 | Med | ★★ | ★★★ | Low |
| 8 | Crypto L2 | A3 | Med–Low | ★★ | ★★★ | Low–Med |
| 9 | Form D nowcasting | A2–A3 | Med | ★★★ | ★★ | Low |
| 10 | Paper rec as research portfolio | A2 | High | ★ | ★★★ | Med (IR-only trap) |

---

## Ranked top 3 (recommendation)

### 1) Founder ↔ investor matching recommender
**Why first.** Only idea that simultaneously maxes Mario’s named recommender interest and Pedro’s VC intrigue without health, without Kaggle credit, and without “predict AAPL tomorrow.” Open graphs + Form D give a defensible data story; sklearn baselines → PyTorch GNN is a clean ambition ladder for 6 weeks.

**6-week skeleton.** W1 data assembly & leakage rules · W2 content + CF baselines · W3 embeddings & ranking metrics · W4 optional GNN · W5 ablations/errors · W6 paper + oral demo (ranked shortlist UI optional).

### 2) Multi-source early-stage success (VCBench and/or PHBench)
**Why second.** Highest “real VC job” authenticity; brand-new benchmarks (2025) make the project feel current; extreme class imbalance forces serious ML craft (calibration, lift@k). Slightly weaker for Mario unless pitched as **deal-flow ranking**.

**Mitigation.** Add a ranking/evaluation framing (“top 1% of weekly launches”) so it feels recommender-adjacent.

### 3) Polymarket calibration & mispricing
**Why third.** Maximally non-generic markets ML; excellent public data; strong for Mario; Pedro-safe if the claim is information aggregation quality, not “we beat elections.” Natural sklearn vs deep sequence comparison.

**Keep LOB / Form D / earnings-call as backups** if top-3 data access stalls (PHBench gate, investor-graph thinness, etc.).

---

## What to veto in this cluster
- Standalone Kaggle “startup acquired vs closed” 2013 dumps without new features/RQ  
- Close-to-close equity LSTM on Yahoo OHLCV  
- Credit-default scoring clones  
- Anything health/clinical (partner veto)  
- Pure “FinBERT sentiment → stock up/down” without conditioning / second-moment RQ  

---

## Risks and open questions
- Exact course rubric beyond “real data + paper-like report + oral” still foggy (`docs/decisions/LEDGER.md`).  
- Crunchbase remains the VC gold standard but is the main **data-access landmine** — prefer Form D / Open Funding / VCBench / PHBench.  
- Recommender projects need offline metrics *and* a crisp business story for BAM oral.  
- Two-person ~30h group-work budget (syllabus) implies ruthless scoping: one primary RQ, one stretch ablation.

## Suggested next phases
1. Pedro + Mario pick among top 3 (or hybrid: Form D features inside Idea 1).  
2. Day-0 data dry-run (download + schema notebook) before committing.  
3. Write RQ + leakage protocol half-page; then implement.

## Sources (primary)
- VCBench: https://github.com/Vela-Engineering/VCBench-Starter-Kit · https://arxiv.org/abs/2509.14448  
- PHBench: https://github.com/ihlamury/phbench  
- Open Funding Data: https://openfundingdata.com/  
- Form D: https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets  
- Polymarket docs + HF archive: https://docs.polymarket.com/ · https://huggingface.co/datasets/od2961/polymarket-full-market-dataset  
- FI-2010 / DeepLOB: https://service.tib.eu/ldmservice/en/dataset/fi-2010 · https://arxiv.org/abs/1808.03668  
- ClimateBERT: https://www.chatclimate.ai/climatebert  
- AI4Risk interbank: https://github.com/AI4Risk/interbank  
- Crypto LOB: https://huggingface.co/datasets/Goooddy/crypto-lob-stream  
- Earnings transcripts: https://huggingface.co/datasets/Bose345/sp500_earnings_transcripts  
- OpenAlex: https://developers.openalex.org/  
- Local intake context: `research/briefs/research-brief-ml-project-intake.md`, `docs/decisions/LEDGER.md`

