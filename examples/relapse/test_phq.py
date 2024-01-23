from utilities import PHQ9Analysis

phq_analysis_obj = PHQ9Analysis()

intervals = phq_analysis_obj.return_probability_intervals(group_type="maintenance")
# updated_intervals = phq_analysis_obj.interpolate_probability_intervals(intervals)
phq_analysis_obj.plot_interpolated_probability_intervals(intervals)

intervals = phq_analysis_obj.return_probability_intervals(group_type="discontinued")
# updated_intervals = phq_analysis_obj.interpolate_probability_intervals(intervals)
phq_analysis_obj.plot_interpolated_probability_intervals(intervals)

phq_analysis_obj.plot_cumulative_probabilities("maintenace")

# print(np.sum(updated_intervals))

