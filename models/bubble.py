from models.event import Event, EventTypesIO, EventTypesPR

from typing import List


class Bubble:

    def __init__(self, name: str, events_in: List[Event], events_out: List[Event]):
        self.name = name
        self.slug = name.lower()

        self.events_in = []
        self.events_out = []

    def tick(self):
        # What happens at one instance of dt / one tick
        pass
