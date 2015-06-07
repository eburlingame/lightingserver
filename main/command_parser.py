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

    def __init__(self, controller):
        self.controller = controller
        self.patterns = (
        {
            # patch channel [channel number] dmx [dmx address] ~fixture ~[fixture] ~label ~[label]
            "pattern": "(?:patch)(?:channel)(\d+)(?:dmx)(\d+)(?:fixture)?(\d+)?(?:label)?(\w+)?",
            "function": self.controller.patch_channel_list,
            "params" : ["int", "int", "string", "string"]
        },
        {
            # ~Channel [Channel Selection] (@, at, *) [percent]
            "pattern": "(?:channel)?(.+)(?:@|at|\*)(\d+)",
            "function": self.controller.at_list,
            "params" : ["channel_range", "int"]
        },
        {
            # save (group, grp) [name] {channel selection}
            "pattern": "(?:save)(?:group)(.+){(.+)}",
            "function": self.controller.save_group_list,
            "params" : ["string", "channel_range"]
        },
        {
            # save (group, grp) [name]
            "pattern": "(?:save)(?:group)(.+)",
            "function": self.controller.save_group_list,
            "params" : ["string"]
        },
        {
            # (@, at, *) [percent]
            "pattern": "(?:@|at|\*)(\d+)",
            "function": self.controller.last_at_list,
            "params" : [ "int" ]
        },
    )


    def parseCommand(self, command):

        noWhite = re.sub("\s", "", command) # remove whitespace
        noWhite = noWhite.lower() # make lower case
        for p in self.patterns:

            match = re.match(p["pattern"], noWhite) # match this pattern
            params = p["params"] # get the parameters
            func = p["function"] # get a reference to the function
            args = []

            if match and len(match.groups()) == len(params): # If the pattern matches our template
                i = 1
                for param in params: # For each parameter that we expect to find
                    toAdd = match.group(i) # If it's a string

                    if param == "int":
                        toAdd = int(toAdd)
                    elif param == "decimal":
                        toAdd = float(toAdd)
                    elif param == "range":
                        toAdd = RangeParser(toAdd)
                    elif param == "channel_range":
                        rng = ChannelRangeParser(toAdd, self.controller)
                        toAdd = ChannelSet(rng.set)
                        try:
                            pass
                        except Exception, e:
                            return e.message;

                    # Increment i if we aren't skipping this one
                    if param != "skip":
                        args.append(toAdd)
                        i += 1

                return func(args) # Call the function
        return "Didn't regonize input"