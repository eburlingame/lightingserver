__author__ = 'Eric Burlingame'
import re
from dmx_out import DmxOutput
from command_parser import CommandParser
from controller import Controller

controller = Controller()
command = CommandParser(controller)
dmxOut = DmxOutput(controller)

def lighting_main():
    print "LightingServer starting..."

    print "Loading start file:"
    start_file = open('start.txt', 'w')
    for line in start_file:
        print line
        runCommand(line)


    while cmd != "quit":
        cmd = raw_input(">>> ")
        runCommand(cmd)


def runCommand(strCommand):
    print command.runCommand(strCommand)
    print controller.patch.dmx
    print ""


lighting_main()