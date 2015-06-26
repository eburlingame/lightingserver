__author__ = 'eric'

from main.command_shortcut import *

short = CommandShortcut("#t#half", "[0] thru [1] at 50")
print short.pattern
print short.args_count
print short.replace("1t5hlf")