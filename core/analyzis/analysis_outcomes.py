class AnalysisOutcomes:
    def __init__(self, patient_id):

        self.patient_id = patient_id
        self.waiting_time = 0.0
        self.total_duration = 0.0
        self.n_relapse = 0

        self.relapses = {}
