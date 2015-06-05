__author__ = 'eric'

import re
from range_parser import RangeParser

class ChannelRangeParser:
    """
        The goal of this class is to parse fixture labels and group names before parsing the standard
        numeric channel ranges (like 1 thru 10)
    """

    tokenAnd        = "(and|\+)"
    tokenExp        = "(except|-)"
    tokenThru       = "(\/|thru|through)"

    tokenPre        = tokenAnd + "?" + tokenExp + "?"

    tokenAndLook    = "(?=and|\+)"
    tokenExpLook    = "(?=except|-)"
    tokenThruLook   = "(?=\/|thru|through)"

    regGroup = "group.+"

    def __init__(self, raw):
        self.raw = raw
        self.set = set()

    def parse(self):
        noWhite = re.sub("\s", "", self.raw) # remove whitespace
        noWhite = noWhite.lower()



    def match_groups(self, noWhite):
        reg = self.tokenPre + self.regGroup + self.tokenAndLook

