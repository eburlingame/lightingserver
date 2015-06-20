__author__ = 'Eric Burlingame'
import re
import copy
from channel_range_parser import *
import operator

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

    # Returns the sorted pairs of channel, numbers in alist
    def get_sorted_pairs(self):
        return sorted(self.states, key=operator.itemgetter("number"))

    def get_num_channels(self):
        return len(self.states)

    def get_channel_set(self):
        newSet = set()
        for state in self.states:
            newSet.add(int(state['number']))
        return ChannelSet(newSet)

    def channel_at(self, channel, value):
        # Check to see if the channel has already been saved
        for state in self.states:
            if channel == state["number"]:
                self.states.remove(state)
        # Add new channel to the end
        self.states.append({
                "number": channel,
                "value": value
            })

    def set_at(self, channelSet, value):
        for channel in channelSet.set:
            self.channel_at(channel, value)

    def group_by_values(self):
        channels = copy.deepcopy(self.states)
        values = set()
        for channel in channels:
            values.update([ channel["value"] ])

        groups = []
        for value in values:
            chnSet = []
            for channel in channels:
                if channel["value"] == value:
                    chnSet.append(channel)
            groups.append(chnSet)

        return groups


    def to_string(self):
        str = ""
        groups = self.group_by_values()
        i = 0
        for group in groups:
            chnSet = []
            for channel in group:
                chnSet.append(channel["number"])
            channelSet = ChannelSet(chnSet)
            value = group[0]["value"]
            str += "%s at %s" % (channelSet.to_string(), value)
            if i != len(groups) - 1:
                str += "; "
            i += 1

        return str


# Represents a selection of channels
class ChannelSet:
    def __init__(self, set = None):
        self.set = set

    def group_by_adjacents(self):
        channels = sorted(list(copy.deepcopy(self.set)))
        adjacents = []

        set = [ channels[0] ]
        for i in range(0, len(channels) - 1):
            if channels[i] + 1 == channels[i + 1]:
                set.append(channels[i + 1])
            else:
                adjacents.append(set)
                set = [ channels[i + 1] ]

        adjacents.append(set) # Add last set

        return adjacents


    def to_string(self):
        if len(self.set) == 0:
            return 'Empty'

        string = ""
        groups = self.group_by_adjacents()
        i = 0
        for group in groups:
            if len(group) == 1:
                string += str(group[0])
            elif len(group) == 2:
                string += str(group[0]) + " and " + str(group[1])
            elif len(group) > 2:
                string += str(group[0]) + " thru " + str(group[len(group) - 1])
            if i != len(groups) - 1: # Not the last one
                string += " and "
            i += 1

        return string