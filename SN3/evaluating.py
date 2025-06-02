
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import os

with open('SN3/Data-LightCurves/Data-LightCurves/EI2019-Data-LightCurves-SN-Redshifts.txt', 'r') as f:
    y_true = np.array([float(line.strip()) for line in f if line.strip()])

iterations = np.arange(1, 10)  
hyperparams = np.linspace(0.1, 1.0, 10)  

mae_matrix = np.zeros((len(iterations), len(hyperparams)))

for i, it in enumerate(iterations):
    for j, hp in enumerate(hyperparams):
        np.random.seed(it * 100 + j)  
        y_pred = y_true + np.random.normal(loc=0, scale=j, size=len(y_true))
        mae = np.mean(np.abs(y_pred - y_true))
        mae_matrix[i, j] = mae

X, Y = np.meshgrid(hyperparams, iterations)
Z = mae_matrix

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.85)
ax.set_xlabel('Hyperparamètre (écart-type du bruit)')
ax.set_ylabel('Itération')
ax.set_zlabel('MAE')
ax.set_title('MAE en fonction des itérations et hyperparamètres')
fig.colorbar(surf, shrink=0.5, aspect=10, label='MAE')
plt.tight_layout()
plt.show()
