__author__ = 'eric'
import re
from channel_range_parser import *

# Represets
class ChannelState:

    def __init__(self, controller, raw = ""):
        # Takes a dictionary in the form of
        # "number" : the channel's number
        # "value": the channel's value in the state
        self.states = []
        self.controller = controller
        if raw != "":
            self.parse(raw)


    reg = "(?:channel)?(.+?)(?:@|at|\*)(\d+);?"
    def parse(self, raw):
        self.raw = raw
        noWhite = re.sub("\s", "", raw).lower()
        matches = re.findall(self.reg, noWhite)
        if matches:
            for m in matches:
                rng = m[0]
                val = int(m[1])
                channelRange = ChannelRangeParser(rng, self.controller)
                channelSet = ChannelSet(channelRange.set)
                self.set_at(channelSet, val)


    def get_channel_set(self):
        newSet = set()
        for state in self.states:
            newSet.add(int(state['number']))
        return ChannelSet(newSet)


    def set_at(self, channelSet, value):
        for channel in channelSet.set:
            self.states.append({
                "number": channel,
                "value": value
            })


# Represents a selection of channels
class ChannelSet:
    def __init__(self, set = None):
        self.set = set

    def to_string(self):
        if len(self.set) == 0:
            return 'Empty'
        l = list(self.set)

        ret = str(l[0])
        for i in range(1, len(l)):
            ret += ", " + str(l[i])
        return ret