"""
FNO Model Architecture for the FNO×RG Unified Turbulence Framework.

Implements a shared-backbone FNO with system-specific input/output heads
for six turbulent systems: Navier-Stokes, quantum, compressible, MHD,
stratified, and active matter.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange
from typing import Optional, Dict, Tuple
import math


class SpectralConv2d(nn.Module):
    """2D spectral convolution layer for FNO."""

    def __init__(self, in_channels: int, out_channels: int, num_modes: int):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_modes = num_modes

        scale = 1.0 / (in_channels * out_channels)
        self.weights1 = nn.Parameter(
            scale * torch.rand(in_channels, out_channels, num_modes, num_modes, dtype=torch.cfloat)
        )
        self.weights2 = nn.Parameter(
            scale * torch.rand(in_channels, out_channels, num_modes, num_modes, dtype=torch.cfloat)
        )

    def compl_mul2d(self, input: torch.Tensor, weights: torch.Tensor) -> torch.Tensor:
        """Complex multiplication for spectral convolution."""
        return torch.einsum("bixy,ioxy->boxy", input, weights)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.shape[0]
        x_ft = torch.fft.rfft2(x)

        out_ft = torch.zeros(
            batch_size, self.out_channels, x.size(-2), x.size(-1) // 2 + 1,
            dtype=torch.cfloat, device=x.device
        )

        # Upper-left modes
        out_ft[:, :, :self.num_modes, :self.num_modes] = self.compl_mul2d(
            x_ft[:, :, :self.num_modes, :self.num_modes], self.weights1
        )
        # Upper-right modes
        out_ft[:, :, -self.num_modes:, :self.num_modes] = self.compl_mul2d(
            x_ft[:, :, -self.num_modes:, :self.num_modes], self.weights2
        )

        return torch.fft.irfft2(out_ft, s=(x.size(-2), x.size(-1)))


class SpectralConv3d(nn.Module):
    """3D spectral convolution layer for FNO (used in volumetric systems)."""

    def __init__(self, in_channels: int, out_channels: int, num_modes: int):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_modes = num_modes

        scale = 1.0 / (in_channels * out_channels)
        self.weights1 = nn.Parameter(
            scale * torch.rand(in_channels, out_channels, num_modes, num_modes, num_modes, dtype=torch.cfloat)
        )
        self.weights2 = nn.Parameter(
            scale * torch.rand(in_channels, out_channels, num_modes, num_modes, num_modes, dtype=torch.cfloat)
        )
        self.weights3 = nn.Parameter(
            scale * torch.rand(in_channels, out_channels, num_modes, num_modes, num_modes, dtype=torch.cfloat)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.shape[0]
        x_ft = torch.fft.rfftn(x, dim=[-3, -2, -1])

        out_ft = torch.zeros(
            batch_size, self.out_channels,
            x.size(-3), x.size(-2), x.size(-1) // 2 + 1,
            dtype=torch.cfloat, device=x.device
        )

        m = self.num_modes
        out_ft[:, :, :m, :m, :m] = torch.einsum(
            "bixyz,ioxyz->boxyz",
            x_ft[:, :, :m, :m, :m], self.weights1
        )
        out_ft[:, :, -m:, :m, :m] = torch.einsum(
            "bixyz,ioxyz->boxyz",
            x_ft[:, :, -m:, :m, :m], self.weights2
        )
        out_ft[:, :, :m, -m:, :m] = torch.einsum(
            "bixyz,ioxyz->boxyz",
            x_ft[:, :, :m, -m:, :m], self.weights3
        )

        return torch.fft.irfftn(out_ft, s=(x.size(-3), x.size(-2), x.size(-1)), dim=[-3, -2, -1])


class FNOBlock(nn.Module):
    """Single FNO layer: spectral conv + pointwise conv + activation."""

    def __init__(self, in_channels: int, out_channels: int, num_modes: int,
                 activation: str = "silu", use_3d: bool = False):
        super().__init__()
        ConvClass = SpectralConv3d if use_3d else SpectralConv2d

        self.spectral_conv = ConvClass(in_channels, out_channels, num_modes)
        self.pointwise = nn.Conv2d(in_channels, out_channels, 1) if not use_3d else nn.Conv3d(in_channels, out_channels, 1)

        if activation == "silu":
            self.activation = nn.SiLU()
        elif activation == "gelu":
            self.activation = nn.GELU()
        elif activation == "relu":
            self.activation = nn.ReLU()
        else:
            raise ValueError(f"Unknown activation: {activation}")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.activation(self.spectral_conv(x) + self.pointwise(x))


class FNOBackbone(nn.Module):
    """
    Shared FNO backbone with L Fourier layers.

    Default configuration (from paper Appendix A):
        - L=4 Fourier layers
        - 64 Fourier modes per layer
        - Lifting dimension d_v=128
        - SiLU activation
        - Spectral residual connections
    """

    def __init__(
        self,
        in_channels: int = 3,
        num_modes: int = 64,
        lifting_dim: int = 128,
        num_layers: int = 4,
        activation: str = "silu",
        use_3d: bool = False,
    ):
        super().__init__()
        self.num_layers = num_layers
        self.lifting_dim = lifting_dim

        # Lifting layer: project input to higher-dimensional space
        if use_3d:
            self.lifting = nn.Conv3d(in_channels, lifting_dim, 1)
        else:
            self.lifting = nn.Conv2d(in_channels, lifting_dim, 1)

        # Fourier layers
        self.fno_layers = nn.ModuleList([
            FNOBlock(lifting_dim, lifting_dim, num_modes, activation, use_3d)
            for _ in range(num_layers)
        ])

        # Projection layer: project back to output dimension
        self.projection = nn.Sequential(
            nn.Linear(lifting_dim, 256) if not use_3d else nn.Linear(lifting_dim, 256),
            nn.SiLU(),
            nn.Linear(256, 64),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Input field tensor, shape (B, C_in, *spatial_dims)

        Returns:
            Learned spectral features, shape (B, 64, *spatial_dims)
        """
        x = self.lifting(x)

        for layer in self.fno_layers:
            x = layer(x) + x  # Spectral residual connection

        # Reshape for projection
        if x.dim() == 4:  # (B, C, H, W)
            x = rearrange(x, "b c h w -> b h w c")
        elif x.dim() == 5:  # (B, C, D, H, W)
            x = rearrange(x, "b c d h w -> b d h w c")

        x = self.projection(x)

        if x.dim() == 4:
            x = rearrange(x, "b h w c -> b c h w")
        elif x.dim() == 5:
            x = rearrange(x, "b d h w c -> b c d h w")

        return x


class SpectralClosureHead(nn.Module):
    """
    System-specific output head that produces the spectral closure Γ_κ(k).

    Each system has different input fields and output structure:
        - NS: u(x,t) → Γ_κ(k)
        - Quantum: ψ(x,t) → Γ_κ(k, L)
        - Compressible: (ρ, u, T) → Γ_κ(k, Ma)
        - MHD: (z+, z-) → (Γ_κ+, Γ_κ-)
        - Stratified: (u, b) → (Γ_κ^v, Γ_κ^b)
        - Active: (u, Q) → (Γ_κ^v, Γ_κ^Q)
    """

    def __init__(self, system: str, backbone_out_dim: int = 64, num_modes: int = 64):
        super().__init__()
        self.system = system

        if system == "navier_stokes":
            self.in_channels = 3  # (u_x, u_y, u_z)
            self.out_channels = 2  # Γ_κ real and imaginary parts
        elif system == "quantum":
            self.in_channels = 2  # ψ real and imaginary
            self.out_channels = 4  # Γ_κ(k, L) for different polarization sectors
        elif system == "compressible":
            self.in_channels = 5  # (ρ, u_x, u_y, u_z, T)
            self.out_channels = 4  # Γ_κ(k, Ma) - Mach-dependent
        elif system == "mhd":
            self.in_channels = 6  # (z+_x, z+_y, z+_z, z-_x, z-_y, z-_z)
            self.out_channels = 4  # (Γ_κ+, Γ_κ-)
        elif system == "stratified":
            self.in_channels = 4  # (u_x, u_y, u_z, b)
            self.out_channels = 4  # (Γ_κ^v, Γ_κ^b)
        elif system == "active_matter":
            self.in_channels = 7  # (u_x, u_y, u_z, Q_xx, Q_xy, Q_xz, Q_yy)
            self.out_channels = 4  # (Γ_κ^v, Γ_κ^Q)
        else:
            raise ValueError(f"Unknown system: {system}")

        self.head = nn.Sequential(
            nn.Conv2d(self.in_channels, 128, 1),
            nn.SiLU(),
            nn.Conv2d(128, 64, 1),
            nn.SiLU(),
            nn.Conv2d(64, self.out_channels, 1),
        )

    def forward(self, input_field: torch.Tensor) -> torch.Tensor:
        """
        Args:
            input_field: System-specific input, shape (B, C_in, H, W)

        Returns:
            Spectral closure Γ_κ, shape (B, C_out, H, W)
        """
        return self.head(input_field)


class FNOxRGModel(nn.Module):
    """
    Complete FNO×RG model: backbone + system-specific closure head.

    Usage:
        model = FNOxRGModel(system="navier_stokes")
        closure = model(input_field)  # Returns Γ_κ(k)
    """

    def __init__(
        self,
        system: str,
        num_modes: int = 64,
        lifting_dim: int = 128,
        num_layers: int = 4,
        activation: str = "silu",
        use_3d: bool = False,
    ):
        super().__init__()
        self.system = system

        # Determine input channels based on system
        system_in_channels = {
            "navier_stokes": 3,
            "quantum": 2,
            "compressible": 5,
            "mhd": 6,
            "stratified": 4,
            "active_matter": 7,
        }

        in_ch = system_in_channels[system]

        # Shared backbone
        self.backbone = FNOBackbone(
            in_channels=in_ch,
            num_modes=num_modes,
            lifting_dim=lifting_dim,
            num_layers=num_layers,
            activation=activation,
            use_3d=use_3d,
        )

        # System-specific closure head
        self.closure_head = SpectralClosureHead(
            system=system,
            backbone_out_dim=64,
            num_modes=num_modes,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Full forward pass: input field → FNO features → spectral closure Γ_κ.

        Args:
            x: Input field tensor, shape (B, C_in, *spatial)

        Returns:
            Spectral closure Γ_κ(k), shape (B, C_out, *spatial)
        """
        features = self.backbone(x)
        closure = self.closure_head(x)
        return closure

    def get_config(self) -> Dict:
        """Return model configuration for reproducibility."""
        return {
            "system": self.system,
            "num_modes": self.backbone.fno_layers[0].spectral_conv.num_modes,
            "lifting_dim": self.backbone.lifting_dim,
            "num_layers": self.backbone.num_layers,
        }
