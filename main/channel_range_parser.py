__author__ = 'eric'

import re
from range_parser import RangeParser


class ChannelRangeParser:
    """
        The goal of this class is to parse fixture labels and group names before parsing the standard
        numeric channel ranges (like 1 thru 10)
    """

    tokenAnd = "(and|\+)"
    tokenExp = "(except|-)"
    tokenThru = "(\/|thru|through)"

    tokenPre = tokenAnd + "?" + tokenExp + "?"

    tokenAndLook = "(?=and|\+)"
    tokenExpLook = "(?=except|-)"
    tokenThruLook = "(?=\/|thru|through)"

    regGroup = "group.+"

    def __init__(self, raw, controller):
        self.set = set() # Holds the net channels set
        self.adds = set() # Holds what channels have been added to the set
        self.exps = set() # Holds what channels have been subtracted from the set

        self.controller = controller

        rangeParser = RangeParser(raw)  # Parse plain channel values first
        self.adds = rangeParser.adds
        self.exps = rangeParser.exps
        self.raw = rangeParser.removed  # Get the raw text with those commands removed (e.g. 1/3 will be removed)

        self.parse()
        self.set = self.adds - self.exps

    def parse(self):
        noWhite = re.sub("\s", "", self.raw)  # remove whitespace
        noWhite = noWhite.lower()
        self.match_groups(noWhite)
        self.match_fixtures(noWhite)

    def match_groups(self, noWhite):
        # ((and|\+)|(except|-)|^)group(.+?)(?=(?:and|\+)|(?:except|-))
        reg = "((and|\+)|(except|-)|^)group(.+?)(?=(?=and|\+)|(?=except|-)|$)"
        matches = re.findall(reg, noWhite)
        if matches:
            for match in matches:
                add = True
                name = match[3]
                if match[2] != "":  # We find and "except" modifier
                    add = False

                group = self.get_group(name)
                if group == False:
                    raise Exception("Group not found")

                if add:
                    self.add(list(group.channelSet.set))
                else:
                    self.remove(list(group.channelSet.set))

    def match_fixtures(self, noWhite):
        # ((and|\+)|(except|-)|^)group(.+?)(?=(?:and|\+)|(?:except|-))
        reg = "((and|\+)|(except|-)|^)fixture(.+?)((?:channel)(\d+))?(?=(?=and|\+)|(?=except|-)|$)"
        matches = re.findall(reg, noWhite)
        if matches:
            for match in matches:
                add = True
                channel = -1
                name = match[3]
                if match[2] != "":  # Found an "except" modifier
                    add = False
                if match[4] != "": # Found a channel specificed
                    channel = int(match[5])

                print name

                group = self.get_channels_in_fixture(name)

                if len(group) == 0:
                    raise Exception("Fixture not found")

                toAct = set()
                if channel != -1:
                    try:
                        toAct = [ group[channel - 1] ]
                    except:
                        raise Exception("Channel not found in fixture")
                else:
                    toAct = group

                if add:
                    self.add(toAct)
                else:
                    self.remove(toAct)


    def get_group(self, name):
        for group in self.controller.groups:
            if group.name == name:
                return group

        return False

    def get_channels_in_fixture(self, fixture):
        group = []
        for channel in self.controller.patch.channels:
            if channel.fixture == fixture:
                group.append(channel.number)
        return group

    def get_channel_by_label(self, name):
        for channel in self.controller.patch.channels:
            if channel.label == name:
                return channel
        return False

    def add(self, array):
        self.adds.update(set(array))
        self.set.update(set(array))

    def remove(self, array):
        self.exps.update((set(array)))
        self.set -= set(array)
