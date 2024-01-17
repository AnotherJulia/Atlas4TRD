class PatientProfile:
    def __init__(self, patient_id, initial_parameters, demographics):
        self.patient_id = patient_id
        self.initial_parameters = initial_parameters
        self.demographics = demographics

        self.event_logs = []

    def __repr__(self):
        return (f"Patient ID: {self.patient_id} || Initial parameters: {self.initial_parameters} "
                f"|| Demographics: {self.demographics} || Events: {self.event_logs}")

    def __str__(self):
        return (f"Patient ID: {self.patient_id} || Initial parameters: {self.initial_parameters} "
                f"|| Demographics: {self.demographics}")

    def add_event(self, log):
        self.event_logs.append(log)
