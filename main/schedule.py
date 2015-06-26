__author__ = 'eric'
import datetime
class Schedule:

    def __init__(self, command, time):
        self.command = command
        self.time = time
        self.fired = False

    def time_matches(self):
        now = datetime.datetime.now()
        if not self.matches(now):
            self.fired = False
            return False

        if self.fired:
            return False

        self.fired = True
        return True

    def matches(self, another):
        if another.hour != self.time.hour:
            return False
        if another.minute != self.time.minute:
            return False
        if another.second != self.time.second:
            return False
        return True

    def to_string(self):
        strtime = self.time.strftime("%H:%M:%S")
        return "Command '%s' scheduled for %s" % (self.command, strtime)