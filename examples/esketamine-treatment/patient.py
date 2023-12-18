from core import Agent


class Patient(Agent):

    def __init__(self, name, start, score):
        super().__init__(name, start_bubble=start)

        self.score = score

    def determine_next_step(self, environment):
        available_connections = environment.find_available_connections(self.current_bubble, type="step")

        # Available connections represent the possible treatment steps that a patient could choose


        pass
