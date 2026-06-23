# Week 3 - Hybrid Engine Results

Two label-free detection layers, evaluated on the UNSW-NB15 test set.

## Signature layer
Simple deterministic rules (port scan, brute force, data exfiltration) flagged
**1,869 flows**. These rules are fast and fully interpretable but coarse, so they act
as a first-pass filter rather than a precise detector.

## Benign-only autoencoder (anomaly detection)
Trained only on benign traffic, then flags flows whose reconstruction error exceeds
`mean + 3*std` of benign errors:

| Metric | Value |
|---|---|
| Threshold | 0.0243 |
| Attack recall (caught) | 0.35 |
| Benign false-positive rate | 0.008 |

At a very low false-alarm rate (0.8%), the autoencoder catches about a third of
attacks **without using any attack labels** - a useful complement to the supervised
models from Week 2. The reconstruction-error distribution (benign vs attack) is in
`week3_recon_error.png`. Reproduce with `python -m src.hybrid`.
