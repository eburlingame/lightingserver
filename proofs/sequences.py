__author__ = 'eric'

from main.controller import Controller
from main.channel_set import *

controller = Controller()

print controller.patch_channel(1, 1)
print controller.patch_channel(2, 2)
print controller.patch_channel(3, 3)

print controller.at(ChannelState(controller, "1 at 100"))

print controller.save_sequence("Test")
print controller.save_sequence("Test")
print controller.save_sequence("Test")

print controller.list_sequences()

print controller.print_sequence("Test")

