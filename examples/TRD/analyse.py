import matplotlib.pyplot as plt
import numpy as np

def analyse_instances(simulation_instances):
    # where simulation_instances is a dictionary of key: name of sim -- value: []

    print("----------------------")
    
    calculate_parameters(simulation_instances)
    
    # analyse_remission(simulation_instances)
    analyse_recovery(simulation_instances)
    analyse_recovery_percentages(simulation_instances)
    analyse_waiting_list(simulation_instances)
    # analyse_waiting_list_compare_bubbles(simulation_instances)

    pass

def analyse_recovery(simulation_instances):
    recovery = {}

    all_times = []  # This will collect all time arrays to find the maximum length if they differ

    for name, instances in simulation_instances.items():
        all_occupations = []  # Collect all occupations for this name to compute the average later
        for instance in instances:
            time_data = instance.run_data["time"]
            all_times.append(time_data)  # Collect all time data
            all_occupations.append(instance.run_data["bubble_occupancies"]["recovery"])

        # Ensure all occupation arrays are the same length before averaging
        max_length = max(len(occ) for occ in all_occupations)
        padded_occupations = [np.pad(occ, (0, max_length - len(occ)), 'constant', constant_values=(0)) for occ in all_occupations]
        
        # Compute the average occupation for each time point
        average_occupation = np.mean(padded_occupations, axis=0)
        recovery[name] = average_occupation

    # Determine the longest time array if they vary
    if not all_times:
        time = np.arange(0, 53, 1)
    else:
        max_length_time = max(len(time) for time in all_times)
        time = np.arange(0, max_length_time, 1)

    plt.figure(figsize=(10, 6))
    for name, occupation in recovery.items():
        # Ensure the occupation array matches the length of the time array
        if len(occupation) < len(time):
            occupation = np.pad(occupation, (0, len(time) - len(occupation)), 'constant', constant_values=(0))
        plt.plot(time, occupation, label=name)

    plt.xlabel("Time in weeks")
    plt.ylabel("Number of patients")
    plt.title("Average number of patients in recovery")
    plt.legend()
    plt.show()

def analyse_remission(simulation_instances):
    remission = {}

    all_times = []  # This will collect all time arrays to find the maximum length if they differ

    for name, instances in simulation_instances.items():
        all_occupations = []  # Collect all occupations for this name to compute the average later
        for instance in instances:
            time_data = instance.run_data["time"]
            all_times.append(time_data)  # Collect all time data
            all_occupations.append(instance.run_data["bubble_occupancies"]["remission"])

        # Ensure all occupation arrays are the same length before averaging
        max_length = max(len(occ) for occ in all_occupations)
        padded_occupations = [np.pad(occ, (0, max_length - len(occ)), 'constant', constant_values=(0)) for occ in all_occupations]
        
        # Compute the average occupation for each time point
        average_occupation = np.mean(padded_occupations, axis=0)
        remission[name] = average_occupation

    # Determine the longest time array if they vary
    if not all_times:
        time = np.arange(0, 53, 1)
    else:
        max_length_time = max(len(time) for time in all_times)
        time = np.arange(0, max_length_time, 1)

    plt.figure(figsize=(10, 6))
    for name, occupation in remission.items():
        # Ensure the occupation array matches the length of the time array
        if len(occupation) < len(time):
            occupation = np.pad(occupation, (0, len(time) - len(occupation)), 'constant', constant_values=(0))
        plt.plot(time, occupation, label=name)

    plt.xlabel("Time in weeks")
    plt.ylabel("Number of patients")
    plt.title("Average number of patients in remission")
    plt.legend()
    plt.show()

def analyse_recovery_percentages(simulation_instances):
    recovery_rates = {}  # Dictionary for average recovery rates for all cases
    total_occupancies_dict = {}  # Dictionary for total occupancies including waiting lists
    all_times = []

    # Gather all time points
    for case, instances in simulation_instances.items():
        for instance in instances:
            time_data = instance.run_data["time"]
            all_times.extend(time_data)

    # Determine the longest time series
    max_time = max(all_times) if all_times else 53  # Default to 53 if no time data
    time = np.arange(0, max_time + 1, 1)

    for case, instances in simulation_instances.items():
        case_recovery_rates = []
        case_total_occupancies = []

        for instance in instances:
            occupancies = instance.run_data["bubble_occupancies"]
            waiting_lists = instance.run_data["waiting_list"]
            recovery_occupancies = occupancies.get("recovery", [0] * len(time))

            # Combine occupancies and waiting list sizes for total occupancies
            combined_total_occupancies = []
            for t in range(len(time)):
                total_at_t = sum(occupancies.get(bubble, [0] * len(time))[t] for bubble in occupancies)
                waiting_list_at_t = sum(waiting_lists.get(bubble, [0] * len(time))[t] for bubble in waiting_lists)
                combined_total_occupancies.append(total_at_t + waiting_list_at_t)

            case_total_occupancies.append(combined_total_occupancies)

            recovery_rate = [recovery / total if total > 0 else 0 for recovery, total in zip(recovery_occupancies, combined_total_occupancies)]
            case_recovery_rates.append(recovery_rate)

        recovery_rates[case] = np.mean(case_recovery_rates, axis=0).tolist()
        total_occupancies_dict[case] = np.mean(case_total_occupancies, axis=0).tolist()
    
    rec_rates = []
    for case, rates in recovery_rates.items():
        mean_rates = np.mean(rates)
        rec_rates.append(mean_rates)

        print(f"Case: {case} | Recovery: {mean_rates*100}%")

    # Plot total occupancies including waiting lists
    # plt.figure(figsize=(10, 6))
    # for case, occupancies in total_occupancies_dict.items():
    #     plt.plot(time, occupancies, label=case)
    # plt.xlabel('Time')
    # plt.ylabel('Total Occupancies Including Waiting Lists')
    # plt.title('Total Occupancies Over Time by Case Including Waiting Lists')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # Plot recovery rates
    plt.figure(figsize=(10, 6))
    for case, rates in recovery_rates.items():
        plt.plot(time, rates, label=case)
    plt.xlabel('Time')
    plt.ylabel('Recovery Rate')
    plt.title('Recovery Rates Over Time')
    plt.legend()
    plt.ylim(0, 1)
    plt.show()


# def analyse_recovery_percentages(simulation_instances):
#     recovery_rates = {}  # Dictionary for average recovery rates for all cases
#     total_occupancies_dict = {}  # Dictionary for total occupancies including waiting lists
#     all_times = []

#     # Gather all time points
#     for case, instances in simulation_instances.items():
#         for instance in instances:
#             time_data = instance.run_data["time"]
#             all_times.extend(time_data)

#     # Determine the longest time series
#     max_time = max(all_times) if all_times else 53  # Default to 53 if no time data
#     time = np.arange(0, max_time + 1, 1)

#     for case, instances in simulation_instances.items():
#         case_recovery_rates = []
#         case_total_occupancies = []

#         for instance in instances:
#             occupancies = instance.run_data["bubble_occupancies"]

#             waiting_lists = instance.run_data["waiting_list"]
#             recovery_occupancies = occupancies.get("recovery", [0] * len(time))
#             # num_agents = instance.run_data["num_agents"]

#             # Combine occupancies and waiting list sizes for total occupancies
#             combined_total_occupancies = []
#             for t in range(len(time)):
#                 total_at_t = sum(occupancies.get(bubble, [0] * len(time))[t] for bubble in occupancies)
#                 waiting_list_at_t = sum(waiting_lists.get(bubble, [0] * len(time))[t] for bubble in waiting_lists)
#                 combined_total_occupancies.append(total_at_t + waiting_list_at_t)

#             case_total_occupancies.append(combined_total_occupancies)
#             
#             recovery_rate = []
#             for t in time:
#                 rec_rate_at_t = occupancies['recovery'][t] / num_agents[t]
#                 recovery_rate.append(rec_rate_at_t)

#             case_recovery_rates.append(recovery_rate)

#         recovery_rates[case] = np.mean(case_recovery_rates, axis=0).tolist()
#         total_occupancies_dict[case] = np.mean(case_total_occupancies, axis=0).tolist()
#     
#     rec_rates = []
#     for case, rates in recovery_rates.items():
#         mean_rates = np.mean(rates)
#         rec_rates.append(mean_rates)

#         print(f"Case: {case} | Recovery: {mean_rates*100}%")

#     # Plot total occupancies including waiting lists
#     plt.figure(figsize=(10, 6))
#     for case, occupancies in total_occupancies_dict.items():
#         plt.plot(time, occupancies, label=case)
#     plt.xlabel('Time')
#     plt.ylabel('Total Occupancies Including Waiting Lists')
#     plt.title('Total Occupancies Over Time by Case Including Waiting Lists')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

#     # Plot recovery rates
#     plt.figure(figsize=(10, 6))
#     for case, rates in recovery_rates.items():
#         plt.plot(time, rates, label=case)
#     plt.xlabel('Time')
#     plt.ylabel('Recovery Rate')
#     plt.title('Recovery Rates Over Time')
#     plt.legend()
#     plt.ylim(0, 1)
#     plt.show()



def analyse_waiting_list(simulation_instances):
     # Define the bubbles of interest
    bubbles_of_interest = ["ad", "ap", "ad_ap", "esketamine", "ect"]

    for case, instances in simulation_instances.items():
        treatment_bubbles = {}
        
        # Initialize a dictionary to hold time series and waiting list sizes for each treatment bubble
        for instance in instances:
            time_series = instance.run_data["time"]
            for bubble, waiting_list in instance.run_data["waiting_list"].items():
                # Filter out bubbles not of interest
                if bubble not in bubbles_of_interest:
                    continue

                if bubble not in treatment_bubbles:
                    treatment_bubbles[bubble] = {"times": [], "sizes": []}
                
                treatment_bubbles[bubble]["times"].append(time_series)
                treatment_bubbles[bubble]["sizes"].append(waiting_list)
        
        # Create a new figure for each case
        plt.figure(figsize=(10, 5))
        for bubble, data in treatment_bubbles.items():
            # Aggregate time points and waiting list sizes across instances
            time_points = np.unique(np.concatenate(data["times"]))
            avg_sizes = np.zeros_like(time_points, dtype=float)

            # Compute the average waiting list size at each time point
            for i, time_point in enumerate(time_points):
                size_at_time = []
                for j, time_series in enumerate(data["times"]):
                    if time_point in time_series:
                        index = np.where(time_series == time_point)[0][0]
                        size_at_time.append(data["sizes"][j][index])
                avg_sizes[i] = np.mean(size_at_time) if size_at_time else np.nan

            plt.plot(time_points, avg_sizes, label=bubble)

        plt.title(f'Case: {case}')  # instances[0] is the key
        plt.xlabel('Time')
        plt.ylabel('Average Waiting List Size')
        plt.legend()
        plt.show()         

def analyse_waiting_list_compare_bubbles(simulation_instances):
    # Define the bubbles of interest
    bubbles_of_interest = ["ad", "ap", "ad_ap", "esketamine", "ect"]

    # Iterate over each bubble of interest
    for bubble in bubbles_of_interest:
        plt.figure(figsize=(10, 5))  # Create a new figure for each bubble

        # Iterate over each case to plot its data for the current bubble
        for case, instances in simulation_instances.items():
            time_series_aggregated = []
            waiting_lists_aggregated = []

            # Collect time series and waiting list sizes for the current bubble across all instances of the current case
            for instance in instances:
                if bubble in instance.run_data["waiting_list"]:
                    time_series = instance.run_data["time"]
                    waiting_list = instance.run_data["waiting_list"][bubble]

                    time_series_aggregated.extend(time_series)
                    waiting_lists_aggregated.extend(waiting_list)

            if not time_series_aggregated:  # Skip if there's no data for this bubble in the current case
                continue

            # Aggregate time points and waiting list sizes
            time_points = np.unique(time_series_aggregated)
            avg_sizes = np.zeros_like(time_points, dtype=float)

            # Compute the average waiting list size at each time point
            for i, time_point in enumerate(time_points):
                sizes_at_time = [waiting_lists_aggregated[j] for j, t in enumerate(time_series_aggregated) if t == time_point]
                avg_sizes[i] = np.mean(sizes_at_time) if sizes_at_time else np.nan

            # Plot the average waiting list size over time for the current bubble in the current case
            plt.plot(time_points, avg_sizes, label=case)

        plt.title(f'Bubble: {bubble}')
        plt.xlabel('Time')
        plt.ylabel('Average Waiting List Size')
        plt.legend()
        plt.show()

def calculate_parameters(simulation_instances):

    # Calculate employment rate for each of the cases

    employment_rates = []
    for _, instances in simulation_instances.items():
        employment = []
        for instance in instances:
            agents = instance.agents
            
            employment_count = 0
            for agent in agents:
                if agent.employed == True:
                    employment_count += 1

            employment.append(employment_count/len(agents))
        
        # Averag out the number of employment rates
        avg_employment_rate = np.mean(employment)
        employment_rates.append(avg_employment_rate)
    
    avg_employment_rate = np.mean(employment_rates)
    print(f"Employment Rate: {avg_employment_rate*100}%")


