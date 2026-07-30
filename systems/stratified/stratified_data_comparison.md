---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 3308874814206131_0/project_7662556975707816201-files/FNO_RG_research/stratified_turbulence/stratified_data_comparison.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 3308874814206131#1785416188525
    ReservedCode2: ""
---
# FNO×RG Stratified Turbulence: DNS/Experimental Data Comparison

**Date**: 2026-07-16  
**Framework**: FNO×RG Predictions vs. Published DNS/Experimental/Observational Data

---

## 1. Spectral Index Comparisons

### 1.1 Horizontal Kinetic Energy Spectrum E(k_h)

**FNO×RG Prediction** (at BO fixed point, moderate stratification):
- E_v(k) ~ k^{-11/5} = k^{-2.2} (isotropic, angle-averaged)
- E_v(k_h) ~ k_h^{-5/3} ≈ k_h^{-1.67} (horizontal, strong stratification)

| Study | Grid | Re_b | Fr | Observed E(k_h) slope | FNO×RG prediction | Match? |
|-------|------|------|-----|----------------------|-------------------|--------|
| Lindborg (2006) [(Lindborg, JFM 550, 207-242, 2006)](https://doi.org/10.1017/S0022112005008128) | Hyperviscosity | High | ~0.01 | k_h^{-5/3} | k_h^{-5/3} (FP3: re-entrant K41) | ✓ |
| Brethouwer et al. (2007) [(Brethouwer et al., JFM 585, 343-368, 2007)](https://doi.org/10.1017/S0022112007006854) | 512²×128 to 1024²×512 | 0.4-9.6 | 0.01-0.1 | k_h^{-5/3} for R>>1 | k_h^{-5/3} (FP3) | ✓ |
| Rosenberg et al. (2015) [(Rosenberg et al., Phys. Fluids 27, 055105, 2015)](https://doi.org/10.1063/1.4921076) | 4096³ | 32 | 0.024 | BO: k^{-11/5} at large scales | k^{-11/5} (FP2) | ✓ |
| de Bruyn Kops (2015) [(de Bruyn Kops, JFM 775, 436-463, 2015)](http://people.umass.edu/debk/Papers/debk15.pdf) | 8192×8192×4096 | 13-220 | Low | KOC: k^{-5/3} at Re_b=220 | k^{-5/3} (FP1 recovery) | ✓ |
| Bartello & Tobias (2013) [(cited in Alam 2025)](https://doi.org/10.1017/jfm.2013.170) | Various | Varied | Varied | k_h^{-5/3} at high Re_b | k_h^{-5/3} (FP3) | ✓ |
| Kitamura & Matsuda (2006) [(Kitamura & Matsuda, GRL 33, L05809, 2006)](https://doi.org/10.1029/2005GL024996) | Nonhydrostatic | N/A | N/A | k_H^{-3} (synoptic), k_H^{-5/3} (mesoscale) | k_H^{-3} (enstrophy cascade), k_H^{-5/3} (energy cascade) | ✓ |
| Song et al. (2026) [(Song et al., arXiv:2606.09490)](https://arxiv.org/abs/2606.09490) | 512²×128 | 0.06-2300 | 0.01-1 | k_⊥^{-5/3} at high R_{IB} | k_⊥^{-5/3} (FP3) | ✓ |

**Summary**: The FNO×RG three-FP structure correctly captures the observed spectra across the full parameter range. The k^{-11/5} BO spectrum is observed in the 4096³ DNS by Rosenberg et al. (2015) at large scales, while the k^{-5/3} spectrum is observed at small scales (below Ozmidov) and in the horizontal direction of strongly stratified flows.

### 1.2 Vertical Kinetic Energy Spectrum E(k_z)

**FNO×RG Prediction**: E(k_z) ~ k_z^{-3} for strongly stratified flows (FP3)

| Study | Observed E(k_z) slope | FNO×RG prediction | Match? |
|-------|----------------------|-------------------|--------|
| Brethouwer et al. (2007) | k_z^{-3} | k_z^{-3} (FP3) | ✓ |
| Lindborg (2006) | k_z^{-3} | k_z^{-3} | ✓ |
| Cot (2001) atmospheric obs. | k_z^{-3} | k_z^{-3} | ✓ |

### 1.3 Angle-Averaged (Isotropic) Spectrum

**FNO×RG Prediction**: E(k) ~ k^{-11/5} at the BO fixed point (Fr ~ O(1))

| Study | Method | Observed slope | FNO×RG prediction | Match? |
|-------|--------|---------------|-------------------|--------|
| Kimura & Herring (1996) | DNS | k^{-11/5} | k^{-11/5} (FP2) | ✓ |
| Kumar, Chatterjee & Verma (2014) [(Kumar et al., Phys. Rev. E 90, 023016, 2014)](https://doi.org/10.1103/PhysRevE.90.023016) | DNS | k^{-11/5} | k^{-11/5} | ✓ |
| Kumar & Verma (2015) [(Kumar & Verma, Phys. Rev. E 91, 043014, 2015)](https://doi.org/10.1103/PhysRevE.91.043014) | Shell model | k^{-11/5} | k^{-11/5} | ✓ |
| Bhattacharjee (2015) [(cited in Alam 2019)](https://doi.org/10.1016/j.physleta.2014.12.035) | Theory | k^{-11/5} | k^{-11/5} | ✓ |
| Bhattacharjee (2022) [(Bhattacharjee, Phil. Trans. R. Soc. A 380, 20210075)](https://doi.org/10.1098/rsta.2021.0075) | Stirred model | k^{-11/5} with K_0 ~ O(0.1) | k^{-11/5} with small amplitude | ✓ |

**Note on the dual scaling controversy**: Alam, Guha & Verma (2019) [(Alam et al., JFM 875, 961-973, 2019)](https://doi.org/10.1017/jfm.2019.529) challenge the BO prediction of a k^{-5/3} recovery at k > k_B. They argue that the velocity field is too weak at small scales to sustain constant kinetic energy flux, and thus the k^{-5/3} regime is absent. The FNO×RG framework is consistent with this: at the BO fixed point, the kinetic energy flux Π_v(k) ~ k^{-4/5} decreases, and there is no reason for it to become constant unless Re_b is large enough for a separate K41 range to develop below the Ozmidov scale. This is a **nuanced point** that requires careful scale separation.

---

## 2. Froude Number Scaling

### 2.1 Vertical Length Scale l_v

**FNO×RG Prediction**: l_v/l_h ~ Fr (for Re_b >> 1); l_v/l_h ~ Re^{-1/2} (for Re_b << 1)

| Study | Re_b | Observed l_v scaling | FNO×RG prediction | Match? |
|-------|------|---------------------|-------------------|--------|
| Brethouwer et al. (2007) | 0.1-9.6 | l_v ~ U/N for R>>1; l_v ~ l_h Re^{-1/2} for R<<1 | Same | ✓ |
| Billant & Chomaz (2001) | Various | l_v ~ U/N | l_v/l_h ~ Fr | ✓ |

### 2.2 Vertical Velocity Scaling w_rms

**FNO×RG Prediction**: 
- SSA (Billant-Chomaz): w ~ Fr·U (outside turbulent patches)
- MSA (Chini et al.): w ~ Fr^{1/2}·U (within turbulent patches)

| Study | Method | Observed scaling | FNO×RG context | Match? |
|-------|--------|-----------------|----------------|--------|
| Maffioli & Davidson (2016) [(cited in Garaud et al. 2024)](https://doi.org/10.1017/jfm.2015.667) | DNS | w ~ Fr^{1/2} (tentative) | MSA prediction | ✓ (tentative) |
| Garaud et al. (2024) [(Garaud et al., arXiv:2404.05896)](https://arxiv.org/html/2404.05896v2) | DNS | w ~ Fr^{1/2} in patches; w ~ Fr outside | Both MSA and SSA | ✓ |
| Brethouwer et al. (2007) | DNS | w ~ Fr (SSA) | SSA | ✓ |

**Critical note**: The FNO×RG framework predicts that **both scalings coexist** in the same flow, with the Fr^{1/2} scaling dominating within active turbulent patches and the Fr scaling applying in the quiescent (non-turbulent) regions. The domain-averaged w_rms then depends on the filling factor φ_turb:

```
w_rms² ~ φ_turb · Fr · U² + (1 - φ_turb) · Fr² · U²
```

This explains the apparent discrepancy between different DNS studies — the effective exponent depends on Re_b (which controls φ_turb).

---

## 3. Intermittency Parameters

### 3.1 Velocity Intermittency Exponent μ_v

**FNO×RG Prediction**: μ_v ≈ 0.25 ± 0.05 (at scales near Taylor microscale)

| Study | Re_b | Observed μ_v | FNO×RG prediction | Match? |
|-------|------|-------------|-------------------|--------|
| de Bruyn Kops (2015) | 48-220 | 0.25 ± 0.05 | ~0.25 | ✓ |
| de Bruyn Kops (2015) | 13 | Higher (bimodal) | > 0.25 (predicted due to patchiness) | ✓ (qualitative) |

**Note**: No broad inertial range was found in the DNS, so the intermittency exponents are measured near the Taylor scale, not in a true inertial range. The FNO×RG prediction for the true inertial-range μ_v requires higher Re_b simulations.

### 3.2 Scalar/Buoyancy Intermittency Exponent μ_b

**FNO×RG Prediction**: μ_b ≈ 0.35 ± 0.1

| Study | Re_b | Observed μ_b | FNO×RG prediction | Match? |
|-------|------|-------------|-------------------|--------|
| de Bruyn Kops (2015) | 48-220 | 0.35 ± 0.1 | ~0.35 | ✓ |
| Mydlarski & Warhaft (1998) [(cited in de Bruyn Kops 2015)] | Grid turb. | ~0.2 | Lower (passive scalar) | Consistent (stratification enhances) |

### 3.3 Dissipation Rate PDFs

**FNO×RG Prediction**: Bimodal PDFs at moderate Re_b, lognormal at high Re_b

| Study | Re_b | Observed PDF shape | FNO×RG prediction | Match? |
|-------|------|-------------------|-------------------|--------|
| de Bruyn Kops (2015) | 48-220 | Lognormal for ε, χ at Re_b ≥ 48 | Lognormal | ✓ |
| de Bruyn Kops (2015) | 13 | Bimodal for ε, χ | Bimodal | ✓ |

---

## 4. Anisotropy Data

### 4.1 Scale-Dependent Anisotropy

**FNO×RG Prediction**: Anisotropy increases with scale above k_{Oz}, decreases toward isotropy below k_{Oz}. Re_b > 500 needed for same small-scale isotropy as unstratified turbulence.

| Study | Re_b | Key finding | FNO×RG prediction | Match? |
|-------|------|-------------|-------------------|--------|
| Lang & Waite (2019) [(Lang & Waite, Phys. Rev. Fluids 4, 044801, 2019)](https://doi.org/10.1103/PhysRevFluids.4.044801) | Up to 50 | Re_b > 500 needed for isotropy; Ozmidov-scale eddies become more isotropic with Re_b | Same trend | ✓ |
| Garanaik & Venayagamoorthy (2018) [(Garanaik & Venayagamoorthy, Phys. Fluids 30, 126602, 2018)](https://doi.org/10.1063/1.5055871) | Various | Small-scale isotropy for Fr > 1; anisotropy for Fr < O(1) | Same | ✓ |

### 4.2 Axisymmetric Spectral Data

| Study | Fr | Observed spectral anisotropy | FNO×RG prediction |
|-------|-----|------------------------------|-------------------|
| Song et al. (2026) | 0.004-0.224 | Energy concentrated along k_∥ ≈ 5k_⊥ at strong stratification; isotropic at Fr=∞ | Consistent with FP3→FP1 crossover |
| Song et al. (2026) | 0.013 | E(k_⊥) ~ k_⊥^{-5/3} at high k_⊥ | k_⊥^{-5/3} (FP3) |
| Song et al. (2026) | 0.004 | E(k_∥) steep, ~k_∥^{-3} | k_∥^{-3} (FP3) |

---

## 5. Buoyancy Reynolds Number Dependence

### 5.1 Regime Boundaries

**FNO×RG Prediction**: Three regimes controlled by Re_b = Fr²·Re

| Re_b | FNO×RG regime | DNS observations |
|------|---------------|-----------------|
| Re_b << 1 | Viscously dominated (no turbulence) | Confirmed by [(Brethouwer et al. 2007)](https://doi.org/10.1017/S0022112007006854) |
| Re_b ~ O(1)-O(10) | LAST regime (layered anisotropic stratified turbulence) | Confirmed by [(Falder, White & Caulfield 2016)](https://doi.org/10.1017/S0022112005008128); [(de Bruyn Kops 2015)](http://people.umass.edu/debk/Papers/debk15.pdf) |
| Re_b >> O(10) | Forward cascade with partial isotropy recovery below k_{Oz} | Confirmed by [(Rosenberg et al. 2015)](https://doi.org/10.1063/1.4921076) (Re_b=32) |

### 5.2 Bolgiano-Obukhov vs. K41 at Different Re_b

| Study | Re_b | Fr | Dominant spectrum | FNO×RG FP |
|-------|------|-----|-------------------|-----------|
| Rosenberg et al. (2015) | 32 | 0.024 | BO at large scales, K41 at small scales | FP2 → FP1 |
| de Bruyn Kops (2015) | 220 | Low | KOC (Kolmogorov-Obukhov-Corrsin) | FP1 |
| Brethouwer et al. (2007) | 0.4-9.6 | 0.01-0.1 | k_h^{-5/3} for R>>1 | FP3 |
| Kumar et al. (2014) | N/A (shell) | Fr ~ 1 | k^{-11/5} | FP2 |

---

## 6. Atmospheric and Oceanic Observations

### 6.1 Atmospheric Spectra

| Observation | Source | Spectral slope | FNO×RG regime |
|-------------|--------|---------------|---------------|
| Nastrom & Gage (1985) | Commercial aircraft | k_h^{-3} (synoptic), k_h^{-5/3} (mesoscale) | FP3: enstrophy cascade + energy cascade |
| Lindborg (2007) | Upper troposphere | k_h^{-5/3} for divergence spectrum | FP3: forward cascade |
| Cho et al. (1999) | Aircraft | k_h^{-5/3} at mesoscale, latitude-independent | FP3 |

### 6.2 Oceanic Observations

| Observation | Source | Finding | FNO×RG context |
|-------------|--------|---------|----------------|
| Ocean microstructure | Various | Fr ~ O(10^{-4})-O(10^{-2}), Re_b varies widely | Full FP1→FP2→FP3 landscape |
| Internal wave continuum | MU radar, etc. | Wave spectrum distinct from turbulence | IGW contribution in §5 of derivation |

---

## 7. Points of Tension and Unresolved Issues

### 7.1 BO k^{-11/5} Spectrum: Rarely Observed in Isotropic Form

The angle-averaged k^{-11/5} spectrum is **difficult to observe** in DNS and experiments. The randomly stirred model [(Bhattacharjee 2022)](https://doi.org/10.1098/rsta.2021.0075) provides a reason: the amplitude K_0 ~ O(0.1) is much smaller than the Kolmogorov constant C_K ≈ 1.6, making the BO range hard to distinguish from the K41 range with limited dynamic range.

**FNO×RG status**: The FNO×RG correctly predicts the BO spectrum but acknowledges the practical difficulty of observing it. The key test is the **decreasing kinetic energy flux** Π_v(k) ~ k^{-4/5}, which is a more robust signature than the spectral slope alone. This was confirmed by [(Kumar et al. 2014)](https://doi.org/10.1103/PhysRevE.90.023016) and shell model results.

### 7.2 Dual Scaling (k^{-11/5} → k^{-5/3}): Controversial

The original BO phenomenology predicts a dual scaling with a transition at k_B. However:
- Alam, Guha & Verma (2019) argue the k^{-5/3} recovery is **absent** in moderate stratification.
- The FNO×RG framework resolves this by noting that the K41 recovery requires **sufficient scale separation** between k_{Oz} and k_η, i.e., Re_b >> 1. At moderate Re_b, there is no separate K41 range.

**Verdict**: The FNO×RG prediction is consistent with data: the k^{-5/3} recovery is **conditional on high Re_b**, not a universal feature of BO scaling.

### 7.3 Re-entrant K41 at Strong Stratification

The Basu-Bhattacharjee (2019) prediction of re-entrant K41 for horizontal spectra at very strong stratification is a striking FNO×RG prediction (FP3). Direct confirmation from DNS is limited because:
- Very strong stratification (Fr << 0.01) requires extremely high Re to maintain Re_b > 1.
- Most DNS at low Fr have Re_b ~ O(1) or less, where viscous effects dominate.

**Status**: The re-entrant K41 is a **falsifiable prediction** that requires DNS at Re > 10⁵ with Fr < 0.01.

### 7.4 Vertical Velocity Scaling: Fr vs Fr^{1/2}

The coexistence of w ~ Fr (SSA/Billant-Chomaz) and w ~ Fr^{1/2} (MSA/Chini et al.) in the same flow is a nontrivial prediction. The Garaud et al. (2024) DNS provides the first comprehensive verification, showing that:
- Within turbulent patches: w ~ Fr^{1/2}
- Outside patches: w ~ Fr
- Domain average: intermediate scaling

**FNO×RG status**: The FNO×RG framework naturally accommodates both scalings through the concept of spatially intermittent (patchy) turbulence. The filling factor φ_turb bridges the two limits.

---

## 8. Quantitative Scorecard

| Prediction | Data sources | Verification level |
|------------|-------------|-------------------|
| E(k) ~ k^{-11/5} (BO, Fr~1) | Shell models, DNS (Kumar 2014, Rosenberg 2015) | **Confirmed** (limited range) |
| E(k_h) ~ k_h^{-5/3} (strong strat.) | Lindborg 2006, Brethouwer 2007, de Bruyn Kops 2015 | **Strongly confirmed** |
| E(k_z) ~ k_z^{-3} (strong strat.) | Brethouwer 2007, atmospheric obs. | **Strongly confirmed** |
| l_v/l_h ~ Fr (Re_b >> 1) | Brethouwer 2007, Billant-Chomaz 2001 | **Strongly confirmed** |
| w ~ Fr (outside patches) | Brethouwer 2007, Garaud 2024 | **Confirmed** |
| w ~ Fr^{1/2} (inside patches) | Maffioli-Davidson 2016, Garaud 2024 | **Tentatively confirmed** |
| μ_v ≈ 0.25 | de Bruyn Kops 2015 | **Partial** (near Taylor scale only) |
| μ_b ≈ 0.35 | de Bruyn Kops 2015 | **Partial** |
| Bimodal dissipation PDFs | de Bruyn Kops 2015 | **Confirmed** |
| Re-entrant K41 at Fr << 1 | Limited DNS data | **Unconfirmed** (falsifiable prediction) |
| Γ ∝ Fr for 0.05 < Fr < 0.3 | Feraco et al. 2018 | **Tentatively confirmed** |
| K_0 ~ O(0.1) for BO | Bhattacharjee 2022 | **Consistent** (indirect) |

**Overall assessment**: The FNO×RG three-fixed-point structure (K41 → BO → 2D) is **well supported** by the existing DNS and observational data. The main quantitative predictions (spectral slopes, Froude scaling, anisotropy) are confirmed. The intermittency predictions and the re-entrant K41 at extreme stratification remain the most important **open predictions** requiring further verification.

---

## References

Full references in stratified_derivation.md. Key additional sources:

- Garaud, P., et al. (2024). Numerical validation of scaling laws for stratified turbulence. arXiv:2404.05896v2.
- Song, G., et al. (2026). Scaling laws and local enhancements of buoyancy flux. arXiv:2606.09490.
- Alam, S. (2025). Anisotropic energy transfers and vertical layering. Phys. Fluids 37, 095132.
- Feraco, F., et al. (2018). Vertical drafts and mixing in stratified turbulence. arXiv:1806.00342.

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
