import uuid


class Bubble:

    def __init__(self, name, capacity, type):
        self.id = uuid.uuid4()
        self.name = name
        self.agents = []
        self.sub_bubbles = []
        self.capacity = capacity
        self.occupancy = 0

        self.type = type

        self.next_connections = []

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
