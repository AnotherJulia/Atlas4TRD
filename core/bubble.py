import json
import uuid


class Bubble:

    def __init__(self, slug, description):
        self.id = uuid.uuid4()
        self.slug = slug
        self.description = description

        self.current_agents = []
        self.connections = []

    def __str__(self):
        return f"Bubble: {self.slug} - {self.description}"

    def get_occupancy(self):
        return len(self.current_agents)

    def add_agent(self, agent):
        self.current_agents.append(agent)

    def connect(self, other_bubble):
        # Connects bubble objects to others
        self.connections.append(other_bubble)


class StepBubble(Bubble):

    def __init__(self, slug, description, capacity, treatment_config):
        super().__init__(slug, description)
        self.capacity = capacity
        self.waiting_queue = []

        # Treatment specific parameters (non-changing)
        self.treatment_config = treatment_config
        self.treatment_parameters = self.read_config()
        self.duration = self.treatment_parameters['duration']
        self.cost = self.treatment_parameters['cost']
        self.response_rate = self.treatment_parameters['response_rate']
        self.remission_rate = self.treatment_parameters['remission_rate']
        self.relapse_rate = self.treatment_parameters['relapse_rate']
        self.suicide_rate = self.treatment_parameters['suicide_rate']
        self.treatment_adherence = self.treatment_parameters['treatment_adherence']
        self.mean_delta_madrs = self.treatment_parameters['mean_delta_madrs']
        self.sd_delta_madrs = self.treatment_parameters['sd_delta_madrs']

    def __str__(self):
        return f"Bubble: {self.slug} - {self.description} | {self.get_occupancy()}/{self.capacity} | Waiting: {self.waiting_queue}"

    def read_config(self):
        with open(self.treatment_config) as json_file:
            config = json.load(json_file)
            return config

    def add_agent(self, agent):
        # In a StepBubble, only add the agent if capacity allows
        if len(self.current_agents) < self.capacity:
            self.current_agents.append(agent)
        else:
            self.waiting_queue.append(agent)  # add the agent to waiting queue if bubble is full


class StateBubble(Bubble):

    def __init__(self, slug, description):
        super().__init__(slug, description)
