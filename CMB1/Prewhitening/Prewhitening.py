import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def robust_quotient_tod(signal, fs=1000.0):
    """Compute properly scaled quotient TOD"""
    N = len(signal)
    
    # Compute FFT
    fft_vals = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    
    # Remove DC component
    working_freqs = freqs[1:]
    working_fft = fft_vals[1:]
    magnitudes = np.abs(working_fft)
    
    # Fit noise model
    def model(f, a, b):
        return np.sqrt(a + b/f)
    
    popt, _ = curve_fit(model, working_freqs, magnitudes, p0=(1, 1), maxfev=5000)
    a, b = popt
    fitted = model(working_freqs, a, b)
    
    # PROPER SCALING APPLIED HERE
    quotient = (np.sqrt(a) * magnitudes) / fitted
    
    # Reconstruct FFT
    reconstructed = np.zeros_like(fft_vals, dtype=complex)
    reconstructed[0] = fft_vals[0]  # DC component
    
    # Apply scaled quotient while preserving phase
    reconstructed[1:] = quotient * np.exp(1j * np.angle(working_fft))
    
    # Handle Nyquist frequency for even N
    if N % 2 == 0:
        reconstructed[-1] = (np.sqrt(a) * np.abs(fft_vals[-1])) / fitted[-1] * np.exp(1j * np.angle(fft_vals[-1]))
    
    # Inverse FFT
    quotient_tod = np.fft.irfft(reconstructed, n=N)
    
    return quotient_tod, a, b

# Load data
with fits.open('TOD_day0.fits') as hdul:
    signal = hdul[0].data.flatten()

# Compute properly scaled quotient TOD
quotient_tod, a, b = robust_quotient_tod(signal)
print(f"Fit parameters: a={a:.3e}, b={b:.3e}")

# Verify results
plt.figure(figsize=(12,4))
plt.subplot(121)
plt.plot(quotient_tod[:1000])
plt.title(f"First 1000 samples (mean={np.mean(quotient_tod):.2f})")
plt.axhline(1.0, color='r', linestyle='--')

plt.subplot(122)
plt.hist(quotient_tod, bins=100)
plt.title("Distribution of quotient TOD")
plt.tight_layout()
plt.show()

# Save results
fits.PrimaryHDU(quotient_tod).writeto('properly_scaled_quotient.fits', overwrite=True)