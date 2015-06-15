__author__ = 'eric'
from patch import Patch
from channel_set import *
from group import *
from scene import *

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



    # ------------------ Patching ----------------------
    # Takes (channel number, channel value, ~label, fixture ~fixture)
    def patch_channel(self, channelNumber, channelValue, label = "", fixture = ""):
        self.patch_channel_list((channelNumber, channelValue, label, fixture))
    def patch_channel_list(self, args):
        number  = required_arg(args, 0, "A name must be supplied")
        dmx     = required_arg(args, 1, "A dmx channel must be supplied")
        label   = optional_arg(args, 2, "")
        fixture = optional_arg(args, 3, "")

        number = int(number)
        dmx = int(dmx)

        self.patch.patch_channel(number, dmx, label, fixture)
        return "Patched channel %s to dmx address %s" % (number, dmx)


    # ------------------ Scenes ----------------------

    def save_scene_current(self, name, fade):
        return self.save_scene_current_list((name, fade))
    def save_scene_current_list(self, args):
        name    = required_arg(args, 0, "A name must be supplied")
        fade    = optional_arg(args, 1, -1)

        rawSet = set()
        for channel in self.patch.channels:
            if channel.value > 0: # If the channel is above 0% it's "active"
                rawSet.add(channel.number)

        channelSet = ChannelSet(rawSet)
        return self.save_scene_current_set(name, fade, channelSet)



    def save_scene_current_set(self, name, fade, channelSet):
        self.save_scene_current_set_list((name, fade, channelSet))
    def save_scene_current_set_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied")
        fade        = optional_arg(args, 1, -1)
        channelSet  = required_arg(args, 2, "A ChannelSet must be supplied")

        channelState = ChannelState(self)
        for channel in channelSet.set:
            channelState.channel_at(channel, self.patch.get_channel_value(channel))

        return self.save_scene(name, channelState, fade)


    def save_scene(self, name, channelState, fade = -1):
        return self.save_scene_list((name, channelState, fade))
    def save_scene_list(self, args):
        name            = required_arg(args, 0, "A name must be supplied")
        channelState    = required_arg(args, 1, "A channel state must be supplied")
        fade            = optional_arg(args, 2, -1)

        scene = Scene(name, channelState, fade)
        self.scenes.append(scene)
        return "Scene '%s' saved with %s channels" % (name, len(channelState.states))


    def list_scenes(self):
        return self.list_scenes_list

    def list_scenes_list(self, args):
        str = "Current Saved Scenes:\n"
        for scene in self.scenes:
            chnCount = len(scene.channelState.get_channel_set().set)
            str += "\tName: %s\t\tFade time: %s\t\tChannels: %s" % (scene.name, scene.fade, chnCount)
            str += "\n"
        return str

    # ------------------ Groups ----------------------
    def save_group(self, name, channelSet):
        self.save_group_list((name, channelSet))
    def save_group_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied")
        channelSet  = optional_arg(args, 1, self.lastSelected)

        newGroup = Group(name, channelSet)
        self.groups.append(newGroup)
        return "Group %s saved with channels %s" % (name, channelSet.to_string())



    # ------------------ Channel Control ----------------------
    def range_at(self, channelRange, value):
        self.range_at_list((channelRange, value))
    def range_at_list(self, args):
        channelRange    = required_arg(args, 0, "Channel range instance must be supplied")
        value           = required_arg(args, 1, "Value must be supplied")

        set = ChannelSet(channelRange.set)
        self.lastSelected = set
        state = ChannelState(self)
        state.set_at(set, value)

        self.patch.set_channel_state(state)
        self.update()
        return "Set to %s " % value

    def last_at(self, value):
        self.last_at_list((value))
    def last_at_list(self, args):
        value   = required_arg(args, 0, "A value must be supplied")

        state = ChannelState(self)
        state.set_at(self.lastSelected, value)

        self.patch.set_channel_state(state)
        self.update()
        return "Set to %s " % value

    # Takes (ChannelSet, value)
    def set_at(self, channelSet, value):
        self.at_list((channelSet, value))
    def set_at_list(self, args):
        channelSet  = required_arg(args, 0, "ChannelSet instance must be supplied")
        value       = required_arg(args, 1, "Value must be supplied")

        self.lastSelected = channelSet

        state = ChannelState(self)
        state.set_at(channelSet, value)

        self.patch.set_channel_state(state)
        self.update()
        return "Set to %s " % value

    # Takes (ChannelSet, value)
    def at(self, channelState):
        self.at_list((channelState))
    def at_list(self, args):
        channelState  = required_arg(args, 0, "ChannelState instance must be supplied")

        self.lastSelected = channelState.get_channel_set()
        value = channelState.states[0]["value"]

        self.patch.set_channel_state(channelState)
        self.update()
        return "Set to %s " % value


    # ------------------ Util Functions ----------------------
    def update(self):
        self.patch.update_channels(1)


    def __init__(self):
        self.patch = Patch()
        self.lastSelected = ChannelSet()
        self.groups = []
        self.scenes = []
