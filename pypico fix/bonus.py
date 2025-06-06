import pandas as pd
import numpy as np
from scipy.optimize import minimize

c = 299792.458  # Speed of light in km/s
H0 = 70  # Hubble constant in km/s/Mpc

df = pd.read_csv("SN3/supernova_fitting_results_20250603_152308.csv")
z = df["redshift"].values
mu_obs = df["mu"].values
s = df["s"].values

def mu_th(z):
    dL = c*z / H0  # Approximation for z << 1
    return 5 * np.log10(dL * 10**6) + 25  # Theoretical distance modulus

def distance(params):
    alpha, M = params
    mu_corr = mu_obs - alpha * (s - 1) # Corrected distance modulus 
    mu_model = mu_th(z)
    return np.sum((mu_corr - mu_model - M)**2)

res = minimize(distance, x0=[0, 0])
alpha_fit, M_fit = res.x

print(f"alpha = {alpha_fit}, M = {M_fit}")
