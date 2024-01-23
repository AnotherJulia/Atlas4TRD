from collections import defaultdict

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
    def run(self):
        waiting_times = []
        n_relapse = []
        relapse_dicts = []
        for index, instance in enumerate(self.simulation_instances):
            outcomes = self.run_analysis(run_id=index)
            waiting_times.append(outcomes.waiting_time)
            n_relapse.append(outcomes.n_relapse)
            relapse_dicts.append(outcomes.relapses)
            print(f"----- INSTANCE #{index} -----")
            print("Average waiting times: ", outcomes.waiting_time)
            print("Average relapse events: ", outcomes.n_relapse)
        avg_waiting_times = sum(waiting_times)/len(waiting_times)
        avg_n_relapse = sum(n_relapse)/len(n_relapse)
        average_relapses = self.merge_and_average_dicts(relapse_dicts)

        print("----- SUMMARY -----")
        print("Average waiting times: ", avg_waiting_times)
        print("Average # relapse events: ", avg_n_relapse)
        self.plot_n_relapse(average_relapses)

    def run_analysis(self, run_id=0, plot=False):
        instance = self.simulation_instances[run_id]
        patients = instance.patient_profiles
        # run general analysis
        n_patients = len(patients)
        # print("n_patients: ", n_patients)
        # run patient by patient analysis
        analysis_outcomes = self.analyze_patients(patients)
        waiting_times = []
        relapses = {}
        for outcome in analysis_outcomes:
            waiting_times.append(outcome.waiting_time)
            if outcome.n_relapse in relapses.keys():
                relapses[outcome.n_relapse] += 1
            else:
                relapses[outcome.n_relapse] = 1
        from core.analyzis import AnalysisOutcomes
        outcomes = AnalysisOutcomes(patient_id=None)
        # avg_relapse = sum(relapses)/len(relapses)
        avg_waiting_time = sum(waiting_times)/len(waiting_times)
        outcomes.waiting_time = avg_waiting_time
        outcomes.n_relapse = self.average_relapses(relapses)
        outcomes.relapses = relapses
        if plot:
            self.plot_n_relapse(relapses)
        return outcomes
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
    def analyze_patients(self, patients):
        analysis_outcomes = []
        for patient_id, patient_details in patients.items():
            out = self.analyze_patient(patient_details)
            analysis_outcomes.append(out)
        return analysis_outcomes
    @staticmethod
    def analyze_patient(patient):
        from core.analyzis import AnalysisOutcomes
        analysis_outcomes = AnalysisOutcomes(patient.patient_id)
        for index, event in enumerate(patient.event_logs):
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