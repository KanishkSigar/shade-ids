"""Week 3 - hybrid detection engine.

Runs the two label-free layers together:
  1. Signature rules catch obvious known-bad flows instantly.
  2. A benign-only autoencoder flags anomalies (incl. unseen attacks) by high
     reconstruction error.

Reports how well each layer detects attacks on the held-out test set and saves a
reconstruction-error distribution figure.  Run:  python -m src.hybrid
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from sklearn.model_selection import train_test_split

from src.data import load
from src.features import pipeline
from src.models import autoencoder as ae
from src.signature import rules


def main(cfg_path: str = "config.yaml") -> None:
    cfg = yaml.safe_load(open(cfg_path))
    d, sp, aecfg = cfg["data"], cfg["split"], cfg["autoencoder"]
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
    y_train = train_df[label_col].to_numpy()
    y_test = test_df[label_col].to_numpy()

    out = cfg["output"]["results_dir"]
    os.makedirs(out, exist_ok=True)
    results = {}

    # --- Signature layer ---
    sig_hits = test_df.apply(lambda r: rules.match(r.to_dict()) is not None, axis=1).to_numpy()
    if sig_hits.any():
        precision = float(y_test[sig_hits].mean())  # fraction of flagged that are attacks
    else:
        precision = float("nan")
    results["signature"] = {"flows_flagged": int(sig_hits.sum()),
                            "precision": precision}
    print(f"[signature] flagged {sig_hits.sum()} flows; precision={precision:.3f}")

    # --- Autoencoder (benign-only) ---
    model = ae.train_autoencoder(
        X_train[y_train == 0], aecfg["hidden_dims"], aecfg["epochs"],
        aecfg["batch_size"], aecfg["lr"], aecfg["device"],
    )
    benign_train_err = ae.reconstruction_error(model, X_train[y_train == 0])
    thr = ae.choose_threshold(benign_train_err, aecfg["threshold_k"])
    err_test = ae.reconstruction_error(model, X_test)
    flagged = err_test > thr
    recall = float(flagged[y_test == 1].mean())       # attacks caught
    fpr = float(flagged[y_test == 0].mean())          # benign wrongly flagged
    results["autoencoder"] = {"threshold": thr, "attack_recall": recall, "benign_fpr": fpr}
    print(f"[autoencoder] threshold={thr:.5f}  attack recall={recall:.3f}  benign FPR={fpr:.3f}")

    with open(os.path.join(out, "hybrid_metrics.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nsaved metrics -> {out}/hybrid_metrics.json")

    # --- Reconstruction-error distribution figure ---
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(np.clip(err_test[y_test == 0], 0, np.quantile(err_test, 0.99)), bins=60,
            alpha=0.6, label="benign", color="#4c72b0", density=True)
    ax.hist(np.clip(err_test[y_test == 1], 0, np.quantile(err_test, 0.99)), bins=60,
            alpha=0.6, label="attack", color="#c44e52", density=True)
    ax.axvline(thr, color="k", ls="--", label="threshold")
    ax.set_title("Autoencoder reconstruction error: benign vs attack")
    ax.set_xlabel("reconstruction error"); ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out, "recon_error_dist.png"), dpi=150)
    print(f"saved figure -> {out}/recon_error_dist.png")


if __name__ == "__main__":
    main()
