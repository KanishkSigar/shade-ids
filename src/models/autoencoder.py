"""Week 3 - benign-only autoencoder for anomaly / zero-day detection.

Trained only on benign traffic, the autoencoder learns to reconstruct normal flows.
Attacks reconstruct poorly, so a high reconstruction error flags an anomaly - this
catches suspicious traffic without needing attack labels.
"""
from __future__ import annotations

import numpy as np
import torch
from torch import nn


class AutoEncoder(nn.Module):
    def __init__(self, n_features: int, hidden_dims: list[int]):
        super().__init__()
        dims = [n_features] + hidden_dims
        enc = []
        for a, b in zip(dims[:-1], dims[1:]):
            enc += [nn.Linear(a, b), nn.ReLU()]
        rev = list(reversed(dims))
        dec = []
        for a, b in zip(rev[:-1], rev[1:]):
            dec += [nn.Linear(a, b), nn.ReLU()]
        dec = dec[:-1]  # no activation on the final reconstruction
        self.encoder = nn.Sequential(*enc)
        self.decoder = nn.Sequential(*dec)

    def forward(self, x):
        return self.decoder(self.encoder(x))


def train_autoencoder(X_benign, hidden_dims, epochs, batch_size, lr, device="cpu") -> AutoEncoder:
    dev = device if torch.cuda.is_available() else "cpu"
    model = AutoEncoder(X_benign.shape[1], hidden_dims).to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    data = torch.tensor(np.asarray(X_benign), dtype=torch.float32)
    loader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(data), batch_size=batch_size, shuffle=True
    )
    model.train()
    for ep in range(epochs):
        total = 0.0
        for (batch,) in loader:
            batch = batch.to(dev)
            opt.zero_grad()
            loss = loss_fn(model(batch), batch)
            loss.backward()
            opt.step()
            total += loss.item() * len(batch)
        if (ep + 1) % 10 == 0 or ep == 0:
            print(f"[autoencoder] epoch {ep+1}/{epochs}  loss={total/len(data):.6f}")
    return model


@torch.no_grad()
def reconstruction_error(model: AutoEncoder, X) -> np.ndarray:
    """Per-row mean squared reconstruction error = anomaly score."""
    dev = next(model.parameters()).device
    t = torch.tensor(np.asarray(X), dtype=torch.float32).to(dev)
    recon = model(t)
    return ((recon - t) ** 2).mean(dim=1).cpu().numpy()


def choose_threshold(benign_errors: np.ndarray, k: float = 3.0) -> float:
    """Flag as anomalous above mean + k*std of benign reconstruction errors."""
    return float(benign_errors.mean() + k * benign_errors.std())
