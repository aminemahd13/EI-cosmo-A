import numpy as np
import os
import glob

# --- Main Data Loading Script ---

def load_all_supernova_data(light_curve_dir, redshift_file_path, model_file_path):
    """
    Loads all supernova data: individual light curves, redshifts, and the model light curve.

    Args:
        light_curve_dir (str): The directory containing the light curve files.
                               Assumes files are named like 'EI2019-Data-LightCurves-SN-{i}_lightcurve.txt'.
        redshift_file_path (str): The path to the file containing redshifts.
        model_file_path (str): The path to the file containing the SNIa model light curve.

    Returns:
        tuple: (all_light_curves, all_redshifts, model_light_curve, num_supernovae)
               all_light_curves (list): A list of numpy arrays. Each array contains
                                        the (time, magnitude, error_magnitude) for a supernova.
               all_redshifts (numpy.ndarray): A 1D array of redshifts.
               model_light_curve (numpy.ndarray): A 2D array of (time, absolute_magnitude)
                                                  for the model.
               num_supernovae (int): The actual number of loaded supernovae.
    """
    all_light_curves = []
      # Find all light curve files in the directory (exclude model and redshift files)
    light_curve_pattern = os.path.join(light_curve_dir, "EI2019-Data-LightCurves-SN-*_lightcurve.txt")
    all_files = sorted(glob.glob(light_curve_pattern))
    # Filter out non-supernova files (model and redshift files)
    light_curve_files = [f for f in all_files if not ("SNI-Average" in f or "Redshifts" in f)]
    
    print(f"Found {len(light_curve_files)} light curve files in: {light_curve_dir}")
    
    for i, filename in enumerate(light_curve_files):
        try:
            # Each file is expected to have 3 columns: time, magnitude, error_magnitude
            lc_data = np.loadtxt(filename)
            if lc_data.ndim == 1: # handles case where there might be only one row
                if lc_data.shape[0] == 3: # and it has the 3 expected values
                     lc_data = lc_data.reshape(1,3)
                else:
                    print(f"Warning: Light curve file {filename} has unexpected shape for a single row: {lc_data.shape}. Skipping.")
                    all_light_curves.append(None) # Or handle error appropriately
                    continue
            elif lc_data.ndim == 2 and lc_data.shape[1] != 3:
                print(f"Warning: Light curve file {filename} does not have 3 columns. Shape: {lc_data.shape}. Skipping.")
                all_light_curves.append(None) # Or handle error appropriately
                continue
            
            all_light_curves.append(lc_data)
            if i <= 3 or i == len(light_curve_files) - 1: # Print info for first few and last
                 print(f"Successfully loaded: {os.path.basename(filename)}, shape: {lc_data.shape}")
        except FileNotFoundError:
            print(f"Error: Light curve file not found: {filename}")
            all_light_curves.append(None) # Add a placeholder or handle error
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            all_light_curves.append(None) # Add a placeholder or handle error

    num_supernovae = len(light_curve_files)
    
    print(f"\nAttempting to load redshifts from: {redshift_file_path}")
    try:
        # Expected to be a single column file with redshifts for each supernova
        all_redshifts = np.loadtxt(redshift_file_path)
        if all_redshifts.shape[0] != num_supernovae:
            print(f"Warning: Redshift file {redshift_file_path} contains {all_redshifts.shape[0]} entries, expected {num_supernovae}.")
        print(f"Successfully loaded redshifts, shape: {all_redshifts.shape}")
    except FileNotFoundError:
        print(f"Error: Redshift file not found: {redshift_file_path}")
        all_redshifts = None # Handle error
    except Exception as e:
        print(f"Error loading {redshift_file_path}: {e}")
        all_redshifts = None

    print(f"\nAttempting to load SNIa model light curve from: {model_file_path}")
    try:
        # Expected to be a 2-column file: time, absolute_magnitude
        model_light_curve = np.loadtxt(model_file_path)
        if model_light_curve.ndim != 2 or model_light_curve.shape[1] != 2:
             print(f"Warning: Model light curve file {model_file_path} does not have 2 columns or is not 2D. Shape: {model_light_curve.shape}")
        print(f"Successfully loaded model light curve, shape: {model_light_curve.shape}")
    except FileNotFoundError:
        print(f"Error: Model light curve file not found: {model_file_path}")
        model_light_curve = None # Handle error
    except Exception as e:
        print(f"Error loading {model_file_path}: {e}")
        model_light_curve = None

    return all_light_curves, all_redshifts, model_light_curve, num_supernovae

# --- Example Usage ---
if __name__ == "__main__":
    # Configuration - Real data paths
    DATA_DIRECTORY = os.path.join("data", "Data-LightCurves")  # Path to the real data directory
    
    LIGHT_CURVE_FILES_DIR = DATA_DIRECTORY 
    REDSHIFT_FILE = os.path.join(DATA_DIRECTORY, "EI2019-Data-LightCurves-SN-Redshifts.txt")
    MODEL_FILE = os.path.join(DATA_DIRECTORY, "EI2019-Data-LightCurves-SN-SNI-Average_LightCurve.txt")

    print("--- Starting Real Data Loading ---")
    light_curves, redshifts, model_sn_lc, num_supernovae = load_all_supernova_data(
        light_curve_dir=LIGHT_CURVE_FILES_DIR,
        redshift_file_path=REDSHIFT_FILE,
        model_file_path=MODEL_FILE
    )

    print("\n--- Data Loading Summary ---")
    # Verify loaded data (basic checks)
    if light_curves:
        loaded_lc_count = sum(1 for lc in light_curves if lc is not None)
        print(f"Number of successfully loaded light curves: {loaded_lc_count}/{num_supernovae}")
        if loaded_lc_count > 0:
            # Display info for the first successfully loaded light curve
            first_valid_lc = next((lc for lc in light_curves if lc is not None), None)
            if first_valid_lc is not None:
                print(f"Data for the first loaded supernova (example):\n{first_valid_lc[:3,:]}...") # Print first 3 rows
                print("Columns: time_days, magnitude, error_magnitude")

    if redshifts is not None:
        print(f"\nRedshifts array shape: {redshifts.shape}")
        print(f"First 5 redshifts (example): {redshifts[:5]}")

    if model_sn_lc is not None:
        print(f"\nModel SNIa light curve array shape: {model_sn_lc.shape}")
        print(f"First 3 points of the model (example):\n{model_sn_lc[:3,:]}...")
        print("Columns: time_days_relative_peak, absolute_magnitude")

    print("\n--- Next Steps ---")
    print("With the real data loaded, you can now proceed with WP-SN-3 tasks:")
    print("1. For each supernova:")
    print("   a. Access its light curve data (e.g., light_curves[i]).")
    print("   b. Access its redshift (e.g., redshifts[i]).")
    print("   c. Fit the observed light curve (time-shifted and magnitude-adjusted due to redshift and distance)")
    print("      to the model light curve (model_sn_lc), possibly adjusting for stretch/color.")
    print("   d. Determine the distance modulus.")
    print("2. Use all distance moduli and redshifts to constrain cosmological parameters using MCMC.")
    print("3. Collaborate with the CMB team for a joint analysis.")