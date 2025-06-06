# EI Cosmo A: Cosmological Parameters Estimation

A comprehensive cosmological analysis project combining Type Ia Supernovae (SNe Ia) observations and Cosmic Microwave Background (CMB) data to constrain cosmological parameters using MCMC methods.

## Project Overview

This project implements a full pipeline for cosmological parameter estimation using:
- **SN3**: Type Ia Supernovae analysis for distance modulus measurements
- **CMB3**: Cosmic Microwave Background power spectrum analysis  
- **Joint Analysis**: Combined constraints from both datasets


## Features

### Supernovae Analysis (SN3)
- **Light Curve Fitting**: Fits individual SN Ia light curves to template
- **Distance Modulus Calculation**: Derives distance measurements from apparent magnitudes
- **Stretch Correction**: Applies Phillips relation for luminosity standardization
- **MCMC Parameter Estimation**: Constrains Ωₘ, ΩΛ, and H₀

### CMB Analysis (CMB3)  
- **Power Spectrum Analysis**: Uses observed CMB temperature anisotropies
- **CAMB Integration**: Theoretical power spectrum calculations
- **Acoustic Peak Fitting**: Constrains cosmological parameters from peak positions

### Joint Analysis
- **Combined Likelihood**: Simultaneous fitting of SN and CMB data
- **Parameter Degeneracy Breaking**: Improved constraints from complementary datasets
- **Systematic Error Handling**: Accounts for intrinsic scatter and observational uncertainties

## Installation

### Requirements
```bash
pip install numpy matplotlib pandas scipy emcee iminuit healpy camb
```

### Dependencies
- **Python 3.7+**
- **NumPy**: Numerical computations
- **Matplotlib**: Plotting and visualization
- **Pandas**: Data handling and CSV operations
- **SciPy**: Optimization and statistical functions
- **emcee**: MCMC sampling
- **iminuit**: χ² minimization
- **HealPy**: Spherical harmonics for CMB maps
- **CAMB**: Cosmological parameter calculations

## Usage

### 1. Supernovae Analysis

Run the main SN analysis:
```python
# Load and analyze SN data
jupyter notebook SN3/SN3_EI_Cosmo.ipynb
```

Key functions in [`cosmolib.py`](SN3/cosmolib.py):
```python
import cosmolib as cs

# Calculate distance modulus
mu = cs.musn1a(redshift, {'omega_M_0': 0.3, 'omega_lambda_0': 0.7, 'h': 0.7})

# Run MCMC fitting
data = cs.Data(z, mu_obs, sigma_mu, model_function)
chain = data.run_mcmc(initial_guess, nbmc=10000)
```

### 2. Joint SN + CMB Analysis

Execute the combined analysis:
```python
jupyter notebook SN3+CMB3/final.ipynb
```

The pipeline:
1. Loads latest SN fitting results from CSV
2. Loads CMB power spectrum data from [`cl_forWP3.txt`](SN3+CMB3/cl_forWP3.txt)
3. Runs separate MCMC chains for SN, CMB, and joint analysis
4. Generates corner plots and parameter constraints

## Data Files

### Input Data
- **Supernova Light Curves**: Individual SN Ia photometric time series
- **Redshift Catalog**: `EI2019-Data-LightCurves-SN-Redshifts.txt`
- **Template Light Curve**: `EI2019-Data-LightCurves-SN-SNI-Average_LightCurve.txt`
- **CMB Power Spectrum**: [`cl_forWP3.txt`](SN3+CMB3/cl_forWP3.txt) (ℓ, Dℓ, σDℓ)

### Output Files
- **SN Fitting Results**: `supernova_fitting_results_YYYYMMDD_HHMMSS.csv`
  - Columns: redshift, μ, μ_err, stretch factor, χ², etc.
- **MCMC Chains**: Parameter samples for cosmological constraints

## Key Functions

### Cosmological Calculations
```python
# Distance modulus for flat ΛCDM
def musn1a(z, cosmo):
    """Calculate distance modulus for Type Ia supernovae"""
    
# Angular diameter distance  
def angdist(z, cosmo):
    """Compute angular diameter distance"""

# Sound horizon at decoupling
def rs(cosmo, zd=1059.25):
    """Sound horizon scale for CMB analysis"""
```

### MCMC Implementation
```python
class Data:
    def run_mcmc(self, guess, nbmc=10000, allvariables=None, fixpars=None):
        """Run MCMC parameter estimation"""
        
    def plot_contours(self, chain, parameters):
        """Generate corner plots for parameter constraints"""
```

## Results

The analysis constrains cosmological parameters:
- **Ωₘ**: Matter density parameter  
- **ΩΛ**: Dark energy density parameter
- **H₀**: Hubble constant
- **w₀**: Dark energy equation of state (when varied)

Typical outputs:
```
Best-fit parameters (68% confidence):
Ωₘ = 0.30 ± 0.05
ΩΛ = 0.70 ± 0.05  
H₀ = 70 ± 5 km/s/Mpc
```

## Error Handling

The code includes robust error handling for:
- **Missing data files**: Automatic detection of latest CSV files
- **Convergence issues**: MCMC chain diagnostics
- **Numerical instabilities**: Parameter bounds and priors
- **CAMB integration**: Fallback to approximate calculations

## Troubleshooting

### Common Issues

1. **CAMB installation**: Requires Fortran compiler
   ```bash
   conda install -c conda-forge camb
   ```

2. **Memory errors**: Reduce MCMC chain length for testing
   ```python
   chain = data.run_mcmc(guess, nbmc=1000)  # Reduced from 10000
   ```

3. **CSV file not found**: Ensure SN analysis completed successfully
   ```python
   # Check for output files
   import glob
   csv_files = glob.glob('supernova_fitting_results_*.csv')
   ```

## Contributing

When adding new features:
1. Follow existing code structure in [`cosmolib.py`](SN3+CMB3/cosmolib.py)
2. Add error handling and input validation
3. Update progress bars for long computations using [`progress_bar()`](SN3+CMB3/cosmolib.py#L110)
4. Document functions with docstrings

## License
This project is part of the ST4: cosmology and particle physics coursework at CentraleSupelec. Please cite appropriately if using components of this analysis.