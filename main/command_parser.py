__author__ = 'eric'
import re
from range_parser import RangeParser
from controller import Controller

class CommandParser:
    """The controller class holds the primary logic for controlling the channels.
    There is a method for every major command that can be entered on the command line
    (except some utility commands). """

    controller = Controller()
    functions = controller.getFunctions()

    patterns = (
        {
            # patch channel [channel number] dmx [dmx address] ~fixture ~[fixture] ~label ~[label]
            "pattern": "(?:patch)(?:channel)(\d+)(?:dmx)(\d+)(?:fixture)?(\d+)?(?:label)?(\w+)?",
            "function": controller.patch,
            "params" : ()
        },

    )

    def __init__(self, controller):
        self.controller = controller

    def parseCommand(self, command):

        noWhite = re.sub("\s", "", command) # remove whitespace
        for p in self.patterns:
            ""



    # Commands
    def patchChannel(self):
