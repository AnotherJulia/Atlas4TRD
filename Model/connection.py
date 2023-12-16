from Model import Bubble, MoveAgentEvent

class Connection:

    def __init__(self, name: str, start: Bubble, end: Bubble):
        self.name = name
        self.start = start
        self.end = end

    def check_move_event(self, event: MoveAgentEvent):
        if (event.from_bubble == self.start and event.to_bubble == self.end):
            return True
        else:
            return False

