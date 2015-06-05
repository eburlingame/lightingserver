__author__ = 'eric'

# Represets
class ChannelState:

    def __init__(self):
        # Takes a dictionary in the form of
        # "number" : the channel's number
        # "value": the channel's value in the state
        self.states = []

    def get_channel_set(self):
        channelSet = set()
        for state in self.states:
            channelSet += int(state.number)

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