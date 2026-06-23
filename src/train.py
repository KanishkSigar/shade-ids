"""Week 2 - train + evaluate supervised detectors.

Run:  python -m src.train

Loads UNSW-NB15, builds features, makes a stratified train/test split, trains
RandomForest and XGBoost, evaluates on the held-out test set, and saves a metrics
report plus ROC and confusion-matrix figures.
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from sklearn.metrics import RocCurveDisplay
from sklearn.model_selection import train_test_split

from src.data import load
from src.features import pipeline
from src.models import baselines


def main(cfg_path: str = "config.yaml") -> None:
    cfg = yaml.safe_load(open(cfg_path))
    d, sp = cfg["data"], cfg["split"]
    label_col, cat_col = d["label_col"], d["attack_cat_col"]

    df = load.load_raw(d["train_csv"], d.get("test_csv"))
    df = load.clean(df, d["drop_cols"], cat_col)
    print(f"rows={len(df):,}  cols={df.shape[1]}")

    y = df[label_col].to_numpy()
    train_df, test_df = train_test_split(
        df, test_size=sp["test_size"], random_state=sp["random_state"], stratify=y
    )

    exclude = [label_col, cat_col, "split"]
    ct = pipeline.build_transformer(train_df, exclude, sp["scaler"])
    X_train = pipeline.transform(ct, train_df, exclude, fit=True)
    X_test = pipeline.transform(ct, test_df, exclude, fit=False)
    y_train = train_df[label_col].to_numpy()
    y_test = test_df[label_col].to_numpy()

    out = cfg["output"]["results_dir"]
    os.makedirs(out, exist_ok=True)
    results = {}

    rf = baselines.train_random_forest(X_train, y_train, **cfg["models"]["random_forest"])
    results["random_forest"] = baselines.evaluate(rf, X_test, y_test, "RandomForest")

    xgb = baselines.train_xgboost(X_train, y_train, **cfg["models"]["xgboost"])
    results["xgboost"] = baselines.evaluate(xgb, X_test, y_test, "XGBoost")

    with open(os.path.join(out, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nsaved metrics -> {out}/metrics.json")

    # ROC comparison figure.
    fig, ax = plt.subplots(figsize=(5, 4.5))
    for name, clf in [("RandomForest", rf), ("XGBoost", xgb)]:
        RocCurveDisplay.from_estimator(clf, X_test, y_test, ax=ax, name=name)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.3)
    ax.set_title("UNSW-NB15 - supervised detection ROC")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "roc_supervised.png"), dpi=150)
    print(f"saved ROC figure -> {out}/roc_supervised.png")


if __name__ == "__main__":
    main()
