from collections import defaultdict
import numpy as np

class SimAnalyzer:

    def __init__(self, simulation_instances):
        self.simulation_instances = simulation_instances
    
    def print_logs(self, run_id=None):
        if run_id is None:
            for simulation in self.simulation_instances:
                simulation.printout()
        else:
            self.simulation_instances[run_id].printout()
        for instance in self.simulation_instances:
            print(instance.patient_profiles)
    
    def retrieve_simulation_instances(self, simulation_id):
        # Extract specific simulation instance corresponding with simulation ID
        return self.simulation_instances[simulation_id]
    
    # Running the analyzer for multiple simulation instances
    def run(self, plot=False):
        waiting_times = []
        n_relapse = []
        relapse_dicts = []
        total_durations = []
        final_states = []

        n_patients = []
   
        for index,_ in enumerate(self.simulation_instances):
    
            outcomes = self.run_analysis(run_id=index, plot=plot)
            n_patients.append(self.simulation_instances[index].retrieve_n_patients())
            waiting_times.append(outcomes.waiting_time)
            n_relapse.append(outcomes.n_relapse)
            relapse_dicts.append(outcomes.relapses)
            total_durations.append(outcomes.total_duration)
            final_states.append(outcomes.final_states)

            print(f"----- INSTANCE #{index} -----")
            print(f"Average waiting times (wk): {outcomes.waiting_time}")
            print("Average relapse events: ", outcomes.n_relapse)
            print(f"Average time in system (wk): {outcomes.total_duration}")

            print(final_states)
        
        avg_waiting_times = sum(waiting_times)/len(waiting_times)
        sd_waiting_times = np.std(waiting_times)

        avg_n_relapse = sum(n_relapse)/len(n_relapse)
        average_relapses = self.merge_and_average_dicts(relapse_dicts)

        print("----- SUMMARY -----")
        print(f"Average waiting times (wk): {avg_waiting_times} ({sd_waiting_times})")
        print("Average # relapse events: ", avg_n_relapse)

        if len(total_durations) != 0:
            avg_treatment_duration = sum(total_durations)/len(total_durations)
            sd_treatment_duration = np.std(total_durations)
            print(f"Average time in system (wk): {avg_treatment_duration} ({sd_treatment_duration})")
        else:
            print(f"Average time in the system (wk) : UNKNOWN")

        # State distributions
        avg_remission, avg_recovery, avg_in_treatment = self.find_percentages(final_states)
        print(f"Remission: {avg_remission}, Recovery: {avg_recovery}, In treatment: {avg_in_treatment}")

        category_distributions = {
                "remission": avg_remission,
                "recovery": avg_recovery,
                "in_treatment": avg_in_treatment
        }

        if plot:

            self.plot_bar_distribution(category_distributions, np.mean(n_patients))
            self.plot_n_relapse(average_relapses)


    # Run the analysis for a single simulation instance
    def run_analysis(self, run_id=0, plot=False):
        instance = self.simulation_instances[run_id]
        patients = instance.patient_profiles
        
        # Running the analysis for all the patients
        analysis_outcomes = self.analyze_patients(patients)
        waiting_times = []
        relapses = {}
        total_duration = []
        final_states = {
            "in_treatment": 0,
            "remission": 0,
            "recovery": 0
        }
  
        for outcome in analysis_outcomes:
            waiting_times.append(outcome.waiting_time)

            if outcome.final_state == "in_treatment": final_states["in_treatment"] += 1
            elif outcome.final_state == "remission": final_states["remission"] += 1
            elif outcome.final_state == "recovery": final_states["recovery"] += 1
            else: raise ValueError(f"ValueError: Outcome Final State not set up")
            
            if outcome.total_duration != 0:
                total_duration.append(outcome.total_duration)

            if outcome.n_relapse in relapses.keys():
                relapses[outcome.n_relapse] += 1
            else:
                relapses[outcome.n_relapse] = 1
        
        from core.analyzis import AnalysisOutcomes
        outcomes = AnalysisOutcomes(patient_id=None)
        
        avg_waiting_time = sum(waiting_times)/len(waiting_times)

        if len(total_duration) != 0:
            avg_treatment_duration = sum(total_duration)/len(total_duration)
        else:
            avg_treatment_duration = 0

        outcomes.total_duration = avg_treatment_duration
        outcomes.waiting_time = avg_waiting_time
        outcomes.n_relapse = int(self.average_relapses(relapses))
        outcomes.relapses = relapses
        outcomes.final_states = final_states
        
        if plot:
            self.plot_n_relapse(relapses)
            waiting_list, time = instance.retrieve_waiting_list()
            occupancies, time = instance.retrieve_occupancies()

            self.process_env_waiting_list(waiting_list, time, start_time=100)
            self.process_env_occupancies(occupancies, time, start_time=100)

        
        return outcomes
    
    def find_percentages(self, dicts):

        percentages = []

        # find percentages for each indiv dict
        for states in dicts:
            total_len = self.find_total_dict_length(states)
            p = {}

            for key, value in states.items():
                p[key] = value / total_len

            percentages.append(p)

        # lets find the averages
        
        remission = []
        recovery = []
        in_treatment = []

        for states in percentages:
            remission.append(states["remission"])
            recovery.append(states["recovery"])
            in_treatment.append(states["in_treatment"])

        avg_remission = np.mean(remission)
        # sd_remission = np.std(remission)

        avg_recovery = np.mean(recovery)
        # sd_recovery = np.std(recovery)

        avg_in_treatment = np.mean(in_treatment)
        # sd_in_treatment = np.std(in_treatment)

        return avg_remission, avg_recovery, avg_in_treatment

    
    def find_total_dict_length(self, dictionary):
        l = 0
        for _, value in dictionary.items():
            l += value
        return l

    @staticmethod
    def average_relapses(relapses):
        total = sum(int(relapse) * count for relapse, count in relapses.items())
        count = sum(relapses.values())
        average = total / count
        return average
    
    @staticmethod
    def merge_and_average_dicts(dicts):
        # Accumulate counts
        total_counts = defaultdict(int)
        count_per_key = defaultdict(int)
        
        for d in dicts:
            for k, v in d.items():
                total_counts[k] += v
                count_per_key[k] += 1
        
        # Compute averages
        avg_dict = {k: total_counts[k] / count_per_key[k] for k in total_counts}
        return avg_dict
   
    # Running analysis for all the patients
    def analyze_patients(self, patients):
        analysis_outcomes = []
        
        for _, patient_details in patients.items():
            out = self.analyze_patient(patient_details)
            analysis_outcomes.append(out)
        return analysis_outcomes
    
    # Running the analysis for a single patient
    @staticmethod
    def analyze_patient(patient):
        from core.analyzis import AnalysisOutcomes
        analysis_outcomes = AnalysisOutcomes(patient.patient_id)

        # find the total duration in the system (from intake to recovery)
        if (patient.event_logs[-1]["type"] == "recovery"):
            first_event_time = patient.event_logs[0]["time"]
            recovery_time = patient.event_logs[-1]["time"]
            total_duration = recovery_time - first_event_time
            print(f"Total Duration: {total_duration}")
            analysis_outcomes.total_duration = total_duration
        else:
            analysis_outcomes.total_duration = 0


        # print(f"Last Event: {patient.event_logs[-1]}")

        # find the final state of the patient
        if patient.event_logs[-1]["type"] == "movement_event" and patient.event_logs[-1]["data"]["state"] == "remission":
            final_state = "remission"
        elif patient.event_logs[-1]["type"] == "bubble-change" and patient.event_logs[-1]["data"]["bubble"] == "remission":
            final_state = "remission"
        elif patient.event_logs[-1]["type"] == "bubble-change" and patient.event_logs[-1]["data"]["bubble"] == "recovery":
            final_state = "recovery"
        else:
            final_state = "in_treatment"

        analysis_outcomes.final_state = final_state
         
        for index, event in enumerate(patient.event_logs):

            # Manage the waiting events -> adding to total waiting time
            if event["type"] == "waiting":
                if index != len(patient.event_logs)-1:
                    next_event = patient.event_logs[index+1]
                    waiting_time = next_event['time'] - event["time"]
                    analysis_outcomes.waiting_time += waiting_time
            if event["type"] == "relapse":
                analysis_outcomes.n_relapse += 1
        
        return analysis_outcomes
    
    def plot_n_relapse(self, relapses):
        import matplotlib.pyplot as plt
        keys = relapses.keys()
        values = relapses.values()
        
        # Create bar plot
        plt.bar(keys, values)
        plt.xticks(range(0, int(max(keys)) + 1))
        
        # Customize labels
        plt.xlabel('# of Relapse Events')
        plt.ylabel('Occurence')
        plt.title('Relapse Events')
        plt.show()


    def process_env_waiting_list(self, waiting_list, time, start_time=0):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,6))
        
        # print(f"Waiting List: {waiting_list}")
        cut_time = time[start_time:]

        for bubble, waiting_list in waiting_list.items():
            if np.sum(waiting_list) != 0:
                cut = waiting_list[start_time:]
                plt.plot(cut_time, cut, label=bubble)
        
        plt.legend()
        plt.title("Waiting Lists")
        plt.show()

    def process_env_occupancies(self, occupancies, time, start_time=0):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,6))
        cut_time = time[start_time:]

        for bubble, occupancies in occupancies.items():
            if np.sum(occupancies) != 0:
                cut = occupancies[start_time:]
                plt.plot(cut_time, cut, label=bubble)

        plt.legend()
        plt.title("Occupancies")
        plt.show()
    
    def plot_bar_distribution(self, percentages, n_patients):
        import matplotlib.pyplot as plt

        keys = percentages.keys()
        percentages = percentages.values()
        values = []

        for p in percentages:
            values.append(p*n_patients)
     
        plt.bar(keys, values)

        plt.xlabel("Categories")
        plt.ylabel("Number of patients")
        plt.title("Final states of Patients")
        plt.show()
        
