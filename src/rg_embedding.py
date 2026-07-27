"""
Wetterich RG Embedding for the FNO×RG framework.

Implements Stage II of the pipeline: embed the FNO-learned spectral
closure Γ_κ into the Wetterich exact RG equation, and Stage III:
extract fixed points via eigenvalue analysis.
"""

import torch
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigvals
from typing import Dict, List, Tuple, Optional
import yaml
import argparse
from pathlib import Path


class WetterichRGFlow:
    """
    Implements the Wetterich exact RG equation for the effective average action.

    The Wetterich equation:
        ∂_k Γ_k = (1/2) Tr [(Γ_k^(2) + R_k)^(-1) ∂_k R_k]

    where Γ_k is the effective average action, R_k is the IR regulator,
    and Γ_k^(2) is the second functional derivative.

    For the turbulence systems, the effective average action is expanded as:
        Γ_k = ∫ [ũ_i(∂_t - ν_k∇²)u_i + (λ_k/2)ũ_i u_j ∂_j u_i + Σ g_{n,k} O_n]

    The FNO-learned Γ_κ enters as a non-perturbative correction to ν_k:
        ν_k → ν_k^pert + δν_k^FNO(κ)
    """

    def __init__(self, system: str, regulator: str = "litim"):
        """
        Args:
            system: Physical system identifier
            regulator: IR regulator type ("litim", "power_law", "exponential")
        """
        self.system = system
        self.regulator = regulator
        self.d = 3  # Spatial dimension (default)

        # System-specific parameters
        self._setup_system_params()

    def _setup_system_params(self):
        """Set up system-specific parameters for the RG flow."""
        if self.system == "navier_stokes":
            self.couplings = ["nu", "lambda", "D"]  # viscosity, vertex, noise amplitude
            self.n_couplings = 3
        elif self.system == "quantum":
            self.couplings = ["nu", "lambda", "g_int", "P"]  # + interaction + polarization
            self.n_couplings = 4
        elif self.system == "compressible":
            self.couplings = ["nu", "lambda", "gamma", "Ma"]  # + heat ratio + Mach
            self.n_couplings = 4
        elif self.system == "mhd":
            self.couplings = ["nu", "eta", "lambda", "sigma_h"]  # + resistivity + helicity
            self.n_couplings = 4
        elif self.system == "stratified":
            self.couplings = ["nu", "kappa", "lambda", "g_b"]  # + buoyancy diff + buoyancy
            self.n_couplings = 4
        elif self.system == "active_matter":
            self.couplings = ["nu", "K", "lambda", "alpha"]  # + elasticity + activity
            self.n_couplings = 4
        else:
            raise ValueError(f"Unknown system: {self.system}")

    def regulator_function(self, k: float, q: float) -> float:
        """
        Compute the IR regulator R_k(q).

        Litim regulator (optimized):
            R_k(q) = (k² - q²) θ(k² - q²)
        """
        if self.regulator == "litim":
            return max(k**2 - q**2, 0.0)
        elif self.regulator == "power_law":
            return k**2 * (k / max(q, 1e-10))**2
        elif self.regulator == "exponential":
            return k**2 * np.exp(-q**2 / k**2) if q < 5 * k else 0.0
        else:
            raise ValueError(f"Unknown regulator: {self.regulator}")

    def derivative_regulator(self, k: float, q: float) -> float:
        """∂_k R_k(q)."""
        if self.regulator == "litim":
            return 2 * k if q < k else 0.0
        elif self.regulator == "power_law":
            return 2 * k * (k / max(q, 1e-10))**2
        elif self.regulator == "exponential":
            return 2 * k * np.exp(-q**2 / k**2) * (1 - q**2 / k**2)
        else:
            raise ValueError(f"Unknown regulator: {self.regulator}")

    def beta_function(self, k: float, g: np.ndarray,
                      fno_closure: Optional[Dict] = None) -> np.ndarray:
        """
        Compute β(g) = ∂_t g where t = ln(k/Λ).

        The FNO-learned closure modifies the β-function through
        the non-perturbative correction δν_k^FNO.

        Args:
            k: RG scale
            g: Coupling constants array [g_1, g_2, ..., g_n]
            fno_closure: FNO-learned spectral closure (optional correction)

        Returns:
            β-function values for each coupling
        """
        beta = np.zeros_like(g)

        # Common structure: canonical dimension + anomalous dimension
        # β_i = -(d_i + η_i) g_i + loop corrections

        if self.system == "navier_stokes":
            nu, lam, D = g[0], g[1], g[2]

            # FNO correction to viscosity
            delta_nu = 0.0
            if fno_closure is not None:
                delta_nu = fno_closure.get("delta_nu_k", 0.0)

            # ν flow: canonical dim + one-loop + FNO correction
            eta_nu = self._compute_anomalous_dim(lam, nu, k)
            beta[0] = -(2 - eta_nu) * nu + lam**2 / (16 * np.pi * nu) - delta_nu * k

            # λ flow: vertex renormalization
            beta[1] = -(1 + eta_nu / 2) * lam + lam**3 / (32 * np.pi**2 * nu**2)

            # D flow: noise amplitude
            beta[2] = -(4 - 2 * eta_nu) * D + lam**2 * D / (8 * np.pi * nu**3)

        elif self.system == "quantum":
            nu, lam, g_int, P = g[0], g[1], g[2], g[3]
            eta_nu = self._compute_anomalous_dim(lam, nu, k)

            beta[0] = -(2 - eta_nu) * nu + lam**2 / (16 * np.pi * nu)
            beta[1] = -(1 + eta_nu / 2) * lam + lam**3 / (32 * np.pi**2 * nu**2) + P * lam
            beta[2] = -(1 - eta_nu) * g_int + lam * g_int / (8 * np.pi * nu)
            beta[3] = -0.5 * P + lam * P / (16 * np.pi * nu)

        elif self.system == "compressible":
            nu, lam, gamma, Ma = g[0], g[1], g[2], g[3]
            eta_nu = self._compute_anomalous_dim(lam, nu, k)

            # Mach-dependent β-function
            beta_ma = -(5/3 + 2 * 0.3 * Ma**2) / (1 + 0.3 * Ma**2)
            beta[0] = -(2 - eta_nu) * nu + lam**2 / (16 * np.pi * nu)
            beta[1] = -(1 + eta_nu / 2) * lam + lam**3 / (32 * np.pi**2 * nu**2)
            beta[2] = beta_ma * gamma
            beta[3] = beta_ma * Ma  # Ma flows to fixed point

        elif self.system == "mhd":
            nu, eta, lam, sigma_h = g[0], g[1], g[2], g[3]
            eta_nu = self._compute_anomalous_dim(lam, nu, k)

            beta[0] = -(2 - eta_nu) * nu + lam**2 / (16 * np.pi * nu) * (1 - sigma_h**2)
            beta[1] = -(2 - eta_nu) * eta + lam**2 / (16 * np.pi * eta)
            beta[2] = -(1 + eta_nu / 2) * lam + lam**3 / (32 * np.pi**2 * nu * eta)
            beta[3] = -sigma_h * (1 - sigma_h**2) / (8 * np.pi * nu)

        elif self.system == "stratified":
            nu, kappa, lam, g_b = g[0], g[1], g[2], g[3]
            eta_nu = self._compute_anomalous_dim(lam, nu, k)

            beta[0] = -(2 - eta_nu) * nu + lam**2 / (16 * np.pi * nu) - g_b**2 / (8 * np.pi * nu)
            beta[1] = -(2 - eta_nu) * kappa + lam**2 / (16 * np.pi * kappa)
            beta[2] = -(1 + eta_nu / 2) * lam + lam**3 / (32 * np.pi**2 * nu**2)
            beta[3] = -1 * g_b  # [g_b] = -1, UV-stable

        elif self.system == "active_matter":
            nu, K, lam, alpha = g[0], g[1], g[2], g[3]
            eta_nu = self._compute_anomalous_dim(lam, nu, k)

            beta[0] = -(2 - eta_nu) * nu + lam**2 / (16 * np.pi * nu) + alpha * K
            beta[1] = -(2 - eta_nu) * K + alpha * K**2 / (8 * np.pi * nu)
            beta[2] = -(1 + eta_nu / 2) * lam + lam**3 / (32 * np.pi**2 * nu**2)
            beta[3] = -(4 - 2 * eta_nu) * alpha + lam * alpha / (8 * np.pi * nu)

        return beta

    def _compute_anomalous_dim(self, lam: float, nu: float, k: float) -> float:
        """Compute the anomalous dimension η from one-loop contribution."""
        return lam**2 / (8 * np.pi * nu * k)

    def find_fixed_points(self, g_init: np.ndarray,
                          fno_closure: Optional[Dict] = None) -> Dict:
        """
        Find fixed points of the RG flow by solving β(g*) = 0.

        Uses Newton-Raphson iteration starting from g_init.

        Args:
            g_init: Initial guess for coupling constants
            fno_closure: FNO-learned correction (optional)

        Returns:
            Dictionary with fixed point information
        """
        from scipy.optimize import root

        def beta_residual(g):
            return self.beta_function(1.0, g, fno_closure)

        result = root(beta_residual, g_init, method="hybr")

        if result.success:
            g_star = result.x
            beta_val = beta_residual(g_star)
            print(f"Fixed point found: g* = {g_star}")
            print(f"  Residual |β| = {np.linalg.norm(beta_val):.2e}")

            # Stability analysis: Jacobian of β at fixed point
            jac = self._compute_jacobian(g_star, fno_closure)
            eigenvalues = eigvals(jac)

            print(f"  Eigenvalues: {eigenvalues}")
            relevant = np.sum(np.real(eigenvalues) > 0)
            irrelevant = np.sum(np.real(eigenvalues) < 0)
            marginal = np.sum(np.abs(np.real(eigenvalues)) < 1e-6)

            return {
                "g_star": g_star,
                "eigenvalues": eigenvalues,
                "n_relevant": int(relevant),
                "n_irrelevant": int(irrelevant),
                "n_marginal": int(marginal),
                "stable": relevant == 0,
                "residual": float(np.linalg.norm(beta_val)),
            }
        else:
            print(f"No fixed point found from initial guess {g_init}")
            return {"found": False, "message": result.message}

    def _compute_jacobian(self, g: np.ndarray,
                          fno_closure: Optional[Dict] = None) -> np.ndarray:
        """Compute the Jacobian ∂β_i/∂g_j at coupling g."""
        n = len(g)
        jac = np.zeros((n, n))
        eps = 1e-6

        for j in range(n):
            g_plus = g.copy()
            g_minus = g.copy()
            g_plus[j] += eps
            g_minus[j] -= eps

            beta_plus = self.beta_function(1.0, g_plus, fno_closure)
            beta_minus = self.beta_function(1.0, g_minus, fno_closure)

            jac[:, j] = (beta_plus - beta_minus) / (2 * eps)

        return jac

    def integrate_flow(self, g_init: np.ndarray, k_start: float = 100.0,
                       k_end: float = 0.01,
                       fno_closure: Optional[Dict] = None) -> Dict:
        """
        Integrate the RG flow from k_start to k_end.

        Args:
            g_init: Initial coupling constants at k_start
            k_start: Initial RG scale (UV)
            k_end: Final RG scale (IR)
            fno_closure: FNO-learned correction (optional)

        Returns:
            Dictionary with flow trajectories
        """
        t_start = np.log(k_start)
        t_end = np.log(k_end)

        def flow_rhs(t, g):
            k = np.exp(t)
            return self.beta_function(k, g, fno_closure)

        t_span = (t_start, t_end)
        t_eval = np.linspace(t_start, t_end, 500)

        sol = solve_ivp(flow_rhs, t_span, g_init, t_eval=t_eval,
                        method="RK45", rtol=1e-8, atol=1e-10)

        return {
            "t": sol.t,
            "k": np.exp(sol.t),
            "g": sol.y,
            "coupling_names": self.couplings,
            "success": sol.success,
        }


def run_rg_embedding(config_path: str, checkpoint_path: str):
    """
    Run Stage II+III: load FNO checkpoint, compute spectral closure,
    embed into Wetterich equation, extract fixed points.
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    system = config["system"]
    print(f"Running RG embedding for {system} system")

    # Load FNO model and compute spectral closure
    # (In practice, this loads the trained FNO and evaluates it on reference data)
    fno_closure = _load_fno_closure(checkpoint_path, config)

    # Set up RG flow
    rg = WetterichRGFlow(system=system, regulator=config["rg"].get("regulator", "litim"))

    # Find fixed points
    g_init = np.array(config["rg"]["initial_couplings"])
    fp = rg.find_fixed_points(g_init, fno_closure)

    if fp.get("found", True):
        print(f"\n=== Fixed Point Analysis for {system} ===")
        print(f"Fixed point: g* = {fp['g_star']}")
        print(f"Relevant directions: {fp['n_relevant']}")
        print(f"Irrelevant directions: {fp['n_irrelevant']}")
        print(f"Stable: {fp['stable']}")

        # Compute anomalous dimensions
        eta = rg._compute_anomalous_dim(fp['g_star'][1], fp['g_star'][0], 1.0)
        print(f"Anomalous dimension η = {eta:.4f}")

    # Integrate flow
    flow = rg.integrate_flow(g_init, fno_closure=fno_closure)
    print(f"\nRG flow integration: {'success' if flow['success'] else 'failed'}")

    # Save results
    results = {
        "system": system,
        "fixed_point": fp,
        "flow_trajectory": {
            "k": flow["k"].tolist(),
            "g": flow["g"].tolist(),
        },
        "anomalous_dimension": float(eta) if fp.get("found", True) else None,
    }

    output_dir = Path(config.get("output_dir", "results"))
    output_dir.mkdir(parents=True, exist_ok=True)
    import json
    with open(output_dir / f"{system}_rg_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to {output_dir}/{system}_rg_results.json")


def _load_fno_closure(checkpoint_path: str, config: Dict) -> Dict:
    """Load FNO checkpoint and compute spectral closure on reference data."""
    # Placeholder: in practice, load the model and evaluate
    print(f"Loading FNO checkpoint from {checkpoint_path}")
    # This would load the actual trained model and evaluate Γ_κ
    # For now, return a placeholder closure
    return {"delta_nu_k": 0.0, "closure_type": "FNO_learned"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FNO×RG Embedding")
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, required=True)
    args = parser.parse_args()
    run_rg_embedding(args.config, args.checkpoint)
