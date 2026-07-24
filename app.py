"""SHADE-IDS dashboard (Week 5).

The application front end: browse detection results, inspect explanations, and try
the signature layer live. Reads the committed artifacts in docs/ so it starts fast
and works anywhere without retraining.

Run:  streamlit run app.py     (opens at http://localhost:8501)
"""
from __future__ import annotations

import os

import streamlit as st

from src.signature import rules

DOCS = "docs"

st.set_page_config(page_title="SHADE-IDS", page_icon="🛡️", layout="wide")
st.title("🛡️ SHADE-IDS")
st.caption("Explainable hybrid intrusion detection - signature rules, supervised "
           "models, and a benign-only autoencoder, with SHAP explanations.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Detection results", "Explainability", "Live signature check"]
)


def show(path: str, caption: str | None = None):
    """Display a committed figure if present."""
    if os.path.exists(path):
        st.image(path, caption=caption)
    else:
        st.info(f"Figure not generated yet: `{path}`")


with tab1:
    st.header("How it works")
    st.markdown(
        "1. **Signature rules** catch obvious known-bad flows instantly.\n"
        "2. **Supervised models** (RandomForest / XGBoost) detect known attack types.\n"
        "3. **A benign-only autoencoder** flags unusual traffic without needing "
        "attack labels.\n"
        "4. **SHAP** explains every alert so an analyst can see *why* a flow was flagged."
    )
    st.subheader("Dataset")
    st.markdown(
        "UNSW-NB15: 257,673 network flows, 93,000 benign, across 9 attack families."
    )
    show(os.path.join(DOCS, "week1_attack_distribution.png"),
         "Attack category distribution")

with tab2:
    st.header("Detection results")
    st.subheader("Supervised detectors (Week 2)")
    st.markdown(
        "| Model | Accuracy | Recall (attack) | ROC-AUC |\n"
        "|---|---|---|---|\n"
        "| RandomForest | 0.95 | 0.96 | 0.9925 |\n"
        "| XGBoost | 0.95 | 0.96 | 0.9925 |"
    )
    show(os.path.join(DOCS, "week2_roc.png"), "ROC comparison")

    st.subheader("Anomaly detection (Week 3)")
    st.markdown(
        "The benign-only autoencoder catches **35%** of attacks at just a **0.8%** "
        "false-alarm rate, without ever seeing an attack label."
    )
    show(os.path.join(DOCS, "week3_recon_error.png"),
         "Reconstruction error: benign vs attack")

with tab3:
    st.header("Explainability (SHAP)")
    st.markdown(
        "`sttl` (source TTL) dominates the model's decisions, followed by connection-"
        "count features. Below: what drives detections overall, and why one specific "
        "flow was flagged."
    )
    c1, c2 = st.columns(2)
    with c1:
        show(os.path.join(DOCS, "week4_shap_global.png"), "Global feature importance")
    with c2:
        show(os.path.join(DOCS, "week4_shap_one_alert.png"), "Why this flow was flagged")

with tab4:
    st.header("Live signature check")
    st.markdown("Adjust a flow's properties - matching rules fire instantly.")
    c1, c2, c3 = st.columns(3)
    spkts = c1.number_input("spkts (source packets)", 0, 100000, 1)
    sbytes = c1.number_input("sbytes (source bytes)", 0, 50_000_000, 40)
    dbytes = c2.number_input("dbytes (destination bytes)", 0, 50_000_000, 0)
    rate = c2.number_input("rate", 0.0, 1_000_000.0, 1500.0)
    service = c3.selectbox("service", ["-", "http", "dns", "ftp", "ssh", "smtp"])
    state = c3.selectbox("state", ["FIN", "CON", "INT", "REQ"])

    flow = {"spkts": spkts, "sbytes": sbytes, "dbytes": dbytes,
            "rate": rate, "service": service, "state": state}
    hit = rules.match(flow)
    if hit:
        st.error(f"⚠️ Signature match: **{hit}**")
    else:
        st.success("No signature matched - this flow would be passed to the ML layer.")
