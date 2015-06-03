__author__ = 'eric'

from channel import Channel

def to_255(value):
    return (value / 100.0) * 255.0

class Patch:

    channels = [] # Holds the Channel objects
    dmx = [] # Holds an output array for the raw DMX

    # Sets a single channel
    def set_channel(self, channelNumer, value, fadeTime = 0):

        chn = self.get_channel(channelNumer)
        if chn == False:
            raise Exception("Channel not found")

        chn.fadeTo(value, fadeTime)

    # Patches a single channel to a DMX address
    def patch_channel(self, number, dmxAddr, label = "", fixture = ""):
        newChn = Channel(number, dmxAddr, label, fixture)
        self.channels.append(newChn)
        self.make_room()

    # Extends the size of dmx[] from 0 to the maximum channel's DMX address
    def make_room(self):
        max = 0
        for chn in self.channels:
            if chn.dmxAddr > max:
                max = chn.dmxAddr

        self.dmx = [0 for i in range(0, max + 1)]

    def get_channel(self, num):
        for chn in self.channels:
            if chn.number == num:
                return chn
        return False

    # Updates all the channel fades and dmx output array
    # Takes diff in seconds
    def update_channels(self, diff):
        for channel in self.channels:
            channel.update(diff)
            self.dmx[channel.dmxAddr] = to_255(channel.value)
