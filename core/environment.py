import heapq
import uuid


class Environment:

    def __init__(self, name, dt):
        self.id = uuid.uuid4()
        self.name = name

        self.time = 0
        self.dt = dt

        self.bubbles = []
        self.agents = []
        self.connections = []
        self.event_queue = []

        self.data = {
            "time": [],
            "bubble_occupancies": {},
            "waiting_list": []
        }

    def run(self, until, verbose=False):
        if verbose: self.print_progress()

        self.process_events_up_to(self.time)
        self.collect_data()

        self.time += self.dt

    def print_progress(self):
        pass

    def add_bubble(self, bubble):
        self.bubbles.append(bubble)

    def add_agent(self, agent):
        self.agents.append(agent)

    def add_connection(self, from_bubble, to_bubble):
        from core import Connection
        connection = Connection(from_bubble, to_bubble)
        self.connections.append(connection)

    def find_available_connections(self, origin_bubble, type):
        connections = []
        for bubble in self.bubbles:
            if bubble.id == origin_bubble.id and bubble.type == type:
                connections.append(bubble)

        return connections

    # def connect_bubbles(self, from_bubble, to_bubble):
    #     if from_bubble in self.bubbles and to_bubble in self.bubbles:
    #         self.connections.append((from_bubble, to_bubble))
    #     else:
    #         raise ValueError("Invalid connection. Ensure bubbles are part of environment before connecting")

    def process_events_up_to(self, time_limit):
        from .event import Event
        while self.event_queue and self.event_queue[0].time <= time_limit:
            next_event: Event = self.event_queue.pop(0)
            # print("Executing Event: ", next_event.name)
            next_event.execute(environment=self)

    def schedule_event(self, event):
        heapq.heappush(self.event_queue, event)

    def collect_data(self):
        self.data['time'].append(self.time)
