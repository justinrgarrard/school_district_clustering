"""
This program runs regressions on each cluster in the dataset, outputting results
to the data/interim directory.

- jrgarrar
"""

import os
import pathlib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import matplotlib.pyplot as plt

PARENT_DIR = pathlib.Path(__file__).parent.absolute()


def filter_out_factor(df, column_name):
    ## Identify records with null values in column
    bad_records = df[df[column_name].isnull()]
    # bad_records.to_csv(f'missing_{column_name}.csv')

    ## Drop records with null values in column
    df = df[df[column_name].notnull()]
    return df


def regress_on_df(df, metric, ignore_metrics=['read_test_pct_prof_midpt', 'math_test_pct_prof_midpt', 'label', 'number_of_schools']):
    features = df.drop(ignore_metrics, axis=1)
    features = features.drop([metric], axis=1)
    labels = df[metric]

    # Visualize the resulting model
    return sm.OLS(labels,features).fit().summary(yname=metric, xname=list(features.columns))


def anonymize_df(df):
    id_cols = ['leaid', 'year', 'lea_name', 'fips']
    id_df = df[id_cols]
    data_df = df.drop(id_cols, axis=1)
    return id_df, data_df


def run_regressions(logger, filepath, input_filename, output_filepath):
    # Read in the feature dataset
    target_file = os.path.join(filepath, input_filename)
    logger.info(f'Reading processed data from {target_file}...')
    labeled_df = pd.read_csv(target_file)

    # Filter out unlabeled data
    labeled_df = filter_out_factor(labeled_df, 'label')
    
    # Remove id data
    _, labeled_df = anonymize_df(labeled_df)

    # For each cluster, generate a regression on test scores
    # and output to file
    n_clusters = len(np.unique(labeled_df['label']))
    subset_data = []
    for i in range(1, n_clusters+1):
        subset_df = labeled_df[labeled_df['label'] == i]
        subset_data.append(subset_df)
        regression_output = regress_on_df(subset_df, 'academic_performance')
        filename = f'regression_{i}.csv'
        with open(os.path.join(output_filepath, filename), 'w+') as f:
            f.write(subset_df.describe().to_csv())
            f.write(regression_output.as_csv())

    # Generate a box-plot for each metric
    for col in labeled_df.columns:
        plot_data = [subset_df[col] for subset_df in subset_data]

        plt.close()
        plt.style.use('ggplot')
        plt.figure(figsize=(8, 8))
        plt.boxplot(plot_data)
        plt.title(f'{col} Across Categories')
        plt.savefig(os.path.join(output_filepath, f'{col}_boxplot.png'))


if __name__ == '__main__':
    pass

