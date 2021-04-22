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
    coords_df = processed_df[(processed_df['agency_type'] == 1) | (processed_df['agency_type'] == 2)]
    max_yrs_indices = coords_df.groupby(['leaid'])['year'].idxmax()
    coords_df = coords_df.loc[max_yrs_indices]
    # print(list(coords_df.columns))

    # Build the "test" table
    test_df = pd.merge(processed_df, coords_df)
    # print(list(test_df.columns))
    # test_df = processed_df.join(coords_df, how='inner', on='leaid')

    # Build the "out" table
    out_df = pd.merge(labeled_df, test_df)
    # out_df = labeled_df.join(test_df, on=['leaid', 'year'])

    # Output to file
    output_path = os.path.join(output_filepath, 'csv_to_json3.csv')
    out_df.to_csv(output_path)


if __name__ == '__main__':
    pass
