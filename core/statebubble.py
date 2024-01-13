from core import Bubble


class StateBubble(Bubble):

    def __init__(self, slug, description, depth, env):
        super().__init__(slug, description, depth, env)

    def __str__(self):
        return f"Bubble: {self.slug} | Occupancy: {len(self.current_agents)}"

    def add_agent(self, agent):
        # from core import MovementEvent
        super().add_agent(agent)  # call the base class method to add the agent

        if self.slug == "intake":
            # agent.decide_and_schedule_next_event()
            pass
        elif self.slug == "remission":
            # Keep them there, no further action needed
            pass
        elif self.slug == "relapse":
            # Schedule a movement event back to intake
            # event_time = self.environment.time + self.environment.dt        # TODO: MODEL DATE UNTIL RELAPSE
            #
            # movement_event = MovementEvent(event_time, agent, self, self.get_connected_bubbles("intake"))
            # self.environment.schedule_event(movement_event)
            pass
