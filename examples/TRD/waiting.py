import numpy as np


def determine_waiting_results(simulation_instances, stabilistion_point=300, cutoff_point=650):
    total_times = {}
    total_waiting = {}
    treatment_waiting = {}

    for case, instances in simulation_instances.items():
        case_times = []
        case_waiting = []
        case_treatment_waiting = []

        # Dictionary to store waiting times for each treatment
        treatment_waiting_times = {}

        for instance in instances:
            instance_times = []
            instance_waiting = []

            # Dictionary to store waiting times for each treatment in this instance
            instance_treatment_waiting_times = {}

            for agent in instance.agents:
                access = agent.medical_history[0]['time']
                if access < stabilistion_point or access > cutoff_point:
                    continue

                agent_total = determine_total_time(agent)
                instance_times.append(agent_total)

                agent_waiting = determine_waiting_time(agent)
                instance_waiting.append(agent_waiting)

                # Calculate waiting time for each treatment
                agent_treatment_waiting = determine_treatment_waiting(agent)
                for treatment, waiting_time in agent_treatment_waiting.items():
                    if treatment in instance_treatment_waiting_times:
                        instance_treatment_waiting_times[treatment].append(waiting_time)
                    else:
                        instance_treatment_waiting_times[treatment] = [waiting_time]

            mean_time, std_time = np.mean(instance_times), np.std(instance_times)
            case_times.append([mean_time, std_time])

            mean_waiting, std_waiting = np.mean(instance_waiting), np.std(instance_waiting)
            case_waiting.append([mean_waiting, std_waiting])

            # Aggregate waiting times for each treatment across all agents in this instance
            for treatment, waiting_times in instance_treatment_waiting_times.items():
                if treatment in treatment_waiting_times:
                    treatment_waiting_times[treatment].extend(waiting_times)
                else:
                    treatment_waiting_times[treatment] = waiting_times

        # Calculate mean and standard deviation for each treatment across all instances
        for treatment, waiting_times in treatment_waiting_times.items():
            mean_treatment = np.mean(waiting_times)
            std_treatment = np.std(waiting_times)
            if case in treatment_waiting:
                treatment_waiting[case][treatment] = [mean_treatment, std_treatment]
            else:
                treatment_waiting[case] = {treatment: [mean_treatment, std_treatment]}

        # Calculate mean and standard deviation for total times and waiting times
        mean_time, std_time = np.mean(case_times), np.std(case_times)
        total_times[case] = [mean_time, std_time]

        mean_waiting, std_waiting = np.mean(case_waiting), np.std(case_waiting)
        total_waiting[case] = [mean_waiting, std_waiting]

    # Print results for total times
    print("Total Times:")
    for case, (mean_time, std_time) in total_times.items():
        print(f"Case: {case} - Mean: {mean_time:.2f}, Std: {std_time:.2f}")

    # Print results for total waiting
    print("\nTotal Waiting:")
    for case, (mean_waiting, std_waiting) in total_waiting.items():
        print(f"Case: {case} - Mean: {mean_waiting:.2f}, Std: {std_waiting:.2f}")

    # Print results for treatment waiting
    print("\nTreatment Waiting:")
    for case, treatments in treatment_waiting.items():
        print(f"Case: {case}")
        for treatment, (mean_treatment, std_treatment) in treatments.items():
            print(f"- Treatment: {treatment} - Mean: {mean_treatment:.2f}, Std: {std_treatment:.2f}")


def determine_total_time(agent):
    events = agent.medical_history
    agent_duration = 0

    for i, event in enumerate(events):
        # This makes sure that the very last event is not counted (likely to be recovery)
        if i+1 < len(events):
            duration = events[i+1]['time'] - events[i]['time']
            agent_duration += duration

    return agent_duration

def determine_waiting_time(agent):
    events = agent.medical_history
    agent_waiting_duration = 0

    for i, event in enumerate(events):

        if i+1 < len(events):
            if event['type'] == "waiting":
                duration = events[i+1]['time'] - event['time']
                agent_waiting_duration += duration

    return agent_waiting_duration

# Modify the determine_treatment_waiting function to calculate waiting time for each treatment
def determine_treatment_waiting(agent):
    events = agent.medical_history
    treatment_waiting_times = {}

    current_treatment_start = None

    for event in events:
        if event['type'] == 'treatment_enter':  # Check if the event is the start of treatment
            current_treatment_start = event['time']
        elif current_treatment_start is not None:
            # Calculate the waiting time until the next event after entering the treatment
            treatment = event['data']['treatment']
            treatment_time = event['time'] - current_treatment_start

            if treatment in treatment_waiting_times:
                treatment_waiting_times[treatment].append(treatment_time)
            else:
                treatment_waiting_times[treatment] = [treatment_time]

            current_treatment_start = None  # Reset the current treatment start time

    # Calculate total waiting time for each treatment
    total_waiting_time_per_treatment = {}
    for treatment, waiting_times in treatment_waiting_times.items():
        total_waiting_time_per_treatment[treatment] = sum(waiting_times)

    return total_waiting_time_per_treatment
