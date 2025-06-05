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

all_l = []
all_b = []

# --- Loop over 9 days ---
for day in range(9):
    print(f"Processing day {day}...")

    # Load TOD
    with fits.open(f"TOD/TOD_day{day}.fits") as hdul_tod:
        tod = hdul_tod[0].data

    # Load pointings
    with fits.open(f"Pointings/pointing_day{day}.fits") as hdul_point:
        point_array = hdul_point[0].data

    # Extract Galactic coordinates
    b = point_array[5]  # Galactic latitude
    l = point_array[6]  # Galactic longitude

    all_l.append(l)
    all_b.append(b)

    # Convert to HEALPix angles
    sky_coords = SkyCoord(l=l * u.deg, b=b * u.deg, frame="galactic")
    theta = np.pi / 2 - sky_coords.b.radian
    phi = sky_coords.l.radian

    pixel_indices = hp.ang2pix(nside, theta, phi)

    # Accumulate TOD values and hit counts
    for i, pix in enumerate(pixel_indices):
        combined_map[pix] += tod[i]
        hit_count[pix] += 1

# --- Normalize final map ---
final_map = np.full(npix, hp.UNSEEN)
valid = hit_count > 0
final_map[valid] = combined_map[valid] / hit_count[valid]

# Save hit count for reference
hdu = fits.PrimaryHDU(hit_count)
hdu.writeto("hit_count_combined.fits", overwrite=True)

# --- Compute mean Galactic center for plot ---
all_l = np.concatenate(all_l)
all_b = np.concatenate(all_b)
mean_l = np.mean(all_l)
mean_b = np.mean(all_b)

# --- Plot ---
hp.gnomview(final_map,
            rot=[mean_l, mean_b, 0],  # Centered on average galactic coords
            coord='G',
            reso=30,
            min=-200,
            max=200,
            title="Combined Galactic Map (Days 0–8)")

hp.graticule()
plt.show()
