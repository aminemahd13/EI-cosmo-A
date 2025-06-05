import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from scipy.optimize import curve_fit
from astropy.io import fits

# === Step 1: Load data from FITS ===
with fits.open("TOD_day0.fits") as hdul:
    data = hdul[0].data

data = data.flatten()
n = len(data)

# === Step 2: FFT and frequencies ===
Y_f = fft(data)
freqs = fftfreq(n)
P_Y = np.abs(Y_f)**2

# === Step 3: Identify frequency indices ===
half_n = n // 2
if n % 2 == 0:
    # Even length
    pos_slice = slice(1, half_n)
    neg_slice = slice(n - 1, half_n, -1)
    nyquist_idx = half_n
else:
    # Odd length
    pos_slice = slice(1, half_n + 1)
    neg_slice = slice(n - 1, half_n, -1)
    nyquist_idx = None

# === Step 4: Fit pink noise model to high positive freqs ===
freqs_pos = freqs[pos_slice]
P_Y_pos = P_Y[pos_slice]

cutoff = int(0.8 * len(freqs_pos))
fit_freqs = freqs_pos[cutoff:]
fit_power = P_Y_pos[cutoff:]

def pink_noise_model(f, c):
    return c / f

c_opt, _ = curve_fit(pink_noise_model, fit_freqs, fit_power)
c = c_opt[0]
N_f_pos = c / freqs_pos

# === Step 5: Estimate signal power and filter ===
S_f_pos = P_Y_pos - N_f_pos
S_f_pos[S_f_pos < 0] = 0
H_f_pos = S_f_pos / (S_f_pos + N_f_pos + 1e-12)

# === Step 6: Apply Wiener filter ===
Y_f_filtered = np.zeros_like(Y_f, dtype=complex)
Y_f_filtered[0] = Y_f[0]
Y_f_filtered[pos_slice] = H_f_pos * Y_f[pos_slice]
Y_f_filtered[neg_slice] = np.conj(Y_f_filtered[pos_slice][::-1])
if nyquist_idx is not None:
    Y_f_filtered[nyquist_idx] = Y_f[nyquist_idx]

# === Step 7: Inverse FFT to get filtered signal ===
x_est = np.real(ifft(Y_f_filtered))

# === Step 8: Save Wiener-filtered signal to .fits ===
hdu = fits.PrimaryHDU(data=x_est.astype(np.float32))
hdu.writeto("Wiener_filtered_map.fits", overwrite=True)
print("✅ Saved filtered signal to 'Wiener_filtered_map.fits'")

# === Plot time-domain signals ===
plt.figure(figsize=(10, 4))
plt.plot(data, label='Original Signal (with Pink Noise)', alpha=0.5)
plt.plot(x_est, label='Wiener Filtered Signal', linewidth=2)
plt.xlabel('Time Index')
plt.ylabel('Amplitude')
plt.title('Wiener Filtering with 1/f Noise (Full FFT)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Plot power spectrum fit ===
plt.figure(figsize=(8, 4))
plt.loglog(freqs_pos, P_Y_pos, label='Observed Power Spectrum')
plt.loglog(freqs_pos, N_f_pos, '--', label='Fitted 1/f Noise Power')
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.title('Power Spectrum and 1/f Noise Model')
plt.legend()
plt.grid(True, which='both')
plt.tight_layout()
plt.show()

print(f"Estimated pink noise model: N(f) = {c:.3e} / f")
