from core import Event


class MovementEvent(Event):
    def __init__(self, time, agent, start_bubble, end_bubble):
        super().__init__(time)
        self.agent = agent
        self.start_bubble = start_bubble        # Bubble object
        self.end_bubble = end_bubble            # Bubble Object

    def __repr__(self):
        return f"Movement Event({self.time}) - {self.start_bubble} to {self.end_bubble}"

    def process(self, environment):
        from core import StateBubble, MovementEvent

        if self.agent.current_bubble != self.start_bubble:
            raise ValueError(f"Agent {self.agent.id} is not in the expected start bubble. "
                             f"Start {self.start_bubble.slug} | Current {self.agent.current_bubble.slug}")

        # Move the agent from start to end bubble
        self.start_bubble.remove_agent(self.agent)
        self.end_bubble.add_agent(self.agent)
        self.agent.current_bubble = self.end_bubble

        # Handling different types of StateBubbles
        if isinstance(self.end_bubble, StateBubble):
            if self.end_bubble.slug == "intake":
                # Determine the next step for the agent
                self.agent.decide_and_schedule_next_event()

            elif self.end_bubble.slug == "remission":
                # Keep the agent in remission, no further action needed
                pass

            elif self.end_bubble.slug == "relapse":
                # Schedule a movement event back to intake
                intake_bubble = next(bubble for bubble in environment.bubbles if bubble.slug == "intake")
                movement_event = MovementEvent(self.time + environment.dt, self.agent, self.end_bubble, intake_bubble)
                environment.schedule_event(movement_event)
