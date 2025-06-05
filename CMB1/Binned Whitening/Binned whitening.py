import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def robust_quotient_tod_binned(signal, fs=1000.0, n_bins=50):
    """Compute properly scaled quotient TOD using binned whitening."""
    N = len(signal)
    
    # FFT
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    
    # Remove DC
    working_freqs = freqs[1:]
    working_fft = fft_vals[1:]
    magnitudes = np.abs(working_fft)
    
    # Binned averaging
    log_freqs = np.log10(working_freqs)
    bins = np.linspace(log_freqs.min(), log_freqs.max(), n_bins+1)
    digitized = np.digitize(log_freqs, bins)
    
    binned_freqs = []
    binned_magnitudes = []
    
    for i in range(1, n_bins+1):
        idx = digitized == i
        if np.any(idx):
            binned_freqs.append(np.mean(working_freqs[idx]))
            binned_magnitudes.append(np.mean(magnitudes[idx]))
    
    binned_freqs = np.array(binned_freqs)
    binned_magnitudes = np.array(binned_magnitudes)
    
    # Fit noise model to binned data
    def model(f, a, b):
        return np.sqrt(a + b / f)
    
    popt, _ = curve_fit(model, binned_freqs, binned_magnitudes, p0=(1, 1), maxfev=5000)
    a, b = popt
    
    # Use fitted model for original (unbinned) frequencies
    fitted = model(working_freqs, a, b)
    
    # Compute scaled quotient
    quotient = (np.sqrt(a) * magnitudes) / fitted
    
    # Reconstruct FFT
    reconstructed = np.zeros_like(fft_vals, dtype=complex)
    reconstructed[0] = fft_vals[0]  # DC component
    reconstructed[1:] = quotient * np.exp(1j * np.angle(working_fft))
    
    # Nyquist
    if N % 2 == 0:
        reconstructed[-1] = (np.sqrt(a) * np.abs(fft_vals[-1])) / fitted[-1] * np.exp(1j * np.angle(fft_vals[-1]))
    
    # Inverse FFT
    quotient_tod = np.fft.irfft(reconstructed, n=N)
    
    return quotient_tod, a, b, binned_freqs, binned_magnitudes, bins

# Load data
with fits.open('TOD_day0.fits') as hdul:
    signal = hdul[0].data.flatten()

# Compute binned whitening quotient TOD
quotient_tod, a, b, binned_freqs, binned_magnitudes, bins = robust_quotient_tod_binned(signal)

print(f"Fit parameters (binned whitening): a={a:.3e}, b={b:.3e}")

# Plotting
plt.figure(figsize=(14,5))
plt.subplot(131)
plt.plot(quotient_tod[:1000])
plt.title(f"First 1000 samples (mean={np.mean(quotient_tod):.2f})")
plt.axhline(1.0, color='r', linestyle='--')

plt.subplot(132)
plt.hist(quotient_tod, bins=100, density=True)
plt.title("Distribution of quotient TOD")

plt.subplot(133)
plt.loglog(binned_freqs, binned_magnitudes, 'o', label='Binned data')
plt.loglog(binned_freqs, np.sqrt(a + b / binned_freqs), '-', label='Fitted noise model')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.legend()
plt.title("Noise model fit (binned whitening)")

plt.tight_layout()
plt.show()

# Save
fits.PrimaryHDU(quotient_tod).writeto('binned_whitened_quotient.fits', overwrite=True)