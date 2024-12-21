# CONN First Level Extraction

This script is designed to parse .mat files generated from CONN first-level ROI-to_ROI analyses (https://web.conn-toolbox.org/resources) 
and output them in a format that can be used by COMBAT (https://github.com/Jfortin1/ComBatHarmonization). 

Inputs are the CONN analysis directory, and an output directory where the outputs should be stored, and (optional) a list of ROIs of interest.

Outputs consist of one CSV file per subject containing the correlation data for each ROI, and a combined CSV file containing all subjects' data.

## Options

- `-d`, `--conn_directory`: Path to the CONN analysis directory. Required.
- `-o`, `--output_directory`: Path to the directory where the outputs will be saved. Default is the current directory.
- `-r`, `--rois`: List of regions of interest (ROIs) to export. Default is all ROIs.
- `-l`, `--limit`: Limits output to only ROI-to-ROI data (as opposed to ROIs-to-all including atlas and networks).

## Example

```
python extract_for_combat.py -d /path/to/conn_directory -o /path/to/output_dir -r ROI1 ROI2 ROI3
```

## Requirements

- Python 3.x (tested with python 3.11.11)

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/trevorbryanjackson/CONN_First_Level_Extraction.git
    ```
2. Navigate to the project directory:
    ```
    cd CONN_First_Level_Extraction
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## License

This project is licensed under the MIT License.
