__author__ = 'Eric Burlingame'

class Group:

    def __init__(self, name, channelSet):
        self.name = name
        self.channelSet = channelSet

    def get_set(self):
        return self.channelSet.set

    def to_string(self):
        return "Name: %s\t\tChannels: %s" % (self.name, self.channelSet.to_string())

    def to_command(self):
        return "save group %s channel %s \n" % (self.name, self.channelSet.to_string())
