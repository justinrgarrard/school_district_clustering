"""
This program produces median values of each cluster, for use by the visualization.

- Pat O'Brien & jrgarrard
"""


import os
import pandas as pd


# df = pd.read_csv("data/processed_features_labeled.csv")
# df = df['label'] = df['label'].astype(int)
# df = df['year'] = df['year'].astype(int)


def generate_median_file(logger, input_filepath, input_filename, output_filepath):
    # Read in data
    input_path = os.path.join(input_filepath, input_filename)
    df = pd.read_csv(input_path)

    # print(df.dtypes)
    # print(df.columns)
    df2 = pd.DataFrame(columns = df.columns.values)
    years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
    for i in range(16):
        for j in years:
            concatdf = df[df['label'] == (i + 1)]
            concatdf = concatdf[concatdf['year'] == j]

            meds = pd.DataFrame(concatdf.median())
            meds2 = meds.transpose()
            if meds2['label'].iloc[0] == 1:
                meds2["cluster_name"] = 'Single School Higher Performance Districts'
                meds2["cluster_category"] = 'Single'
                meds2["cluster_desc"] = 'School districts with a single school, generally with less than 50 students.* Academic performance trends high (64.5 - 82.0 out of 100).**'
            elif meds2['label'].iloc[0] == 2:
                meds2["cluster_name"] = 'Single High Enrollment School Districts'
                meds2["cluster_category"] = 'Single'
                meds2["cluster_desc"] = 'School districts with a single school, generally with 1,000+ students.* Academic performance varies widely (45.5 - 79.5 out of 100).**'
            elif meds2['label'].iloc[0] == 3:
                meds2["cluster_name"] = 'Single School Lower Performance Districts'
                meds2["cluster_category"] = 'Single'
                meds2["cluster_desc"] = 'School districts with a single school, generally with less than 50 students.* Academic performance trends low (24.5 - 47.5 out of 100).**'
            elif meds2['label'].iloc[0] == 4:
                meds2["cluster_name"] = 'Single Very High Enrollment School Districts'
                meds2["cluster_category"] = 'Single'
                meds2["cluster_desc"] = 'School districts with a single school, serving 3,000+ students under a single school name. Academic performance trends low (31.6 - 59.3 out of 100).**'
            elif meds2['label'].iloc[0] == 5:
                meds2["cluster_name"] = 'Small Higher Performance Districts'
                meds2["cluster_category"] = 'Small'
                meds2["cluster_desc"] = 'Small school districts (2-3 schools), generally with less than 700 students.* Academic performance trends high (69.5 - 84.0 out of 100).**'
            elif meds2['label'].iloc[0] == 6:
                meds2["cluster_name"] = 'Small Very High Enrollment Districts'
                meds2["cluster_category"] = 'Small'
                meds2["cluster_desc"] = 'Small school districts (2-3 schools), generally with 2,000+ students.* Academic performance varies widely (39.0 - 79.3 out of 100).**'
            elif meds2['label'].iloc[0] == 7:
                meds2["cluster_name"] = 'Small Lower Performance Districts'
                meds2["cluster_category"] = 'Small'
                meds2["cluster_desc"] = 'Small school districts (2-3 schools), generally with less than 700 students.* Academic performance trends low (33.0 - 50.0 out of 100).**'
            elif meds2['label'].iloc[0] == 8:
                meds2["cluster_name"] = 'Small High Enrollment Districts'
                meds2["cluster_category"] = 'Small'
                meds2["cluster_desc"] = 'Small school districts (2-3 schools), generally with 1,000+ students.* Academic performance varies widely (54.5 - 78.5 with numerous outliers out of 100).**'
            elif meds2['label'].iloc[0] == 9:
                meds2["cluster_name"] = 'Medium Higher Performance Districts'
                meds2["cluster_category"] = 'Medium'
                meds2["cluster_desc"] = 'Mid-sized school districts (4-10 schools), generally with less than 2,500 students.* Academic performance trends high (69.5 - 84.5 out of 100).**'
            elif meds2['label'].iloc[0] == 10:
                meds2["cluster_name"] = 'Medium Lower Performance Districts'
                meds2["cluster_category"] = 'Medium'
                meds2["cluster_desc"] = 'Mid-sized school districts (4-10 schools), generally with less than 2,500 students.* Academic performance trends low (33.5 - 50.5 out of 100).**'
            elif meds2['label'].iloc[0] == 11:
                meds2["cluster_name"] = 'Medium Very High Enrollment Districts'
                meds2["cluster_category"] = 'Medium'
                meds2["cluster_desc"] = 'Mid-sized school districts (4-10 schools), generally with 5,000+ students.* Academic performance varies widely (47.0 - 77.5 out of 100).**'
            elif meds2['label'].iloc[0] == 12:
                meds2["cluster_name"] = 'Medium High Enrollment Districts'
                meds2["cluster_category"] = 'Medium'
                meds2["cluster_desc"] = 'Mid-sized school districts (4-10 schools), generally with 3,000+ students.* Academic performance varies widely (60.0 - 81.5 with numerous outliers out of 100).**'
            elif meds2['label'].iloc[0] == 13:
                meds2["cluster_name"] = 'Large Lower Performance Districts'
                meds2["cluster_category"] = 'Large'
                meds2["cluster_desc"] = 'Large school districts (11+ schools), generally with less than 20,000 students.* Academic performance trends low (36.0 - 52.0 out of 100).**'
            elif meds2['label'].iloc[0] == 14:
                meds2["cluster_name"] = 'Large Higher Performance Districts'
                meds2["cluster_category"] = 'Large'
                meds2["cluster_desc"] = 'Large school districts (11+ schools), generally with less than 20,000 students.* Academic performance trends high (47.5 - 76.5 out of 100).**'
            elif meds2['label'].iloc[0] == 15:
                meds2["cluster_name"] = 'Large High Enrollment Districts'
                meds2["cluster_category"] = 'Large'
                meds2["cluster_desc"] = 'Large school districts (11+ schools), generally with 80,000+ students.* Academic performance varies widely (47.5 - 76.5 out of 100).**'
            elif meds2['label'].iloc[0] == 16:
                meds2["cluster_name"] = 'Large Very High Enrollment School Districts'
                meds2["cluster_category"] = 'Large'
                meds2["cluster_desc"] = 'Large school districts (11+ schools), generally with 350,000+ students.* Academic performance trends low (39.75 - 57.5 out of 100).**'
            # print(df2)
            df2 = df2.append(meds2, ignore_index=True)

    output_path = os.path.join(output_filepath, 'median_clusters.csv')
    df2.to_csv(output_path)
