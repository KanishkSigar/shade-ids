"""Week 4 - generate SHAP explanations for the detector.

Trains the XGBoost detector, then produces:
  * a global SHAP summary (what drives detections overall)
  * a per-alert explanation for one flow the model flagged as an attack

Run:  python -m src.explain_run
"""
from __future__ import annotations

import json
import os

import numpy as np
import yaml
from sklearn.model_selection import train_test_split

from src.data import load
from src.explain import shap_explain
from src.features import pipeline
from src.models import baselines


def main(cfg_path: str = "config.yaml") -> None:
    cfg = yaml.safe_load(open(cfg_path))
    d, sp = cfg["data"], cfg["split"]
    label_col, cat_col = d["label_col"], d["attack_cat_col"]

    df = load.load_raw(d["train_csv"], d.get("test_csv"))
    df = load.clean(df, d["drop_cols"], cat_col)
    y = df[label_col].to_numpy()
    train_df, test_df = train_test_split(
        df, test_size=sp["test_size"], random_state=sp["random_state"], stratify=y
    )

    exclude = [label_col, cat_col, "split"]
    ct = pipeline.build_transformer(train_df, exclude, sp["scaler"])
    X_train = pipeline.transform(ct, train_df, exclude, fit=True)
    X_test = pipeline.transform(ct, test_df, exclude, fit=False)
    names = pipeline.feature_names(ct)
    y_train = train_df[label_col].to_numpy()
    y_test = test_df[label_col].to_numpy()

    clf = baselines.train_xgboost(X_train, y_train, **cfg["models"]["xgboost"])

    out = cfg["output"]["results_dir"]
    os.makedirs(out, exist_ok=True)
    n = min(cfg["explain"]["shap_sample"], len(X_test))

    # Global: what drives detections overall.
    vals = shap_explain.global_summary(
        clf, X_test[:n], names, os.path.join(out, "shap_global.png")
    )
    mean_abs = np.abs(vals).mean(axis=0)
    top = np.argsort(mean_abs)[::-1][:10]
    top_features = {names[i]: round(float(mean_abs[i]), 4) for i in top}
    print("\nTop features driving detections (mean |SHAP|):")
    for k, v in top_features.items():
        print(f"  {k:30s} {v}")

    # Local: explain one flow the model flagged as an attack.
    pred = clf.predict(X_test)
    flagged = np.where((pred == 1) & (y_test == 1))[0]
    contrib = {}
    if len(flagged):
        i = int(flagged[0])
        contrib = shap_explain.explain_one(
            clf, X_test[i], names, os.path.join(out, "shap_one_alert.png")
        )
        print(f"\nPer-alert explanation for test flow #{i} "
              f"(true attack category: {test_df.iloc[i][cat_col]})")
        for k, v in contrib.items():
            print(f"  {k:30s} {v:+.4f}")

    with open(os.path.join(out, "explain_summary.json"), "w") as f:
        json.dump({"top_global_features": top_features, "example_alert": contrib}, f, indent=2)
    print(f"\nsaved -> {out}/shap_global.png, {out}/shap_one_alert.png, {out}/explain_summary.json")


if __name__ == "__main__":
    main()
