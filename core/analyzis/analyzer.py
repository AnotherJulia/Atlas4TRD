

class SimAnalyzer:

    def __init__(self, simulation_instances):
        self.simulation_instances = simulation_instances

    def print_logs(self, run_id=None):
        # if run_id is None:
        #     for simulation in self.simulation_instances:
        #         simulation.printout()
        # else:
        #     self.simulation_instances[run_id].printout()

        for instance in self.simulation_instances:
            print(instance.patient_profiles)

    def retrieve_simulation_instances(self, simulation_id):
        # Extract specific simulation instance corresponding with simulation ID
        return self.simulation_instances[simulation_id]

    def analyze_specific_patient(self, patient_id):
        patient_data = []

        for instance in self.simulation_instances:
            if patient_id in instance.patient_journeys:
                patient_data.append(instance.patient_journeys[patient_id])

        return self.aggregate_patient_data(patient_data)

    def aggregate_patient_data(self, patient_data):
        aggregated = {
            "average_treatment_duration": 0,
            "average_waiting_time": 0,
            "total_events": 0,
            # ... other metrics you want to calculate
        }

        total_treatment_duration = 0
        total_waiting_time = 0
        total_events = 0

        for journey in patient_data:
            total_treatment_duration += sum(journey.treatment_durations)
            total_waiting_time += sum(journey.waiting_times)
            total_events += len(journey.events)

        num_journeys = len(patient_data)
        if num_journeys > 0:
            aggregated["average_treatment_duration"] = total_treatment_duration / num_journeys
            aggregated["average_waiting_time"] = total_waiting_time / num_journeys
            aggregated["total_events"] = total_events

        return aggregated

    def run(self):
        pass