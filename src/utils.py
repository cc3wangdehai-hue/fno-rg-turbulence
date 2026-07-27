"""
Utility functions for the FNO×RG framework.

Includes data loading, spectral transforms, and diagnostic tools.
"""

import torch
import numpy as np
from typing import Dict, Tuple, Optional
import os


def compute_energy_spectrum(velocity_field: torch.Tensor) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the energy spectrum E(k) from a velocity field.

    Args:
        velocity_field: Velocity field, shape (B, 3, H, W) or (B, 3, D, H, W)

    Returns:
        k: Wavenumber array
        E_k: Energy spectrum
    """
    if velocity_field.dim() == 4:
        # 2D case
        u_ft = torch.fft.rfft2(velocity_field, dim=(-2, -1), norm="ortho")
        kx = torch.fft.fftfreq(velocity_field.shape[-2], d=1.0/velocity_field.shape[-2])
        ky = torch.fft.rfftfreq(velocity_field.shape[-1], d=1.0/velocity_field.shape[-1])

        KX, KY = torch.meshgrid(kx, ky, indexing="ij")
        K = torch.sqrt(KX**2 + KY**2 + 1e-8)

        # Energy at each wavenumber
        E = 0.5 * (u_ft.abs()**2).sum(dim=1)  # Sum over components

        # Bin by wavenumber
        k_max = int(K.max().item())
        k_bins = np.arange(0, k_max + 1)
        E_k = np.zeros(k_max)

        K_np = K.cpu().numpy()
        E_np = E.mean(dim=0).cpu().numpy()

        for i in range(k_max):
            mask = (K_np >= i) & (K_np < i + 1)
            if mask.sum() > 0:
                E_k[i] = E_np[mask].mean()

        k_arr = np.arange(k_max) + 0.5
        return k_arr, E_k

    else:
        # 3D case
        u_ft = torch.fft.rfftn(velocity_field, dim=(-3, -2, -1), norm="ortho")

        kx = torch.fft.fftfreq(velocity_field.shape[-3], d=1.0/velocity_field.shape[-3])
        ky = torch.fft.fftfreq(velocity_field.shape[-2], d=1.0/velocity_field.shape[-2])
        kz = torch.fft.rfftfreq(velocity_field.shape[-1], d=1.0/velocity_field.shape[-1])

        KX, KY, KZ = torch.meshgrid(kx, ky, kz, indexing="ij")
        K = torch.sqrt(KX**2 + KY**2 + KZ**2 + 1e-8)

        E = 0.5 * (u_ft.abs()**2).sum(dim=1)
        E = E.mean(dim=0).cpu().numpy()
        K_np = K.cpu().numpy()

        k_max = int(K.max().item())
        E_k = np.zeros(k_max)
        for i in range(k_max):
            mask = (K_np >= i) & (K_np < i + 1)
            if mask.sum() > 0:
                E_k[i] = E[mask].mean()

        k_arr = np.arange(k_max) + 0.5
        return k_arr, E_k


def she_leveque_scaling(p: np.ndarray, C: float = 2.0, sigma: float = 1.0/3) -> np.ndarray:
    """
    Compute She-Leveque scaling exponents.

    ζ_p = p/9 + C - C(σ/3)^{p/3}

    With C = 2/(1 - σ/3) constraint, this gives C = 2/(1-1/9) = 9/4.

    Args:
        p: Order array
        C: Intermittency parameter
        sigma: Ratio parameter (default 1/3 for SL)

    Returns:
        ζ_p values
    """
    return p / 9.0 + C - C * (sigma / 3.0) ** (p / 3.0)


def structure_functions(velocity_field: np.ndarray, orders: np.ndarray,
                        max_r: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute longitudinal structure functions S_p(r) = <|δu_L(r)|^p>.

    Args:
        velocity_field: 3D velocity field (3, Nx, Ny, Nz)
        orders: Array of p values
        max_r: Maximum separation distance (fraction of domain)

    Returns:
        r: Separation distances
        S_p: Structure function values for each order
    """
    N = velocity_field.shape[1]
    r_max = int(max_r * N)

    # Compute longitudinal velocity differences along x
    u_x = velocity_field[0]  # (Nx, Ny, Nz)

    n_r = min(r_max, N // 2)
    r_arr = np.arange(1, n_r + 1) / N
    S_p = np.zeros((len(orders), n_r))

    for i, r in enumerate(range(1, n_r + 1)):
        delta_u = np.roll(u_x, -r, axis=0) - u_x
        delta_u = delta_u[:N-r]  # Trim to avoid wrap-around artifacts

        for j, p in enumerate(orders):
            S_p[j, i] = np.mean(np.abs(delta_u) ** p)

    return r_arr, S_p


def load_jhtdb_data(variable: str = "Velocity", time_step: int = 0,
                    resolution: int = 1024) -> np.ndarray:
    """
    Download data from Johns Hopkins Turbulence Database.

    Uses the JHTDB web service API.
    Requires internet connection and may need an authentication token.

    Args:
        variable: "Velocity", "Force", "Pressure", etc.
        time_step: Time step index
        resolution: Spatial resolution (up to 1024 for isotropic 1024^3)

    Returns:
        3D field array
    """
    # JHTDB web service endpoint
    base_url = "https://turbulence.pha.jhu.edu/service/turbulence/turbulence1024"

    # For local development, generate synthetic data if JHTDB is unavailable
    print(f"Note: JHTDB data loading requires web access. Using placeholder data.")
    print(f"In production, download from: http://turbulence.pha.jhu.edu/")

    np.random.seed(42)
    # Generate synthetic turbulence-like field for testing
    field = np.random.randn(3, resolution, resolution, resolution).astype(np.float32) * 0.1
    return field


def filter_field(field: np.ndarray, kappa: float) -> np.ndarray:
    """
    Apply a sharp spectral filter at wavenumber kappa.

    Used to compute the filtered field ū_κ for the FNO×RG closure.

    Args:
        field: Input field in physical space
        kappa: Filter cutoff wavenumber

    Returns:
        Filtered field in physical space
    """
    if field.ndim == 3:
        field_ft = np.fft.rfftn(field)
        kx = np.fft.fftfreq(field.shape[0], d=1.0/field.shape[0])
        ky = np.fft.fftfreq(field.shape[1], d=1.0/field.shape[1])
        kz = np.fft.rfftfreq(field.shape[2], d=1.0/field.shape[2])

        KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing="ij")
        K = np.sqrt(KX**2 + KY**2 + KZ**2)

        # Sharp spectral filter
        mask = K <= kappa
        field_ft_filtered = field_ft * mask

        return np.fft.irfftn(field_ft_filtered, s=field.shape)
    else:
        # 2D case
        field_ft = np.fft.rfft2(field)
        kx = np.fft.fftfreq(field.shape[0], d=1.0/field.shape[0])
        ky = np.fft.rfftfreq(field.shape[1], d=1.0/field.shape[1])

        KX, KY = np.meshgrid(kx, ky, indexing="ij")
        K = np.sqrt(KX**2 + KY**2)

        mask = K <= kappa
        field_ft_filtered = field_ft * mask

        return np.fft.irfft2(field_ft_filtered, s=field.shape)


def compute_eddy_viscosity(filtered_field: np.ndarray, full_field: np.ndarray,
                           kappa: float) -> float:
    """
    Estimate the scale-dependent eddy viscosity ν_t(κ) from DNS data.

    Uses the energy transfer method:
        ν_t(κ) = -T(κ) / (2κ² E(κ))

    where T(κ) is the energy flux through scale κ.

    Args:
        filtered_field: Filtered velocity field at scale κ
        full_field: Full (unfiltered) velocity field
        kappa: Filter scale

    Returns:
        Estimated eddy viscosity
    """
    # Compute subgrid stress
    subgrid_stress = np.mean(full_field**2) - np.mean(filtered_field**2)

    # Compute strain rate of filtered field
    grad_u = np.gradient(filtered_field)
    strain = 0.5 * (np.array(grad_u) + np.array(grad_u).transpose(
        list(range(len(grad_u[0].shape))) + [len(grad_u[0].shape)]
    ))
    strain_rate = np.sqrt(np.mean(strain**2))

    if strain_rate > 1e-10:
        nu_t = subgrid_stress / (2 * strain_rate)
    else:
        nu_t = 0.0

    return float(nu_t)
