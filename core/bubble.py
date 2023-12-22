import uuid


class Bubble:

    def __init__(self, name, capacity, type, duration, probabilities):
        self.id = uuid.uuid4()
        self.name = name
        self.type = type
        self.capacity = capacity
        self.occupancy = 0
        self.duration = duration
        self.probabilities = probabilities

        self.agents = []
        self.sub_bubbles = []
        self.next_connections = []

    def __str__(self):
        return f"Bubble: {self.id} - {self.name}"

    def add_agent(self, agent):
        self.agents.append(agent)

    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
            return True
        else:
            return False

    def find_occupancy(self):
        return len(self.agents)

    def has_agent(self, agent):
        return agent in self.agents

    def get_next_connection(self, agent):
        # this function should return the next connection the given agent should take
        pass
