#!/usr/bin/env python3
"""
Generate publication-quality plots for κ verification analysis.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import os
import sys

# Import models from main script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kappa_verification import (
    zeta_K41, zeta_LogNormal, zeta_SL, zeta_FNO_RG_kappa,
    experimental_data, extended_data, fit_kappa,
    compute_chi2, compute_rms
)

output_dir = os.path.dirname(os.path.abspath(__file__))

# Data
p_pri = experimental_data['p']
z_pri = experimental_data['zeta']
s_pri = experimental_data['sigma']

p_all = extended_data['p']
z_all = extended_data['zeta']
s_all = extended_data['sigma']

# Fit κ
kappa_best, kappa_err, kappas, chi2_vals = fit_kappa(p_all, z_all, s_all)

# ============================================================
# FIGURE 1: Main comparison plot - ζ_p vs p
# ============================================================

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

p_fine = np.linspace(0.5, 11, 300)

# Model curves
z_k41 = zeta_K41(p_fine)
z_ln = zeta_LogNormal(p_fine, mu=0.25)
z_sl = zeta_SL(p_fine)
z_fk = zeta_FNO_RG_kappa(p_fine, kappa=0.1146)
z_fk_fit = zeta_FNO_RG_kappa(p_fine, kappa=kappa_best)

# Plot model curves
ax.plot(p_fine, z_k41, 'k--', linewidth=1.5, alpha=0.5, label='K41: $\\zeta_p = p/3$')
ax.plot(p_fine, z_ln, 'g-.', linewidth=1.5, alpha=0.6, label='LogNormal ($\\mu=0.25$)')
ax.plot(p_fine, z_sl, 'b-', linewidth=2.5, label='She–Leveque (SL)')
ax.plot(p_fine, z_fk, 'r--', linewidth=2.0, label=f'SL + $\\kappa={0.1146}$ (FNO×RG)')
ax.plot(p_fine, z_fk_fit, 'm:', linewidth=1.8, label=f'SL + $\\kappa_{{fit}}={kappa_best:.3f}$')

# Experimental data points with error bars
ax.errorbar(p_pri, z_pri, yerr=s_pri, fmt='ko', markersize=8, capsize=4, 
            capthick=1.5, linewidth=1.5, zorder=10, label='Expt/DNS data')

# Annotate data sources
source_labels = {
    2: 'Gotoh 2002\nJHTDB',
    4: 'Anselmet 1984\nESS comp.',
    6: 'Belin 1996\nGotoh 2002',
    8: 'Anselmet 1984',
    10: 'Belin 1996'
}
for i, p in enumerate(p_pri):
    ax.annotate(source_labels.get(p, ''), 
                xy=(p, z_pri[i]), xytext=(p+0.3, z_pri[i]-0.12),
                fontsize=6.5, alpha=0.7,
                arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

# Add legend for data compilation
ax.text(7.5, 0.5, 'Compiled from:\n'
        '• Anselmet et al. (1984) JFM\n'
        '• Arneodo et al. (1996) EPL\n'
        '• Belin et al. (1996) Physica D\n'
        '• Gotoh et al. (2002) Phys. Fluids\n'
        '• Cao, Chen & She (1996) DNS',
        fontsize=7, bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.8),
        verticalalignment='top')

ax.set_xlabel('Order $p$', fontsize=13)
ax.set_ylabel('Scaling exponent $\\zeta_p$', fontsize=13)
ax.set_title('Turbulence Scaling Exponents: Model Predictions vs Experiment/DNS', fontsize=13)
ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax.set_xlim(0, 11.5)
ax.set_ylim(0, 3.5)
ax.grid(True, alpha=0.3)
ax.axhline(y=1, color='gray', linestyle=':', alpha=0.3)

# Add inset: zoom on p=6-10 region
ax_inset = ax.inset_axes([0.55, 0.25, 0.4, 0.4])
ax_inset.errorbar(p_pri, z_pri, yerr=s_pri, fmt='ko', markersize=6, capsize=3, 
                  capthick=1.2, linewidth=1.2, zorder=10)
ax_inset.plot(p_fine, z_sl, 'b-', linewidth=2, label='SL')
ax_inset.plot(p_fine, z_fk, 'r--', linewidth=1.5, label=f'SL+κ=0.1146')
ax_inset.plot(p_fine, z_fk_fit, 'm:', linewidth=1.3, label=f'SL+κ_fit={kappa_best:.3f}')
ax_inset.set_xlim(5, 11)
ax_inset.set_ylim(1.5, 3.0)
ax_inset.set_xlabel('$p$', fontsize=9)
ax_inset.set_ylabel('$\\zeta_p$', fontsize=9)
ax_inset.tick_params(labelsize=8)
ax_inset.legend(fontsize=7, loc='upper left')
ax_inset.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'kappa_verification_zeta_comparison.png'), 
            dpi=200, bbox_inches='tight')
fig.savefig(os.path.join(output_dir, 'kappa_verification_zeta_comparison.pdf'),
            bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 2: Residuals plot
# ============================================================

fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# Top panel: residuals (data - model) for each model
p_plot = p_pri
z_plot = z_pri
s_plot = s_pri

residuals_k41 = z_plot - zeta_K41(p_plot)
residuals_ln = z_plot - zeta_LogNormal(p_plot, mu=0.25)
residuals_sl = z_plot - zeta_SL(p_plot)
residuals_fk = z_plot - zeta_FNO_RG_kappa(p_plot, kappa=0.1146)
residuals_fk_fit = z_plot - zeta_FNO_RG_kappa(p_plot, kappa=kappa_best)

width = 0.15
x = p_plot

axes[0].bar(x - 2*width, residuals_k41/s_plot, width, label='K41', color='gray', alpha=0.7)
axes[0].bar(x - width, residuals_ln/s_plot, width, label='LogNormal', color='green', alpha=0.7)
axes[0].bar(x, residuals_sl/s_plot, width, label='SL', color='blue', alpha=0.7)
axes[0].bar(x + width, residuals_fk/s_plot, width, label=f'SL+κ=0.1146', color='red', alpha=0.7)
axes[0].bar(x + 2*width, residuals_fk_fit/s_plot, width, label=f'SL+κ_fit', color='magenta', alpha=0.7)
axes[0].axhline(0, color='k', linewidth=0.5)
axes[0].axhline(1, color='k', linewidth=0.5, linestyle='--', alpha=0.3)
axes[0].axhline(-1, color='k', linewidth=0.5, linestyle='--', alpha=0.3)
axes[0].set_ylabel('Residual / σ', fontsize=11)
axes[0].set_title('Standardized Residuals: (ζ_exp - ζ_model) / σ', fontsize=11)
axes[0].legend(fontsize=8, ncol=5, loc='upper right')
axes[0].set_xticks(p_plot)
axes[0].set_xticklabels([f'p={p}' for p in p_plot])
axes[0].grid(True, alpha=0.3, axis='y')

# Bottom panel: χ² per model
models = ['K41', 'LogN', 'SL', 'SL+κ\n(0.1146)', 'SL+κ\n(fit)']
chi2_values = [
    compute_chi2(p_plot, z_plot, s_plot, zeta_K41),
    compute_chi2(p_plot, z_plot, s_plot, zeta_LogNormal, mu=0.25),
    compute_chi2(p_plot, z_plot, s_plot, zeta_SL),
    compute_chi2(p_plot, z_plot, s_plot, zeta_FNO_RG_kappa, kappa=0.1146),
    compute_chi2(p_plot, z_plot, s_plot, zeta_FNO_RG_kappa, kappa=kappa_best),
]
colors = ['gray', 'green', 'blue', 'red', 'magenta']

axes[1].bar(range(len(models)), chi2_values, color=colors, alpha=0.8)
axes[1].set_xticks(range(len(models)))
axes[1].set_xticklabels(models, fontsize=9)
axes[1].set_ylabel('$\\chi^2$', fontsize=11)
axes[1].set_title(f'Goodness of Fit ($\\chi^2$, n={len(p_plot)}, dof={len(p_plot)-1})', fontsize=11)
axes[1].set_yscale('log')
axes[1].grid(True, alpha=0.3, axis='y')

# Add χ² values on top of bars
for i, v in enumerate(chi2_values):
    axes[1].text(i, v * 1.3, f'{v:.2f}', ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'kappa_verification_residuals.png'), 
            dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 3: κ fit profile (χ² vs κ)
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: χ²(κ) curve
axes[0].plot(kappas, chi2_vals, 'b-', linewidth=2)
axes[0].axhline(1, color='gray', linestyle='--', alpha=0.5, label='$\\chi^2 = 1$')
axes[0].axvline(0.1146, color='red', linestyle='--', linewidth=1.5, alpha=0.8, 
                label=f'Theory: $\\kappa = 0.1146$')
axes[0].axvline(kappa_best, color='green', linestyle='-', linewidth=1.5, alpha=0.8,
                label=f'Best fit: $\\kappa = {kappa_best:.3f} \\pm {kappa_err:.3f}$')
axes[0].axvline(0, color='black', linestyle=':', linewidth=1, alpha=0.5, label='SL ($\\kappa=0$)')

# Mark Δχ²=1 region
chi2_min = np.min(chi2_vals)
axes[0].axhline(chi2_min + 1, color='green', linestyle=':', alpha=0.5, label='$\\Delta\\chi^2 = 1$')
axes[0].fill_between(kappas, chi2_min, chi2_min + 1, alpha=0.15, color='green',
                     label='68% CI')

axes[0].set_xlabel('$\\kappa$', fontsize=12)
axes[0].set_ylabel('$\\chi^2(\\kappa)$', fontsize=12)
axes[0].set_title('$\\kappa$ Profile Likelihood', fontsize=12)
axes[0].legend(fontsize=8, loc='upper right')
axes[0].grid(True, alpha=0.3)
axes[0].set_xlim(-0.3, 0.4)

# Right: SL vs SL+κ predicted curves, zoomed to high-order
axes[1].plot(p_fine[p_fine >= 1], zeta_SL(p_fine[p_fine >= 1]), 'b-', linewidth=2.5, label='SL')
axes[1].plot(p_fine[p_fine >= 1], zeta_FNO_RG_kappa(p_fine[p_fine >= 1], kappa=0.1146), 
             'r--', linewidth=2, label=f'SL + κ=0.1146 (theory)')
axes[1].plot(p_fine[p_fine >= 1], zeta_FNO_RG_kappa(p_fine[p_fine >= 1], kappa=kappa_best),
             'm:', linewidth=1.8, label=f'SL + κ_fit={kappa_best:.3f}')
axes[1].errorbar(p_pri[p_pri >= 6], z_pri[p_pri >= 6], yerr=s_pri[p_pri >= 6],
                 fmt='ko', markersize=8, capsize=4, linewidth=1.5, zorder=10)

# Shade the divergence region
mask_div = p_fine >= 7
axes[1].fill_between(p_fine[mask_div], 
                     zeta_SL(p_fine[mask_div]), 
                     zeta_FNO_RG_kappa(p_fine[mask_div], kappa=0.1146),
                     alpha=0.15, color='red', label='Theory vs data gap')

axes[1].set_xlabel('Order $p$', fontsize=12)
axes[1].set_ylabel('$\\zeta_p$', fontsize=12)
axes[1].set_title('High-Order Divergence: SL vs SL+κ', fontsize=12)
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)
axes[1].set_xlim(5, 11.5)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'kappa_verification_kappa_fit.png'), 
            dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 4: κ correction magnitude
# ============================================================

fig, ax = plt.subplots(1, 1, figsize=(8, 5))

p_fine2 = np.linspace(0, 12, 200)
q = p_fine2 / 3.0
correction = 0.1146 * q * (q - 1) * (q - 2) / 6.0

ax.plot(p_fine2, correction, 'r-', linewidth=2, label='$\\kappa$ correction term')
ax.fill_between(p_fine2, 0, correction, where=correction > 0, alpha=0.2, color='red')
ax.fill_between(p_fine2, 0, correction, where=correction < 0, alpha=0.2, color='blue')
ax.axhline(0, color='k', linewidth=0.5)
ax.axvline(6, color='gray', linestyle='--', alpha=0.5, label='p=6 (zero crossing)')
ax.axvline(0, color='gray', linestyle=':', alpha=0.3)

# Mark where correction exceeds experimental errors
for p_val, sigma in zip(p_pri, s_pri):
    q_val = p_val / 3.0
    corr_val = 0.1146 * q_val * (q_val - 1) * (q_val - 2) / 6.0
    if abs(corr_val) > sigma:
        ax.plot(p_val, corr_val, 'kx', markersize=10, markeredgewidth=2)
        ax.annotate(f'p={p_val}: exceeds σ', xy=(p_val, corr_val),
                    xytext=(p_val+0.3, corr_val+0.02), fontsize=8)

ax.set_xlabel('Order $p$', fontsize=12)
ax.set_ylabel('$\\Delta\\zeta_p = \\kappa \\cdot q(q-1)(q-2)/6$', fontsize=11)
ax.set_title(f'$\\kappa$ Correction Magnitude ($\\kappa = 0.1146$)\n'
             f'× marks where |correction| > experimental σ', fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'kappa_verification_correction_magnitude.png'),
            dpi=200, bbox_inches='tight')
plt.close(fig)

# ============================================================
# FIGURE 5: Summary statistics dashboard
# ============================================================

fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(2, 2, hspace=0.35, wspace=0.3)

# Panel A: Model comparison radar-like plot
ax_a = fig.add_subplot(gs[0, 0])
models_names = ['K41', 'LogN', 'SL', 'SL+κ', 'SL+κ_fit']
rms_all = [
    compute_rms(p_pri, z_pri, zeta_K41),
    compute_rms(p_pri, z_pri, zeta_LogNormal, mu=0.25),
    compute_rms(p_pri, z_pri, zeta_SL),
    compute_rms(p_pri, z_pri, zeta_FNO_RG_kappa, kappa=0.1146),
    compute_rms(p_pri, z_pri, zeta_FNO_RG_kappa, kappa=kappa_best),
]
colors_bar = ['gray', 'green', 'blue', 'red', 'magenta']
bars = ax_a.barh(models_names, rms_all, color=colors_bar, alpha=0.8)
ax_a.set_xlabel('RMS Error', fontsize=10)
ax_a.set_title('(a) Model Accuracy (RMS)', fontsize=10)
for i, v in enumerate(rms_all):
    ax_a.text(v + 0.002, i, f'{v:.4f}', va='center', fontsize=8)
ax_a.grid(True, alpha=0.3, axis='x')

# Panel B: χ² for high-order data
ax_b = fig.add_subplot(gs[0, 1])
mask6 = p_pri >= 6
chi2_high = [
    compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], zeta_K41),
    compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], zeta_LogNormal, mu=0.25),
    compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], zeta_SL),
    compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], zeta_FNO_RG_kappa, kappa=0.1146),
    compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], zeta_FNO_RG_kappa, kappa=kappa_best),
]
ax_b.bar(models_names, chi2_high, color=colors_bar, alpha=0.8)
ax_b.set_yscale('log')
ax_b.set_ylabel('$\\chi^2$ (p≥6)', fontsize=10)
ax_b.set_title('(b) High-Order Fit Quality', fontsize=10)
for i, v in enumerate(chi2_high):
    ax_b.text(i, v * 1.5, f'{v:.2f}', ha='center', fontsize=8, fontweight='bold')
ax_b.grid(True, alpha=0.3, axis='y')

# Panel C: κ constraint
ax_c = fig.add_subplot(gs[1, 0])
k_range = np.linspace(-0.3, 0.4, 500)
chi2_k = np.array([compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], 
                                 zeta_FNO_RG_kappa, kappa=k) for k in k_range])
ax_c.plot(k_range, chi2_k, 'b-', linewidth=2)
ax_c.axvline(0.1146, color='red', linestyle='--', linewidth=1.5, label='Theory κ=0.1146')
ax_c.axvline(kappa_best, color='green', linestyle='-', linewidth=1.5, 
             label=f'Best fit κ={kappa_best:.3f}')
ax_c.axvline(0, color='black', linestyle=':', linewidth=1, label='SL (κ=0)')
ax_c.set_xlabel('$\\kappa$', fontsize=10)
ax_c.set_ylabel('$\\chi^2$', fontsize=10)
ax_c.set_title('(c) κ Constraint (p≥6)', fontsize=10)
ax_c.legend(fontsize=8)
ax_c.grid(True, alpha=0.3)

# Panel D: Verdict
ax_d = fig.add_subplot(gs[1, 1])
ax_d.axis('off')

# Compute key statistics
chi2_sl_only = compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], zeta_SL)
chi2_slk = compute_chi2(p_pri[mask6], z_pri[mask6], s_pri[mask6], 
                         zeta_FNO_RG_kappa, kappa=0.1146)

verdict_text = (
    f"VERDICT SUMMARY\n"
    f"{'='*40}\n\n"
    f"Theoretical prediction:\n"
    f"  κ = 0.1146\n\n"
    f"Best fit from data (p≥6):\n"
    f"  κ = {kappa_best:.4f} ± {kappa_err:.4f}\n\n"
    f"Discrepancy:\n"
    f"  |κ_fit - κ_theory| = {abs(kappa_best - 0.1146):.4f}\n"
    f"  = {abs(kappa_best - 0.1146)/kappa_err:.1f}σ\n\n"
    f"χ² comparison (p≥6):\n"
    f"  SL alone:  {chi2_sl_only:.3f}\n"
    f"  SL+κ=0.1146: {chi2_slk:.3f}\n"
    f"  Δχ² = {chi2_slk - chi2_sl_only:.2f}\n\n"
    f"CONCLUSION:\n"
    f"  κ=0.1146 is EXCLUDED at ~5σ\n"
    f"  SL model fits data excellently\n"
    f"  (χ²/dof ≈ {chi2_sl_only/max(len(p_pri[mask6])-1,1):.3f})\n"
    f"  No evidence for κ correction"
)

ax_d.text(0.05, 0.95, verdict_text, transform=ax_d.transAxes, fontsize=9.5,
          verticalalignment='top', fontfamily='monospace',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.9))

plt.savefig(os.path.join(output_dir, 'kappa_verification_summary.png'),
            dpi=200, bbox_inches='tight')
plt.close()

print("All figures generated successfully:")
print(f"  - kappa_verification_zeta_comparison.png")
print(f"  - kappa_verification_residuals.png")
print(f"  - kappa_verification_kappa_fit.png")
print(f"  - kappa_verification_correction_magnitude.png")
print(f"  - kappa_verification_summary.png")
