import time
from dateutil import parser

__author__ = 'Eric Burlingame'
import re
from range_parser import *
from channel_set import *
from channel_range_parser import *
from command_shortcut import *

class CommandParser:
    """The controller class holds the primary logic for controlling the channels.
    There is a method for every major command that can be entered on the command line
    (except some utility commands). """

    # ------------------ Commmand Patterns ----------------------
    def __init__(self, controller):
        self.controller = controller
        self.shortcuts = []
        self.patterns = (

        # Console Util Commands
        {
            # patch channel [channel number] dmx [dmx address] ~fixture ~[fixture] ~label ~[label]
            "pattern": "(?:patch)(?:channel)(\d+)(?:dmx)(\d+)(?:fixture)?(\d+)?(?:label)?(\w+)?",
            "function": self.controller.patch_channel_list,
            "params" : ["int", "int", "string", "string"]
        },
        {
            # define "[template]" as "[command]"
            "pattern": "(?:define)\"(.+?)\"as\"(.+?)\"",
            "function": self.define_shortcut,
            "params" : [ "string", "string" ]
        },
        {
            # list shortcuts
            "pattern": "listshortcuts?",
            "function": self.list_shortcuts,
            "params" : [  ]
        },
        {
            # delete shortcut "[shortcut name]"
            "pattern": "deleteshortcut\"(.+)\"",
            "function": self.delete_shortcut,
            "params" : [ "string" ]
        },


        # Scheduling

        {
            # schedule "[command]" at [time]
            "pattern": "schedule\"(.+?)\"at(.+)",
            "function": self.controller.schedule_command_list,
            "params" : [ "string", "time" ]
        },
        {
            # delete schedule [time]
            "pattern": "deleteschedule(.+)",
            "function": self.controller.delete_schedule_list,
            "params" : [ "time" ]
        },
        {
            # list schedules
            "pattern": "listschedules?",
            "function": self.controller.list_schedules_list,
            "params" : [  ]
        },


        # Patching
        {
            # patch channel [channel number] dmx [dmx address] ~fixture ~[fixture] ~label ~[label]
            "pattern": "(?:patch)(?:channel)(\d+)(?:dmx)(\d+)(?:fixture)?(\d+)?(?:label)?(\w+)?",
            "function": self.controller.patch_channel_list,
            "params" : ["int", "int", "string", "string"]
        },
        {
            # patch (one-to-one, one2one) channel [channel selection] dmx [channel address selection]
            "pattern": "patch(?:one-to-one|one2one)channel(.+?)dmx(.+?)$",
            "function": self.controller.patch_one_to_one_list,
            "params" : [ "channel_range", "channel_range" ]
        },
        {
            # unpatch dmx [channel selection]
            "pattern": "unpatchdmx(.+)",
            "function": self.controller.unpatch_dmx_list,
            "params" : [ "channel_range" ]
        },
        {
            # unpatch dmx [channel selection]
            "pattern": "printpatch",
            "function": self.controller.print_patch_list,
            "params" : [  ]
        },
        {
            # unpatch channel [channel selection]
            "pattern": "unpatchchannels?(.+)",
            "function": self.controller.unpatch_channel_list,
            "params" : [ "channel_range" ]
        },



        # Channel Control
        {
            # ~Channel [Channel Selection] (@, at, *) [percent]
            "pattern": "(^(?:channel)?(?:[^{]+?)(?:@|at|\*)(?:\d+))",
            "function": self.controller.at_list,
            "params" : ["channel_state"]
        },
        {
            # (@, at, *) [percent]
            "pattern": "^(?:@|at|\*)(\d+)",
            "function": self.controller.last_at_list,
            "params" : [ "int" ]
        },

        # Groups
        {
            # save (group, grp) [name] {channel selection}
            "pattern": "(?:save)(?:group)(.+?)(?:channels?)(.+)",
            "function": self.controller.save_group_list,
            "params" : ["string", "channel_range"]
        },
        {
            # save (group, grp) [name]
            "pattern" : "(?:save)(?:group)(.+)",
            "function": self.controller.save_group_list,
            "params"  : ["string"]
        },
        {
            # list groups
            "pattern" : "(?:list)(?:group)s?",
            "function": self.controller.list_groups_list,
            "params"  : [  ]
        },
        {
            # print group [group name]
            "pattern" : "printgroup(.+)",
            "function": self.controller.print_group_list,
            "params"  : [ "string" ]
        },

        # Scenes
        {
            # load scene [scene name] ~fade [~fade time] channel [channel selection]
            "pattern": "(?:load)(?:scene)(.+?)(?:(?:fade)([\d|\.]+))?(?:%(\d+))?channel(.+)$",
            "function": self.controller.load_scene_channels_list,
            "params" : [ "string", "decimal", "int", "channel_range" ]
        },
        {
            # load scene [scene name] ~fade [~fade time]
            "pattern": "(?:load)(?:scene)(.+?)(?:(?:fade)([\d|\.]+))?(?:%(\d+))?$",
            "function": self.controller.load_scene_list,
            "params" : [ "string", "decimal", "int" ]
        },
        {
            # save scene [scene name] ~fade ~[fade time] { [channel commands} }
            "pattern": "(?:save)(?:scene)(.+?)(?:(?:fade)([\d|\.]+))?{(.+)}",
            "function": self.controller.save_scene_list,
            "params" : [ "string", "decimal", "channel_state" ]
        },
        {
            # save scene [scene name] ~fade ~[fade time] ~channel [channel selection]
            "pattern": "(?:save)(?:scene)(.+?)(?:(?:fade)([\d|\.]+))?(?:channel)(.+)",
            "function": self.controller.save_scene_current_set_list,
            "params" : [ "string", "decimal", "channel_range" ]
        },
        {
            # save scene [scene name] ~fade ~[fade time]
            "pattern": "(?:save)(?:scene)(.+?)(?:(?:(?:fade)([\d|\.]+))?)$",
            "function": self.controller.save_scene_current_list,
            "params" : [ "string", "decimal" ]
        },
        {
            # clear sequences
            "pattern": "clearscenes",
            "function": self.controller.clear_scenes_list,
            "params" : [ ]
        },
        {
            # delete scene [scene name]
            "pattern": "delete(?:scene)(.+)",
            "function": self.controller.delete_scene,
            "params" : [ "string" ]
        },
        {
            # list scenes
            "pattern": "listscenes?",
            "function": self.controller.list_scenes_list,
            "params" : [  ]
        },
        {
            # print scene [scene name]
            "pattern": "printscene(.+)",
            "function": self.controller.print_scene_list,
            "params" : [ "string" ]
        },


        # Sequences
        {
            # load sequence [sequence name] ~fade [~fade time] ~wait [~wait time] ~step ~[step number] ~(cued)
            "pattern": "loadsequence(.+?)((?:insert|step|fade|wait|all|cued|norepeat)(?:.+?)?)?channel(.+?)$",
            "function": self.parse_load_sequence_channel_set,
            "params" : [ "string", "string", "channel_range" ]
        },
        {
            # load sequence [sequence name] ~fade [~fade time] ~wait [~wait time] ~step ~[step number] ~(cued)
            "pattern": "loadsequence(.+?)((?:insert|step|fade|wait|all|cued|norepeat)(?:.+?)?)?$",
            "function": self.parse_load_sequence,
            "params" : [ "string", "string" ]
        },
        {
            # save sequence [sequence name] ~insert ~step ~[step] ~fade [~fade time]
            # ~wait [~wait time] ~all ~cued { [channel commands] }
            "pattern": "savesequence(.+?)((?:insert|step|fade|wait|all|cued|norepeat)(?:.+?)?)?{(.+?)}$",
            "function": self.parse_save_sequence_channel_state,
            "params" : [ "string", "string", "channel_state" ]
        },
        {
            # save sequence [sequence name] ~insert ~step ~[step] ~fade [~fade time]
            # ~wait [~wait time] ~all ~cued ~channel ~[channel selection]
            "pattern": "savesequence(.+?)((?:insert|step|fade|wait|all|cued|norepeat)(?:.+?)?)?channel(.+?)$",
            "function": self.parse_save_sequence_channel_set,
            "params" : [ "string", "string", "channel_range" ]
        },
        {
            # save sequence [sequence name] ~insert ~step ~[step] ~fade [~fade time]
            # ~wait [~wait time] ~all ~cued
            "pattern": "savesequence(.+?)((?:insert|step|fade|wait|all|cued|norepeat)(?:.+?)?)?$",
            "function": self.parse_save_sequence,
            "params" : [ "string", "string" ]
        },
        {
            # clear sequences
            "pattern": "clearsequences",
            "function": self.controller.clear_sequences_list,
            "params" : [ ]
        },
        {
            # delete sequence [sequence name] step [step number]
            "pattern": "delete(?:sequence)(.+?)(?:step)(\d+)",
            "function": self.controller.delete_sequence_step_list,
            "params" : [ "string", "int" ]
        },
        {
            # delete sequence [sequence name]
            "pattern": "delete(?:sequence)(.+?)",
            "function": self.controller.delete_sequence_list,
            "params" : [ "string" ]
        },
        {
            # unload sequence [sequence name]
            "pattern": "(?:unload|stop)(?:sequence)?(all)?(.+?)?(?:id)?(\d+)?$",
            "function": self.controller.unload_sequence_list,
            "params" : [ "string", "string", "int" ]
        },
        {
            # unload sequence [sequence name]
            "pattern": "(?:pause|hold)(?:sequence)?(all)?(.+?)(?:id)?(\d+)?$",
            "function": self.controller.pause_sequence_list,
            "params" : [ "string", "string", "int" ]
        },
        {
            # (advance, go) sequence ~all [sequence name] ~fade ~[fade time] ~id [running id number]
            "pattern": "(?:advance|go)(?:sequence)?(all)?(.+?)(?:fade)?([\d|\.]+)?(?:id)?(\d+)?$",
            "function": self.controller.advance_sequence_list,
            "params" : [ "string", "string", "decimal", "int"]
        },
        {
            # unload sequence [sequence name]
            "pattern": "(?:unpause|play)(?:sequence)?(all)?(.+?)(?:id)?(\d+)?$",
            "function": self.controller.unpause_sequence_list,
            "params" : [ "string", "string", "int" ]
        },
        {
            # print sequence [sequence name]
            "pattern": "printsequence(.+)",
            "function": self.controller.print_sequence_list,
            "params" : [ "string" ]
        },
        {
            # list sequences
            "pattern": "listsequences?",
            "function": self.controller.list_sequences_list,
            "params" : [  ]
        },
        {
            # list running
            "pattern": "listrunnings?",
            "function": self.controller.list_running_list,
            "params" : [  ]
        },


        {
            # print channels
            "pattern": "print(?:channels)?",
            "function": self.controller.print_channels_list,
            "params" : [  ]
        },


        )

    def runCommand(self, command):
        command = re.sub("\s", "", command) # remove whitespace
        command = command.lower() # make lower case

        # Don't replace shortcuts if we are trying to define or delete one
        if not re.match("(?:define)\"(.+?)\"as\"(.+?)\"", command) and not re.match("deleteshortcut\"(.+)\"", command):
            command = self.process_patterns(command)

        split = self.split_by_brackets(command)
        ret = ""
        for line in split:
           ret += "\n" + self.parseCommand(line)
        return ret

    def split_by_brackets(self, command):
        open = False
        middles = []
        last = ""
        for i in range(0, len(command)):
            if command[i] == "\"" or command[i] == "{" or command[i] == "}":
                open = False if open else True

            if command[i] == ";":
                if not open:
                    middles.append(last)
                    last = ""
                else:
                    last = last + command[i]
            else:
                last = last + command[i]

        middles.append(last)
        return middles

    # ------------------ Parsing and Calling Commands ----------------------
    def parseCommand(self, command):

        noWhite = re.sub("\s", "", command) # remove whitespace
        noWhite = noWhite.lower() # make lower case

        for p in self.patterns:

            match = re.match(p["pattern"], noWhite) # match this pattern
            params = p["params"] # get the parameters
            func = p["function"] # get a reference to the function
            if match and len(match.groups()) == len(params): # If the pattern matches our template
                # print "Matched: " + p['pattern']
                return self.match_and_call(params, match, func)

        return "Didn't regonize input"
        # raise Exception("Didn't regonize input")

    def match_and_call(self, params, match, func):
        args = []
        i = 1
        for param in params: # For each parameter that we expect to find
            toAdd = match.group(i) # If it's a string
            if toAdd != "" and toAdd != None:
                if param == "int":
                    toAdd = int(toAdd)
                elif param == "decimal":
                    toAdd = float(toAdd)
                elif param == "range":
                    toAdd = RangeParser(toAdd)
                elif param == "channel_state":
                    toAdd = ChannelState(self.controller, toAdd)
                elif param == "channel_range":
                    rng = ChannelRangeParser(toAdd, self.controller)
                    toAdd = ChannelSet(rng.set)
                elif param == "time":
                    toAdd = parser.parse(toAdd)

            # Increment i if we aren't skipping this one
            if param != "skip":
                args.append(toAdd)
                i += 1

        # print "Args %s " % args
        return func(args) # Call the function

    def process_patterns(self, command):
        for shortcut in self.shortcuts:
            command = shortcut.replace(command)

        return command


    # ------------------ Custom Parsing Functions ----------------------

    # Takes a (name, optionsStr, channelSet) as args
    def parse_load_sequence_channel_set(self, args):
        name            = args[0]
        optionsStr      = args[1]
        channelSet      = args[2]

        if args[1] == None:
            optionsStr = ""

        opt = self.parse_load_options_string(optionsStr)

        # (name, percent, fade, wait, step, cued, channelSet)
        return self.controller.load_sequence(name,
                                             opt["percent"],
                                             opt["fade"],
                                             opt["wait"],
                                             opt["step"],
                                             opt["cued"],
                                             channelSet)
    # Takes a (name, optionsStr) as args
    def parse_load_sequence(self, args):
        name            = args[0]
        optionsStr      = args[1]

        if args[1] == None:
            optionsStr = ""

        opt = self.parse_load_options_string(optionsStr)

        # (name, percent, fade, wait, step, cued, channelSet)
        return self.controller.load_sequence(name,
                                             opt["percent"],
                                             opt["fade"],
                                             opt["wait"],
                                             opt["step"],
                                             opt["cued"],
                                             opt["norepeat"])


    # Takes (name, optionsStr, channelState) as args
    def parse_save_sequence_channel_state(self, args):
        name            = args[0]
        optionsStr      = args[1]
        channelState    = args[2]

        if args[1] == None:
            optionsStr = ""
        if args[2] == None:
            return self.parse_save_sequence(args)

        opt = self.parse_save_options_string(optionsStr)

        # (self, name, insert = False, step = -1, fade = -1, wait = -1,
        #        repeat = False, all = False, cued = False, channelSet = None)
        return self.controller.save_sequence(name,
                                             opt["insert"],
                                             opt["step"],
                                             opt["fade"],
                                             opt["wait"],
                                             opt["norepeat"],
                                             opt["all"],
                                             opt["cued"],
                                             None, channelState)

    # Takes (name, optionsStr, channelSet) as args
    def parse_save_sequence_channel_set(self, args):
        name            = args[0]
        optionsStr      = args[1]
        channelSet      = args[2]

        if args[1] == None:
            optionsStr = ""
        if args[2] == None:
            return self.parse_save_sequence(args)

        opt = self.parse_save_options_string(optionsStr)

        # (self, name, insert = False, step = -1, fade = -1, wait = -1,
        #        repeat = False, all = False, cued = False, channelSet = None)
        return self.controller.save_sequence(name,
                                             opt["insert"],
                                             opt["step"],
                                             opt["fade"],
                                             opt["wait"],
                                             opt["norepeat"],
                                             opt["all"],
                                             opt["cued"],
                                             channelSet)

    # Takes (name, optionsStr) as args
    def parse_save_sequence(self, args):
        name            = args[0]
        optionsStr      = args[1]
        if args[1] == None:
            optionsStr = ""

        opt = self.parse_save_options_string(optionsStr)

        # (self, name, insert = False, step = -1, fade = -1, wait = -1,
        #        repeat = False, all = False, cued = False, channelSet = None)
        return self.controller.save_sequence(name,
                                             opt["insert"],
                                             opt["step"],
                                             opt["fade"],
                                             opt["wait"],
                                             opt["norepeat"],
                                             opt["all"],
                                             opt["cued"])

    def parse_save_options_string(self, optionsStr):
        # insert = False
        # step = -1
        # fade = -1
        # wait = -1
        # repeat = True
        # all = False
        # cued = False
        return {
        "insert" : self.match_first("insert", optionsStr, False),
        "step"   : self.match_first("step(\d+)", optionsStr, -1),
        "fade"   : self.match_first("fade([\d|\.]+)", optionsStr, -1, float),
        "wait"   : self.match_first("wait([\d|\.]+)", optionsStr, -1, float),
        "norepeat": self.match_first("norepeat", optionsStr, False),
        "all"    : self.match_first("all", optionsStr, False),
        "cued"   : self.match_first("cued", optionsStr, False)
        }

    def parse_load_options_string(self, optionsStr):
        # fade = -1
        # wait = -1
        # repeat = True
        # all = False
        # cued = False
        # percent = 100
        return {
        "fade"     : self.match_first("fade([\d|\.]+)", optionsStr, -1, float),
        "wait"     : self.match_first("wait([\d|\.]+)", optionsStr, -1, float),
        "step"     : self.match_first("step(\d+)", optionsStr, 0),
        "norepeat" : self.match_first("norepeat", optionsStr, False),
        "all"      : self.match_first("all", optionsStr, False),
        "cued"     : self.match_first("cued", optionsStr, False),
        "percent"  : self.match_first("%(\d+)", optionsStr, 100)
        }

    def match_first(self, pattern, string, default, typeFunc = int):
        match = re.search(pattern, string)
        if match:
            if len(match.groups()) > 0:
                return typeFunc(match.group(1))
            return True
        else:
            return default

    def define_shortcut(self, args):
        if len(args) < 2:
            return "Not enough arguments"

        shortcut = args[0]
        command = args[1]

        replace = False
        for short in self.shortcuts:
            if short.shortcut == shortcut:
                self.shortcuts.remove(short)
                replace = True

        short = CommandShortcut(shortcut, command)
        self.shortcuts.append(short)
        if replace:
            return "Replaced shortcut"
        else:
            return "Created new shortcut"

    def list_shortcuts(self, args):
        str = "Currently Save Shortcuts:\n"
        for shortcut in self.shortcuts:
            str += "\t" + shortcut.to_string()
        return str

    def delete_shortcut(self, args):
        if len(args) < 1:
            return "Not enough arguments"

        cmd = args[0]
        for shortcut in self.shortcuts:
            if shortcut.shortcut == cmd:
                self.shortcuts.remove(shortcut)

        return "Removed shortcut '%s'" % cmd