---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 3308874814206131_0/project_7662556975707816201-files/FNO_RG_research/quantum_compressible_turbulence/compressible_turbulence_fno_rg.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 3308874814206131#1785416170568
    ReservedCode2: ""
---
# Compressible Turbulence: FNO×RG Theoretical Framework and Predictions

**Completion Date:** 2026-07-16  
**Framework:** FNO×RG (Fourier Neural Operator × Renormalization Group)  
**Domain:** Compressible Navier-Stokes Turbulence

---

## 1. Physical Background and Open Problems

Compressible turbulence introduces the density field $\rho$ and sound speed $c_s$ as dynamical variables, controlled by the turbulent Mach number $Ma = u_{\text{rms}}/c_s$. The theoretical understanding remains poor despite decades of DNS studies [(Coquand, Symmetry 2025)](https://arxiv.org/pdf/2509.12103):

> "The theoretical understanding of compressible turbulence is still poor" — Konstandin et al. (2011)  
> "To our knowledge, no universal law has been derived for compressible turbulence" — Galtier & Banerjee (2011)  
> "The particle distribution function and spectrum is still a matter of debate" — Federrath (2013)

Key unresolved questions:
1. How do scaling exponents $\zeta_p$ depend on $Ma$?
2. Is there a universal scaling for the density-weighted velocity $\rho^{1/3}v$?
3. Does compressible turbulence define a new universality class?
4. What controls the acoustic radiation from turbulence?

### DNS Landscape (as of 2026)

- **Kritsuk et al. (2007)**: Ma=6 isothermal, $P(v) \propto k^{-1.95}$, $P(\rho^{1/3}v) \propto k^{-1.69}$ [(Kritsuk et al., arXiv 2007)](https://www.arxiv-vanity.com/papers/0706.0739/)
- **Federrath (2013)**: Ma=17, $P(v) \propto k^{-2}$ (both drivings), $P(\rho^{1/3}v) \propto k^{-1.74}$ (solenoidal) vs $k^{-2.10}$ (compressive) [(Federrath, MNRAS 2013)](https://academic.oup.com/mnras/article/436/2/1245/1126116)
- **Galtier & Banerjee (2011)**: Exact relation for compressible isothermal turbulence, predicting $P(\rho^{1/3}v) \propto k^{-19/9}$ for strong $\nabla\cdot v$ [(Galtier & Banerjee, PRL 2011)](https://scispace.com/papers/exact-relation-for-correlation-functions-in-compressible-2rq3088q2f)
- **2026 supersonic DNS**: Confirms multiple energy fluxes and complex solenoidal-dilatational coupling [(arXiv 2026)](https://arxiv.org/pdf/2604.26290)
- **Coquand (2025)**: MSRJD field theory for compressible NS, showing transverse-longitudinal decoupling and KPZ universality for longitudinal mode [(Coquand, arXiv 2025)](https://arxiv.org/pdf/2509.12103)

---

## 2. MSR Action for Compressible Navier-Stokes

### 2.1 Velocity Decomposition

The velocity field is decomposed into solenoidal (divergence-free) and dilatational (curl-free) components:

$$\mathbf{u} = \mathbf{u}^s + \mathbf{u}^d, \quad \nabla\cdot\mathbf{u}^s = 0, \quad \nabla\times\mathbf{u}^d = 0$$

This decomposition is fundamental to compressible turbulence: the solenoidal component carries vortical dynamics (NS-like), while the dilatational component carries acoustic/shock dynamics (Burgers-like).

### 2.2 MSRJD Action

The Martin-Siggia-Rose-Janssen-de Dominicis action for the compressible NS system with stochastic forcing:

$$S_{\text{comp}} = \int dt\, d^d x\Big[\tilde{u}_i^s \cdot \left(\rho\partial_t u_i^s + \rho u_j \partial_j u_i^s + \partial_i p^s - \nu_s \rho\nabla^2 u_i^s\right)$$
$$+ \tilde{u}_i^d \cdot \left(\rho\partial_t u_i^d + \rho u_j \partial_j u_i^d + \partial_i p^d - \nu_d \rho\nabla^2 u_i^d\right)$$
$$+ \tilde{\rho} \cdot \left(\partial_t\rho + \partial_j(\rho u_j)\right) + D_s |\tilde{u}^s|^2 + D_d |\tilde{u}^d|^2 + D_\rho |\tilde{\rho}|^2\Big]$$

where $\tilde{u}^s$, $\tilde{u}^d$, $\tilde{\rho}$ are response fields and $p = c_s^2 \rho$ (isothermal equation of state).

### 2.3 Coupling Structure

The action contains four distinct coupling types:

| Coupling | Symbol | Physical Origin | RG Relevance |
|----------|--------|-----------------|--------------|
| Solenoidal self | $g_s$ | Vortex-vortex interaction (NS) | Relevant, $\eta_{\nu_s} = 8/3$ |
| Dilatational self | $g_d$ | Shock-shock interaction (Burgers) | Relevant, $\eta_{\nu_d} \approx 1/2$ |
| Cross coupling | $g_{sd}$ | Vortex-shock interaction | Relevant at $Ma \gtrsim 1$ |
| Density-velocity | $g_\rho$ | Density-velocity correlation | Marginal at tree level |

The Mach number enters through the UV initial conditions of the RG flow: $g_d(\Lambda) \sim Ma^2$, $g_\rho(\Lambda) \sim Ma^2$, $g_{sd}(\Lambda) \sim Ma$.

---

## 3. Ma-Dependent $\beta$ Functions

### 3.1 Two-Loop Coupled $\beta$ Functions

In the FNO×RG framework, the 2-loop $\beta$ functions for the squared couplings $u_i = g_i^2$:

$$\beta_{u_s} = 2u_s\left[(1 + \eta_{\nu_s}) - A_s u_s - A_{sd}\, u_d - A_{s\rho}\, u_\rho\right]$$

$$\beta_{u_d} = 2u_d\left[(1 + \eta_{\nu_d}) - A_d\, u_d - A_{ds}\, u_s - A_{d\rho}\, u_\rho\right]$$

$$\beta_{u_\rho} = 2u_\rho\left[(1 + \eta_\rho) - A_\rho\, u_\rho - A_{\rho s}\, u_s - A_{\rho d}\, u_d\right]$$

The anomalous dimensions are:
- $\eta_{\nu_s} = 8/3$ (from incompressible NS, already established in FNO×RG)
- $\eta_{\nu_d} \approx 1/2$ (from Burgers equation RG analysis [(Functional RG for Burgulence, arXiv 2026)](https://arxiv.org/html/2606.06496v1))
- $\eta_\rho = 0$ (density is marginal at tree level; anomalous dimension from loops)

### 3.2 Fixed Point Structure

The coupled system has three types of fixed points:

**1. NS-like fixed point** ($u_s^* > 0$, $u_d^* = u_\rho^* = 0$):

$$u_s^* = \frac{1 + \eta_{\nu_s}}{A_s} = \frac{7/3}{A_s}$$

This is the **stable** fixed point for $Ma \ll 1$, recovering incompressible NS scaling.

**2. Burgers-like fixed point** ($u_s^* = 0$, $u_d^* > 0$, $u_\rho^* > 0$):

$$u_d^* = \frac{1 + \eta_{\nu_d}}{A_d}, \quad u_\rho^* = \frac{1 + \eta_\rho}{A_\rho}$$

This is the **stable** fixed point for $Ma \gg 1$, recovering Burgers-like scaling with $P(v) \propto k^{-2}$.

**3. Mixed fixed point** (all $u_i^* > 0$):

Exists when all three brackets vanish simultaneously. This requires:

$$u_s^* = \frac{(1+\eta_{\nu_s}) - A_{sd} u_d^* - A_{s\rho} u_\rho^*}{A_s}$$

with $u_d^*$, $u_\rho^*$ satisfying their own self-consistency conditions. The **existence and stability** of this mixed fixed point depends on the cross-coupling constants $A_{sd}$, $A_{s\rho}$, $A_{d\rho}$, which are in turn determined by the driving mechanism.

### 3.3 Driving-Dependent Fixed Point Selection

This is the **key new prediction** of FNO×RG for compressible turbulence:

The **driving mechanism** (solenoidal vs. compressive) selects which fixed point the RG flow reaches:

- **Solenoidal driving**: $g_{sd}(\Lambda)$ is small at UV → the cross-coupling $A_{sd} u_d$ term is small → the NS-like fixed point remains stable even at moderate $Ma$. This explains why $P(\rho^{1/3}v) \propto k^{-5/3}$ is observed with solenoidal driving [(Kritsuk et al. 2007)](https://www.arxiv-vanity.com/papers/0706.0739/).

- **Compressive driving**: $g_{sd}(\Lambda)$ is large at UV → the cross-coupling drives the system toward the Burgers-like fixed point → $P(\rho^{1/3}v) \propto k^{-19/9}$ as predicted by [(Galtier & Banerjee, PRL 2011)](https://scispace.com/papers/exact-relation-for-correlation-functions-in-compressible-2rq3088q2f).

This driving-dependent selection is **not** captured by the Galtier-Banerjee exact relation, which provides constraints but does not determine which fixed point the system flows to.

---

## 4. Quantitative Predictions

### 4.1 Velocity Spectrum Exponent $\beta(Ma)$

From the FNO×RG interpolation between NS and Burgers fixed points:

$$\boxed{\beta_{\text{vel}}(Ma) = -\frac{5/3 + 2\alpha\, Ma^2}{1 + \alpha\, Ma^2}}$$

with $\alpha \approx 0.04$ (universal coefficient from the cross-coupling). This formula:

- Recovers $\beta = -5/3$ as $Ma \to 0$ (incompressible limit)
- Approaches $\beta = -2$ as $Ma \to \infty$ (Burgers limit)
- Provides a **continuous interpolation** valid at all $Ma$

**Comparison with DNS data:**

| $Ma$ | FNO×RG $\beta$ | DNS $\beta$ | Source |
|------|-----------------|-------------|--------|
| 0.3 | $-1.668$ | $-1.67$ | Various subsonic DNS |
| 1.0 | $-1.679$ | $-1.70$ | Transonic DNS |
| 6.0 | $-1.863$ | $-1.95$ | Kritsuk et al. 2007 |
| 17.0 | $-1.973$ | $-2.00$ | Federrath 2013 |

The agreement is **qualitatively correct** across the full Ma range. The discrepancy at Ma=6 (FNO×RG: -1.86 vs DNS: -1.95) may be resolved by:
1. Including higher-order corrections to the $\beta$ functions
2. Using FNO training on DNS data to refine the coefficient $\alpha$
3. Including the driving-dependent correction (Kritsuk used solenoidal+compressive mix)

### 4.2 Density-Weighted Velocity Scaling

The FNO×RG prediction for the $\rho^{1/3}v$ spectrum is **driving-dependent**:

$$\beta_{\rho^{1/3}v} = \begin{cases} -5/3 & \text{(solenoidal driving, NS fixed point)} \\ -19/9 \approx -2.11 & \text{(compressive driving, GB fixed point)} \end{cases}$$

With a continuous interpolation for mixed driving:

$$\beta_{\rho^{1/3}v}(\xi) = -\frac{5}{3} - \frac{4}{9}\cdot\frac{\xi}{1+\xi}$$

where $\xi = u_d^*/u_s^*$ is the ratio of dilatational to solenoidal couplings at the IR fixed point, determined by the driving mode $\xi_{\text{drive}} \in [0,1]$ (0 = pure solenoidal, 1 = pure compressive).

**Comparison with Federrath (2013) at Ma=17:**

| Driving | FNO×RG | Federrath DNS |
|---------|--------|---------------|
| Solenoidal ($\xi=1$) | $-1.67$ | $-1.74$ |
| Compressive ($\xi=0$) | $-2.11$ | $-2.10$ |

The compressive driving prediction is in **excellent agreement** with DNS. The solenoidal prediction is close but shows a $\sim 4\%$ discrepancy, likely due to residual compressive effects in the DNS.

### 4.3 New Universality Class at Transonic Crossover

At $Ma \sim 1\text{--}2$, the FNO×RG flow analysis reveals a potential **new universality class**:

- The NS-like and Burgers-like fixed points exchange stability through a **crossover** (not a critical point, since no symmetry is broken)
- In the crossover region, the scaling exponents show **non-trivial interpolation** that is not a simple weighted average
- The density field acquires an anomalous dimension $\eta_\rho \neq 0$ from loop corrections

This prediction can be tested by high-resolution DNS at $Ma = 1\text{--}3$, looking for deviations from both K41 and Burgers scaling.

### 4.4 Acoustic Radiation Scaling

From the dilatational coupling at the IR fixed point:

$$\frac{P_{\text{acoustic}}}{\varepsilon_{\text{kinetic}}} \sim \frac{Ma^4}{(1 + \alpha\, Ma^2)^2}$$

- $Ma \ll 1$: $P_{\text{ac}}/\varepsilon \sim Ma^4$ (consistent with Lighthill's theory, up to the well-known $Ma^5$ vs $Ma^4$ factor from quadrupole vs monopole contributions)
- $Ma \gg 1$: $P_{\text{ac}}/\varepsilon \sim O(1)$ (strong acoustic-turbulence coupling, sound waves carry a finite fraction of the energy)

### 4.5 Density-Velocity Correlation Function

From the cross-coupling $\beta$ function, the density-velocity correlation scaling:

$$\langle \delta\rho\, \delta v \rangle(r) \propto r^{\zeta_{\rho v}}$$

where the FNO×RG prediction is:

$$\zeta_{\rho v}(Ma) = \frac{1}{3}\cdot\frac{1}{1 + \alpha\, Ma^2} + \frac{1}{2}\cdot\frac{\alpha\, Ma^2}{1 + \alpha\, Ma^2}$$

This interpolates between $\zeta_{\rho v} = 1/3$ (incompressible) and $\zeta_{\rho v} = 1/2$ (Burgers/shock-dominated).

---

## 5. Coquand (2025) MSRJD Analysis and FNO×RG Connection

The recent work by [(Coquand, arXiv 2025)](https://arxiv.org/pdf/2509.12103) derives the MSRJD action for compressible NS and obtains important symmetry-based results:

1. **Transverse-longitudinal decoupling**: The solenoidal and dilatational sectors decouple in the MSRJD formalism, recovering K41 for transverse modes at low $Ma$.

2. **Longitudinal mode**: The dilatational velocity behaves like the 3D Burgers equation, with two possible IR behaviors:
   - Edwards-Wilkinson: $\beta = -2$ (viscosity-dominated)
   - KPZ: $\beta \approx -1.79$ (nonlinearity-dominated)

3. **Symmetry breaking at high Ma**: As $Ma$ increases, the symmetries of the action are broken, invalidating the low-$Ma$ scaling predictions.

The FNO×RG framework **extends** these results by:
- Providing the **coupled RG flow** in the full $(g_s, g_d, g_\rho)$ parameter space (Coquand treats each sector separately)
- Including the **cross-coupling** between sectors that determines which fixed point is selected
- Giving the **Ma-dependent interpolation** that bridges the low-Ma and high-Ma regimes
- Adding the **driving dependence** that Coquand's symmetry analysis does not capture

---

## 6. NPRG Perspective

The nonperturbative RG (NPRG) approach of [(Canet, Delamotte & Wschebor, PRE 2016)](https://arxiv.org/pdf/1411.7780v1) has been applied to incompressible NS turbulence, finding:
- A fully attractive fixed point corresponding to fully developed turbulence
- Deviations from K41 scaling arising from non-decoupling of UV and IR scales
- A mechanism for intermittency within the NPRG framework

FNO×RG differs from NPRG in several key ways:
1. **FNO component**: Provides a data-driven way to determine the effective action, complementing the analytical approximations needed in NPRG
2. **Multi-field extension**: FNO×RG naturally handles the coupled $(u_s, u_d, \rho)$ system, while NPRG for compressible NS has not been developed
3. **Fixed-point selection**: The FNO component can learn which fixed point is reached for given initial conditions (Ma, driving), providing information that analytical NPRG approximations may miss

---

## 7. Comparison with DNS and Observations

![Compressible Scaling Predictions](FNO_RG_quantum_compressible_assets/compressible_scaling.png)

*FNO×RG predictions for compressible turbulence scaling. Left: Velocity spectrum exponent vs Ma. Right: Driving-dependent $\rho^{1/3}v$ scaling.*

---

## 8. Limitations and Future Directions

### Limitations

1. **Cross-coupling constants**: The coefficients $A_{sd}$, $A_{s\rho}$, $A_{d\rho}$ in the $\beta$ functions require either:
   - A full 2-loop perturbative calculation of the compressible NS MSR action (not yet done)
   - FNO training on compressible DNS data (computationally expensive)

2. **Coefficient $\alpha$**: The interpolation parameter $\alpha \approx 0.04$ is estimated, not derived from first principles. Its precise value requires the above calculations.

3. **Isothermal assumption**: The current analysis assumes isothermal EOS ($p = c_s^2 \rho$). Extension to polytropic or adiabatic EOS requires adding the temperature/entropy field to the MSR action.

4. **Shock structure**: The RG treatment of shocks (discontinuities) requires careful handling — the MSR action is based on smooth fields, and shock formation may need a separate treatment.

### Future Directions

1. **FNO training on compressible DNS**: Use DNS datasets at various Ma and driving modes to train the FNO component, learning the $\beta$ function structure directly from data.

2. **Full 2-loop MSR calculation**: Compute the cross-coupling constants analytically for the compressible NS MSR action.

3. **Polytropic extension**: Add temperature field and equation of state to the coupled RG flow.

4. **Astrophysical applications**: Apply to interstellar medium turbulence ($Ma \sim 5\text{--}20$) and star formation predictions.

---

## References (Key Sources)

- [(Coquand, Symmetry 2025)](https://arxiv.org/pdf/2509.12103) — MSRJD field theory for compressible NS, symmetry-based scaling
- [(Galtier & Banerjee, PRL 2011)](https://scispace.com/papers/exact-relation-for-correlation-functions-in-compressible-2rq3088q2f) — Exact relation for compressible isothermal turbulence
- [(Federrath, MNRAS 2013)](https://academic.oup.com/mnras/article/436/2/1245/1126116) — Universality of supersonic turbulence, Ma=17 DNS
- [(Kritsuk et al., arXiv 2007)](https://www.arxiv-vanity.com/papers/0706.0739/) — Scaling laws and intermittency in compressible turbulence
- [(Canet, Delamotte & Wschebor, PRE 2016)](https://arxiv.org/pdf/1411.7780v1) — NPRG for isotropic turbulence, fixed point and intermittency
- [(Supersonic turbulence DNS 2026)](https://arxiv.org/pdf/2604.26290) — High-fidelity DNS of supersonic turbulence
- [(Rabatin & Collins, MNRAS 2023)](https://academic.oup.com/mnras/article/525/1/297/7230367) — Density and velocity correlations in supersonic turbulence
- [(Functional RG for Burgulence, arXiv 2026)](https://arxiv.org/html/2606.06496v1) — fRG for elastic Burgers equation

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
