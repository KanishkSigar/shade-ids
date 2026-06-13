# SHADE-IDS — 6-Week Build Plan

The repository grows one milestone per week; each week is tagged (`week-1` … `week-6`)
as that week's submission. Focus is the **application** (a working, explainable IDS),
not a research paper.

| Week | Milestone | Key deliverables |
|---|---|---|
| **1** | **Foundation** | repo scaffold, 6-week plan, data ingestion (load + clean UNSW-NB15), feature pipeline, quick EDA |
| **2** | **Supervised detection** | RandomForest / XGBoost training, train/test split, metrics report (precision/recall/F1, ROC-AUC) |
| **3** | **Hybrid engine** | benign-only autoencoder (anomaly / zero-day) + fast signature rules; combined scoring |
| **4** | **Explainability** | SHAP global + per-alert attributions wired into detections |
| **5** | **Application** | Streamlit dashboard: inspect flows, run detection, view SHAP, browse results |
| **6** | **Ship it** | unit tests + CI, packaging (requirements/Docker), deploy to Streamlit Cloud, final docs + demo |

## Dataset
**UNSW-NB15** (binary `label` + multi-class `attack_cat`). Training/testing CSVs go in
`data/`. Public mirror used in development:
`https://github.com/Nir-J/ML-Projects` (UNSW-Network_Packet_Classification).

## Conventions
- Small, frequent commits; one logical change each.
- Each week ends with a `git tag week-N` snapshot = the submission for that week.
