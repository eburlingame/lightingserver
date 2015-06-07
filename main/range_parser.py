__author__ = 'eric'

import re

class RangeParser(object):
    tokenAnd    = "(and|\+)"
    tokenExp    = "(except|-)"
    tokenThru   = "(\/|thru|through)"

    regAnd  = tokenAnd + "(\s+)?(\d+)" # Regex pattern for and
    regExp  = tokenExp + "(\s+)?(\d+)" # Regex pattern for or
    regThru = tokenAnd + "?" + \
              tokenExp + "?" + \
              "(\d+)" + tokenThru + "(\d+)" # Regex pattern for through

    # ((and|\+)|(except|-)|^)(\d+)(\/|thru|through)?(\d+)?
    reg = "(%s|%s|^)(\d+)%s?(\d+)?" % (tokenAnd, tokenExp, tokenThru)

    raw = ""

    def parseAll(self):
        noWhite = re.sub("\s", "", self.raw) # remove whitespace
        noWhite = noWhite.lower()
        all = re.findall(self.reg, noWhite) # find all patterns
        for m in all:
            add = True
            rng = [ int(m[3]) ]
            if m[2] != "": # Using an "except" keyword
                add = False
            if m[4] != "": # Using a "through" operator
                rng = range( int(m[3]), int(m[5]) + 1 ) # Inclusive range

            if add:
                self.add(rng)
            else:
                self.remove(rng)

        self.removed = re.sub(self.reg, "", noWhite)

    def add(self, array):
        self.adds.update(set(array))
        self.set.update(set(array))

    def remove(self, array):
        self.exps.update(set(array))
        self.set -= set(array)

    def toString(self):
        toRet = ""
        for i in self.set:
            toRet += str(i) + " "
        return toRet

    def __init__(self, _raw):
        self.raw = _raw
        self.set  = set() # Holds the net channels set
        self.adds = set() # Holds what channels have been added to the set
        self.exps = set() # Holds what channels have been subtracted from the set
        self.removed = "" # Holds the raw commands with the numerical commands (e.g. 1/3) removed
        self.parseAll()
