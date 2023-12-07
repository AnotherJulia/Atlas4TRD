from enum import Enum


class AgentTypes(Enum):
    PATIENT = 0,
    STAFF = 1


class PatientStates(Enum):
    HEALTHY = 0,
    DEPRESSED = 1,
    TRD = 2,
    TREATED = 3,


class Agent:

    def __init__(self, location, agent_type: AgentTypes, patient_state: PatientStates = None):
        self.location = location  # Where location is the current bubble slug [eg. waiting_room].

        self.agent_type = agent_type
        self.state = patient_state

    def tick(self):
        # What happends with the agent at a specific Tick
        pass
