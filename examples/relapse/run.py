import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Your provided data and functions
n = 487
phq_scores_maintenance = {
    "baseline": [3.9, 3.5],
    "6wk": [4.1, 3.8],
    "12wk": [4.1, 3.8],
    "26wk": [4.2, 3.7],
    "39wk": [3.8, 3.9],
    "52wk": [3.7, 3.7]
}
phq_threshold = 5


def simulate_and_plot_scores(week_scores, n_patients):
    scores = np.random.normal(loc=week_scores[0], scale=week_scores[1], size=n_patients)
    relapse_score = np.sum(scores >= phq_threshold)
    relapse_rate = relapse_score / n_patients
    return relapse_rate


num_simulations = 1000
relapse_rates_all = []

for _ in range(num_simulations):
    relapse_rates = [simulate_and_plot_scores(phq_scores_maintenance[week], n) for week in phq_scores_maintenance]
    relapse_rates_all.append(relapse_rates)

relapse_rates_all = np.array(relapse_rates_all)
relapse_means = relapse_rates_all.mean(axis=0)
relapse_cis = [stats.norm.interval(0.95, loc=mu, scale=stats.sem(relapse_rates_all[:, i]))
               for i, mu in enumerate(relapse_means)]

week_labels = ['baseline', '6wk', '12wk', '26wk', '39wk', '52wk']
week_numbers = [0, 6, 12, 26, 39, 52]
# week_numbers = np.arange(len(week_labels))

poly_degree = 2
# Adjusting the polynomial fit to align with the actual week numbers
poly_coeffs = np.polyfit(week_numbers, relapse_means, poly_degree)
line_poly = np.poly1d(poly_coeffs)

# Generating a range of week numbers for plotting the polynomial line
week_range = np.linspace(min(week_numbers), max(week_numbers), 100)

# Enhanced Plotting with adjusted polynomial fit
plt.figure(figsize=(12, 6))

# Polynomial fit line
plt.plot(week_range, line_poly(week_range), 'r-', label=f'Polynomial Fit (Degree {poly_degree})', linewidth=2)

# Error bars and data points
# plt.errorbar(x=week_numbers, y=relapse_means, yerr=[relapse_means - np.array(relapse_cis)[:, 0],
#             np.array(relapse_cis)[:, 1] - relapse_means], fmt='ok', label='Simulated Data Points',
#             ecolor='black', capsize=5, markersize=8, markeredgecolor='black', markeredgewidth=1)

# Labeling
plt.xticks(week_numbers, week_labels)
plt.xlabel('Weeks', fontsize=12)
plt.ylabel('Relapse Rate', fontsize=12)
plt.title('Relapse Rate over Time with Polynomial Fit', fontsize=14)
plt.legend(loc='best', fontsize=10)

# Grid
plt.grid(color='grey', linestyle='--', linewidth=0.5)

# Display the plot
plt.show()


# Function to calculate the probability of relapse at each time point
def probability_of_relapse(mean, std, threshold, n_patients):
    return stats.norm.cdf(threshold, loc=mean, scale=std)


# Probability of relapse at each time point and cumulative probability
prob_relapse_at_week = []
cumulative_prob_relapse = []

for week in week_labels:
    # Probability of relapse at the current week
    current_week_prob = probability_of_relapse(*phq_scores_maintenance[week], phq_threshold, n)
    prob_relapse_at_week.append(current_week_prob)

    # Cumulative probability up to the current week
    if cumulative_prob_relapse:
        cumulative_prob = 1 - (1 - cumulative_prob_relapse[-1]) * (1 - current_week_prob)
    else:
        cumulative_prob = current_week_prob
    cumulative_prob_relapse.append(cumulative_prob)

# In case of a logarithmic fit the degree is typically set to 1
poly_degree = 1
# Small constant to avoid log(0)
eps = 1e-7

# Get rid of baseline week (week0)
adjusted_week_numbers = week_numbers[1:]
adjusted_cumulative_prob_relapse = cumulative_prob_relapse[1:]
# Add eps to all elements of adjusted_cumulative_prob_relapse
adjusted_cumulative_prob_relapse = np.array(adjusted_cumulative_prob_relapse) + eps

week_range = np.linspace(min(adjusted_week_numbers), max(adjusted_week_numbers), 100)

plt.figure(figsize=(12, 6))
plt.plot(adjusted_week_numbers, adjusted_cumulative_prob_relapse, 'b-o', markersize=8,
         label='Cumulative Relapse Probability')

plt.xticks(adjusted_week_numbers, week_labels[1:]) # Skip the baseline week
plt.xlabel('Weeks', fontsize=12)
plt.ylabel('Cumulative Relapse Probability', fontsize=12)
plt.title('Cumulative Probability of Relapse Over Time With Logarithmic Fit', fontsize=14)
plt.legend(loc='best', fontsize=10)
plt.grid(color='grey', linestyle='--', linewidth=0.5)
plt.show()
