import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import UnivariateSpline, interp1d
from scipy.optimize import curve_fit
# PHQ-9 scores data for maintenance and discontinued groups
phq_scores_maintenance = {
    "baseline": [3.9, 3.5],
    "6wk": [4.1, 3.8],
    "12wk": [4.1, 3.8],
    "26wk": [4.2, 3.7],
    "39wk": [3.8, 3.9],
    "52wk": [3.7, 3.7]
}
phq_scores_discontinued = {
    "baseline": [3.8, 3.6],
    "6wk": [4.4, 4.0],
    "12wk": [6.3, 5.1],
    "26wk": [5.0, 4.6],
    "39wk": [4.4, 4.2],
    "52wk": [4.0, 4.5]
}
# Threshold for considering relapse
relapse_threshold = 6
# Time points in months
time_points = {"baseline": 0, "6wk": 1.5, "12wk": 3, "26wk": 6.5, "39wk": 9.75, "52wk": 13}
sorted_times = sorted(time_points.keys(), key=lambda x: time_points[x])
sorted_time_values = [time_points[time] for time in sorted_times]

# Function to calculate proportions of relapse
def calculate_proportions(phq_scores):
    proportions = {}
    for time, (mean, sd) in phq_scores.items():
        proportion_relapse = norm.sf(relapse_threshold, loc=mean, scale=sd)
        proportions[time] = proportion_relapse
    return proportions

# Transforming cumulative probabilities to interval probabilities
def cumulative_to_interval(cumulative_probs):
    sorted_probs = [cumulative_probs[time] for time in sorted_times]
    interval_probs = [sorted_probs[0]]
    for i in range(1, len(sorted_probs)):
        interval_prob = sorted_probs[i] - sorted_probs[i - 1]
        interval_probs.append(max(interval_prob, 0))  # Ensure non-negative probabilities
    return interval_probs

# Calculate proportions and interval probabilities for both groups
proportions_maintenance = calculate_proportions(phq_scores_maintenance)
proportions_discontinued = calculate_proportions(phq_scores_discontinued)
interval_probs_maintenance = cumulative_to_interval(proportions_maintenance)
interval_probs_discontinued = cumulative_to_interval(proportions_discontinued)

# Function to calculate cumulative probability up to a certain time point
def calculate_cumulative_probability(time_point, interval_probs, time_values):
    cumulative_probability = 0
    for i, time in enumerate(time_values):
        if time_points[time] <= time_point:  # Use time_points[time] instead of just time
            cumulative_probability += interval_probs[i]
        else:
            break
    return cumulative_probability  # Also, you missed returning this value

# Customizing the appearance of the step function plot
plt.figure(figsize=(12, 8))
plt.step(sorted_time_values, interval_probs_maintenance, label='Maintenance Group', where='mid', linewidth=2)
plt.step(sorted_time_values, interval_probs_discontinued, label='Discontinued Group', where='mid', linestyle='--', linewidth=2)
# Customizing x-axis ticks and labels
plt.xticks(sorted_time_values, sorted_times)
plt.xlabel('Time (months)')
# Adding a y-axis label
plt.ylabel('Probability of Relapse in Interval')
# Customizing the title
plt.title('Interval Relapse Probability Over Time for Maintenance and Discontinued Groups', fontsize=14)
# Customizing legend
plt.legend(loc='upper right')
# Setting axis limits and grid
plt.xlim(0, 13)
plt.ylim(0, 0.4)
plt.grid(True, linestyle='--', alpha=0.6)
# Adding a horizontal line at y=0.5 for reference
plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
# Showing the plot
plt.show()

x_interp = np.linspace(0, 13, 1000)  # Create a smooth x-axis
f_maintenance = interp1d(sorted_time_values, interval_probs_maintenance, kind='cubic')
f_discontinued = interp1d(sorted_time_values, interval_probs_discontinued, kind="quadratic")
print(f_maintenance)
y_interp_maintenance = f_maintenance(x_interp)
y_interp_discontinued = f_discontinued(x_interp)
# Customizing the appearance of the continuous curves
plt.figure(figsize=(12, 8))
plt.plot(x_interp, y_interp_maintenance, label='Maintenance Group', linewidth=2)
plt.plot(x_interp, y_interp_discontinued, label='Discontinued Group', linestyle='--', linewidth=2)
# Customizing x-axis ticks and labels
plt.xlabel('Time (months)')
# Adding a y-axis label
plt.ylabel('Probability of Relapse in Interval')
# Customizing the title
plt.title('Interval Relapse Probability Over Time for Maintenance and Discontinued Groups', fontsize=14)
# Customizing legend
plt.legend(loc='upper right')
# Setting axis limits and grid
plt.xlim(0, 13)
plt.ylim(0, 0.4)
plt.grid(True, linestyle='--', alpha=0.6)
# Adding a horizontal line at y=0.5 for reference
plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
# Showing the plot
plt.show()

time_interval = np.arange(0, 52, 2)
def plot_cumulative_probabilties(time_interval, interval_probs, sorted_times, label="Cumulative Probability"):
    probs = [calculate_cumulative_probability(time, interval_probs, sorted_times) for time in time_interval]
    # Create a plot for cumulative probabilities
    plt.figure(figsize=(10, 6))
    plt.plot(time_interval, probs, label='Group')
    plt.title('Cumulative Probability of Relapse Over Time')
    plt.xlabel('Time (months)')
    plt.ylabel('Cumulative Probability')
    plt.legend()
    plt.grid(True)
    plt.show()
# plot_cumulative_probabilties(time_interval, interval_probs_maintenance, sorted_times, label="Maintenance")
# plot_cumulative_probabilties(time_interval, interval_probs_discontinued, sorted_times, label="Discontinued")
# Your data points
time_interval = np.array([0, 1.5, 3, 6.5, 9.75, 13])  # Time points
cumulative_probs_maintenance = [calculate_cumulative_probability(time, interval_probs_maintenance, sorted_times) for time in time_interval]
cumulative_probs_discontinued = [calculate_cumulative_probability(time, interval_probs_discontinued, sorted_times) for time in time_interval]
cumulative_probs_maintenance_np = np.array(cumulative_probs_maintenance)
cumulative_probs_discontinued_np = np.array(cumulative_probs_discontinued)
# Define the logistic function
def logistic_function(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))
# Fit the logistic function to your data with improved initial guesses
params_maintenance, _ = curve_fit(logistic_function, time_interval, cumulative_probs_maintenance, p0=(1, 1, 1))
params_discontinued, _ = curve_fit(logistic_function, time_interval, cumulative_probs_discontinued, p0=(1, 1, 1))
# Generate a smoother curve
smooth_time = np.linspace(0, 13, 1000)  # More points for smoother curve
smooth_probs_maintenance = logistic_function(smooth_time, *params_maintenance)
smooth_probs_discontinued = logistic_function(smooth_time, *params_discontinued)
# Create a plot for cumulative probabilities with the logistic curves
plt.figure(figsize=(10, 6))
plt.plot(time_interval, cumulative_probs_maintenance, 'o', label='Maintenance Group Data')
plt.plot(smooth_time, smooth_probs_maintenance, label='Maintenance Group Logistic Fit', linestyle='--')
plt.plot(time_interval, cumulative_probs_discontinued, 'o', label='Discontinued Group Data')
plt.plot(smooth_time, smooth_probs_discontinued, label='Discontinued Group Logistic Fit', linestyle='--')
plt.title('Cumulative Probability of Relapse Over Time (Logistic Fit)')
plt.xlabel('Time (months)')
plt.ylabel('Cumulative Probability')
plt.legend()
plt.grid(True)
plt.show()