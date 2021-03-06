__author__ = 'eric'
import re

class CommandShortcut:

    def __init__(self, shortcut, command):
        self.shortcut = shortcut
        self.command = command

        escaped = re.escape(self.shortcut)
        self.pattern = re.sub("\\\#", "(.+?)", escaped)
        self.args_count = self.shortcut.count('#')
        # print "Pattern %s" % self.pattern

    def replace(self, command):
        final = re.sub(self.pattern, self.command, command)
        match = re.match(self.pattern, command)
        if not match:
            return final

        args = match.groups()

        if len(args) != self.args_count:
            return "Arugment mismatch"

        for i in range(0, self.args_count):
            final = re.sub("\["+ str(i) + "\]", args[i], final)

        return final

    def to_command(self):
        return 'define "%s" as "%s"\n' % (self.shortcut, self.command)

    def to_string(self):
        return 'Shortcut: "%s" with command "%s"\n' % (self.shortcut, self.command)