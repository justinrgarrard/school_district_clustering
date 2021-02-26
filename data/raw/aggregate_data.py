# Pat O'Brien
# Reading in Data for EdTech Project - CSE 6242
# All data taken from https://educationdata.urban.org/documentation/school-districts.html

# This program aggregates data for assessment results and graduation rates into one large file,
import pandas as pd
import glob
import xlrd
import pandasql as ps


def joinfiles(path):
    all_files = glob.glob(path + "/*.csv")
    # print(all_files)
    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    return frame


#assessment = joinfiles(
    #r"C:\Users\Patrick O'Brien\Desktop\School\Grad School\Spring 2021\DVA\project\data\assessment_data")

grad_rates = joinfiles(
    r"C:\Users\Patrick O'Brien\Desktop\School\Grad School\Spring 2021\DVA\project\data\grad_rates_data")
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

grad_rates_clean = grad_rates.query('race == 99 and lep == 99 and homeless == 99 and disability == 99 and '
                                    'econ_disadvantaged == 99 and foster_care == 99')

grad_rates_clean.to_csv(path_or_buf="grad_rates_clean.csv", index=False)
#assessment_code = pd.read_excel(
    #r"C:\Users\Patrick O'Brien\Desktop\School\Grad School\Spring 2021\DVA\project\data\codebook_districts_edfacts_assessments.xls",
    #sheet_name='values')

