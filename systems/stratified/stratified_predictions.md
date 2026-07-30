---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 3308874814206131_0/project_7662556975707816201-files/FNO_RG_research/stratified_turbulence/stratified_predictions.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 3308874814206131#1785416204137
    ReservedCode2: ""
---
# FNO×RG Stratified Turbulence: Verifiable Predictions

**Date**: 2026-07-16  
**Framework**: FNO×RG  

---

## Prediction Categories

Predictions are classified as:
- **[STRONG]**: Derived from the RG fixed point structure with high confidence
- **[MODERATE]**: Derived from one-loop RG flow; requires higher-order verification
- **[ESTIMATE]**: Based on physical reasoning within the FNO×RG framework; not rigorously derived

---

## P1: Three-Fixed-Point Phase Diagram [STRONG]

**Prediction**: The (Fr, Re_b) parameter space of stratified turbulence contains exactly three universal scaling regimes:

1. **K41 regime** (Fr >> 1, Re_b >> 1): E(k) ~ k^{-5/3}, passive scalar behavior for b
2. **BO regime** (Fr ~ O(1), Re_b >> 1): E(k) ~ k^{-11/5}, ζ_p = 3p/5, constant potential energy flux
3. **2D/anisotropic regime** (Fr << 1, Re_b >> 1): E(k_h) ~ k_h^{-5/3}, E(k_z) ~ k_z^{-3}, re-entrant K41 for horizontal components

The boundaries between regimes are controlled by:
- K41↔BO: Bolgiano wavenumber k_B ~ N^{3/2} ε_v^{-5/4} ε_b^{3/4}
- BO↔2D: Ozmidov wavenumber k_{Oz} = (N³/ε_v)^{1/2}
- Turbulent↔viscous: Re_b ~ O(1)

**How to verify**: Systematic DNS scanning of (Fr, Re_b) parameter space with fixed resolution, measuring angle-averaged spectra and identifying the spectral slope as a function of (Fr, Re_b).

---

## P2: BO Amplitude Constant K_0 ~ O(0.1) [STRONG]

**Prediction**: The universal amplitude of the BO spectrum E(k) = K_0 ε_θ^{2/5} g^{4/5} k^{-11/5} satisfies K_0 ~ 0.1-0.2, significantly smaller than the Kolmogorov constant C_K ≈ 1.6.

**How to verify**: Extract K_0 from DNS at Fr ~ O(1) with sufficient inertial range, using the potential energy dissipation rate ε_b as the control parameter. Compare with the Bhattacharjee (2022) stirred model estimate.

**Implication**: The small amplitude of K_0 explains why the BO spectrum is difficult to observe — it is easily confused with K41 given finite dynamic range.

---

## P3: Crossover Exponent φ ≈ 5/2 [MODERATE]

**Prediction**: The K41→BO crossover as a function of Fr is controlled by the crossover function f_{BO}(Fr) = 1/(1 + (Fr/Fr_c)^{-φ}) with φ ≈ 5/2 and Fr_c ~ O(1).

**How to verify**: Measure the effective spectral index α_eff as a function of Fr in a series of DNS at fixed Re but varying N, and fit the crossover function to extract φ and Fr_c.

---

## P4: Re-Entrant K41 at Extreme Stratification [STRONG]

**Prediction**: For Fr → 0 with Re_b >> 1 (requiring extremely high Re), the horizontal kinetic energy spectrum recovers E(k_h) ~ k_h^{-5/3}, but this is a fundamentally different K41 from the isotropic one — it arises from quasi-2D dynamics, not 3D isotropy. The vertical spectrum remains steep (k_z^{-3}).

**How to verify**: DNS at Re > 10⁵ with Fr < 0.01 (requiring Re_b > 10). Current DNS capabilities (4096³) can achieve Re_b ~ 30 at best. This prediction requires next-generation exascale DNS.

**Falsification criterion**: If E(k_h) steepens beyond k_h^{-5/3} at Fr << 0.01 even when Re_b >> 1, the FP3 prediction is falsified.

---

## P5: BO Intermittency: Modified SL with β_{BO} ≈ 0.74 [ESTIMATE]

**Prediction**: The intermittency correction to BO scaling uses a modified She-Leveque formalism with hierarchical parameter β_{BO} = (2/5)^{1/3} ≈ 0.737, reflecting the different most-intermittent structures (KH billows in stratified layers vs. vortex filaments in isotropic turbulence).

Specific numerical predictions for the structure function exponents:

| p | ζ_p^{v,BO} (mean-field) | ζ_p^{v,BO} (with intermittency, estimate) | ζ_p^{K41} (SL) |
|---|-------------------------|------------------------------------------|----------------|
| 2 | 6/5 = 1.200 | ~1.15 | 0.695 |
| 3 | 9/5 = 1.800 | ~1.70 | 0.975 |
| 4 | 12/5 = 2.400 | ~2.25 | 1.210 |
| 5 | 15/5 = 3.000 | ~2.78 | 1.420 |
| 6 | 18/5 = 3.600 | ~3.30 | 1.610 |

**How to verify**: High-Re DNS at Fr ~ O(1) with sufficient scale separation to measure structure functions of orders p = 2-8 in the inertial range.

**Caveat**: The exact form of the BO intermittency correction is not rigorously derived. The specific numbers above are estimates.

---

## P6: Cross-Intermittency Exponent μ_{vb} ≈ 0.30 [ESTIMATE]

**Prediction**: The cross-correlation of velocity and buoyancy dissipation rates scales as ⟨ε_v(r)ε_b(0)⟩ ~ r^{-μ_{vb}} with μ_{vb} ≈ (μ_v + μ_b)/2 ≈ 0.30.

**How to verify**: DNS measurement of the joint velocity-buoyancy dissipation rate correlation function.

---

## P7: Turbulent Patch Filling Factor φ_turb ~ Fr^{1/2} [MODERATE]

**Prediction**: The volume fraction occupied by active turbulent patches (where w ~ Fr^{1/2} U) scales as φ_turb ~ Fr^{1/2}. The domain-averaged vertical velocity then scales as:

```
w_rms ~ (φ_turb · Fr + (1-φ_turb) · Fr²)^{1/2} · U
```

**How to verify**: Identify turbulent patches in DNS by threshold criterion (e.g., gradient Richardson number Ri_g < 1/4), measure φ_turb as a function of Fr at fixed Re.

---

## P8: Mixing Efficiency Γ ∝ Fr for 0.05 < Fr < 0.3 [MODERATE]

**Prediction**: The mixing efficiency scales linearly with Fr in the resonant range where wave and nonlinear time scales are comparable near the Ozmidov scale:

```
Γ = ⟨ε_b⟩/⟨ε_v⟩ ~ α · Fr + Γ_0
```

with α ~ O(1) and Γ_0 ~ 0.1.

**How to verify**: DNS at varying Fr (0.01-1) with fixed Re, measuring Γ = ⟨ε_b⟩/⟨ε_v⟩.

---

## P9: Wave-Vortex Energy Partition at BO Fixed Point [MODERATE]

**Prediction**: At the BO fixed point, the vortex (toroidal) mode carries most of the energy (~80%), with the wave (poloidal) mode carrying ~20%. The VSHF (vertically sheared horizontal flow) mode energy peaks at intermediate Fr and vanishes at both extremes:

```
E_vortex/E_total ~ 0.8 (at FP2)
E_wave/E_total ~ 0.2 (at FP2)
E_VSHF/E_total peaks at Fr ~ Fr_c
```

**How to verify**: Wave-vortex decomposition of DNS velocity fields at varying Fr.

---

## P10: Anisotropy Recovery Scale Depends on Re_b [STRONG]

**Prediction**: The degree of small-scale isotropy depends on Re_b, not Fr alone. Specifically, Re_b > 500 is needed to achieve the same degree of small-scale isotropy as in unstratified turbulence at the same Re.

**How to verify**: Compare isotropy tensor invariants from stratified DNS at varying Re_b with unstratified DNS at the same grid resolution.

---

## P11: Buoyancy Flux Kurtosis Scales with Re_b [MODERATE]

**Prediction**: The kurtosis of the buoyancy flux B_f increases as a power law with Re_b, saturating in the passive scalar limit:

```
Kurt(B_f) ~ Re_b^γ  for Re_b < Re_b^{sat}
Kurt(B_f) ~ const   for Re_b > Re_b^{sat}
```

with γ > 0 and Re_b^{sat} ~ O(100).

**How to verify**: DNS measurement of B_f statistics at varying Re_b.

---

## P12: FNO Kernel Anisotropy Structure [STRONG]

**Prediction**: The FNO-learned kernel W_{ij}(k; ℓ) for stratified turbulence exhibits a characteristic angular dependence that encodes the three fixed points. Specifically:
- At large ℓ (UV), the kernel is isotropic (K41-like)
- At intermediate ℓ, the kernel develops cos²θ anisotropy (BO)
- At small ℓ (IR), the kernel projects onto horizontal modes (2D)

The transition between these kernel structures occurs at scales corresponding to k_B and k_{Oz}.

**How to verify**: Train FNO on multi-scale stratified turbulence DNS data and analyze the learned kernel's angular structure as a function of the coarse-graining scale.

---

## Priority Ranking for Verification

| Priority | Prediction | Feasibility with current DNS | Impact |
|----------|-----------|------------------------------|--------|
| 1 | P1 (Three-FP phase diagram) | Feasible with 1024³-4096³ | High |
| 2 | P4 (Re-entrant K41) | Requires exascale | Very high (falsifiable) |
| 3 | P5 (BO intermittency) | Feasible with 4096³ at high Re_b | High |
| 4 | P7 (Filling factor) | Feasible with 1024³ | Medium |
| 5 | P8 (Γ ∝ Fr) | Feasible with 512³ | Medium |
| 6 | P2 (K_0 ~ O(0.1)) | Feasible with current DNS | Medium |
| 7 | P3 (Crossover φ ≈ 5/2) | Requires systematic Fr scan | Medium |
| 8 | P10 (Re_b > 500 for isotropy) | Challenging | High |
| 9 | P12 (FNO kernel structure) | Requires FNO training | High (novel methodology) |

---

## References

See stratified_derivation.md for full reference list.

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
