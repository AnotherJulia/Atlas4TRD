from enum import Enum

class EventTypesIO(Enum):
    IN = 0,
    OUT = 1

class EventTypesPR(Enum):
    P = 0, # probability
    R = 1, # rate
    E = 2, # equation

class Event:

    def __init__(self, name: str, eventIO_type: EventTypesIO, eventPR_type: EventTypesPR, p: float = None, r: float = None):
        # Identifier
        self.name = name

        # Different event types for DES / ABM
        self.eventIO_type = eventIO_type
        self.eventPR_type = eventPR_type

        # Depends on the event type (are we using rate, or is it probability)
        self.p = p          #   Probability
        self.r = r          #   Rate

    def __str__(self):
        return f"Event | Name: {self.name} | Type: {self.eventIO_type} & {self.eventPR_type}"