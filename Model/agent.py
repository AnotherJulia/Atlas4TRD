from Model import Bubble, Event, Environment

class Agent:

    def __init__(self, id: int, start_bubble: Bubble):
        self.id = id
        self.bubble = start_bubble

        self.bubble_history = [start_bubble]
        self.event_history = []

    def __str__(self):
        return f"Agent: {self.id} | Bubble: {self.bubble}"
    
    def apply_move(self, bubble: Bubble):
        self.bubble = bubble
        self.bubble_history.append(bubble)
    
    def apply_event(self, event: Event):
        self.event_history.append(event)

        # Let the event happen here
        self.apply_event_action() 
    
    def apply_event_action(self, event: Event):
        # This function will have to made in the child class, and will apply the different event actions based on the event
        pass

    def determine_next_step(self, environment: Environment):
        # this function has to be made in the child class, and will use the existing data to determine the 
        # next step in the simulation
        pass
