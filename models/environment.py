from models.event import Event
from models.bubble import Bubble
from models.agent import Agent, AgentTypes, PatientStates

from typing import List


class Environment:

    def __init__(self, name: str, t_end: int, dt: int):
        # identifier
        self.name: str = name

        # scheduler / time variables
        self.time: int = 0
        self.t_end: int = t_end
        self.dt: int = dt

        # overview of all the components
        self.bubbles: List[Bubble] = []
        self.events: List[Event] = []
        self.agents: List[Agent] = []


    def run(self):
        # Run the env simulation
        while not self.end_condition():
            self.time += self.dt
            self.tick()

    def end_condition(self):
        # Define the condition to end the simulation
        if (self.time >= self.t_end):
            return True
        else:
            return False


    # ------------------------------------------------ #
    # Instantiate new Components of the Environment    #
    # ------------------------------------------------ #

    ## Bubbles
    def create_bubble(self, name: str, events_in: List[Event], events_out: List[Event]):

        self.events.extend(events_in)
        self.events.extend(events_out)

        bubble = Bubble(name, events_in, events_out)
        self.bubbles.append(bubble)

    def add_bubble(self, bubble: Bubble):
        self.events.extend(bubble.events_in)
        self.events.extend(bubble.events_out)

        self.bubbles.append(bubble)

    ## Agents
    def create_agent(self):
        agent = Agent(AgentTypes.PATIENT, PatientStates.DEPRESSED)
        self.agents.append(agent)

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    ## Simulation Loop
    def tick(self):

        for bubble in self.bubbles:
            bubble.tick()

        for agent in self.agents:
            agent.tick()
