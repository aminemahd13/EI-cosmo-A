import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.coordinates import SkyCoord, CartesianRepresentation
import astropy.units as u
from PIL import Image
import io

# --- Setup ---
nside = 64
npix = hp.nside2npix(nside)
combined_map = np.zeros(npix)
combined_hits = np.zeros(npix)
sin_pol = np.zeros(npix)
cos_pol = np.zeros(npix)

# --- Loop over all 9 days ---
for day in range(9):
    print(f"Processing day {day}...")

    with fits.open(f"TOD/TOD_day{day}.fits") as hdul_tod:
        tod = hdul_tod[0].data

    with fits.open(f"Pointings/pointing_day{day}.fits") as hdul_point:
        point_array = hdul_point[0].data

    # Elevation mask
    mask = point_array[2] > 20.0
    tod = tod[mask]
    l = point_array[1][mask]
    b = point_array[3][mask]

    # Convert galactic to equatorial
    sky_gal = SkyCoord(l=l * u.deg, b=b * u.deg, frame='galactic')
    sky_eq = sky_gal.icrs
    theta = (np.pi / 2) - sky_eq.dec.radian
    phi = sky_eq.ra.radian

    # Orientation vector and polarization angle
    x_gal = point_array[4][mask]
    y_gal = point_array[5][mask]
    z_gal = point_array[6][mask]
    orientation_gal = CartesianRepresentation(x_gal, y_gal, z_gal)
    orientation_eq = SkyCoord(orientation_gal, frame='galactic').transform_to('icrs')
    pol_angle = np.arctan2(
        orientation_eq.cartesian.y.value,
        orientation_eq.cartesian.x.value
    )

    pixel_indices = hp.ang2pix(nside, theta, phi)

    for i, pix in enumerate(pixel_indices):
        combined_map[pix] += tod[i]
        sin_pol[pix] += np.sin(pol_angle[i])
        cos_pol[pix] += np.cos(pol_angle[i])
        combined_hits[pix] += 1

# Final normalized map
final_map = np.full(npix, hp.UNSEEN)
valid = combined_hits > 0
final_map[valid] = combined_map[valid] / combined_hits[valid]
final_pol_angle = np.zeros(npix)
final_pol_angle[valid] = np.arctan2(sin_pol[valid], cos_pol[valid])

# --- Plot Intensity Map with Polarization Vectors ---
hp.mollview(
    final_map,
    title="Combined Map (9 Days)",
    unit="μK",
    min=-100, max=100,
    cmap="viridis"
)
hp.graticule()

# Overlay polarization vectors
plt.figure()
ax = plt.gca()
indices = np.where(valid)[0][::50]
theta_pix, phi_pix = hp.pix2ang(nside, indices)
P = 0.2
x = P * np.cos(final_pol_angle[indices])
y = P * np.sin(final_pol_angle[indices])

hp.projscatter(theta_pix, phi_pix, c='k', s=2, lonlat=False)
for i in range(len(indices)):
    ax.quiver(
        phi_pix[i], np.pi/2 - theta_pix[i],
        x[i], y[i],
        color='red', scale=25, width=0.003, headwidth=0
    )
hp.graticule()
plt.tight_layout()

plt.show()
