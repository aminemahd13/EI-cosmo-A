import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Générer des données fictives (redshifts et distance modulus)
np.random.seed(42)
n_points = 150
z_data = np.sort(np.random.uniform(0.01, 1.0, n_points))
mu_data = 42 + 5 * np.log10(z_data) + np.random.normal(0, 0.2, n_points)
mu_err = np.full_like(mu_data, 0.2)

# Modèle cosmologique général (Lambda-CDM, courbure libre)
def distance_modulus(z, H0, Omega_m, Omega_L):
    c = 299792.458  # km/s
    Omega_k = 1.0 - Omega_m - Omega_L

    def E(z):
        return np.sqrt(Omega_m * (1 + z)**3 + Omega_k * (1 + z)**2 + Omega_L)

    dl = []
    for zi in z:
        integral, _ = quad(lambda zp: 1.0 / E(zp), 0, zi)
        if np.isclose(Omega_k, 0):
            d_c = (c / H0) * integral
        elif Omega_k > 0:
            d_c = (c / H0) / np.sqrt(Omega_k) * np.sinh(np.sqrt(Omega_k) * integral)
        else:
            d_c = (c / H0) / np.sqrt(-Omega_k) * np.sin(np.sqrt(-Omega_k) * integral)
        d_l = (1 + zi) * d_c
        dl.append(d_l)
    dl = np.array(dl)
    mu = 5 * np.log10(dl) + 25
    return mu

# Fonction de vraisemblance
def log_likelihood(params, z, mu_obs, mu_err):
    H0, Omega_m, Omega_L = params
    mu_model = distance_modulus(z, H0, Omega_m, Omega_L)
    chi2 = np.sum(((mu_obs - mu_model) / mu_err) ** 2)
    return -0.5 * chi2

# Priors uniformes
def log_prior(params):
    H0, Omega_m, Omega_L = params
    Omega_k = 1.0 - Omega_m - Omega_L
    if 50 < H0 < 90 and 0.0 < Omega_m < 1.0 and 0.0 < Omega_L < 1.5 and -1.0 < Omega_k < 1.0:
        return 0.0
    return -np.inf

def log_posterior(params, z, mu_obs, mu_err):
    lp = log_prior(params)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(params, z, mu_obs, mu_err)

# MCMC Metropolis-Hastings
def run_mcmc(z, mu_obs, mu_err, n_steps=7000):
    chain = []
    params = [70, 0.3, 0.7]  # Valeurs initiales
    logp = log_posterior(params, z, mu_obs, mu_err)
    for i in range(n_steps):
        proposal = params + np.random.normal([0, 0, 0], [0.5, 0.02, 0.02])
        logp_prop = log_posterior(proposal, z, mu_obs, mu_err)
        if np.log(np.random.rand()) < logp_prop - logp:
            params = proposal
            logp = logp_prop
        chain.append(params.copy())
    return np.array(chain)

# Exécution de la chaîne MCMC
chain = run_mcmc(z_data, mu_data, mu_err, n_steps=10000)
burn_in = 2000
samples = chain[burn_in:]

# Affichage des résultats
H0_samples = samples[:, 0]
Omega_m_samples = samples[:, 1]
Omega_L_samples = samples[:, 2]
Omega_k_samples = 1.0 - Omega_m_samples - Omega_L_samples

print(f"Best-fit H0: {np.mean(H0_samples):.2f} ± {np.std(H0_samples):.2f}")
print(f"Best-fit Omega_m: {np.mean(Omega_m_samples):.3f} ± {np.std(Omega_m_samples):.3f}")
print(f"Best-fit Omega_Lambda: {np.mean(Omega_L_samples):.3f} ± {np.std(Omega_L_samples):.3f}")
print(f"Best-fit Omega_k: {np.mean(Omega_k_samples):.3f} ± {np.std(Omega_k_samples):.3f}")

plt.figure(figsize=(15,4))
plt.subplot(1,3,1)
plt.hist(H0_samples, bins=30, color='skyblue')
plt.xlabel('H0')
plt.ylabel('Frequency')
plt.subplot(1,3,2)
plt.hist(Omega_m_samples, bins=30, color='salmon')
plt.xlabel('Omega_m')
plt.subplot(1,3,3)
plt.hist(Omega_k_samples, bins=30, color='lightgreen')
plt.xlabel('Omega_k')
plt.tight_layout()
plt.show()

print("Résumé des valeurs cosmologiques estimées par MCMC :")
print(f"H0 moyen = {np.mean(H0_samples):.2f} ± {np.std(H0_samples):.2f}")
print(f"Omega_m moyen = {np.mean(Omega_m_samples):.3f} ± {np.std(Omega_m_samples):.3f}")
print(f"Omega_lambda moyen = {np.mean(Omega_L_samples):.3f} ± {np.std(Omega_L_samples):.3f}")
print(f"Omega_k moyen = {np.mean(Omega_k_samples):.3f} ± {np.std(Omega_k_samples):.3f}")
