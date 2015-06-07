__author__ = 'eric'

class Scene:

    def __init__(self, name, channelState, fade = -1):
        self.channelState = channelState
        self.fade = fade
        self.name = name

