import matplotlib.pyplot as plt
import numpy as np

def analyse_instances(simulation_instances):
    print("----------------------")
    # calculate_employment_rate_by_case(simulation_instances)
    # calculate_time_in_system(simulation_instances, cr=800)
    calculate_cost_effectiveness(simulation_instances)
    # print("----------------------")

    analyse_aspect(simulation_instances, aspect='remission', title="Average number of patients in remission")
    # analyse_aspect_percentages(simulation_instances, 'remission')

    analyse_aspect(simulation_instances, aspect='recovery', title="Average number of patients in recovery")
    analyse_aspect_percentages(simulation_instances, 'recovery')

    # analyse_waiting_list(simulation_instances)

def plot_data(time, data, title):
    plt.figure(figsize=(10, 6))
    for name, occupation in data.items():
        occupation = np.pad(occupation, (0, len(time) - len(occupation)), 'constant', constant_values=(0)) if len(occupation) < len(time) else occupation
        plt.plot(time, occupation, label=name)

    plt.xlabel("Time in weeks")
    plt.ylabel("Number of patients")
    plt.title(title)
    plt.legend()
    plt.show()

def analyse_aspect(simulation_instances, aspect, title):
    aspect_data = {}
    all_times = []

    for name, instances in simulation_instances.items():
        all_occupations = []
        for instance in instances:
            time_data = instance.run_data["time"]
            all_times.append(time_data)
            all_occupations.append(instance.run_data["bubble_occupancies"][aspect])

        max_length = max(len(occ) for occ in all_occupations)
        padded_occupations = [np.pad(occ, (0, max_length - len(occ)), 'constant', constant_values=(0)) for occ in all_occupations]
        average_occupation = np.mean(padded_occupations, axis=0)
        aspect_data[name] = average_occupation

    max_length_time = max(len(time) for time in all_times) if all_times else 53
    time = np.arange(0, max_length_time, 1)

    plot_data(time, aspect_data, title)

def analyse_aspect_percentages(simulation_instances, aspect):
    assert aspect in ["recovery", "remission"], "Aspect must be either 'recovery' or 'remission'"
    
    aspect_rates = {}  # Dictionary for average rates for all cases
    all_times = []

    # Gather all time points
    for instances in simulation_instances.values():
        for instance in instances:
            time_data = instance.run_data["time"]
            all_times.extend(time_data)

    # Determine the longest time series
    max_time = max(all_times) if all_times else 52  # Default to 53 if no time data is available
    time = np.arange(0, max_time + 1, 1)

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

            # Compute aspect rates
            aspect_rate = np.divide(aspect_occupancies, combined_total_occupancies, out=np.zeros_like(aspect_occupancies, dtype=np.float64), where=np.array(combined_total_occupancies) > 0)
            case_aspect_rates.append(aspect_rate)

        aspect_rates[case] = np.mean(case_aspect_rates, axis=0)

    # Plot aspect rates
    plt.figure(figsize=(10, 6))
    for case, rates in aspect_rates.items():
        plt.plot(time, rates, label=case)
    plt.xlabel('Time (weeks)')
    plt.ylabel(f'{aspect.capitalize()} Rate')
    plt.title(f'{aspect.capitalize()} Rates Over Time')
    plt.legend()
    plt.ylim(0, 1)  # Aspect rates should be between 0 and 1
    plt.show()


def analyse_waiting_list(simulation_instances):
    # Define the treatment bubbles of interest
    bubbles_of_interest = ["ad", "ap", "ad_ap", "esketamine", "ect"]

    # Initialize a dictionary to hold waiting list data for each case and bubble
    waiting_list_data = {case: {bubble: [] for bubble in bubbles_of_interest} for case in simulation_instances}
   
    all_times = [time for instances in simulation_instances.values() for instance in instances for time in instance.run_data["time"]]
    max_time = max(all_times) if all_times else 53
    time_axis = np.arange(0, max_time + 1, 1)

    for case, instances in simulation_instances.items():
        for instance in instances:
            time_data = instance.run_data["time"]
            for bubble in bubbles_of_interest:
                waiting_list_sizes = instance.run_data["waiting_list"].get(bubble, np.zeros(len(time_data)))
                waiting_list_data[case][bubble].append(np.interp(time_axis, time_data, waiting_list_sizes))

    # Plot average waiting list sizes for each bubble in each case
    for case, bubbles in waiting_list_data.items():
        plt.figure(figsize=(10, 5))
        for bubble, sizes in bubbles.items():
            if sizes:  # Only plot if there is data
                avg_sizes = np.mean(sizes, axis=0)
                plt.plot(time_axis, avg_sizes, label=bubble)

        plt.title(f'Average Waiting List Size Over Time - {case}')
        plt.xlabel('Time (weeks)')
        plt.ylabel('Average Waiting List Size')
        plt.legend()
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


def calculate_cost_effectiveness(simulation_instances):
    QOL_REMISSION = 0.901
    QOL_RESPONSE = 0.673
    QOL_NO_RESPONSE = 0.417
    TRT = {'ad', "ap", "ad_ap", "esketamine", "ect"}
    pass
