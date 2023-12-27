import json
import uuid
import random

from utilities.config import read_config


class Agent:

    def __init__(self, current_bubble, episode_duration, symptom_severity, psychosis, functional_impairment,
                 treatment_failures, environment):
        self.environment = environment
        self.id = uuid.uuid4()
        self.current_bubble = current_bubble
        self.history = []  # TODO : Add a TreatmentHistory object to simply store that here

        # DM_TRD Parameters
        trd_parameters = ["episode_duration", "symptom_severity", "psychosis", "functional_impairment", "treatment_failures"]
        self.episode_duration = episode_duration
        self.symptom_severity = symptom_severity
        self.psychosis = psychosis
        self.functional_impairment = functional_impairment # not used, not tracked
        self.treatment_failures = treatment_failures # not used, not tracked

        # MADRS
        self.MADRS = self.calculate_madrs_score() # we can use this to calculate madrs score -> and add madrs score changes to reflect treatment effectiveness

    def __str__(self):
        return f'{self.id} @ {self.current_bubble} | Episode: {self.episode_duration} Symptom Severity: {self.symptom_severity} w/ Psychosis: {self.psychosis}'

    def move_agent(self, bubble):
        self.current_bubble = bubble
        bubble.add_agent(agent=self)

    def decide_and_schedule_next_event(self, event_time=None):
        from core import MovementEvent

        print(f"Agent {self.id} deciding next event from {self.current_bubble.slug}")

        if event_time is None: event_time = self.environment.time
        next_event_slug, event_type = self.decide_next_event()

        print(f"Agent {self.id} decided on event type: {event_type}")

        if event_type == "stay":
            print(f"Agent {self.id} will stay in {self.current_bubble.slug}")
            return

        # Debug: Print next bubble
        print(f"Agent {self.id} is moving to bubble: {next_event_slug}")

        # Find the next bubble based on the slug
        next_bubble = self.current_bubble.get_connected_bubbles(next_event_slug)
        if not next_bubble:
            print(f"Error: No connected bubble found for slug: {next_event_slug}")
            raise ValueError(f"No connected bubble found for slug: {next_event_slug}")

        # Schedule a movement event to the next bubble
        print(f"Scheduling movement event for Agent {self.id} to {next_event_slug} at time {event_time}")
        movement_event = MovementEvent(event_time, self, self.current_bubble, next_bubble)
        self.environment.schedule_event(movement_event)

    def decide_next_event(self):
        # Check the current bubble and decide the next step

        # Implement previous treatment failures and functional impairment to the decision tree

        print(f"Agent {self.id} is in bubble: {self.current_bubble.slug}")
        global decision

        if self.current_bubble.slug == "intake":
            next_event_slug = random.choices(["ad", "ad_ap", "ap"], weights=[0.33, 0.33, 0.34])[0]
            decision = (next_event_slug, 'movement')
        elif self.current_bubble.slug == "ad" or self.current_bubble.slug == "ad_ap" or self.current_bubble.slug == "ap":
            # After augmented therapies treatment, move to esketamine
            decision = ('esketamine', 'movement')
        elif self.current_bubble.slug == "esketamine":
            # After esketamine, move to ect
            decision = ('ect', 'movement')
        elif self.current_bubble.slug == "ect":
            # After ect, go back to intake for reassessment
            decision = ('ad', 'movement')
        elif self.current_bubble.slug == "remission":
            # If in remission, stay there
            decision = ('stay', 'stay')
        elif self.current_bubble.slug == "relapse":
            # If relapsed, go back to intake
            decision = ('intake', 'movement')

        print(f"Agent {self.id} decided on next event: {decision}")
        return decision

    def calculate_madrs_score(self):
        scoring_method = read_config("../../config/dm_trd_scoring.json")
        patient_score = 0

        # Manually coding this right now // todo: automate

        # Determine episode duration score
        if self.episode_duration == "acute":
            patient_score += scoring_method["episode_duration"]["acute"]
        elif self.episode_duration == "subacute":
            patient_score += scoring_method["episode_duration"]["subacute"]
        elif self.episode_duration == "chronic":
            patient_score += scoring_method["episode_duration"]["chronic"]
        else:
            raise ValueError(f"Invalid episode duration: {self.episode_duration}")

        # Determine symptom severity score
        if self.symptom_severity == "mild":
            patient_score += scoring_method["symptom_severity"]["mild"]
        elif self.symptom_severity == "moderate":
            patient_score += scoring_method["symptom_severity"]["moderate"]
        elif self.symptom_severity == "severe":
            if self.psychosis:
                patient_score += scoring_method["symptom_severity"]["severe_with_psychosis"]
            else:
                patient_score += scoring_method["symptom_severity"]["severe_without_psychosis"]
        else:
            raise ValueError(f"Invalid symptom severity: {self.symptom_severity}")

        # Determine score change from functional impairment
        if self.functional_impairment == "mild":
            patient_score += scoring_method["functional_impairment"]["mild"]
        elif self.functional_impairment == "moderate":
            patient_score += scoring_method["functional_impairment"]["moderate"]
        elif self.functional_impairment == "severe":
            patient_score += scoring_method["functional_impairment"]["severe"]

        # Determine score change from treatment failures
        if self.treatment_failures == "0":
            pass
        elif self.treatment_failures == "1-2":
            patient_score += scoring_method["treatment_failures"]["1-2"]
        elif self.treatment_failures == "3-4":
            patient_score += scoring_method["treatment_failures"]["3-4"]
        elif self.treatment_failures == "5-6":
            patient_score += scoring_method["treatment_failures"]["5-6"]

        print(patient_score)
        return patient_score
