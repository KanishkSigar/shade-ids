# SHADE-IDS - Explainable Hybrid Intrusion Detection System

A network intrusion detection **application** that combines a fast signature layer,
supervised detectors, and a benign-only anomaly detector, with **SHAP** explanations
for every alert - wrapped in an interactive dashboard.

> Built as a **4-week internship project** (see [`docs/WEEK_PLAN.md`](docs/WEEK_PLAN.md)):
> Week 1 foundation, Week 2 supervised detection, Week 3 hybrid engine + SHAP, Week 4
> application + delivery + research paper. **Status: complete.** This single repo holds
> both the **application** and the **research paper** ([`paper/`](paper/)).

## Current capabilities
- Ingest network-flow data and engineer features.
- Detect known attacks (signature rules) and learn supervised + anomaly detectors.
- Explain each alert with SHAP so an analyst can see *why* a flow was flagged.
- Browse committed evaluation figures and replay a recorded flow CSV in the Streamlit dashboard.
- Replay columns are `spkts,sbytes,dbytes,rate,service,state`. An optional binary `label` column enables error counts for the signature layer.

## Progress
- **Week 1 - Foundation:** project scaffold, data ingestion (load + clean UNSW-NB15),
  feature pipeline, quick EDA.
- **Week 2 - Supervised detection:** RandomForest + XGBoost binary attack/benign
  detectors with a metrics report. Both reach ~95% accuracy and ROC-AUC 0.99 on the
  held-out test set - see [`docs/week2_metrics.md`](docs/week2_metrics.md).
- **Week 3 - Hybrid engine:** a signature-rule layer plus a benign-only autoencoder
  that flags anomalies by reconstruction error (no attack labels needed) - see
  [`docs/week3_hybrid.md`](docs/week3_hybrid.md).
- **Week 4 - Explainability:** SHAP explanations for every detection, both global
  (what drives detections overall) and per-alert (why *this* flow was flagged) - see
  [`docs/week4_explainability.md`](docs/week4_explainability.md).
- **Application:** a Streamlit dashboard (`app.py`) that brings the detection
  results, explanations, and a live signature check together in one interface.
- **Quality and delivery:** unit tests with GitHub Actions CI, plus a deployment
  guide in [`DEPLOY.md`](DEPLOY.md).

## Research paper
The IEEE-format paper is in [`paper/`](paper/) - source `main.tex`, compiled
`main.pdf`, and editable draw.io figures in `paper/fig/`. It studies when supervised
NIDS generalize to unseen attack families across UNSW-NB15 and CIC-IDS2017, using SHAP
and feature ablation, and compares against prior work. Results summary:
[`docs/research_results.md`](docs/research_results.md).

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# place UNSW-NB15 CSVs under data/ (see docs/WEEK_PLAN.md), then:
python -m src.eda      # Week 1: explore the data
python -m src.train    # Week 2: train + evaluate supervised detectors
python -m src.hybrid   # Week 3: signature + autoencoder hybrid engine
python -m src.explain_run  # Week 4: SHAP global + per-alert explanations
streamlit run app.py       # launch the dashboard (see DEPLOY.md)
```

## Layout
```
config.yaml            # paths, split, model params
src/
  data/load.py         # load + clean the dataset
  features/pipeline.py # scaling + encoding
  models/baselines.py  # RandomForest / XGBoost + evaluation
  models/autoencoder.py# benign-only autoencoder (anomaly detection)
  signature/rules.py   # fast known-attack rules
  explain/shap_explain.py # SHAP global + per-alert explanations
  eda.py               # Week 1: class-balance / feature summary
  train.py             # Week 2: train + evaluate supervised detectors
  hybrid.py            # Week 3: signature + autoencoder hybrid engine
  explain_run.py       # Week 4: generate SHAP explanations
docs/WEEK_PLAN.md      # 6-week milestone plan
data/                  # datasets (gitignored)
```
