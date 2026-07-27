"""
Fixed-point extraction and stability analysis.

Stage III of the FNO×RG pipeline: given the RG flow from Stage II,
identify all fixed points and classify their stability.
"""

import numpy as np
from scipy.optimize import root, minimize
from scipy.linalg import eigvals
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path

from rg_embedding import WetterichRGFlow


class FixedPointAnalyzer:
    """
    Systematic fixed-point search and classification for the RG flow.
    """

    def __init__(self, system: str, regulator: str = "litim"):
        self.system = system
        self.rg = WetterichRGFlow(system=system, regulator=regulator)
        self.fixed_points: List[Dict] = []

    def scan_initial_conditions(self, n_samples: int = 100,
                                g_range: Tuple[float, float] = (-2.0, 2.0),
                                fno_closure: Optional[Dict] = None) -> List[Dict]:
        """
        Scan multiple initial conditions to find all fixed points.

        Args:
            n_samples: Number of random initial conditions
            g_range: Range for random coupling initialization
            fno_closure: FNO-learned closure (optional)

        Returns:
            List of distinct fixed points found
        """
        np.random.seed(42)
        all_fps = []

        for i in range(n_samples):
            g_init = np.random.uniform(
                g_range[0], g_range[1],
                size=self.rg.n_couplings
            )

            fp = self.rg.find_fixed_points(g_init, fno_closure)
            if fp.get("found", True) and fp.get("residual", 1.0) < 1e-6:
                all_fps.append(fp)

        # Cluster and deduplicate
        self.fixed_points = self._deduplicate(all_fps, tol=1e-4)
        print(f"\nFound {len(self.fixed_points)} distinct fixed points "
              f"from {n_samples} initial conditions")

        return self.fixed_points

    def _deduplicate(self, fps: List[Dict], tol: float = 1e-4) -> List[Dict]:
        """Remove duplicate fixed points."""
        unique = []
        for fp in fps:
            is_dup = False
            for ufp in unique:
                if np.linalg.norm(fp["g_star"] - ufp["g_star"]) < tol:
                    is_dup = True
                    break
            if not is_dup:
                unique.append(fp)
        return unique

    def classify_stability(self) -> List[Dict]:
        """
        Classify each fixed point by stability type.

        Returns:
            Updated fixed points with stability classification
        """
        for fp in self.fixed_points:
            eigs = np.real(fp["eigenvalues"])

            if all(e < -1e-6 for e in eigs):
                fp["stability"] = "UV-stable (IR-repulsive)"
                fp["type"] = "attractive"
            elif all(e > 1e-6 for e in eigs):
                fp["stability"] = "IR-stable (UV-repulsive)"
                fp["type"] = "repulsive"
            else:
                n_pos = np.sum(eigs > 1e-6)
                n_neg = np.sum(eigs < -1e-6)
                fp["stability"] = f"saddle ({n_pos} relevant, {n_neg} irrelevant)"
                fp["type"] = "saddle"

        return self.fixed_points

    def compute_critical_exponents(self) -> List[Dict]:
        """
        Compute critical exponents (anomalous dimensions) at each fixed point.

        The critical exponent ν = 1/λ where λ is the most relevant eigenvalue.
        """
        for fp in self.fixed_points:
            eigs = np.real(fp["eigenvalues"])

            # Most relevant eigenvalue (largest positive)
            lambda_max = np.max(eigs) if np.max(eigs) > 0 else np.max(np.abs(eigs))

            if lambda_max > 1e-6:
                fp["nu_critical"] = 1.0 / lambda_max
                fp["eta_anomalous"] = self.rg._compute_anomalous_dim(
                    fp["g_star"][1] if len(fp["g_star"]) > 1 else fp["g_star"][0],
                    fp["g_star"][0],
                    1.0
                )
            else:
                fp["nu_critical"] = float("inf")
                fp["eta_anomalous"] = 0.0

        return self.fixed_points

    def generate_report(self) -> str:
        """Generate a text report of all fixed points."""
        lines = [f"\n{'='*60}"]
        lines.append(f"Fixed Point Analysis: {self.system}")
        lines.append(f"{'='*60}")

        for i, fp in enumerate(self.fixed_points):
            lines.append(f"\nFixed Point #{i+1}:")
            lines.append(f"  Couplings: g* = {fp['g_star']}")
            lines.append(f"  Stability: {fp.get('stability', 'unknown')}")
            lines.append(f"  Eigenvalues: {fp['eigenvalues']}")
            lines.append(f"  Relevant directions: {fp['n_relevant']}")
            if "nu_critical" in fp:
                lines.append(f"  Critical exponent ν = {fp['nu_critical']:.4f}")
                lines.append(f"  Anomalous dimension η = {fp['eta_anomalous']:.4f}")

        return "\n".join(lines)

    def save_results(self, output_path: str):
        """Save results to JSON."""
        results = []
        for fp in self.fixed_points:
            result = {
                "g_star": fp["g_star"].tolist(),
                "eigenvalues": fp["eigenvalues"].tolist() if hasattr(fp["eigenvalues"], 'tolist') else fp["eigenvalues"],
                "n_relevant": fp["n_relevant"],
                "n_irrelevant": fp["n_irrelevant"],
                "stability": fp.get("stability", "unknown"),
            }
            if "nu_critical" in fp:
                result["nu_critical"] = fp["nu_critical"]
                result["eta_anomalous"] = fp["eta_anomalous"]
            results.append(result)

        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")


def analyze_system(system: str, output_dir: str = "results"):
    """Run complete fixed-point analysis for a system."""
    analyzer = FixedPointAnalyzer(system)

    # Scan for fixed points
    analyzer.scan_initial_conditions(n_samples=200)

    # Classify stability
    analyzer.classify_stability()

    # Compute critical exponents
    analyzer.compute_critical_exponents()

    # Report
    report = analyzer.generate_report()
    print(report)

    # Save
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    analyzer.save_results(f"{output_dir}/{system}_fixed_points.json")

    # Save report
    with open(f"{output_dir}/{system}_fp_report.txt", "w") as f:
        f.write(report)

    return analyzer.fixed_points


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", type=str, required=True,
                        choices=["navier_stokes", "quantum", "compressible",
                                 "mhd", "stratified", "active_matter"])
    parser.add_argument("--output_dir", type=str, default="results")
    args = parser.parse_args()

    analyze_system(args.system, args.output_dir)
