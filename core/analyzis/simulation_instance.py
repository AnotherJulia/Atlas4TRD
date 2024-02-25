
class SimulationInstance:

    def __init__(self, run_id, agents, environment, run_data=None):
        self.id = run_id
        self.agents = agents
        self.run_data = run_data
        self.environment = environment
        
        self.patient_profiles = self.create_patient_profiles()
        self.patient_logs = self.process_patient_logs()
        # self.patient_journeys = {}

    def retrieve_occupancies(self):
        if not self.run_data: 
            return None
        return self.run_data["bubble_occupancies"], self.run_data["time"]

    def retrieve_waiting_list(self):
        if not self.run_data:
            return None
        
        return self.run_data["waiting_list"], self.run_data["time"]

    def retrieve_n_patients(self):
        return len(self.agents)

    def create_patient_profiles(self):
        from core import PatientProfile

        profiles = {}

        for agent in self.agents:
            patient_id = agent.id
            initial_parameters = {
                "episode_duration": agent.episode_duration,
                "symptom_severity": agent.symptom_severity,
                "psychosis": agent.psychosis,
                "functional_impairment": agent.functional_impairment
            }
            demographics = {
                "employed": agent.employed
            }

            profiles[patient_id] = PatientProfile(patient_id, initial_parameters, demographics)

        return profiles

    def process_patient_logs(self):
        # Extract the agents medical logs and return them
        patient_logs = []

        for agent in self.agents:
            for log in agent.medical_history:
                patient_id = log["patient_id"]
                self.patient_profiles[patient_id].add_event(log)

        return patient_logs

    def printout(self):
        print("PATIENT PROFILES")
        print(self.patient_profiles.values())
