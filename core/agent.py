from core_types.effects import EffectType
from core.event import Event, MoveAgentEvent, EndAgentEvent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.environment import Environment


class Agent:
    def __init__(self, id: int, initial_depression_score, initial_bubble: str):
        self.id = id

        self.depression_score = initial_depression_score
        self.bubble = initial_bubble
        self.location_history = []

    def __str__(self):
        return f"Agent: {self.id} | Score: {self.depression_score} | Bubble: {self.bubble}"

    def implement_effect(self, effect_type: EffectType, effect):
        # Filter the different core_types of effects in this function

        # If the effect has some kind of effect on the score
        if effect_type == EffectType.SCORE:
            self.depression_score += effect

    def move_to(self, new_bubble: str):
        # TODO : Can we add some validator that this new_location / exists and is of type bubble

        # Store the current location for the future
        self.location_history.append(self.bubble)

        # Update the location to the new one
        self.bubble = new_bubble

    def find_next_step(self, environment: 'Environment'):
        # How do we find the next step in the treatment? -> look at prev. bubbles and look at depression score

        if self.bubble == "waiting":
            return MoveAgentEvent(name="Moving Agent to Intake", time=environment.time + 2, agent_id=self.id,
                                  from_bubble="waiting", to_bubble="intake")

        if self.bubble == "intake":
            return MoveAgentEvent(name="Moving Agent to Diagnosis", time=environment.time + 2, agent_id=self.id,
                                  from_bubble="intake", to_bubble="diagnosis")

        if self.bubble == "diagnosis":

            if self.depression_score >= 10:
                return MoveAgentEvent(name="Moving Agent to Pharmacological Treatment", time=environment.time + 1 + 10, agent_id=self.id,
                                      from_bubble="diagnosis", to_bubble="medical_treatment")
            elif 5 < self.depression_score < 10:
                return MoveAgentEvent(name="Moving Agent to Therapy Treatment", time=environment.time + 1 + 10,
                                      agent_id=self.id, from_bubble="diagnosis", to_bubble="therapy_treatment")

            else:
                return EndAgentEvent(name="Moving Agent to treated", time=environment.time+1, agent_id=self.id)



        # default return value
        return EndAgentEvent(name="Ending Agent", time=environment.time + 1, agent_id=self.id)

    # def update_treatment_plan(self, new_plan):
    #     # TODO : Can we add a treatment plan validator and create a type out of them
    #     self.treatment_plan = new_plan
