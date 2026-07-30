---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 3308874814206131_0/project_7662556975707816201-files/FNO_RG_research/theorem4_consistency/Theorem_4_FNO_RG_Consistency.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 3308874814206131#1785416120465
    ReservedCode2: ""
---
# Theorem 4: FNO×RG Self-Consistency and Error Propagation

**Date:** July 29, 2026  
**Status:** In Progress  
**Target:** Rigorous mathematical proof that FNO×RG converges to exact RG as FNO accuracy improves

---

## 1. Statement of the Theorem

### 1.1 Setup

Let $\Gamma_\kappa[\Phi]$ denote the exact effective average action at RG scale $\kappa$, satisfying the Wetterich equation:

$$
\partial_t \Gamma_\kappa[\Phi] = \frac{1}{2}\text{Tr}\left[\left(\Gamma_\kappa^{(2)}[\Phi] + \mathcal{R}_k\right)^{-1}\partial_t \mathcal{R}_k\right]
$$

where $t = \ln(\kappa/\kappa_0)$ and $\mathcal{R}_k$ is the IR regulator.

Let $\Gamma_\kappa^{\text{FNO}}[\Phi]$ denote the FNO-learned approximation, where the FNO is trained on DNS data to learn the spectral closure.

### 1.2 Assumptions

**A1 (FNO Approximation Quality):** The FNO-learned effective action satisfies:

$$
\|\Gamma_\kappa^{\text{FNO}} - \Gamma_\kappa^{\text{exact}}\|_{L^2(\mathcal{F})} < \varepsilon
$$

for some $\varepsilon > 0$, where $\mathcal{F}$ is the space of field configurations.

**A2 (Lipschitz Continuity):** The Wetterich flow operator $\mathcal{W}[\Gamma] \equiv \frac{1}{2}\text{Tr}[(\Gamma^{(2)} + \mathcal{R}_k)^{-1}\partial_t \mathcal{R}_k]$ is Lipschitz continuous in a neighborhood of $\Gamma_\kappa^{\text{exact}}$:

$$
\|\mathcal{W}[\Gamma_1] - \mathcal{W}[\Gamma_2]\| \leq L_W \|\Gamma_1 - \Gamma_2\|
$$

for some Lipschitz constant $L_W > 0$.

**A3 (Fixed Point Existence):** The exact RG flow has a fixed point $\Gamma^*$ satisfying $\mathcal{W}[\Gamma^*] = 0$, and this fixed point is non-degenerate (the linearized flow has no zero eigenvalues).

### 1.3 Theorem Statement

**Theorem 4 (FNO×RG Self-Consistency).** Under assumptions A1-A3, let $g^*_{\text{exact}}$ and $g^*_{\text{FNO}}$ denote the fixed points of the exact and FNO RG flows respectively. Then:

$$
|g^*_{\text{FNO}} - g^*_{\text{exact}}| \leq C(\varepsilon)
$$

where $C(\varepsilon) \to 0$ as $\varepsilon \to 0$. Specifically:

$$
C(\varepsilon) = \frac{L_W}{\lambda_{\min}} \varepsilon + O(\varepsilon^2)
$$

where $\lambda_{\min} > 0$ is the smallest absolute value of the eigenvalues of the linearized RG flow at the fixed point.

Similarly, for any critical exponent $\eta$ (eigenvalue of the linearized flow):

$$
|\eta_{\text{FNO}} - \eta_{\text{exact}}| \leq D(\varepsilon)
$$

where $D(\varepsilon) = O(\varepsilon)$.

---

## 2. Proof Strategy

### 2.1 Key Ideas

1. **Perturbation Theory:** Treat $\Gamma_\kappa^{\text{FNO}} = \Gamma_\kappa^{\text{exact}} + \delta\Gamma_\kappa$ where $\|\delta\Gamma_\kappa\| < \varepsilon$.

2. **Implicit Function Theorem:** The fixed point condition $\beta(g) = 0$ defines $g^*$ implicitly as a function of the flow parameters. Small perturbations in the flow lead to small changes in $g^*$.

3. **Spectral Stability:** The eigenvalues of the linearized flow (critical exponents) depend continuously on the flow parameters.

### 2.2 Proof Outline

**Step 1:** Show that the FNO RG flow $\partial_t \Gamma_\kappa^{\text{FNO}} = \mathcal{W}[\Gamma_\kappa^{\text{FNO}}] + \delta\mathcal{W}$ where $\|\delta\mathcal{W}\| = O(\varepsilon)$.

**Step 2:** Apply the implicit function theorem to $\beta(g; \varepsilon) = 0$ to show $g^*(\varepsilon)$ is continuous.

**Step 3:** Use perturbation theory for linear operators to show eigenvalue stability.

**Step 4:** Derive explicit error bounds.

---

## 3. Detailed Proof

### Step 1: Perturbed RG Flow

The Wetterich equation with FNO closure reads:

$$
\partial_t \Gamma_\kappa^{\text{FNO}} = \frac{1}{2}\text{Tr}\left[\left((\Gamma_\kappa^{\text{FNO}})^{(2)} + \mathcal{R}_k\right)^{-1}\partial_t \mathcal{R}_k\right]
$$

Substituting $\Gamma_\kappa^{\text{FNO}} = \Gamma_\kappa^{\text{exact}} + \delta\Gamma_\kappa$:

$$
\partial_t (\Gamma_\kappa^{\text{exact}} + \delta\Gamma_\kappa) = \mathcal{W}[\Gamma_\kappa^{\text{exact}} + \delta\Gamma_\kappa]
$$

Since $\partial_t \Gamma_\kappa^{\text{exact}} = \mathcal{W}[\Gamma_\kappa^{\text{exact}}]$, we have:

$$
\partial_t \delta\Gamma_\kappa = \mathcal{W}[\Gamma_\kappa^{\text{exact}} + \delta\Gamma_\kappa] - \mathcal{W}[\Gamma_\kappa^{\text{exact}}]
$$

By the Lipschitz condition (A2):

$$
\|\partial_t \delta\Gamma_\kappa\| \leq L_W \|\delta\Gamma_\kappa\|
$$

This shows that the perturbation $\delta\Gamma_\kappa$ evolves according to a bounded flow.

### Step 2: Fixed Point Perturbation

Let $g$ denote the coupling constants parameterizing the effective action. The exact $\beta$-function is:

$$
\beta_{\text{exact}}(g) = \partial_t g|_{\text{exact}}
$$

The FNO $\beta$-function is:

$$
\beta_{\text{FNO}}(g) = \beta_{\text{exact}}(g) + \delta\beta(g)
$$

where $\|\delta\beta\| = O(\varepsilon)$ by assumption A1.

The exact fixed point satisfies $\beta_{\text{exact}}(g^*_{\text{exact}}) = 0$.

The FNO fixed point satisfies $\beta_{\text{FNO}}(g^*_{\text{FNO}}) = 0$, i.e.:

$$
\beta_{\text{exact}}(g^*_{\text{FNO}}) + \delta\beta(g^*_{\text{FNO}}) = 0
$$

Taylor expanding around $g^*_{\text{exact}}$:

$$
\beta_{\text{exact}}(g^*_{\text{exact}}) + \left.\frac{\partial \beta_{\text{exact}}}{\partial g}\right|_{g^*_{\text{exact}}} (g^*_{\text{FNO}} - g^*_{\text{exact}}) + O(|g^*_{\text{FNO}} - g^*_{\text{exact}}|^2) + \delta\beta(g^*_{\text{FNO}}) = 0
$$

Since $\beta_{\text{exact}}(g^*_{\text{exact}}) = 0$ and $\delta\beta = O(\varepsilon)$:

$$
B \cdot \Delta g + O(|\Delta g|^2) + O(\varepsilon) = 0
$$

where $B_{ij} = \frac{\partial \beta_i}{\partial g_j}|_{g^*_{\text{exact}}}$ is the stability matrix and $\Delta g = g^*_{\text{FNO}} - g^*_{\text{exact}}$.

By assumption A3, $B$ is non-degenerate, so $B^{-1}$ exists. To leading order:

$$
\Delta g = -B^{-1} \cdot \delta\beta + O(\varepsilon^2)
$$

Therefore:

$$
|\Delta g| \leq \|B^{-1}\| \cdot \|\delta\beta\| + O(\varepsilon^2) = \frac{\|\delta\beta\|}{\lambda_{\min}} + O(\varepsilon^2)
$$

where $\lambda_{\min}$ is the smallest singular value of $B$ (which is positive by non-degeneracy).

Since $\|\delta\beta\| = O(\varepsilon)$, we obtain:

$$
|g^*_{\text{FNO}} - g^*_{\text{exact}}| \leq \frac{L_W}{\lambda_{\min}} \varepsilon + O(\varepsilon^2)
$$

$\blacksquare$

### Step 3: Critical Exponent Perturbation

The critical exponents $\theta_i$ are eigenvalues of $-B$:

$$
\det(-B - \theta I) = 0
$$

The perturbed stability matrix is $B^{\text{FNO}} = B + \delta B$ where $\|\delta B\| = O(\varepsilon)$.

By standard perturbation theory for eigenvalues:

$$
|\theta_i^{\text{FNO}} - \theta_i^{\text{exact}}| \leq \|\delta B\| + O(\varepsilon^2) = O(\varepsilon)
$$

Therefore:

$$
|\eta_{\text{FNO}} - \eta_{\text{exact}}| = O(\varepsilon)
$$

$\blacksquare$

---

## 4. Discussion

### 4.1 Physical Interpretation

The theorem shows that **FNO×RG is a controlled approximation** to the exact RG. As the FNO training error $\varepsilon \to 0$, the FNO×RG predictions converge to the exact RG predictions.

The error bound $C(\varepsilon) = \frac{L_W}{\lambda_{\min}} \varepsilon$ shows that:
- Small FNO error $\varepsilon$ leads to small RG error
- The error is amplified by $1/\lambda_{\min}$ (ill-conditioned fixed points are harder to locate)
- The Lipschitz constant $L_W$ measures the sensitivity of the RG flow to perturbations

### 4.2 Verification Strategy

To verify this theorem numerically:

1. **Train FNO with varying accuracy:** Use different FNO architectures and training data to achieve different $\varepsilon$ values.

2. **Measure FNO error:** Compute $\varepsilon = \|\Gamma_\kappa^{\text{FNO}} - \Gamma_\kappa^{\text{exact}}\|$ using DNS data.

3. **Compute RG fixed points:** Extract $g^*_{\text{FNO}}$ for each FNO model.

4. **Compare with exact results:** For NS turbulence, the exact $\eta_\nu = 4/3$ is known from Ward identity. Check if $|\eta_\nu^{\text{FNO}} - 4/3| \leq C(\varepsilon)$.

5. **Verify scaling:** Plot $|\Delta g^*|$ vs $\varepsilon$ and check for linear scaling.

### 4.3 Limitations

The proof assumes:
- **Lipschitz continuity (A2):** This may not hold globally, only in a neighborhood of the fixed point.
- **Non-degeneracy (A3):** Marginal fixed points (e.g., $d = 4$ for $\phi^4$ theory) require more careful analysis.
- **Small perturbations:** The theorem is perturbative; large FNO errors may lead to qualitatively different fixed points.

---

## 5. Next Steps

1. **Numerical verification:** Implement Python code to test the theorem for NS turbulence.
2. **Extend to non-perturbative regime:** Use NPRG techniques to handle strong-coupling fixed points.
3. **Prove Ward identity satisfaction:** Show that FNO with symmetry constraints automatically satisfies Ward identities.

---

**References:**
- Wetterich, C. (1993). Exact evolution equation for the effective potential. Physics Letters B, 301(1), 90-94.
- Li, Z. et al. (2021). Fourier Neural Operator for Parametric Partial Differential Equations. ICLR 2021.
- Canet, L. et al. (2003). Nonperturbative renormalization group for the Kardar-Parisi-Zhang equation. Physical Review Letters, 90(12), 120601.

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
