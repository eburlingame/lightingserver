__author__ = 'eric'

from main.command_shortcut import *
from main.command_parser import *
from main.controller import *

short = CommandShortcut("#t#half", "[0] thru [1] at 50")
print short.pattern
print short.args_count
print short.replace("1t5hlf")

controller = Controller(None)
command = CommandParser(controller)
print command.split_by_brackets("this; is a test")
print command.split_by_brackets('{this is; s; s; a; s; }; {is a test}')
print command.split_by_brackets('define "bo" as "unload all; load scene bo"')
print command.split_by_brackets('this; is a test')