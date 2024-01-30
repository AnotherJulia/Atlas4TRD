from core import Event
import numpy as np


class MovementEvent(Event):
    def __init__(self, time, agent, start_bubble, end_bubble):
        super().__init__(time)
        self.agent = agent
        self.start_bubble = start_bubble  # Bubble object
        self.end_bubble = end_bubble  # Bubble Object

    def __repr__(self):
        return f"Movement Event({self.time}) - {self.start_bubble.slug} to {self.end_bubble.slug}"

    def process(self, environment):
        from core import StateBubble, MovementEvent

        if self.agent.current_bubble != self.start_bubble:
            raise ValueError(f"Agent {self.agent.id} is not in the expected start bubble. "
                             f"Start {self.start_bubble.slug} | Current {self.agent.current_bubble.slug}")

        # Move the agent from start to end bubble
        self.start_bubble.remove_agent(self.agent)
        self.end_bubble.add_agent(self.agent)
        self.agent.current_bubble = self.end_bubble

        # Handling different types of StateBubble
        if isinstance(self.end_bubble, StateBubble):
            if self.end_bubble.slug == "intake":
                # Determine the next step for the agent

                event_data = {
                    "start_bubble": self.start_bubble.slug,
                    "end_bubble": self.end_bubble.slug
                }

                self.agent.add_to_medical_history(event_type="movement_event", event_data=event_data, time=self.time)

                self.agent.decide_and_schedule_next_event()

            elif self.end_bubble.slug == "remission":
                
                # Instead use Tom's system (inefficiency 101)

                precomputed_probs = [self.end_bubble.phq_analyzer.get_prob_at_time(t, p=self.start_bubble.relapse_rate, type="maintenance") for t in range(0, 25)]

                for t, prob in enumerate(precomputed_probs):
                    # prob = self.end_bubble.phq_analyzer.get_prob_at_time(t, p=self.start_bubble.relapse_rate, type="maintenance")
                    if prob < np.random.random():
                        relapse = next(bubble for bubble in environment.bubbles if bubble.slug == "relapse")
                        movement_event = MovementEvent(self.time + t, self.agent, self.end_bubble, relapse)
                        break

                event_data = {
                        "state": "recovery"
                    }

                self.agent.add_to_medical_history(event_type="movement_event", event_data=event_data,
                                                      time=self.time)

                recovery = next(bubble for bubble in environment.bubbles if bubble.slug == "recovery")
                movement_event = MovementEvent(self.time + 24, self.agent, self.end_bubble, recovery)

                environment.schedule_event(movement_event)


            elif self.end_bubble.slug == "recovery":
                 
                relapse_rate = 0.3

                for event in reversed(self.agent.medical_history):
                    if event["type"] == "treatment_end":
                        relapse_rate = event['data'].get('relapse_rate')
                        break

                if relapse_rate is None:
                    raise ValueError(f"No Last treatment bubble found")

                precomputed_probs = [self.end_bubble.phq_analyzer.get_prob_at_time(t, p=relapse_rate, type="discontinued") for t in range(0, 25)]

                for t, prob in enumerate(precomputed_probs):
                    # prob = self.end_bubble.phq_analyzer.get_prob_at_time(t, p=0.3, type="maintenance")
                    if prob < np.random.random():
                        relapse = next(bubble for bubble in environment.bubbles if bubble.slug == "relapse")
                        movement_event = MovementEvent(self.time + t, self.agent, self.end_bubble, relapse)
                        break

                event_data = {
                        "state": "recovery"
                    }

                self.agent.add_to_medical_history(event_type="movement_event", event_data=event_data,
                                                      time=self.time)

                recovery = next(bubble for bubble in environment.bubbles if bubble.slug == "recovery")
                movement_event = MovementEvent(self.time + 24, self.agent, self.end_bubble, recovery)

                environment.schedule_event(movement_event)

            elif self.end_bubble.slug == "relapse":
                # Schedule a movement event back to intake

                event_data = {
                    "start_bubble": self.start_bubble.slug,
                    "end_bubble": self.end_bubble.slug
                }

                self.agent.add_to_medical_history(event_type="relapse", event_data=event_data, time=self.time)

                next_bubble = next(bubble for bubble in environment.bubbles if bubble.slug == "intake")
                movement_event = MovementEvent(self.time + environment.dt, self.agent, self.end_bubble, next_bubble)
                environment.schedule_event(movement_event)
            else:
                raise ValueError
