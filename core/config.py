from dataclasses import dataclass


@dataclass
class SimulationConfig:

    def __init__(self, name: str = 'simulation', dt: int = 1):
        self.name = name
        self.dt = dt
