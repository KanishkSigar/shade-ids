# SHADE-IDS - 4-Week Build Plan

The repository grows one milestone per week. Focus is the **application** (a working,
explainable IDS), delivered alongside a **research paper** (`paper/`).

| Week | Milestone | Key deliverables |
|---|---|---|
| **1** | **Foundation** | repo scaffold, data ingestion (load + clean UNSW-NB15), feature pipeline, quick EDA |
| **2** | **Supervised detection** | RandomForest / XGBoost, train/test split, metrics report (precision/recall/F1, ROC-AUC) |
| **3** | **Hybrid engine + explainability** | benign-only autoencoder + signature rules; SHAP global + per-alert explanations |
| **4** | **Application + delivery + paper** | Streamlit dashboard, unit tests + CI, deployment guide, and the research paper |

## Git tags
The repo history is tagged as it grew. The tags map onto the four weeks as:
`week-1` = foundation; `week-2` = supervised; `week-3` + `week-4` = hybrid engine +
SHAP; `week-5` + `week-6` = application, tests/CI and deployment.

## Research paper
The IEEE-format paper is in [`paper/`](../paper/) (source `main.tex`, compiled
`main.pdf`, editable draw.io figures in `paper/fig/`). It studies when supervised NIDS
generalize to unseen attack families across UNSW-NB15 and CIC-IDS2017, with SHAP and
feature ablation. Results summary: [`docs/research_results.md`](research_results.md).

## Dataset
**UNSW-NB15** (binary `label` + multi-class `attack_cat`). Training/testing CSVs go in
`data/`. Public mirror used in development:
`https://github.com/Nir-J/ML-Projects` (UNSW-Network_Packet_Classification).

## Conventions
- Small, frequent commits; one logical change each.
- Each milestone ends with a `git tag` snapshot.
