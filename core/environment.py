import heapq
import uuid

class Environment:
    def __init__(self, time, dt):
        self.patient_rate = None
        self.id = uuid.uuid4()
        self.time = time
        self.dt = dt

        self.bubbles = []
        self.agents = []
        self.connections = []
        self.event_queue = []
        self.factory = None

        self.data = {
            "time": [],
            "bubble_occupancies": {},
            "waiting_list": {}
        }

    def run(self, until, verbose=False):

        while self.time < until:
            # Let's update all the bubbles
            for bubble in self.bubbles:
                bubble.update()

            # Adding new agents to the intake
            self.factory_tick()
            self.process_events_up_to(self.time)

            self.collect_data()
            self.time += self.dt

            if verbose: self.print_progress()


    def print_progress(self):
        print(f"----- Time: {self.time} -----")
        print(f"----- Bubble occupancies:")
        for bubble in self.bubbles:
            print(bubble)

        print(f"----- Events:")
        for event in self.event_queue:
            print(event[1])

    def add_bubble(self, bubble):
        self.bubbles.append(bubble)

    def create_step(self, slug, description, capacity, config, depth, env):
        from core import StepBubble

        bubble = StepBubble(slug, description, capacity, config, depth, env)
        self.bubbles.append(bubble)

    def create_state(self, slug, description, depth, env):
        from core import StateBubble

        bubble = StateBubble(slug, description, depth, env)
        self.bubbles.append(bubble)

    def add_connection(self, connection):
        self.connections.append(connection)

    def create_connection(self, start_slug, end_slug):
        from core import Connection
        global start_bubble
        global end_bubble

        for bubble in self.bubbles:
            if bubble.slug == start_slug:
                start_bubble = bubble
            elif bubble.slug == end_slug:
                end_bubble = bubble

        if start_bubble is None:
            print(f"Could not find a start bubble with the slug: {start_slug}")
            return
        if end_bubble is None:
            print(f"Could not find an end bubble with the slug: {end_slug}")
            return

        connection = Connection(start_bubble, end_bubble)
        self.connections.append(connection)

    def schedule_event(self, event):
        heapq.heappush(self.event_queue, (event.time, event))

    def process_events_up_to(self, end_time):
        from core import Event
        while self.event_queue and self.event_queue[0][0] <= end_time:
            _, next_event = heapq.heappop(self.event_queue)
            next_event.process(environment=self)

    def collect_data(self):
        self.data['time'].append(self.time)

        for bubble in self.bubbles:
            occupancy = bubble.get_occupancy()
            waiting = bubble.get_waiting()
            if bubble.slug not in self.data['bubble_occupancies']:
                self.data['bubble_occupancies'][bubble.slug] = []
                self.data['waiting_list'][bubble.slug] = []

            self.data['bubble_occupancies'][bubble.slug].append(occupancy)
            self.data['waiting_list'][bubble.slug].append(waiting)


    def connect_factory(self, factory):
        factory.connect_environment(self)
        self.factory = factory

    def factory_tick(self):
        if not self.factory:
            raise ValueError("Factory not set up yet")

        # Select the intake bubble
        intake_bubble = next(bubble for bubble in self.bubbles if bubble.slug == "intake")
        if intake_bubble is None:
            return ValueError("No Intake Bubble Found")

        for _ in range(self.patient_rate):
            new_agent = self.factory.create_agent(intake_bubble)
            intake_bubble.add_agent(new_agent)

    def create_initial_agents(self, num_agents, initial_bubble_slug):
        from core import TreatmentEvent, StateBubble

        for _ in range(num_agents):
            initial_bubble = next(bubble for bubble in self.bubbles if bubble.slug == initial_bubble_slug)

            if initial_bubble is None:
                raise ValueError(f"{initial_bubble_slug} not found in environment bubbles")

            agent = self.factory.create_agent(initial_bubble)

            self.agents.append(agent)  # Add the agents to the environment storage
            initial_bubble.add_agent(agent)  # Add the agents to their initial bubble

    def set_patient_rate(self, patient_rate):
        # TODO: Make the Patient Rate varied per dt (week) / mean / sd
        self.patient_rate = patient_rate

    def plot_occupancies(self, bubbles_to_plot=None):
        import matplotlib.pyplot as plt
        # Check if there is data to plot
        if not self.data['time'] or not self.data['bubble_occupancies']:
            print("No data to plot.")
            return

        # If no specific bubbles are provided, plot all bubbles
        if bubbles_to_plot is None:
            bubbles_to_plot = self.data['bubble_occupancies'].keys()

        plt.figure(figsize=(10, 6))  # Adjust the size as needed

        for bubble_slug, occupancies in self.data['bubble_occupancies'].items():
            if bubble_slug in bubbles_to_plot:
                plt.plot(self.data['time'], occupancies, label=bubble_slug)

        plt.xlabel('Time')
        plt.ylabel('Occupancy')
        plt.title('Bubble Occupancies Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_waiting_queues(self, bubbles_to_plot=None):
        import matplotlib.pyplot as plt
        # Check if there is data to plot
        if not self.data['time'] or not self.data['waiting_list']:
            print("No data to plot.")
            return

        # If no specific bubbles are provided, plot all bubbles
        if bubbles_to_plot is None:
            bubbles_to_plot = self.data['waiting_list'].keys()

        plt.figure(figsize=(10, 6))  # Adjust the size as needed

        for bubble_slug, occupancies in self.data['waiting_list'].items():
            if bubble_slug in bubbles_to_plot:
                plt.plot(self.data['time'], occupancies, label=bubble_slug)

        plt.xlabel('Time')
        plt.ylabel('Waiting')
        plt.title('Bubble Waiting List size Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()
