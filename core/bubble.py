import uuid


class Bubble:

    def __init__(self, slug, description, depth, environment):
        self.id = uuid.uuid4()
        self.environment = environment
        self.slug = slug
        self.description = description
        self.depth = depth

        self.current_agents = []
        self.connections = []

    def __str__(self):
        return f"Bubble: {self.slug} - {self.description}"

    def update(self):
        pass  # implement for own

    def get_occupancy(self):
        return len(self.current_agents)

    def add_agent(self, agent):
        print(f"Adding agent {agent.id} to {self.slug}")
        self.current_agents.append(agent)

    # def remove_agent(self, agent):
    #     if agent in self.current_agents:
    #         print(f"Removing agent {agent.id} from {self.slug}")
    #         self.current_agents.remove(agent)
    #     else:
    #         raise ValueError(f"Agent {agent.id} not found in bubble {self.slug}. Current bubble: {agent.current_bubble.slug}")

    def remove_agent(self, agent):
        if agent in self.current_agents:
            print(f"Removing agent {agent.id} from {self.slug}")
            self.current_agents.remove(agent)
        else:
            # Handling the case where the agent is not found in the current bubble
            agent_current_bubble_slug = agent.current_bubble.slug if agent.current_bubble else "None"
            print(
                f"Error: Attempted to remove agent {agent.id} from {self.slug}, but the agent was not found. Agent's current bubble: {agent_current_bubble_slug}")

    def connect(self, other_bubble):
        # Connects bubble objects to others
        self.connections.append(other_bubble)

    def get_connected_bubbles(self, bubble_slug):
        try:
            bubble = next(bubble for bubble in self.connections if bubble.slug == bubble_slug)
        except StopIteration:
            bubble = None
        return bubble

    def get_waiting(self):
        return 0    # waiting list implemented in child objects





