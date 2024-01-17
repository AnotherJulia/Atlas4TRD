import uuid


class MedicalHistoryLog:
    # each object of this class = 1 "medical log" in their medical historyr

    def __init__(self, bubble_name, time_of_enter):
        self.bubble_name = bubble_name          # indicated location of log
        self.time = time_of_enter                # indicates duration of this "history"

    def __repr__(self):
        return f"NAME: {self.bubble_name} | TIME: {self.time}"


