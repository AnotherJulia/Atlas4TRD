import uuid


class MedicalHistoryLog:
    # each object of this class = 1 "medical log" in their medical history

    def __init__(self, type, bubble_name, time_of_enter, end_bubble=None):
        self.type = type
        self.bubble_name = bubble_name          # indicated location of log
        self.end_bubble = end_bubble
        self.time = time_of_enter                # indicates duration of this "history"

    def __repr__(self):
        return (f"TYPE: {self.type} | NAME: {self.bubble_name} | END: {self.end_bubble if self.end_bubble else None} | "
                f"TIME: {self.time}")
