"""
This program runs various scripts to convert the features dataset into a model.

- jrgarrar
"""

import os
import json
import pathlib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

PARENT_DIR = pathlib.Path(__file__).parent.absolute()
FEATURE_SELECTION_JSON = os.path.join(PARENT_DIR, 'feature_selection.json')


def anonymize_df(df):
    id_cols = ['leaid', 'year', 'lea_name', 'fips']
    id_df = df[id_cols]
    data_df = df.drop(id_cols, axis=1)
    return id_df, data_df


def segment_df(df):
    # Place data into four categories, to prevent clustering from emphasizing size
    single_df = df[df['number_of_schools'] == 1]
    
    small_df = df[(df['number_of_schools'] > 1) & 
                                   (df['number_of_schools'] <= 3)]
    
    medium_df = df[(df['number_of_schools'] > 3) & 
                                   (df['number_of_schools'] <= 10)]
    
    large_df = df[(df['number_of_schools'] > 10)]
    
    df_list = [single_df, small_df, medium_df, large_df]
    return df_list


def normalize_df(df):
    return StandardScaler().fit_transform(df)


# Build a cluster and return the labels
def build_cluster(df, k=6, random_seed=777):
    kmeans_learner = KMeans(n_clusters=k, random_state=random_seed)
    results = kmeans_learner.fit_predict(df)
    return results


# Regenerate the input dataset, but with labels
def reconstitute_data(df_list, results_list):
    # Map results to dataframe
    for i in range(0, len(df_list)):
        offset = (4 * i) + 1
        df_list[i]['label'] = results_list[i] + offset

    # Merge dataframes
    output = pd.concat(df_list)
    return output


def convert_to_model(logger, filepath, input_filename):
    # Read in the feature dataset
    target_file = os.path.join(filepath, input_filename)
    logger.info(f'Reading processed data from {target_file}...')
    feature_df = pd.read_csv(target_file)

    # Strip away identifying info, storing for later use
    id_df, feature_df = anonymize_df(feature_df)

    # Manually subset by size
    df_list = segment_df(feature_df)

    # Normalize within clusters to detect patterns besides size
    normed_df_list = []
    for df in df_list:
        normed_df_list.append(normalize_df(df))

    # Perform clustering
    results = []
    for df in normed_df_list:
        results.append(build_cluster(df, k=4))

    # Combine outputs into a representation of all clustered data
    labeled_feature_dataset = reconstitute_data(df_list, results)

    # Add the identifying information back in
    labeled_feature_dataset = labeled_feature_dataset.join(id_df)

    # Join the clustered data to the data that couldn't be clustered,
    # creating a label for "null" records which couldn't be categorized
    # target_file = os.path.join(filepath, input_filename)
    # logger.info(f'Reading processed data from {target_file}...')
    # processed_df = pd.read_csv(target_file)
    #
    # output = processed_df.join(labeled_feature_dataset, on=['leaid', 'year'], how='outer')


    # Output to file
    output_filename = input_filename.replace('.csv', '_labeled.csv')
    logger.info(f"Outputting to {output_filename}...")
    labeled_feature_dataset.to_csv(os.path.join(filepath, output_filename), index=False)


if __name__ == '__main__':
    pass

