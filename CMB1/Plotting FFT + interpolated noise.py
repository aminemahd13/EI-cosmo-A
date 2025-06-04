import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy.optimize import curve_fit

# --- Load signal from FITS file ---
filename = 'TOD_day0.fits'

with fits.open(filename) as hdul:
    data = hdul[0].data
    signal = data.flatten()

# --- Sampling rate in Hz ---
fs = 1000.0  # <-- Replace with actual value

# --- Compute FFT ---
N = len(signal)
freqs = np.fft.rfftfreq(N, d=1/fs)
fft_vals = np.fft.rfft(signal)
magnitude = np.abs(fft_vals)


# --- Remove f=0 to avoid division by zero in model ---
freqs = freqs[1:]
magnitude = magnitude[1:]

# --- Fit model: sqrt(a + b/f) to magnitude spectrum ---
def model(f, a, b):
    return np.sqrt(a + b / f)

popt, _ = curve_fit(model, freqs, magnitude, p0=(1, 1))
fitted_magnitude = model(freqs, *popt)
quotient = magnitude / fitted_magnitude
# --- Plot ---
plt.figure(figsize=(10, 5))
plt.plot(np.log10(freqs), magnitude, label='|FFT(signal)|', color='blue')
plt.plot(np.log10(freqs), fitted_magnitude, label='Fit: √(a + b/f)', color='red', linestyle='--')
plt.plot(np.log10(freqs), quotient*1e6, label='quotient', color="green")
plt.xlabel('log₁₀(Frequency [Hz])')
plt.ylabel('Magnitude')
plt.title('FFT Magnitude and √(a + b/f) Fit')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Print fitted parameters ---
print(f"Fitted parameters:\n  a = {popt[0]:.4e}\n  b = {popt[1]:.4e}")
