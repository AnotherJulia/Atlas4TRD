from models import Environment, Event, EventTypesPR, EventTypesIO


def emergency_room_simulation():
    environment = Environment(name="emergency_room", t_end=10, dt=1)

    # lets add some bubbles to this environment

    ## Intake
    intake_in = Event(name="intake_in", eventIO_type=EventTypesIO.IN, eventPR_type=EventTypesPR.R, r=20)
    intake_wait = Event(name="waiting_room", eventIO_type=EventTypesIO.OUT, eventPR_type=EventTypesPR.R, r=18)
    intake_urgent = Event(name="immediate_help", eventIO_type=EventTypesIO.OUT, eventPR_type=EventTypesPR.R, r=2)

    environment.create_bubble(name="intake", events_in=[intake_in], events_out=[intake_wait, intake_urgent])

