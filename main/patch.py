__author__ = 'eric'

from channel import Channel

# Helper methods
def to_255(value):
    return (value / 100.0) * 255.0

class Patch:

    channels = [] # Holds the Channel objects
    dmx = [] # Holds an output array for the raw DMX

    # Sets a single channel
    def set_channel(self, channelNumer, value, fadeTime = 0):
        chn = self.get_channel(channelNumer)
        if chn == False:
            return False

        chn.fadeTo(value, fadeTime)


    # Sets the channels according to the supplied ChannelState instance
    def set_channel_state(self, channelState, fadeTime = 0):
        for channel in channelState.states:
            self.set_channel(channel["number"], channel["value"], fadeTime)


    # Patches a single channel to a DMX address
    def patch_channel(self, number, dmxAddr, label = "", fixture = ""):
        self.unpatch_channel(number) # Remove the channel, if it's been patched
        self.unpatch_dmx(dmxAddr) # Remove the channel with dmx addression, if it's been patched
        newChn = Channel(number, dmxAddr, label, fixture)
        self.channels.append(newChn)
        self.make_room()


    # Extends the size of dmx[] from 0 to the maximum channel's DMX address
    def make_room(self):
        max = 0
        for chn in self.channels:
            if chn.dmxAddr > max:
                max = chn.dmxAddr

        self.dmx = [0 for i in range(0, max)]

    def get_channel_value(self, num):
        chn = self.get_channel(num)
        if not chn:
            return chn.value
        return False

    def get_channel(self, num):
        for chn in self.channels:
            if chn.number == num:
                return chn
        return False

    def get_channel_by_dmx(self, dmx):
        for chn in self.channels:
            if chn.dmx == dmx:
                return chn
        return False



    def unpatch_channel(self, num):
        for chn in self.channels:
            if chn.number == num:
                self.channels.remove(chn)
                return True
        return False

    def unpatch_dmx(self, dmx):
        for chn in self.channels:
            if chn.dmxAddr == dmx:
                self.channels.remove(chn)
                return True
        return False



    # Updates all the channel fades and dmx output array
    # Takes diff in seconds
    def update_channels(self, diff):
        for channel in self.channels:
            channel.update(diff)
            self.dmx[channel.dmxAddr - 1] = to_255(channel.value)

