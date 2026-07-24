# Week 4 - Explainability (SHAP)

Every detection can now be explained, so an analyst can see *why* a flow was flagged
instead of trusting a black box. We use TreeSHAP on the XGBoost detector.

## Global: what drives detections overall
Top features by mean |SHAP| across 800 test flows (`week4_shap_global.png`):

| Feature | mean abs SHAP |
|---|---|
| `sttl` (source time-to-live) | 4.04 |
| `ct_dst_sport_ltm` | 1.13 |
| `service_dns` | 1.01 |
| `ct_dst_src_ltm` | 0.75 |
| `ct_state_ttl` | 0.66 |

`sttl` dominates by a wide margin: low TTL values push strongly toward "benign", so
the model leans heavily on TTL behaviour to separate attacks from normal traffic.

## Local: explaining a single alert
For one flow the detector flagged (true category **Generic**), the biggest
contributions pushing it toward "attack" were (`week4_shap_one_alert.png`):

| Feature | SHAP value |
|---|---|
| `service_dns` | +3.97 |
| `ct_dst_sport_ltm` | +3.43 |
| `sttl` | +1.65 |
| `ct_dst_src_ltm` | -1.32 |

Red bars push toward attack, blue toward benign. Reproduce with
`python -m src.explain_run`.
