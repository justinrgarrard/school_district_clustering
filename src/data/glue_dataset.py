"""
A script for assembling all the trimmed datasets into a single file.

- jrgarrard
"""

import os
import pathlib
import pandas as pd

OUTPUT_FILENAME = 'edtech_dataset.csv'


def combine_files(logger, interim_path, output_path):
    # Identify trimmed files
    logger.info('Gathering files...')
    scan = os.scandir(interim_path)
    target_files = [file.name for file in scan if os.path.isfile(file) and '_trimmed' in file.name]

    # Combine files
    logger.info('Combining files...')
    output_df = pd.DataFrame()
    for file in target_files:
        # Open file
        logger.info(f'... {file}...')
        filename = os.path.join(interim_path, file)
        input_df = pd.read_csv(filename)

        # Generate primary key
        input_df['primary_key'] = input_df['year'] + '_' + input_df['leaid']

        # Join to output
        output_df = output_df.merge(input_df, on='primary_key')

    # Output to file
    logger.info(f'Outputting file {OUTPUT_FILENAME}...')
    output_df.to_csv(os.path.join(output_path, interim_path))


if __name__ == '__main__':
    pass
