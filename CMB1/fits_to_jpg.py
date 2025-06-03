from astropy.io import fits
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Charger les données FITS
hdul = fits.open("map.fits")  # Remplace "map.fits" par ton nom de fichier
data = hdul[0].data
hdul.close()

# Normalisation simple : retrait du NaN et centrage
data = np.nan_to_num(data)
data_min = np.percentile(data, 1)
data_max = np.percentile(data, 99)
scaled_data = np.clip((data - data_min) / (data_max - data_min), 0, 1)

# Conversion en image RGB (optionnel)
image_array = (scaled_data * 255).astype(np.uint8)
image = Image.fromarray(image_array)

# Sauvegarde en JPEG
image.save("map.jpg")