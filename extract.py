import os
import scipy.io as sio
import numpy as np
import pandas as pd
import glob

# Define the directory where your .mat files are located
data_dir = '/path/to/your/data/directory'

# Define the pattern to match files (Subject_*_Condition_*)
file_pattern = os.path.join(data_dir, 'Subject_*_Condition_*.mat')

# Find all matching files using glob
mat_files = glob.glob(file_pattern)

# Initialize a list to store the Fisher's Z-scores
z_scores_list = []

# Loop through each .mat file
for file in mat_files:
    # Load the .mat file
    mat_data = sio.loadmat(file)
    
    # You may need to explore the contents of mat_data to determine the correct key for the Z-scores
    # Let's assume the Z-scores are stored in a key called 'z_scores'
    # For example, if z_scores are stored as a matrix in mat_data['z_scores']
    
    try:
        z_scores = mat_data['z_scores']  # Replace with the actual key name from your .mat files
        
        # If the Z-scores are in a 2D array, you might need to apply Fisher's Z transformation
        # if the data is in Pearson's r format. You can skip this if Z-scores are already provided.
        
        # Check if z_scores need Fisher's Z transformation (if data is in Pearson's r format)
        # For example, let's assume it's a correlation matrix:
        if z_scores.ndim == 2:
            # Fisher's Z transformation for correlation matrix (if necessary)
            # Z = 0.5 * ln((1 + r) / (1 - r)) where r is the correlation coefficient
            z_scores = 0.5 * np.log((1 + z_scores) / (1 - z_scores))
        
        # Flatten the Z-scores if necessary and append to the list
        z_scores_list.append(z_scores.flatten())
    
    except KeyError as e:
        print(f"KeyError: {e} in file {file}. Skipping this file.")
        continue

# Convert the list into a numpy array or a pandas DataFrame
z_scores_array = np.array(z_scores_list)

# Optionally, create a DataFrame to label rows/columns for easier identification
df = pd.DataFrame(z_scores_array)

# Save the data in a format COMBAT can use (e.g., CSV)
output_file = '/path/to/save/combined_z_scores.csv'
df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")
