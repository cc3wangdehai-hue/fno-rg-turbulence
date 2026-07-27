"""
Scaling exponent analysis: compute ζ_p from FNO×RG results
and compare with the She-Leveque model.
"""

import numpy as np
import json
import argparse
from pathlib import Path

def she_leveque_model(p, C=2.0, sigma=1.0/3):
    """She-Leveque scaling: ζ_p = p/9 + C - C(σ/3)^{p/3}"""
    return p / 9.0 + C - C * (sigma / 3.0) ** (p / 3.0)

def compute_zeta_from_fixedpoint(rg_results_path):
    """Extract ζ_p from RG fixed point analysis."""
    with open(rg_results_path, 'r') as f:
        data = json.load(f)

    # The anomalous dimension from the fixed point
    eta = data.get('anomalous_dimension', 0.0)

    # ζ_p = p/3 * (1 - eta/3) for simple scaling
    p = np.arange(1, 11)
    zeta_p = p / 3.0 * (1.0 - eta / 3.0)

    return p, zeta_p

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--system', type=str, default='navier_stokes')
    parser.add_argument('--results_dir', type=str, default='results')
    args = parser.parse_args()

    # Load RG results
    rg_path = Path(args.results_dir) / f"{args.system}_rg_results.json"
    fp_path = Path(args.results_dir) / f"{args.system}_fixed_points.json"

    print(f"Scaling Exponent Analysis: {args.system}")
    print("=" * 50)

    # She-Leveque reference
    p = np.arange(1, 11)
    zeta_sl = she_leveque_model(p)

    print(f"\nShe-Leveque reference (ζ_p = p/9 + 2 - 2(1/9)^{{p/3}}):")
    for pi, zi in zip(p, zeta_sl):
        print(f"  ζ_{int(pi)} = {zi:.4f}")

    # FNO×RG results (if available)
    if rg_path.exists():
        p_rg, zeta_rg = compute_zeta_from_fixedpoint(rg_path)
        print(f"\nFNO×RG results:")
        for pi, zi in zip(p_rg, zeta_rg):
            diff = zi - she_leveque_model(np.array([pi]))[0]
            print(f"  ζ_{int(pi)} = {zi:.4f}  (SL diff: {diff:+.4f})")

if __name__ == "__main__":
    main()
