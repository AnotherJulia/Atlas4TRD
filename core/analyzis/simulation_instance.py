
class SimulationInstance:

    def __init__(self, run_id, agents):
        self.id = run_id
        self.agents = agents
        self.patient_profiles = self.create_patient_profiles()

        self.patient_logs = self.process_patient_logs()
        self.patient_journeys = {}

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

    # def process_patient_log(self, log):
    #     patient_id = self.extract_patient_id(log)
    #     if patient_id not in self.patient_journeys:
    #         self.patient_journeys[patient_id] = PatientJourney(patient_id)
    #     self.patient_journeys[patient_id].add_event(log)

    def printout(self):
        print("PATIENT PROFILES")
        print(self.patient_profiles.values())
