import random

from utilities.config import read_config


class Leaf:

    def __init__(self, config_path, current_node_slug=None):

        if current_node_slug is None:
            self.current_node = "start"
        else:
            self.current_node = current_node_slug

        self.weights = read_config(config_path)

        self.episode_duration_dist = self.weights["episode_duration_dist"]
        self.symptom_severity_dist = self.weights["symptom_severity_dist"]
        self.functional_impairment_dist = self.weights["functional_impairment_dist"]
        self.treatment_failures_dist = self.weights["treatment_failures_dist"]

        self.symptom_severity = None
        self.episode_duration = None
        self.psychosis = None
        self.functional_impairment = None
        self.treatment_failures = None

        self.generate_attributes()
        self.madrs = self.calculate_madrs_score()

    def clean(self):
        self.symptom_severity = None
        self.episode_duration = None
        self.psychosis = None
        self.functional_impairment = None
        self.treatment_failures = None
        self.generate_attributes()
        self.madrs = self.calculate_madrs_score()



    def _choose_randomly(self, options, weights):
        return random.choices(options, weights=weights)[0]

    def generate_attributes(self):
        episode_duration_options = ['acute', 'subacute', 'chronic']
        symptom_severity_options = ['mild', 'moderate', 'severe', 'severe_psychosis']
        functional_impairment_options = ['mild', 'moderate', 'severe']
        treatment_failures_options = ['0', '1-2', '3+']

        self.episode_duration = self._choose_randomly(episode_duration_options, self.episode_duration_dist)
        self.symptom_severity = self._choose_randomly(symptom_severity_options, self.symptom_severity_dist)

        self.psychosis = self.symptom_severity == "severe_psychosis"
        if self.psychosis:
            self.symptom_severity = "severe"

        self.functional_impairment = self._choose_randomly(functional_impairment_options,
                                                           self.functional_impairment_dist)
        self.treatment_failures = self._choose_randomly(treatment_failures_options, self.treatment_failures_dist)

    def calculate_madrs_score(self):
        scoring_method = read_config("../../config/dm_trd_scoring.json")
        patient_score = 0

        # Calculate the score based on different attributes
        # (code for calculating scores based on episode_duration, symptom_severity, etc.)

        return patient_score
