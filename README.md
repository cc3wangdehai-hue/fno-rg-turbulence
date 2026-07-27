# FNO × RG Unified Turbulence Framework

Companion code for the paper: **"From Classical to Quantum Turbulence: A Unified FNO×RG Framework Across Six Physical Systems"** by Dehai Wang.

## Overview

This repository implements the three-stage FNO×RG pipeline described in the paper:

1. **Stage I — FNO Spectral Learning**: Learn scale-dependent eddy viscosity and vertex corrections from DNS/experimental data using a Fourier Neural Operator architecture.
2. **Stage II — Wetterich RG Embedding**: Embed the FNO-learned spectral closure Γ_κ into the Wetterich exact renormalization group equation for the effective average action.
3. **Stage III — Fixed-Point Extraction**: Extract fixed points, critical exponents, and anomalous dimensions through eigenvalue analysis of the linearized RG flow.

## Supported Systems

| System | Section | Control Parameter | Key Result |
|--------|---------|-------------------|------------|
| Navier–Stokes | Sec. III | Re → ∞ | η_ν = 4/3, SL scaling |
| Quantum Turbulence | Sec. IV | Π_P = P/P_c | KS/LN crossover |
| Compressible | Sec. V | Ma | β(Ma) crossover |
| MHD | Sec. VI | σ_h, Re_m | Double inertial range |
| Stratified | Sec. VII | Fr, Re_b | Triple fixed points |
| Active Matter | Sec. VIII | Π_a | NATFP/PATFP resolution |

## Repository Structure

```
├── src/
│   ├── model.py            # FNO architecture (shared backbone + system-specific heads)
│   ├── training.py         # Training pipeline with spectral loss
│   ├── rg_embedding.py     # Wetterich equation embedding
│   ├── fixedpoint.py       # Fixed-point extraction and stability analysis
│   └── utils.py            # Data loading, spectral transforms, diagnostics
├── configs/
│   ├── navier_stokes.yaml  # NS system configuration
│   ├── quantum.yaml        # Quantum turbulence configuration
│   ├── compressible.yaml   # Compressible turbulence configuration
│   ├── mhd.yaml            # MHD turbulence configuration
│   ├── stratified.yaml     # Stratified turbulence configuration
│   └── active_matter.yaml  # Active matter configuration
├── analysis/
│   ├── scaling_exponents.py   # Compute ζ_p and compare with SL model
│   ├── beta_function.py       # Extract β-function from RG flow
│   ├── universality_table.py  # Generate cross-system comparison table
│   └── plot_spectra.py        # Visualize energy spectra and fixed points
├── data/
│   └── download_data.py    # Download public datasets (JHTDB, solar wind, GPE)
├── notebooks/
│   └── demo_ns.ipynb       # Demo: Navier–Stokes full pipeline walkthrough
├── requirements.txt
└── README.md
```

## Data Sources

All training data uses publicly available datasets:

- **Navier–Stokes**: [Johns Hopkins Turbulence Database (JHTDB)](http://turbulence.pha.jhu.edu/) — Li et al. (2008), Yeung et al. (2009)
- **Quantum Turbulence**: GPE simulation data — Brachet et al. (2021), [CPC 258, 107579]
- **Solar Wind (MHD)**: Cluster and Parker Solar Probe missions — Alexandrova et al. (2013), Fox et al. (2016)
- **Compressible**: Public DNS databases — Almeida et al. (2021), Wang et al. (2017)
- **Stratified & Active Matter**: Generated using the included simulation scripts with parameters from the literature

## Requirements

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# 1. Download public datasets
python data/download_data.py --system navier_stokes

# 2. Train FNO for a specific system
python src/training.py --config configs/navier_stokes.yaml

# 3. Run RG embedding and extract fixed points
python src/rg_embedding.py --config configs/navier_stokes.yaml --checkpoint checkpoints/ns_best.pt

# 4. Analyze results
python analysis/scaling_exponents.py --system navier_stokes
python analysis/beta_function.py --system navier_stokes
```

## Training Hyperparameters (Default)

- **Architecture**: L=4 Fourier layers, 64 modes/layer, d_v=128, SiLU activation
- **Optimizer**: Adam, lr=1e-3 with cosine annealing
- **Batch size**: 8
- **Epochs**: 500
- **Loss**: Standard L² spectral loss

## Citation

```bibtex
@article{wang2026fno_rg,
  title={From Classical to Quantum Turbulence: A Unified FNO$\times$RG Framework Across Six Physical Systems},
  author={Wang, Dehai},
  year={2026},
  note={Preprint}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.
