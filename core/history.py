class MedicalHistoryLog:

    # each object of this class = 1 "medical log" in their medical historyr

    def __init__(self, bubble_name, duration, state):
        self.bubble_name = bubble_name          # indicated location of log
        self.duration = duration                # indicates duration of this "history"
        self.state = state                      # indicated QaLy state


