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
    ## Logging
    # logger.info(processed_df.shape)

    # Build the "coords" table
    ## Drop records with an agency type other than 1 or 2
    coords_df = processed_df[(processed_df['agency_type'] == 1) | (processed_df['agency_type'] == 2)]
    coords_df = coords_df[(coords_df['state_location'] != "AS") & (coords_df['state_location'] != "GU") &
                          (coords_df['state_location'] != "MP") & (coords_df['state_location'] != "VI") &
                          (coords_df['state_location'] != "PR")]
    ## Only keep records from the latest year for each leaid
    max_yr_series = coords_df.groupby(['leaid'])['year'].max()
    coords_df['max_yr'] = coords_df['leaid'].apply(lambda x: max_yr_series[x])
    coords_df = coords_df[coords_df['year'] == coords_df['max_yr']]
    ## Logging
    # logger.info(coords_df.shape)
    # logger.info(coords_df.columns)

    # Build the "test" table
    ## Merge "coords" with the "processed" dataset to get the full scope of years
    test_df = pd.merge(processed_df, coords_df, how='left', on=['leaid'])
    ## Logging
    # logger.info(test_df.shape)
    # logger.info(list(test_df.columns))

    ## Do some data shuffling to get the columns back to their proper shape
    test_df.rename(columns={'latitude_x': 'latitude', 'longitude_x': 'longitude', 'lea_name_x': 'lea_name',
                            'city_location_x': 'city_location', 'state_location_x': 'state_location',
                            'latitude_y': 'lat', 'longitude_y': 'long', 'lea_name_y': 'name',
                            'city_location_y': 'city', 'state_location_y': 'state'}, inplace=True)
    dispose_cols = [x for x in list(test_df.columns) if '_y' in x]
    test_df.drop(dispose_cols, axis=1, inplace=True)
    fix_cols = {x: x.strip('_x') for x in list(test_df.columns) if '_x' in x}
    test_df.rename(columns=fix_cols, inplace=True)
    test_df = test_df[test_df['lat'].notna()]
    # logger.info(test_df.shape)
    # logger.info(test_df.columns)

    ## Add in the cluster labels
    out_df = pd.merge(test_df, labeled_df[['leaid', 'year', 'label']], how='left')
    # logger.info(out_df.shape)
    # logger.info(out_df.columns)

    # Output to file
    output_path = os.path.join(output_filepath, 'csv_to_json3.csv')
    out_df.to_csv(output_path)


if __name__ == '__main__':
    pass
