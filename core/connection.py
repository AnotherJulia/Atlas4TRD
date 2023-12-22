import uuid


class Connection:

    def __init__(self, start, end):
        self.id = uuid.uuid4()
        self.start = start
        self.end = end

        start.connect(end)
        # end.connect(start) # < removing this to make it 1 sided