# Week 2 - Supervised Detection Results

Binary attack-vs-benign detection on UNSW-NB15 (stratified 80/20 split,
257,673 flows). Evaluated on the held-out test set.

| Model | Accuracy | Precision (attack) | Recall (attack) | F1 (attack) | ROC-AUC |
|---|---|---|---|---|---|
| RandomForest | 0.95 | 0.96 | 0.96 | 0.96 | 0.9925 |
| XGBoost | 0.95 | 0.97 | 0.96 | 0.96 | 0.9925 |

Both models detect known attacks accurately. ROC comparison: `week2_roc.png`.
Reproduce with `python -m src.train`.
