from typing import List
from Model import Connection, Agent

class Bubble:

    def __init__(self, name: str, capacity: int):
            """
            Initialize a Bubble object.

            Args:
                name (str): The name of the bubble.
                capacity (str): The capacity of the bubble.
            """
            self.name = name
            self.capacity = capacity
            
            self.occupation = 0 # empty on init

            self.connections: List[Connection] = []
            self.agents = []

    
    def add_agent(self, agent: Agent):
            """
            Adds an agent to the bubble.

            Parameters:
            agent (Agent): The agent to be added.

            Returns:
            bool: True if the agent was successfully added, False otherwise.
            """
            self.occupation = len(self.agents)

            if self.occupation < self.capacity:
                self.agents.append(agent)
                agent.apply_move(self)
                return True

            else:
                # No room in the current location
                return False
            
    def remove_agent(self, agent: Agent):
            """
            Removes the specified agent from the list of agents in the bubble.

            Args:
                agent (Agent): The agent to be removed.

            Returns:
                None
            """
            if agent in self.agents:
                 self.agents.remove(agent)

    
                 


