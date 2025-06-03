import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

# --- Load Data from Files ---
# Load TOD (1D array)
tod = np.loadtxt("tod_data.txt")

# Load pointings (lon, lat in degrees) and convert to radians
lon_deg, lat_deg = np.loadtxt("pointings.txt", unpack=True)
lon = np.radians(lon_deg)        # RA-like [0, 360°] → [0, 2π]
lat = np.radians(lat_deg)        # Dec-like [-90°, 90°] → [-π/2, π/2]
theta = np.pi/2 - lat            # HEALPix theta [0, π]

# --- Bin TOD into HEALPix Map ---
nside = 64                       # Pixel resolution (must be power of 2)
pixel_indices = hp.ang2pix(nside, theta, lon)
hpx_map = np.zeros(hp.nside2npix(nside))
for i, pix in enumerate(pixel_indices):
    hpx_map[pix] += tod[i]       # Sum TOD per pixel (or use np.bincount)

# --- Plot ---
hp.mollview(hpx_map, title="TOD Binned into HEALPix Map", unit="ΔT")
hp.graticule()                    # Add grid lines
plt.show()