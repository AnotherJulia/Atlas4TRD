import uuid


class Agent:

    def __init__(self, initial_bubble, environment):
        self.environment = environment
        self.id = uuid.uuid4()
        self.current_bubble = initial_bubble
        self.event_slug_dict = {}

        self.num_treatments_tried = 0
        self.num_relapses = 0

        self.medical_history = []

        self.total_waiting_time = 0  # Initialize total waiting time
        self.start_time = environment.time

    def __str__(self):
        return f'{self.id} @ {self.current_bubble}'

    # def move_agent(self, bubble):
    #     self.current_bubble = bubble
    #     bubble.add_agent(agent=self)

    def add_to_medical_history(self, event_type, event_data, time):
        event_with_id = {
            "patient_id": self.id,
            "type": event_type,
            "data": event_data,
            "time": time
        }
        self.medical_history.append(event_with_id)

        if event_type == "treatment_enter":
            self.num_treatments_tried += 1
            # Check for the most recent 'waiting' event before this 'treatment_enter' event
            waiting_events = [event for event in self.medical_history if event['type'] == 'waiting']
            if waiting_events:
                last_waiting_event = waiting_events[-1]
                waiting_time = time - last_waiting_event['time']
                self.total_waiting_time += waiting_time

        if event_type == "relapse":
            self.num_relapses += 1


    def decide_and_schedule_next_event(self, event_time=None):

        if event_time is None:
            event_time = self.environment.time
        next_event_slug, event_type = self.decide_next_event()

        if event_type == "stay":
            self.handle_stay_event()
        elif event_type is not None:
            self.schedule_movement_event(next_event_slug, event_time)
        else:
            raise ValueError

    def handle_stay_event(self):
        # print(f"Agent {self.id} will stay in {self.current_bubble.slug}")
        pass

    def schedule_movement_event(self, next_event_slug, event_time):
        next_bubble = self.current_bubble.get_connected_bubbles(next_event_slug)
        if not next_bubble:
            raise ValueError(f"No connected bubble found for slug: {next_event_slug}")

        from core import MovementEvent
        movement_event = MovementEvent(event_time, self, self.current_bubble, next_bubble)

        # print(f"Scheduling movement event for Agent {self.id} to {next_event_slug} at time {event_time}")
        self.environment.schedule_event(movement_event)

    def decide_next_event(self):
        decision = self.event_slug_dict[self.current_bubble.slug]()
        # print(f"Person {self.id} decided on next event: {decision}")
        return decision
