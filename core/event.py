import heapq
import uuid


class Event:
    def __init__(self, time, name=None):
        self.id = uuid.uuid4()
        self.time = time
        self.name = name or self.__class__.__name__

    def __lt__(self, other):
        return self.time < other.time

    def execute(self, environment):
        raise NotImplementedError("Subclasses should implement this!")


class ArrivalEvent(Event):
    def __init__(self, time, agent, bubble):
        super().__init__(time)
        self.agent = agent
        self.bubble = bubble

    def execute(self, environment):
        environment.add_agent(self.agent, self.bubble)


class DepartureEvent(Event):
    def __init__(self, time, agent):
        super().__init__(time)
        self.agent = agent

    def execute(self, environment):
        environment.remove_agent(self.agent)


class MoveEvent(Event):
    def __init__(self, time, agent, from_bubble, to_bubble):
        super().__init__(time)
        self.agent = agent
        self.from_bubble = from_bubble
        self.to_bubble = to_bubble

    def execute(self, environment):
        if self.from_bubble.has_agent(self.agent):  # You'll need to implement has_agent in Bubble class
            self.from_bubble.remove_agent(self.agent)  # Implement remove_agent in Bubble class
            self.to_bubble.add_agent(self.agent)  # Implement add_agent in Bubble class
