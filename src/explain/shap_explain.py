"""Week 4 - SHAP explanations for SHADE-IDS.

Turns a detection into something an analyst can read:
  * global  - which flow features matter most across all traffic.
  * local   - for one flagged flow, which features pushed it toward "attack".

TreeSHAP is exact and fast for tree models, so we explain the XGBoost detector.
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import shap


def positive_class(values):
    """Reduce TreeSHAP output to 2D (samples, features) for the attack class.

    SHAP returns different shapes across versions for a binary classifier:
      list [class0, class1]           -> take class1
      3D array (samples, features, 2) -> take [..., 1]
      2D array                        -> already per-output (e.g. XGBoost margin)
    """
    if isinstance(values, list):
        return values[1]
    if getattr(values, "ndim", 2) == 3:
        return values[:, :, 1]
    return values


def global_summary(model, X, feature_names: list[str], out_path: str, max_display: int = 15):
    """Beeswarm summary: the features driving detections overall."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    vals = positive_class(shap.TreeExplainer(model).shap_values(X))
    shap.summary_plot(vals, X, feature_names=feature_names, show=False, max_display=max_display)
    plt.title("SHAP - features driving attack detections")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return vals


def explain_one(model, X_row, feature_names: list[str], out_path: str, top_k: int = 10):
    """Per-alert explanation: top features pushing one flow toward attack/benign."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    row = np.asarray(X_row).reshape(1, -1)
    vals = positive_class(shap.TreeExplainer(model).shap_values(row))[0]
    idx = np.argsort(np.abs(vals))[::-1][:top_k][::-1]
    colors = ["#c44e52" if vals[i] > 0 else "#4c72b0" for i in idx]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh([feature_names[i] for i in idx], [vals[i] for i in idx], color=colors)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("SHAP value (right = pushes toward attack)")
    ax.set_title("Why this flow was flagged")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return {feature_names[i]: float(vals[i]) for i in idx[::-1]}
