from core_types import EffectType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.environment import Environment


class Event:
    def __init__(self, name: str = None, time: int = 0, agent_id: int = 0, effect_type: EffectType = None, effect=None):
        self.name = name  # What is the name of the agent (/ description)
        self.time = time
        self.agent_id = agent_id  # To what agent is this event connected

        self.effect_type = effect_type
        self.effect = effect  # This effect is an impact or consequence that the event has on the system

        self.disabled = False

    def __str__(self):
        return f"Name: {self.name} | Agent: {self.agent_id} | Effect: {self.effect_type} for {self.effect}"

    def execute(self, environment: 'Environment'):
        # Find the specific agent in the environment
        agent = next((agent for agent in environment.agents if agent.id == self.agent_id), None)

        if agent:
            agent.implement_effect(self.effect_type, self.effect)

    def destruct(self):
        self.disabled = True


class MoveAgentEvent(Event):
    def __init__(self, name: str, time: int, agent_id: int, from_bubble: str, to_bubble: str):
        super().__init__(name=name, time=time, agent_id=agent_id)

        self.from_bubble = from_bubble
        self.to_bubble = to_bubble

    def __str__(self):
        return f"Event: {self.name} | Agent: {self.agent_id} | Move from -> to: {self.from_bubble} -> {self.to_bubble}"

    def execute(self, environment: 'Environment'):
        agent = next((agent for agent in environment.agents if agent.id == self.agent_id), None)

        if agent:
            from_bubble = environment.bubbles[self.from_bubble]
            to_bubble = environment.bubbles[self.to_bubble]

            from_bubble.release_agent(agent)
            to_bubble.admit_agent(agent)

            # The moment an agent is admitted, it needs to find a new goal / event
            new_step = agent.find_next_step(environment=environment)
            if new_step is not None:
                environment.add_event(new_step)

            # After being executed, remove the event instance -- OPTION : keep this saved somewhere
            self.destruct()
        else:
            print("Cannot Identify the Agent from the environment: ", environment.name)


class EndAgentEvent(Event):
    def __init__(self, name: str, time: int, agent_id: int):
        super().__init__(name=name, time=time, agent_id=agent_id)

    def execute(self, environment: 'Environment'):
        # Find the specific agent in the environment
        agent = next((agent for agent in environment.agents if agent.id == self.agent_id), None)

        if agent:
            print(f"Agent {agent.id} has ended its path.")

        # Remove the agent from the environment or perform any other cleanup actions here
        environment.agents = [a for a in environment.agents if a.id != self.agent_id]