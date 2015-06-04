__author__ = 'eric'
from patch import Patch
from channel_set import *

# Helper functions:

# Both functions get the argument in args at the ith position
# Will get a required argument, or raise an Excpetion with message error
def required_arg(args, i, error):
    try:
        return args[i]
    except:
        raise Exception(error)

# Will get an optional argument, or return the supplied default
def optional_arg(args, i, default):
    try:
        return args[i]
    except:
        return default


class Controller:
    # Capital letters refer to a class instance
    # Lowercase refer to a generic type
    # ~ denotes an optional field
    # [Function]_list takes arguments as a list



    # Takes (channel number, channel value, ~label, fixture ~fixture)
    def patch_channel(self, *args):
        self.patch_channel_list(args)
    def patch_channel_list(self, args):
        number  = required_arg(args, 0, "A name must be supplied")
        dmx     = required_arg(args, 1, "A dmx channel must be supplied")
        label   = optional_arg(args, 2, "")
        fixture = optional_arg(args, 3, "")

        number = int(number)
        dmx = int(dmx)

        self.patch.patch_channel(number, dmx, label, dmx)



    # Takes (ChannelSet, value)
    def at(self, *args):
        self.at_list(args)
    def at_list(self, args):
        channelSet = required_arg(args, 0, "ChannelSet instance must be supplied")
        value = required_arg(args, 1, "Value must be supplied")
        value = int(value)
        state = ChannelState()
        state.set_at(channelSet, value)
        self.patch.set_channel_state(state)

    # Util functions

    def update(self):
        self.patch.update_channels(1)


    def __init__(self):
        self.patch = Patch()
