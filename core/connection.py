import uuid


class Connection:
    def __init__(self, from_bubble, to_bubble):
        self.id = uuid.uuid4()
        self.from_bubble = from_bubble
        self.to_bubble = to_bubble
