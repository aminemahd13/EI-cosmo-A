import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# --- Load signal from FITS file ---
filename = 'TOD_day0.fits'

with fits.open(filename) as hdul:
    hdul.info()  # optional: shows what's inside
    data = hdul[0].data  # assume signal is in primary HDU
    signal = data.flatten()  # ensure it's 1D

# --- Set sampling rate (Hz) ---
fs = 1000.0  # <-- CHANGE THIS to your actual sampling rate

# --- Compute FFT ---
N = len(signal)
freqs = np.fft.rfftfreq(N, d=1/fs)
fft_vals = np.fft.rfft(signal)
magnitude = np.abs(fft_vals)

# --- Plot FFT magnitude with log-frequency x-axis ---
plt.figure(figsize=(10, 5))
plt.plot(np.log10(freqs[1:]), magnitude[1:], label='|FFT(signal)|')  # skip freq=0 to avoid log(0)
plt.xlabel('log₁₀(Frequency [Hz])')
plt.ylabel('Magnitude')
plt.title('FFT of TOD_day0.fits (Log Frequency Scale)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
