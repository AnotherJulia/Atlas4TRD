import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

colors_treatments = {
        "ad": "blue",
        "ap": "purple",
        "ad_ap": "orange",
        "ect": "green",
        "esketamine": "red"
}

markers_treatments = {
        "ad": "o",
        "ap": "D",
        "ad_ap": "s",
        "ect": "v",
        "esketamine": "^"
}

colors_cases = {
        "10% of capacity Esketamine": "blue",
        "20% of capacity Esketamine": "red",
        "40% of capacity Esketamine": "green",
        "Without Esketamine": "orange"
}

markers_cases = {
        "10% of capacity Esketamine": "o",
        "20% of capacity Esketamine": "s",
        "40% of capacity Esketamine": "D",
        "Without Esketamine": "^",
}

markevery = 0.1

def analyse_instances(simulation_instances):
    stabilization_time=400

    print("----------------------")
    # calculate_employment_rate_by_case(simulation_instances)
    # calculate_time_in_system(simulation_instances, cr=800)
    # calculate_cost_effectiveness(simulation_instances)
    # calculate_transition_rates_post_stabilization(simulation_instances, stabilization_time)
    # calculate_patient_durations(simulation_instances, stabilization_time)
    # calculate_average_treatments(simulation_instances)
    # calculate_average_relapses(simulation_instances)

    # # Call the function with your simulation_instances data
    # calculate_average_waiting_times_post_stabilization(simulation_instances, stabilization_time)
    # print("----------------------")

    analyse_aspect(simulation_instances, aspect='remission', title="Average number of patients in remission")
    analyse_aspect_percentages(simulation_instances, 'remission')

    analyse_aspect(simulation_instances, aspect='recovery', title="Average number of patients in recovery")
    analyse_aspect_percentages(simulation_instances, 'recovery')

    analyse_waiting_list(simulation_instances)

    plot_total_waiting_list_size(simulation_instances)
    # plot_waiting_list_proportions(simulation_instances)
    analyse_waiting_list_proportions(simulation_instances)


def plot_data(time, data, title):
    plt.figure(figsize=(6, 4.5))
    for name, occupation in data.items():
        occupation = np.pad(occupation, (0, len(time) - len(occupation)), 'constant', constant_values=(0)) if len(occupation) < len(time) else occupation
        plt.plot(time, occupation, label=name)

    plt.xlabel("Time in weeks")
    plt.ylabel("Number of patients")
    # plt.title(title)
    plt.legend()
    plt.show()

def analyse_aspect(simulation_instances, aspect, title, confidence_level=0.95, last_n_weeks=52):
    aspect_data = {}
    aspect_cis = {}  # Store CIs for each case for all weeks
    all_times = []

    print(f"--- Analyzing {title} ---")

    for name, instances in simulation_instances.items():
        all_occupations = []
        for instance in instances:
            time_data = instance.run_data["time"]
            all_times.append(time_data)  # Collect all time data for plotting
            all_occupations.append(instance.run_data["bubble_occupancies"][aspect])

        # Calculate mean for the entire time range
        mean_occupation = np.mean(all_occupations, axis=0)
        aspect_data[name] = mean_occupation

        # Calculate SEM and CI for all weeks
        sem = stats.sem(all_occupations, axis=0, nan_policy='omit')
        dof = len(all_occupations) - 1  # Degrees of freedom
        t_critical = stats.t.ppf((1 + confidence_level) / 2, dof)
        ci = t_critical * sem
        aspect_cis[name] = ci
 
        # Calculate and print the average aspect value and CI for the last 52 weeks
        trimmed_mean = np.mean(mean_occupation[-last_n_weeks:])
        trimmed_ci = np.mean(ci[-last_n_weeks:])
        print(f"{name} - Average {aspect} over the last {last_n_weeks} weeks: {trimmed_mean:.2f} ±{trimmed_ci:.2f}")

    max_length_time = max(len(time) for time in all_times)
    time = np.arange(0, max_length_time, 1)

    # Plot data with CI fill for all weeks
    plt.figure(figsize=(6, 4.5))
    for name, occupation in aspect_data.items():
        ci = aspect_cis[name]
        plt.plot(time, occupation, label=name, color=colors_cases[name], marker=markers_cases[name], markevery=markevery)
        # plt.fill_between(time, occupation - ci, occupation + ci, alpha=0.2)

    plt.xlabel("Time in weeks")
    plt.ylabel(f"Number of patients")

    ylim=1400
    if aspect == "remission":
        ylim = 100
        
    plt.xlim(0, 750)
    plt.ylim(0, ylim)

    # plt.title(title)
    plt.savefig(f'results/fig_{aspect}.png', dpi=300, bbox_inches='tight')

    plt.legend()
    plt.grid(True)
    plt.show()

def analyse_aspect_percentages(simulation_instances, aspect, confidence_level=0.95, last_n_weeks=52):
    # Aspect must be either 'recovery' or 'remission'
    assert aspect in ["recovery", "remission"] 

    aspect_rates = {}  # Dictionary for average rates for all cases
    aspect_cis = {}  # Store CIs for each case for all weeks
    all_times = []

    print(f"--- Analyzing {aspect} percentages ---")

    # Gather all time points
    for instances in simulation_instances.values():
        for instance in instances:
            time_data = instance.run_data["time"]
            all_times.append(time_data)

    # Determine the time range for the entire dataset
    max_length_time = max(len(time) for time in all_times)
    time = np.arange(0, max_length_time, 1)

    for case, instances in simulation_instances.items():
        case_aspect_rates = []
        case_total_occupancies = []

        for instance in instances:
            occupancies = instance.run_data["bubble_occupancies"]
            waiting_lists = instance.run_data["waiting_list"]
            aspect_occupancies = occupancies.get(aspect, np.zeros(len(time)))

            # Combine occupancies and waiting list sizes for total occupancies
            combined_total_occupancies = []
            for t in range(len(time)):
                total_at_t = sum(occupancies.get(bubble, np.zeros(len(time)))[t] for bubble in occupancies)
                waiting_list_at_t = sum(waiting_lists.get(bubble, np.zeros(len(time)))[t] for bubble in waiting_lists)
                combined_total_occupancies.append(total_at_t + waiting_list_at_t)

            case_total_occupancies.append(combined_total_occupancies)

            # Compute aspect rates for the entire time frame
            aspect_rate = np.divide(aspect_occupancies, combined_total_occupancies, out=np.zeros_like(aspect_occupancies, dtype=np.float64), where=np.array(combined_total_occupancies) > 0)
            case_aspect_rates.append(aspect_rate)

        # Calculate mean rates and SEM for the entire time frame
        mean_rates = np.mean(case_aspect_rates, axis=0)
        sem = stats.sem(case_aspect_rates, axis=0, nan_policy='omit')
        aspect_rates[case] = mean_rates

        # Calculate CI for all weeks
        aspect_cis[case] = sem * stats.t.ppf((1 + confidence_level) / 2, len(case_aspect_rates) - 1)

        # Calculate and print the average rate and CI for the last 52 weeks
        trimmed_mean = np.mean(mean_rates[-last_n_weeks:])
        trimmed_ci = np.mean(aspect_cis[case][-last_n_weeks:])
        print(f"{case} - Average {aspect} percentage for the last {last_n_weeks} weeks: {trimmed_mean * 100:.2f}% ±{trimmed_ci * 100:.2f}%")

    # Plot data with CI fill for all weeks
    plt.figure(figsize=(6, 4.5))
    for case, rates in aspect_rates.items():
        ci = aspect_cis[case]
        plt.plot(time, rates, label=case, color=colors_cases[case], marker=markers_cases[case], markevery=markevery)  # Convert to percentage
        # plt.fill_between(time, (rates - ci) * 100, (rates + ci) * 100, alpha=0.2)  # Convert to percentage

    plt.xlim(0, 750)
    
    ylim = 1
    if aspect == "remission":
        ylim = 0.1
    elif aspect == "recovery":
        ylim = 1

    plt.ylim(0, ylim)

    plt.xlabel('Time in Weeks')
    plt.ylabel(f'Proportion of patients')
    # plt.title(f'{aspect.capitalize()} Rates Over Time with CI')
    plt.legend()
    plt.grid(True)

    plt.savefig(f'results/fig_{aspect}_proportion.png', dpi=300, bbox_inches='tight')

    plt.show()


def analyse_waiting_list(simulation_instances):
    # Define the treatment bubbles of interest

    bubbles_of_interest = ["ad", "ap", "ad_ap", "ect", "esketamine"]

    # Initialize a dictionary to hold waiting list data for each case and bubble
    waiting_list_data = {case: {bubble: [] for bubble in bubbles_of_interest} for case in simulation_instances}
   
    all_times = [time for instances in simulation_instances.values() for instance in instances for time in instance.run_data["time"]]
    max_time = max(all_times) if all_times else 52
    time_axis = np.arange(0, max_time + 1, 1)

    for case, instances in simulation_instances.items():
        if case == "Without Esketamine": bubbles_of_interest = ["ad", "ap", "ad_ap", "ect"]
        else: bubbles_of_interest = ["ad", "ap", "ad_ap", "ect", "esketamine"]

        for instance in instances:
            time_data = instance.run_data["time"]
            for bubble in bubbles_of_interest:
                waiting_list_sizes = instance.run_data["waiting_list"].get(bubble, np.zeros(len(time_data)))
                waiting_list_data[case][bubble].append(np.interp(time_axis, time_data, waiting_list_sizes))

    # Plot average waiting list sizes for each bubble in each case
    for case, bubbles in waiting_list_data.items():
        plt.figure(figsize=(6, 4.5))
        for bubble, sizes in bubbles.items():
            if sizes:  # Only plot if there is data
                avg_sizes = np.mean(sizes, axis=0)
                plt.plot(time_axis, avg_sizes, label=bubble, color=colors_treatments[bubble], marker=markers_treatments[bubble], markevery=markevery)

        # plt.title(f'Average Waiting List Size Over Time - {case}')
       

        plt.xlim(0, 750)
        plt.ylim(0, 1300)

        plt.xlabel('Time in Weeks')
        plt.ylabel('Number of patients')
        plt.legend()
        plt.grid(True)

        plt.savefig(f'results/fig_waiting_{case}.png', dpi=300, bbox_inches='tight')

        plt.show()

def plot_total_waiting_list_size(simulation_instances):
    # Initialize a dictionary to hold total waiting list size data for each case
    total_waiting_list_data = {case: [] for case in simulation_instances}
    time_data = []

    # Aggregate waiting list sizes across all bubbles for each case at each time step
    for case, instances in simulation_instances.items():
        all_waiting_list_sizes = []

        for instance in instances:
            instance_time_data = instance.run_data["time"]
            time_data.extend(instance_time_data)  # Collect all time data for plotting

            # Initialize as a float64 array to match the data type of waiting_list_sizes
            instance_waiting_list_sizes = np.zeros_like(instance_time_data, dtype=np.float64)

            for bubble, waiting_list in instance.run_data["waiting_list"].items():
                # Interpolate or extend waiting list sizes to match the time steps
                waiting_list_sizes = np.interp(instance_time_data, instance_time_data[:len(waiting_list)], waiting_list, left=0, right=waiting_list[-1] if waiting_list else 0)
                instance_waiting_list_sizes += waiting_list_sizes

            all_waiting_list_sizes.append(instance_waiting_list_sizes)

        # Calculate mean waiting list size at each time step for this case
        if all_waiting_list_sizes:
            mean_waiting_list_sizes = np.mean(all_waiting_list_sizes, axis=0)
            total_waiting_list_data[case] = mean_waiting_list_sizes

    # Determine the time range for plotting
    max_time = max(time_data)
    time_axis = np.arange(0, max_time + 1, 1)

    # Plot total waiting list size for each case
    plt.figure(figsize=(6, 4.5))
    for case, waiting_list_sizes in total_waiting_list_data.items():
        plt.plot(time_axis[:len(waiting_list_sizes)], waiting_list_sizes, label=case, color=colors_cases[case], marker=markers_cases[case], markevery=markevery)

    plt.xlabel("Time in weeks")
    plt.ylabel("Number of patients")

    plt.xlim(0, 750)
    plt.ylim(0, 1400)

    plt.legend()
    plt.grid(True)

    plt.savefig(f'results/fig_total_waiting.png', dpi=300, bbox_inches='tight')

    plt.show()

def analyse_waiting_list_proportions(simulation_instances):
    bubbles_of_interest=["ap", "ad", "ad_ap", "ect", "esketamine"]
    plt.figure(figsize=(6, 4.5))
    
    # Iterate through each case in the simulation instances
    for case, instances in simulation_instances.items():
        total_waiting_list = []
        total_population = []
        time_points = []

        # Aggregate waiting list sizes and total occupancies across all instances for this case
        for instance in instances:
            time_data = instance.run_data["time"]
            time_points.extend(time_data)  # Collect all time data for plotting

            waiting_list_sizes = np.zeros(len(time_data))
            total_occupancies = np.zeros(len(time_data))

            for bubble in bubbles_of_interest:
                bubble_waiting_list = instance.run_data["waiting_list"].get(bubble, [])
                if len(bubble_waiting_list) < len(time_data):
                    bubble_waiting_list = np.pad(bubble_waiting_list, (0, len(time_data) - len(bubble_waiting_list)), 'constant', constant_values=(0))
                waiting_list_sizes += bubble_waiting_list

            for bubble, occupancies in instance.run_data["bubble_occupancies"].items():
                bubble_occupancies = np.array(occupancies)
                if len(bubble_occupancies) < len(time_data):
                    bubble_occupancies = np.pad(bubble_occupancies, (0, len(time_data) - len(bubble_occupancies)), 'constant', constant_values=(0))
                total_occupancies += bubble_occupancies

            total_waiting_list.append(waiting_list_sizes)
            total_population.append(total_occupancies + waiting_list_sizes)  # Include waiting list in total population

        # Calculate mean waiting list size and total occupancy across all instances for this case
        mean_waiting_list = np.mean(total_waiting_list, axis=0)
        mean_population = np.mean(total_population, axis=0)
        
        # Calculate the proportion of people on the waiting list
        proportion_on_waiting_list = mean_waiting_list / mean_population

        # Plot the proportion of people on the waiting list for this case
        plt.plot(time_points[:len(proportion_on_waiting_list)], proportion_on_waiting_list, label=case, color=colors_cases.get(case, 'grey'), marker=markers_cases.get(case, 'o'), markevery=markevery)

    plt.xlabel("Time in weeks")
    plt.ylabel("Proportion of patients")

    plt.xlim(0, 750)
    plt.ylim(0, 1)

    # plt.title("Proportion of People on Waiting List Over Time")
    plt.legend()
    plt.grid(True)

    plt.savefig(f'results/fig_total_waiting_proportions.png', dpi=300, bbox_inches='tight')

    plt.show()

def plot_waiting_list_proportions(simulation_instances):
    plt.figure(figsize=(6, 4.5))
    
    # Iterate through each case in the simulation instances
    for case, instances in simulation_instances.items():
        total_waiting_list = []
        total_population = []
        time_points = []

        # Aggregate waiting list sizes and total occupancies across all instances for this case
        for instance in instances:
            time_data = instance.run_data["time"]
            time_points.extend(time_data)  # Collect all time data for plotting

            waiting_list_sizes = np.zeros(len(time_data))
            total_occupancies = np.zeros(len(time_data))

            for bubble, sizes in instance.run_data["waiting_list"].items():
                # Ensure the size array matches the time data length
                size_array = np.array(sizes)
                if len(size_array) < len(time_data):
                    size_array = np.pad(size_array, (0, len(time_data) - len(size_array)), 'constant', constant_values=(0))
                waiting_list_sizes += size_array
            
            for bubble, occupancies in instance.run_data["bubble_occupancies"].items():
                occupancy_array = np.array(occupancies)
                if len(occupancy_array) < len(time_data):
                    occupancy_array = np.pad(occupancy_array, (0, len(time_data) - len(occupancy_array)), 'constant', constant_values=(0))
                total_occupancies += occupancy_array

            total_waiting_list.append(waiting_list_sizes)
            total_population.append(total_occupancies)

        # Calculate mean waiting list size and total occupancy across all instances for this case
        mean_waiting_list = np.mean(total_waiting_list, axis=0)
        mean_population = np.mean(total_population, axis=0)
        
        # Calculate the proportion of people on the waiting list
        proportion_on_waiting_list = np.divide(mean_waiting_list, mean_population, where=mean_population!=0)

        # Plot the proportion of people on the waiting list for this case
        plt.plot(time_points[:len(proportion_on_waiting_list)], proportion_on_waiting_list/100, label=case, color=colors_cases.get(case, 'grey'), marker=markers_cases.get(case, 'o'), markevery=markevery)

    plt.xlabel("Time in weeks")
    plt.ylabel("Proportion of patients")
    # plt.title("Proportion of People on Waiting List Over Time")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 750)
    plt.ylim(0, 0.5)

    plt.savefig(f'results/fig_total_waiting_proportion.png', dpi=300, bbox_inches='tight')

    plt.show()

def calculate_employment_rate(simulation_instances):
    employment_rates = [np.mean([agent.employed for agent in instance.agents]) for _, instances in simulation_instances.items() for instance in instances]
    print(f"Employment Rate: {np.mean(employment_rates)*100}%")

def calculate_employment_rate_by_case(simulation_instances):
    for case_name, instances in simulation_instances.items():
        # Collect all employment statuses for this case
        employment_statuses = [agent.employed for instance in instances for agent in instance.agents]
        
        # Calculate the employment rate for this case
        employment_rate = np.mean(employment_statuses) * 100  # Convert to percentage
        
        # Print the employment rate for this case
        print(f"Employment Rate for {case_name}: {employment_rate:.2f}%")

def calculate_time_in_system(simulation_instances, cr=500):
    total_times = []
    recovery_extension = 24

    for instances in simulation_instances.values():
        for instance in instances:
            for agent in instance.agents:
                if agent.medical_history:
                    # Filter events that occur at or after t=cr
                    filtered_history = [event for event in agent.medical_history if event['time'] >= cr]
                    
                    if filtered_history:
                        first_event_time = filtered_history[0]['time']
                        last_event = filtered_history[-1]

                        last_event_state = last_event["data"].get('state', "")
                        
                        # Check if the last event is 'recovery'
                        if last_event_state == 'recovery':
                            # Consider the time up to the last 'recovery' event plus an additional 24 weeks
                            last_event_time = last_event['time'] + recovery_extension
                        else:
                            # If the last event is not 'recovery', skip this agent
                            continue

                        # Calculate total time in the system for the agent with the specified conditions
                        total_time = last_event_time - first_event_time
                        total_times.append(total_time)

    average_time_in_system = np.mean(total_times) if total_times else 0  # Avoid division by zero if total_times is empty
    print(f"Average time in system from t={cr} with recovery cutoff (wk): {average_time_in_system}")


# def calculate_cost_effectiveness(simulation_instances):
#     QOL_REMISSION = 0.901
#     QOL_RESPONSE = 0.673
#     QOL_NO_RESPONSE = 0.417
#     TRT = {'ad', "ap", "ad_ap", "esketamine", "ect"}
#     pass
def calculate_transition_rates(simulation_instances):
    remission_transitions = 0
    recovery_transitions = 0
    total_patients = 0

    for instances in simulation_instances.values():
        for instance in instances:
            for agent in instance.agents:
                total_patients += 1  # Count each patient
                entered_remission = False
                entered_recovery = False

                for event in agent.medical_history:
                    if event['type'] == 'treatment_end' and event['data'].get('state') == 'remission':
                        entered_remission = True
                    if event['type'] == 'movement_event' and event['data'].get('state') == 'recovery':
                        entered_recovery = True

                if entered_remission:
                    remission_transitions += 1
                if entered_recovery:
                    recovery_transitions += 1

    remission_rate = remission_transitions / total_patients if total_patients > 0 else 0
    recovery_rate = recovery_transitions / total_patients if total_patients > 0 else 0

    print(f"Remission Rate: {remission_rate:.2f}")
    print(f"Recovery Rate: {recovery_rate:.2f}")

def calculate_transition_rates_post_stabilization(simulation_instances, stabilization_time=750):
    print("--- Transition Rates Post Stabilization ---")

    case_results = {}

    for case_name, instances in simulation_instances.items():
        remission_transitions = 0
        recovery_transitions = 0
        relapse_events = 0  # Track relapse events
        patients_considered = 0

        for instance in instances:
            for agent in instance.agents:
                # Filter the medical history for events after stabilization_time
                post_stabilization_history = [event for event in agent.medical_history if event['time'] >= stabilization_time]

                if not post_stabilization_history:
                    continue  # Skip this agent if no relevant history after stabilization

                patients_considered += 1  # Count this patient as considered
                entered_remission = False
                entered_recovery = False
                experienced_relapse = False  # Track if the patient experienced relapse

                for event in post_stabilization_history:
                    if event['type'] == 'treatment_end' and event['data'].get('state') == 'remission':
                        entered_remission = True
                    if event['type'] == 'movement_event' and event['data'].get('state') == 'recovery':
                        entered_recovery = True
                    if event['type'] == 'relapse' or (event['type'] == 'bubble-change' and event['data'].get('bubble') == 'relapse'):
                        experienced_relapse = True

                if entered_remission:
                    remission_transitions += 1
                if entered_recovery:
                    recovery_transitions += 1
                if experienced_relapse:
                    relapse_events += 1  # Increment relapse count

        remission_rate = remission_transitions / patients_considered if patients_considered > 0 else 0
        recovery_rate = recovery_transitions / patients_considered if patients_considered > 0 else 0
        relapse_rate = relapse_events / patients_considered if patients_considered > 0 else 0  # Calculate relapse rate

        case_results[case_name] = {
            'remission_rate': remission_rate,
            'recovery_rate': recovery_rate,
            'relapse_rate': relapse_rate,  # Add relapse rate to results
            'patients_considered': patients_considered
        }

    # Print the results for each case
    for case_name, results in case_results.items():
        print(f"Case '{case_name}':")
        print(f"  Patients considered: {results['patients_considered']}")
        print(f"  Remission Rate: {results['remission_rate']:.2f}")
        print(f"  Recovery Rate: {results['recovery_rate']:.2f}")
        print(f"  Relapse Rate: {results['relapse_rate']:.2f}\n")  # Print relapse rate

def calculate_patient_durations(simulation_instances, stabilization_time=800):
    print("--- Durations ---")
    case_averages = {}

    for case_name, instances in simulation_instances.items():
        durations = []
        waiting_times = []

        # Initialize average and CI variables to default values
        avg_duration = 0
        duration_ci = 0
        avg_waiting_time = 0
        waiting_ci = 0

        for instance in instances:
            for agent in instance.agents:
                # Filter the medical history for events after stabilization_time
                filtered_history = [event for event in agent.medical_history if event['time'] >= stabilization_time]

                if not filtered_history:
                    continue  # Skip this patient if no relevant history after stabilization

                reached_recovery = any(
                    event['type'] == 'bubble-change' and event['data'].get('bubble') == 'recovery'
                    for event in filtered_history
                )

                if not reached_recovery:
                    continue  # Skip if the patient has not reached recovery

                # Calculate the duration in the system and total waiting time
                start_time = filtered_history[0]['time']
                end_time = filtered_history[-1]['time']
                duration = end_time - start_time

                total_waiting_time = 0
                for i, event in enumerate(filtered_history[:-1]):  # Exclude the last event
                    if event['type'] == 'waiting':
                        next_event_time = filtered_history[i + 1]['time']
                        total_waiting_time += next_event_time - event['time']

                durations.append(duration)
                waiting_times.append(total_waiting_time)
         
        # Calculate average and confidence interval for duration and waiting time
        if durations:
            avg_duration = np.mean(durations)
            duration_sem = stats.sem(durations)
            duration_ci = duration_sem * stats.t.ppf((1 + 0.95) / 2, len(durations) - 1)

        if waiting_times:
            avg_waiting_time = np.mean(waiting_times)
            waiting_sem = stats.sem(waiting_times)
            waiting_ci = waiting_sem * stats.t.ppf((1 + 0.95) / 2, len(waiting_times) - 1)

        case_averages[case_name] = {
            'avg_duration': avg_duration,
            'duration_ci': duration_ci,
            'avg_waiting_time': avg_waiting_time,
            'waiting_ci': waiting_ci
        }

    # Print the results
    for case_name, metrics in case_averages.items():
        print(f"Case '{case_name}':")
        print(f"  Average Duration in system: {metrics['avg_duration']:.2f} weeks, CI: ±{metrics['duration_ci']:.2f}")
        print(f"  Average Waiting Time: {metrics['avg_waiting_time']:.2f} weeks, CI: ±{metrics['waiting_ci']:.2f}\n")


def calculate_average_treatments(simulation_instances):
    print("--- Num. Treatments from Agents ---")
    case_treatment_averages = {}

    for case_name, instances in simulation_instances.items():
        total_treatments = 0
        total_patients = 0

        for instance in instances:
            for agent in instance.agents:
                # Directly use the num_treatments_tried attribute
                total_treatments += agent.num_treatments_tried
                total_patients += 1

        # Calculate the average number of treatments per patient for this case
        average_treatments = total_treatments / total_patients if total_patients > 0 else 0
        case_treatment_averages[case_name] = average_treatments

    # Print the average number of treatments for each case
    for case_name, avg_treatments in case_treatment_averages.items():
        print(f"Case '{case_name}': Average Treatments per Patient: {avg_treatments:.2f}")


def calculate_average_relapses(simulation_instances):
    print("--- Average Num. Relapses per Case ---")
    case_relapse_averages = {}

    for case_name, instances in simulation_instances.items():
        total_relapses = 0
        total_patients = 0

        for instance in instances:
            for agent in instance.agents:
                # Add the number of relapses for this agent to the total count for the case
                total_relapses += agent.num_relapses
                total_patients += 1

        # Calculate the average number of relapses per patient for this case
        average_relapses = total_relapses / total_patients if total_patients > 0 else 0
        case_relapse_averages[case_name] = average_relapses

    # Print the average number of relapses for each case
    for case_name, avg_relapses in case_relapse_averages.items():
        print(f"Case '{case_name}': Average Relapses per Patient: {avg_relapses:.2f}")

def calculate_average_waiting_times_post_stabilization(simulation_instances, stabilization_time):
    print("--- Average Waiting Times Post Stabilization for New Patients ---")
    case_waiting_time_averages = {}

    for case_name, instances in simulation_instances.items():
        total_waiting_time = 0
        new_agents_waited = 0

        for instance in instances:
            for agent in instance.agents:
                if agent.medical_history:
                    # Determine the entry time of the agent into the system
                    entry_time = agent.medical_history[0]['time']

                    # Proceed only if the agent entered the system after stabilization
                    if entry_time >= stabilization_time:
                        # Sum up waiting times from the medical history
                        new_agents_waited += 1
                        total_waiting_time += agent.total_waiting_time
        
        # Calculate the average waiting time for new agents post-stabilization
        average_waiting_time = total_waiting_time / new_agents_waited if new_agents_waited > 0 else 0
        case_waiting_time_averages[case_name] = average_waiting_time

    # Print the average waiting times for each case
    for case_name, avg_waiting_time in case_waiting_time_averages.items():
        print(f"Case '{case_name}': Average Waiting Time for New Patients Post Stabilization: {avg_waiting_time:.2f} weeks")

