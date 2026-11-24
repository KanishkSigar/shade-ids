"""SHADE-IDS dashboard.

The application front end: browse detection results, inspect explanations, and try
the signature layer live. Reads the committed artifacts in docs/ so it starts fast
and works anywhere without retraining.

Run:  streamlit run app.py     (opens at http://localhost:8501)
"""
from __future__ import annotations

import os

import pandas as pd

import streamlit as st

from src.signature import rules

DOCS = "docs"

st.set_page_config(page_title="SHADE-IDS", page_icon="🛡️", layout="wide")
st.title("🛡️ SHADE-IDS")
st.caption("Explainable hybrid intrusion detection - signature rules, supervised "
           "models, and a benign-only autoencoder, with SHAP explanations.")

tab1, tab2, tab3, tab4, replay = st.tabs(
    ["Overview", "Detection results", "Explainability", "Live signature check", "CSV replay"]
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

with replay:
    st.header("Replay recorded flows")
    st.caption(
        "Upload previously recorded flow summaries. This replay runs the signature layer "
        "on each row and reports the matching rule. Labels, when present, are used only "
        "to count false alerts and missed detections."
    )
    uploaded = st.file_uploader("Flow CSV (up to 10,000 rows)", type="csv")
    if uploaded is not None:
        numeric_fields = ["spkts", "sbytes", "dbytes", "rate"]
        required_fields = numeric_fields + ["service", "state"]
        try:
            rows = pd.read_csv(uploaded, nrows=10_001)
            missing = [field for field in required_fields if field not in rows]
            if missing:
                raise ValueError("Missing columns: " + ", ".join(missing))
            if rows.empty or len(rows) > 10_000:
                raise ValueError("Provide between 1 and 10,000 rows.")
            for field in numeric_fields:
                rows[field] = pd.to_numeric(rows[field], errors="raise")
                if rows[field].isna().any() or not rows[field].between(0, 1e15).all():
                    raise ValueError(f"{field} must contain finite, nonnegative numbers.")
            if rows[["service", "state"]].isna().any().any():
                raise ValueError("Every row needs a service and state.")
        except (ValueError, UnicodeError, pd.errors.ParserError) as exc:
            st.error(str(exc))
        else:
            results = rows[required_fields].copy()
            results.insert(0, "row", results.index + 1)
            results["matching_rule"] = [
                rules.match(flow) or "" for flow in rows[required_fields].to_dict("records")
            ]
            alerted = results["matching_rule"].ne("")
            st.metric("Signature alerts", f"{alerted.sum():,} / {len(results):,}")
            if "label" in rows:
                labels = pd.to_numeric(rows["label"], errors="coerce")
                if labels.isin([0, 1]).all():
                    results["label"] = labels.astype(int)
                    col1, col2 = st.columns(2)
                    col1.metric("False alerts", int((alerted & labels.eq(0)).sum()))
                    col2.metric("Missed detections", int((~alerted & labels.eq(1)).sum()))
                else:
                    st.info("Use 0 (benign) or 1 (attack) in every label row to see error counts.")
            if st.checkbox("Show matching flows only", value=True):
                results = results[alerted]
            st.dataframe(results, hide_index=True)
            exported = results.copy()
            for field in ["service", "state"]:
                exported[field] = exported[field].astype(str).str.replace(
                    r"^([\s]*[=+@-])", r"'\1", regex=True
                )
            st.download_button(
                "Export displayed rows as CSV",
                exported.to_csv(index=False),
                file_name="shade-signature-replay.csv",
                mime="text/csv",
            )
