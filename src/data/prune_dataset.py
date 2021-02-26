"""
A script for pruning CSV data files by removing unnecessary columns.

- jrgarrard
"""

import os
import json
import pathlib
import pandas as pd

PARENT_DIR = pathlib.Path(__file__).parent.absolute()
COLUMN_SELECTION_JSON = os.path.join(PARENT_DIR, 'column_selection.json')


def prune_data(logger, filepath, filename):
    # Open the data file
    logger.info(f"Opening {filename}...")
    full_path_filename = os.path.join(filepath, filename)
    df = pd.read_csv(full_path_filename)

    # Read "columns to keep" from a data file
    logger.info(f"Reading column selections from {COLUMN_SELECTION_JSON}...")
    with open(COLUMN_SELECTION_JSON) as f:
        select_data = json.load(f)

    # Apply the filtering
    logger.info(f"Dropping unnecessary columns...")
    allowed_columns = select_data[filename]
    df = df[allowed_columns]

    # Output pruned data file to interim
    output_filename = filename.replace("_clean", "_trimmed")
    logger.info(f"Outputting pruned file {output_filename}...")
    output_path = os.path.join(filepath, output_filename)
    df.to_csv(output_path, index=False)


if __name__ == '__main__':
    pass
