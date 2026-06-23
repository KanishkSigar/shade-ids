# SHADE-IDS - Explainable Hybrid Intrusion Detection System

A network intrusion detection **application** that combines a fast signature layer,
supervised detectors, and a benign-only anomaly detector, with **SHAP** explanations
for every alert - wrapped in an interactive dashboard.

> Built as a **6-week internship project**. The repository grows one milestone per
> week; see [`docs/WEEK_PLAN.md`](docs/WEEK_PLAN.md). **Current: Week 3 - Hybrid engine.**

## What it will do (by Week 6)
- Ingest network-flow data and engineer features.
- Detect known attacks (signature rules) and learn supervised + anomaly detectors.
- Explain each alert with SHAP so an analyst can see *why* a flow was flagged.
- Serve it all through a Streamlit dashboard, tested and deployed.

## Progress
- **Week 1 - Foundation:** project scaffold, data ingestion (load + clean UNSW-NB15),
  feature pipeline, quick EDA.
- **Week 2 - Supervised detection:** RandomForest + XGBoost binary attack/benign
  detectors with a metrics report. Both reach ~95% accuracy and ROC-AUC 0.99 on the
  held-out test set - see [`docs/week2_metrics.md`](docs/week2_metrics.md).
- **Week 3 - Hybrid engine:** a signature-rule layer plus a benign-only autoencoder
  that flags anomalies by reconstruction error (no attack labels needed) - see
  [`docs/week3_hybrid.md`](docs/week3_hybrid.md).

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# place UNSW-NB15 CSVs under data/ (see docs/WEEK_PLAN.md), then:
python -m src.eda      # Week 1: explore the data
python -m src.train    # Week 2: train + evaluate supervised detectors
python -m src.hybrid   # Week 3: signature + autoencoder hybrid engine
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
  eda.py               # Week 1: class-balance / feature summary
  train.py             # Week 2: train + evaluate supervised detectors
  hybrid.py            # Week 3: signature + autoencoder hybrid engine
docs/WEEK_PLAN.md      # 6-week milestone plan
data/                  # datasets (gitignored)
```
