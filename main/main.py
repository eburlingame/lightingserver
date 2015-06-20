__author__ = 'Eric Burlingame'

from dmx_out import DmxOutput
from command_parser import CommandParser
from controller import Controller

controller = Controller()
command = CommandParser(controller)
dmxOut = DmxOutput(controller, 0.05)

def lighting_main():
    print "LightingServer starting..."

    pre_commands = []

    for i in range(1, 20):
        s = str(i)
        pre_commands.append( "patch channel " + s +" dmx " + s + " fixture led" )

    pre_commands.append("save sequence test wait 0.5 fade 0.5 { 1 * 100}")
    pre_commands.append("save sequence test wait 0.5 fade 0.5 { 1 * 0  }")

    pre_commands.append("print sequence test")
    pre_commands.append("load sequence test")

    for cmd in pre_commands:
        print ">>> " + cmd
        runCommand(cmd)

    while cmd != "quit":
        cmd = raw_input(">>> ")
        runCommand(cmd)
        dmxOut.run()


def runCommand(strCommand):
    print command.parseCommand(strCommand)
    print controller.patch.dmx
    print ""


lighting_main()