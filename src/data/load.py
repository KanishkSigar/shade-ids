"""Week 1 — data ingestion for SHADE-IDS.

Loads the UNSW-NB15 flow CSVs and applies light cleaning. The dataset has a binary
`label` column (0 = benign, 1 = attack) and a multi-class `attack_cat` column.
"""
from __future__ import annotations

import pandas as pd

DEFAULT_DROP = ["id"]
LABEL_COL = "label"
ATTACK_CAT_COL = "attack_cat"


def load_raw(train_csv: str, test_csv: str | None = None) -> pd.DataFrame:
    """Load train (and optional test) CSVs into one DataFrame with a `split` flag."""
    train = pd.read_csv(train_csv)
    train["split"] = "train"
    if test_csv:
        test = pd.read_csv(test_csv)
        test["split"] = "test"
        return pd.concat([train, test], ignore_index=True)
    return train


def clean(df: pd.DataFrame, drop_cols: list[str] | None = None,
          attack_cat_col: str = ATTACK_CAT_COL) -> pd.DataFrame:
    """Drop id-like columns, normalize the attack-category text, fill numeric NaNs."""
    drop_cols = DEFAULT_DROP if drop_cols is None else drop_cols
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")
    if attack_cat_col in df.columns:
        df[attack_cat_col] = (
            df[attack_cat_col].astype(str).str.strip()
            .replace({"-": "Normal", "nan": "Normal"})
        )
    num_cols = df.select_dtypes("number").columns
    df[num_cols] = df[num_cols].fillna(0)
    return df
