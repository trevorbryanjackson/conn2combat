import os
import sys
import glob
import argparse
import subprocess
import h5py
import pandas as pd

def options():
    parser = argparse.ArgumentParser(
    description="""
                    This script is designed to parse .mat files generated from CONN first-level ROI-to_ROI analyses (https://web.conn-toolbox.org/resources) 
                    and output them in a format that can be used by COMBAT (https://github.com/Jfortin1/ComBatHarmonization). 

                    Inputs are the CONN analysis directory, and an output directory where the outputs should be stored, and (optional) a list of ROIs of interest.

                    Outputs consist of one CSV file per subject containing the correlation data for each ROI, and a combined CSV file containing all subjects' data.

                    Usage:
                        python extract_for_combat.py -d /path/to/conn_directory -o /path/to/output_dir -r ROI1 ROI2 ROI3
                    """)
    parser.add_argument("-d", "--conn_directory", type=str, help="Path to the CONN analysis directory. Required.", required=True)
    parser.add_argument("-o", "--output_directory", type=str, help="Path to the directory where the outputs will be saved. Default is the current directory.", default=".")
    parser.add_argument("-r", "--rois", type=str, nargs='*',  help="List of regions of interest (ROIs) to export. Default is all ROIs.")
    parser.add_argument("-l", "--limit", action="store_true",  help="Limits output to only ROI-to-ROI data (as opposed to ROIs-to-all including atlas and networks).")
    options = parser.parse_args()
    if options.conn_directory:
        print(f"Using connection directory: {options.conn_directory}")
    if options.output_directory:
        print(f"Saving output to: {options.output_directory}")
    if options.rois:
        print(f"Processing the following ROIs: {', '.join(options.rois)}")
    return options

######## CODE ########
def conn2combat(data_dir, output_directory, rois, limit):
    pattern = 'resultsROI_Subject*_Condition001.mat'
    files = os.path.join(data_dir, pattern)
    all_data = {}
    for file in glob.glob(files):
        with h5py.File(file, 'r') as mat_data:
            names_dataset = mat_data['names']
            names2_dataset = mat_data['names2']
            names = []
            for ref in names_dataset[:, 0]:
                ascii_array = mat_data[ref][()]
                name = ''.join(chr(code[0]) for code in ascii_array)
                names.append(name)
            names2 = []
            for ref in names2_dataset[:, 0]:
                ascii_array = mat_data[ref][()]
                name2 = ''.join(chr(code[0]) for code in ascii_array)
                names2.append(name2)
            Z_dataset = mat_data['Z']
            Z = Z_dataset[:]
            if Z.shape != (len(names2), len(names)):
                raise ValueError(
                    f"Mismatch in matrix dimensions: Z.shape = {Z.shape}, len(names2) = {len(names2)}, len(names) = {len(names)}"
                )
            data = []
            for i, row_name in enumerate(names2):
                if limit or rois:
                    if row_name not in rois:
                        continue
                for j, col_name in enumerate(names):
                    if limit:
                        if col_name not in rois:
                            continue
                    if row_name == col_name:
                        continue
                    data.append((f"{row_name}_{col_name}", Z[i, j]))
            df = pd.DataFrame(data, columns=["Name", "Score"])
            output_file = os.path.join(output_directory, f"{os.path.basename(file).split('.')[0]}_correlation_data_filtered.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved filtered data: {output_file}")
            subject_name = os.path.basename(file).split('_')[1] 
            all_data[subject_name] = df.set_index("Name")["Score"]

    combined_df = pd.concat(all_data, axis=1)
    combined_df.columns = list(all_data.keys())
    subject_row = pd.DataFrame([combined_df.columns], columns=combined_df.columns)
    combined_df_with_header = pd.concat([subject_row, combined_df], ignore_index=True)
    combined_output_file = os.path.join(output_directory, "combat_correlation_data.csv")
    combined_df_with_header.to_csv(combined_output_file, header=False, index=False)
    print(f"Saved combined data: {combined_output_file}")

def main():
    options = options()
    if options.conn_directory:
        print(f"Using connection directory: {options.conn_directory}")
    if options.output_directory:
        print(f"Saving output to: {options.output_directory}")
    if options.rois:
        print(f"Processing the following ROIs: {', '.join(options.rois)}")
    if options.limit:
        print(f"Limiting output to ROI-to-ROI data.")
    conn2combat(options.conn_directory, options.output_directory, options.rois, options.limit)


if __name__ == "__main__":
    main()