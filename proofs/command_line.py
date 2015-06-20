__author__ = 'eric'
import re
from main.range_parser import RangeParser
from main.command_parser import CommandParser
from main.controller import Controller

channels = []
control = Controller()
command = CommandParser(control)

def main():

    pre_commands = []

    pre_commands.append( "patch channel 1 dmx 1 fixture led" )
    pre_commands.append( "patch channel 2 dmx 2 fixture led" )
    pre_commands.append( "patch channel 3 dmx 3 fixture led" )

    pre_commands.append( "1*100" )


    pre_commands.append( "save sequence test wait 1 fade 1 { 1/2 * 100 }" )
    pre_commands.append( "save sequence test wait 1 fade 1 { 1/2 * 0   } " )


    pre_commands.append( "print sequence test" )

    pre_commands.append( "load sequence test" )




    for cmd in pre_commands:
        print ">>> " + cmd
        runCommand(cmd)

    while cmd != "quit":
        cmd = raw_input(">>> ")
        runCommand(cmd)


def runCommand(strCommand):
    print command.parseCommand(strCommand)
    control.update(1)
    print control.patch.dmx
    print ""

main()