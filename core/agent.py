import uuid
import random


class Agent:

    def __init__(self, current_bubble, episode_duration, symptom_severity, psychosis, functional_impairment,
                 treatment_failures):
        self.id = uuid.uuid4()
        self.current_bubble = current_bubble
        self.history = []

        # DM_TRD Parameters
        self.episode_duration = episode_duration
        self.symptom_severity = symptom_severity
        self.psychosis = psychosis
        self.functional_impairment = functional_impairment
        self.treatment_failures = treatment_failures

    def __str__(self):
        return f'{self.id} @ {self.current_bubble} | Episode: {self.episode_duration} Symptom Severity: {self.symptom_severity} w/ Psychosis: {self.psychosis}'

