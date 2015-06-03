__author__ = 'eric'
import re
from main.rangeParser import RangeParser

channels = []

def main():
    cmd = "1/10-1/5"
    runCommand(cmd)

    while cmd != "quit":
        cmd = raw_input(">>>")
        runCommand(cmd)


def runCommand(strCommand):
    parser = RangeParser(strCommand)
    print("Result: " + parser.toString())


main()