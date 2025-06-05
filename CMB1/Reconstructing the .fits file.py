import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit

# --- Load original FITS signal ---
filename = 'TOD_day0.fits'
with fits.open(filename) as hdul:
    data = hdul[0].data
    signal = data.flatten()

# --- Sampling rate ---
fs = 1000.0  # Replace with actual sampling rate

# --- FFT ---
N = len(signal)
freqs = np.fft.rfftfreq(N, d=1/fs)
fft_vals = np.fft.rfft(signal)

# --- Magnitude and phase ---
magnitude = np.abs(fft_vals)
phase = np.angle(fft_vals)

# --- Remove DC ---
freqs = freqs[1:]
magnitude = magnitude[1:]
phase = phase[1:]

# --- Fit model ---
def model(f, a, b):
    return np.sqrt(a + b / f)

popt, _ = curve_fit(model, freqs, magnitude, p0=(1, 1))
fitted_magnitude = model(freqs, *popt)
quotient = magnitude / fitted_magnitude

# --- Reconstruct FFT (remove DC separately) ---
reconstructed_fft = np.zeros(N//2 + 1, dtype=complex)
reconstructed_fft[1:] = quotient * fitted_magnitude * np.exp(1j * phase)

# Optionally restore DC component as zero or mean
reconstructed_fft[0] = 0.0  # or np.mean(np.real(fft_vals))

# --- Inverse FFT ---
reconstructed_signal = np.fft.irfft(reconstructed_fft, n=N)

# --- Save to FITS ---
hdu = fits.PrimaryHDU(reconstructed_signal.reshape(data.shape))
hdu.writeto('reconstructed_signal.fits', overwrite=True)

print("Reconstructed signal saved to 'reconstructed_signal.fits'")
