__author__ = 'Eric Burlingame'
import os
import re

from output.dmx_out_serial import DmxOutput
from output.dummy_output import DummyOutput
from main.command_parser import CommandParser
from main.controller import Controller
from main.server import WSServer
# from main.rpc_server import *

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Main:

    def __init__(self):
        print "LightingServer starting..."
        self.controller = Controller(self)
        self.command = CommandParser(self.controller)
        self.dmxOut = DmxOutput(self.controller)
        # self.rpc = RPCServer(self)

        self.startPath = self.get_abs_path("start.txt")
        self.dataPath = self.get_abs_path("data.txt")

        self.read_file(self.startPath)

        while True:
            cmd = raw_input(">>> ")
            self.run_command(cmd)

    def run_command(self, cmd):
        response = self.parse_command(cmd)
        print response

    def run_server_command(self, cmd):
        response = self.parse_command(cmd, False)
        print response
        return response

    def parse_command(self, cmd, print_colors = True):
        noWhite = re.sub("\s", "", cmd).lower()

        if re.match("quit", noWhite):
          self.quit()

        elif re.match("read(.+)", noWhite):
            match = re.match("read(.+)", noWhite)
            return self.read_file(match.group(1))
        elif re.match("read", noWhite):
            return self.read_file(self.dataPath)

        elif re.match("write(.+)", noWhite):
            match = re.match("read(.+)", noWhite)
            return self.write_file(match.group(1))
        elif re.match("write", noWhite):
            return self.write_file(self.dataPath)

        elif re.match("startserver(\d+)", noWhite):
            match = re.match("startserver(\d+)", noWhite)
            return self.start_server(int(match.group(1)))
        elif re.match("startserver", noWhite):
            return self.start_server()

        elif re.match("open", noWhite):
            return self.open_interface()
        elif re.match("close", noWhite):
            return self.close_interface()

        else:
            return colors.OKGREEN + self.command.runCommand(cmd) + colors.ENDC
            try:
                if print_colors:
                    return colors.OKGREEN + self.command.runCommand(cmd) + colors.ENDC
                else:
                    return self.command.runCommand(cmd)
            except Exception, e:
                if print_colors:
                    return colors.WARNING + e.message + colors.ENDC
                else:
                    return e.message

    def get_abs_path(self, filepath):
        wd = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(wd, filepath)

    def read_file(self, filepath):
        try:
            file = open(filepath, 'r')
        except:
            return "File could not be opened"

        for line in file:
            noWhite = re.sub("\s", "", line)
            noWhite = re.sub("\n", "", noWhite)
            if noWhite != "":
                if len(noWhite) > 0 and noWhite[0] != "#":
                    print line
                    self.run_command(line)
                else:
                    print colors.HEADER + line[1:] + colors.ENDC # print line without the comment
        file.close()
        return "Loaded file %s:" % file.name

    def write_file(self, filepath):
        toWrite = self.controller.to_commands(self.command.shortcuts)
        file = open(filepath, 'w')
        file.write(toWrite)
        file.close()
        return "Wrote file %s " % filepath

    def start_server(self, port = 8080):
        server = WSServer(self, port)
        return "Server started on port %s" % server.port

    def open_interface(self):
        self.dmxOut = DmxOutput(self.controller)
        start = self.dmxOut.start()
        if start == "Could not open DMX output on serial port":
            self.dmxOut = DummyOutput(self.controller)
            return start + "\n" + self.dmxOut.start()

        return start

    def close_interface(self):
        return self.dmxOut.stop()

    def quit(self):
        self.write_file(self.dataPath)
        self.dmxOut.stop()
        quit(0)


main = Main()