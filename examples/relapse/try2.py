import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.interpolate import PchipInterpolator

import statsmodels.api as sm

time_points = {"baseline": 0, "6wk": 1.5, "12wk": 3, "26wk": 6.5, "39wk": 9.75, "52wk": 13}
phq_scores_maintenance = {"baseline": [3.9, 3.5], "6wk": [4.1, 3.8], "12wk": [4.1, 3.8], "26wk": [4.2, 3.7], "39wk": [3.8, 3.9], "52wk": [3.7, 3.7]}
phq_scores_discontinued = {"baseline": [3.8, 3.6], "6wk": [4.4, 4.0], "12wk": [6.3, 5.1], "26wk": [5.0, 4.6], "39wk": [4.4, 4.2], "52wk": [4.0, 4.5]}
relapse_threshold = 5


# SOURCE ESKETAMINE DATA
# Castro, M., Wilkinson, S. T., al Jurdi, R. K., Petrillo, M. P., Zaki, N., Borentain, S., Fu, D. J., Turkoz, I.,
# Sun, L., Brown, B., & Cabrera, P. (2023). Efficacy and Safety of Esketamine Nasal Spray in Patients with
# Treatment-Resistant Depression Who Completed a Second Induction Period: Analysis of the Ongoing SUSTAIN-3 Study.
# CNS Drugs, 37(8), 715–723. https://doi.org/10.1007/s40263-023-01026-3

data = [
    [0, 12],
    [3, 7],
    [7, 7],
    [10, 7],
    [14, 8],
    [17, 7],
    [21, 7],
    [24, 7],
    [28, 8],
    [31, 7],
    [35, 7],
    [38, 7],
    [42, 8],
    [45, 7],
    [48, 8],
    [52, 9]
]

phq_scores_esketamine = {f"{d[0]}wk" if d[0] != 0 else "baseline": [d[1], 3] for d in data}

print(phq_scores_esketamine)
#
# time_points = {time: int(time[:-2]) / 4 if time != "baseline" else 0
#                           for time in phq_scores_esketamine.keys()}
# print(time_points)

def calculate_cumulative_proportions(interval_probs):
    cumulative_probs = [interval_probs[0]]
    for i in range(1, len(interval_probs)):
        cumulative_prob = cumulative_probs[i - 1] + interval_probs[i]
        cumulative_probs.append(cumulative_prob)
    return cumulative_probs


class GroupData:
    def __init__(self, name, phq_scores):
        self.name = name
        self.phq_scores = phq_scores
        self.sorted_times = sorted(time_points.keys(), key=lambda x: time_points[x])
        self.sorted_time_values = [time_points[time] for time in self.sorted_times]

    def calculate_proportions(self):
        proportions = {}
        for time, (mean, sd) in self.phq_scores.items():
            proportion_relapse = norm.sf(relapse_threshold, loc=mean, scale=sd)
            proportions[time] = proportion_relapse
        return proportions

    def cumulative_to_interval(self, cumulative_probs):
        sorted_probs = [cumulative_probs[time] for time in self.sorted_times]
        interval_probs = [sorted_probs[0]]
        for i in range(1, len(sorted_probs)):
            interval_prob = sorted_probs[i] - sorted_probs[i - 1]
            interval_probs.append(max(interval_prob, 0))
        return interval_probs

    def calculate_interval_probs(self):
        proportions = self.calculate_proportions()
        return self.cumulative_to_interval(proportions)

    def plot_interval_probs(self, interval_probs, linestyle):
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.step(self.sorted_time_values, interval_probs,
                label=f'{self.name} Group',
                where='mid',
                linestyle=linestyle,
                linewidth=2)

        # Customize the title
        title = f'Interval Relapse Probability Over Time for {self.name} Group\n' \
                'Step plot: each horizontal line represents the probability of relapse in that interval.'
        plt.title(title, fontsize=14)

        plt.xlabel('Time (months)')
        plt.ylabel('Probability of Relapse in Interval')
        plt.legend(loc='upper right')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
        plt.show()

    def interp_interval_plot(self, interval_probs, interp_kind='cubic'):
        # Interpolate the interval probs based on the sorted time values
        sorted_time_values_np = np.array(self.sorted_time_values)
        interval_probs_np = np.array(interval_probs)

        f = interp1d(sorted_time_values_np, interval_probs_np, kind=interp_kind)
        xnew = np.linspace(0, 13, num=1000, endpoint=True)

        fig, ax = plt.subplots(figsize=(12, 8))
        plt.scatter(sorted_time_values_np, interval_probs_np,  label=f'{self.name} !scatter!', linewidth=2)
        plt.plot(xnew, f(xnew), label=f'{self.name} Group', linewidth=2)
        title = f'Interpolated Interval Relapse Probability Over Time for {self.name} Group\n' \
                'The curve represents interpolation of interval probabilities of relapse.'
        plt.title(title, fontsize=14)

        plt.xlabel('Time (months)')
        plt.ylabel('Interpolated Probability of Relapse in Interval')
        plt.legend(loc='upper right')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
        plt.show()


    def interp_plot(self, interval_probs, interp_kind='cubic'):
        sorted_time_values_np = np.array(self.sorted_time_values)
        interval_probs_np = np.array(interval_probs)
        f = interp1d(sorted_time_values_np, interval_probs_np, kind=interp_kind)
        xnew = np.linspace(0, 13, num=1000, endpoint=True)
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.plot(xnew, f(xnew), label=f'{self.name} Group', linewidth=2)
        plt.xlabel('Time (months)')
        plt.ylabel('Probability of Relapse in Interval')
        title = f'Interval Relapse Probability Over Time for {self.name} Group\n' \
                'This plot shows the estimated probability of a participant relapsing within specific time intervals.'
        plt.title(title, fontsize=14)
        plt.legend(loc='upper right')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
        plt.show()

    def calculate_cumulative_probability(self, time_point, interval_probs):
        cumulative_probability = 0
        for i, time in enumerate(self.sorted_time_values):
            if time <= time_point:
                cumulative_probability += interval_probs[i]
            else:
                break
        return cumulative_probability

    def interp_cumulative_plot(self, interval_probs):
        cumulative_probs = calculate_cumulative_proportions(interval_probs)
        f = PchipInterpolator(np.array(self.sorted_time_values), np.array(cumulative_probs))
        xnew = np.linspace(0, 13, num=1000, endpoint=True)
        plt.figure(figsize=(10, 6))
        plt.plot(xnew, f(xnew), label=f'{self.name} Group', linewidth=2)
        plt.xlabel('Time (months)')
        plt.ylabel('Cumulative Probability')
        title = f'Cumulative Probability of Relapse Over Time for {self.name} Group\n' \
                'This plot shows the estimated cumulative probability of a participant relapsing over time.'
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()


def compare_interval_probs(group_data1, interval_probs1, group_data2, interval_probs2, interp_kind='cubic'):
    # Interpolate the interval probabilities for the first group
    sorted_time_values_np1 = np.array(group_data1.sorted_time_values)
    interval_probs_np1 = np.array(interval_probs1)
    f1 = interp1d(sorted_time_values_np1, interval_probs_np1, kind=interp_kind)

    # Interpolate the interval probabilities for the second group
    sorted_time_values_np2 = np.array(group_data2.sorted_time_values)
    interval_probs_np2 = np.array(interval_probs2)
    f2 = interp1d(sorted_time_values_np2, interval_probs_np2, kind=interp_kind)

    xnew = np.linspace(0, 13, num=1000, endpoint=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.plot(xnew, f1(xnew), label=f'{group_data1.name} Group', linewidth=2)
    plt.plot(xnew, f2(xnew), label=f'{group_data2.name} Group', linewidth=2)

    title = 'Interpolated Interval Relapse Probability Over Time\nFor the Maintenance and Discontinued Groups'
    plt.title(title, fontsize=14)
    plt.xlabel('Time (months)')
    plt.ylabel('Interpolated Probability of Relapse in Interval')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1)
    plt.show()


maintenance_data = GroupData('Maintenance', phq_scores_maintenance)
discontinued_data = GroupData('Discontinued', phq_scores_discontinued)

interval_probs_maintenance = maintenance_data.calculate_interval_probs()
interval_probs_discontinued = discontinued_data.calculate_interval_probs()


maintenance_data.plot_interval_probs(interval_probs_maintenance, '-')
discontinued_data.plot_interval_probs(interval_probs_discontinued, '--')
plt.show()

maintenance_data.interp_cumulative_plot(interval_probs_maintenance)
discontinued_data.interp_cumulative_plot(interval_probs_discontinued)

maintenance_data.interp_interval_plot(interval_probs_maintenance)
discontinued_data.interp_interval_plot(interval_probs_discontinued)

# Comparison plot
# compare_interval_probs(maintenance_data, interval_probs_maintenance, discontinued_data, interval_probs_discontinued, 'quadratic')

# esketamine_data = GroupData("Esketamine", phq_scores_esketamine)
# interval_probs_esketamine = esketamine_data.calculate_interval_probs()
#
# esketamine_data.plot_interval_probs(interval_probs_esketamine, linestyle="-")
# plt.show()
#
# esketamine_data.interp_cumulative_plot(interval_probs_esketamine)
# esketamine_data.interp_interval_plot(interval_probs_esketamine)