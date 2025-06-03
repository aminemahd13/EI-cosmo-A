import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner
import cosmolib as cs  # Assure-toi que ce fichier contient musn1a()
from tqdm import tqdm

# -------------------- Données factices (exemple) --------------------
np.random.seed(42)
redshifts = np.linspace(0.01, 1.0, 30)
true_cosmo = {'omega_M_0': 0.3, 'omega_lambda_0': 0.7, 'w0': -1, 'h': 0.7}
mu_exp = cs.musn1a(redshifts, true_cosmo)
sigma_mu_exp = 0.15 * np.ones_like(mu_exp)
mu_exp += np.random.normal(0, sigma_mu_exp)

# -------------------- Fonction chi² et log-vraisemblance --------------------
def chi2(theta):
    omega_M_0, omega_lambda_0, h = theta
    cosmo = {'omega_M_0': omega_M_0, 'omega_lambda_0': omega_lambda_0, 'w0': -1, 'h': h}
    mu_th = cs.musn1a(redshifts, cosmo)
    return np.sum(((mu_th - mu_exp) / sigma_mu_exp) ** 2)

def log_likelihood(theta):
    if np.any(np.array(theta) <= 0) or theta[0] + theta[1] > 1.5:
        return -np.inf
    return -0.5 * chi2(theta)

def log_prior(theta):
    omega_M_0, omega_lambda_0, h = theta
    if 0.0 < omega_M_0 < 1.0 and 0.0 < omega_lambda_0 < 1.0 and 0.4 < h < 1.0:
        return 0.0  # Prior uniforme
    return -np.inf

def log_posterior(theta):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta)

# -------------------- Paramètres MCMC --------------------
ndim = 3
nwalkers = 50
nsteps = 2000
initial_guess = [0.3, 0.7, 0.7]
pos = initial_guess + 1e-2 * np.random.randn(nwalkers, ndim)

# -------------------- MCMC run --------------------
sampler = emcee.EnsembleSampler(nwalkers, ndim, log_posterior)

print("Running MCMC...")
sampler.run_mcmc(pos, nsteps, progress=True)

samples = sampler.get_chain(discard=500, thin=10, flat=True)

# -------------------- Corner plot --------------------
labels = [r"$\Omega_{M,0}$", r"$\Omega_{\Lambda,0}$", r"$h$"]
fig = corner.corner(
    samples,
    labels=labels,
    truths=[true_cosmo['omega_M_0'], true_cosmo['omega_lambda_0'], true_cosmo['h']],
    show_titles=True,
    title_fmt=".3f",
    title_kwargs={"fontsize": 12}
)
plt.show()

# -------------------- Histogrammes marginals --------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for i in range(3):
    ax = axes[i]
    data = samples[:, i]
    median = np.median(data)
    p16 = np.percentile(data, 16)
    p84 = np.percentile(data, 84)

    ax.hist(data, bins=30, density=True, alpha=0.6)
    ax.axvline(median, color='r', label=f"Médiane = {median:.3f}")
    ax.axvline(p16, color='r', linestyle='--', label="68% intervalle")
    ax.axvline(p84, color='r', linestyle='--')

    ax.set_xlabel(labels[i])
    ax.set_ylabel("Densité")
    ax.legend()
plt.tight_layout()
plt.show()

# -------------------- Fit modèle vs données --------------------
best_params = np.median(samples, axis=0)
cosmo_best = {'omega_M_0': best_params[0], 'omega_lambda_0': best_params[1], 'w0': -1, 'h': best_params[2]}
mu_model = cs.musn1a(redshifts, cosmo_best)

plt.errorbar(redshifts, mu_exp, yerr=sigma_mu_exp, fmt='o', label='Données SNIa')
plt.plot(redshifts, mu_model, label='Modèle ajusté', color='red')
plt.xlabel("Redshift $z$")
plt.ylabel("Distance Modulus $\mu$")
plt.legend()
plt.title("Ajustement cosmologique (meilleur modèle)")
plt.grid(True)
plt.show()