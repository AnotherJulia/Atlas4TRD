import math

# Total number of employees at Erasmus MC
total_employees = 16180

# Estimating the number of employees in mental health services
# using a range of 5% to 10% of the total workforce
lower_bound_percentage = 0.05
upper_bound_percentage = 0.10

# Calculating the estimated number of employees in mental health services
lower_bound_estimate = total_employees * lower_bound_percentage
upper_bound_estimate = total_employees * upper_bound_percentage

# Estimating the number of employees in the depression care system
# using a range of 10% to 20% of the psychiatric department workforce
lower_bound_percentage_depression = 0.10
upper_bound_percentage_depression = 0.20

# Calculating the estimated number of employees in the depression care system
# using the lower and upper bounds of the estimated psychiatric department workforce
lower_bound_estimate_depression = lower_bound_estimate * lower_bound_percentage_depression
upper_bound_estimate_depression = upper_bound_estimate * upper_bound_percentage_depression

# Estimating the number of employees qualified to treat patients
# using a range of 60% to 70% of the estimated depression care workforce
lower_bound_percentage_treatment = 0.60
upper_bound_percentage_treatment = 0.70

# Calculating the estimated number of employees qualified to treat patients
# in the depression care system
lower_bound_estimate_treatment = lower_bound_estimate_depression * lower_bound_percentage_treatment
upper_bound_estimate_treatment = upper_bound_estimate_depression * upper_bound_percentage_treatment

# Estimating the proportion of MDD among depression patients
lower_bound_mdd_proportion = 0.20
upper_bound_mdd_proportion = 0.30

# Percentage of MDD patients with TRD
trd_proportion_in_mdd = 0.30

# Calculating the proportion of TRD patients among all depression patients
lower_bound_trd_proportion = lower_bound_mdd_proportion * trd_proportion_in_mdd
upper_bound_trd_proportion = upper_bound_mdd_proportion * trd_proportion_in_mdd

# Average time per patient in hours
average_time_per_patient = 4

# Standard working hours per week for each employee
working_hours_per_week = 40

# Proportion of time spent on direct patient care
time_for_patient_care = 0.50

# Calculating the total available hours for patient care per week for the lower and upper bounds of estimated employees
total_care_hours_lower_bound = lower_bound_estimate_treatment * working_hours_per_week * time_for_patient_care
total_care_hours_upper_bound = upper_bound_estimate_treatment * working_hours_per_week * time_for_patient_care

# Estimating the weekly processing capacity for TRD patients
weekly_capacity_lower_bound = total_care_hours_lower_bound / average_time_per_patient
weekly_capacity_upper_bound = total_care_hours_upper_bound / average_time_per_patient

print(f"Weekly capacity for TRD patients: {weekly_capacity_lower_bound} - {weekly_capacity_upper_bound}")

# Calculating the mean of the weekly capacity
mean_weekly_capacity = (weekly_capacity_lower_bound + weekly_capacity_upper_bound) / 2

# Calculating the standard deviation of the weekly capacity
standard_deviation = (weekly_capacity_upper_bound - weekly_capacity_lower_bound) / math.sqrt(12)

print(f"Mean weekly capacity: {mean_weekly_capacity} | Standard deviation: {standard_deviation}")
