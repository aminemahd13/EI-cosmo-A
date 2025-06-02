import numpy as np
import os # Used for creating dummy files for demonstration

# --- Helper function to create dummy files for demonstration ---
def create_dummy_files(num_supernovae=150, data_dir="sn_data"):
    """Creates dummy data files for demonstration purposes."""
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Dummy light curve files
    for i in range(1, num_supernovae + 1):
        filename = os.path.join(data_dir, f"supernova_{i:03d}.txt")
        # Each file has 10 observations, 3 columns: time, mag, err_mag
        time = np.sort(np.random.rand(10) * 100) # time in days
        mag = 18 + np.random.rand(10) * 2 - 1    # magnitude
        err_mag = 0.1 + np.random.rand(10) * 0.1 # error in magnitude
        data = np.column_stack((time, mag, err_mag))
        np.savetxt(filename, data, header="time_days magnitude error_magnitude", comments="# ")
    print(f"Created {num_supernovae} dummy light curve files in '{data_dir}'")

    # Dummy redshift file
    redshift_filename = os.path.join(data_dir, "redshifts.txt")
    redshifts = np.random.rand(num_supernovae) * 0.5 # redshifts up to 0.5
    np.savetxt(redshift_filename, redshifts, header="redshift", comments="# ")
    print(f"Created dummy redshift file: '{redshift_filename}'")

    # Dummy model light curve file
    model_filename = os.path.join(data_dir, "model_snia_light_curve.txt")
    model_time = np.linspace(-20, 50, 71) # time in days relative to peak
    model_abs_mag = -19.3 + (model_time/10)**2 - (model_time/30)**3 # A very simple model
    model_data = np.column_stack((model_time, model_abs_mag))
    np.savetxt(model_filename, model_data, header="time_days_relative_peak absolute_magnitude", comments="# ")
    print(f"Created dummy model light curve file: '{model_filename}'")

# --- Main Data Loading Script ---

def load_all_supernova_data(num_supernovae, light_curve_dir, redshift_file_path, model_file_path):
    """
    Loads all supernova data: individual light curves, redshifts, and the model light curve.

    Args:
        num_supernovae (int): The total number of supernovae.
        light_curve_dir (str): The directory containing the light curve files.
                               Assumes files are named like 'supernova_001.txt', etc.
        redshift_file_path (str): The path to the file containing redshifts.
        model_file_path (str): The path to the file containing the SNIa model light curve.

    Returns:
        tuple: (all_light_curves, all_redshifts, model_light_curve)
               all_light_curves (list): A list of numpy arrays. Each array contains
                                        the (time, magnitude, error_magnitude) for a supernova.
               all_redshifts (numpy.ndarray): A 1D array of redshifts.
               model_light_curve (numpy.ndarray): A 2D array of (time, absolute_magnitude)
                                                  for the model.
    """
    all_light_curves = []
    
    print(f"Attempting to load light curves from: {light_curve_dir}")
    for i in range(1, num_supernovae + 1):
        # Adjust the filename pattern as needed
        # Example: 'sn_data_fieldX_numY.txt', 'supernova_id_Z.txt'
        filename = os.path.join(light_curve_dir, f"supernova_{i:03d}.txt")
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
            if i <= 3 or i == num_supernovae : # Print info for first few and last
                 print(f"Successfully loaded: {filename}, shape: {lc_data.shape}")
        except FileNotFoundError:
            print(f"Error: Light curve file not found: {filename}")
            all_light_curves.append(None) # Add a placeholder or handle error
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            all_light_curves.append(None) # Add a placeholder or handle error

    print(f"\nAttempting to load redshifts from: {redshift_file_path}")
    try:
        # Expected to be a single column file with 'num_supernovae' rows
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

    return all_light_curves, all_redshifts, model_light_curve

# --- Example Usage ---
if __name__ == "__main__":
    # Configuration - IMPORTANT: Adjust these paths to your actual data locations
    NUMBER_OF_SUPERNOVAE = 150
    DATA_DIRECTORY = "sn_data_wp3"  # Create this directory and place your files here
                                 # or point to your existing directory.
    
    # Create dummy files for the script to run.
    # In a real scenario, you would comment this line out and use your actual files.
    create_dummy_files(num_supernovae=NUMBER_OF_SUPERNOVAE, data_dir=DATA_DIRECTORY)

    LIGHT_CURVE_FILES_DIR = DATA_DIRECTORY 
    REDSHIFT_FILE = os.path.join(DATA_DIRECTORY, "redshifts.txt")
    MODEL_FILE = os.path.join(DATA_DIRECTORY, "model_snia_light_curve.txt")

    print("--- Starting Data Loading ---")
    light_curves, redshifts, model_sn_lc = load_all_supernova_data(
        num_supernovae=NUMBER_OF_SUPERNOVAE,
        light_curve_dir=LIGHT_CURVE_FILES_DIR,
        redshift_file_path=REDSHIFT_FILE,
        model_file_path=MODEL_FILE
    )

    print("\n--- Data Loading Summary ---")
    # Verify loaded data (basic checks)
    if light_curves:
        loaded_lc_count = sum(1 for lc in light_curves if lc is not None)
        print(f"Number of successfully loaded light curves: {loaded_lc_count}/{NUMBER_OF_SUPERNOVAE}")
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
    print("With the data loaded, you can now proceed with WP-SN-3 tasks:")
    print("1. For each supernova:")
    print("   a. Access its light curve data (e.g., light_curves[i]).")
    print("   b. Access its redshift (e.g., redshifts[i]).")
    print("   c. Fit the observed light curve (time-shifted and magnitude-adjusted due to redshift and distance)")
    print("      to the model light curve (model_sn_lc), possibly adjusting for stretch/color.")
    print("   d. Determine the distance modulus.")
    print("2. Use all distance moduli and redshifts to constrain cosmological parameters using MCMC.")
    print("3. Collaborate with the CMB team for a joint analysis.")