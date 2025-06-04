# MCMC
import numpy as np
import cosmolib as cs
from matplotlib.pyplot import rc, errorbar, xlim, xlabel, ylabel, legend, show, plot
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import glob
import os

# Find the latest CSV file automatically
csv_pattern = 'supernova_fitting_results_*.csv'
csv_files = glob.glob(csv_pattern)

if not csv_files:
    raise FileNotFoundError(f"No CSV files found matching pattern: {csv_pattern}")

# Sort files by modification time (most recent first)
latest_csv = max(csv_files, key=os.path.getmtime)
print(f"Using latest CSV file: {latest_csv}")

df = pd.read_csv(latest_csv)

z = df['redshift'].values
mu_exp = df['mu'].values
sigma_mu_exp = df['mu_err'].values


def chi_deux(z, par):
    return (cs.musn1a(z, {'omega_M_0': par[0], 'omega_lambda_0': par[1], 'h': par[2], 'w0': -1})-mu_exp)**2/sigma_mu_exp

def muPred(z, par):
    res = cs.musn1a(z, {'omega_M_0': par[0], 'omega_lambda_0': par[1], 'h': par[2], 'w0': -1})
    return res 

data = cs.Data(z, np.round(mu_exp, 2), sigma_mu_exp,  muPred)


guess = np.array([0.7, 0.3, 0.7])
np.random.seed(42)
chain = data.run_mcmc(guess, nbmc=1000, allvariables=['p0','p1','p2'], fixpars=[2])

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(chain['p0'], chain['p1'], c='b', marker=',', alpha=0.1, label='MCMC samples')
plt.scatter(0.389, 0.389, c='g', marker='*', s=200, label='True Value')
plt.xlabel('omegaM')
plt.ylabel('omegaL')
plt.legend()
plt.title('MCMC samples in omegaM vs omegaL')
plt.show()

omegaM_chain = chain['p0']
omegaL_chain = chain['p1']
omegaM_best = np.median(omegaM_chain)
omegaL_best = np.median(omegaL_chain)

print(omegaM_best, omegaL_best)
