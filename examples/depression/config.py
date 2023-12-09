from core import SimulationConfig


class DepressionSimulationConfig(SimulationConfig):

    def __init__(self, name: str, waiting_capacity: int, intake_capacity: int, diagnosis_capacity: int, therapy_capacity: int, medication_capacity: int):
        super().__init__()

        self.name = name

        self.waiting_capacity = waiting_capacity
        self.intake_capacity = intake_capacity
        self.diagnosis_capacity = diagnosis_capacity
        self.therapy_capacity = therapy_capacity
        self.medication_capacity = medication_capacity

        self.intake_duration = 1
        self.diagnosis_duration = 1
        self.therapy_duration = 10
        self.medication_duration = 10
