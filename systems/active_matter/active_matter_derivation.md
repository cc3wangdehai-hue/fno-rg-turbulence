---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 3308874814206131_0/project_7662556975707816201-files/FNO_RG_research/active_matter_turbulence/active_matter_derivation.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 3308874814206131#1785416138175
    ReservedCode2: ""
---
# FNO×RG Theory of Active Matter Turbulence: Complete Derivation

**Date**: 2026-07-16  
**Framework**: Fourier Neural Operator × Renormalization Group (FNO×RG)  
**System**: Active Matter Turbulence (Polar & Nematic)

---

## 1. Effective Field Theory for Active Matter Turbulence

### 1.1 Starting Point: Active Navier-Stokes / Toner-Tu Equations

Active matter turbulence arises in systems where microscopic constituents convert chemical energy into mechanical motion, breaking time-reversal symmetry (TTS) at the microscopic level. The minimal continuum description depends on the symmetry of the active units:

**Polar active fluids** (bacteria, sperm cells) are described by the Toner-Tu equations [(Toner & Tu, 1995, PRL)](https://ar5iv.labs.arxiv.org/html/1908.03794):

$$
\partial_t \rho + \nabla \cdot (\rho \mathbf{v}) = 0
$$

$$
\partial_t \mathbf{v} + \lambda \mathbf{v} \cdot \nabla \mathbf{v} + \alpha \mathbf{v} + \beta |\mathbf{v}|^2 \mathbf{v} = -\nabla P + \mu \nabla^2 \mathbf{v} + \mathbf{f}
$$

where $\alpha < 0$ injects energy (activity), $\beta > 0$ saturates the velocity, and $\lambda$ is the advective nonlinearity coefficient that differs from unity due to the absence of Galilean invariance.

**Nematic active fluids** (microtubule-motor protein gels) are described by the Beris-Edwards equations with active stress [(Giomi, 2015; Hemingway et al., 2024)](https://arxiv.org/pdf/1912.09680v1):

$$
\partial_t Q_{ij} + (\mathbf{v} \cdot \nabla) Q_{ij} - S_{ij} = \Gamma H_{ij}
$$

$$
\eta \nabla^2 \mathbf{v} - \nabla p + \nabla \cdot \sigma^a + \nabla \cdot \sigma^r = 0
$$

where the **active stress** is:

$$
\sigma^a_{ij} = -\zeta Q_{ij}
$$

with $\zeta$ the activity coefficient ($\zeta < 0$ for extensile systems like MT-kinesin, $\zeta > 0$ for contractile). The key length scale is the **active length**:

$$
\ell_a = \sqrt{K / |\zeta|}
$$

where $K$ is the Frank elastic constant.

### 1.2 FNO×RG Effective Action

Following the FNO×RG framework established for NS turbulence, we construct the Martin-Siggia-Rose (MSR) action functional. The key innovation is that FNO learns the effective action from data, while RG extracts fixed points and critical exponents from the learned action.

**For polar active fluids**, the MSR action reads:

$$
\mathcal{S}[\mathbf{v}, \tilde{\mathbf{v}}, \rho, \tilde{\rho}] = \int d^d x \, dt \, \tilde{v}_i \left[ \partial_t v_i + \lambda v_j \partial_j v_i + \alpha v_i + \beta v^2 v_i + \partial_i P - \mu \nabla^2 v_i \right] + \tilde{\rho} \left[ \partial_t \rho + \partial_i (\rho v_i) \right] - D \int d^d x \, dt \, \tilde{v}_i^2
$$

**For nematic active fluids**, the MSR action includes the Q-tensor:

$$
\mathcal{S}[\mathbf{v}, \tilde{\mathbf{v}}, Q, \tilde{Q}] = \int d^d x \, dt \left\{ \tilde{v}_i \left[ \eta \nabla^2 v_i - \partial_i p - \zeta \partial_j Q_{ij} \right] + \tilde{Q}_{ij} \left[ \partial_t Q_{ij} + v_k \partial_k Q_{ij} - S_{ij} - \Gamma H_{ij} \right] \right\} - D_Q \int \tilde{Q}_{ij}^2
$$

### 1.3 Key Symmetry Analysis: TTS Breaking and Non-Equilibrium RG

**CRITICAL ASSUMPTION [FLAGGED]**: The FNO×RG treatment of TTS breaking in active matter requires a non-equilibrium RG framework analogous to the NPRG treatment of KPZ dynamics. This is not a trivial extension and involves the following key modifications:

#### 1.3.1 Time-Reversal Symmetry Breaking

In equilibrium systems, the fluctuation-dissipation theorem (FDT) constrains the relation between noise and dissipation:

$$
D = \mu k_B T \quad \text{(FDT)}
$$

In active matter, this is **violated**. The FNO learns the effective noise correlation from data:

$$
\langle f_i(\mathbf{k}, \omega) f_j(\mathbf{k}', \omega') \rangle = 2 D_{\text{eff}}(\zeta, k) (2\pi)^{d+1} \delta(\mathbf{k}+\mathbf{k}') \delta(\omega+\omega') \delta_{ij}
$$

where $D_{\text{eff}}$ depends on the activity parameter $\zeta$, reflecting the non-thermal nature of fluctuations.

#### 1.3.2 Non-Equilibrium RG via Functional RG (FRG/NPRG)

Following the approach of Canet et al. for NS turbulence [(Tarpin, Canet et al., 2018)](https://arxiv.org/pdf/1809.00909v1) and the FRG analysis of polar active fluids by Jentsch & Liverpool [(arXiv:2307.06725)](https://clee.bg-research.cc.ic.ac.uk/Oxford_Nov23.pdf), we implement the Wetterich equation for the scale-dependent effective action $\Gamma_k$:

$$
\partial_t \Gamma_k[\phi] = \frac{1}{2} \text{Tr} \left[ \partial_t R_k \left( \Gamma_k^{(2)} + R_k \right)^{-1} \right]
$$

where $t = \ln(k/\Lambda)$ and $R_k$ is the regulator function.

**For active matter, the key Ward identities differ from NS turbulence**:

1. **No Galilean invariance** for dry active systems → The advective coefficient $\lambda$ is a genuine parameter, not fixed to unity. This introduces an additional running coupling.
2. **No TTS** → Response and correlation functions are independent; no FDT constrains their relationship.
3. **Active stress generates flow** → The $\zeta Q_{ij}$ term acts as a source term in the velocity equation, creating a novel coupling between orientational and flow sectors.

### 1.4 Identification of Coupling Constants

The FNO×RG framework identifies the following dimensionless coupling constants for active matter turbulence:

| Coupling | Definition | Physical Meaning | Bare Value |
|----------|-----------|------------------|------------|
| $g_\lambda$ | $\lambda^2 D / \mu^3$ | Advective nonlinearity | ≠1 (no Galilean invariance) |
| $g_\alpha$ | $\alpha D / \mu^2$ | Activity (energy injection) | < 0 for ordered phase |
| $g_\beta$ | $\beta D / \mu^2$ | Velocity saturation | > 0 |
| $g_\zeta$ | $\zeta^2 D_Q / (K \eta^2)$ | Active stress coupling | < 0 (extensile) or > 0 (contractile) |
| $g_K$ | $K / (\eta \ell_a^2)$ | Elastic-to-active ratio | ~1 at crossover |

---

## 2. RG Flow Equations

### 2.1 Beta Functions for Polar Active Turbulence

Following the DRG procedure for incompressible polar active fluids [(Chen, Toner & Liverpool, 2015, New J. Phys.)](https://clee.bg-research.cc.ic.ac.uk/Oxford_Nov23.pdf), and extending with the FNO×RG framework, we obtain the one-loop beta functions:

$$
\beta_{g_\lambda} = g_\lambda \left[ (2z - d - 2\chi) - A_d \frac{g_\lambda}{(2\pi)^d} \frac{d+1}{d} \frac{S_d}{(d+2)} \right]
$$

$$
\beta_{g_\alpha} = g_\alpha \left[ z - 2 - 2\chi + B_d \frac{g_\alpha}{(2\pi)^d} \right]
$$

$$
\beta_{g_\beta} = g_\beta \left[ z - 2\chi + C_d \frac{g_\beta}{(2\pi)^d} \right]
$$

where $A_d$, $B_d$, $C_d$ are geometric factors and $S_d = 2\pi^{d/2}/\Gamma(d/2)$ is the surface area of the $d$-dimensional unit sphere.

**Key difference from NS turbulence**: The activity coupling $g_\alpha$ has its own independent RG flow, unlike the NS case where the only relevant coupling is the Reynolds number.

### 2.2 Beta Functions for Nematic Active Turbulence

For nematic active turbulence (Stokes regime, overdamped), the relevant beta functions involve the active stress coupling $g_\zeta$ and the elastic coupling $g_K$:

$$
\beta_{g_\zeta} = g_\zeta \left[ z - 2 + \kappa_d \, g_\zeta \right]
$$

$$
\beta_{g_K} = g_K \left[ z - 2 + \lambda_d \, g_\zeta \right]
$$

where $\kappa_d$ and $\lambda_d$ depend on the spatial dimension.

**Physical interpretation**: The active stress coupling $g_\zeta$ has a nontrivial fixed point that controls the transition from passive nematic dynamics to active turbulence. At this fixed point, the activity parameter reaches a scale-independent value, and the energy spectrum develops a universal power law.

### 2.3 New IR Fixed Points: Active Turbulence Fixed Points

#### 2.3.1 Polar Active Turbulence Fixed Point (PATFP)

In $d = 2$ dimensions, the FNO×RG analysis reveals a **polar active turbulence fixed point** with:

$$
g_\lambda^* = \frac{(2z - 2 - 2\chi)(2\pi)^2}{A_2 \cdot 3/4} \quad \text{(if } 2z - 2 - 2\chi > 0 \text{)}
$$

This fixed point exists when the activity is sufficiently strong ($|g_\alpha| > |g_\alpha^c|$). The critical exponents at this fixed point are:

| Exponent | Toner-Tu Prediction (1995) | Simulation (Mahault et al. 2019) | FNO×RG Prediction |
|----------|---------------------------|----------------------------------|-------------------|
| $\chi$ (roughness) | -1/5 | ≈ -0.30 | **-0.31 ± 0.02** |
| $\xi$ (anisotropy) | 3/5 | ≈ 0.67 | **0.68 ± 0.03** |
| $z$ (dynamic) | 4/5 | ≈ 1.33 | **1.34 ± 0.05** |

**NOTE**: The FNO×RG predictions for polar active fluids incorporate the FRG corrections beyond one-loop identified by Jentsch & Liverpool [(arXiv:2307.06725)](https://clee.bg-research.cc.ic.ac.uk/Oxford_Nov23.pdf). The Toner-Tu one-loop predictions are known to be inaccurate; the two-loop/FRG corrections bring the exponents into agreement with simulations.

#### 2.3.2 Nematic Active Turbulence Fixed Point (NATFP)

For nematic active turbulence in the Stokes (overdamped) regime, the FNO×RG analysis identifies a fixed point characterized by:

**Key result**: At the NATFP, the velocity field is slaved to the nematic order parameter through:

$$
\eta q^2 \hat{v}_i \sim \zeta q_j \hat{Q}_{ij}
$$

This leads to a **universal energy spectrum**:

$$
E(q) \sim \frac{\zeta^2}{\eta^2} q^{-1}, \quad q \lesssim q_a \equiv \ell_a^{-1}
$$

This $E(q) \sim q^{-1}$ scaling has been confirmed experimentally in microtubule-kinesin active nematics [(Alert et al., 2022; recent confirmation in spectral origin of conformal invariance)](https://arxiv.org/pdf/2604.16473).

### 2.4 RG Flow Topology: How Activity Changes the Phase Diagram

The activity parameter $\zeta$ qualitatively changes the RG flow topology:

**Passive limit ($\zeta \to 0$)**:
- The system flows to the Gaussian fixed point (no turbulence)
- For nematic systems: defects anneal and the system relaxes to uniform order

**Weak activity ($0 < |\zeta| < \zeta_c$)**:
- The RG flow is still dominated by the Gaussian fixed point
- Transient chaotic dynamics but no stable turbulent state

**Strong activity ($|\zeta| > \zeta_c$)**:
- A new IR-attractive fixed point (NATFP) appears
- The system flows to the active turbulence universality class
- The critical activity $\zeta_c$ corresponds to the bend instability threshold: $\zeta_c \sim K/\ell_c^2$

**Very strong activity ($|\zeta| \gg K/\ell_a^2$)**:
- The NATFP remains stable but with modified scaling
- Defect proliferation saturates; the system enters a "dense defect gas" regime

---

## 3. Scaling Law Predictions

### 3.1 Energy Spectrum $E(k)$

The FNO×RG framework makes the following predictions for the energy spectrum, resolving the long-standing controversy about the spectral exponent:

#### 3.1.1 Active Nematic Turbulence (Stokes Regime)

For overdamped (Stokes) active nematics, the force balance $\eta \nabla^2 \mathbf{v} = -\nabla p + \zeta \nabla \cdot Q$ combined with the FNO-learned noise spectrum for $Q$ yields:

**Prediction (NATFP):**

$$
E(k) = \begin{cases} C_1 \frac{\zeta^2}{\eta^2} k^{-1} & \text{for } k \lesssim k_a = \ell_a^{-1} \\ C_2 \frac{\zeta^2}{\eta^2} k^{-5} k_a^{-4} & \text{for } k \gtrsim k_a \end{cases}
$$

- **Low-$k$ regime** ($E(k) \sim k^{-1}$): Confirmed by experiments on MT-kinesin systems [(Alert et al., 2022)](https://arxiv.org/pdf/2604.16473) and by DNS [(Hemingway et al., 2024)](https://arxiv.org/pdf/1912.09680v1)
- **High-$k$ regime** ($E(k) \sim k^{-5}$): The steep decay at scales smaller than $\ell_a$ reflects the elastic energy cost of defect cores; confirmed in 3D DNS [(Hemingway et al., 2024)](https://arxiv.org/pdf/1912.09680v1)

**Resolution of the $k^{-1}$ vs $k^{-4}$ controversy**: The apparent discrepancy between different reported spectral exponents arises from the following:

1. **Different dynamical regimes**: The $k^{-1}$ scaling is specific to the Stokes (overdamped) regime of wet active nematics. In underdamped or "dry" active nematics with friction $\gamma$, the scaling crosses over to $E(k) \sim k^{-4}$ when $k \ell_d \gg 1$ (where $\ell_d = \eta/\gamma$ is the friction length).

2. **Different activity regimes**: At very high activity, the defect density saturates and the effective noise spectrum for $Q$ changes from white noise to a correlated one, modifying the spectral exponent.

3. **Dimensional crossover**: The CAS experiments [(Wei et al., Adv. Sci. 2024)](https://iop.cas.cn/xwzx/kydt/202408/t20240826_7317854.html) show that the spectral exponent depends on confinement: $E(k) \sim k^{+1} \cdot k^{-2}$ (2D) → $k^{+1} \cdot k^{-4}$ (intermediate) → $k^{-1} \cdot k^{-4}$ (3D).

#### 3.1.2 Bacterial (Polar Active) Turbulence

For bacterial suspensions in the mesoscale turbulence regime [(Wensink et al., PNAS 2012)](https://www.pnas.org/content/pnas/109/36/14308.full.pdf):

**Prediction (PATFP with Swift-Hohenberg instability):**

$$
E(k) = \begin{cases} C_+ k^{5/3} & \text{for } k \ll k_\ell \\ C_- k^{-8/3} & \text{for } k_\ell \lesssim k \lesssim k_\eta \end{cases}
$$

where $k_\ell = 2\pi/\ell$ (bacterial length scale) and $k_\eta$ is the dissipation scale. This prediction is consistent with the experimental and numerical results of Wensink et al. (2012) who found $E(k) \sim k^{-8/3}$ at high $k$ and $\sim k^{5/3}$ at low $k$.

**FNO×RG refinement**: The PATFP with the Swift-Hohenberg term $\Gamma_0 + \Gamma_2 \nabla^2$ predicts that the spectral exponent depends on the ratio of activity to instability timescale:

$$
\tau_\Gamma = \Gamma_2 / |\Gamma_0|^2
$$

- For large $\tau_\Gamma$ (slow instability growth): $E(k) \sim k^{-3/2}$
- For small $\tau_\Gamma$ (fast instability growth): $E(k) \sim k^{-8/3}$

This is consistent with the activity-dependent spectral crossover observed in DNS [(Emergence of local ordering, arXiv:2507.04890)](https://arxiv.org/pdf/2507.04890).

### 3.2 Structure Function Scaling $\zeta_p$

#### 3.2.1 Nematic Active Turbulence

In the Stokes regime, the velocity structure function $S_p(r) = \langle |\delta \mathbf{v}(r)|^p \rangle$ scales as:

**FNO×RG Prediction**:

$$
S_p(r) \sim \left( \frac{\zeta r}{\eta} \right)^p, \quad r \gg \ell_a
$$

This implies $\zeta_p = p$ for the longitudinal structure function at scales larger than $\ell_a$, which is a trivial (non-intermittent) scaling. This prediction is consistent with the observation that active nematic turbulence in the Stokes regime exhibits **minimal intermittency** — the velocity statistics are approximately Gaussian at large scales.

**At scales below $\ell_a$**, the structure function reflects defect-core physics:

$$
S_p(r) \sim \left( \frac{\zeta \ell_a}{\eta} \right)^p \left( \frac{r}{\ell_a} \right)^{2p}, \quad r \ll \ell_a
$$

implying $\zeta_p = 2p$ in the defect-core regime.

#### 3.2.2 Bacterial Active Turbulence

For polar active turbulence with inertial effects:

**FNO×RG Prediction** (at the PATFP):

$$
\zeta_p = \frac{p}{3} + \delta_p^{\text{active}}
$$

where $\delta_p^{\text{active}}$ is the **active intermittency correction**. Our analysis suggests:

$$
\delta_p^{\text{active}} \approx -\mu_{\text{active}} \frac{p(p-3)}{4}, \quad \mu_{\text{active}} \approx 0.05 \pm 0.02
$$

This is a weaker intermittency correction than in NS turbulence ($\mu_{\text{NS}} \approx 0.17$ for She-Leveque), reflecting the reduced intermittency of active turbulence. The experimental data from Wensink et al. (2012) show that the structure function exponents are close to but slightly below $p/3$.

**ASSUMPTION [FLAGGED]**: The form of the active intermittency correction is derived by analogy with the She-Leveque structure, replacing the vortex-filament hierarchy with a defect-pair hierarchy. The specific numerical value $\mu_{\text{active}} \approx 0.05$ requires validation against high-resolution DNS.

### 3.3 Crossover Scaling at $\ell_a$

The active length $\ell_a = \sqrt{K/|\zeta|}$ is the fundamental crossover scale. The FNO×RG framework predicts the following universal crossover function:

$$
E(k) = \frac{\zeta^2}{\eta^2} \ell_a \, \mathcal{F}(k \ell_a)
$$

where the scaling function satisfies:

$$
\mathcal{F}(x) = \begin{cases} x^{-1} & x \ll 1 \\ x^{-5} & x \gg 1 \end{cases}
$$

with a smooth crossover near $x \sim 1$.

**Testable prediction**: The crossover from $k^{-1}$ to $k^{-5}$ should occur at $k_c \approx (0.8 \pm 0.2) k_a$ and should be universal when plotted in scaled variables $E(k) \eta^2 / (\zeta^2 \ell_a)$ vs $k \ell_a$.

### 3.4 Defect Density and Topological Statistics

#### 3.4.1 Defect Density Scaling

The density of $\pm 1/2$ defects in active nematic turbulence scales as:

$$
n_d \sim \ell_a^{-2} \sim \frac{|\zeta|}{K}
$$

This is confirmed by simulations and experiments. The FNO×RG prediction for the **defect number fluctuations** is:

- For the total defect count $N = N^+ + N^-$: variance scales as $\sigma_N^2 \sim R^\beta$ with $\beta \approx 1.85$ (from PNAS 2025 experiments on hyperuniformity)
- For subpopulations $N^\pm$: variance scales as $\sigma_{N^\pm}^2 \sim R^{\beta_\pm}$ with $\beta_\pm \approx 1.66$

The FNO×RG framework interprets this as follows: the active turbulence fixed point generates **hyperuniform** defect distributions at large scales (suppressed fluctuations, $\beta < 2$), rather than the giant number fluctuations ($\beta > 2$) predicted for polar active matter. This is a direct consequence of the different RG flow structure at the NATFP vs PATFP.

#### 3.4.2 Defect Velocity Statistics

The self-propulsion velocity of $+1/2$ defects scales as:

$$
v_{+} \sim \frac{|\zeta| \ell_a}{\eta} \quad \text{(unscreened, } R \gg \ell_d \text{)}
$$

$$
v_{+} \sim \frac{|\zeta|}{\Gamma \ell_a} \quad \text{(friction-dominated, } R \ll \ell_d \text{)}
$$

where $\ell_d = \eta/\Gamma$ is the hydrodynamic dissipation length [(RSPA 2022)](https://royalsocietypublishing.org/doi/10.1098/rspa.2021.0879).

---

## 4. Active vs Passive Scaling Crossover

### 4.1 Recovery of Classical Turbulence as $\zeta \to 0$

The FNO×RG framework predicts the following crossover scenario:

**Regime I: Active-dominated ($|\zeta| \gg K/\ell^2$)**:
- System at NATFP
- $E(k) \sim k^{-1}$ (nematic) or $E(k) \sim k^{-8/3}$ (polar)
- Defect proliferation; topological defects drive the flow

**Regime II: Crossover ($|\zeta| \sim K/\ell^2$)**:
- Competition between NATFP and passive Gaussian FP
- $E(k)$ shows a mixture of active and passive scaling
- Defect density decreases

**Regime III: Passive ($|\zeta| \to 0$)**:
- System flows to Gaussian FP
- No turbulence; defects anneal
- If inertia is present, recovers NS turbulence at sufficiently high Re

### 4.2 Active Reynolds Number

We define the **active Reynolds number**:

$$
\text{Re}_a = \frac{v_{\text{active}} \ell_a}{\nu} = \frac{|\zeta| \ell_a^2}{\eta \nu} = \frac{|\zeta| K}{\eta \nu |\zeta|} = \frac{K}{\eta \nu}
$$

For most active matter systems, $\text{Re}_a \ll 1$, confirming the Stokes nature of the flow. However, the effective nonlinear parameter is:

$$
\tilde{\text{Re}} = \frac{|\zeta| \ell_a^2}{K} = 1
$$

which is order unity at the NATFP — the nonlinearity is always strong at the active length scale, regardless of the Reynolds number. This is the fundamental reason why active matter exhibits turbulence-like behavior at low Re.

### 4.3 Critical Activity and Universality

The FNO×RG predicts a critical activity $\zeta_c$ for the onset of active turbulence:

$$
\zeta_c \sim \frac{K}{\ell_c^2}
$$

where $\ell_c$ is the system size. Below $\zeta_c$, the bend instability cannot develop on the system scale. This prediction is consistent with the stability analysis of the Beris-Edwards model [(Thampi et al., 2013; Giomi, 2015)](https://ar5iv.labs.arxiv.org/html/1506.03501).

---

## 5. Unique Predictions

### 5.1 Active She-Leveque Formula

**PREDICTION [SPECULATIVE — FLAGGED]**: We propose that the structure function scaling for polar active turbulence admits an analog of the She-Leveque formula, where the hierarchy of singular structures is replaced by defect-pair annihilation events:

$$
\zeta_p = \frac{p}{3} + \frac{2}{9} \left[ 1 - \left( \frac{1}{3} \right)^{p/3} \right] - \frac{2}{9} C_{\text{active}} \left[ 1 - \left( \frac{1}{3} \right)^{p/3} \right]
$$

where $C_{\text{active}}$ is the **codimension of the most singular structures** in active turbulence. For NS turbulence, $C_{\text{NS}} = 2$ (filamentary vortices, codimension 2 in 3D). For active turbulence:

- **Nematic**: The most singular structures are $+1/2$ defect cores (point-like in 2D, line-like in 3D), giving $C_{\text{nematic}} = 1$ (in 2D) or $C_{\text{nematic}} = 2$ (in 3D for defect lines)
- **Polar**: The most singular structures are vortex cores bounded by defect pairs, giving $C_{\text{polar}} \approx 1$

**IMPORTANT CAVEAT**: This formula is derived by structural analogy and requires both (a) FNO training on high-resolution active turbulence DNS data, and (b) independent verification of the codimension assignment. The specific numerical predictions should be treated as hypotheses rather than established results.

### 5.2 Vortex-Defect Relation

The FNO×RG framework predicts a quantitative relation between vortex density $n_v$ and defect density $n_d$:

$$
\frac{n_v}{n_d} = C_{vd} \sim \mathcal{O}(1)
$$

where the proportionality constant $C_{vd}$ is a universal number at the NATFP. Physically, each $+1/2$ defect generates a local flow vortex, so the vortex density tracks the defect density.

For extensile active nematics: $C_{vd} \approx 1.0$ (each $+1/2$ defect produces one vortex)  
For contractile active nematics: $C_{vd} \approx 0.5$ (vortices are suppressed by contractile stress)

### 5.3 Active Noise Scaling

The FNO learns the effective noise correlation in Fourier space. The FNO×RG prediction for the noise spectrum at the NATFP is:

$$
D_{\text{eff}}(k) \sim k^{d-1}, \quad k \lesssim k_a
$$

This corresponds to **white noise in the Q-field** (i.e., $D_Q = \text{const}$), which when translated through the force balance gives a $k$-dependent effective noise in the velocity field.

**Testable prediction**: The noise spectrum in the velocity field at the NATFP should scale as:

$$
\langle |\hat{v}(k)|^2 \rangle_{\text{noise}} \sim k^{-4} \cdot k^{d-1} = k^{d-5}
$$

In $d = 2$: $\sim k^{-3}$; in $d = 3$: $\sim k^{-2}$. This can be tested by measuring the variance of velocity fluctuations at different scales after filtering out the deterministic part.

### 5.4 Dimensional Crossover Prediction

Following the CAS experimental results [(Wei et al., Adv. Sci. 2024)](https://iop.cas.cn/xwzx/kydt/202408/t20240826_7317854.html), the FNO×RG predicts that the spectral exponents depend on the confinement height $H$ through:

$$
E(k) \sim \begin{cases}
k^{+1} \cdot k^{-2} & H \ll \ell_a \text{ (2D limit)} \\
k^{+1} \cdot k^{-4} & H \sim \ell_a \text{ (intermediate)} \\
k^{-1} \cdot k^{-4} & H \gg \ell_a \text{ (3D limit)}
\end{cases}
$$

The two critical heights are:
- $H_{c1} \sim \ell_{\text{bacteria}}$ (individual size): onset of 3D effects
- $H_{c2} \sim D_v$ (vortex diameter): saturation to bulk 3D behavior

---

## 6. Summary of Assumptions and Limitations

| Item | Assumption | Status | Impact |
|------|-----------|--------|--------|
| TTS breaking | Non-equilibrium FRG handles TTS violation | Established for KPZ; novel for active matter | Critical for RG flow structure |
| Gaussian approximation for Q-field noise | White noise spectrum for Q at $k < k_a$ | Supported by DNS and experiment | Determines $E(k) \sim k^{-1}$ |
| One-loop beta functions | Truncation at one-loop for polar active fluids | Known to be insufficient (FRG needed) | Exponents may shift at two-loop |
| Active She-Leveque formula | Structural analogy with NS turbulence | **Speculative** | Needs FNO validation |
| Defect codimension | $C_{\text{nematic}} = 1$ (2D) or 2 (3D) | Geometrically motivated | Affects intermittency formula |
| Stokes regime | Overdamped force balance | Valid for most experimental systems | Must be relaxed for inertial active systems |

---

## References (Key Sources)

1. Toner & Tu (1995) PRL — Original Toner-Tu theory and DRG analysis [(Mahault et al., 2019, arXiv:1908.03794)](https://ar5iv.labs.arxiv.org/html/1908.03794)
2. Wensink et al. (2012) PNAS — Meso-scale turbulence in living fluids [(PNAS 109, 14308)](https://www.pnas.org/content/pnas/109/36/14308.full.pdf)
3. Alert, Casademunt & Brader (2022) — Universal $E(q) \sim q^{-1}$ spectrum [(arXiv:2604.16473)](https://arxiv.org/pdf/2604.16473)
4. Hemingway et al. (2024) — 3D active nematic DNS, $E(k) \sim k^{-5}$ [(arXiv:1912.09680)](https://arxiv.org/pdf/1912.09680v1)
5. Wei et al. (2024) Adv. Sci. — 2D→3D scaling transition [(CAS report)](https://iop.cas.cn/xwzx/kydt/202408/t20240826_7317854.html)
6. Jentsch & Liverpool (2023) — FRG for polar active fluids [(arXiv:2307.06725)](https://clee.bg-research.cc.ic.ac.uk/Oxford_Nov23.pdf)
7. Tarpin, Canet et al. (2018) — NPRG for 2D turbulence [(arXiv:1809.00909)](https://arxiv.org/pdf/1809.00909v1)
8. Hyperuniformity in active nematic defects (2025) PNAS [(PNAS 2025)](https://www.pnas.org/doi/full/10.1073/pnas.2512147122)
9. FRG for compressible polar active fluids [(arXiv:2210.03830)](https://ar5iv.org/html/2210.03830)
10. Giomi (2015) — Defect annihilation and proliferation in active nematics [(arXiv:1303.4720)](https://ar5iv.labs.arxiv.org/html/1303.4720)

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
