import random
from utilities.config import read_config


class Factory:

<<<<<<< HEAD
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
=======
    def __init__(self, config, agent_class_type):
        self.environment = None
        self.agent_class = agent_class_type

        # Set up the Factory
        self.weights = read_config(config)
        self.expected_weights = []
        self._generate_weights()

    def _generate_weights(self):
        self.expected_weights = self._extract_weight_names()

        for weight in self.expected_weights:
            dist_key = weight + "_dist"
            if dist_key in self.weights:
                setattr(self, weight, self.weights[dist_key])
            else:
                raise KeyError(f"{dist_key} not found in the weights configuration.")

    def _extract_weight_names(self):
        weight_names = []
        for key in self.weights.keys():
            if key.endswith("_dist"):
                weight_names.append(key[:-5])  # Remove '_dist' suffix
        return weight_names

    def create_agent(self, start_bubble):
        if self.environment is None:
            raise ValueError("Environment not yet attached to the factory. "
                             "Use factory.connect_environment(env) to connect")

        agent_params = {
            "initial_bubble": start_bubble,
            "environment": self.environment
        }

        # Add parameters from distribution
        for weight in self.expected_weights:
            # Get names and distributions from the configuration
            state_name = f"{weight}_states"
            dist_name = f"{weight}_dist"
            if state_name in self.weights and dist_name in self.weights:
                states = self.weights[state_name]
                dist = self.weights[dist_name]
                # Generate a state for each parameter from the distribution
                agent_params[weight] = random.choices(states, weights=dist, k=1)[0]

        return self.agent_class(**agent_params)

    def create_and_add_agents(self, bubble, environment):
        new_agent = self.create_agent(bubble)
        environment.agents.append(new_agent)
        bubble.add_agent(new_agent)
        new_agent.decide_and_schedule_next_event()
>>>>>>> origin/packaging/framework

    def create_agents(self, num_agents, start_bubble):
        agents = []
        for _ in range(num_agents):
            agent = self.create_agent(start_bubble)
            agents.append(agent)
        return agents

    def connect_environment(self, environment):
        self.environment = environment
