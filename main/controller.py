__author__ = 'Eric Burlingame'
from patch import Patch
from channel_set import *
from group import *
from scene import *
from sequence import *

# Helper functions:

# Both functions get the argument in args at the ith position
# Will get a required argument, or raise an Exception with message error
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
        return self.patch_channel_list((channelNumber, channelValue, label, fixture))
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

        channelSet = self.patch.get_active_channel_set()

        return self.save_scene_current_set(name, fade, channelSet)

    def save_scene_current_set(self, name, fade, channelSet):
        return self.save_scene_current_set_list((name, fade, channelSet))
    def save_scene_current_set_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied")
        fade        = optional_arg(args, 1, -1)
        channelSet  = required_arg(args, 2, "A ChannelSet must be supplied")

        channelState = self.patch.get_current_channel_state(self, channelSet)

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
        return self.print_scene_list(list(sceneName))
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
        return self.save_group_list((name, channelSet))
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
        return self.range_at_list((channelRange, value))
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
        return self.last_at_list((value))
    def last_at_list(self, args):
        value   = required_arg(args, 0, "A value must be supplied")

        state = ChannelState(self)
        state.set_at(self.lastSelected, value)

        self.patch.set_channel_state(state)
        self.update(0.001)
        return "Set to %s " % value

    # Takes (ChannelSet, value)
    def set_at(self, channelSet, value):
        return self.at_list((channelSet, value))
    def set_at_list(self, args):
        channelSet  = required_arg(args, 0, "ChannelSet instance must be supplied")
        value       = required_arg(args, 1, "Value must be supplied")

        self.lastSelected = channelSet

        state = ChannelState(self)
        state.set_at(channelSet, value)

        self.patch.set_channel_state(state)
        self.update(0.001)
        return "Set to %s " % value

    # Takes (ChannelState)
    def at(self, channelState):
        return self.at_list([channelState])
    def at_list(self, args):
        channelState  = required_arg(args, 0, "ChannelState instance must be supplied")

        if channelState.get_num_channels() == 0:
            return "No selected channels"

        self.lastSelected = channelState.get_channel_set()
        value = channelState.states[0]["value"]

        self.patch.set_channel_state(channelState)
        self.update(0.001)
        return "Set to %s " % value





    # ------------------ Sequences ----------------------

    def get_sequence(self, name):
        for sequence in self.sequences:
            if sequence.name == name:
                return sequence
        return False

    def load_sequence(self, name, percent = 100, fade = -1, wait = -1, step = 0, cued = False, channelSet = None):
        return self.load_sequence_list((name, percent, fade, wait, step, cued, channelSet))
    def load_sequence_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied") # Name of the sequence
        percent     = optional_arg(args, 1, 100)
        fade        = optional_arg(args, 2, -1)
        wait        = optional_arg(args, 3, -1)
        step        = optional_arg(args, 4, 0)
        cued        = optional_arg(args, 5, False)
        channelSet  = optional_arg(args, 6, None)
        print "FADE: %s" % fade
        sequence = self.get_sequence(name)
        if sequence == False:
            return "Sequence not found"

        # controller, id, sequence, channelSet = None, percent = 100,
        # cued = False, fade = -1, wait = -1, step = 0, repeat = True
        runner = SequenceRunner(self, 0, sequence, channelSet, percent, cued, fade, wait, step)
        self.sequenceRunners.append(runner)
        return "Loaded sequence %s " % name


    def save_sequence(self, name, insert = False, step = -1, fade = -1, wait = -1,
                      repeat = False, all = False, cued = False, channelSet = None, channelState = None):
        return self.save_sequence_list((name, insert, step, fade, wait, repeat, all, cued, channelSet, channelState))
    def save_sequence_list(self, args):
        name         = required_arg(args, 0, "A name must be supplied") # Name of the sequence
        insert       = optional_arg(args, 1, False) # Whether the step will be inserted
        step         = optional_arg(args, 2, -1)    # The step where to insert/overwrite the scene
        fade         = optional_arg(args, 3, -1)    # The fade time of the step
        wait         = optional_arg(args, 4, -1)    # The wait time of the step
        repeat       = optional_arg(args, 5, True)  # Whether all channels should be included
        all          = optional_arg(args, 6, False) # Whether all channels should be included
        cued         = optional_arg(args, 7, False) # Whether the step will be manually cued
        channelSet   = optional_arg(args, 8, None)  # The set of channels to record into the step
        channelState = optional_arg(args, 9, None)  # The state of the channel to use

        # Find the sequence, or make a new one
        sequence = self.get_sequence(name)
        if sequence == False:
            sequence = Sequence(name, repeat)
            self.sequences.append(sequence)
            sequence = self.sequences[len(self.sequences) - 1]


        if channelSet == None:
            channelSet = self.patch.get_active_channel_set(self)

        channelStateToSet = self.patch.get_current_channel_state(self, channelSet)

        # If we want all the channels to be included
        if all == True:
            channelStateToSet = self.patch.get_all_channel_state(self)

        if channelState != None:
            channelStateToSet = channelState

        # If the step will be added at the end
        stepNum = step
        if step == -1 or step == None:
            stepNum = len(sequence.steps)

        # If we want the step to be advanced manually
        if cued:
            wait = -1

        # Make and add the new step
        newStep = SequenceStep(stepNum, name, channelStateToSet, fade, wait)

        numChannels = channelStateToSet.get_num_channels()
        if insert:
            sequence.insert_step(newStep, stepNum)
            return "Inserted new step #%s in sequence %s with %s channels" % (stepNum + 1, name, numChannels)

        elif step != -1 and step != None:
            sequence.replace_step(newStep, stepNum)
            return "Replaced step #%s in sequence %s with %s channels" % (stepNum + 1, name, numChannels)

        else:
            sequence.append_step(newStep)
            return "Added new step #%s to sequence %s with %s channels" % (stepNum + 1, name, numChannels)

    def print_sequence(self, name):
        return self.print_sequence([name])
    def print_sequence_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied") # Name of the sequence

        seq = self.get_sequence(name)
        if seq == False:
            return "Sequence not found"

        return seq.to_string()

    def list_sequences(self):
        return self.list_sequences_list(None)
    def list_sequences_list(self, args):
        str = "Saved Sequences: "
        for sequence in self.sequences:
            str += "\n\t" + sequence.to_string_short()
        return str





    # ------------------ Util Functions ----------------------
    def update(self, diff):
        for runner in self.sequenceRunners:
            runner.update(diff)
        self.patch.update_channels(diff)


    def __init__(self):
        self.patch = Patch()
        self.lastSelected       = ChannelSet()
        self.groups             = []
        self.scenes             = []
        self.sequences          = []
        self.sequenceRunners    = []

        self.defaultFade = 3
        self.defaultWait = 3