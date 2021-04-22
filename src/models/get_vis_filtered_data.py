"""
This program produces a copy of the final dataset filtered for use by the visual.
The code used is a direct interpretation of the SQL files originally used (see rawSQL.sql
in references/).

- Pat O'Brien & jrgarrard
"""


import os
import numpy as np
import pandas as pd


def generate_vis_data_file(logger, input_filepath, processed_filename, labeled_filename, output_filepath):
    # Read in data
    input_path = os.path.join(input_filepath, processed_filename)
    processed_df = pd.read_csv(input_path)

    input_path = os.path.join(input_filepath, labeled_filename)
    labeled_df = pd.read_csv(input_path)

    # Build the "coords" table
    ## Drop records with an agency type other than 1 or 2
    coords_df = processed_df[(processed_df['agency_type'] == 1) | (processed_df['agency_type'] == 2)]
    ## Drop records without a latitude value
    coords_df = coords_df[coords_df['latitude'].notna()]
    ## Only keep records from the latest year
    max_yr = coords_df['year'].max()
    coords_df = coords_df[coords_df['year'] == max_yr]
    logger.info(coords_df.shape)
    logger.info(coords_df.columns)

    # Build the "test" table
    # test_df = pd.merge(processed_df, coords_df)
    # logger.info(test_df.shape)
    # logger.info(test_df.columns)

    # Build the "out" table
    out_df = pd.merge(labeled_df, coords_df)
    logger.info(out_df.shape)
    logger.info(out_df.columns)

    # Output to file
    output_path = os.path.join(output_filepath, 'csv_to_json3.csv')
    coords_df.to_csv(output_path)


if __name__ == '__main__':
    pass
