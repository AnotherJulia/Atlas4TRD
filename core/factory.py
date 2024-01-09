import random
from utilities.config import read_config


class Factory:

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

    def create_agents(self, num_agents, start_bubble):
        agents = []
        for _ in range(num_agents):
            agent = self.create_agent(start_bubble)
            agents.append(agent)
        return agents

    def connect_environment(self, environment):
        self.environment = environment
