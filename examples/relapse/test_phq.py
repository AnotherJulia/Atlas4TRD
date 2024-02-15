import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utilities import PHQ9Analysis

# phq_analysis_obj = PHQ9Analysis()

# intervals = phq_analysis_obj.return_probability_intervals(group_type="maintenance")
# # updated_intervals = phq_analysis_obj.interpolate_probability_intervals(intervals)
# phq_analysis_obj.plot_interpolated_probability_intervals(intervals)

# intervals = phq_analysis_obj.return_probability_intervals(group_type="discontinued")
# # updated_intervals = phq_analysis_obj.interpolate_probability_intervals(intervals)
# phq_analysis_obj.plot_interpolated_probability_intervals(intervals)

# phq_analysis_obj.plot_cumulative_probabilities("maintenace")

# print(np.sum(updated_interva wls))

phq_analysis = PHQ9Analysis()

# intervals = phq_analysis.return_probability_intervals(group_type="maintenance")
# phq_analysis.plot_interpolated_probability_intervals(intervals)

# intervals = phq_analysis.return_probability_intervals(group_type="discontinued")
# phq_analysis.plot_interpolated_probability_intervals(intervals, group="discontinued")

# Assuming 'return_probability_intervals' method exists and returns the intervals for the specified group
maintenance_intervals = phq_analysis.return_probability_intervals(group_type="maintenance")
discontinued_intervals = phq_analysis.return_probability_intervals(group_type="discontinued")

# Plotting both on the same graph
phq_analysis.plot_combined_interpolated_probabilities(maintenance_intervals, discontinued_intervals)

