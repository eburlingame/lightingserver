__author__ = 'Eric Burlingame'
import os
from dmx_out import DmxOutput
from command_parser import CommandParser
from controller import Controller

controller = Controller()
command = CommandParser(controller)
dmxOut = DmxOutput(controller)

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def lighting_main():
    print "LightingServer starting..."

    wd = os.path.dirname(os.path.realpath(__file__))

    read_file(wd + "/start.txt")

    cmd = raw_input(">>> ")
    runCommand(cmd)
    while cmd != "quit":
        cmd = raw_input(">>> ")
        runCommand(cmd)


def runCommand(strCommand):
    try:
        print colors.OKGREEN
        print command.runCommand(strCommand)
    except Exception, e:
        print colors.WARNING
        print e.message
    finally:
        print colors.ENDC

def read_file(filepath):
    file = open(filepath, 'r')
    print "Loading file %s:" % file.name
    for line in file:
        if len(line) > 0 and line[0] != "#":
            print line
            runCommand(line)
        else:
            print colors.HEADER
            print line[1:] # print line without the comment
            print colors.ENDC

def write_file(filepath):
    toWrite = controller.to_commands()


lighting_main()