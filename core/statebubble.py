import numpy as np

from core import Bubble


class StateBubble(Bubble):

    def __init__(self, slug, description, depth, env):
        super().__init__(slug, description, depth, env)

        from utilities import PHQ9Analysis
        self.phq_analyzer = PHQ9Analysis()

    def __str__(self):
        return f"Bubble: {self.slug} | Occupancy: {len(self.current_agents)}"

    def add_agent(self, agent):
        # from core import MovementEvent
        super().add_agent(agent)  # call the base class method to add the agent

        if self.slug == "intake":
            # agent.decide_and_schedule_next_event()
            pass
        elif self.slug == "remission":
            # Test them for relapse up until the 6 month - taking up medical cost
            pass
        elif self.slug == "recovered":
            # Test them for relapse -- no longer taking up medical costs
            pass
        elif self.slug == "relapse":
            # print(f"Adding agent to relapse bubble")
            
            # Schedule a movement event back to intake
            # event_time = self.environment.time + self.environment.dt        # TODO: MODEL DATE UNTIL RELAPSE

            # from core import MovementEvent
            # movement_event = MovementEvent(event_time, agent, self, self.get_connected_bubbles("intake"))
            # self.environment.schedule_event(movement_event)

            pass
