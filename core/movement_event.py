from core import Event
<<<<<<< HEAD
=======
import numpy as np
>>>>>>> origin/packaging/framework


class MovementEvent(Event):
    def __init__(self, time, agent, start_bubble, end_bubble):
        super().__init__(time)
        self.agent = agent
<<<<<<< HEAD
        self.start_bubble = start_bubble        # Bubble object
        self.end_bubble = end_bubble            # Bubble Object

    def process(self, environment):
        from core import StepBubble, TreatmentEvent, StateBubble, MovementEvent

        print(f"Processing MovementEvent: Agent {self.agent.id} from {self.start_bubble.slug} to {self.end_bubble.slug}")

        if self.agent.current_bubble != self.start_bubble:
            print(
                f"Warning: Agent {self.agent.id} is not in the expected start bubble {self.start_bubble.slug}. Current bubble: {self.agent.current_bubble.slug}")
            # Optionally, reschedule the event or take other appropriate actions
            return
=======
        self.start_bubble = start_bubble  # Bubble object
        self.end_bubble = end_bubble  # Bubble Object

    def __repr__(self):
        return f"Movement Event({self.time}) - {self.start_bubble.slug} to {self.end_bubble.slug}"

    def process(self, environment):
        from core import StateBubble, MovementEvent

        if self.agent.current_bubble != self.start_bubble:
            raise ValueError(f"Agent {self.agent.id} is not in the expected start bubble. "
                             f"Start {self.start_bubble.slug} | Current {self.agent.current_bubble.slug}")
>>>>>>> origin/packaging/framework

        # Move the agent from start to end bubble
        self.start_bubble.remove_agent(self.agent)
        self.end_bubble.add_agent(self.agent)
        self.agent.current_bubble = self.end_bubble

<<<<<<< HEAD
        # If the end bubble is a StepBubble, schedule a treatment event
        if isinstance(self.end_bubble, StepBubble):
            treatment_start_time = self.time + environment.dt
            treatment_event = TreatmentEvent(treatment_start_time, self.agent, self.end_bubble)
            environment.schedule_event(treatment_event)

        # Handling different types of StateBubbles
        elif isinstance(self.end_bubble, StateBubble):
            if self.end_bubble.slug == "intake":
                # Determine the next step for the agent
                self.agent.decide_and_schedule_next_event()

            elif self.end_bubble.slug == "remission":
                # Keep the agent in remission, no further action needed
                pass

            elif self.end_bubble.slug == "relapse":
                # Schedule a movement event back to intake
                intake_bubble = next(bubble for bubble in environment.bubbles if bubble.slug == "intake")
                movement_event = MovementEvent(self.time + environment.dt, self.agent, self.end_bubble, intake_bubble)
                environment.schedule_event(movement_event)
=======
        # Handling different types of StateBubbles
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

                # With some probability, the patient can relapse
                if np.random.random() < self.start_bubble.relapse_rate:
                    next_step_bubble = next(bubble for bubble in environment.bubbles if bubble.slug == "relapse")

                    time_until_relapse = self.end_bubble.phq_analyzer.time_to_relapse("maintenance")
                    if time_until_relapse > 24:
                        recovery = next(bubble for bubble in environment.bubbles if bubble.slug == "recovery")
                        movement_event = MovementEvent(self.time + 24, self.agent, self.end_bubble,
                                                       recovery)

                    else:
                        movement_event = MovementEvent(self.time + time_until_relapse, self.agent, self.end_bubble,
                                                       next_step_bubble)

                # if patient doesn't relapse, then they go to recovery after 6 months!
                else:
                    recovery = next(bubble for bubble in environment.bubbles if bubble.slug == "recovery")

                    event_data = {
                        "state": "recovery"
                    }

                    self.agent.add_to_medical_history(event_type="movement_event", event_data=event_data,
                                                      time=self.time)

                    movement_event = MovementEvent(self.time + 24, self.agent, self.end_bubble,
                                                   recovery)
                environment.schedule_event(movement_event)

            elif self.end_bubble.slug == "recovery":

                time_until_relapse = self.end_bubble.phq_analyzer.time_to_relapse("discontinued")
                relapse_chance = (np.sum(self.end_bubble.phq_analyzer.interval_probs_discontinued))

                if np.random.random() < relapse_chance:
                    relapse = next(bubble for bubble in environment.bubbles if bubble.slug == "relapse")
                    movement_event = MovementEvent(self.time + time_until_relapse, self.agent, self.end_bubble,
                                                   relapse)
                    environment.schedule_event(movement_event)

                # otherwise we just stay here! patient recovers

            elif self.end_bubble.slug == "relapse":
                # Schedule a movement event back to intake

                event_data = {
                    "start_bubble": self.start_bubble.slug,
                    "end_bubble": self.end_bubble.slug
                }

                self.agent.add_to_medical_history(event_type="relapse", event_data=event_data, time=self.time)

                next_bubble = next(bubble for bubble in environment.bubbles if bubble.slug == "esketamine")
                movement_event = MovementEvent(self.time + environment.dt, self.agent, self.end_bubble, next_bubble)
                environment.schedule_event(movement_event)
            else:
                raise ValueError
>>>>>>> origin/packaging/framework
