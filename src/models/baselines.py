"""Week 2 - supervised detectors for SHADE-IDS.

RandomForest and XGBoost classifiers for binary attack/benign detection, plus a
shared evaluation helper. False-positive rate matters as much as recall for an IDS,
so we report the full classification report and ROC-AUC.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier


def train_random_forest(X, y, **kw) -> RandomForestClassifier:
    clf = RandomForestClassifier(**kw)
    clf.fit(X, y)
    return clf


def train_xgboost(X, y, **kw) -> XGBClassifier:
    clf = XGBClassifier(eval_metric="logloss", **kw)
    clf.fit(X, y)
    return clf


def evaluate(clf, X, y, name: str) -> dict:
    """Return accuracy / precision / recall / F1 / ROC-AUC + confusion matrix."""
    pred = clf.predict(X)
    proba = clf.predict_proba(X)[:, 1] if hasattr(clf, "predict_proba") else pred
    report = classification_report(y, pred, output_dict=True, zero_division=0)
    auc = roc_auc_score(y, proba) if len(np.unique(y)) > 1 else float("nan")
    cm = confusion_matrix(y, pred).tolist()
    print(f"\n=== {name} ===")
    print(classification_report(y, pred, zero_division=0))
    print(f"ROC-AUC: {auc:.4f}")
    return {"name": name, "report": report, "roc_auc": auc, "confusion_matrix": cm}
