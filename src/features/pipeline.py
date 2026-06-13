"""Week 1 — feature preparation for SHADE-IDS.

Scales numeric flow features and one-hot encodes categoricals (proto/service/state),
returning a single fitted transformer so train/test/live data share preprocessing.
"""
from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler


def build_transformer(df: pd.DataFrame, exclude: list[str], scaler: str = "standard") -> ColumnTransformer:
    """Build (unfitted) a transformer: scale numeric cols, one-hot categorical cols."""
    feats = df.drop(columns=[c for c in exclude if c in df.columns], errors="ignore")
    num_cols = feats.select_dtypes("number").columns.tolist()
    cat_cols = feats.select_dtypes(exclude="number").columns.tolist()
    scaler_obj = StandardScaler() if scaler == "standard" else MinMaxScaler()
    return ColumnTransformer([
        ("num", scaler_obj, num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ])


def feature_names(ct: ColumnTransformer) -> list[str]:
    """Recover output feature names after fitting."""
    return ct.get_feature_names_out().tolist()


def transform(ct: ColumnTransformer, df: pd.DataFrame, exclude: list[str], fit: bool):
    """Fit-or-apply the transformer, dropping excluded (label) columns first."""
    feats = df.drop(columns=[c for c in exclude if c in df.columns], errors="ignore")
    return ct.fit_transform(feats) if fit else ct.transform(feats)
