"""Week 1 — quick exploratory data analysis for SHADE-IDS.

Loads + cleans UNSW-NB15, prints class balance, and saves an attack-category
distribution chart. Run:  python -m src.eda
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.data import load

TRAIN = "data/UNSW_NB15_training-set.csv"
TEST = "data/UNSW_NB15_testing-set.csv"
OUT = "results"


def main() -> None:
    df = load.load_raw(TRAIN, TEST if os.path.exists(TEST) else None)
    df = load.clean(df)

    print(f"rows={len(df):,}  cols={df.shape[1]}")
    print("\nlabel balance:\n", df["label"].value_counts())
    print("\nattack categories:\n", df["attack_cat"].value_counts())

    os.makedirs(OUT, exist_ok=True)
    counts = df["attack_cat"].value_counts().sort_values()
    ax = counts.plot.barh(color="#4c72b0")
    ax.set_title("UNSW-NB15 — attack category distribution")
    ax.set_xlabel("number of flows")
    plt.tight_layout()
    path = os.path.join(OUT, "attack_cat_distribution.png")
    plt.savefig(path, dpi=150)
    print(f"\nsaved -> {path}")


if __name__ == "__main__":
    main()
