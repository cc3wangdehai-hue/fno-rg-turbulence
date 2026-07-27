"""
Download public datasets used in the FNO×RG paper.
"""

import argparse
import os
from pathlib import Path


def download_jhtdb_data(output_dir, resolution=1024):
    """Download Navier-Stokes data from JHTDB."""
    print("JHTDB Data Download")
    print("=" * 40)
    print("The Johns Hopkins Turbulence Database provides:")
    print(f"  - Isotropic turbulence at {resolution}^3 resolution")
    print("  - Velocity, pressure, forcing fields")
    print("  - Multiple time steps for temporal correlation")
    print()
    print("Access via: http://turbulence.pha.jhu.edu/")
    print("API docs: http://turbulence.pha.jhu.edu/web_services.aspx")
    print()
    print("To download programmatically, register for a token at:")
    print("  http://turbulence.pha.jhu.edu/register.aspx")
    print()
    os.makedirs(os.path.join(output_dir, "ns"), exist_ok=True)
    print(f"Output directory: {output_dir}/ns/")


def download_solar_wind_data(output_dir):
    """Download solar wind / MHD turbulence data."""
    print("Solar Wind Data (MHD Turbulence)")
    print("=" * 40)
    print("Data sources:")
    print("  1. Cluster mission: https://www.cosmos.esa.int/web/cluster")
    print("  2. Parker Solar Probe: https://parkersolarprobe.jhuapl.edu/")
    print("  3. CDAWeb: https://cdaweb.gsfc.nasa.gov/")
    print()
    print("Recommended datasets:")
    print("  - Alexandrova et al. (2013) MHD spectra")
    print("  - PSP/FIELDS magnetic field data")
    print()
    os.makedirs(os.path.join(output_dir, "mhd"), exist_ok=True)
    print(f"Output directory: {output_dir}/mhd/")


def download_gpe_data(output_dir):
    """Download quantum turbulence (GPE simulation) data."""
    print("Quantum Turbulence (GPE) Data")
    print("=" * 40)
    print("Data source:")
    print("  Brachet et al. (2021) GPE simulation data")
    print("  DOI: 10.1016/j.cpc.2020.107579")
    print()
    print("Contact authors for raw simulation data,")
    print("or use the synthetic GPE data generator included in this repo.")
    print()
    os.makedirs(os.path.join(output_dir, "quantum"), exist_ok=True)
    print(f"Output directory: {output_dir}/quantum/")


def main():
    parser = argparse.ArgumentParser(description="Download public datasets")
    parser.add_argument('--system', type=str, default='all',
                        choices=['all', 'navier_stokes', 'quantum', 'mhd'])
    parser.add_argument('--output_dir', type=str, default='data')
    args = parser.parse_args()

    print(f"Data Download Tool for FNO×RG Framework")
    print(f"{'='*50}\n")

    if args.system in ('all', 'navier_stokes'):
        download_jhtdb_data(args.output_dir)
        print()

    if args.system in ('all', 'mhd'):
        download_solar_wind_data(args.output_dir)
        print()

    if args.system in ('all', 'quantum'):
        download_gpe_data(args.output_dir)
        print()

    print("All data download links prepared.")
    print("Note: Compressible, stratified, and active matter data")
    print("can be generated using DNS codes with parameters from the literature.")


if __name__ == "__main__":
    main()
