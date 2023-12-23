class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

    def process(self, environment):
        pass  # To be implemented in child class

    def update(self):
        pass  # To be implemented in child class if necessary





