from core import Bubble


class StepBubble(Bubble):

    def __init__(self, slug, description, capacity, treatment_config, depth, env):
        super().__init__(slug, description, depth, env)
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
        return f"Bubble: {self.slug} - {self.description} | {self.get_occupancy()}/{self.capacity} | Waiting: {self.get_waiting()}"

    def update(self):
        self.check_available_spots()

    def read_config(self):
        import json

        with open(self.treatment_config) as json_file:
            config = json.load(json_file)
            return config

    def add_agent(self, agent):
        from core import TreatmentEvent

        # Check if the bubble's capacity allows adding the agent
        if len(self.current_agents) < self.capacity:
            # Add the agent to the bubble
            super().add_agent(agent)

            # Schedule a TreatmentEvent
            event_time = self.environment.time + self.duration
            treatment_event = TreatmentEvent(event_time, agent, self)
            self.environment.schedule_event(treatment_event)
        else:
            # Add the agent to the waiting queue if capacity is full
            self.waiting_queue.append(agent)

    def check_available_spots(self):
        if len(self.current_agents) < self.capacity and len(self.waiting_queue) != 0:
            # let's allow the next agent from the waiting list into the bubble!
            next_agent = self.waiting_queue.pop(0)
            self.current_agents.append(next_agent)

    def get_waiting(self):
        return len(self.waiting_queue)
