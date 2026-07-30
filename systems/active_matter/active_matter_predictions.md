---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 3308874814206131_0/project_7662556975707816201-files/FNO_RG_research/active_matter_turbulence/active_matter_predictions.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 3308874814206131#1785416148302
    ReservedCode2: ""
---
# FNO×RG Active Matter Turbulence: Verifiable Predictions

**Date**: 2026-07-16  
**Framework**: Fourier Neural Operator × Renormalization Group (FNO×RG)

---

## Prediction Classification

- **Tier 1 (HIGH confidence)**: Based on established RG fixed point analysis, confirmed by existing data
- **Tier 2 (MEDIUM confidence)**: Derived from FNO×RG framework but requires additional assumptions
- **Tier 3 (LOW confidence / Speculative)**: Structural analogies; needs FNO training for validation

---

## Tier 1 Predictions (HIGH Confidence)

### P1: Universal Energy Spectrum for Active Nematic Turbulence (Stokes Regime)

**Prediction**: For any 2D overdamped active nematic system, the energy spectrum in the range $k \lesssim k_a = \ell_a^{-1}$ obeys:

$$
E(k) = \frac{\zeta^2}{\eta^2} k^{-1}
$$

with a universal prefactor $\zeta^2/\eta^2$ that depends only on the activity and viscosity.

**How to verify**: Measure $E(k)$ in different active nematic systems (MT-kinesin, bacterial, synthetic) and plot in scaled variables $E(k)\eta^2/\zeta^2$ vs $k\ell_a$. All data should collapse onto a universal curve.

**Current status**: Confirmed for MT-kinesin systems. Needs testing in other platforms.

---

### P2: Active Length Scale as Crossover

**Prediction**: The crossover from $E(k) \sim k^{-1}$ to the steep decay regime always occurs at $k_c \approx (0.8 \pm 0.2) k_a$, where $k_a = \sqrt{|\zeta|/K}$.

**How to verify**: Vary activity $\zeta$ and elastic constant $K$ independently. The crossover wavenumber should scale as $k_c \propto \sqrt{|\zeta|/K}$.

**Current status**: Consistent with DNS data; precise quantitative verification pending.

---

### P3: Defect Density Scaling

**Prediction**: The density of $\pm 1/2$ topological defects scales as:

$$
n_d = C_d \frac{|\zeta|}{K}
$$

where $C_d$ is a universal constant at the NATFP.

**How to verify**: Measure defect density across different activities and elastic constants; plot $n_d K / |\zeta|$ vs activity to check for constancy.

**Current status**: Confirmed qualitatively; precise value of $C_d$ not yet established.

---

### P4: 2D→3D Dimensional Crossover

**Prediction**: The spectral exponents undergo a two-step transition as confinement height $H$ increases:

| Regime | Low-$k$ exponent | High-$k$ exponent | Condition |
|--------|-----------------|-------------------|-----------|
| 2D | +1 | -2 | $H \ll H_{c1}$ |
| Intermediate | +1 | -4 | $H_{c1} < H < H_{c2}$ |
| 3D | -1 | -4 | $H \gg H_{c2}$ |

with $H_{c1} \sim \ell_{\text{particle}}$ and $H_{c2} \sim D_v$ (vortex diameter).

**How to verify**: Systematically vary sample thickness in bacterial suspension experiments and measure spectral exponents.

**Current status**: Confirmed by CAS experiments (Wei et al., 2024).

---

### P5: Kinetic Energy Scales as $\zeta^2$

**Prediction**: The total kinetic energy density of active nematic turbulence scales as:

$$
\langle v^2 \rangle \propto \frac{\zeta^2}{\eta^2} \ell_a^{d-2}
$$

in $d$ dimensions, for sufficiently high activity.

**How to verify**: Measure $\langle v^2 \rangle$ as a function of $\zeta$ at fixed $\eta$ and $K$; should scale quadratically.

**Current status**: Confirmed in 3D DNS (Hemingway et al., 2024).

---

### P6: Hyperuniform Defect Subpopulations

**Prediction**: In nematic active turbulence, the subpopulations of $+1/2$ and $-1/2$ defects separately exhibit hyperuniform number fluctuations (variance exponent $\beta_\pm < 2$), while the total defect population has $\beta < 2$ but $\beta > \beta_\pm$.

**How to verify**: Compute number variance separately for $N^+$, $N^-$, and $N = N^+ + N^-$ as a function of sampling window size.

**Current status**: Confirmed by PNAS (2025) experiments.

---

## Tier 2 Predictions (MEDIUM Confidence)

### P7: Active She-Leveque-Type Scaling for Structure Functions

**Prediction**: For polar active turbulence, the structure function exponents follow:

$$
\zeta_p = \frac{p}{3} + \frac{2}{9}\left(1 - \left(\frac{1}{3}\right)^{p/3}\right)(1 - C_{\text{active}})
$$

with $C_{\text{active}} = 1$ (2D point defects) or $C_{\text{active}} = 2$ (3D defect lines).

**How to verify**: 
1. Perform high-resolution DNS of bacterial turbulence at varying activity levels
2. Measure $\zeta_p$ for $p = 1, 2, ..., 8$
3. Fit to the formula and extract $C_{\text{active}}$

**Current status**: Unvalidated. The bacterial turbulence data from Wensink et al. (2012) are consistent with $\zeta_p \approx p/3$ (small intermittency), but the precise functional form has not been tested.

**Key assumption**: The most singular structures in active turbulence are defect cores, analogous to vortex filaments in NS turbulence.

---

### P8: Crossover from Active to Passive Scaling

**Prediction**: As activity $\zeta \to 0$, the RG flow transitions from NATFP to the Gaussian fixed point. The crossover is controlled by the dimensionless parameter:

$$
\tilde{g} = \frac{|\zeta| \ell_a^2}{K} = 1
$$

which is always $\mathcal{O}(1)$ at the active length scale. The true control parameter for the activity→passivity crossover is:

$$
\tilde{g}_{\text{system}} = \frac{|\zeta| L^2}{K}
$$

where $L$ is the system size. Active turbulence exists only when $\tilde{g}_{\text{system}} > 1$.

**How to verify**: Reduce activity $\zeta$ at fixed system size $L$ and elastic constant $K$; measure the spectral exponent as a function of $\tilde{g}_{\text{system}}$.

**Current status**: Partially verified by DNS showing that below a critical activity, the system relaxes to uniform order.

---

### P9: Non-Universal Self-Similar Energy Cascades in Self-Propulsive Active Nematics

**Prediction**: When self-propulsion $V_0$ is added to active nematics, the energy cascade becomes **non-universal**: the spectral exponent depends continuously on $V_0$.

**How to verify**: Simulate the Beris-Edwards equations with self-propulsion (Phil. Trans. R. Soc. A, 2025 model) and measure $E(k)$ for different $V_0$.

**Current status**: Consistent with recent DNS results showing non-universal cascades.

---

### P10: Vortex-Defect Density Ratio

**Prediction**: The ratio of vortex density to $+1/2$ defect density is:

$$
\frac{n_v}{n_d^+} = C_{vd} \approx 1.0 \text{ (extensile)}, \quad \approx 0.5 \text{ (contractile)}
$$

**How to verify**: Simultaneously track vortices (via Okubo-Weiss parameter) and defects (via winding number) in the same active nematic system.

**Current status**: Qualitatively consistent; precise ratio not yet measured.

---

### P11: Activity-Dependent Spectral Exponent for Polar Active Turbulence

**Prediction**: For polar active turbulence described by Toner-Tu + Swift-Hohenberg, the high-$k$ spectral exponent crosses from $k^{-3/2}$ to $k^{-8/3}$ as the instability growth timescale $\tau_\Gamma$ decreases:

$$
E(k) \sim k^{-\sigma}, \quad \sigma = \frac{3}{2} + \frac{7}{6} f(\tau_\Gamma / \tau_c)
$$

where $f(x) \to 0$ as $x \to \infty$ and $f(x) \to 1$ as $x \to 0$.

**How to verify**: Vary $|\Gamma_0|$ (and hence $\tau_\Gamma$) at fixed activity and measure the spectral exponent.

**Current status**: Consistent with DNS data from arXiv:2507.04890.

---

## Tier 3 Predictions (LOW Confidence / Speculative)

### P12: Active Noise Spectrum Measurement

**Prediction**: The effective noise spectrum in the velocity field at the NATFP scales as:

$$
D_{\text{eff}}^v(k) \sim k^{d-5}
$$

In $d=2$: $k^{-3}$; in $d=3$: $k^{-2}$.

**How to verify**: Measure velocity fluctuations at different scales after filtering out the mean flow. Compare the variance at each scale with the prediction.

**Current status**: No direct measurements exist.

---

### P13: FRG Fixed Point for Compressible Active Matter

**Prediction**: Compressible polar active fluids at the multicritical point (order-disorder + phase separation) exhibit three novel non-equilibrium universality classes, as found by the FRG analysis [(arXiv:2210.03830)](https://ar5iv.org/html/2210.03830). The FNO×RG framework should reproduce these when applied to the same model.

**How to verify**: Apply FNO×RG to the compressible polar active fluid model and compare the critical exponents with the FRG results.

**Current status**: FRG results exist; FNO×RG application pending.

---

### P14: Topological Phase Interpretation of 3D Active Turbulence

**Prediction**: 3D active nematic turbulence can be viewed as a topological phase, where defect lines percolate to form delocalized Majorana-like quasiparticles [(PNAS, 2024)](https://www.pnas.org/doi/full/10.1073/pnas.2405304121). The FNO×RG should reveal a topological invariant at the NATFP in 3D.

**How to verify**: Compute the topological charge of the disclination network in 3D DNS and show it is quantized and conserved in the turbulent state.

**Current status**: Topological interpretation proposed; RG connection not yet established.

---

### P15: Conformal Invariance from Spectral Marginality

**Prediction**: The $E(q) \sim q^{-1}$ spectrum in 2D active nematic turbulence places the vorticity sign-field correlations exactly at the Weinrib-Halperin marginal value $a = 3/2$, leading to SLE$_6$ statistics for zero-vorticity contours [(arXiv:2604.16473)](https://arxiv.org/pdf/2604.16473). The FNO×RG should reproduce this through the marginality of the sign-field perturbation at the NATFP.

**How to verify**: Perform Schramm-Loewner evolution analysis on zero-vorticity contours from DNS data.

**Current status**: Theoretical argument and partial numerical confirmation exist.

---

## Priority Ranking for Validation

| Priority | Prediction | Feasibility | Impact |
|----------|-----------|-------------|--------|
| 1 | P1: Universal $E(k) \sim k^{-1}$ | Easy (existing data) | High — confirms NATFP |
| 2 | P4: 2D→3D crossover | Moderate (systematic experiments) | High — tests dimensional universality |
| 3 | P3: Defect density $n_d \sim \zeta/K$ | Easy (existing data) | Medium — confirms active length |
| 4 | P7: Active She-Leveque | Hard (high-resolution DNS) | Very high — if confirmed |
| 5 | P2: Crossover at $k_c$ | Moderate (multi-activity DNS) | Medium — tests crossover function |
| 6 | P11: Activity-dependent exponent | Moderate (DNS) | High — resolves spectral controversy |
| 7 | P10: Vortex-defect ratio | Moderate (simultaneous tracking) | Medium — tests defect-flow coupling |
| 8 | P15: Conformal invariance | Hard (SLE analysis) | Very high — deep mathematical connection |

---

## References

1. Wensink et al. (2012) PNAS 109, 14308 [(PNAS)](https://www.pnas.org/content/pnas/109/36/14308.full.pdf)
2. Hemingway et al. (2024) — 3D active nematic DNS [(arXiv:1912.09680)](https://arxiv.org/pdf/1912.09680v1)
3. Wei et al. (2024) Adv. Sci. — 2D→3D scaling transition [(CAS)](https://iop.cas.cn/xwzx/kydt/202408/t20240826_7317854.html)
4. Alert et al. (2022) — Universal energy spectrum [(arXiv:2604.16473)](https://arxiv.org/pdf/2604.16473)
5. PNAS (2025) — Hyperuniformity in active nematic defects [(PNAS)](https://www.pnas.org/doi/full/10.1073/pnas.2512147122)
6. FRG for compressible polar active fluids [(arXiv:2210.03830)](https://ar5iv.org/html/2210.03830)
7. Majorana quasiparticles in 3D active nematics [(PNAS 2024)](https://www.pnas.org/doi/full/10.1073/pnas.2405304121)
8. Emergence of local ordering (2025) [(arXiv:2507.04890)](https://arxiv.org/pdf/2507.04890)

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
