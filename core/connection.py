import uuid


class Connection:
    def __init__(self, name, from_bubble, to_bubble):
        self.id = uuid.uuid4()
        self.name = name
        self.from_bubble = from_bubble
        self.to_bubble = to_bubble
