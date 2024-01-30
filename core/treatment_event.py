from core import Event


class TreatmentEvent(Event):
    def __init__(self, time, agent, treatment_bubble):
        super().__init__(time)
        self.agent = agent
        self.treatment_bubble = treatment_bubble

    def __repr__(self):
        return f"Treatment Event({self.time}) @ {self.treatment_bubble}"

    def process(self, environment):
        import random

        event_time = self.time + self.treatment_bubble.duration

        event_data = {
            "treatment": self.treatment_bubble.slug,
        }

        # Determine outcome of treatment
        remission_chance, response_chance, relapse_chance = (
            self.treatment_bubble.remission_rate,
            self.treatment_bubble.response_rate,
            self.treatment_bubble.relapse_rate
        )
        
        event_data["relapse_rate"] = relapse_chance
   
        random_number = random.random()
        if random_number < remission_chance:
            next_bubble_slug = "remission"
            event_data["state"] = "remission"
        elif random_number < response_chance:
            event_data["state"] = "response"
            self.schedule_treatment_event(event_time, environment)
            return
        else:
            event_data["state"] = "no_response"
            next_bubble_slug, _ = self.agent.decide_next_event()

        if next_bubble_slug == "stay":
            # If the next action is to stay, do not schedule a movement event
            return

        # Find the next bubble and proceed with scheduling a movement event
        next_bubble = self.find_next_bubble(next_bubble_slug, environment)
        if next_bubble is None:
            raise ValueError(f"No bubble found with slug '{next_bubble_slug}'")

        self.agent.add_to_medical_history(event_type="treatment_end", event_data=event_data, time=event_time)
        self.schedule_movement_event(next_bubble, event_time, environment)

    @staticmethod
    def find_next_bubble(bubble_slug, environment):
        for bubble in environment.bubbles:
            if bubble.slug == bubble_slug:
                return bubble
        raise ValueError(f"No bubble found with slug '{bubble_slug}'")

    def schedule_movement_event(self, next_bubble, event_time, environment):
        from core import MovementEvent
        movement_event = MovementEvent(event_time, self.agent, self.treatment_bubble, next_bubble)
        environment.schedule_event(movement_event)

    def schedule_treatment_event(self, event_time, environment):
        treatment_event = TreatmentEvent(event_time, self.agent, self.treatment_bubble)
        environment.schedule_event(treatment_event)
