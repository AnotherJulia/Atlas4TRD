from typing import TYPE_CHECKING

from Model import Environment


class Event:
    """
    Represents an event that can be executed in an environment.

    Attributes:
        description (str): Description of the event.
        time (int): Time at which the event executes.
        agent_id (int): ID of the agent connected to this event.
        disabled (bool): Flag indicating if the event is disabled.
    """

    # TODO : Possibly need to add some kind of ID to the events

    def __init__(self, description: str, time: int, agent_id: int):
        """
        Initializes a new instance of the Event class.

        Args:
            description (str): Description of the event.
            time (int): Time at which the event executes.
            agent_id (int): ID of the agent connected to this event.
        """

        self.description = description
        self.time = time
        self.agent_id = agent_id

        self.disabled = False

    def __str__(self):
        """
        Returns a string representation of the Event object.

        Returns:
            str: String representation of the Event object.
        """
        return f"Name: {self.description} | Agent: {self.agent_id}"

    def execute(self, environment: 'Environment'):
        """
        Executes the event on the specified environment.

        Args:
            environment (Environment): The environment in which the event is executed.
        """

        # Find the specific agent in the environment
        agent = next((agent for agent in environment.agents if agent.id == self.agent_id), None)

        if agent:
            # TODO: what does event do to the agent?
            pass

        else:
            # TODO: what happens if no agent is found?
            pass

    def destruct(self):
        """
        Disables the event.
        """
        self.disabled = True


class MoveAgentEvent(Event):
    """
    Event class representing the movement of an agent from one bubble to another.

    Attributes:
        description (str): Description of the move event.
        time (int): Time at which the event is executed by the environment.
        agent_id (int): ID of the agent associated with the move event.
        from_bubble (str): Slug of the bubble where the agent is currently located.
        to_bubble (str): Slug of the bubble where the agent is to be sent.
    """

    def __init__(self, description: str, time: int, agent_id: int, from_bubble: str, to_bubble: str):
        """
        Initializes a new MoveAgentEvent instance.

        Args:
            description (str): Description of the move event.
            time (int): Time at which the event is executed by the environment.
            agent_id (int): ID of the agent associated with the move event.
            from_bubble (str): Slug of the bubble where the agent is currently located.
            to_bubble (str): Slug of the bubble where the agent is to be sent.
        """
        super().__init__(description=description, time=time, agent_id=agent_id)

        self.from_bubble = from_bubble
        self.to_bubble = to_bubble

    def __str__(self):
        return f"Event: {self.description} | Agent: {self.agent_id} | Move from -> to: {self.from_bubble} -> {self.to_bubble}"

    def execute(self, environment: 'Environment'):
        """
        Executes the event by moving the agent from one bubble to another in the given environment.

        Args:
            environment (Environment): The environment in which the event is executed.

        Returns:
            None
        """
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
    """
    Represents an event that marks the end of an agent's path.

    Args:
        name (str): The name of the event.
        time (int): The time at which the event occurs.
        agent_id (int): The ID of the agent associated with the event.
    """
    def __init__(self, name: str, time: int, agent_id: int):
        super().__init__(name=name, time=time, agent_id=agent_id)

    def execute(self, environment: 'Environment'):
        """
        Executes the end agent event.

        Args:
            environment (Environment): The environment in which the event occurs.
        """
        # Find the specific agent in the environment
        agent = next((agent for agent in environment.agents if agent.id == self.agent_id), None)

        if agent:
            print(f"Agent {agent.id} has ended its path.")

        # Remove the agent from the environment or perform any other cleanup actions here
        environment.agents = [a for a in environment.agents if a.id != self.agent_id]

    