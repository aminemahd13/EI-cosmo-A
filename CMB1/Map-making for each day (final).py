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

azimuth = point_array[0]
l = point_array[1]
elevation = point_array[2]
ra = point_array[3]
dec = point_array[4]
b = point_array[5]
_ = point_array[6]

# --- Convert to HEALPix angles ---
sky_coords = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame="icrs")
theta = np.pi / 2 - sky_coords.dec.radian
phi = sky_coords.ra.radian

pixel_indices = hp.ang2pix(nside, theta, phi)

# --- Fill map and hit count ---
for i, pix in enumerate(pixel_indices):
    day_map[pix] += tod[i]
    hit_count[pix] += 1

# --- Normalize ---
final_map = np.full(npix, hp.UNSEEN)
valid = hit_count > 0
final_map[valid] = day_map[valid] / hit_count[valid]
np.savetxt("hit_count_day_"+str(day)+".txt", hit_count, fmt="%d")
# --- Plot ---
hp.mollview(
    final_map,
    title="Sky Map - Day "+ str(day)+ "(RA/Dec, No Elevation Mask)",
    unit="μK",
    coord="C",
    cmap="inferno",
    min=np.percentile(final_map[valid], 1),
    max=np.percentile(final_map[valid], 99)
)
hp.graticule()
plt.show()
