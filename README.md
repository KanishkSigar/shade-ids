# SHADE-IDS - Explainable Hybrid Intrusion Detection System

A network intrusion detection **application** that combines a fast signature layer,
supervised detectors, and a benign-only anomaly detector, with **SHAP** explanations
for every alert - wrapped in an interactive dashboard.

> Built as a **6-week internship project**. The repository grows one milestone per
> week; see [`docs/WEEK_PLAN.md`](docs/WEEK_PLAN.md). **Current: Week 1 - Foundation.**

## What it will do (by Week 6)
- Ingest network-flow data and engineer features.
- Detect known attacks (signature rules) and learn supervised + anomaly detectors.
- Explain each alert with SHAP so an analyst can see *why* a flow was flagged.
- Serve it all through a Streamlit dashboard, tested and deployed.

## Week 1 - Foundation (this submission)
- Project scaffold and 6-week plan.
- Data ingestion: load + clean the UNSW-NB15 flow dataset.
- Feature pipeline (scaling + encoding) and a quick exploratory summary.

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# place UNSW-NB15 CSVs under data/ (see docs/WEEK_PLAN.md), then:
python -m src.eda
```

## Layout (Week 1)
```
src/
  data/load.py        # load + clean the dataset
  features/pipeline.py# scaling + encoding
  eda.py              # quick class-balance / feature summary
docs/WEEK_PLAN.md     # 6-week milestone plan
data/                 # datasets (gitignored)
```
