"""
β-function extraction from RG flow trajectories.
"""

import numpy as np
import json
import argparse
from pathlib import Path

def extract_beta_function(flow_trajectory, coupling_idx=0):
    """
    Extract β(g) from the RG flow trajectory.

    β(g) = dg/dt where t = ln(k)
    """
    k = np.array(flow_trajectory['k'])
    g = np.array(flow_trajectory['g'])

    t = np.log(k)
    g_coupling = g[coupling_idx]

    # Numerical derivative dg/dt
    beta = np.gradient(g_coupling, t)

    return g_coupling, beta

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--system', type=str, default='navier_stokes')
    parser.add_argument('--results_dir', type=str, default='results')
    args = parser.parse_args()

    rg_path = Path(args.results_dir) / f"{args.system}_rg_results.json"

    if not rg_path.exists():
        print(f"No results found at {rg_path}")
        return

    with open(rg_path, 'r') as f:
        data = json.load(f)

    flow = data.get('flow_trajectory', {})
    if not flow:
        print("No flow trajectory data found.")
        return

    print(f"β-function Analysis: {args.system}")
    print("=" * 50)

    for idx, name in enumerate(['ν', 'λ', 'D']):
        if idx >= len(flow['g']):
            break
        g, beta = extract_beta_function(flow, idx)
        # Find where β ≈ 0 (fixed points)
        zero_crossings = np.where(np.diff(np.sign(beta)))[0]
        print(f"\n  Coupling {name} (index {idx}):")
        print(f"    Range: [{g.min():.4f}, {g.max():.4f}]")
        print(f"    β zero crossings at g ≈ {g[zero_crossings]}")

if __name__ == "__main__":
    main()
