from channel_set import ChannelState

__author__ = 'Eric Burlingame'

class Scene:

    def __init__(self, name, channelState, fade = -1):
        self.channelState = channelState
        self.fade = fade
        self.name = name

    def toString(self):
        str = "Scene " + self.name + ": \n"
        str += "\t Fade: %s" % self.fade
        for state in self.channelState.states:
            str += "\n\t\tChannel %s at %s" % (state["number"], state["value"])
        return str

    def get_channel_state(self, controller, percent):
        values = self.channelState.get_sorted_pairs()
        newState = ChannelState(controller);
        ratio = (percent / 100.0)
        for value in values:
            newState.channel_at(value["number"], value["value"] * ratio)

        return newState

    def get_custom_channel_state(self, controller, percent, channelSet):
        set = channelSet.set
        values = self.channelState.get_sorted_pairs()
        newState = ChannelState(controller)
        ratio = (percent / 100.0)
        i = 0
        for channel in set:
            newState.channel_at(channel, values[i]["value"] * ratio)
            i = (i + 1) % len(values)

        return newState

    def to_command(self):
        str = "save scene %s " % self.name
        if self.fade != -1:
            str += " fade %s " % self.fade
        str += " { %s } \n" % self.channelState.to_string()
        return str