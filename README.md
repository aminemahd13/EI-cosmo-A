# EI Cosmo A - VS Code Setup Instructions

## Setup Instructions

### 1. Install Dependencies
First, install all required Python packages:

```powershell
pip install -r requirements.txt
```

Or install them individually:
```powershell
pip install PyDrive astropy pandas numpy matplotlib scipy oauth2client
```

### 2. Google Drive Authentication Setup

To use Google Drive functionality, you need to:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file and save it as `client_secrets.json` in this directory

### 3. Usage

#### Option A: Use the main script
```powershell
python "exemple drive.py"
```

This will:
- Set up the environment
- Authenticate with Google Drive
- Allow you to select which datasets to download
- Extract the downloaded files automatically

#### Option B: Manual approach
If you prefer to work step by step, you can import the functions:

```python
from exemple_drive import GoogleDriveDownloader, setup_environment

# Setup environment
setup_environment()

# Create downloader and authenticate
downloader = GoogleDriveDownloader()
downloader.authenticate()

# Download specific files
downloader.download_file('1QeWXTbwe60QuH06l18IJ45wv2eBgg62C', 'Test-Data.tgz')
downloader.extract_tar_file('Test-Data.tgz')
```

## Available Datasets

- **Test-Data.tgz** (ID: 1QeWXTbwe60QuH06l18IJ45wv2eBgg62C) - Contains test data with true values
- **Data-Search.tgz** (ID: 1F1mFRZFAFCEJumipFGoJr8TJb6oc7naI) - WP-SN-1 search data
- **Data-Photometry.tgz** (ID: 1hCuUymLv2o17R9noyAV0Hrxp9CV8rv3k) - WP-SN-2 photometry data  
- **Data-LightCurves.tgz** (ID: 1Ih8AQsMCmSESWytcztyJKGVvnP_-VAsC) - WP-SN-3 light curves data

## Notes

- The script automatically configures matplotlib for VS Code usage
- Pandas display formatting is set to show 2 decimal places
- All imports are handled with error checking
- Authentication credentials are saved locally for reuse

## Troubleshooting

- If authentication fails, ensure you have the correct `client_secrets.json` file
- For permission errors, make sure your Google account has access to the shared files
- If imports fail, try reinstalling packages with `pip install --upgrade package_name`
