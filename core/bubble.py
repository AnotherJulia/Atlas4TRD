from core.agent import Agent


class Bubble:
    # TODO : ADD CONNECTIONS TO AND FROM OTHER BUBBLES FOR VALIDATION OF MOVE EVENTS

    def __init__(self, name: str, capacity):
        self.name = name
        self.capacity = capacity
        self.current_agents = []

        self.connections = []

    def __str__(self):
        return f"Bubble: {self.name} | Occupancy: {self.get_occupancy()} / {self.capacity}"

    def admit_agent(self, agent: Agent):
        # If there is room in the bubble, then add the patient and move them
        if self.capacity is None: # No wait list to automatically allow moving in
            self.current_agents.append(agent)
            agent.move_to(self.name)
            return True

        if len(self.current_agents) < self.capacity:
            self.current_agents.append(agent)
            agent.move_to(self.name)
            return True

        # Otherwise return that the patient couldn't be admitted
        return False

    def release_agent(self, agent):
        if agent in self.current_agents:
            self.current_agents.remove(agent)

    def get_occupancy(self):
        return len(self.current_agents)