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
              "(\s+)?(\d+)(\s+)?" + tokenThru + "(\s+)?(\d+)" # Regex pattern for through

    reg = tokenAnd + "?" + tokenExp + "?" + "(\d+)" + tokenThru +"?(\d+)?"

    raw = ""

    def parseAll(self):
        noWhite = re.sub("\s", "", self.raw) # remove whitespace
        all = re.findall(self.reg, noWhite) # find all patterns
        for m in all:
            add = True
            rng = [ int(m[2]) ]
            if m[1] != "": # Using an "execpt" keyword
                add = False
            if m[3] != "": # Using a "through" operator
                rng = range( int(m[2]), int(m[4]) + 1 )

            if add:
                self.add(rng)
            else:
                self.remove(rng)


    def parseThroughs(self):
        allThrus = re.findall(self.regThru, self.raw)
        for m in allThrus:
            subtract = (m[1] != "")
            frm = int(m[3])
            to = int(m[7])
            rng = range(frm, to + 1)
            if subtract:
                self.remove(rng)
            else:
                self.add(rng)
            self.raw = re.sub(self.regThru, "", self.raw) # Remove found token

    def parseAnds(self):
        allAnds = re.findall(self.regAnd, self.raw)
        for m in allAnds:
            self.add([ int(m[2]) ])
            self.raw = re.sub(self.regAnd, "", self.raw) # Remove found token

    def parseExcepts(self):
        allExps = re.findall(self.regExp, self.raw)
        for m in allExps:
            self.remove([ int(m[2]) ])
            self.raw = re.sub(self.regExp, "", self.raw) # Remove found token

    def addLast(self):
        m = re.match("(\d+)", self.raw)
        if m:
            val = int(m.group(1))
            self.add([ val ])


    def add(self, array):
        self.set.update(set(array))

    def remove(self, array):
        self.set -= set(array)

    def toString(self):
        toRet = ""
        for i in self.set:
            toRet += str(i) + " "
        return toRet

    def __init__(self, _raw):
        self.raw = _raw
        self.set = set()

        # self.parseThroughs()
        # self.parseAnds()
        # self.parseExcepts()
        # self.addLast()
        self.parseAll()
