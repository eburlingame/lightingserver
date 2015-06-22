__author__ = 'Eric Burlingame'
import re
from range_parser import *
from channel_set import *
from channel_range_parser import *
from controller import Controller

class CommandParser:
    """The controller class holds the primary logic for controlling the channels.
    There is a method for every major command that can be entered on the command line
    (except some utility commands). """

    # ------------------ Commmand Patterns ----------------------
    def __init__(self, controller):
        self.controller = controller
        self.patterns = (
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
            "pattern": "(?:save)(?:group)(.+){(.+)}",
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
            "pattern": "listscenes",
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
            "pattern": "loadsequence(.+?)((?:insert|step|fade|wait|all|cued)(?:.+?)?)?channel(.+?)$",
            "function": self.parse_load_sequence_channel_set,
            "params" : [ "string", "string", "channel_range" ]
        },
        {
            # load sequence [sequence name] ~fade [~fade time] ~wait [~wait time] ~step ~[step number] ~(cued)
            "pattern": "loadsequence(.+?)((?:insert|step|fade|wait|all|cued)(?:.+?)?)?$",
            "function": self.parse_load_sequence,
            "params" : [ "string", "string" ]
        },
        {
            # save sequence [sequence name] ~insert ~step ~[step] ~fade [~fade time]
            # ~wait [~wait time] ~all ~cued { [channel commands] }
            "pattern": "savesequence(.+?)((?:insert|step|fade|wait|all|cued)(?:.+?)?)?{(.+?)}$",
            "function": self.parse_save_sequence_channel_state,
            "params" : [ "string", "string", "channel_state" ]
        },
        {
            # save sequence [sequence name] ~insert ~step ~[step] ~fade [~fade time]
            # ~wait [~wait time] ~all ~cued ~channel ~[channel selection]
            "pattern": "savesequence(.+?)((?:insert|step|fade|wait|all|cued)(?:.+?)?)?channel(.+?)$",
            "function": self.parse_save_sequence_channel_set,
            "params" : [ "string", "string", "channel_range" ]
        },
        {
            # save sequence [sequence name] ~insert ~step ~[step] ~fade [~fade time]
            # ~wait [~wait time] ~all ~cued
            "pattern": "savesequence(.+?)((?:insert|step|fade|wait|all|cued)(?:.+?)?)?$",
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
            # delete sequence [sequence name]
            "pattern": "delete(?:sequence)(.+?)(?:step)(\d+)",
            "function": self.controller.delete_sequence_step_list,
            "params" : [ "string", "int" ]
        },
        {
            # delete sequence [sequence name] step [step number]
            "pattern": "delete(?:sequence)(.+?)",
            "function": self.controller.delete_sequence,
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
            "pattern": "listsequences",
            "function": self.controller.list_sequences_list,
            "params" : [  ]
        },
        {
            # list running
            "pattern": "listrunning",
            "function": self.controller.list_running_list,
            "params" : [  ]
        },


        {
            # (@, at, *) [percent]
            "pattern": "print(?:channels)?",
            "function": self.controller.print_channels_list,
            "params" : [  ]
        },


        )

    def runCommand(self, command):
        split = re.split(";", command)
        ret = ""
        for line in split:
           ret += "\n" + self.parseCommand(line)


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
                try:
                    pass
                except Exception, e:
                    return "Error: " + e.message


        return "Didn't regonize input"

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

            # Increment i if we aren't skipping this one
            if param != "skip":
                args.append(toAdd)
                i += 1

        # print "Args %s " % args
        return func(args) # Call the function



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
                                             opt["cued"])


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
                                             opt["repeat"],
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
                                             opt["repeat"],
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
                                             opt["repeat"],
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
        "repeat" : self.match_first("repeat", optionsStr, True),
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
        "fade"    : self.match_first("fade([\d|\.]+)", optionsStr, -1, float),
        "wait"    : self.match_first("wait([\d|\.]+)", optionsStr, -1, float),
        "step"    : self.match_first("step(\d+)", optionsStr, 0),
        "repeat"  : self.match_first("repeat", optionsStr, True),
        "all"     : self.match_first("all", optionsStr, False),
        "cued"    : self.match_first("cued", optionsStr, False),
        "percent" : self.match_first("%(\d+)", optionsStr, 100)
        }

    def match_first(self, pattern, string, default, typeFunc = int):
        match = re.search(pattern, string)
        if match:
            if len(match.groups()) > 0:
                return typeFunc(match.group(1))
            return True
        else:
            return default



