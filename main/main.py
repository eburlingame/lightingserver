__author__ = 'Eric Burlingame'
import os
import re
from dmx_out import DmxOutput
from command_parser import CommandParser
from controller import Controller

controller = Controller()
command = CommandParser(controller)
dmxOut = DmxOutput(controller)

wd = os.path.dirname(os.path.realpath(__file__))
startPath = wd + "/../start.txt"
dataPath = wd + "/../data.txt"


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

    read_file(startPath)

    while True:
        cmd = raw_input(">>> ")
        runCommand(cmd)


def runCommand(cmd):

    if re.match("quit", cmd):
      exit()
    elif re.match("read(.+)", cmd):
        match = re.match("read(.+)", cmd)
        read_file(match.group(1))
    elif re.match("read", cmd):
        read_file(dataPath)
    elif re.match("write(.+)", cmd):
        match = re.match("read(.+)", cmd)
        write_file(match.group(1))
    elif re.match("write", cmd):
        write_file(dataPath)
    else:
        try:
            print colors.OKGREEN + command.runCommand(cmd)
        except Exception, e:
            print colors.WARNING + e.message
        finally:
            print colors.ENDC

def read_file(filepath):
    try:
        file = open(filepath, 'r')
    except:
        print "File could not be opened"

    print "Loading file %s:" % file.name
    for line in file:
        noWhite = re.sub("\s", "", line)
        noWhite = re.sub("\n", "", noWhite)
        if noWhite != "":
            if len(noWhite) > 0 and noWhite[0] != "#":
                print line
                runCommand(line)
            else:
                print colors.HEADER + line[1:] + colors.ENDC # print line without the comment
    file.close()

def write_file(filepath):
    toWrite = controller.to_commands()
    file = open(filepath, 'w')
    file.write(toWrite)
    file.close()


lighting_main()