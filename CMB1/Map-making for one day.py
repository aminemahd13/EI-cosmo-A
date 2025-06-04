import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.coordinates import SkyCoord, CartesianRepresentation
import astropy.units as u

# --- Load Data ---
with fits.open("TOD/TOD_day1.fits") as hdul_tod:
    tod = hdul_tod[0].data  # Shape: (N,) for intensity

with fits.open("Pointings/pointing_day1.fits") as hdul_point:
    point_array = hdul_point[0].data  # shape: (7, N)

# --- Filter by elevation ---
mask = point_array[2] > 20.0  # Skip low elevation
tod = tod[mask]
l = point_array[1][mask]
b = point_array[3][mask]

# --- Convert (l, b) → Equatorial (RA, Dec) ---
sky_gal = SkyCoord(l=l * u.deg, b=b * u.deg, frame='galactic')
sky_eq = sky_gal.icrs
theta = (np.pi / 2) - sky_eq.dec.radian  # HEALPix colatitude
phi = sky_eq.ra.radian                   # HEALPix longitude

# --- Compute Polarization Angle (from orientation vectors) ---
x_gal = point_array[4][mask]
y_gal = point_array[5][mask]
z_gal = point_array[6][mask]
orientation_gal = CartesianRepresentation(x_gal, y_gal, z_gal)
orientation_eq = SkyCoord(orientation_gal, frame='galactic').transform_to('icrs')
pol_angle = np.arctan2(orientation_eq.cartesian.y.value, orientation_eq.cartesian.x.value)

# --- HEALPix Map Setup ---
nside = 64
npix = hp.nside2npix(nside)
hpx_map = np.zeros(npix)       # Intensity map
pol_angle_map = np.zeros(npix) # Polarization angle map
hits = np.zeros(npix)

# --- Assign TOD and pol_angle to pixels ---
pixel_indices = hp.ang2pix(nside, theta, phi)
for i, pix in enumerate(pixel_indices):
    hpx_map[pix] += tod[i]          # Accumulate intensity
    pol_angle_map[pix] = pol_angle[i] # Store latest pol_angle per pixel
    hits[pix] += 1

# Normalize intensity by hits
hpx_map[hits > 0] /= hits[hits > 0]
hpx_map[hits == 0] = hp.UNSEEN

# --- Plot Intensity with Polarization Vectors ---
hp.mollview(hpx_map, title="Intensity + Polarization Angle", unit="μK", min=-100, max=100)

# Prepare vector components
indices = np.where(hits > 0)[0]
theta_pix, phi_pix = hp.pix2ang(nside, indices)
P = 0.2  # Vector length scaling factor

# Convert spherical to Cartesian coordinates for vector directions
x = P * np.cos(pol_angle_map[indices])
y = P * np.sin(pol_angle_map[indices])

# Plot vectors using quiver (corrected approach)
plt.figure()
ax = plt.gca()
hp.projscatter(theta_pix, phi_pix, c='k', s=1, lonlat=False)  # Pointings
for i in range(len(indices)):
    ax.quiver(
        phi_pix[i], np.pi/2 - theta_pix[i],  # Convert to (lon, lat)
        x[i], y[i],
        color='red', scale=25, width=0.002, headwidth=0
    )
hp.graticule()
plt.show()