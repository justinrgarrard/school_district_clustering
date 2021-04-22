"""
This program runs various scripts to convert the processed dataset into a set of features (indicators),
to be used in modeling.

- jrgarrar
"""

import os
import json
import pathlib
import numpy as np
import pandas as pd


PARENT_DIR = pathlib.Path(__file__).parent.absolute()
FEATURE_SELECTION_JSON = os.path.join(PARENT_DIR, 'feature_selection.json')
YEAR_RANGE = [2009, 2016]


# Useful functions
def null_counter(df):
    record_nulls = []
    for col in df.columns:
        nulls = df[col].isnull().sum()
        percent_null = round((nulls / df.shape[0]) * 100, 2)
        record_nulls.append([col, nulls, percent_null])
    output = pd.DataFrame(record_nulls, columns=['Attribute', 'Null Count', '% Null'])
    return output


def get_year_range(df):
    year_range = list(df['year'].unique())
    year_range.sort()
    return year_range


def subset_by_states_only(df):
    df = df[df['fips'] <= 56]
    return df


def remove_flag_features(df):
    for col in df.columns:
        if col not in ['leaid', 'year', 'lea_name']:
            df[col] = df[col].apply(lambda x: np.nan if x < 0 else x)
    return df


def filter_out_factor(df, column_name):
    ## Drop records with null values in column
    df = df[df[column_name].notnull()]

    ## Drop empty records
    df = df[df[column_name] != 0]
    return df


def filter_all_factors(df):
    for col in df.columns:
        df = filter_out_factor(df, column_name=col)
    return df


def convert_to_features(logger, filepath, input_filename):
    # Read in the processed dataset
    target_file = os.path.join(filepath, input_filename)
    logger.info(f'Reading processed data from {target_file}...')
    processed_df = pd.read_csv(target_file)

    # Read in the indicators, and restrict dataset to only contain such indicators
    logger.info(f"Reading column selections from {FEATURE_SELECTION_JSON}...")
    with open(FEATURE_SELECTION_JSON) as f:
        select_data = json.load(f)
    processed_df = processed_df[select_data['feature_list']]

    logger.info(f"Beginning filtering process...")
    # Restrict to the applicable year range
    processed_df = processed_df[(processed_df['year'] >= 2009) & (processed_df['year'] <= 2016)]

    # Restrict to states only (no territories)
    processed_df = subset_by_states_only(processed_df)

    # Remove "flag" features, which are really nulls with justifications
    processed_df = remove_flag_features(processed_df)

    # Remove null values for each feature
    processed_df = filter_all_factors(processed_df)

    # Feature generation
    output = processed_df.copy()
    # output['leaid'] = processed_df['leaid']
    # output['year'] = processed_df['year']
    # output['lea_name'] = processed_df['lea_name']
    # output['fips'] = processed_df['fips']
    # output['enrollment'] = processed_df['enrollment_x']
    output['students_per_school'] = processed_df['enrollment_x'] / processed_df['number_of_schools']
    output['students_per_teacher'] = processed_df['enrollment_x'] / processed_df['teachers_total_fte']
    output['spending_per_student'] = processed_df['exp_total'] / processed_df['enrollment_x']
    output['academic_performance'] = (processed_df['read_test_pct_prof_midpt'] + processed_df['math_test_pct_prof_midpt']) / 2
    output['special_ed_students_percent'] = processed_df['enrollment_x'] / processed_df['spec_ed_students']

    # Output to file
    output_filename = input_filename.replace('.csv', '_features.csv')
    logger.info(f"Outputting to {output_filename}...")
    output.to_csv(os.path.join(filepath, output_filename), index=False)


if __name__ == '__main__':
    pass

