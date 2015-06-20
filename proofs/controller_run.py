__author__ = 'Eric Burlingame'

from main.controller import Controller
from main.channel_set import *

control = Controller()

control.patch_channel(1, 1)
control.patch_channel(2, 2)
control.patch_channel(3, 3)
control.patch_channel(4, 4)

print control.patch.dmx

set = ChannelSet(set([1, 2, 3, 4]))
control.at(set, 50)

control.update()

print control.patch.dmx