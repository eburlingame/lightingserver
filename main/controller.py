__author__ = 'Eric Burlingame'
from patch import Patch
from channel_set import *
from group import *
from scene import *
from sequence import *
from schedule import *
from csv_file import *

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

    def patch_one_to_one(self, channelSet, dmxChannelSet):
        return self.patch_one_to_one_list((channelSet, dmxChannelSet))
    def patch_one_to_one_list(self, args):
        channelSet      = required_arg(args, 0, "A channelSet must be supplied")
        dmxChannelSet   = required_arg(args, 1, "A dmx channelSet must be supplied")

        if len(channelSet.set) != len(dmxChannelSet.set):
            return "The same number of channel must be supplied for one to one patching"

        channels = sorted(list(channelSet.set))
        dmxs     = sorted(list(dmxChannelSet.set))
        for i in range(0, len(channels)):
            self.patch.patch_channel(channels[i], dmxs[i])

        return "Patched channels (%s) to DMX channels (%s)" % (channelSet.to_string(), dmxChannelSet.to_string())

    def unpatch_dmx(self, channelSet):
        return self.unpatch_dmx_list([channelSet])
    def unpatch_dmx_list(self, args):
        channelSet = required_arg(args, 0, "A ChannelSet must be supplied")

        for channel in channelSet.set:
            self.patch.unpatch_dmx(channel)

        return "Unpatch DMX channels %s" % channelSet.to_string()

    def unpatch_channel(self, channelSet):
        return self.unpatch_channel_list([channelSet])
    def unpatch_channel_list(self, args):
        channelSet = required_arg(args, 0, "A ChannelSet must be supplied")

        for channel in channelSet.set:
            self.patch.unpatch_channel(channel)

        return "Unpatch control channels %s" % channelSet.to_string()

    def print_patch(self):
        return self.print_patch_list([ ])
    def print_patch_list(self, args):
        return "Patched Channels: \n" + self.patch.to_string()

    def print_channels(self):
        return self.print_channels_list([])
    def print_channels_list(self, args):
        str = "Active Channels:\n\n"

        i = 1
        for channel in self.patch.channels:
            str += "\tChn\t%s\t: %s\t" % (channel.number, "{:10.2f}".format(channel.value))
            if i % 4 == 0:
                str += "\n"
            i += 1
        return str


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

        channelSet = self.patch.get_active_channel_set(self)

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

    def clear_scenes_list(self, args):
        self.scenes = []
        return "All scenes deleted"

    def delete_scene(self, name):
        return self.delete_scene_list([name])
    def delete_scene_list(self, args):
        name = required_arg(args, 0, "A scene name must be supplied")
        scene = self.find_scene(name)
        if scene == False:
            return "Scene not found"
        self.scenes.remove(scene)
        return "Scene %s deleted" % name


    # ------------------ Groups ----------------------
    def get_group(self, name):
        for group in self.groups:
            if group.name == name:
                return group
        return False

    def save_group(self, name, channelSet):
        return self.save_group_list((name, channelSet))
    def save_group_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied")
        channelSet  = optional_arg(args, 1, self.lastSelected)

        if channelSet.set == False:
            return "No channels selected previously"

        newGroup = Group(name, channelSet)

        overwrite = False
        group = self.get_group(name)
        if group != False:
            self.groups.remove(group)
            overwrite = True

        self.groups.append(newGroup)

        if overwrite:
            return "Group %s overwritten with channels %s" % (name, channelSet.to_string())
        else:
            return "Group %s saved with channels %s" % (name, channelSet.to_string())

    def list_groups(self):
        return self.list_groups_list
    def list_groups_list(self, args):
        str = "Current Saved Groups:\n"
        for group in self.groups:
            str += "\t" + group.to_string() + "\n"
        return str

    def print_group(self, name):
        return self.print_group_list([name])
    def print_group_list(self, args):
        name = required_arg(args, 0, "A group name is required")

        group = self.get_group(name)
        if group == False:
            return "Group not found"

        return "\t" + group.to_string()


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
        return state.to_string()

    def last_at(self, value):
        return self.last_at_list((value))
    def last_at_list(self, args):
        value   = required_arg(args, 0, "A value must be supplied")

        state = ChannelState(self)
        state.set_at(self.lastSelected, value)

        self.patch.set_channel_state(state)
        self.update(0.001)
        return state.to_string()

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
        return state.to_string()

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
        return channelState.to_string()


    # ------------------ Sequences ----------------------

    def get_sequence(self, name):
        for sequence in self.sequences:
            if sequence.name == name:
                return sequence
        return False
    def get_sequence_runner(self, name, id = None):
        if id == None:
            runners = []
            for runner in self.sequenceRunners:
                if runner.sequence.name == name:
                    runners.append(runner)
            return runners
        else:
            for runner in self.sequenceRunners:
                if runner.sequence.name == name and runner.id == id:
                    return runner
            return False

    def load_sequence(self, name, percent = 100, fade = -1, wait = -1, step = 0, cued = False, norepeat=False, channelSet = None):
        return self.load_sequence_list((name, percent, fade, wait, step, cued, norepeat, channelSet))
    def load_sequence_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied") # Name of the sequence
        percent     = optional_arg(args, 1, 100)
        fade        = optional_arg(args, 2, -1)
        wait        = optional_arg(args, 3, -1)
        step        = optional_arg(args, 4, 0)
        cued        = optional_arg(args, 5, False)
        norepeat    = optional_arg(args, 6, False)
        channelSet  = optional_arg(args, 7, None)

        sequence = self.get_sequence(name)
        if sequence == False:
            return "Sequence not found"

        running_id = 0
        for runner in self.sequenceRunners:
            if runner.sequence.name == name:
                running_id = runner.id + 1 # Set the new runner to be one more than the last

        # controller, id, sequence, channelSet = None, percent = 100,
        # cued = False, fade = -1, wait = -1, step = 0, repeat = True
        runner = SequenceRunner(self, running_id, sequence, channelSet, percent, cued, fade, wait, step, norepeat)
        self.sequenceRunners.append(runner)
        return "Loaded sequence %s (running id: %s) " % (name, running_id)

    def save_sequence(self, name, insert = False, step = -1, fade = -1, wait = -1,
                      norepeat = False, all = False, cued = False, channelSet = None, channelState = None):
        return self.save_sequence_list((name, insert, step, fade, wait, norepeat, all, cued, channelSet, channelState))
    def save_sequence_list(self, args):
        name         = required_arg(args, 0, "A name must be supplied") # Name of the sequence
        insert       = optional_arg(args, 1, False) # Whether the step will be inserted
        step         = optional_arg(args, 2, -1)    # The step where to insert/overwrite the scene
        fade         = optional_arg(args, 3, -1)    # The fade time of the step
        wait         = optional_arg(args, 4, -1)    # The wait time of the step
        norepeat     = optional_arg(args, 5, False)  # Whether the sequence should repeat
        all          = optional_arg(args, 6, False) # Whether all channels should be included
        cued         = optional_arg(args, 7, False) # Whether the step will be manually cued
        channelSet   = optional_arg(args, 8, None)  # The set of channels to record into the step
        channelState = optional_arg(args, 9, None)  # The state of the channel to use

        # Find the sequence, or make a new one
        sequence = self.get_sequence(name)
        if sequence == False:
            sequence = Sequence(name)
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
        newStep = SequenceStep(stepNum, name, channelStateToSet, fade, wait, norepeat)

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

    def unload_sequence(self, all = None, name = None, id = None):
        return self.unload_sequence_list([all, name, id])
    def unload_sequence_list(self, args):
        all     = optional_arg(args, 0, False)
        name    = optional_arg(args, 1, None)
        id      = optional_arg(args, 2, None)
        if all != False:
            self.sequenceRunners = []
            return "All sequences removed from running queue"
        # Cancel all with a matching name
        if id == None and name != None:
            runners = self.get_sequence_runner(name, id)
            for runner in runners:
                self.sequenceRunners.remove(runner)
            return "All sequences %s removed from running queue " % name
        # Cancel one with a particular id
        else:
            runner = self.get_sequence_runner(name, id)
            self.sequenceRunners.remove(runner)
            return "Sequence %s removed from running queue with id %s" % (name, id)

    def pause_sequence(self, all = None, name = None, id = None):
        return self.pause_sequence_list([all, name, id])
    def pause_sequence_list(self, args):
        all     = optional_arg(args, 0, False)
        name    = optional_arg(args, 1, None)
        id      = optional_arg(args, 2, None)

        if all != False:
            for runner in self.sequenceRunners:
                runner.pause()
            return "All sequences removed from running queue"
        # Pause all with a matching name
        if id == None and name != None:
            runners = self.get_sequence_runner(name, id)
            for runner in runners:
                runner.pause()
            return "All sequences %s paused " % name
        # Pause one with a particular id
        else:
            runner = self.get_sequence_runner(name, id)
            runner.pause()
            return "Sequence %s paused with id %s" % (name, id)

    def unpause_sequence(self, all = None, name = None, id = None):
        return self.pause_sequence_list([all, name, id])
    def unpause_sequence_list(self, args):
        all     = optional_arg(args, 0, False)
        name    = optional_arg(args, 1, None)
        id      = optional_arg(args, 2, None)

        if all != False:
            for runner in self.sequenceRunners:
                runner.unpause()
            return "All sequences removed from running queue"
        # Pause all with a matching name
        if id == None and name != None:
            runners = self.get_sequence_runner(name, id)
            for runner in runners:
                runner.unpause()
            return "All sequences %s paused " % name
        # Pause one with a particular id
        else:
            runner = self.get_sequence_runner(name, id)
            runner.unpause()
            return "Sequence %s paused with id %s" % (name, id)


    def advance_sequence(self, all = None, name = None, id = None):
        return self.pause_sequence_list([all, name, id])
    def advance_sequence_list(self, args):
        all     = optional_arg(args, 0, False)
        name    = optional_arg(args, 1, None)
        id      = optional_arg(args, 2, None)

        if all != False:
            for runner in self.sequenceRunners:
                runner.advance()
            return "All sequences advanced"
        # Pause all with a matching name
        if id == None and name != None:
            runners = self.get_sequence_runner(name, id)
            for runner in runners:
                runner.advance()
            return "All sequences %s advanced " % name
        # Pause one with a particular id
        else:
            runner = self.get_sequence_runner(name, id)
            runner.advance()
            return "Sequence %s advanced with id %s" % (name, id)

    def print_sequence(self, name):
        return self.print_sequence([name])
    def print_sequence_list(self, args):
        name        = required_arg(args, 0, "A name must be supplied") # Name of the sequence

        seq = self.get_sequence(name)
        if seq == False:
            return "Sequence not found"

        return seq.to_string()

    def list_running(self):
        return self.list_running_list()
    def list_running_list(self, args):
        str = "Running Sequences: "
        for runner in self.sequenceRunners:
            str += "\n\t" + runner.to_string()
        return str

    def list_sequences(self):
        return self.list_sequences_list(None)
    def list_sequences_list(self, args):
        str = "Current Saved Sequences: "
        for sequence in self.sequences:
            str += "\n\t" + sequence.to_string_short()
        return str

    def clear_sequences_list(self, args):
        self.sequences = []
        return "All sequences deleted"

    def delete_sequence_step(self, name, step):
        return self.delete_scene_list()
    def delete_sequence_step_list(self, args):
        name = required_arg(args, 0, "A sequence name must be supplied")
        step = required_arg(args, 1, "A sequence step must be supplied")

        sequence = self.get_sequence(name)
        if sequence == False:
            return "Sequence not found"

        id = sequence.delete_step(step)
        if id != -1:
            return "Deleted step %s in sequence %s" % (id, sequence)
        else:
            return "Step %s not found in sequence %s" % (id, sequence)

    def delete_sequence(self, name):
        return self.delete_sequence_list([name])
    def delete_sequence_list(self, args):
        name = required_arg(args, 0, "A sequence name must be supplied")
        sequence = self.get_sequence(name)
        if sequence == False:
            return "Sequence not found"
        self.sequences.remove(sequence)
        return "Sequence %s deleted" % name


    # ------------------ Scheduleing ----------------------

    def schedule_command(self, command, time):
        return self.schedule_command_list((command, time))
    def schedule_command_list(self, args):
        command = required_arg(args, 0, "A command must be supplied")
        time    = required_arg(args, 1, "A datetime must be supplied")

        schedule = Schedule(command, time)
        self.schedules.append(schedule)

        strtime = time.strftime("%H:%M:%S")
        return "New schedule saved for %s" % strtime

    def delete_schedule(self, time):
        return self.delete_schedule((time))
    def delete_schedule_list(self, args):
        time    = required_arg(args, 0, "A datetime must be supplied")

        for schedule in self.schedules:
            if schedule.matches(time):
                self.schedules.remove(schedule)

        strtime = time.strftime("%H:%M:%S")
        return "Removed scheudles starting at %s " % strtime

    def list_schedules(self):
        return self.list_schedules([ ])
    def list_schedules_list(self, args):
        toRet = "Currently saved scheduled commands:"
        for schedule in self.schedules:
            toRet += "\n\t" + schedule.to_string()
        return toRet



    # ------------------ Util Functions ----------------------
    def update(self, diff):
        for runner in self.sequenceRunners:
            runner.update(diff)
            # Remove the runner if it has completed the sequence
            if runner.done:
                self.sequenceRunners.remove(runner)
        self.patch.update_channels(diff)
        self.check_time()

    def check_time(self):
        for schedule in self.schedules:
            if schedule.time_matches():
                self.main.run_command(schedule.command)
                print "Running scheduled command '%s'" % schedule.command

    def to_commands(self, shortcuts):
        str = "#PATCH:"
        str += self.patch.to_commands()

        str += "\n\n"

        str += "#GROUPS:\n"
        for group in self.groups:
            str += group.to_command()
        str += "\n"

        str += "#SCENES:\n"
        for scene in self.scenes:
            str += scene.to_command()
        str += "\n"

        str += "#SEQUENCES:\n"
        for sequence in self.sequences:
            str += sequence.to_command()

        str += "\n"
        str += "#SHORTCUTS:\n"
        for shortcut in shortcuts:
            str += shortcut.to_command()

        return str

    def read_csv(self, filepath):
        return self.read_csv_list([filepath])
    def read_csv_list(self, args):
        filepath = required_arg(args, 0, "A filepath must be supplied")
        absPath = self.main.get_abs_path(filepath)
        print "abs path %s" % absPath
        try:
            csv = CSVFile(absPath, self)
        except Exception, e:
            return e.message

        self.sequences.append(csv.sequence)
        return "Added sequence %s with %s steps" % (csv.sequence.name, len(csv.sequence.steps))



    def __init__(self, main):
        self.patch = Patch()
        self.lastSelected       = ChannelSet()
        self.groups             = []
        self.scenes             = []
        self.sequences          = []
        self.sequenceRunners    = []
        self.schedules          = []

        self.defaultFade = 3
        self.defaultWait = 3

        self.main = main

















