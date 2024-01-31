import random

from core.agent import Agent


class PatientEsk(Agent):

    def __init__(self, environment, initial_bubble, episode_duration, symptom_severity, functional_impairment,
                 treatment_failures):
        super().__init__(environment=environment, initial_bubble=initial_bubble)


        # Set up the decision-making choices
        self.event_slug_dict = {
            "intake": lambda: (random.choices(["ad", "ad_ap", "ap"], weights=[0.60, 0.35, 0.05])[0], 'movement'),
            "ad": lambda: ('esketamine', 'movement'),
            "ad_ap": lambda: ('esketamine', 'movement'),
            "ap": lambda: ('esketamine', 'movement'),
            "esketamine": lambda: ('ect', 'movement'),
            "ect": lambda: ('ad', 'movement'),
            "remission": lambda: ('recovery', 'stay'),
            "relapse": lambda: ('intake', 'movement')
        }

        # DM_TRD Parameters
        trd_parameters = ["episode_duration", "symptom_severity", "functional_impairment", "treatment_failures"]
        self.episode_duration = episode_duration
        self.symptom_severity = symptom_severity

        if self.symptom_severity == "severe w/ psychosis":
            self.psychosis = True
            self.symptom_severity = "severe"
        else:
            self.psychosis = False

        self.functional_impairment = functional_impairment # not used, not tracked
        self.treatment_failures = treatment_failures # not used, not tracked

        self.employed = determine_employment(self.functional_impairment, self.symptom_severity)

    def __str__(self):
        return (f'{self.id} @ {self.current_bubble} | Episode: {self.episode_duration} '
                f'Symptom Severity: {self.symptom_severity} w/ Psychosis: {self.psychosis}')

    def update(self):
        self.employed = determine_employment(self.functional_impairment, self.symptom_severity)

def determine_employment(func_impairment, symptom_severity):
    # A patient is not employed if they have severe functional impairment or severe symptom severity
    if func_impairment == "severe" or symptom_severity == "severe" or func_impairment == "moderate":
        return False
    # In all other cases, the patient is employed
    return True
