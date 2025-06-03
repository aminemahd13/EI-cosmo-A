# MCMC

import numpy as np
import cosmolib as cs
from matplotlib.pyplot import rc, errorbar, xlim, xlabel, ylabel, legend, show, plot


# ------------------------------- Example data -------------------------------
rc('figure',figsize=(10,5))
x = np.linspace(0,1,10)
sy = 0.2
y = 3*x + 2 + np.random.randn(10)*sy
sigma_y = np.zeros(10) + sy
errorbar(x,y,yerr=sigma_y,fmt='ro', label='Sample Data')
xlim(-0.1,1.1)
xlabel('x')
ylabel('y')
legend(loc='upper left')
show()
# -----------------------------------------------------------------------------
z = np.linspace(0, 1, 150)  # Redshift values
mu_exp = np.linspace(0, 1, 150)
sigma_mu_exp = np.zeros(150) + 0.1  # Assuming a constant error for demonstration

def chi_deux(z, par):
    return (cs.musn1a(z, {'omega_M_0': par[0], 'omega_lambda_0': par[1], 'h': par[2], 'w0': -1})-mu_exp)**2/sigma_mu_exp

data = cs.Data(z, mu_exp, sigma_mu_exp, chi_deux)

# Running the MCMC exploration
guess = np.array([0.3, 0.7, 1.])
chain = data.run_mcmc(guess, nbmc=1000, allvariables=['p0', 'p1'])

# Plotting the elements of the chain
plot(chain['p0'], chain['p1'], ',', alpha=0.1)
plot(2,3,'g*', label='True Value',ms=20)
xlabel('m')
ylabel('s')
show()
