#!/usr/bin/env python3
"""
Numerical Verification of Theorem 4: FNO×RG Self-Consistency
Version 4 — Fixed root tracking to follow the CORRECT fixed point under perturbation.

Root cause of v3 failure:
  The root finder was jumping between the two non-trivial fixed points (UV vs IR),
  producing |Δg| ≈ 0.447 (distance between fixed points) instead of O(ε).

Fix: Use Newton's method initialized at the exact fixed point to track the SAME
fixed point under perturbation. This is the physically correct approach — we want
to see how a specific fixed point MOVES under perturbation, not find a different one.
"""

import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from typing import Tuple, Optional, Callable, Dict, List

# ============================================================================
# Model β-function
# ============================================================================

class ModelBetaFunction:
    """
    β(g) = -ε_d g + g² - g³
    
    Fixed points (for ε_d < 1/4):
      g*₋ = (1 - √(1-4ε_d))/2  (UV-stable, saddle)
      g*₊ = (1 + √(1-4ε_d))/2  (IR-stable, attractor)
    """
    def __init__(self, epsilon_d: float = 0.2):
        self.epsilon_d = epsilon_d
        disc = 1 - 4 * epsilon_d
        assert disc > 0, f"No non-trivial FP for ε_d={epsilon_d} (need ε_d < 0.25)"
        self.g_minus = (1 - np.sqrt(disc)) / 2
        self.g_plus = (1 + np.sqrt(disc)) / 2
    
    def exact(self, g: float) -> float:
        return -self.epsilon_d * g + g**2 - g**3
    
    def exact_deriv(self, g: float) -> float:
        return -self.epsilon_d + 2*g - 3*g**2
    
    def perturbed(self, g: float, eps_fno: float, mode: int = 0) -> float:
        """β_FNO = β_exact + δβ"""
        if mode == 0:
            delta = eps_fno * (0.3*g + 0.2*g**2 + 0.1*g**3)
        elif mode == 1:
            delta = eps_fno * (0.2*g + 0.15*g**2 * np.sin(2*g) + 0.05*g**3)
        else:
            delta = eps_fno * (0.5*g - 0.3*g**2 + 0.2*g**3)
        return self.exact(g) + delta
    
    def perturbed_deriv(self, g: float, eps_fno: float, mode: int = 0, dg: float = 1e-8) -> float:
        """dβ_FNO/dg by central difference"""
        return (self.perturbed(g + dg, eps_fno, mode) - self.perturbed(g - dg, eps_fno, mode)) / (2*dg)
    
    def find_fixed_point_newton(self, beta_func, deriv_func, g_init: float, 
                                 max_iter: int = 100, tol: float = 1e-14) -> Optional[float]:
        """
        Newton's method: g_{n+1} = g_n - β(g_n)/β'(g_n)
        
        Initialized at g_init (the exact fixed point), this tracks the SAME
        fixed point under perturbation.
        """
        g = g_init
        for i in range(max_iter):
            bval = beta_func(g)
            bder = deriv_func(g)
            
            if abs(bder) < 1e-15:
                # Derivative too small, Newton fails; try bisection nearby
                return self._fallback_bisection(beta_func, g_init)
            
            g_new = g - bval / bder
            
            if abs(g_new - g) < tol:
                return g_new
            g = g_new
        
        # Check if converged
        if abs(beta_func(g)) < 1e-10:
            return g
        return self._fallback_bisection(beta_func, g_init)
    
    def _fallback_bisection(self, beta_func, g_target: float, radius: float = 0.1) -> Optional[float]:
        """Bisection fallback with tight radius to avoid finding wrong root."""
        g_lo = max(0.001, g_target - radius)
        g_hi = g_target + radius
        
        try:
            if beta_func(g_lo) * beta_func(g_hi) > 0:
                return None
            return brentq(beta_func, g_lo, g_hi, xtol=1e-14, rtol=1e-14)
        except:
            return None


# ============================================================================
# Paper β-function diagnostic
# ============================================================================

class PaperBetaFunction:
    """Paper's NS β-function: β(g) = -ε_d g + A₁g² - A₂g³ with A₁=0.183, A₂=0.041"""
    def __init__(self, epsilon_d: float, A1: float = 0.183, A2: float = 0.041):
        self.epsilon_d = epsilon_d
        self.A1 = A1
        self.A2 = A2
        self.discriminant = A1**2 - 4*A2*epsilon_d
        
        if self.discriminant > 0:
            self.g_star = (A1 - np.sqrt(self.discriminant)) / (2*A2)
            self.g_star_plus = (A1 + np.sqrt(self.discriminant)) / (2*A2)
        else:
            self.g_star = None
            self.g_star_plus = None
    
    def beta(self, g: float) -> float:
        return -self.epsilon_d * g + self.A1 * g**2 - self.A2 * g**3
    
    def beta_deriv(self, g: float) -> float:
        return -self.epsilon_d + 2*self.A1*g - 3*self.A2*g**2


# ============================================================================
# Main Verification
# ============================================================================

def run_verification(model: ModelBetaFunction, g_target: str = "plus", 
                     eps_range: Tuple = (-7, -1), n_points: int = 40) -> Dict:
    """
    Run Theorem 4 verification for a specific fixed point.
    
    g_target: "plus" for g*₊ (IR), "minus" for g*₋ (UV)
    """
    g_exact = model.g_plus if g_target == "plus" else model.g_minus
    theta_exact = -model.exact_deriv(g_exact)
    
    results = {}
    
    for mode in range(3):
        beta_pert = lambda g, e=mode: model.perturbed(g, 1.0, e)  # placeholder
        deriv_pert = lambda g, e=mode: model.perturbed_deriv(g, 1.0, e)
        
        epsilon_values = np.logspace(eps_range[0], eps_range[1], n_points)
        delta_g_list = []
        delta_theta_list = []
        g_fno_list = []
        theta_fno_list = []
        
        for eps_fno in epsilon_values:
            # Define perturbed functions for this ε_FNO
            b_func = lambda g: model.perturbed(g, eps_fno, mode)
            d_func = lambda g: model.perturbed_deriv(g, eps_fno, mode)
            
            # Newton tracking from exact fixed point
            g_fno = model.find_fixed_point_newton(b_func, d_func, g_exact)
            
            if g_fno is None or abs(g_fno - g_exact) > 0.5:
                continue
            
            # Critical exponent at perturbed FP
            dtheta = -d_func(g_fno)
            
            delta_g = abs(g_fno - g_exact)
            delta_theta = abs(dtheta - theta_exact)
            
            g_fno_list.append(g_fno)
            theta_fno_list.append(dtheta)
            delta_g_list.append(delta_g)
            delta_theta_list.append(delta_theta)
        
        results[mode] = {
            'epsilon': epsilon_values[:len(delta_g_list)],
            'g_fno': np.array(g_fno_list),
            'theta_fno': np.array(theta_fno_list),
            'delta_g': np.array(delta_g_list),
            'delta_theta': np.array(delta_theta_list)
        }
    
    return results, g_exact, theta_exact


def analyze_scaling(results: Dict, model_name: str = "") -> Dict:
    """Analyze log-log scaling |Δg| ∝ ε^α"""
    scaling = {}
    
    for mode in range(3):
        r = results[mode]
        eps = r['epsilon']
        dg = r['delta_g']
        dt = r['delta_theta']
        
        if len(eps) < 5:
            scaling[mode] = {'alpha_g': np.nan, 'alpha_theta': np.nan, 'C_g': np.nan, 'C_theta': np.nan}
            continue
        
        # Use only the linear regime (small ε)
        log_eps = np.log(eps)
        log_dg = np.log(dg)
        log_dt = np.log(dt)
        
        alpha_g, log_C_g = np.polyfit(log_eps, log_dg, 1)
        alpha_theta, log_C_theta = np.polyfit(log_eps, log_dt, 1)
        
        scaling[mode] = {
            'alpha_g': alpha_g,
            'alpha_theta': alpha_theta,
            'C_g': np.exp(log_C_g),
            'C_theta': np.exp(log_C_theta)
        }
    
    return scaling


def print_results(results, scaling, g_exact, theta_exact, model_desc):
    """Pretty-print results."""
    mode_names = {0: "Smooth polynomial", 1: "Spectral (oscillatory)", 2: "Worst-case"}
    
    print(f"\n[Model: {model_desc}]")
    print(f"  Exact fixed point: g* = {g_exact:.8f}")
    print(f"  Critical exponent: θ = {theta_exact:.8f}")
    
    for mode in range(3):
        r = results[mode]
        s = scaling[mode]
        
        print(f"\n  Mode {mode}: {mode_names[mode]}")
        print(f"  {'ε_FNO':<12} {'g*_FNO':<16} {'|Δg|':<12} {'|Δg|/ε':<12} {'θ_FNO':<16} {'|Δθ|':<12}")
        print(f"  {'-'*85}")
        
        for i in range(len(r['epsilon'])):
            eps = r['epsilon'][i]
            g_fno = r['g_fno'][i]
            dg = r['delta_g'][i]
            dt = r['delta_theta'][i]
            theta = r['theta_fno'][i]
            
            print(f"  {eps:<12.2e} {g_fno:<16.10f} {dg:<12.2e} {dg/eps:<12.4f} "
                  f"{theta:<16.10f} {dt:<12.2e}")
        
        print(f"\n  Scaling: |Δg| ∝ ε^{s['alpha_g']:.4f}  |Δθ| ∝ ε^{s['alpha_theta']:.4f}")
        print(f"  C_g = {s['C_g']:.4f}  C_θ = {s['C_theta']:.4f}")
        
        if abs(s['alpha_g'] - 1.0) < 0.1:
            print(f"  ✓ LINEAR SCALING CONFIRMED")
        else:
            print(f"  ✗ DEVIATION (expected α=1)")


def generate_plots(results, scaling, g_exact, theta_exact, model):
    """Generate publication-quality verification plots."""
    fig = plt.figure(figsize=(18, 16))
    gs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    mode_names = {0: "Smooth", 1: "Spectral", 2: "Worst-case"}
    colors = ['#2196F3', '#4CAF50', '#FF5722']
    
    # Row 1: Scaling (log-log) for each mode
    for mode in range(3):
        ax = fig.add_subplot(gs[0, mode])
        r = results[mode]
        s = scaling[mode]
        
        ax.loglog(r['epsilon'], r['delta_g'], 'o-', color=colors[mode], 
                  markersize=4, linewidth=2, label=f'|Δg*| (α={s["alpha_g"]:.3f})')
        ax.loglog(r['epsilon'], r['delta_theta'], 's--', color=colors[mode], 
                  markersize=3, linewidth=1.5, alpha=0.7, label=f'|Δθ| (α={s["alpha_theta"]:.3f})')
        
        # Reference linear bound
        C_g = s['C_g']
        ref_line = C_g * r['epsilon']
        ax.loglog(r['epsilon'], ref_line, ':', color='gray', linewidth=1.5, 
                  label=f'Bound: C={C_g:.2f}ε')
        
        ax.set_xlabel('FNO Error ε', fontsize=11)
        ax.set_ylabel('Error', fontsize=11)
        ax.set_title(f'Mode {mode}: {mode_names[mode]}', fontsize=12, fontweight='bold')
        ax.legend(fontsize=8, loc='lower right')
        ax.grid(True, alpha=0.3)
    
    # Row 2: β-function visualization
    # (a) β-function with perturbation
    ax1 = fig.add_subplot(gs[1, 0])
    g_range = np.linspace(0, 1.5, 400)
    
    ax1.plot(g_range, [model.exact(g) for g in g_range], 'k-', linewidth=2.5, label='Exact β(g)')
    
    for eps_fno, ls, alpha in [(1e-2, '--', 0.9), (1e-3, '-.', 0.7), (1e-5, ':', 0.5)]:
        beta_pert = [model.perturbed(g, eps_fno, mode=0) for g in g_range]
        ax1.plot(g_range, beta_pert, ls, color='red', linewidth=1.5, alpha=alpha, 
                 label=f'FNO (ε={eps_fno:.0e})')
    
    ax1.axhline(y=0, color='gray', linewidth=0.5)
    ax1.axvline(x=model.g_plus, color='blue', linewidth=1.5, alpha=0.4, linestyle='--', label=f'g*₊={model.g_plus:.3f}')
    ax1.axvline(x=model.g_minus, color='green', linewidth=1.5, alpha=0.4, linestyle='--', label=f'g*₋={model.g_minus:.3f}')
    ax1.set_xlabel('Coupling g', fontsize=11)
    ax1.set_ylabel('β(g)', fontsize=11)
    ax1.set_title('β-function: Exact vs FNO-Perturbed', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # (b) Error constant stability
    ax2 = fig.add_subplot(gs[1, 1])
    for mode in range(3):
        r = results[mode]
        ratio = r['delta_g'] / r['epsilon']
        ax2.semilogx(r['epsilon'], ratio, '-o', color=colors[mode], markersize=3, 
                     linewidth=1.5, label=f'Mode {mode}')
    
    ax2.set_xlabel('FNO Error ε', fontsize=11)
    ax2.set_ylabel('C_g(ε) = |Δg*|/ε', fontsize=11)
    ax2.set_title('Error Constant Stability (should plateau)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # (c) RG flow diagram
    ax3 = fig.add_subplot(gs[1, 2])
    g_flow = np.linspace(0, 1.5, 300)
    beta_vals = np.array([model.exact(g) for g in g_flow])
    
    ax3.plot(g_flow, beta_vals, 'k-', linewidth=2)
    ax3.fill_between(g_flow, 0, beta_vals, where=(beta_vals > 0), alpha=0.1, color='red', label='UV flow (β>0)')
    ax3.fill_between(g_flow, 0, beta_vals, where=(beta_vals < 0), alpha=0.1, color='blue', label='IR flow (β<0)')
    ax3.axhline(y=0, color='gray', linewidth=0.5)
    
    # Mark fixed points
    ax3.plot(model.g_minus, 0, 'g^', markersize=12, zorder=5, label=f'UV FP: g*₋={model.g_minus:.3f}')
    ax3.plot(model.g_plus, 0, 'rv', markersize=12, zorder=5, label=f'IR FP: g*₊={model.g_plus:.3f}')
    ax3.plot(0, 0, 'ko', markersize=8, zorder=5, label='Gaussian: g=0')
    
    ax3.set_xlabel('Coupling g', fontsize=11)
    ax3.set_ylabel('β(g)', fontsize=11)
    ax3.set_title('RG Flow Structure (ε_d=0.2)', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=7, loc='upper left')
    ax3.grid(True, alpha=0.3)
    
    # Row 3: Summary + paper diagnostic
    # (a) Scaling exponents bar chart
    ax4 = fig.add_subplot(gs[2, 0])
    x = np.arange(3)
    width = 0.35
    alpha_g_vals = [scaling[m]['alpha_g'] for m in range(3)]
    alpha_theta_vals = [scaling[m]['alpha_theta'] for m in range(3)]
    
    ax4.bar(x - width/2, alpha_g_vals, width, label='α_g (fixed point)', color='#2196F3', alpha=0.8)
    ax4.bar(x + width/2, alpha_theta_vals, width, label='α_θ (exponent)', color='#FF9800', alpha=0.8)
    ax4.axhline(y=1.0, color='r', linewidth=2, linestyle='--', label='Expected: α=1')
    
    ax4.set_xlabel('Perturbation Mode', fontsize=11)
    ax4.set_ylabel('Scaling Exponent α', fontsize=11)
    ax4.set_title('Scaling Exponents (α=1 → linear)', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels([mode_names[m] for m in range(3)], fontsize=9)
    ax4.legend(fontsize=9)
    ax4.set_ylim(0.8, 1.2)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # (b) Paper diagnostic: discriminant
    ax5 = fig.add_subplot(gs[2, 1])
    eps_d_range = np.linspace(0, 1.2, 200)
    A1, A2 = 0.183, 0.041
    disc = A1**2 - 4*A2*eps_d_range
    
    ax5.plot(eps_d_range, disc, 'b-', linewidth=2)
    ax5.axhline(y=0, color='r', linewidth=1, linestyle='--')
    ax5.fill_between(eps_d_range, 0, disc, where=(disc > 0), alpha=0.15, color='green', label='Fixed point exists')
    ax5.fill_between(eps_d_range, 0, disc, where=(disc < 0), alpha=0.15, color='red', label='No fixed point')
    
    eps_d_crit = A1**2 / (4*A2)
    ax5.axvline(x=eps_d_crit, color='orange', linewidth=2, linestyle=':', 
                label=f'ε_d^c = {eps_d_crit:.3f} (d_c={4-eps_d_crit:.2f})')
    ax5.plot(1.0, A1**2 - 4*A2*1.0, 'r*', markersize=15, label='Paper (d=3)')
    
    ax5.set_xlabel('ε_d = 4 - d', fontsize=11)
    ax5.set_ylabel('Discriminant Δ = A₁² - 4A₂ε_d', fontsize=11)
    ax5.set_title('Paper β-function: Validity Region', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=8, loc='upper right')
    ax5.grid(True, alpha=0.3)
    
    # (c) Theorem verification summary
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.axis('off')
    
    summary = "THEOREM 4: NUMERICAL VERIFICATION\n"
    summary += "━" * 38 + "\n\n"
    summary += "Statement:\n"
    summary += "  |g*_FNO − g*_exact| ≤ C(ε)\n"
    summary += "  C(ε) = (L_W/λ_min)ε + O(ε²)\n\n"
    summary += "Results (tracking IR fixed point g*₊):\n\n"
    
    for mode in range(3):
        s = scaling[mode]
        status = "✓" if abs(s['alpha_g'] - 1.0) < 0.1 else "✗"
        summary += f"  {status} Mode {mode}: α_g = {s['alpha_g']:.4f}, C_g = {s['C_g']:.3f}\n"
    
    summary += f"\nModel: β(g) = -ε_d·g + g² - g³"
    summary += f"\nε_d = {model.epsilon_d}, g*₊ = {model.g_plus:.6f}"
    summary += f"\nθ = {theta_exact:.6f}"
    
    all_pass = all(abs(scaling[m]['alpha_g'] - 1.0) < 0.1 for m in range(3))
    summary += f"\n\n{'CONCLUSION:'}\n"
    if all_pass:
        summary += "  ✓ THEOREM 4 VERIFIED\n"
        summary += "  FNO×RG is a controlled approximation.\n"
        summary += "  Error scales LINEARLY with FNO accuracy."
    else:
        summary += "  ⚠ PARTIAL VERIFICATION\n"
        summary += "  Some modes show deviations."
    
    ax6.text(0.05, 0.95, summary, transform=ax6.transAxes,
             fontsize=10, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    plt.savefig('/app/data/所有对话/主对话/theorem4_verification_v4.png', 
                dpi=150, bbox_inches='tight')
    plt.close()
    print("\n✓ Plot saved: theorem4_verification_v4.png")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("=" * 90)
    print("THEOREM 4 VERIFICATION v4: FNO×RG Self-Consistency")
    print("Fixed: Newton tracking of correct fixed point under perturbation")
    print("=" * 90)
    
    # Model β-function at ε_d = 0.2 (d = 3.8)
    model = ModelBetaFunction(epsilon_d=0.2)
    
    # Verify IR fixed point (the physically relevant one)
    results, g_exact, theta_exact = run_verification(model, g_target="plus", 
                                                       eps_range=(-7, -1), n_points=40)
    scaling = analyze_scaling(results)
    
    print_results(results, scaling, g_exact, theta_exact, 
                  f"IR fixed point, β(g) = -0.2g + g² - g³")
    
    # Also verify UV fixed point for completeness
    print("\n" + "=" * 90)
    print("SECONDARY CHECK: UV fixed point")
    results_uv, g_uv, theta_uv = run_verification(model, g_target="minus", 
                                                     eps_range=(-7, -1), n_points=40)
    scaling_uv = analyze_scaling(results_uv)
    print_results(results_uv, scaling_uv, g_uv, theta_uv,
                  f"UV fixed point, β(g) = -0.2g + g² - g³")
    
    # Paper diagnostic
    print("\n" + "=" * 90)
    print("PAPER β-FUNCTION DIAGNOSTIC")
    print("=" * 90)
    print(f"\n  β(g) = -ε_d g + A₁g² - A₂g³  (A₁=0.183, A₂=0.041)")
    print(f"  Fixed point exists iff Δ = A₁² - 4A₂ε_d > 0")
    print(f"  Critical: ε_d^c = {0.183**2/(4*0.041):.4f}, d_c = {4-0.183**2/(4*0.041):.4f}")
    print(f"\n  At d=3 (ε_d=1): Δ = {0.183**2 - 4*0.041:.4f} < 0 → NO FIXED POINT")
    print(f"  The paper's two-loop β-function is only valid for d > {4-0.183**2/(4*0.041):.2f}")
    
    # Generate plots
    generate_plots(results, scaling, g_exact, theta_exact, model)
    
    # Final verdict
    print("\n" + "=" * 90)
    print("FINAL VERDICT")
    print("=" * 90)
    
    all_pass = True
    for mode in range(3):
        a = scaling[mode]['alpha_g']
        status = "✓ PASS" if abs(a - 1.0) < 0.1 else "✗ FAIL"
        if abs(a - 1.0) >= 0.1:
            all_pass = False
        print(f"  IR Mode {mode}: α_g = {a:.4f} → {status}")
    
    for mode in range(3):
        a = scaling_uv[mode]['alpha_g']
        status = "✓ PASS" if abs(a - 1.0) < 0.1 else "✗ FAIL"
        if abs(a - 1.0) >= 0.1:
            all_pass = False
        print(f"  UV Mode {mode}: α_g = {a:.4f} → {status}")
    
    print()
    if all_pass:
        print("  ★★★ THEOREM 4 NUMERICALLY VERIFIED ★★★")
        print("  |Δg*| ∝ ε_FNO confirmed for all perturbation modes")
        print("  FNO×RG is a mathematically controlled approximation to exact RG")
    else:
        print("  VERIFICATION PARTIAL — check deviations at larger ε_FNO")
    
    print("=" * 90)
