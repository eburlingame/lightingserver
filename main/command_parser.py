__author__ = 'eric'
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
            # save sequence [sequence name] ~insert ~step ~[step] ~fade [~fade time]
            # ~wait [~wait time] ~all ~cued ~channel ~[channel selection]
            "pattern": self.parse_save_sequence,
            "params" : [ "string", "string", "channel_range" ]
        },


        )


    # ------------------ Parsing and Calling Commands ----------------------
    def parseCommand(self, command):

        noWhite = re.sub("\s", "", command) # remove whitespace
        noWhite = noWhite.lower() # make lower case
        for p in self.patterns:

            match = re.match(p["pattern"], noWhite) # match this pattern
            params = p["params"] # get the parameters
            func = p["function"] # get a reference to the function
            if match and len(match.groups()) == len(params): # If the pattern matches our template
                print "Matched: " + p['pattern']
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

        return func(args) # Call the function




    # ------------------ Custom Parsing Functions ----------------------

    def parse_save_sequence(self, name, optionsStr, channelSet):
        