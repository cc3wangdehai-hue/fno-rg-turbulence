# FNO × RG Unified Turbulence Framework

Companion code for the paper: **"From Classical to Quantum Turbulence: A Unified FNO×RG Framework Across Six Physical Systems"** by Dehai Wang.

- **Paper**: `paper/paper1_bible_v27.tex` (single-column, v27, 2026-07-30)
- **Preprint**: [Research Square](https://www.researchsquare.com/article/rs-10495977/latest) | DOI: `10.21203/rs.3.rs-10495977/v1`

## Overview

This repository implements the three-stage FNO×RG pipeline described in the paper:

1. **Stage I — FNO Spectral Learning**: Learn scale-dependent eddy viscosity and vertex corrections from DNS/experimental data using a Fourier Neural Operator architecture.
2. **Stage II — Wetterich RG Embedding**: Embed the FNO-learned spectral closure Γ_κ into the Wetterich exact renormalization group equation for the effective average action.
3. **Stage III — Fixed-Point Extraction**: Extract fixed points, critical exponents, and anomalous dimensions through eigenvalue analysis of the linearized RG flow.

## Key Results

| Quantity | Prediction | Experiment/DNS |
|----------|-----------|----------------|
| η_ν (Ward + dim. analysis) | 4/3 (exact) | 1.29–1.33 |
| ζ₂ | 0.700 | 0.70 ± 0.02 |
| ζ₃ | 1.000 (4/5 law) | 1.12 ± 0.24 (direct) |
| Flatness F | 3.34 | 3.4 ± 0.2 |
| β-function zero g* | ~5.3 | Consistent w/ DNS |
| η_ν (viscosity) | 0.042 | Range 0.03–0.05 |

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
├── src/                            # Core FNO×RG implementation
│   ├── model.py                    # FNO architecture (shared backbone + system heads)
│   ├── training.py                 # Training pipeline with spectral loss
│   ├── rg_embedding.py             # Wetterich equation embedding
│   ├── fixedpoint.py               # Fixed-point extraction & stability analysis
│   └── utils.py                    # Data loading, spectral transforms
├── configs/                        # System-specific configurations
│   ├── navier_stokes.yaml
│   ├── quantum.yaml
│   ├── compressible.yaml
│   ├── mhd.yaml
│   ├── stratified.yaml
│   └── active_matter.yaml
├── analysis/                       # Post-processing & visualization
│   ├── scaling_exponents.py        # ζ_p computation & SL comparison
│   ├── beta_function.py            # β-function extraction from RG flow
│   ├── universality_table.py       # Cross-system comparison table
│   └── plot_spectra.py             # Energy spectra & fixed point plots
├── verification/                   # 21 validation tests + golden standard
│   ├── dns_fno/                    # DNS–FNO verification (Kolmogorov -5/3)
│   ├── golden_standard/            # Independent synthetic-DNS checks
│   ├── extended/                   # Extended DNS data verification
│   └── ward_identity/              # Ward identity numerical checks
├── computation/                    # Core theoretical computations
│   ├── fno_beta/                   # β-function computation via FNO
│   ├── ns_twoloop_beta/            # NS two-loop β-function derivation
│   ├── beta_rederivation/          # β-function re-derivation & predictions
│   └── error_propagation/          # Error propagation chain analysis
├── systems/                        # Per-system derivations & results
│   ├── active_matter/              # Active matter turbulence
│   ├── mhd/                        # Magnetohydrodynamic turbulence
│   ├── quantum_compressible/       # Quantum & compressible turbulence
│   ├── stratified/                 # Stratified turbulence
│   └── intermittency/              # Turbulence intermittency & κ-verification
├── proofs/                         # Mathematical theorem verifications
│   ├── consistency/                # Consistency theorem proof
│   ├── theorem3/                   # Non-perturbative fixed-point theorem
│   └── theorem4/                   # FNO×RG consistency assumptions
├── paper/                          # Manuscript source
│   ├── paper1_bible_v27.tex        # Main paper (single-column, latest)
│   └── paper1_bible_v27.bib        # BibTeX references (606 entries)
├── data/
│   └── download_data.py            # Download public datasets
├── requirements.txt
└── README.md
```

## AI-Assisted Processing

The author used AI-assisted tools (Coze multi-agent framework with Claude/GPT backends) to assist in symbolic computation, numerical verification, literature search, and manuscript preparation. All theoretical results, proofs, and physical conclusions were independently verified by the author.

## Citation

```bibtex
@misc{wang2026fnorg,
  title = {From Classical to Quantum Turbulence: A Unified {FNO$\times$RG} Framework Across Six Physical Systems},
  author = {Wang, Dehai},
  year = {2026},
  doi = {10.21203/rs.3.rs-10495977/v1},
  url = {https://github.com/cc3wangdehai-hue/fno-rg-turbulence}
}
```

## License

MIT
