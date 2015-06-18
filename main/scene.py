__author__ = 'eric'

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

    def get_channel_state(self, channelSet):
        set = channelSet.set
        for chann