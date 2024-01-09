import uuid


class Agent:

    def __init__(self, initial_bubble, environment):
        self.environment = environment
        self.id = uuid.uuid4()
        self.current_bubble = initial_bubble
        self.event_slug_dict = {}

    def __str__(self):
        return f'{self.id} @ {self.current_bubble}'

    def move_agent(self, bubble):
        self.current_bubble = bubble
        bubble.add_agent(agent=self)

    def decide_and_schedule_next_event(self, event_time=None):

        if event_time is None: event_time = self.environment.time
        next_event_slug, event_type = self.decide_next_event()

        if event_type == "stay":
            self.handle_stay_event(next_event_slug)
        elif event_type is not None:
            self.schedule_movement_event(next_event_slug, event_time)
        else:
            raise ValueError

    def handle_stay_event(self, next_event_slug):
        print(f"Agent {self.id} will stay in {self.current_bubble.slug}")

    def schedule_movement_event(self, next_event_slug, event_time):
        next_bubble = self.current_bubble.get_connected_bubbles(next_event_slug)
        if not next_bubble:
            print(f"Error: No connected bubble found for slug: {next_event_slug}")
            raise ValueError(f"No connected bubble found for slug: {next_event_slug}")
        print(f"Scheduling movement event for Agent {self.id} to {next_event_slug} at time {event_time}")

        from core import MovementEvent
        movement_event = MovementEvent(event_time, self, self.current_bubble, next_bubble)
        self.environment.schedule_event(movement_event)

    def decide_next_event(self):

        decision = self.event_slug_dict[self.current_bubble.slug]()
        print(f"Person {self.id} decided on next event: {decision}")
        return decision
