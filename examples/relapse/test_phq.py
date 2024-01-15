from utilities import PHQ9Analysis
import numpy as np

phq_analysis_obj = PHQ9Analysis()
# cumulative_probs, params = phq_analysis_obj.cumulative_probabilities(type="maintenance")
#
# # desired time
# time = 1
#
#
# def logistic_function(x, L, k, x0):
#     return L / (1 + np.exp(-k * (x - x0)))
#
#
# # calculate probability
# probability = logistic_function(time, *params)
#
# print(probability)
intervals = phq_analysis_obj.return_probability_intervals(group_type="maintenance")
updated_intervals = phq_analysis_obj.interpolate_probability_intervals(intervals)
print(np.sum(updated_intervals))