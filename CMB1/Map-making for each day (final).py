import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

# --- HEALPix Setup ---
nside = 128
npix = hp.nside2npix(nside)
day_map = np.zeros(npix)
hit_count = np.zeros(npix)

day = 0
print(f"Processing day {day}...")
with fits.open(f"TOD/TOD_day{day}.fits") as hdul_tod:
    tod = hdul_tod[0].data

with fits.open(f"Pointings/pointing_day{day}.fits") as hdul_point:
    point_array = hdul_point[0].data  # Shape: (7, N)

# --- Assign fields ---
azimuth = point_array[1]             # Horizontal azimuth (not used here)
elevation = point_array[2]           # Horizontal elevation (not used here)
ra = point_array[3]                  # Right Ascension (unused for this version)
dec = point_array[4]                 # Declination (unused for this version)
b = point_array[5]                   # Galactic latitude
l = point_array[6]                   # Galactic longitude

# --- Convert to HEALPix angles using Galactic coordinates ---
sky_coords = SkyCoord(l=l * u.deg, b=b * u.deg, frame="galactic")
theta = np.pi / 2 - sky_coords.b.radian  # co-latitude
phi = sky_coords.l.radian                # longitude

pixel_indices = hp.ang2pix(nside, theta, phi)

# --- Fill map and hit count ---
for i, pix in enumerate(pixel_indices):
    day_map[pix] += tod[i]
    hit_count[pix] += 1

# --- Normalize ---
final_map = np.full(npix, hp.UNSEEN)
valid = hit_count > 0
final_map[valid] = day_map[valid] / hit_count[valid]
hdu = fits.PrimaryHDU(hit_count)
hdu.writeto("hit_count_day"+str(day)+".fits", overwrite=True)

# --- Plot ---
hp.gnomview(final_map,
            rot=[np.mean(l), np.mean(b), 0],
            coord='G',           # 'G' for Galactic coordinates
            reso=20,
            min=-200,
            max=200)

hp.graticule()
plt.show()
