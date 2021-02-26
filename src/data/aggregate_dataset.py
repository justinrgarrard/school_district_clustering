"""
This program aggregates data for assessment results and graduation rates into one large file

All data taken from https://educationdata.urban.org/documentation/school-districts.html

- Pat O'Brien & jrgarrard
"""

import os
import shutil
import pathlib
from zipfile import ZipFile
import pandas as pd
import glob
import xlrd
import pandasql as ps

PARENT_DIR = pathlib.Path(__file__).parent.absolute()


def joinfiles(logger, input_filepath, zip_filename, output_filepath):
    # Unzip the target data
    logger.info(f"Unzipping {zip_filename}...")
    target_zip_file = os.path.join(input_filepath, zip_filename)
    with ZipFile(target_zip_file) as f:
        f.extractall(input_filepath)
    extracted_dir = target_zip_file.replace(".zip", "")
    print(extracted_dir)

    # Combine the CSV's into a single dataframe
    logger.info("Aggregating csv's...")
    all_files = glob.glob(extracted_dir + "/*.csv")
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    frame = pd.concat(li, axis=0, ignore_index=True)

    # Output file
    output_filename = zip_filename.replace(".zip", "").replace(" ", "_") + '_clean.csv'
    logger.info(f"Outputting to {output_filename}...")
    frame.to_csv(os.path.join(output_filepath, output_filename), index=False)

    # Cleanup folder
    logger.info(f"Cleaning up...")
    shutil.rmtree(extracted_dir)


#assessment = joinfiles(
    #r"C:\Users\Patrick O'Brien\Desktop\School\Grad School\Spring 2021\DVA\project\data\assessment_data")

# grad_rates = joinfiles(
#     r"C:\Users\Patrick O'Brien\Desktop\School\Grad School\Spring 2021\DVA\project\data\grad_rates_data")
# print(grad_rates.head())
# print(grad_rates.describe())

#enrollment = joinfiles(r"C:\Users\Patrick O'Brien\Desktop\School\Grad School\Spring 2021\DVA\project\data\enrollment_data")
# assessment.to_csv(path_or_buf="assessment.csv", index=False)
# grad_rates.to_csv(path_or_buf="grad_rates.csv", index=False)
#enrollment.to_csv(path_or_buf="enrollment.csv", index=False)

#assessment_clean = assessment.query('grade_edfacts == 99 and race == 99 and sex == 99 and lep == 99 and homeless == '
                                    #'99 and migrant == 99 and disability == 99 and econ_disadvantaged == 99 and '
                                   # 'foster_care == 99 and military_connected == 99')
#assessment_clean.to_csv(path_or_buf="assessment_clean.csv", index=False)

# grad_rates_clean = grad_rates.query('race == 99 and lep == 99 and homeless == 99 and disability == 99 and '
#                                     'econ_disadvantaged == 99 and foster_care == 99')

# grad_rates_clean.to_csv(path_or_buf="grad_rates_clean.csv", index=False)
#assessment_code = pd.read_excel(
    #r"C:\Users\Patrick O'Brien\Desktop\School\Grad School\Spring 2021\DVA\project\data\codebook_districts_edfacts_assessments.xls",
    #sheet_name='values')

if __name__ == '__main__':
   pass
