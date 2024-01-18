import math

total_employees = 20

# Estimating the number of employees in the depression care system
# using a range of 10% to 20% of the psychiatric department workforce
lower_bound_percentage_depression = 0.20
upper_bound_percentage_depression = 0.30

# Calculating the estimated number of employees in the depression care system
# using the lower and upper bounds of the estimated psychiatric department workforce
lower_bound_estimate_depression = total_employees * lower_bound_percentage_depression
upper_bound_estimate_depression = total_employees * upper_bound_percentage_depression

# Estimating the number of employees qualified to treat patients
# using a range of 60% to 70% of the estimated depression care workforce

# Calculating the estimated number of employees qualified to treat patients
# in the depression care system
lower_bound_estimate_treatment = lower_bound_estimate_depression
upper_bound_estimate_treatment = upper_bound_estimate_depression

# Estimating the proportion of MDD among depression patients
lower_bound_mdd_proportion = 0.30
upper_bound_mdd_proportion = 0.40

# Calculating the proportion of TRD patients among all depression patients
lower_bound_trd_proportion = lower_bound_mdd_proportion
upper_bound_trd_proportion = upper_bound_mdd_proportion

# Average time per patient in hours
average_time_per_patient = 2

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
