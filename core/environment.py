from core.config import SimulationConfig
from core.agent import Agent
from core.bubble import Bubble
from core.event import Event

from typing import List, Dict


class Environment:

    def __init__(self, config: SimulationConfig):
        self.name = config.name

        self.time = 0
        self.dt = config.dt
        self.running = False

        self.agents: List[Agent] = []
        self.events_queue: List[Event] = []
        self.bubbles: Dict[str, Bubble] = {}
        # self.resources: Dict[Resources] = {}

        self.data = {
            "time": [],
            "bubble_occupancies": {},
            "waiting_list": []
            # Add other data points as needed
        }

    def run(self, until, verbose=False):
        self.running = True

        while self.running and self.time < until:
            if verbose: self.print_sim_progress()

            self.process_events_up_to(self.time)

            self.collect_data()
            self.time += self.dt

        self.running = False

    def print_sim_progress(self):
        print(f"t={self.time} -------")

        print("-- Agents -- ")
        for agent in self.agents:
            print(agent)

        print("-- Bubbles -- ")
        for name, bubble in self.bubbles.items():
            print(bubble)

        print("-- Events -- ")
        for event in self.events_queue:
            if not event.disabled: print(event)

    def process_events_up_to(self, time_limit):
        while self.events_queue and self.events_queue[0].time <= time_limit:
            next_event: Event = self.events_queue.pop(0)
            # print("Executing Event: ", next_event.name)
            next_event.execute(environment=self)

    def schedule_event(self, event: Event):
        self.add_event(event)

    def add_event(self, event: Event):
        self.events_queue.append(event)
        self.events_queue.sort(key=lambda x: x.time)

    def add_agent(self, agent: Agent):
        self.agents.append(agent)
        self.add_event(agent.find_next_step(environment=self))

        if agent.bubble in self.bubbles:
            self.bubbles[agent.bubble].admit_agent(agent)
        else:
            print(f"Error: Bubble '{agent.bubble}' not found")

    def remove_agent(self, agent: Agent):
        if agent in self.agents:
            self.agents.remove(agent)
        else:
            print(f"Unable to find agent with id '{agent.id}' in the environment")

    def add_bubble(self, bubble: Bubble):
        self.bubbles[bubble.name] = bubble
        self.data["bubble_occupancies"][bubble.name] = []

    # DATA ANALYSIS AND VISUALISATION
    def collect_data(self):
        self.data['time'].append(self.time)

        for name, bubble in self.bubbles.items():
            occupancy = bubble.get_occupancy()
            self.data['bubble_occupancies'][name].append(occupancy)

        # Collect other data as required
        # TODO: ADD WAITING LIST
