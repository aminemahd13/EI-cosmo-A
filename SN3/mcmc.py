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



# function to fit
# def fit_function(x, par):
#     return 1./(np.sqrt(2.*np.pi)*par[1]) * np.exp(-(x-par[0])**2/(2.*par[1]**2))

def test_fonction(x, par):
    return par[0] + par[1]*x

data = cs.Data(x, y, sigma_y, test_fonction)

# Running the MCMC exploration
guess = np.array([0., 0.]) # Initial guess for parameters [p0, p1]
chain = data.run_mcmc(guess, nbmc=1000, allvariables=['p0', 'p1'])

# Plotting the elements of the chain
plot(chain['p0'], chain['p1'], ',', alpha=0.1)
plot(2,3,'g*', label='True Value',ms=20)
xlabel('m')
ylabel('s')
show()