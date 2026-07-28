# SHADE — Results Summary

Sections 1–3 use UNSW-NB15 (257,673 flows; 93,000 benign; 9 attack families);
Section 4 cross-validates on CIC-IDS2017. Reproduce §1 with
`python -m src.experiment_loo --config config.yaml`.

## 1. Leave-one-family-out zero-day detection

Each family is held out entirely; supervised models train on the rest, the
autoencoder trains on benign only. Sorted by RandomForest ROC-AUC.
R@5% = recall at 5% benign false-positive rate.

| Held-out family | n | RF AUC | XGB AUC | AE AUC | RF R@5% | AE R@5% |
|---|---|---|---|---|---|---|
| Fuzzers | 24246 | **0.855** | 0.862 | 0.580 | 0.382 | 0.235 |
| Analysis | 2677 | 0.957 | 0.951 | 0.920 | 0.809 | 0.824 |
| Reconnaissance | 13987 | 0.982 | 0.982 | 0.540 | 0.887 | 0.274 |
| Shellcode | 1511 | 0.983 | 0.984 | 0.377 | 0.915 | 0.034 |
| Generic | 58871 | 0.984 | 0.998 | 0.994 | 1.000 | 0.991 |
| Exploits | 44525 | 0.992 | 0.993 | 0.928 | 0.970 | 0.844 |
| Worms | 174 | 0.998 | 0.998 | 0.879 | 0.989 | 0.385 |
| DoS | 16353 | 0.998 | 0.999 | 0.952 | 0.992 | 0.898 |
| Backdoor | 2329 | 0.999 | 1.000 | 0.946 | 0.999 | 0.912 |

**Takeaways:** supervised models generalize to unseen families well (AUC > 0.98 for
7/9). The label-free autoencoder rarely adds value and fails badly on Shellcode,
Reconnaissance, Worms. **Fuzzers** is the blind spot for every method.

## 2. TTL feature ablation

SHAP attributes most of the decision to `sttl` (source TTL). But removing it — or the
whole TTL group — barely changes RandomForest ROC-AUC (≤ 0.003 on any family):

| Held-out family | All features | −`sttl` | −TTL group |
|---|---|---|---|
| Fuzzers | 0.855 | 0.855 | 0.852 |
| Reconnaissance | 0.982 | 0.982 | 0.982 |
| Generic | 0.984 | 0.983 | 0.981 |
| DoS | 0.998 | 0.998 | 0.998 |
| Backdoor | 0.999 | 0.999 | 0.999 |

**Takeaway:** high SHAP attribution ≠ necessity. The TTL signal is redundantly
encoded across correlated features, so cross-family generalization is robust, not a
fragile single-feature shortcut. Feature importance in correlated NIDS feature spaces
must be validated by ablation, not read from attribution alone.

## 3. Explainability (SHAP)

For well-generalized families (DoS) a clean TTL-based separator emerges; for Fuzzers
attributions are diffuse, so no single feature cleanly separates the unseen family —
matching its poor ROC-AUC. See `demo/shap_rf_holdout_{DoS,Fuzzers}.png` and the ROC
panel `demo/roc_zeroday.png`.

## 3a. Autoencoder threshold sweep

The leave-one-family-out table reports the autoencoder at one operating point. Sweeping
the decision threshold `t = mean + k·std` of benign reconstruction error shows the full
trade-off behind that number (`demo/ae_threshold_sweep.png`; reproduce with
`python -m src.experiment_threshold --families DoS,Fuzzers`).

For **DoS** the benign-FPR and zero-day-recall curves separate: a threshold exists
(around `k≈1.5`) that keeps recall ≈ 0.85 at ≈ 2% FPR. For **Fuzzers** the two curves
track each other across the whole range — recall is never much above the FPR you pay
for it — so no threshold makes the autoencoder useful. This is the operating-point view
of the same result the ROC-AUC reports: the autoencoder is a real detector for DoS and
near-random for Fuzzers.

## 4. Cross-dataset validation (CIC-IDS2017)

Same leave-one-family-out protocol on an independent dataset (52 CICFlowMeter
features; cleaned, class-capped subsample of 203,241 flows / 100,000 benign / 6
families). Reproduce with `python scripts/prepare_cicids.py` then
`python -m src.experiment_loo --config config_cicids.yaml --tag _cicids`.

| Held-out family | RF AUC | XGB AUC | AE AUC | RF R@5% | AE R@5% |
|---|---|---|---|---|---|
| Bots | **0.639** | 0.698 | 0.662 | 0.084 | 0.024 |
| Port Scanning | **0.779** | 0.787 | 0.778 | 0.140 | 0.025 |
| Brute Force | 0.974 | 0.976 | 0.704 | 0.997 | 0.000 |
| DDoS | 0.989 | 0.961 | 0.915 | 1.000 | 0.635 |
| DoS | 0.991 | 0.997 | 0.960 | 0.975 | 0.862 |
| Web Attacks | 0.996 | 0.999 | 0.654 | 1.000 | 0.044 |

**Takeaway:** the pattern replicates across datasets. Supervised models generalize to
most unseen families (DoS, DDoS, Brute Force, Web Attacks; AUC > 0.97), the
autoencoder rarely helps, and the supervised blind spots — **Bots** and **Port
Scanning** here (the analogue of Fuzzers on UNSW-NB15) — are exactly where the
autoencoder *also* fails. Anomaly detection is not a reliable zero-day safety net on
either dataset.
