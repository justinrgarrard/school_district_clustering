Create table coords as
SELECT leaid, MAX(year), latitude, longitude, lea_name, city_location, state_location 
FROM processed
WHERE ((agency_type = 1) or (agency_type = 2)) and (latitude is not null) and (state_location not in ("AS","GU","MP","VI", "PR"))
GROUP BY leaid


create table test as
SELECT coords.leaid, year, coords.latitude as lat, coords.longitude as long, coords.lea_name as name, coords.city_location as city, coords.state_location as state, processed.lea_name, state_leaid, 
                 street_location, processed.city_location, processed.state_location,
                 zip_location, zip4_location, fips, agency_type,
                 number_of_schools, county_code, county_name, 
                 processed.latitude, processed.longitude, cbsa, cbsa_type, csa, teachers_total_fte, staff_total_fte,
                    spec_ed_students, english_language_learners, 
                    enrollment_x, enrollment_y, cmsa, district_id,
                    est_population_total, est_population_5_17, 
                    est_population_5_17_poverty, est_population_5_17_poverty_pct,
                    est_population_5_17_pct, enrollment_fall_responsible, 
                    enrollment_fall_school, read_test_num_valid, 
                    read_test_pct_prof_midpt, math_test_num_valid,
                    math_test_pct_prof_midpt, grad_rate_midpt, rev_total, rev_fed_total, rev_state_total,
                rev_local_total, exp_total, exp_current_instruction_total,
                exp_current_supp_serve_total, exp_current_other, exp_nonelsec,
                salaries_total, benefits_employee_total, debt_longterm_outstand_beg_FY
FROM processed
INNER JOIN coords on coords.leaid = processed.leaid;


create table out as
SELECT test.leaid, test.year, lat, long, name, city, state, lea_name, state_leaid, 
                 street_location, city_location, state_location,
                 zip_location, zip4_location, fips, agency_type,
                 number_of_schools, county_code, county_name, 
                 latitude, longitude, cbsa, cbsa_type, csa, teachers_total_fte, staff_total_fte,
                    spec_ed_students, english_language_learners, 
                    enrollment_x, enrollment_y, cmsa, district_id,
                    est_population_total, est_population_5_17, 
                    est_population_5_17_poverty, est_population_5_17_poverty_pct,
                    est_population_5_17_pct, enrollment_fall_responsible, 
                    enrollment_fall_school, read_test_num_valid, 
                    read_test_pct_prof_midpt, math_test_num_valid,
                    math_test_pct_prof_midpt, grad_rate_midpt, rev_total, rev_fed_total, rev_state_total,
                rev_local_total, exp_total, exp_current_instruction_total,
                exp_current_supp_serve_total, exp_current_other, exp_nonelsec,
                salaries_total, benefits_employee_total, debt_longterm_outstand_beg_FY, processed_features.label
FROM test
LEFT JOIN processed_features on test.leaid = processed_features.leaid and test.year = processed_features.year;