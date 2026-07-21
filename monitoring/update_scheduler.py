from datetime import datetime, timedelta

class UpdateScheduler:
    def __init__(self):
        self.last_update = datetime.now()

    def next_update(self, days=7):
        return self.last_update + timedelta(days=days)

    def update_now(self):
        self.last_update = datetime.now()

    def get_last_update(self):
        return self.last_update