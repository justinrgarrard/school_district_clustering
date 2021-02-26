# -*- coding: utf-8 -*-
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

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
    logger.info('making final data set from raw data')

    # TODO: Incorporate raw to interim processing here

    # Run the column drop pruning script
    logger.info('pruning unneeded columns')
    scan = os.scandir(interim_filepath)
    target_files = [file.name for file in scan if os.path.isfile(file) and '_clean' in file.name]
    for file in target_files:
        prune_dataset.prune_data(interim_filepath, file)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
