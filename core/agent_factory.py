from core.agent import Agent
import random


class AgentFactory:
    def __init__(self, amount: int):
        self.agents = []
        self.amount = amount

    def build(self):
        for i in range(self.amount):
            agent = Agent(id=i, initial_bubble="waiting", initial_depression_score=random.randint(6, 12))
            self.agents.append(agent)

        return self.agents
