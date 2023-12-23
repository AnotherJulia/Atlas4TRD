from core import Event


class TreatmentEvent(Event):
    def __init__(self, time, agent, treatment_bubble):
        super().__init__(time)
        self.agent = agent
        self.treatment_bubble = treatment_bubble

    def process(self, environment):
        import random

        event_time = self.time + self.treatment_bubble.duration

        # Determine outcome of treatment
        remission_chance, response_chance, relapse_chance = (
            self.treatment_bubble.remission_rate,
            self.treatment_bubble.response_rate,
            self.treatment_bubble.relapse_rate
        )

        if random.random() < remission_chance:
            # Agent goes into remission
            next_bubble_slug = "remission" if random.random() >= relapse_chance else "relapse"
        elif random.random() < response_chance:
            # Agent responds but doesn't go into remission, tries same treatment again
            next_bubble_slug = self.treatment_bubble.slug
        else:
            # Agent doesn't respond, needs new treatment
            next_bubble_slug, _ = self.agent.decide_next_event()

        if next_bubble_slug == "stay":
            # If the next action is to stay, do not schedule a movement event
            return

        # Find the next bubble and proceed with scheduling a movement event
        next_bubble = self.find_next_bubble(next_bubble_slug, environment)
        if next_bubble is None:
            raise ValueError(f"No bubble found with slug '{next_bubble_slug}'")

        self.schedule_movement_event(next_bubble, event_time, environment)

    def find_next_bubble(self, bubble_slug, environment):
        for bubble in environment.bubbles:
            if bubble.slug == bubble_slug:
                return bubble
        raise ValueError(f"No bubble found with slug '{bubble_slug}'")

    def schedule_movement_event(self, next_bubble, event_time, environment):
        from core import MovementEvent
        movement_event = MovementEvent(event_time, self.agent, self.treatment_bubble, next_bubble)
        environment.schedule_event(movement_event)