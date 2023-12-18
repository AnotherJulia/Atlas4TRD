import uuid


class Agent:

    def __init__(self, name, start_bubble):
        self.id = uuid.uuid4()
        self.name = name

        self.current_bubble = start_bubble

        self.history = []

    def determine_next_step(self):
        # Find an agents next step
        pass
