import time

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.level_start_time = time.time()
        self.level_durations = {
            1: 30,   # Level 1 - 30 seconds
            2: 50,   # Level 2 - 50 seconds
            3: 80,   # Level 3 - 60 seconds
            4: 90,   # Level 4 - 70 seconds
            5: 110    # Level 5 - 80 seconds
        }

    def start_level(self, level=None):
        if level is not None:
            self.current_level = level
        self.level_start_time = time.time()

    def is_level_complete(self):
        elapsed_time = time.time() - self.level_start_time
        level_duration = self.level_durations.get(self.current_level, 60)
        return elapsed_time >= level_duration

    def next_level(self):
        self.current_level += 1
        self.start_level()

    def get_time_left(self):
        elapsed_time = time.time() - self.level_start_time
        level_duration = self.level_durations.get(self.current_level, 60)
        return max(0, level_duration - elapsed_time)

    def handle_special_levels(self):
        if self.current_level == 5:
            print("Level 5 Special Boss appears!")