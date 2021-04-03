# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd

import convert_to_model
import run_regressions

PROCESSED_FILENAME = 'processed_features.csv'
LABELED_FILENAME = 'processed_features_labeled.csv'

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

    # Convert features into CSV files representing clusters
    logger.info('Converting features into model...')
    convert_to_model.convert_to_model(logger, output_filepath, PROCESSED_FILENAME)

    # Run regressions on each cluster
    run_regressions.run_regressions(logger, output_filepath, LABELED_FILENAME, interim_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
