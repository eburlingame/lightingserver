__author__ = 'eric'
import re
from range_parser import RangeParser
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
            "params" : ("int", "int", "string", "string")
        },
        {
            # patch channel [channel number] dmx [dmx address] ~fixture ~[fixture] ~label ~[label]
            "pattern": "(.+)(?:@|at|\*)(\d+)",
            "function": self.controller.range_at_list,
            "params" : ("range", "int")
        },
    )


    def parseCommand(self, command):

        noWhite = re.sub("\s", "", command) # remove whitespace
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

                    # Increment i if
                    if param != "skip":
                        args.append(toAdd)
                        i += 1

                func(args) # Call the function