
class Environment:
    """
    Basic Environment class, that contains all the required functions to run the simulation.
    It keeps track of time, steps, existing bubbles, the events queue and the agents, and stores data for each timestep
    """

    def __init__(self, name: str, dt: int):
        """
        Initializes the Environment object.

        :param name: Environment name
        :param dt: Timestep
        """

        self.name = name
        self.time = 0
        self.dt = dt

        self.running = False
        self.dev = True

        self.bubbles = {}
        self.events_queue = []
        self.agents = []

        self.data = {
            "time": [],
            "bubble_occupancies": {},
            "waiting_list": {}
        }

    def __str__(self):
        """
        Returns a string representation of the Environment object.
        """
        return f"Name: {self.name} | Timestep: {self.dt}"

    def run(self, until: int, verbose=False):
        """
        Runs the entire simulation.

        :param until: Time until which to simulate
        :param verbose: Should the program output progress information
        :return: None
        """

        self.running = True

        while self.running and self.time < until:
            if verbose:
                self.print_progress()

            self.process_events_up_to(self.time)
            self.collect_data()

            self.time += self.dt

    def print_progress(self):
        """
        Prints the simulation progress.

        :return: None
        """
        print(f"----- Time: {self.time} -----")

    def process_events_up_to(self, until: int):
        """
        Executes all the events up to the specified time.

        :param until: Time until which to execute the events
        :return: None
        """
        while self.events_queue and self.events_queue[0].time <= until:
            next_event = self.events_queue.pop(0)
            next_event.execute(environment=self)

    def collect_data(self):
        """
        Collects all the required data for each timestep.

        :return: None
        """
        self.data['time'].append(self.time)

        for name, bubble in self.bubbles.items():
            occupancy = bubble.get_occupancy()
            self.data['bubble_occupancies'].setdefault(name, []).append(occupancy)

        # Collect other data as required
        # TODO: ADD WAITING LIST
