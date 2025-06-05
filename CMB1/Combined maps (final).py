import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

# --- HEALPix Setup ---
nside = 128
npix = hp.nside2npix(nside)
combined_map = np.zeros(npix)
hit_count = np.zeros(npix)

# --- Loop over 9 days ---
for day in range(9):
    print(f"Processing day {day}...")
    with fits.open(f"TOD/TOD_day{day}.fits") as hdul_tod:
        tod = hdul_tod[0].data

    with fits.open(f"Pointings/pointing_day{day}.fits") as hdul_point:
        point_array = hdul_point[0].data  # Shape: (7, N)

    # --- Parameters ---
    azimuth = point_array[0]
    l = point_array[1]             # Galactic longitude
    elevation = point_array[2]     # Altitude in degrees
    ra = point_array[3]            # Right ascension
    dec = point_array[4]           # Declination
    b = point_array[5]             # Galactic latitude
    _ = point_array[6]             # Orientation / unused

    # --- No elevation mask applied ---
    # Use all values as-is

    # --- Convert to HEALPix angles using RA/Dec ---
    sky_coords = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame="icrs")
    theta = np.pi / 2 - sky_coords.dec.radian
    phi = sky_coords.ra.radian

    pixel_indices = hp.ang2pix(nside, theta, phi)

    # --- Accumulate TOD values and hit counts ---
    for i, pix in enumerate(pixel_indices):
        combined_map[pix] += tod[i]
        hit_count[pix] += 1

# --- Normalize map ---
final_map = np.full(npix, hp.UNSEEN)
valid = hit_count > 0
final_map[valid] = combined_map[valid] / hit_count[valid]
np.savetxt("hit_count_combined.txt", hit_count, fmt="%d")
# --- Plot ---
hp.gnomview(final_map,
            rot = [sum(point_array[3]) / len(point_array[3]), sum(point_array[4]) / len(point_array[4]),0],
            coord='C',
            reso = 10, min= -200, max = 200)


hp.graticule()
plt.show()

