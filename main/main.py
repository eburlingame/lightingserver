__author__ = 'Eric Burlingame'

from dmx_out import DmxOutput
from command_parser import CommandParser
from controller import Controller

controller = Controller()
command = CommandParser(controller)
dmxOut = DmxOutput(controller.patch, 0.01)

def main():
    print "LightingServer starting..."

    pre_commands = []

    for i in range(1, 20):
        s = str(i)
        pre_commands.append( "patch channel " + s +" dmx " + s + " fixture led" )

    pre_commands.append("1 * 100")

    for cmd in pre_commands:
        print ">>> " + cmd
        runCommand(cmd)

    while cmd != "quit":
        cmd = raw_input(">>> ")
        runCommand(cmd)
        # dmxOut.run()


def runCommand(strCommand):
    print command.parseCommand(strCommand)
    controller.update()
    print controller.patch.dmx
    print ""


main()