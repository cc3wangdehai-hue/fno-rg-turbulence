"""
Plot energy spectra and fixed-point structures.
"""

import numpy as np
import json
import argparse
from pathlib import Path

def plot_energy_spectrum(k, E_k, system_name, output_path=None):
    """Plot E(k) with K41 reference."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot data
    mask = (k > 0) & (E_k > 0)
    ax.loglog(k[mask], E_k[mask], 'b-', label='FNO×RG', linewidth=2)

    # K41 reference: E(k) ∝ k^(-5/3)
    E_k41 = E_k[mask][0] * (k[mask] / k[mask][0]) ** (-5/3)
    ax.loglog(k[mask], E_k41, 'k--', alpha=0.5, label='K41 ($k^{-5/3}$)')

    ax.set_xlabel('Wavenumber $k$', fontsize=14)
    ax.set_ylabel('Energy Spectrum $E(k)$', fontsize=14)
    ax.set_title(f'Energy Spectrum: {system_name}', fontsize=16)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150)
        print(f"Spectrum plot saved to {output_path}")
    plt.close()


def plot_beta_function(g, beta, system_name, coupling_name, output_path=None):
    """Plot β(g) with zero crossings marked."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(g, beta, 'b-', linewidth=2, label=r'$\beta(g)$')
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)

    # Mark zero crossings (fixed points)
    zero_crossings = np.where(np.diff(np.sign(beta)))[0]
    for idx in zero_crossings:
        g_star = (g[idx] + g[idx+1]) / 2
        ax.axvline(x=g_star, color='r', linestyle=':', alpha=0.7)
        ax.annotate(f'FP: $g^*={g_star:.3f}$',
                    xy=(g_star, 0), xytext=(g_star, beta.max()*0.3),
                    arrowprops=dict(arrowstyle='->', color='r'))

    ax.set_xlabel(f'Coupling $g$ ({coupling_name})', fontsize=14)
    ax.set_ylabel(r'$\beta(g)$', fontsize=14)
    ax.set_title(f'β-function: {system_name} — {coupling_name}', fontsize=16)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150)
        print(f"β-function plot saved to {output_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--system', type=str, default='navier_stokes')
    parser.add_argument('--results_dir', type=str, default='results')
    parser.add_argument('--plot_dir', type=str, default='plots')
    args = parser.parse_args()

    plot_dir = Path(args.plot_dir)
    plot_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating plots for {args.system}...")
    print(f"Output directory: {plot_dir}/")

if __name__ == "__main__":
    main()
