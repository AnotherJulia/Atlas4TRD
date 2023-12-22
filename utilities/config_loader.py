import json
from core import Bubble, Connection

class ConfigLoader:

    def __init__(self, config_file):
        self.config_file = config_file
        self.bubbles = []
        self.connections = []

        self.config_data = []
        self.load_configuration()
        self.process_config()


    def load_configuration(self):
        """Load and parse the configuration file."""
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)

        except FileNotFoundError:
            print(f"Configuration file {self.config_file} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.config_file}.")

    def process_config(self):
        """
        Process the loaded config to obtain information about bubbles
        and connections in a more usable format.
        """
        # We will prepare two dictionaries: one for the bubbles and one for the connections

        # Read bubble information
        for key, value in self.config_data["bubbles"].items():
            bubble = Bubble(name=value['name'], type=value["type"], capacity=value['capacity'], duration=value['duration'], probabilities=value['probabilities'])
            self.bubbles.append(bubble)

        # Read connection information
        for key, value in self.config_data["connections"].items():
            from_bubble = None
            to_bubble = None

            for bubble in self.bubbles:
                if bubble.name == value['start_bubble']:
                    from_bubble = bubble
                elif bubble.name == value["end_bubble"]:
                    to_bubble = bubble

            connection = Connection(name=value["name"], from_bubble=from_bubble, to_bubble=to_bubble)
            self.connections.append(connection)