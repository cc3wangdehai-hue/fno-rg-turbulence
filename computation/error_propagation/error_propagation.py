#!/usr/bin/env python3
"""
FNO x RG Error Propagation Chain: Numerical Computation
=========================================================

Computes the error propagation chain:
    eps_FNO -> delta(lambda_k) -> delta(A2) -> delta(g*) -> delta(eta) -> delta(zeta_2)

Parameters:
    beta(g) = -eps_d * g + A1 * g^2 - A2 * g^3
    eps_d = 4 - d  (for 3D turbulence, eps_d ~ 1 effective)
    A1 = 0.200  (exact analytic value (d-1)/(2(d+2)), d=3)
    A2 ~ 0.002  (estimated, A2/A1^2 ~ 0.05)
    eps_FNO = 0.063  (FNO relative approximation error)
    g* ~ 5.3  (IR stable fixed point)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import sympy as sp

# ============================================================
# Section 0: Parameters
# ============================================================
d = 3
eps_d = 4 - d  # = 1
A1 = 0.200
A2 = 0.002
eps_FNO = 0.063
g_star = 5.3

print("=" * 70)
print("FNO x RG Error Propagation Chain - Numerical Results")
print("=" * 70)
print(f"\nParameters:")
print(f"  d = {d}, eps_d = {eps_d}")
print(f"  A1 = {A1}")
print(f"  A2 = {A2}")
print(f"  eps_FNO = {eps_FNO}")
print(f"  g* = {g_star}")

# ============================================================
# Section 1: Symbolic derivation of beta function properties
# ============================================================
g, eps_d_sym, A1_sym, A2_sym = sp.symbols('g eps_d A1 A2', positive=True)

beta = -eps_d_sym * g + A1_sym * g**2 - A2_sym * g**3
dbeta_dg = sp.diff(beta, g)

# Fixed point condition: beta(g*) = 0
# -eps_d*g* + A1*g*^2 - A2*g*^3 = 0
# g*(-eps_d + A1*g* - A2*g*^2) = 0
# Non-trivial: -eps_d + A1*g* - A2*g*^2 = 0
# => g* = (A1 +/- sqrt(A1^2 - 4*A2*eps_d)) / (2*A2)

print("\n" + "=" * 70)
print("PART 1: eps_FNO -> delta(lambda_k)")
print("=" * 70)

# FNO learns N(u) = -u * du/dx with relative error eps_FNO.
# The effective action Gamma_k has interaction vertices V_k ~ Fourier[N(u)].
# In derivative expansion, V_k maps to coupling lambda_k.
#
# Key argument:
#   The interaction term in the action is S_int = int lambda_k * V_k(u) dx dt
#   where V_k is determined from the nonlinear term N(u).
#   If N_FNO has relative error eps_FNO, then:
#     delta(V_k) / V_k ~ eps_FNO
#     delta(lambda_k) / lambda_k ~ eps_FNO
#
# This is because lambda_k and V_k are determined by matching the RG flow
# to the DNS data through the nonlinear term. The FNO error directly
# propagates as a multiplicative uncertainty on the coupling.

delta_lambda_over_lambda = eps_FNO
print(f"\n  FNO approximation error: eps_FNO = {eps_FNO}")
print(f"  => delta(lambda_k) / lambda_k ~ eps_FNO = {eps_FNO} = {eps_FNO*100:.1f}%")
print(f"\n  Physical reasoning:")
print(f"  - FNO learns N(u) = -u * du/dx with relative L2 error {eps_FNO}")
print(f"  - Effective action Gamma_k interaction vertex V_k ~ F[N(u)]")
print(f"  - In derivative expansion truncation: V_k -> coupling lambda_k")
print(f"  - Therefore: delta(lambda_k)/lambda_k ~ eps_FNO")

# ============================================================
# Section 2: delta(lambda_k) -> delta(A2)
# ============================================================
print("\n" + "=" * 70)
print("PART 2: delta(lambda_k) -> delta(beta(g)) -> delta(A2)")
print("=" * 70)

# A1 = (d-1)/(2(d+2)) = 2/10 = 0.2 is an exact analytic result from
# the one-loop RG calculation. It depends on geometric factors (d-1)/(d+2)
# from angular integration, NOT on the FNO-learned coupling.
# => delta(A1) = 0

# A2 arises from higher-loop corrections. In the two-loop calculation,
# A2 involves integrals over coupling-dependent vertices.
# The ratio A2/A1^2 ~ 0.05 is an estimate.
#
# The uncertainty in A2 comes from:
# (a) Truncation of derivative expansion (systematic, not FNO-related)
# (b) FNO error in the coupling constant
#
# For (b): A2 ~ c * lambda_k^2 / (16 pi^2) type loop factor
#   If lambda_k has error eps_FNO * lambda_k, then:
#   delta(A2) / A2 ~ 2 * delta(lambda_k) / lambda_k ~ 2 * eps_FNO
#   (factor of 2 because A2 involves lambda_k^2 in two-loop)
#
# However, we should be more careful. A2/A1^2 ~ 0.05 means A2 ~ 0.05 * A1^2.
# If A2 receives corrections at order lambda_k^2 from two-loop diagrams,
# and the coupling itself has O(eps_FNO) uncertainty, then:
#   delta(A2) ~ 2 * A2 * eps_FNO  (since A2 ~ lambda^2)
#
# But there's also a contribution from the fact that A2's estimate itself
# has uncertainty. The ratio A2/A1^2 = 0.05 +/- 0.02 (rough estimate).
# The FNO contribution to delta(A2) is the part due to eps_FNO.

# Conservative estimate: delta(A2) from FNO propagates through coupling
# A2 ~ lambda_k^2 * (loop factor), so delta(A2)/A2 ~ 2 * eps_FNO
delta_A2_from_FNO = 2 * A2 * eps_FNO

# There's also a systematic uncertainty from the estimate A2/A1^2 ~ 0.05
# Let's say this is ~40% relative (A2 could be 0.001-0.003)
A2_systematic = 0.4 * A2  # 40% systematic

# Total delta(A2) - combine in quadrature
delta_A2_total = np.sqrt(delta_A2_from_FNO**2 + A2_systematic**2)

print(f"\n  A1 = {A1} is exact analytic: (d-1)/(2(d+2)) = {(d-1)/(2*(d+2))}")
print(f"  => delta(A1) = 0")
print(f"\n  A2 = {A2} (estimated, A2/A1^2 = {A2/A1**2:.2f})")
print(f"\n  FNO contribution to delta(A2):")
print(f"    A2 ~ lambda_k^2 * (loop factor)")
print(f"    => delta(A2)/A2 ~ 2 * eps_FNO = {2*eps_FNO:.3f}")
print(f"    => delta(A2)_FNO = 2 * A2 * eps_FNO = {delta_A2_from_FNO:.6f}")
print(f"\n  Systematic uncertainty (truncation estimate):")
print(f"    A2/A1^2 = 0.05 +/- ~40%")
print(f"    => delta(A2)_syst = {A2_systematic:.6f}")
print(f"\n  Total delta(A2) (quadrature): {delta_A2_total:.6f}")
print(f"  Relative: {delta_A2_total/A2*100:.1f}%")

# ============================================================
# Section 3: delta(beta) -> delta(g*)
# ============================================================
print("\n" + "=" * 70)
print("PART 3: delta(A2) -> delta(g*)")
print("=" * 70)

# beta(g) = -eps_d*g + A1*g^2 - A2*g^3
# Fixed point: beta(g*) = 0
#   -eps_d + A1*g* - A2*g*^2 = 0
#   g* = (A1 - sqrt(A1^2 - 4*A2*eps_d)) / (2*A2)  [IR stable root]

# Verify g*
g_star_check = (A1 - np.sqrt(A1**2 - 4*A2*eps_d)) / (2*A2)
g_star_check_2 = (A1 + np.sqrt(A1**2 - 4*A2*eps_d)) / (2*A2)
print(f"\n  Fixed point equation: -eps_d + A1*g* - A2*g*^2 = 0")
print(f"  Roots: g*_1 = {g_star_check:.4f}, g*_2 = {g_star_check_2:.4f}")
print(f"  IR stable root (smaller): g* = {g_star_check:.4f}")
print(f"  Note: g* = 5.3 as given does NOT satisfy -eps_d + A1*g - A2*g^2 = 0")
print(f"        with eps_d=1, A1=0.2, A2=0.002")
print(f"        Check: beta(5.3) = {-eps_d*5.3 + A1*5.3**2 - A2*5.3**3:.4f}")

# The given g* = 5.3 doesn't satisfy the beta function exactly with these params.
# Let's compute the actual fixed point and also work with g* = 5.3 as specified.
# We'll compute errors for both cases.

# For the implicit function theorem approach, we use g* as given
beta_prime = -eps_d + 2*A1*g_star - 3*A2*g_star**2
print(f"\n  beta'(g*) = -eps_d + 2*A1*g* - 3*A2*g*^2")
print(f"           = {-eps_d} + {2*A1*g_star:.4f} - {3*A2*g_star**2:.4f}")
print(f"           = {beta_prime:.4f}")

# dg*/dA1 = g*^2 / (-beta'(g*))
# dg*/dA2 = -g*^3 / (-beta'(g*))
# delta(g*) = |dg*/dA1| * delta(A1) + |dg*/dA2| * delta(A2)

dg_dA1 = g_star**2 / (-beta_prime)
dg_dA2 = -g_star**3 / (-beta_prime)

print(f"\n  Implicit function theorem:")
print(f"    dg*/dA1 = g*^2 / (-beta'(g*)) = {g_star**2:.2f} / {-beta_prime:.4f} = {dg_dA1:.4f}")
print(f"    dg*/dA2 = -g*^3 / (-beta'(g*)) = -{g_star**3:.2f} / {-beta_prime:.4f} = {dg_dA2:.4f}")

# Contribution from delta(A1) = 0
delta_g_from_A1 = abs(dg_dA1) * 0  # delta(A1) = 0
# Contribution from delta(A2)
delta_g_from_A2_FNO = abs(dg_dA2) * delta_A2_from_FNO
delta_g_from_A2_syst = abs(dg_dA2) * A2_systematic
delta_g_from_A2_total = abs(dg_dA2) * delta_A2_total

# Total delta(g*)
delta_g_star_total = np.sqrt(delta_g_from_A1**2 + delta_g_from_A2_total**2)

print(f"\n  delta(g*) contributions:")
print(f"    From delta(A1)=0: {delta_g_from_A1:.6f}")
print(f"    From delta(A2)_FNO = {delta_A2_from_FNO:.6f}: {delta_g_from_A2_FNO:.6f}")
print(f"    From delta(A2)_syst = {A2_systematic:.6f}: {delta_g_from_A2_syst:.6f}")
print(f"    From delta(A2)_total = {delta_A2_total:.6f}: {delta_g_from_A2_total:.6f}")
print(f"\n  Total delta(g*) = {delta_g_star_total:.6f}")
print(f"  Relative: {delta_g_star_total/g_star*100:.2f}%")

# Also check with the actual fixed point
print(f"\n  --- Verification with actual fixed point g*_actual = {g_star_check:.4f} ---")
beta_prime_actual = -eps_d + 2*A1*g_star_check - 3*A2*g_star_check**2
dg_dA2_actual = -g_star_check**3 / (-beta_prime_actual)
delta_g_actual = abs(dg_dA2_actual) * delta_A2_total
print(f"  beta'(g*_actual) = {beta_prime_actual:.4f}")
print(f"  dg*/dA2 = {dg_dA2_actual:.4f}")
print(f"  delta(g*_actual) = {delta_g_actual:.6f} ({delta_g_actual/g_star_check*100:.2f}%)")

# ============================================================
# Section 4: delta(g*) -> delta(eta)
# ============================================================
print("\n" + "=" * 70)
print("PART 4: delta(g*) -> delta(eta)")
print("=" * 70)

# The anomalous dimension eta at the fixed point:
# eta = eta(g*) = c1 * g*^2 + c2 * g*^3 + ...
#
# For the FNO x RG framework applied to Navier-Stokes:
# The anomalous dimension of the velocity field is related to the
# energy spectrum exponent: E(k) ~ k^(-1-2*eta) or E(k) ~ k^(-5/3)
# for Kolmogorov.
#
# In the RG framework for turbulence (e.g., DeDominicis-Martin, Forster et al.):
# eta = -epsilon_d * g* / (something) at one-loop
# More precisely, for the NS equation in the dynamic RG:
#   eta_v = g* * f(eps_d) at one-loop
#
# We adopt a general parametrization:
#   eta = c1 * g*^2  (leading order, as typical in derivative expansion)
# where c1 is a scheme-dependent coefficient.
#
# For Kolmogorov spectrum E(k) ~ k^(-5/3):
#   The exponent zeta_2 = 2/3 for the second-order structure function
#   zeta_2 = 2 - eta (in some conventions)
#   => eta = 2 - 2/3 = 4/3 in some conventions
#
# But more commonly in the RG literature for turbulence:
#   eta relates to the renormalization of the coupling/viscosity
#   At one-loop: eta ~ g*^2 / (16 pi^2) * (geometric factor)
#
# Let's use a model-independent approach:
#   eta(g*) = alpha * g*^n  where n is the leading power
#
# For a generic anomalous dimension:
#   eta = c * g*^2 (one-loop result for many field theories)

# We'll compute for several common forms
c_coeffs = [0.01, 0.005, 0.001]  # plausible range for c
powers = [2, 3]

print(f"\n  Anomalous dimension: eta(g*) = c * g*^n")
print(f"  delta(eta) = |d(eta)/dg*| * delta(g*) = n * c * g*^(n-1) * delta(g*)")
print(f"  => delta(eta)/eta = n * delta(g*)/g*")
print(f"  => Relative error in eta = n * (delta(g*)/g*)")

print(f"\n  Results for different (c, n):")
print(f"  {'c':>8} {'n':>4} {'eta':>12} {'delta(eta)':>12} {'rel err':>10}")
print(f"  {'-'*50}")

eta_results = []
for c in c_coeffs:
    for n in powers:
        eta = c * g_star**n
        delta_eta = n * c * g_star**(n-1) * delta_g_star_total
        rel_err = delta_eta / eta * 100 if eta > 0 else 0
        eta_results.append((c, n, eta, delta_eta, rel_err))
        print(f"  {c:>8.3f} {n:>4d} {eta:>12.6f} {delta_eta:>12.6f} {rel_err:>9.2f}%")

# Key insight: relative error in eta is n * (delta(g*)/g*)
# independent of c!
rel_eta_generic = [n * delta_g_star_total / g_star * 100 for n in powers]
print(f"\n  KEY INSIGHT: Relative error in eta is INDEPENDENT of c:")
for n, re in zip(powers, rel_eta_generic):
    print(f"    n={n}: delta(eta)/eta = {n} * delta(g*)/g* = {re:.2f}%")

# ============================================================
# Section 5: delta(eta) -> delta(zeta_2)
# ============================================================
print("\n" + "=" * 70)
print("PART 5: delta(eta) -> delta(zeta_2) [scaling exponents]")
print("=" * 70)

# Structure function exponents zeta_p:
# In the RG framework: zeta_p = p * (1 - eta/2) or similar
# For Kolmogorov: zeta_2 = 2/3
#
# A common relation: zeta_2 = 2 - 2*eta (for velocity structure functions)
# or zeta_2 = 2/3 + correction proportional to eta
#
# Let's use: zeta_2 = 2/3 + a * eta  where a is a model-dependent constant
# At one-loop: a ~ -1 (decreasing zeta_2 from K41)
#
# Actually, more standard:
# The energy spectrum E(k) ~ k^(-(1+2*eta_v)) where eta_v is the
# anomalous dimension of the velocity field
# => E(k) ~ k^(-5/3) when 1+2*eta_v = 5/3, i.e. eta_v = 1/3
#
# zeta_2 from E(k): S_2(r) ~ r^(zeta_2), E(k) ~ k^(-(1+zeta_2))
# => 1 + zeta_2 = 1 + 2*eta_v => zeta_2 = 2*eta_v
#
# So delta(zeta_2) = 2 * delta(eta_v)
# => delta(zeta_2)/zeta_2 = delta(eta)/eta (same relative error)

# We'll present results for the case where zeta_2 ~ 2/3
zeta_2_K41 = 2/3

print(f"\n  Kolmogorov (K41): zeta_2 = 2/3 = {zeta_2_K41:.4f}")
print(f"  RG correction: zeta_2 = 2*eta_v")
print(f"  => delta(zeta_2) = 2 * delta(eta_v)")
print(f"  => delta(zeta_2)/zeta_2 = delta(eta)/eta (same relative error)")
print(f"\n  Using n=2 anomalous dimension model:")
c_ref, n_ref = 0.01, 2
eta_ref = c_ref * g_star**n_ref
delta_eta_ref = n_ref * c_ref * g_star**(n_ref-1) * delta_g_star_total
delta_zeta_2 = 2 * delta_eta_ref
zeta_2_ref = zeta_2_K41  # approximately
print(f"    delta(zeta_2) = {delta_zeta_2:.6f}")
print(f"    Relative: {delta_zeta_2/zeta_2_ref*100:.2f}%")

# ============================================================
# Section 6: Summary Table
# ============================================================
print("\n" + "=" * 70)
print("PART 6: SUMMARY TABLE")
print("=" * 70)

print(f"\n  {'Quantity':<25} {'Value':>12} {'Error Bound':>14} {'Rel Error':>12}")
print(f"  {'-'*65}")
print(f"  {'eps_FNO':<25} {eps_FNO:>12.4f} {'---':>14} {'---':>12}")
print(f"  {'delta(lambda_k)/lambda_k':<25} {'---':>12} {eps_FNO:>14.4f} {eps_FNO*100:>11.1f}%")
print(f"  {'delta(A1)':<25} {0:>12.6f} {0:>14.6f} {'0.0':>11}%")
print(f"  {'A2 (central)':<25} {A2:>12.6f} {'---':>14} {'---':>12}")
print(f"  {'  FNO component':<25} {'---':>12} {delta_A2_from_FNO:>14.6f} {delta_A2_from_FNO/A2*100:>11.1f}%")
print(f"  {'  Systematic':<25} {'---':>12} {A2_systematic:>14.6f} {A2_systematic/A2*100:>11.1f}%")
print(f"  {'  Total':<25} {'---':>12} {delta_A2_total:>14.6f} {delta_A2_total/A2*100:>11.1f}%")
print(f"  {'g* (central)':<25} {g_star:>12.4f} {'---':>14} {'---':>12}")
print(f"  {'  delta(g*) total':<25} {'---':>12} {delta_g_star_total:>14.6f} {delta_g_star_total/g_star*100:>11.2f}%")
print(f"  {'eta (n=2, c=0.01)':<25} {eta_ref:>12.6f} {delta_eta_ref:>14.6f} {delta_eta_ref/eta_ref*100:>11.2f}%")
print(f"  {'zeta_2':<25} {zeta_2_ref:>12.4f} {delta_zeta_2:>14.6f} {delta_zeta_2/zeta_2_ref*100:>11.2f}%")

# ============================================================
# Section 7: Additional analysis - which epsilon_d is consistent with g*=5.3?
# ============================================================
print("\n" + "=" * 70)
print("ADDITIONAL: Consistency check for g* = 5.3")
print("=" * 70)

# beta(g*) = 0: -eps_d*g* + A1*g*^2 - A2*g*^3 = 0
# => eps_d = A1*g* - A2*g*^2 = A1 - A2*g* (dividing by g*)
# Actually: eps_d*g* = A1*g*^2 - A2*g*^3 => eps_d = A1*g* - A2*g*^2
eps_d_required = A1*g_star - A2*g_star**2
print(f"\n  For beta(g*=5.3) = 0, need eps_d = A1*g* - A2*g*^2 = {eps_d_required:.4f}")
print(f"  (With d=3, eps_d = 4-3 = 1, but effective eps_d may differ)")
print(f"  This suggests eps_d_eff ~ {eps_d_required:.2f} for g*=5.3")

# Recompute with this effective eps_d
eps_d_eff = eps_d_required
beta_prime_eff = -eps_d_eff + 2*A1*g_star - 3*A2*g_star**2
dg_dA2_eff = -g_star**3 / (-beta_prime_eff)
delta_g_eff = abs(dg_dA2_eff) * delta_A2_total

print(f"\n  With eps_d_eff = {eps_d_eff:.4f}:")
print(f"    beta'(g*) = {beta_prime_eff:.4f}")
print(f"    delta(g*) = {delta_g_eff:.6f} ({delta_g_eff/g_star*100:.2f}%)")

# ============================================================
# Section 8: Visualization
# ============================================================
print("\n" + "=" * 70)
print("Generating visualization...")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# --- Left: Sankey-style error propagation flow ---
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Error Propagation Chain', fontsize=14, fontweight='bold', pad=20)

# Define nodes
nodes = [
    (0.5, 8.5, f'eps_FNO = {eps_FNO}', '#4ECDC4'),
    (0.5, 6.5, f'delta(lambda_k)/lambda_k\n= {delta_lambda_over_lambda*100:.1f}%', '#45B7D1'),
    (0.5, 4.5, f'delta(A2) = {delta_A2_total:.5f}\n(rel: {delta_A2_total/A2*100:.1f}%)', '#96CEB4'),
    (0.5, 2.5, f'delta(g*) = {delta_g_star_total:.4f}\n(rel: {delta_g_star_total/g_star*100:.2f}%)', '#FFEAA7'),
    (0.5, 0.5, f'delta(zeta_2) = {delta_zeta_2:.5f}\n(rel: {delta_zeta_2/zeta_2_ref*100:.2f}%)', '#DDA0DD'),
]

# Draw nodes
for (x, y, text, color) in nodes:
    bbox = FancyBboxPatch((x, y-0.5), 4.0, 1.2, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.8)
    ax.add_patch(bbox)
    ax.text(x+2.0, y+0.1, text, ha='center', va='center', fontsize=8.5, fontweight='bold')

# Draw arrows between nodes
for i in range(len(nodes)-1):
    y1 = nodes[i][1] - 0.5
    y2 = nodes[i+1][1] + 0.7
    ax.annotate('', xy=(2.5, y2), xytext=(2.5, y1),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2.5))

# Add annotations on the right side
annotations = [
    (6.0, 8.5, 'FNO approximation\nerror on N(u)', '#666'),
    (6.0, 6.5, 'Coupling constant\ninherits full FNO error', '#666'),
    (6.0, 4.5, 'A1 exact; A2 gets\n2x amplification + systematic', '#666'),
    (6.0, 2.5, 'Error dampened by\n|beta\'(g*)| denominator', '#666'),
    (6.0, 0.5, 'Linear propagation;\nrelative error preserved', '#666'),
]

for (x, y, text, color) in annotations:
    ax.text(x, y, text, fontsize=7.5, color=color, style='italic', va='center')
    ax.annotate('', xy=(x-0.1, y), xytext=(4.7, y),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1, ls='--'))

# --- Right: Bar chart of relative errors ---
ax2 = axes[1]
labels = ['eps_FNO', 'dlambda/lambda', 'dA2/A2\n(total)', 'dg*/g*\n(eps_d=1)', 'dg*/g*\n(eps_d=eff)',
           'deta/eta\n(n=2)', 'dzeta2/zeta2']
values = [eps_FNO*100, delta_lambda_over_lambda*100, delta_A2_total/A2*100,
          delta_g_star_total/g_star*100, delta_g_eff/g_star*100,
          n_ref*delta_g_star_total/g_star*100, n_ref*delta_g_star_total/g_star*100]
colors = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#F7DC6F', '#DDA0DD', '#BB8FCE']

bars = ax2.barh(range(len(labels)), values, color=colors, edgecolor='black', linewidth=0.8, alpha=0.85)
ax2.set_yticks(range(len(labels)))
ax2.set_yticklabels(labels, fontsize=9)
ax2.set_xlabel('Relative Error (%)', fontsize=11)
ax2.set_title('Error Magnification at Each Stage', fontsize=14, fontweight='bold')
ax2.invert_yaxis()

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, values)):
    ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', va='center', fontsize=8.5, fontweight='bold')

ax2.set_xlim(0, max(values) * 1.25)

plt.tight_layout()
plt.savefig('/app/data/所有对话/主对话/Error_Propagation_Chain/error_propagation.png', dpi=150, bbox_inches='tight')
print("  Saved: error_propagation.png")

# ============================================================
# Section 9: Save detailed data for report
# ============================================================
results = {
    'parameters': {
        'd': d, 'eps_d': eps_d, 'A1': A1, 'A2': A2,
        'eps_FNO': eps_FNO, 'g_star': g_star,
        'eps_d_eff': eps_d_required,
    },
    'propagation': {
        'delta_lambda_over_lambda': delta_lambda_over_lambda,
        'delta_A1': 0,
        'delta_A2_FNO': delta_A2_from_FNO,
        'delta_A2_systematic': A2_systematic,
        'delta_A2_total': delta_A2_total,
        'beta_prime': beta_prime,
        'dg_dA2': dg_dA2,
        'delta_g_star_FNO': delta_g_from_A2_FNO,
        'delta_g_star_total': delta_g_star_total,
        'delta_g_star_eff': delta_g_eff,
    },
    'exponents': {
        'eta_ref': eta_ref,
        'delta_eta_ref': delta_eta_ref,
        'zeta_2_K41': zeta_2_K41,
        'delta_zeta_2': delta_zeta_2,
    }
}

# Save results as text for report generation
with open('/app/data/所有对话/主对话/Error_Propagation_Chain/computed_values.txt', 'w') as f:
    import json
    json.dump(results, f, indent=2)

print("\n  All computations complete.")
print(f"  Computed values saved to computed_values.txt")
