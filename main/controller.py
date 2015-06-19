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
        if args[i] == None:
            return default
        else:
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

    def load_scene(self, name, fade = -1, percent = 100):
        return self.load_scene_list((name, fade, percent))
    def load_scene_list(self, args):
        name    = required_arg(args, 0, "A scene name must be supplied")
        fade    = optional_arg(args, 1, -1)
        percent = optional_arg(args, 2, 100)

        scn = self.find_scene(name)
        if scn == False:
            return "Scene not found"

        toFade = self.defaultFade
        if fade != -1 and fade != None:
            toFade = fade
        if scn.fade != None and scn.fade != -1:
            toFade = scn.fade

        toSet = scn.get_channel_state(self, percent)
        self.patch.set_channel_state(toSet, toFade)
        return "Loading scene %s with fade %s" % (name, toFade)


    def load_scene_channels(self, name, fade, percent, channelSet):
        return self.load_scene_channels_list((name, fade, percent, channelSet))
    def load_scene_channels_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied")
        fade        = optional_arg(args, 1, -1)
        percent     = optional_arg(args, 2, 100)
        channelSet  = required_arg(args, 3, "A ChannelSet must be supplied")

        scn = self.find_scene(name)
        if scn == False:
            return "Scene not found"

        toFade = self.defaultFade
        if fade != -1 and fade != None:
            toFade = fade
        if scn.fade != None and scn.fade != -1:
            toFade = scn.fade

        toSet = scn.get_custom_channel_state(self, percent, channelSet)
        self.patch.set_channel_state(toSet, toFade)
        return "Loading scene %s with fade %s" % (name, toFade)


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
        return self.save_scene_current_set_list((name, fade, channelSet))
    def save_scene_current_set_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied")
        fade        = optional_arg(args, 1, -1)
        channelSet  = required_arg(args, 2, "A ChannelSet must be supplied")

        channelState = ChannelState(self)
        for channel in channelSet.set:
            channelState.channel_at(channel, self.patch.get_channel_value(channel))

        return self.save_scene(name, fade, channelState)


    def save_scene(self, name, fade, channelState):
        return self.save_scene_list((name, fade, channelState))
    def save_scene_list(self, args):
        name            = required_arg(args, 0, "A name must be supplied")
        fade            = optional_arg(args, 1, -1)
        channelState    = required_arg(args, 2, "A channel state must be supplied")

        scene = Scene(name, channelState, fade)
        overwrite = False
        scn = self.find_scene(scene.name)
        if scn != False:
            self.scenes.remove(scn)
            overwrite = True

        self.scenes.append(scene)
        numChannels = channelState.get_num_channels()
        if overwrite:
            return "Scene '%s' overwritten with %s channels" % (name, numChannels)
        else:
            return "Scene '%s' saved with %s channels" % (name, numChannels)


    def print_scene(self, sceneName):
        return self.print_scene_list((sceneName))
    def print_scene_list(self, args):
        name = required_arg(args, 0, "A name must be supplied")
        scn = self.find_scene(name)
        if scn == False:
            return "Scene not found"
        else:
            return scn.toString()

    def list_scenes(self):
        return self.list_scenes_list()
    def list_scenes_list(self, args):
        str = "Current Saved Scenes:\n"
        for scene in self.scenes:
            chnCount = scene.channelState.get_num_channels()
            str += "\tName: %s\t\t\t\tFade time: %s\t\t\t\tChannels: %s" % (scene.name, scene.fade, chnCount)
            str += "\n"
        return str

    def find_scene(self, name):
        for scn in self.scenes:
            if scn.name == name:
                return scn
        return False



    # ------------------ Groups ----------------------
    def save_group(self, name, channelSet):
        self.save_group_list((name, channelSet))
    def save_group_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied")
        channelSet  = optional_arg(args, 1, self.lastSelected)

        newGroup = Group(name, channelSet)
        overwrite = False
        for grp in self.groups:
            if grp.name == newGroup.name:
                self.groups.remove(grp)
                overwrite = True

        self.groups.append(newGroup)

        if overwrite:
            return "Group %s saved with channels %s" % (name, channelSet.to_string())
        else:
            return "Group %s overwritten with channels %s" % (name, channelSet.to_string())

    def list_groups(self):
        return self.list_groups_list
    def list_groups_list(self, args):
        str = "Current Saved Groups:\n"
        for group in self.groups:
            str += "\tName: %s\t\t\t\tChannels: %s" % (group.name, group.channelSet.to_string())
            str += "\n"
        return str





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
        self.update(0.001)
        return "Set to %s " % value

    def last_at(self, value):
        self.last_at_list((value))
    def last_at_list(self, args):
        value   = required_arg(args, 0, "A value must be supplied")

        state = ChannelState(self)
        state.set_at(self.lastSelected, value)

        self.patch.set_channel_state(state)
        self.update(0.001)
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
        self.update(0.001)
        return "Set to %s " % value

    # Takes (ChannelSet, value)
    def at(self, channelState):
        self.at_list((channelState))
    def at_list(self, args):
        channelState  = required_arg(args, 0, "ChannelState instance must be supplied")

        if channelState.get_num_channels() == 0:
            return "No selected channels"

        self.lastSelected = channelState.get_channel_set()
        value = channelState.states[0]["value"]

        self.patch.set_channel_state(channelState)
        self.update(0.001)
        return "Set to %s " % value


    # ------------------ Util Functions ----------------------
    def update(self, diff):
        self.patch.update_channels(diff)


    def __init__(self):
        self.patch = Patch()
        self.lastSelected = ChannelSet()
        self.groups = []
        self.scenes = []

        self.defaultFade = 3
        self.defaultWait = 3