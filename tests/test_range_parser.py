__author__ = 'eric'

import unittest

from main.rangeParser import RangeParser

class RangerParserTest(unittest.TestCase):

    def check_set(self, command, list):
        parser = RangeParser(command)
        rng = parser.captureRange
        self.assertSetEqual(set(list), rng, command + " not equal")

    def test_through(self):
        self.check_set("1/5", [1,2,3,4,5])
        self.check_set("1/1", [1])
        self.check_set("1/2+3/4", [1,2,3,4])
        self.check_set("1/10-1/5", [6, 7, 8, 9, 10])
        self.check_set("1/5-6/10", [1,2,3,4,5])

        self.check_set("1 thru 5", [1,2,3,4,5])
        self.check_set("1 thru 1", [1])
        self.check_set("1 thru 2+3 through 4", [1,2,3,4])
        self.check_set("1 thru 10-1 through 5", [6, 7, 8, 9, 10])
        self.check_set("1 thru 5-6 through 10", [1,2,3,4,5])

    def test_and(self):
        # self.check_set("1+5", [1, 5])
        self.check_set("1+1", [1])
        self.check_set("1+2+3+4", [1,2,3,4])
        self.check_set("1+10-1+5", [5, 10])
        self.check_set("1/2+11+12", [1,2,11,12])

        self.check_set("1 and 1", [1])
        self.check_set("1 and 2 and 3 and 4", [1,2,3,4])
        self.check_set("1 and 10 except 1 and 5", [5, 10])
        self.check_set("1 thru 2 and 11 and 12", [1,2,11,12])



if __name__ == '__main__':
    unittest.main()
