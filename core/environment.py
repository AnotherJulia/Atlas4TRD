class Environment:

    def __init__(self):
        self.bubbles = []
        self.connections = []


    def add_bubble(self, bubble):
        self.bubbles.append(bubble)

    def add_connection(self, connection):
        self.connections.append(connection)
