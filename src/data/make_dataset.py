# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import aggregate_dataset
import prune_dataset


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('interim_filepath', type=click.Path())
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, interim_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    # logger.info('Making final data set from raw data...')

    # Run the file aggregate script
    logger.info('Combining raw annual files into aggregates...')
    scan = os.scandir(input_filepath)
    target_files = [file.name for file in scan if '.zip' in file.name]
    for file in target_files:
        aggregate_dataset.joinfiles(logger, input_filepath, file, interim_filepath)

    # Run the column drop pruning script
    logger.info('Pruning unneeded columns')
    scan = os.scandir(interim_filepath)
    target_files = [file.name for file in scan if os.path.isfile(file) and '_clean' in file.name]
    for file in target_files:
        prune_dataset.prune_data(logger, interim_filepath, file)

    # TODO: Aggregate trimmed files into single entity


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
