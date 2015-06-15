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

    pre_commands.append( "1/3 * 100" )
    # pre_commands.append( " at 0" )

    pre_commands.append( "save group test " )
    pre_commands.append( "save group test {1/3}" )
    pre_commands.append( "save group test2 {1/2}" )
    pre_commands.append( "list groups" )

    pre_commands.append( "save scene test " )

    pre_commands.append( "list scenes " )

    pre_commands.append( "save scene test channel 1/2 " )

    pre_commands.append( "save scene test { 1/3 at 100 } " )

    pre_commands.append( "list scenes " )




    for cmd in pre_commands:
        print ">>> " + cmd
        runCommand(cmd)

    while cmd != "quit":
        cmd = raw_input(">>> ")
        runCommand(cmd)


def runCommand(strCommand):
    print command.parseCommand(strCommand)
    control.update()
    print control.patch.dmx
    print ""

main()