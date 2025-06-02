#!/usr/bin/env python3

# Standard imports
import os
import sys
import logging
import math
import random
import glob
import tarfile
import subprocess

# Scientific computing imports
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import norm
import pandas as pd

# Astronomy specific imports
try:
    from astropy.io import fits
    from astropy.cosmology import WMAP9 as cosmo
except ImportError:
    print("Warning: astropy not found. Install with: pip install astropy")

# Google Drive imports
try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    from oauth2client.client import GoogleCredentials
except ImportError:
    print("Warning: PyDrive not found. Install with: pip install PyDrive")

# Configure matplotlib for VS Code
plt.style.use('default')
plt.rcParams['figure.figsize'] = (17, 10)
plt.rcParams['font.size'] = 12
plt.rcParams['text.usetex'] = False

# Configure pandas display
pd.options.display.float_format = '{:,.2f}'.format

class GoogleDriveDownloader:
    """
    Class to handle Google Drive authentication and file downloading
    """
    
    def __init__(self):
        self.drive = None
        self.authenticated = False
    
    def authenticate(self):
        """
        Authenticate with Google Drive
        Note: This requires setting up OAuth2 credentials
        """
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
            
            self.drive = GoogleDrive(gauth)
            self.authenticated = True
            print("Successfully authenticated with Google Drive")
            
        except Exception as e:
            print(f"Authentication failed: {e}")
            print("Please ensure you have set up OAuth2 credentials")
            self.authenticated = False
    
    def download_file(self, file_id, filename):
        """
        Download a file from Google Drive
        
        Args:
            file_id (str): Google Drive file ID
            filename (str): Local filename to save as
        """
        if not self.authenticated:
            print("Not authenticated. Please run authenticate() first.")
            return False
        
        try:
            download = self.drive.CreateFile({'id': file_id})
            download.GetContentFile(filename)
            print(f"Successfully downloaded {filename}")
            return True
        except Exception as e:
            print(f"Failed to download {filename}: {e}")
            return False
    
    def extract_tar_file(self, filename):
        """
        Extract a .tgz or .tar.gz file
        
        Args:
            filename (str): Path to the tar file
        """
        try:
            with tarfile.open(filename, 'r:gz') as tar:
                tar.extractall()
            print(f"Successfully extracted {filename}")
            return True
        except Exception as e:
            print(f"Failed to extract {filename}: {e}")
            return False

def setup_environment():
    """
    Set up the environment and install required packages
    """
    required_packages = [
        'PyDrive',
        'astropy',
        'pandas',
        'numpy',
        'matplotlib',
        'scipy'
    ]
    
    for package in required_packages:
        try:
            __import__(package.lower())
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_datasets():
    """
    Download all the datasets from Google Drive
    """
    downloader = GoogleDriveDownloader()
    downloader.authenticate()
    
    if not downloader.authenticated:
        print("Cannot proceed without authentication")
        return
    
    # Dataset definitions
    datasets = {
        'Test-Data.tgz': '1QeWXTbwe60QuH06l18IJ45wv2eBgg62C',
        'Data-Search.tgz': '1F1mFRZFAFCEJumipFGoJr8TJb6oc7naI',
        'Data-Photometry.tgz': '1hCuUymLv2o17R9noyAV0Hrxp9CV8rv3k',
        'Data-LightCurves.tgz': '1Ih8AQsMCmSESWytcztyJKGVvnP_-VAsC'
    }
    
    # Ask user which datasets to download
    print("Available datasets:")
    for i, (filename, file_id) in enumerate(datasets.items(), 1):
        print(f"{i}. {filename}")
    
    choice = input("Enter dataset numbers to download (comma-separated, or 'all'): ").strip()
    
    if choice.lower() == 'all':
        selected_datasets = list(datasets.items())
    else:
        try:
            indices = [int(x.strip()) for x in choice.split(',')]
            selected_datasets = [list(datasets.items())[i-1] for i in indices]
        except (ValueError, IndexError):
            print("Invalid selection. Downloading Test-Data by default.")
            selected_datasets = [('Test-Data.tgz', datasets['Test-Data.tgz'])]
    
    # Download and extract selected datasets
    for filename, file_id in selected_datasets:
        print(f"\nDownloading {filename}...")
        if downloader.download_file(file_id, filename):
            print(f"Extracting {filename}...")
            downloader.extract_tar_file(filename)

def list_downloaded_files():
    """
    List all files in the current directory
    """
    print("\nFiles in current directory:")
    for item in sorted(os.listdir('.')):
        if os.path.isfile(item):
            size = os.path.getsize(item)
            print(f"  {item} ({size} bytes)")
        else:
            print(f"  {item}/ (directory)")

def main():
    """
    Main function to run the script
    """
    print("EI Cosmo A - Data Analysis Setup")
    print("=" * 40)
    
    # Setup environment
    print("Setting up environment...")
    setup_environment()
    
    # Download datasets
    print("\nDownloading datasets...")
    download_datasets()
    
    # List files
    list_downloaded_files()
    
    print("\nSetup complete! You can now proceed with your analysis.")

if __name__ == "__main__":
    main()