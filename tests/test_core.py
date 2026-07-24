"""Unit tests for SHADE-IDS core logic.

Kept light (numpy + pandas only) so CI runs fast without the ML stack.
Run:  python -m pytest tests/   or   python -m tests.test_core
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.data import load
from src.signature import rules


def test_clean_normalizes_attack_cat():
    df = pd.DataFrame({"attack_cat": [" DoS ", "-", "nan", "Normal"], "x": [1, 2, 3, 4]})
    out = load.clean(df.copy(), drop_cols=[], attack_cat_col="attack_cat")
    assert list(out["attack_cat"]) == ["DoS", "Normal", "Normal", "Normal"]


def test_clean_fills_nan_and_drops_id():
    df = pd.DataFrame({"id": [1, 2], "attack_cat": ["Normal", "DoS"], "f": [np.nan, 5.0]})
    out = load.clean(df.copy(), drop_cols=["id"], attack_cat_col="attack_cat")
    assert "id" not in out.columns
    assert out["f"].iloc[0] == 0.0


def test_signature_detects_brute_force():
    flow = {"rate": 5000, "service": "ftp", "spkts": 10, "sbytes": 500,
            "dbytes": 0, "state": "CON"}
    assert rules.match(flow) == "BruteForce(rule)"


def test_signature_detects_port_scan():
    flow = {"rate": 5, "service": "-", "spkts": 1, "sbytes": 40,
            "dbytes": 0, "state": "INT"}
    assert rules.match(flow) == "PortScan(rule)"


def test_signature_passes_benign_flow():
    flow = {"rate": 10, "service": "http", "spkts": 20, "sbytes": 800,
            "dbytes": 1200, "state": "FIN"}
    assert rules.match(flow) is None


if __name__ == "__main__":
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS  {name}")
            passed += 1
    print(f"\n{passed} tests passed")
