__author__ = 'Eric Burlingame'

class Group:

    def __init__(self, name, channelSet):
        self.name = name
        self.channelSet = channelSet

    def get_set(self):
        return self.channelSet.set