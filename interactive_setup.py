
# Standard imports for data analysis
import os
import sys
import logging
import math
import random
import glob
import tarfile


# Scientific computing imports
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import norm
import pandas as pd


# Configure matplotlib for VS Code
plt.style.use('default')
plt.rcParams['figure.figsize'] = (17, 10)
plt.rcParams['font.size'] = 12
plt.rcParams['text.usetex'] = False

# Configure pandas display
pd.options.display.float_format = '{:,.2f}'.format

print("Basic imports and configuration complete!")


# Astronomy specific imports
try:
    from astropy.io import fits
    from astropy.cosmology import WMAP9 as cosmo
    print("Astropy imports successful!")
except ImportError:
    print("Warning: astropy not found. Install with: pip install astropy")


# Google Drive imports and setup
try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    from oauth2client.client import GoogleCredentials
    print("PyDrive imports successful!")
except ImportError:
    print("Warning: PyDrive not found. Install with: pip install PyDrive")


# Simple Google Drive authentication function
def authenticate_drive():
    """Simple Google Drive authentication"""
    try:
        gauth = GoogleAuth()
        
        # Try to load saved credentials
        gauth.LoadCredentialsFile("mycreds.txt")
        
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")
        
        drive = GoogleDrive(gauth)
        print("Successfully authenticated with Google Drive")
        return drive
        
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None


# Function to download and extract files
def download_and_extract(drive, file_id, filename):
    """Download and extract a file from Google Drive"""
    try:
        # Download file
        download = drive.CreateFile({'id': file_id})
        download.GetContentFile(filename)
        print(f"Downloaded {filename}")
        
        # Extract if it's a tar file
        if filename.endswith('.tgz') or filename.endswith('.tar.gz'):
            with tarfile.open(filename, 'r:gz') as tar:
                tar.extractall()
            print(f"Extracted {filename}")
            
        return True
    except Exception as e:
        print(f"Error with {filename}: {e}")
        return False


# Authenticate with Google Drive (run this cell first)
drive = authenticate_drive()


# Download Test Data (contains true values)
if drive:
    download_and_extract(drive, '1QeWXTbwe60QuH06l18IJ45wv2eBgg62C', 'Test-Data.tgz')


# Uncomment and run to download Data-Search (WP-SN-1)
# if drive:
#     download_and_extract(drive, '1F1mFRZFAFCEJumipFGoJr8TJb6oc7naI', 'Data-Search.tgz')


# Uncomment and run to download Data-Photometry (WP-SN-2)
# if drive:
#     download_and_extract(drive, '1hCuUymLv2o17R9noyAV0Hrxp9CV8rv3k', 'Data-Photometry.tgz')


# Uncomment and run to download Data-LightCurves (WP-SN-3)
# if drive:
#     download_and_extract(drive, '1Ih8AQsMCmSESWytcztyJKGVvnP_-VAsC', 'Data-LightCurves.tgz')


# List files in current directory
print("Files in current directory:")
for item in sorted(os.listdir('.')):
    if os.path.isfile(item):
        size = os.path.getsize(item)
        print(f"  {item} ({size} bytes)")
    else:
        print(f"  {item}/ (directory)")


# Test plot to verify matplotlib is working
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Test Plot - Matplotlib Working in VS Code')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("Setup complete! You can now proceed with your data analysis.")
