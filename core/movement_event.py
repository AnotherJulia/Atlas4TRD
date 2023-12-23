from core import Event


class MovementEvent(Event):
    def __init__(self, time, agent, start_bubble, end_bubble):
        super().__init__(time)
        self.agent = agent
        self.start_bubble = start_bubble        # Bubble object
        self.end_bubble = end_bubble            # Bubble Object

    def process(self, environment):
        from core import StepBubble, TreatmentEvent, StateBubble, MovementEvent

        print(f"Processing MovementEvent: Agent {self.agent.id} from {self.start_bubble.slug} to {self.end_bubble.slug}")

        if self.agent.current_bubble != self.start_bubble:
            print(
                f"Warning: Agent {self.agent.id} is not in the expected start bubble {self.start_bubble.slug}. Current bubble: {self.agent.current_bubble.slug}")
            # Optionally, reschedule the event or take other appropriate actions
            return

        # Move the agent from start to end bubble
        self.start_bubble.remove_agent(self.agent)
        self.end_bubble.add_agent(self.agent)
        self.agent.current_bubble = self.end_bubble

        # If the end bubble is a StepBubble, schedule a treatment event
        if isinstance(self.end_bubble, StepBubble):
            treatment_start_time = self.time + environment.dt
            treatment_event = TreatmentEvent(treatment_start_time, self.agent, self.end_bubble)
            environment.schedule_event(treatment_event)

        # Handling different types of StateBubbles
        elif isinstance(self.end_bubble, StateBubble):
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
