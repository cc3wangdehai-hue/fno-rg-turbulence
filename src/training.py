"""
Training pipeline for the FNO×RG framework.

Implements the Stage I (FNO spectral learning) with system-specific
data loading, spectral loss computation, and training loop.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import yaml
import os
import argparse
from tqdm import tqdm
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Tuple

from model import FNOxRGModel


class TurbulenceDataset(Dataset):
    """
    Generic turbulence dataset for FNO training.

    Loads (input_field, target_closure) pairs from HDF5 or numpy files.
    The target_closure is the spectral closure Γ_κ computed from DNS data
    via filtering at scale κ.
    """

    def __init__(self, data_path: str, system: str, split: str = "train",
                 num_time_steps: int = 3):
        """
        Args:
            data_path: Path to HDF5 or .npy data file
            system: System identifier (navier_stokes, quantum, etc.)
            split: "train" or "val"
            num_time_steps: Number of time steps to use as input
        """
        self.system = system
        self.num_time_steps = num_time_steps

        if data_path.endswith(".npy"):
            data = np.load(data_path, allow_pickle=True).item()
        else:
            import h5py
            with h5py.File(data_path, "r") as f:
                data = {key: f[key][:] for key in f.keys()}

        if split == "train":
            self.input_fields = data["input_train"]   # (N, T, C_in, H, W)
            self.target_closure = data["target_train"] # (N, C_out, H, W)
        else:
            self.input_fields = data["input_val"]
            self.target_closure = data["target_val"]

    def __len__(self):
        return len(self.input_fields)

    def __getitem__(self, idx):
        x = torch.tensor(self.input_fields[idx], dtype=torch.float32)
        y = torch.tensor(self.target_closure[idx], dtype=torch.float32)
        return x, y


class SpectralLoss(nn.Module):
    """
    Spectral L² loss for FNO training.

    Computes the loss in Fourier space to emphasize large-scale
    (energy-containing) modes, following the FNO paper.
    """

    def __init__(self, max_scale_weight: float = 2.0):
        super().__init__()
        self.max_scale_weight = max_scale_weight

    def forward(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """
        Args:
            pred: Predicted spectral closure, shape (B, C, H, W)
            target: Target spectral closure, shape (B, C, H, W)

        Returns:
            Scalar loss
        """
        # Fourier transform
        pred_ft = torch.fft.rfft2(pred, norm="ortho")
        target_ft = torch.fft.rfft2(target, norm="ortho")

        # Scale-dependent weights (emphasize large scales)
        H, W = pred_ft.shape[-2], pred_ft.shape[-1]
        kx = torch.fft.fftfreq(H, d=1.0 / H).unsqueeze(1).to(pred.device)
        ky = torch.fft.rfftfreq(W, d=1.0 / W).unsqueeze(0).to(pred.device)
        k = torch.sqrt(kx**2 + ky**2 + 1e-8)
        k_norm = k / k.max()

        # Weight: emphasize low-k (large-scale) modes
        weight = self.max_scale_weight * torch.exp(-k_norm)

        # Weighted L² loss in Fourier space
        diff = pred_ft - target_ft
        loss = (weight * diff.abs() ** 2).mean()

        return loss


class CosineAnnealingLR(optim.lr_scheduler._LRScheduler):
    """Cosine annealing learning rate scheduler."""

    def __init__(self, optimizer, T_max: int, eta_min: float = 1e-6):
        self.T_max = T_max
        self.eta_min = eta_min
        super().__init__(optimizer)

    def get_lr(self):
        if self.last_epoch == 0:
            return [group["lr"] for group in self.optimizer.param_groups]
        return [
            self.eta_min + (base_lr - self.eta_min) *
            (1 + np.cos(np.pi * self.last_epoch / self.T_max)) / 2
            for base_lr in self.optimizer.param_groups[0]["lr"]
        ]


def train_epoch(model: nn.Module, dataloader: DataLoader,
                optimizer: optim.Optimizer, loss_fn: nn.Module,
                device: torch.device) -> float:
    """Train for one epoch."""
    model.train()
    total_loss = 0.0

    for batch_idx, (inputs, targets) in enumerate(tqdm(dataloader, desc="Training")):
        inputs = inputs.to(device)
        targets = targets.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_fn(outputs, targets)
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        optimizer.step()
        total_loss += loss.item()

    return total_loss / len(dataloader)


@torch.no_grad()
def validate(model: nn.Module, dataloader: DataLoader,
             loss_fn: nn.Module, device: torch.device) -> float:
    """Validate model."""
    model.eval()
    total_loss = 0.0

    for inputs, targets in dataloader:
        inputs = inputs.to(device)
        targets = targets.to(device)

        outputs = model(inputs)
        loss = loss_fn(outputs, targets)
        total_loss += loss.item()

    return total_loss / len(dataloader)


def train(config_path: str):
    """
    Full training pipeline.

    Args:
        config_path: Path to YAML configuration file
    """
    # Load configuration
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    system = config["system"]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training {system} system on {device}")

    # Create datasets
    train_dataset = TurbulenceDataset(
        data_path=config["data"]["train_path"],
        system=system,
        split="train",
        num_time_steps=config["data"].get("num_time_steps", 3),
    )
    val_dataset = TurbulenceDataset(
        data_path=config["data"]["val_path"],
        system=system,
        split="val",
        num_time_steps=config["data"].get("num_time_steps", 3),
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=config["training"]["batch_size"],
        shuffle=True,
        num_workers=config["training"].get("num_workers", 4),
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config["training"]["batch_size"],
        shuffle=False,
        num_workers=config["training"].get("num_workers", 4),
        pin_memory=True,
    )

    # Create model
    model = FNOxRGModel(
        system=system,
        num_modes=config["model"].get("num_modes", 64),
        lifting_dim=config["model"].get("lifting_dim", 128),
        num_layers=config["model"].get("num_layers", 4),
        activation=config["model"].get("activation", "silu"),
        use_3d=config["model"].get("use_3d", False),
    ).to(device)

    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Optimizer and scheduler
    optimizer = optim.Adam(
        model.parameters(),
        lr=config["training"]["learning_rate"],
        weight_decay=config["training"].get("weight_decay", 1e-5),
    )
    scheduler = CosineAnnealingLR(
        optimizer,
        T_max=config["training"]["epochs"],
        eta_min=config["training"].get("eta_min", 1e-6),
    )

    # Loss function
    loss_fn = SpectralLoss(
        max_scale_weight=config["training"].get("max_scale_weight", 2.0)
    )

    # Training loop
    best_val_loss = float("inf")
    checkpoint_dir = Path(config.get("checkpoint_dir", "checkpoints"))
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, config["training"]["epochs"] + 1):
        train_loss = train_epoch(model, train_loader, optimizer, loss_fn, device)
        val_loss = validate(model, val_loader, loss_fn, device)
        scheduler.step()

        lr = optimizer.param_groups[0]["lr"]
        print(f"Epoch {epoch}/{config['training']['epochs']} | "
              f"Train: {train_loss:.6f} | Val: {val_loss:.6f} | LR: {lr:.2e}")

        # Save best checkpoint
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_loss": val_loss,
                "config": config,
                "model_config": model.get_config(),
            }, checkpoint_dir / f"{system}_best.pt")
            print(f"  -> New best checkpoint (val_loss={val_loss:.6f})")

    # Save final checkpoint
    torch.save({
        "epoch": config["training"]["epochs"],
        "model_state_dict": model.state_dict(),
        "config": config,
        "model_config": model.get_config(),
    }, checkpoint_dir / f"{system}_final.pt")

    print(f"\nTraining complete. Best val loss: {best_val_loss:.6f}")
    print(f"Checkpoints saved to {checkpoint_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FNO×RG Training Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config")
    args = parser.parse_args()
    train(args.config)
