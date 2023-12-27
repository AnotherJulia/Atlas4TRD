import random
from utilities.config import read_config


class Factory:

    def __init__(self, config):
        self.config_file = config
        self.weights = read_config(config)
        self.environment = None

        self.episode_duration_dist = self.weights["episode_duration_dist"]
        self.symptom_severity_dist = self.weights["symptom_severity_dist"]
        self.functional_impairment_dist = self.weights["functional_impairment_dist"]
        self.treatment_failures_dist = self.weights["treatment_failures_dist"]

    def create_agent(self, start_bubble):
        from core import Agent

        episode_duration = random.choices(['acute', 'subacute', 'chronic'], weights=self.episode_duration_dist)[0]
        symptom_severity = random.choices(['mild', 'moderate', 'severe', 'severe_psychosis'], weights=self.symptom_severity_dist)[0]

        psychosis = symptom_severity == "severe_psychosis"
        if psychosis: symptom_severity = "severe"

        functional_impairment = random.choices(['mild', 'moderate', 'severe'], weights=self.functional_impairment_dist)[
            0]
        treatment_failures = random.choices(['0', '1-2', '3+'], weights=self.treatment_failures_dist)[0]

        return Agent(start_bubble, episode_duration, symptom_severity, psychosis, functional_impairment,
                     treatment_failures, self.environment)

    def create_agents(self, num_agents, start_bubble):
        agents = []
        for _ in range(num_agents):
            agent = self.create_agent(start_bubble)
            agents.append(agent)
        return agents

    def connect_environment(self, environment):
        self.environment = environment
