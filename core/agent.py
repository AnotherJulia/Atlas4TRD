import uuid
import random


class Agent:

    def __init__(self, current_bubble, episode_duration, symptom_severity, psychosis, functional_impairment,
                 treatment_failures, environment):
        self.environment = environment
        self.id = uuid.uuid4()
        self.current_bubble = current_bubble
        self.history = []  # TODO : Add a TreatmentHistory object to simply store that here

        # DM_TRD Parameters
        self.episode_duration = episode_duration
        self.symptom_severity = symptom_severity
        self.psychosis = psychosis
        self.functional_impairment = functional_impairment
        self.treatment_failures = treatment_failures

    def __str__(self):
        return f'{self.id} @ {self.current_bubble} | Episode: {self.episode_duration} Symptom Severity: {self.symptom_severity} w/ Psychosis: {self.psychosis}'

    def move_agent(self, bubble):
        self.current_bubble = bubble
        bubble.add_agent(agent=self)

    def decide_and_schedule_next_event(self, event_time=None):
        from core import MovementEvent

        print(f"Agent {self.id} deciding next event from {self.current_bubble.slug}")

        if event_time is None: event_time = self.environment.time
        next_event_slug, event_type = self.decide_next_event()

        print(f"Agent {self.id} decided on event type: {event_type}")

        if event_type == "stay":
            print(f"Agent {self.id} will stay in {self.current_bubble.slug}")
            return

        # Debug: Print next bubble
        print(f"Agent {self.id} is moving to bubble: {next_event_slug}")

        # Find the next bubble based on the slug
        next_bubble = self.current_bubble.get_connected_bubbles(next_event_slug)
        if not next_bubble:
            print(f"Error: No connected bubble found for slug: {next_event_slug}")
            raise ValueError(f"No connected bubble found for slug: {next_event_slug}")

        # Schedule a movement event to the next bubble
        print(f"Scheduling movement event for Agent {self.id} to {next_event_slug} at time {event_time}")
        movement_event = MovementEvent(event_time, self, self.current_bubble, next_bubble)
        self.environment.schedule_event(movement_event)


    def decide_next_event(self):
        # Check the current bubble and decide the next step

        print(f"Agent {self.id} is in bubble: {self.current_bubble.slug}")
        global decision

        if self.current_bubble.slug == "intake":
            next_event_slug = random.choices(["ad", "ad_ap", "ap"], weights=[0.33, 0.33, 0.34])[0]
            decision = (next_event_slug, 'movement')
        elif self.current_bubble.slug == "ad" or self.current_bubble.slug == "ad_ap" or self.current_bubble.slug == "ap":
            # After augmented therapies treatment, move to esketamine
            decision = ('esketamine', 'movement')
        elif self.current_bubble.slug == "esketamine":
            # After esketamine, move to ect
            decision = ('ect', 'movement')
        elif self.current_bubble.slug == "ect":
            # After ect, go back to intake for reassessment
            decision = ('ad', 'movement')
        elif self.current_bubble.slug == "remission":
            # If in remission, stay there
            decision = ('stay', 'stay')
        elif self.current_bubble.slug == "relapse":
            # If relapsed, go back to intake
            decision = ('intake', 'movement')


        print(f"Agent {self.id} decided on next event: {decision}")
        return decision
