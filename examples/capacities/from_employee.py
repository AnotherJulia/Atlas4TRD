num_employees = 24
contact_ratio = 0.5
weekly_hours = 40

total_contact_hours = weekly_hours * contact_ratio * num_employees
print(total_contact_hours)

hours_a_patient = 2

# Determine the Psychology department capacity each week
capacity = total_contact_hours / hours_a_patient
print(capacity)


