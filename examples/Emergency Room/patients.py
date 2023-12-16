
from Model import Agent, Bubble, Environment, Event, Factory, MoveAgentEvent, EndAgentEvent

class Patient(Agent):

    def __init__(self, id: int, start_bubble: Bubble):
        super().__init__(id, start_bubble)

        