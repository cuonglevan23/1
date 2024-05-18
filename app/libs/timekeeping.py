from datetime import datetime

class Timekeeping:
    def __init__(self, person, timestamp=None):
        self.person = person
        self.timestamp = timestamp or datetime.now()

    def get_person(self):
        return self.person

    def get_timestamp(self):
        return self.timestamp

    def set_person(self, person):
        self.person = person

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def __str__(self):
        return 'Person: {}, Timestamp: {}'.format(self.person, self.timestamp)